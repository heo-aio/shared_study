import os

import chromadb
from PyPDF2 import PdfReader
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 임베디드 함수 선언 + 2. 올라마 연동
embed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text:latest")

# 3. chromadb 생성 및 collection 등록
client = chromadb.PersistentClient(path="./store")
store = Chroma(
    client=client,
    collection_name="study",
    embedding_function=embed
)

def add_data(dir:str) -> None:
    for file in os.listdir(dir):
        print(f"{file} 읽어와 저장")
        reader = PdfReader(f"{dir}/{file}")
        text = ''

        for page in reader.pages:
            text += page.extract_text()

        text_spliter = RecursiveCharacterTextSplitter(
            chunk_size=150,
            chunk_overlap=30,
            length_function=len
        )

        docs = []

        for chunk in text_spliter.split_text(text):
            # print(f"chunk: {chunk}")

            # docs.append(Document(id="doc1", page_content=chunk, metadata={"subject" : file}))
            # id를 안넣으면 자동으로 생성해 주기에 안넣어도 된다.
            docs.append(Document(page_content=chunk))

        store.add_documents(docs)
        print(f"{file} 저장완료")


# add_data("data")
# print(store.get())

q = input("pandas, scikit-learn, fast-api 등에 대해서 궁금한 점을 물어보세요.")

# 4. OLLAMA와 LANG-CHAIN 연동할 LLM사용
llm = ChatOllama(model="gemma4:e4b", temperature=0.5)

# 프롬프트 생성
prompt = ChatPromptTemplate.from_template(
    """
    당신은 python을 이용한 데이터 분석 및 인공지능 개발 전문가 입니다.
    [참고문서]의 내용만으로 답변하세요.
    [참고문서]에 나와있지않은 내용이라면 "참고문서에 없는 내용이라 답변이 어렵습니다."라고 대답하세요.
    
    [참고문서]
    {context}
    
    [질문내용]
    {question}
    """
)

# 질문 -> chromadb 검색 -> context에 담는다 -> 모델에 전달 -> 결과값 받음
ret = store.as_retriever(search_kwargs={"k":5})

# question과 그 내용으로 검색된 context를 받는다.
# 그 내용을 prompt에 전달
# prompt 내용을 llm에 전달
# 결과 내용을 StrOutputParser()에 전달하여 문자열만 추출
chain = ({"question" : RunnablePassthrough(), "context" : ret} | prompt | llm | StrOutputParser())

for chunk in chain.stream(q):
    print(chunk, end="", flush=True)