import os
import urllib.request
import re

BASE_URL = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/"
TARGET_CATEGORY = "category-porn"

OUTPUT_DIR = "rules"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "porn.snippets")
POLICY_NAME = "Porn"

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
        line = line.strip().split('@')[0].split('#')[0].strip()
        if not line:
            continue

        if line.startswith("include:"):
            fetch_and_parse(line.replace("include:", "").strip())
            continue

        if line.startswith("regexp:"):
            reg_expr = line.replace("regexp:", "").strip()
            matches = KEYWORD_EXTRACTOR.findall(reg_expr)
            ignored_tlds = {'com', 'net', 'org', 'xyz', 'info', 'buzz', 'top', 'life', 'icu', 'one'}
            valid_kw = [m for m in matches if m.lower() not in ignored_tlds and not m.isdigit()]
            
            if valid_kw:
                parsed_rules.add(f"HOST-KEYWORD,{max(valid_kw, key=len)},{POLICY_NAME}")
            else:
                if reg_expr not in manual_regex:
                    manual_regex.append(reg_expr)
            continue

        if line.startswith("full:"):
            parsed_rules.add(f"HOST,{line.replace('full:', '').strip()},{POLICY_NAME}")
        elif line.startswith("domain:"):
            parsed_rules.add(f"HOST-SUFFIX,{line.replace('domain:', '').strip()},{POLICY_NAME}")
        elif line.startswith("keyword:"):
            parsed_rules.add(f"HOST-KEYWORD,{line.replace('keyword:', '').strip()},{POLICY_NAME}")
        else:
            parsed_rules.add(f"HOST-SUFFIX,{line},{POLICY_NAME}")

def main():
    fetch_and_parse(TARGET_CATEGORY)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Porn Rules for Quantumult X\n")
        f.write(f"# Total Rules: {len(parsed_rules)}\n\n")
        f.write("\n".join(sorted(parsed_rules)))
        
        if manual_regex:
            f.write("\n\n# ==========================================\n")
            f.write("# Skipped Regexp (Need Manual Check):\n")
            f.write("# ==========================================\n")
            for reg in manual_regex:
                f.write(f"# {reg}\n")

if __name__ == "__main__":
    main()
