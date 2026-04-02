import json
import urllib.request
import urllib.parse
from datetime import datetime
import os
import re

def fetch_musinsa_trends():
    target_url = 'https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    scraper_api_key = os.environ.get('SCRAPER_API_KEY')
    
    if not scraper_api_key:
        raise Exception("ScraperAPI 키가 깃허브 Secrets에 등록되지 않았습니다.")
        
    # ScraperAPI를 통해 글로벌 가정용 IP로 위장하여 무신사에 접속
    api_url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={urllib.parse.quote(target_url)}"
    
    try:
        req = urllib.request.Request(api_url)
        with urllib.request.urlopen(req, timeout=40) as response:
            html = response.read().decode('utf-8')
            
            keywords = []
            try:
                data = json.loads(html)
                if 'data' in data and 'keywordList' in data['data']:
                    keywords = [item['keyword'] for item in data['data']['keywordList']]
                elif 'data' in data and 'popularKeyword' in data['data']:
                    keywords = [item['keyword'] for item in data['data']['popularKeyword']]
            except:
                pass
                
            if not keywords:
                matches = re.findall(r'"keyword"\s*:\s*"([^"]+)"', html)
                seen = set()
                for m in matches:
                    if m.strip() and m not in seen:
                        seen.add(m)
                        keywords.append(m)
                        
            if keywords:
                with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
                    json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
                print(f"최종 수집 완료: {len(keywords)}개의 트렌드 키워드 확보 성공")
            else:
                raise Exception("우회 접속은 성공했으나 데이터를 찾지 못했습니다.")
    except Exception as e:
        raise Exception(f"수집 실패: {e}")

if __name__ == "__main__":
    fetch_musinsa_trends()
