"""Markdown parser that preserves structure during translation."""

import re
from typing import Optional


class MarkdownPreserver:
    """Extracts and protects code blocks, inline code, and URLs during translation."""

    PLACEHOLDER_TEMPLATE = "__LF_CODE_{idx}__"

    def __init__(self, content: str):
        self.original = content
        self.protected: dict[str, str] = {}
        self._processed: Optional[str] = None

    def protect(self) -> str:
        """Replace code blocks and inline code with placeholders."""
        text = self.original

        # Protect fenced code blocks (```...```)
        def _protect_block(m):
            idx = len(self.protected)
            ph = self.PLACEHOLDER_TEMPLATE.format(idx=idx)
            self.protected[ph] = m.group(0)
            return ph

        text = re.sub(r"```[\s\S]*?```", _protect_block, text)

        # Protect inline code (`code`)
        def _protect_inline(m):
            idx = len(self.protected)
            ph = self.PLACEHOLDER_TEMPLATE.format(idx=idx)
            self.protected[ph] = m.group(0)
            return ph

        text = re.sub(r"`[^`\n]+`", _protect_inline, text)

        # Protect image references
        def _protect_image(m):
            idx = len(self.protected)
            ph = self.PLACEHOLDER_TEMPLATE.format(idx=idx)
            self.protected[ph] = m.group(0)
            return ph

        text = re.sub(r"!\[.*?\]\(.*?\)", _protect_image, text)

        self._processed = text
        return text

    def restore(self, text: str) -> str:
        """Restore placeholders back to original protected content."""
        for ph, original in self.protected.items():
            text = text.replace(ph, original)
        return text

    def get_stats(self) -> dict:
        return {
            "protected_items": len(self.protected),
            "code_blocks": sum(1 for v in self.protected.values() if v.startswith("```")),
            "inline_code": sum(
                1 for v in self.protected.values()
                if v.startswith("`") and not v.startswith("```")
            ),
            "images": sum(1 for v in self.protected.values() if v.startswith("![")),
            "original_length": len(self.original),
        }


def add_language_badge(lang_code: str, lang_name: str) -> str:
    """Generate a shield.io badge for a language."""
    return (
        f"[![{lang_name}](https://img.shields.io/badge/{lang_code}-{lang_name.replace(' ', '%20')}-blue)]"
        f"(README-{lang_code.upper()}.md)"
    )