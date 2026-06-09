"""Tests for Markdown preserver."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from linguaflow.markdown import MarkdownPreserver


def test_preserve_code_block():
    content = "Hello\n```python\nprint('hello')\n```\nWorld"
    p = MarkdownPreserver(content)
    protected = p.protect()
    assert "print('hello')" not in protected, "Code block should be replaced"
    assert "__LF_CODE_" in protected, "Placeholder should exist"
    restored = p.restore(protected)
    assert restored == content, f"Round-trip failed:\n{restored!r} != \n{content!r}"


def test_preserve_inline_code():
    content = "Use the `os.path.join()` function."
    p = MarkdownPreserver(content)
    protected = p.protect()
    assert "os.path.join" not in protected, "Inline code should be replaced"
    restored = p.restore(protected)
    assert restored == content


def test_preserve_image():
    content = "![Logo](/images/logo.png)"
    p = MarkdownPreserver(content)
    protected = p.protect()
    assert "/images/logo.png" not in protected
    restored = p.restore(protected)
    assert restored == content


def test_preserve_complex_markdown():
    content = """# Title

This is a paragraph with `inline code`.

```bash
echo "hello"
```

And a [link](https://example.com) with an image: ![icon](icon.png)

| Col1 | Col2 |
|------|------|
| A    | B    |
"""
    p = MarkdownPreserver(content)
    protected = p.protect()
    restored = p.restore(protected)
    assert restored == content


def test_empty_content():
    p = MarkdownPreserver("")
    assert p.protect() == ""
    assert p.restore("") == ""


def test_no_code_blocks():
    content = "Just plain text with no special formatting."
    p = MarkdownPreserver(content)
    protected = p.protect()
    assert protected == content


def test_stats():
    content = "A `inline` and ```block``` and ![img](x.png)"
    p = MarkdownPreserver(content)
    p.protect()
    stats = p.get_stats()
    assert stats["protected_items"] == 3
    assert stats["code_blocks"] == 1
    assert stats["inline_code"] == 1
    assert stats["images"] == 1


def test_multiple_code_blocks():
    content = "```a\n1\n```\nText\n```b\n2\n```"
    p = MarkdownPreserver(content)
    protected = p.protect()
    assert protected.count("__LF_CODE_") == 2
    restored = p.restore(protected)
    assert restored == content