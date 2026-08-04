# Quantumult X Rules Generator

自動同步 [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) 專案中的分類規則，並自動轉換為適用於 Quantumult X 的分流片段檔 (`.snippets`)。

透過 GitHub Actions，每日定時抓取上游最新資料庫並自動完成解析、轉換與部署。

---

## 📁 專案結構

```text
.
├── .github/
│   └── workflows/
│       └── update.yml        # GitHub Actions 自動排程更新
├── scripts/
│   ├── convert_porn.py       # 成人網站規則轉換腳本 (category-porn)
│   └── convert_ai.py         # AI 服務規則轉換腳本 (category-ai-!cn)
├── rules/
│   ├── porn.snippets         # 轉換後的 QX Porn 分流規則
│   └── ai.snippets           # 轉換後的 QX AI 分流規則
└── README.md                 # 專案說明文件
