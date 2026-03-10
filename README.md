# Python Crawler Template / Python 爬虫工具包

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready Python web scraping template with dual framework support (Scrapy & Requests), built-in anti-scraping strategies, and multi-storage backends.

一个生产级的 Python 网络爬虫模板，支持 Scrapy 和 Requests 双框架切换，内置反爬策略和多数据存储后端。

---

## 🌟 Features / 项目特色

- **Dual Framework Support** - Switch between Scrapy and Requests easily
- **Anti-Scraping Built-in** - UA pool, proxy rotation, randomized delays
- **Multi-Storage Backends** - CSV, Excel, MySQL, MongoDB
- **Production Ready** - Configuration files, error handling, logging
- **Well Documented** - Bilingual README, runnable examples

---

## 🚀 Quick Start / 快速开始

### Installation / 安装

```bash
git clone https://github.com/martin00000/python-crawler-template.git
cd python-crawler-template
pip install -r requirements.txt
pip install -e .
```

### Basic Usage / 基础用法

```python
from src import BaseScraper

# Create a simple scraper
scraper = BaseScraper(url="https://example.com")
data = scraper.fetch()

# Save to CSV
scraper.save("output.csv")
```

---

## 📖 Documentation / 文档

### API Reference / API 参考

#### BaseScraper / 基础爬虫类

| Method | Description / 描述 |
|--------|-------------------|
| `fetch()` | Fetch page content / 抓取页面内容 |
| `parse(response)` | Parse response data / 解析响应数据 |
| `save(filename, format)` | Save to file / 保存到文件 |

#### Utils / 工具函数

- `get_user_agents()` - Get random user agent / 获取随机 UA
- `get_proxy()` - Get available proxy / 获取可用代理
- `random_delay(min, max)` - Random sleep / 随机延时

---

## 📝 Examples / 示例

See the `examples/` directory for more:

- `simple_scraper.py` - Basic usage / 基础用法
- `pagination_scraper.py` - Multi-page scraping / 分页爬取
- `login_scraper.py` - With authentication / 登录验证

### Running Examples / 运行示例

```bash
cd examples
python simple_scraper.py
```

---

## 🔧 Configuration / 配置

Edit `config.yaml` to customize:

```yaml
# config.yaml
settings:
  delay_between_requests: 1.0
  max_retries: 3
  
proxies:
  enabled: true
  rotation_interval: 10
  
storage:
  default_format: csv
  output_dir: ./outputs
```

---

## 🧪 Testing / 测试

```bash
pytest tests/ -v
```

---

## 📄 License / 授权

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🤝 Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。

---

## 📧 Contact / 联系

alan - dingying02@gmail.com

Project Link: https://github.com/martin00000/python-crawler-template
