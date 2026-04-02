import json
import urllib.request
import re
from datetime import datetime

def fetch_musinsa_trends():
    # 무신사의 데이터센터 IP 차단을 완벽하게 우회하기 위한 징검다리 서버 목록
    # 1. Jina AI 리더 API: 글로벌 레지덴셜 프록시를 사용하여 봇 차단을 통과합니다.
    # 2. 구글 번역기 캐시 서버: 구글의 공식 IP를 빌려 무신사에 우회 접속합니다.
    urls_to_try = [
        'https://r.jina.ai/https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A',
        'https://translate.google.com/website?sl=ko&tl=ko&hl=ko&u=https://api.musinsa.com/api2/sc/v1/keyword/search-home?popularCount=20&gf=A'
    ]
    
    keywords = []
    
    for url in urls_to_try:
        print(f"우회 서버 접속 시도 중: {url[:50]}...")
        try:
            # 봇 차단을 피하기 위한 기본 브라우저 정보 입력
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            with urllib.request.urlopen(req, timeout=20) as response:
                html = response.read().decode('utf-8')
                
                # 우회 서버가 반환하는 복잡한 HTML이나 마크다운 텍스트 속에서 keyword 데이터만 강제로 추출합니다.
                matches = re.findall(r'"keyword"\s*:\s*"([^"]+)"', html)
                
                if matches:
                    seen = set()
                    for m in matches:
                        if m.strip() and m not in seen:
                            seen.add(m)
                            keywords.append(m)
                    
                    print("데이터 우회 추출에 완벽하게 성공했습니다!")
                    break # 성공 시 다음 우회 경로는 시도하지 않고 루프를 종료합니다.
        except Exception as e:
            print(f"해당 경로 우회 실패: {e}")
            
    if keywords:
        # 추출한 데이터를 깃허브 내에 json 파일로 영구 저장합니다.
        with open('musinsa_trends.json', 'w', encoding='utf-8') as f:
            json.dump({"updated_at": str(datetime.now()), "keywords": keywords}, f, ensure_ascii=False)
        print(f"최종 수집 완료: {len(keywords)}개의 트렌드 키워드를 확보했습니다.")
    else:
        print("모든 우회 경로 접속이 차단되었습니다. 수집된 데이터가 없습니다.")

if __name__ == "__main__":
    fetch_musinsa_trends()
