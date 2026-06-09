# linguaflow 🌊

> **AI-powered documentation translation that understands context.**
> Translate your README and docs to 20+ languages in one command.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/ugooe123/linguaflow?style=social)](https://github.com/ugooe123/linguaflow)

## Why linguaflow?

**95% of open-source projects are English-only.** That means billions of developers who don't speak English can't fully participate. Machine translation (Google Translate, DeepL) is word-for-word and destroys technical meaning. Manual translation is too much work to maintain.

**linguaflow solves this** by using AI that understands context:

| Feature | Google Translate | linguaflow |
|---------|:-:|:-:|
| Preserves code blocks | ❌ | ✅ |
| Preserves inline code `like this` | ❌ | ✅ |
| Preserves URLs and links | ❌ | ✅ |
| Understands technical terminology | ❌ | ✅ |
| Maintains Markdown formatting | ❌ | ✅ |
| Batch translates to multiple languages | ❌ | ✅ |

## Quick Start

```bash
# Install
pip install linguaflow

# Set your API key
export LINGUAFLOW_API_KEY=your-key

# Translate your README to Chinese, Japanese, and Korean
linguaflow translate README.md -l zh-CN,ja,ko

# Or translate an entire project
linguaflow translate . -l zh-CN,ja,ko,es,pt-BR
```

## How It Works

```
README.md
  │
  ▼
┌─────────────┐
│ Markdown    │  Preserves ```code```, `inline`, [links],
│ Preserver   │  ![images], tables, headings
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ AI Engine   │  Understands technical context, translates
│ (GPT-4o)    │  naturally while keeping accuracy
└──────┬──────┘
       │
       ▼
README.zh-CN.md  README.ja.md  README.ko.md  ...
```

## Features

### 🎯 Context-Aware Translation
Not word-for-word. AI understands the technical context and translates naturally while keeping terminology accurate.

### 🔒 Markdown Preservation
Code blocks, inline code, URLs, images, tables, headings — all preserved perfectly.

### ⚡ Batch Translation
Translate to 10+ languages in parallel. One command, done.

### 🏷️ Auto Badges
Get ready-to-use language badges for your README.

## Commands

```bash
# Translate a file
linguaflow translate README.md -l zh-CN,ja,ko

# Translate a whole project
linguaflow translate . -l zh-CN,ja,ko,fr,de,es,pt-BR

# Initialize project config
linguaflow init

# Check existing translations
linguaflow detect

# Configure API key
linguaflow config set api_key YOUR_KEY

# View config
linguaflow config --show

# Version
linguaflow version
```

## Configuration

| Method | Example |
|--------|---------|
| Environment variable | `export LINGUAFLOW_API_KEY=sk-...` |
| `linguaflow config` | `linguaflow config set api_key sk-...` |
| Project config | `.linguaflow.json` in your project root |

### Supported Providers

linguaflow works with any OpenAI-compatible API:

```bash
# OpenAI
export LINGUAFLOW_API_KEY=sk-...

# DeepSeek (cheaper, great for translation)
linguaflow config set api_base https://api.deepseek.com/v1
linguaflow config set model deepseek-chat

# Any OpenAI-compatible endpoint
linguaflow config set api_base https://your-proxy.com/v1
```

## Use Cases

### 🌟 Open Source Maintainers
Make your project accessible to the 70% of developers who aren't native English speakers. Get more users, contributors, and stars.

### 📚 Documentation Teams
Keep multi-language docs in sync. Translate once, review, done.

### 🚀 Indie Hackers / SaaS
Localize your documentation for international markets without hiring translators.

## Roadmap

- [x] CLI translation tool
- [x] Markdown structure preservation
- [x] Batch multi-language translation
- [ ] GitHub Action for CI/CD auto-translation
- [ ] Quality scoring per language
- [ ] Custom glossary for technical terms
- [ ] Web UI for non-technical users
- [ ] Translation memory (don't re-translate unchanged sections)

## How You Can Help

- ⭐ Star the repo — it helps others find it
- 🐛 Report bugs or suggest features
- 🌍 Add support for more languages
- 💖 [Sponsor the project](https://github.com/sponsors/ugooe123) to keep it growing

## License

MIT