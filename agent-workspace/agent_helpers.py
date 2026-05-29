"""Agent-editable browser helpers.

Add task-specific browser primitives here. Core helpers from browser_harness.helpers
load this file when BH_AGENT_WORKSPACE points at this directory, or when this
repo's default agent-workspace exists.
"""

import json
import time
import datetime


def dart_scrape_today_disclosures(save_path=None):
    """Scrape today's DART disclosures from dart.fss.or.kr.
    
    Navigates to the mainAll.do page and iterates through all paginated pages.
    
    Args:
        save_path: Optional path to save JSON output.
    
    Returns:
        list of dicts with keys: time, market, company, title, submitter, date
    """
    # Navigate to today's disclosures page
    js("window.location.href = 'https://dart.fss.or.kr/dsac001/mainAll.do';")
    time.sleep(3)
    
    all_items = []
    
    for page in range(1, 7):
        if page > 1:
            js(f"search({page});")
            time.sleep(2)
        
        raw = js("""
            var rows = document.querySelectorAll("table tbody tr");
            var result = [];
            rows.forEach(function(row) {
                var cells = row.querySelectorAll("td");
                if (cells.length >= 4) {
                    var timeVal = cells[0].innerText.trim();
                    var companyCell = cells[1];
                    var marketTag = companyCell.querySelector(
                        ".tagCom_kospi, .tagCom_kosdaq, .tagCom_konex, .tagCom_etc"
                    ) || companyCell.querySelector("span");
                    var marketVal = marketTag ? (marketTag.title || marketTag.innerText.trim()) : "";
                    var companyVal = companyCell.innerText.replace(marketVal, "").trim();
                    var titleVal = cells[2].innerText.trim();
                    var submitterVal = cells.length > 3 ? cells[3].innerText.trim() : "";
                    var dateVal = cells.length > 4 ? cells[4].innerText.trim() : "";
                    
                    if (timeVal && companyVal) {
                        result.push({
                            time: timeVal,
                            market: marketVal,
                            company: companyVal,
                            title: titleVal,
                            submitter: submitterVal,
                            date: dateVal
                        });
                    }
                }
            });
            return JSON.stringify(result);
        """)
        
        page_items = json.loads(raw)
        all_items.extend(page_items)
        print(f"  Page {page}: {len(page_items)} items (total: {len(all_items)})")
    
    # Clean company names
    for item in all_items:
        co = item["company"]
        for prefix in ["유 ", "코 ", "기 ", "넥 "]:
            if co.startswith(prefix):
                co = co[len(prefix):]
        co = co.replace(" IR", "").strip()
        item["company_clean"] = co
    
    if save_path:
        report = {
            "date": datetime.date.today().isoformat(),
            "total_count": len(all_items),
            "disclosures": all_items
        }
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(all_items)} items to {save_path}")
    
    return all_items
