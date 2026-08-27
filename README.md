# Quantumult X Rules Generator

自動同步 [v2fly/domain-list-community](https://github.com/v2fly/domain-list-community) 專案中的分類規則，並自動轉換為適用於 Quantumult X 的分流片段檔 (`.snippets`)。

藉由 GitHub Actions 排程，每日自動抓取上游最新資料庫完成解析、轉譯與部署。

---

## 📌 最新更新狀態

* **最後自動同步時間**： 2026-08-27 16:01:02
* **自動更新機制**：每日 UTC 00:00（台灣時間 08:00）透過 GitHub Actions 自動比對與更新。

---

## 📁 專案結構

```text
.
├── .github/
│   └── workflows/
│       └── update.yml        # GitHub Actions 自動排程與 README 時間戳記更新
├── scripts/
│   ├── convert_porn.py       # 成人網站規則轉換腳本 (上游來源：category-porn)
│   └── convert_ai.py         # AI 服務規則轉換腳本 (上游來源：category-ai-!cn)
├── rules/
│   ├── porn.snippets         # 轉換後的 QX Porn 分流規則檔
│   └── ai.snippets           # 轉換後的 QX AI 分流規則檔
└── README.md                 # 專案說明文件
