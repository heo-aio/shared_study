"""
LLM 활용하는 정보
1. 자체 모델 - 모델이 학습한 내용들 (ollama)
2. RAG - 저장소에서 담고있는 고유의 지식(chromadb)
3. 인터넷 검색 - 최신정보, 실시간 정보(tavily) ---> 유료 API
tavily search API - AI 에이전트 및 LLM을 위해 최적화된 AI전용 검색엔진 서비스 API
"""
import os

from dotenv import load_dotenv
from langchain_tavily import TavilySearch, TavilyExtract

load_dotenv() # .env 불러오기

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def basic_search(query:str):
    ### search_depth
    # basic : 빠르고 저렴한 검색(1credit), 결과마다 간단한 content제공
    # advance : basic * 2배 검색, 문맥적의미까지 분석해 깊게 탐색 ex) 광고 문구 제거

    ### topic
    # general(기본) : 일반 웹 검색 -> 뉴스, 일반 지식, 블로그, 위키디피아 등 웹 전반의 통합검색
    # news : 최신 뉴스/기사 전용 검색
    # finance : 금융 / 경제 / 주식 전용 검색

    search = TavilySearch(max_results=3, search_depth="basic", topic="general")
    result = search.invoke({"query" : query})
    print(f"검색결과: {result["results"]}")

    for r in result["results"]:
        print(f"제목 : {r['title']}")
        print(f"URL : {r['url']}")
        print(f"SUMMARY : {r['content'][:150]}...")

# basic_search("2026년 한국 AI서비스개발 IT채용시장 트렌드 및 경쟁력있는 기술스택")

def detail_content(query:str):
    search = TavilySearch(max_results=3, search_depth="basic", topic="general")
    result = search.invoke({"query": query})
    ### extract_depth
    # basic : 표준적인 본문 텍스트 추출
    # advance : 표, 구조, 동적요소 등 정밀한 추출
    extract = TavilyExtract(extract_dpeth="basic")

    for r in result["results"]:
        print(f"제목 : {r['title']}")
        url = r["url"]
        print(f"URL : {url}")
        content = extract.invoke({"urls": [url]})
        print(content["results"][0].keys())
        print(content["results"][0]["raw_content"])

detail_content("개발 코딩 잘하는 법")
