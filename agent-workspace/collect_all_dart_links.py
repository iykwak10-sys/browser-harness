import json, re, subprocess, time

code = '''
import json, re, time

targets = ["셀트리온", "LS", "한화", "CJ제일제당", "SK하이닉스", "HLB이노베이션", "HD현대", "한국항공우주", "에코프로비엠", "삼성전자", "현대로템", "풍산", "레인보우로보틱스"]
all_matches = []

for page in range(1, 7):
    if page == 1:
        new_tab("https://dart.fss.or.kr/dsac001/mainAll.do")
        time.sleep(4)
    else:
        js("search(" + str(page) + ");")
        time.sleep(2)
    
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
    
    items = json.loads(raw)
    for item in items:
        m = re.search(r"openReportViewer\\('(\\d+)'\\)", item["onclick"])
        if m:
            item["rcpNo"] = m.group(1)
    
    for item in items:
        for t in targets:
            if t in item["company"]:
                all_matches.append(item)
                break

with open("/Users/kwaksmacmini/Downloads/watchlist_dart_all_links.json", "w", encoding="utf-8") as f:
    json.dump(all_matches, f, ensure_ascii=False, indent=2)

for m in all_matches:
    print("DART:" + json.dumps(m, ensure_ascii=False))
print("TOTAL:" + str(len(all_matches)))
'''

result = subprocess.run(
    ["browser-harness", "-c", code],
    capture_output=True, text=True, timeout=120
)
print(result.stdout)
if result.stderr:
    print("ERR:", result.stderr[:500])
