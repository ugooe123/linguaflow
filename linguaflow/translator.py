"""AI Translation Engine - works with any OpenAI-compatible API."""

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import requests

from .config import load_global_config, get_api_key

LANGUAGE_NAMES = {
    "zh-CN": "Simplified Chinese",
    "zh-TW": "Traditional Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pt-BR": "Brazilian Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "th": "Thai",
    "id": "Indonesian",
    "hi": "Hindi",
    "it": "Italian",
    "nl": "Dutch",
    "pl": "Polish",
    "uk": "Ukrainian",
    "en": "English",
}

BATCH_SYSTEM_PROMPT = """You are a professional technical document translator.
Translate the following Markdown content from {source_lang} to {target_lang}.
Rules:
1. Preserve ALL Markdown formatting exactly: code blocks ```, inline code ``, headings ##, links [...](...), images ![alt](url), tables, lists, bold **, italic *, etc.
2. Do NOT translate content inside code blocks or inline code - these are code.
3. Do NOT change URLs or file paths.
4. Keep technical terms accurate (API, CLI, SDK, JSON, etc. stay as-is).
5. Maintain the original heading hierarchy.
6. Return ONLY the translated Markdown, nothing else."""


class TranslationError(Exception):
    pass


def translate_batch(
    content: str,
    target_langs: list[str],
    source_lang: str = "en",
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_workers: int = 3,
) -> dict[str, str]:
    """Translate content into multiple languages in parallel."""
    cfg = load_global_config()
    api_key = get_api_key()
    if not api_key:
        raise TranslationError(
            "No API key found. Set LINGUAFLOW_API_KEY, OPENAI_API_KEY, "
            "or run 'linguaflow config set api_key YOUR_KEY'"
        )

    model = model or cfg.get("model", "gpt-4o-mini")
    temperature = temperature if temperature is not None else cfg.get("temperature", 0.3)
    api_base = cfg.get("api_base", "https://api.openai.com/v1")
    max_retries = cfg.get("max_retries", 3)

    results = {}

    def translate_one(lang: str) -> tuple[str, str]:
        lang_name = LANGUAGE_NAMES.get(lang, lang)
        source_name = LANGUAGE_NAMES.get(source_lang, source_lang)

        messages = [
            {
                "role": "system",
                "content": BATCH_SYSTEM_PROMPT.format(
                    source_lang=source_name, target_lang=lang_name
                ),
            },
            {"role": "user", "content": content},
        ]

        for attempt in range(max_retries):
            try:
                resp = requests.post(
                    f"{api_base.rstrip('/')}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                    },
                    timeout=120,
                )
                resp.raise_for_status()
                data = resp.json()
                translated = data["choices"][0]["message"]["content"]
                return lang, translated.strip()
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise TranslationError(
                        f"Failed to translate to {lang} after {max_retries} retries: {e}"
                    )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(translate_one, lang): lang for lang in target_langs}
        for future in as_completed(futures):
            lang, text = future.result()
            results[lang] = text

    return results


def translate(
    content: str,
    target_lang: str,
    source_lang: str = "en",
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> str:
    """Translate content to a single language."""
    results = translate_batch(content, [target_lang], source_lang, model, temperature)
    return results[target_lang]