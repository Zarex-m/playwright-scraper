# Playwright Quote Scraper · Playwright 动态网页爬虫

A production-style Python scraper built on **Playwright**, crawling both the static and the **JavaScript-rendered** versions of [quotes.toscrape.com](https://quotes.toscrape.com) (a public practice site), following pagination to the end, and exporting clean CSV / JSON.

一个基于 **Playwright** 的工程化 Python 爬虫：可抓取 [quotes.toscrape.com](https://quotes.toscrape.com)（公开练习站）的静态页和 **JS 动态渲染页**，自动翻页，导出干净的 CSV / JSON。

## Features · 功能

| English | 中文 |
|---|---|
| Real headless Chromium, handles JS-rendered content | 真实无头浏览器，支持 JS 动态渲染页面 |
| Automatic pagination (or `--max-pages` limit) | 自动翻页，可用 `--max-pages` 限制页数 |
| Retries with exponential backoff | 失败自动重试，指数退避 |
| Rate limiting (polite crawling) | 请求限速，友好抓取 |
| CSV (Excel-friendly UTF-8 BOM) + JSON export | 导出 CSV（Excel 直接打开不乱码）和 JSON |
| JSON config file + CLI overrides | JSON 配置文件 + 命令行参数覆盖 |
| Structured logging to console / file | 日志输出到终端和文件 |
| pytest suite: unit, offline browser, live tests | pytest 测试：单元、离线浏览器、线上集成 |

## Quick start · 快速开始

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
playwright install chromium

quote-scraper                                   # JS pages, all pages, CSV+JSON → output/
quote-scraper --mode static --max-pages 3 --delay 0.5
quote-scraper --config config.example.json --format json --log-file run.log
python -m quote_scraper --headed                # watch the browser / 显示浏览器窗口
```

### CLI options · 参数

| Option | Description · 说明 |
|---|---|
| `--mode js\|static` | JS-rendered `/js/` or static `/` · 动态页或静态页 |
| `--max-pages N` | Page limit, 0 = all · 最大页数，0 表示全部 |
| `--delay S` | Seconds between requests · 请求间隔（秒） |
| `--retries N` | Retries per page · 每页重试次数 |
| `--output-dir DIR` | Output folder · 输出目录 |
| `--format csv\|json` | Repeatable · 可重复指定 |
| `--config FILE` | JSON config · 配置文件 |
| `--log-level`, `--log-file`, `--headed` | Logging / browser window · 日志与浏览器窗口 |

## Sample output · 示例输出

Full run (10 pages, 100 quotes) in [`sample_output/`](sample_output/) · 完整运行结果见 `sample_output/`。

```json
{
  "text": "The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.",
  "author": "Albert Einstein",
  "tags": ["change", "deep-thoughts", "thinking", "world"],
  "page": 1,
  "source_url": "https://quotes.toscrape.com/js/"
}
```

```
INFO quote_scraper.scraper: Fetching page 10: https://quotes.toscrape.com/js/page/10/
INFO quote_scraper.scraper: Done: 100 quotes from 10 pages
```

## Tests · 测试

```bash
pytest -q                 # 11 tests (includes live-site tests)
SKIP_NETWORK=1 pytest -q  # offline only · 仅离线测试
```

## Project layout · 目录结构

```
src/quote_scraper/  cli.py  config.py  scraper.py  exporters.py  utils.py
tests/              test_utils.py  test_config_export.py  test_parse.py  test_live.py
sample_output/      quotes.csv  quotes.json  run_log.txt
```

## What I can build for you · 我能为你做什么

- **Web scraping & data collection** — dynamic/JS sites, login flows, pagination, scheduled crawls, export to Excel/CSV/DB.
  **网页爬虫与数据采集**：动态网站、登录、翻页、定时抓取，导出 Excel / CSV / 数据库。
- **Automation scripts** — browser automation, form filling, report generation, file/Excel processing.
  **自动化脚本**：浏览器自动化、表单填写、报表生成、文件与 Excel 批处理。
- **APIs & backends** — FastAPI services, data pipelines, deployment with Docker.
  **接口与后端**：FastAPI 服务、数据管道、Docker 部署。
- **AI integration** — LLM chatbots, RAG knowledge bases, agents that use your data.
  **AI 集成**：大模型聊天机器人、RAG 知识库问答、智能体。

Clean, tested, documented code delivered fast. I only take projects that respect site terms and the law.
交付快、代码规范、带测试与文档。仅承接合法合规、遵守网站条款的项目。

📫 GitHub: [@Zarex-m](https://github.com/Zarex-m)

## License

MIT
