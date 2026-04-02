import os
import json
import urllib.request
from datetime import datetime

def fetch_musinsa_trends():
    # 파이썬 로봇을 일반 사용자인 것처럼 위장하여 무신사 방화벽을 통과합니다.
    url = 'https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        keywords = []
        if 'data' in data and 'keywordList' in data['data']:
            keywords = [item['keyword'] for item in data['data']['keywordList']]
        elif 'data' in data and 'popularKeyword' in data['data']:
            keywords = [item['keyword'] for item in data['data']['popularKeyword']]
            
        # 수집한 데이터를 깃허브 저장소 내에 파일로 영구 기록
        with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
            json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
        print("무신사 트렌드 수집 성공 및 파일 저장 완료!")
        
    except Exception as e:
        print(f"무신사 수집 에러: {e}")

if __name__ == "__main__":
    print("데이터 수집 자동화 시작...")
    fetch_musinsa_trends()
    # 유튜브 데이터 데일리 수집 코드는 앱과 연동 확인 후 여기에 추가됩니다.
    print("수집 종료.")
