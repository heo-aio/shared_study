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
    url = "http://localhost:11434",
    model_name = "nomic-embed-text:latest"
)

client = chromadb.PersistentClient(path="./store")
coll = client.get_or_create_collection(
    name = "study",
    embedding_function=ollama_ef
)

tokenizer = tiktoken.get_encoding("cl100k_base")

def my_tokenizer(text):
    text = text.strip()
    if len(text) <= 1:
        return 0
    tokens = len(tokenizer.encode(text))
    return tokens

def insert_data(path):
    lecture = path.split("/")[1].rsplit(".", 1)[0].lower()
    print(lecture)
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )

    chunks = text_spliter.split_text(text)
    ids = []
    for i in range(len(chunks)):
        ids.append(f"idx {i}")

    coll.upsert(documents=chunks, ids=ids)
    print(coll.get())

# insert_data("data/FASTAPI.pdf")
# insert_data("data/pandas.pdf")
# insert_data("data/scikit_learn.pdf")

def search_data(query):
    results = coll.query(
        query_texts=[query],
        n_results=7
    )

    context = results["documents"][0]

    prompt = f"""
    당신은 오픈북 시험 도움을 주는 사람입니다. 제공된 [PDF 본문 발췌부분]을 보고 사용자[질문]에 답해주세요.
    PDF 내용에 근거하여 질문자에게 알기 쉽게 상세히 설명해주세요.
    
    [PDF 본문 발췌부분]
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

q = input("FAST API와 Pandas 그리고 머신러닝에 대해 질문하면 됩니다.\n")
search_data(q)
