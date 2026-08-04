import os
import urllib.request
import re

BASE_RAW_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/"
TARGET_CATEGORY = "category-porn"

# 設定輸出路徑至 rules 資料夾
OUTPUT_DIR = "rules"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "category-porn.snippets")
POLICY_NAME = "Porn"

visited_files = set()
parsed_rules = set()
converted_regex_rules = set()
manual_review_regex = []

KEYWORD_EXTRACTOR = re.compile(r'([a-zA-Z0-9\-]{4,})')

def convert_regexp_to_qx(reg_str):
    clean_reg = reg_str.replace('(^|\\.)', '').replace('$', '').replace('\\', '')
    matches = KEYWORD_EXTRACTOR.findall(clean_reg)
    ignored_tlds = {'com', 'net', 'org', 'xyz', 'info', 'buzz', 'top', 'life', 'icu', 'one'}
    valid_keywords = [m for m in matches if m.lower() not in ignored_tlds and not m.isdigit()]
    
    if valid_keywords:
        main_kw = max(valid_keywords, key=len)
        if len(main_kw) >= 4:
            return f"HOST-KEYWORD,{main_kw},{POLICY_NAME}"
    return None

def fetch_and_parse(filename):
    if filename in visited_files:
        return
    visited_files.add(filename)

    url = BASE_RAW_URL + filename
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"無法下載 {filename}: {e}")
        return

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        line = line.split('@')[0].split('#')[0].strip()
        if not line:
            continue

        if line.startswith("include:"):
            include_target = line.replace("include:", "").strip()
            fetch_and_parse(include_target)
            continue

        rule = None

        if line.startswith("regexp:"):
            reg_expr = line.replace("regexp:", "").strip()
            converted = convert_regexp_to_qx(reg_expr)
            if converted:
                rule = converted
                converted_regex_rules.add(rule)
            else:
                if reg_expr not in manual_review_regex:
                    manual_review_regex.append(reg_expr)
                continue

        elif line.startswith("full:"):
            full_domain = line.replace("full:", "").strip()
            rule = f"HOST,{full_domain},{POLICY_NAME}"

        elif line.startswith("domain:"):
            domain = line.replace("domain:", "").strip()
            rule = f"HOST-SUFFIX,{domain},{POLICY_NAME}"

        elif line.startswith("keyword:"):
            kw = line.replace("keyword:", "").strip()
            rule = f"HOST-KEYWORD,{kw},{POLICY_NAME}"

        else:
            rule = f"HOST-SUFFIX,{line},{POLICY_NAME}"

        if rule and rule not in parsed_rules:
            parsed_rules.add(rule)

def main():
    fetch_and_parse(TARGET_CATEGORY)
    
    # 確保 rules 目錄存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Category-Porn Rules for Quantumult X\n")
        f.write(f"# Total Rules: {len(parsed_rules)}\n")
        f.write(f"# Auto-converted Regexp Keywords: {len(converted_regex_rules)}\n\n")
        
        f.write("\n".join(sorted(parsed_rules)))
        
        if manual_review_regex:
            f.write("\n\n# ==========================================\n")
            f.write("# Skipped Regexp (Too Complex / Need Manual Check):\n")
            f.write("# ==========================================\n")
            for reg in manual_review_regex:
                f.write(f"# {reg}\n")

if __name__ == "__main__":
    main()
