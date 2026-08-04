import os
import urllib.request
import re

BASE_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/"
TARGET_CATEGORY = "category-ai-!cn"

OUTPUT_DIR = "rules"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ai.snippets")
POLICY_NAME = "AI"

visited_files = set()
parsed_rules = set()
manual_regex = []

KEYWORD_EXTRACTOR = re.compile(r'([a-zA-Z0-9\-]{4,})')

def fetch_and_parse(filename):
    if filename in visited_files:
        return
    visited_files.add(filename)

    url = BASE_URL + filename
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode('utf-8').splitlines()
    except Exception as e:
        print(f"無法下載 {filename}: {e}")
        return

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # 清除 @cn, @ads 等屬性標籤與尾端註解
        line = line.split('@')[0].split('#')[0].strip()
        if not line:
            continue

        # 1. 處理 include: 遞迴引用
        if line.startswith("include:"):
            include_target = line.replace("include:", "").strip()
            fetch_and_parse(include_target)
            continue

        # 2. 處理 regexp: (提取核心關鍵字)
        if line.startswith("regexp:"):
            reg_expr = line.replace("regexp:", "").strip()
            matches = KEYWORD_EXTRACTOR.findall(reg_expr)
            ignored_tlds = {'com', 'net', 'org', 'xyz', 'info', 'buzz', 'top', 'life', 'icu', 'one', 'ai', 'io'}
            valid_kw = [m for m in matches if m.lower() not in ignored_tlds and not m.isdigit()]
            
            if valid_kw:
                parsed_rules.add(f"HOST-KEYWORD,{max(valid_kw, key=len)},{POLICY_NAME}")
            else:
                if reg_expr not in manual_regex:
                    manual_regex.append(reg_expr)
            continue

        # 3. 處理 full: (精確域名)
        if line.startswith("full:"):
            domain = line.replace("full:", "").strip()
            parsed_rules.add(f"HOST,{domain},{POLICY_NAME}")

        # 4. 處理 domain: (域名後綴)
        elif line.startswith("domain:"):
            domain = line.replace("domain:", "").strip()
            parsed_rules.add(f"HOST-SUFFIX,{domain},{POLICY_NAME}")

        # 5. 處理 keyword: (關鍵字)
        elif line.startswith("keyword:"):
            kw = line.replace("keyword:", "").strip()
            parsed_rules.add(f"HOST-KEYWORD,{kw},{POLICY_NAME}")

        # 6. 一般域名/Punycode 預設轉 HOST-SUFFIX
        else:
            parsed_rules.add(f"HOST-SUFFIX,{line},{POLICY_NAME}")

def main():
    fetch_and_parse(TARGET_CATEGORY)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# AI Rules for Quantumult X (category-ai-!cn)\n")
        f.write(f"# Total Rules: {len(parsed_rules)}\n\n")
        f.write("\n".join(sorted(parsed_rules)))
        
        if manual_regex:
            f.write("\n\n# ==========================================\n")
            f.write("# Skipped Regexp (Need Manual Check):\n")
            f.write("# ==========================================\n")
            for reg in manual_regex:
                f.write(f"# {reg}\n")

    print(f"AI 規則轉換完成！產出檔案：{OUTPUT_FILE} (共 {len(parsed_rules)} 條規則)")

if __name__ == "__main__":
    main()
