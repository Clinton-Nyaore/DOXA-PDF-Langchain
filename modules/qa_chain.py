from langchain_text_splitters import RecursiveCharacterTextSplitter
from modules.process_pdf import pdf_processor
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

def create_qa_chain(text):
    """"Create a QA chain from text using FAISS + LCEL (LangChain Expression Language).
    """
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), 
        model="gpt-4o-mini", 
        temperature=0
        )
    
    # Split text into overlapping chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    if not chunks:
        raise ValueError("No text chunks created. Check input text.")

    # Create embeddings and vector store (FAISS)
    embedding_model = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vector_store = FAISS.from_texts(chunks, embedding_model)
    retriever = vector_store.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 3}
        )
    
    # Create a prompt template
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Use the following context to answer the question:\n\n"
        "{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )

    # Building a retriever QA chain
    qa_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa_chain

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    pdf_path = os.path.join(base_dir, "docs", "clinton_profile.pdf")

    documents = pdf_processor(pdf_path)
    full_text = " ".join([doc.page_content for doc in documents])

    qa_chain = create_qa_chain(full_text)
    result = qa_chain.invoke("What is the main topic of the document?")
    print(result)
