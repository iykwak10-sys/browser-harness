import json, subprocess, time

# Key rcpNo values to extract
key_disclosures = [
    ("셀트리온", "주식소각결정", "20260506800095"),
    ("셀트리온", "[기재정정]주식소각결정", "20260506800779"),
    ("셀트리온", "연결영업실적", "20260506800093"),
    ("LS", "풍문해명", "20260506800483"),
    ("SK하이닉스", "최대주주변동", "20260506800689"),
    ("한화", "영업실적", "20260506800314"),
    ("HLB이노베이션", "전환사채권", "20260506000681"),
]

disclosure_texts = {}

for name, desc, rcpNo in key_disclosures:
    code = f'''
import json, time

new_tab("https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcpNo}")
time.sleep(5)

text = js("""
    var frame = document.querySelector("iframe#ifrm");
    if (frame && frame.contentDocument) {{
        return frame.contentDocument.body.innerText.substring(0, 5000);
    }}
    return "NO IFRAME";
""")
print("TEXT:" + text)
'''
    
    result = subprocess.run(
        ["browser-harness", "-c", code],
        capture_output=True, text=True, timeout=30
    )
    
    text = result.stdout
    if "TEXT:" in text:
        text = text.split("TEXT:", 1)[1].strip()
    
    disclosure_texts[f"{name}_{desc}"] = text
    print(f"\n=== {name} - {desc} ===")
    print(text[:1000])
    print("...")
    time.sleep(1)

# Save all texts
with open("/Users/kwaksmacmini/Downloads/disclosure_texts.json", "w", encoding="utf-8") as f:
    json.dump(disclosure_texts, f, ensure_ascii=False, indent=2)

print("\nAll disclosure texts saved.")
