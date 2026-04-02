import json
import urllib.request
import re
from datetime import datetime

def fetch_musinsa_trends():
    url = 'https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    
    # 일반 크롬 브라우저인 것처럼 위장
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            raw_data = response.read().decode('utf-8')
        
        keywords = []
        
        # API 구조와 무관하게 keyword 값만 강제로 찾아내는 정규식
        matches = re.findall(r'"keyword"\s*:\s*"([^"]+)"', raw_data)
        
        # 중복 제거 및 순서 유지
        seen = set()
        for m in matches:
            if m.strip() and m not in seen:
                seen.add(m)
                keywords.append(m)
                
        # 수집한 데이터를 파일로 영구 기록
        with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
            json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
            
        print(f"수집 성공! 총 {len(keywords)}개의 키워드를 저장했습니다.")
        
    except Exception as e:
        print(f"수집 에러 발생: {e}")

if __name__ == "__main__":
    fetch_musinsa_trends()
