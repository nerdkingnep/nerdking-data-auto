import json
import urllib.request
import urllib.parse
import re
from datetime import datetime

def fetch_musinsa_trends():
    target_url = 'https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    
    # 여러 개의 프록시(우회) 서비스를 징검다리처럼 설정하여 IP 차단 회피
    proxies = [
        f"https://api.allorigins.win/get?url={urllib.parse.quote(target_url)}",
        f"https://api.codetabs.com/v1/proxy?quest={urllib.parse.quote(target_url)}",
        target_url
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }
    
    raw_data = ""
    
    for proxy_url in proxies:
        print(f"접속 시도: {proxy_url}")
        try:
            req = urllib.request.Request(proxy_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                res_text = response.read().decode('utf-8')
                
                # 우회 서비스 종류에 따라 데이터 추출 방식 변경
                if "allorigins" in proxy_url:
                    json_res = json.loads(res_text)
                    raw_data = json_res.get('contents', '')
                else:
                    raw_data = res_text
                    
                if raw_data and "keyword" in raw_data:
                    print("우회 접속 성공 및 데이터 획득 완료!")
                    break
        except Exception as e:
            print(f"실패: {e}")
            continue
            
    keywords = []
    if raw_data:
        # 방어 구조를 무시하고 텍스트에서 키워드만 강제 추출
        matches = re.findall(r'"keyword"\s*:\s*"([^"]+)"', raw_data)
        seen = set()
        for m in matches:
            if m.strip() and m not in seen:
                seen.add(m)
                keywords.append(m)
                
    if keywords:
        with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
            json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
        print(f"최종 저장 완료: 총 {len(keywords)}개의 키워드를 확보했습니다.")
    else:
        print("모든 우회 접근이 차단되었거나 데이터를 찾을 수 없습니다.")

if __name__ == "__main__":
    fetch_musinsa_trends()
