import json, re, subprocess, sys

# Script to extract DART disclosure rcpNo links for watchlist stocks

code = '''
import json, re, time

new_tab("https://dart.fss.or.kr/dsac001/mainAll.do")
time.sleep(4)

raw = js("""
    var rows = document.querySelectorAll("table tbody tr");
    var result = [];
    rows.forEach(function(row) {
        var cells = row.querySelectorAll("td");
        if (cells.length >= 3) {
            var titleLink = cells[2].querySelector("a");
            var onclick = titleLink ? titleLink.getAttribute("onclick") : "";
            result.push({
                time: cells[0].innerText.trim(),
                company: cells[1].innerText.trim(),
                title: cells[2].innerText.trim(),
                onclick: onclick
            });
        }
    });
    return JSON.stringify(result);
""")

all_items = json.loads(raw)
for item in all_items:
    onclick = item["onclick"]
    m = re.search(r"openReportViewerMain\\('(\\d+)'\\)", onclick)
    if m:
        item["rcpNo"] = m.group(1)
    else:
        m2 = re.search(r"rcpNo=(\\d+)", onclick)
        if m2:
            item["rcpNo"] = m2.group(1)

targets = ["셀트리온", "LS", "한화", "CJ제일제당", "SK하이닉스", "HLB이노베이션", "HD현대", "한국항공우주", "에코프로비엠"]
matches = []
for item in all_items:
    for t in targets:
        if t in item["company"]:
            matches.append(item)
            break

with open("/Users/kwaksmacmini/Downloads/watchlist_dart_links.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)

print("EXTRACTED:" + str(len(matches)))
for m in matches:
    print("ITEM:" + json.dumps(m, ensure_ascii=False))
'''

result = subprocess.run(
    ["browser-harness", "-c", code],
    capture_output=True, text=True, timeout=30
)
print("STDOUT:", result.stdout[:3000])
if result.stderr:
    print("STDERR:", result.stderr[:1000])
