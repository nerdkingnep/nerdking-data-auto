import json
import cloudscraper
from datetime import datetime
import re
import urllib.parse

def fetch_musinsa_trends():
    target_url = 'https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    proxy_url = f"https://api.allorigins.win/raw?url={urllib.parse.quote(target_url)}"
    
    urls_to_try = [target_url, proxy_url]
    
    # 강력한 봇 방어 우회 라이브러리 설정
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    headers = {
        'Referer': 'https://www.musinsa.com/',
        'Origin': 'https://www.musinsa.com'
    }
    
    keywords = []
    
    for url in urls_to_try:
        print(f"접속 시도 중: {url[:50]}...")
        try:
            response = scraper.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'data' in data and 'keywordList' in data['data']:
                        keywords = [item['keyword'] for item in data['data']['keywordList']]
                    elif 'data' in data and 'popularKeyword' in data['data']:
                        keywords = [item['keyword'] for item in data['data']['popularKeyword']]
                except:
                    pass
                    
            if not keywords:
                matches = re.findall(r'"keyword"\s*:\s*"([^"]+)"', response.text)
                seen = set()
                for m in matches:
                    if m.strip() and m not in seen:
                        seen.add(m)
                        keywords.append(m)

            if keywords:
                print("데이터 우회 및 추출에 성공했습니다!")
                break
        except Exception as e:
            print(f"해당 경로 실패: {e}")
            
    if keywords:
        with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
            json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
        print(f"최종 수집 완료: {len(keywords)}개의 트렌드 키워드를 확보했습니다.")
    else:
        # 실패 시 빈 파일을 만들지 않고 스크립트를 에러로 종료시킵니다.
        raise Exception("모든 수집 경로가 차단되어 데이터를 찾지 못했습니다.")

if __name__ == "__main__":
    fetch_musinsa_trends()
