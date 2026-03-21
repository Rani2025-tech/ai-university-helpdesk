import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

OLLAMA_MODEL     = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
OLLAMA_BASE_URL  = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "faiss_index")

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

def ingest_pdf(pdf_path: str):
    loader   = PyPDFLoader(pdf_path)
    docs     = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks   = splitter.split_documents(docs)

    embeddings = get_embeddings()

    if os.path.exists(FAISS_INDEX_PATH):
        existing = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        existing.add_documents(chunks)
        existing.save_local(FAISS_INDEX_PATH)
        print(f"Merged {len(chunks)} chunks into existing FAISS index")
    else:
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local(FAISS_INDEX_PATH)
        print(f"Created new FAISS index with {len(chunks)} chunks")

    return len(chunks)

def load_vectorstore() -> FAISS:
    return FAISS.load_local(
        FAISS_INDEX_PATH,
        get_embeddings(),
        allow_dangerous_deserialization=True
    )

def get_answer(question: str, language: str = "auto") -> str:
    from backend.utils import detect_language

    # Detect or use selected language
    if language == "auto":
        lang = detect_language(question)
    else:
        lang = language

    language_instructions = {
        "en": "Answer in English.",
        "hi": "Answer in Hindi language only. Use Devanagari script.",
        "or": "Answer in Odia language only. Use Odia script."
    }

    lang_instruction = language_instructions.get(lang, "Answer in English.")

    vectorstore = load_vectorstore()
    retriever   = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm         = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

    prompt = PromptTemplate.from_template("""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a helpdesk assistant for NIST University Berhampur Odisha.
Use ONLY the facts from the context below to answer.
{lang_instruction}
Do not say you don't know if the answer is clearly in the context.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Context:
{context}

Question: {question}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>""")

    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
            "lang_instruction": lambda _: lang_instruction
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(question)