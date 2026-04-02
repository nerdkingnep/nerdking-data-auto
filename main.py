import json
from datetime import datetime
from curl_cffi import requests

def fetch_musinsa_trends():
    url = 'https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    try:
        # 실제 크롬 브라우저와 100% 동일한 네트워크 지문을 생성하여 방화벽을 통과합니다.
        response = requests.get(url, impersonate="chrome110", timeout=15)
        
        if response.status_code != 200:
            print(f"접속 실패 (상태 코드: {response.status_code})")
            return
            
        data = response.json()
        keywords = []
        
        if 'data' in data and 'keywordList' in data['data']:
            keywords = [item['keyword'] for item in data['data']['keywordList']]
        elif 'data' in data and 'popularKeyword' in data['data']:
            keywords = [item['keyword'] for item in data['data']['popularKeyword']]
        
        if not keywords:
            print("데이터를 성공적으로 받았으나 키워드 목록이 비어있습니다.")
            return
        
        # 정상적으로 키워드가 수집되었을 때만 파일을 덮어씌워 빈 파일 생성을 방지합니다.
        with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
            json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
        
        print(f"수집 및 저장 완료: 총 {len(keywords)}개의 키워드 확보")
        
    except Exception as e:
        print(f"수집 중 에러 발생: {e}")

if __name__ == "__main__":
    fetch_musinsa_trends()
