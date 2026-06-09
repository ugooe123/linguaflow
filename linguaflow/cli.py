"""linguaflow CLI - AI-powered documentation translation."""

import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from . import __version__, __title__, __description__
from .config import (
    load_global_config,
    save_global_config,
    load_project_config,
    save_project_config,
    get_api_key,
    DEFAULT_CONFIG,
)
from .translator import translate_batch, translate, LANGUAGE_NAMES, TranslationError
from .markdown import MarkdownPreserver, add_language_badge

app = typer.Typer(
    name=__title__,
    help=__description__,
    no_args_is_help=True,
)
console = Console()

LANGUAGE_CHOICES = list(LANGUAGE_NAMES.keys())


@app.callback()
def callback():
    """linguaflow - AI-powered documentation translation."""


@app.command(name="translate")
def translate(
    path: str = typer.Argument(".", help="Path to file or directory to translate"),
    languages: str = typer.Option(
        "", "-l", "--languages",
        help="Target languages (comma-separated, e.g., zh-CN,ja,ko)",
    ),
    output_dir: str = typer.Option(
        "", "-o", "--output",
        help="Output directory (default: alongside original files)",
    ),
    model: Optional[str] = typer.Option(
        None, "-m", "--model",
        help="AI model to use (default: from config)",
    ),
):
    """\n    Translate documentation to multiple languages.\n    """
    path = Path(path)

    # Determine languages
    langs = [l.strip() for l in languages.split(",") if l.strip()] if languages else []
    if not langs:
        cfg = load_global_config()
        langs = cfg.get("target_languages", DEFAULT_CONFIG["target_languages"])

    # Identify files to translate
    files = []
    if path.is_file():
        files = [path]
    elif path.is_dir():
        for pattern in ["README.md", "*.md", "docs/*.md", "docs/**/*.md"]:
            found = list(path.glob(pattern))
            files.extend(found)
        files = list(set(files))  # deduplicate

    if not files:
        console.print("[red]No markdown files found to translate.[/]")
        raise typer.Exit(1)

    # Check API key
    if not get_api_key():
        console.print("[red]No API key configured![/]")
        console.print("Set it with: linguaflow config set api_key YOUR_KEY")
        console.print("Or set the LINGUAFLOW_API_KEY or OPENAI_API_KEY environment variable.")
        raise typer.Exit(1)

    console.print(f"\n[bold]linguaflow[/] v{__version__}")
    console.print(f"Files to translate: {len(files)}")
    console.print(f"Target languages: [green]{', '.join(langs)}[/]")
    console.print()

    total_translations = 0

    for file_path in files:
        rel_path = file_path.relative_to(path) if path.is_dir() else file_path.name
        console.print(f"\n[bold]濡絽鍟幆?{rel_path}[/]")

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        if not source.strip():
            console.print("  [yellow]Empty file, skipping[/]")
            continue

        # Preserve Markdown structure
        preserver = MarkdownPreserver(source)
        protected_text = preserver.protect()
        stats = preserver.get_stats()
        if stats["protected_items"] > 0:
            console.print(
                f"  Protected: {stats['code_blocks']} code blocks, "
                f"{stats['inline_code']} inline codes, {stats['images']} images"
            )

        # Translate
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"Translating to {len(langs)} languages...", total=len(langs)
            )

            try:
                results = translate_batch(protected_text, langs)
                progress.update(task, completed=len(langs))
            except TranslationError as e:
                console.print(f"  [red]Error: {e}[/]")
                continue

        # Write translations
        for lang, translated_text in results.items():
            # Restore protected content
            final_text = preserver.restore(translated_text)

            # Determine output path
            if output_dir:
                out_dir = Path(output_dir)
            else:
                out_dir = file_path.parent

            out_dir.mkdir(parents=True, exist_ok=True)

            stem = file_path.stem
            suffix = file_path.suffix
            out_path = out_dir / f"{stem}.{lang}{suffix}"

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(final_text)

            lang_name = LANGUAGE_NAMES.get(lang, lang)
            console.print(f"  [green]闂佺繝鐒﹁ぐ?] {lang_name} ({lang}) 闂?{out_path.name}")
            total_translations += 1

    console.print(f"\n[bold green]Done![/] {total_translations} translations created.")

    # Suggest badges
    if total_translations > 0:
        console.print("\n[dim]Add these badges to your README:[/]")
        for lang in langs:
            lang_name = LANGUAGE_NAMES.get(lang, lang)
            badge = add_language_badge(lang, lang_name)
            console.print(f"  {badge}")


@app.command()
def init():
    """Initialize linguaflow for your project."""
    cfg = load_project_config()
    if cfg:
        console.print("[yellow]Project already configured.[/]")
        return

    cfg = {
        "source_readme": "README.md",
        "languages": ["zh-CN", "ja", "ko", "es"],
        "output_dir": ".",
    }
    save_project_config(cfg)
    console.print("[green]闂佺繝鐒﹁ぐ?] Created .linguaflow.json")
    console.print("\nNext steps:")
    console.print("  1. Set your API key: linguaflow config set api_key YOUR_KEY")
    console.print("  2. Translate: linguaflow translate")


@app.command()
def config(
    key: Optional[str] = typer.Option(None, "-k", "--key", help="Config key to set"),
    value: Optional[str] = typer.Option(None, "-v", "--value", help="Config value"),
    show: bool = typer.Option(False, "--show", help="Show current config"),
):
    """Manage linguaflow configuration."""
    cfg = load_global_config()

    if show:
        table = Table(title="Global Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")
        for k, v in cfg.items():
            if k == "api_key" and v:
                v = v[:12] + "..." + v[-4:]
            table.add_row(k, str(v))
        console.print(table)
        return

    if key and value:
        cfg[key] = value
        save_global_config(cfg)
        console.print(f"[green]闂佺繝鐒﹁ぐ?] Set {key} = {value}")
        return

    console.print("Usage: linguaflow config --show | --key KEY --value VALUE")


@app.command()
def detect(
    path: str = typer.Argument(".", help="Path to check"),
):
    """Detect translation files in a project."""
    path = Path(path)
    readme = path / "README.md"
    if not readme.exists():
        console.print("[yellow]No README.md found at this path.[/]")
        return

    # Check for translation files
    translations = {}
    for f in path.glob("README.*.md"):
        parts = f.stem.split(".")
        if len(parts) >= 2:
            lang_code = parts[-1]
            if lang_code in LANGUAGE_NAMES:
                translations[lang_code] = f.name

    if translations:
        table = Table(title="Existing Translations")
        table.add_column("Language", style="cyan")
        table.add_column("Code", style="green")
        table.add_column("File")
        for code, filename in sorted(translations.items()):
            table.add_row(LANGUAGE_NAMES.get(code, code), code, filename)
        console.print(table)
    else:
        console.print("No translations found. Try: linguaflow translate README.md -l zh-CN,ja,ko")

    return translations


@app.command()
def version():
    """Show version information."""
    console.print(f"[bold]{__title__}[/] v{__version__}")
    console.print(__description__)


def main():
    app()
