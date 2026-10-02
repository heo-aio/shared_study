# collection : lecture
# 과목 : FAST API, PANDAS, SCIKIT-LEARN 중 택 1 (모두 해도 상관 X)
# 오픈북 시험용 LLM 제작
import chromadb
import ollama
import tiktoken
from PyPDF2 import PdfReader
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name="nomic-embed-text:latest"
)

client = chromadb.PersistentClient(path="./store")
coll = client.get_or_create_collection(
    name="lecture",
    embedding_function=ollama_ef
)

def insert_data(path):
    lecture = path.split("/")[1].rsplit(".", 1)[0].lower()
    print(lecture)

    reader = PdfReader(path)
    text = ""

    for i, page in enumerate(reader.pages):
        text += page.extract_text()

    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=25,
        length_function=len
    )

    chunks = text_spliter.split_text(text)
    print(f"{lecture} chunks = {len(chunks)}")


    ids = []
    for i in range(len(chunks)):
        ids.append(f"idx {i}")

    metas = [{"subject" : lecture} for i in range(len(chunks))]

    coll.upsert(documents=chunks, ids=ids, metadatas=metas)
    print(coll.get(where={"subject": lecture}))



insert_data("data/FASTAPI.pdf")
insert_data("data/pandas.pdf")
insert_data("data/scikit_learn.pdf")

def search_data(subject, query):
    print(f"과목 : {subject} / 질문내용 : {query}")
    results = coll.query(
        query_texts=[query],
        n_results=7,
        where={"subject" : {"$eq" : subject}}
    )

    context = "\n\n".join(results["documents"][0])

    prompt = f"""
    당신은 오픈북 시험 도움을 주는 사람입니다. 제공된 [학습교제]을 보고 사용자[질문]에 답해주세요.
    [학습교제]내용에 근거하여 질문자에게 알기 쉽게 요약해서 정리해주세요.

    [학습교제]
    {context}

    [질문]
    {query}
    """

    # print(results)

    resp = ollama.generate(
        model="gemma4:e4b",
        prompt=prompt,
        stream=True,
        options={
            "num_predict": -1,  # 출력토큰 수 (무제한)
            "num_ctx": 8192  # 입력 + 출력 합친 컨텍스트 크기
        }
    )

    for chunk in resp:
        print(chunk["response"], end="", flush=True)

        if chunk.get('done'):
            print('\n')
            print(f'중지이유 : {chunk.get('done_reason')}')


s = input("물어보고 싶은 과목(fastapi, scikit-learn, pandas)\n")
q = input("질문할 내용\n")
search_data(s, q)
