# Quantumult X Rules Generator

自動同步 [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) 專案中的成人網站規則（`category-porn`），並自動轉換為適用於 Quantumult X 的分流片段檔 (`.snippets`)。

藉由 GitHub Actions，每日定時抓取最新資料庫並自動進行轉換與部署。

---

## 📁 專案結構

```text
.
├── .github/
│   └── workflows/
│       └── update.yml     # GitHub Actions 自動排程更新
├── scripts/
│   └── convert.py         # 規則解析與語法轉換腳本
├── rules/
│   └── porn.snippets      # 轉換後的 Quantumult X 分流規則檔
└── README.md              # 專案說明文件
