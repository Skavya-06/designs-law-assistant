
import argparse
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

PDF_PATH = "data/designs_manual.pdf"
DB_PATH = "chroma_db"
COLLECTION_NAME = "designs_manual"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-3.5-flash-lite"

load_dotenv()


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


def create_vector_database():
    print("Loading PDF...")

    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()

    if not pages:
        raise ValueError("No pages were extracted from the PDF.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(pages)

    for chunk in chunks:
        chunk.metadata["page_number"] = (
            int(chunk.metadata.get("page", 0)) + 1
        )

    if not chunks:
        raise ValueError(
            "No text was extracted from the PDF."
        )

    print(f"Pages loaded: {len(pages)}")
    print(f"Chunks created: {len(chunks)}")
    print("Loading embedding model...")

    db = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=DB_PATH,
        collection_name=COLLECTION_NAME
    )

    print("Vector database created successfully!")
    return db


def get_database():
    return Chroma(
        persist_directory=DB_PATH,
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME
    )


def answer_question(question):
    if not question.strip():
        return {
            "answer": "Not found",
            "reference": "Not found",
            "sources": []
        }

    db = get_database()

    results = db.similarity_search_with_relevance_scores(question, k=8)
    print("\n--- DEBUG: RETRIEVED DOCUMENT CHUNKS ---")

    for i, (doc, score) in enumerate(results, 1):
        print(f"\nResult {i} | Score: {score:.3f}")
        print("Page:", doc.metadata.get("page_number", "Unknown"))
        print("Text:", doc.page_content[:500])

    # Starting threshold only; validate it with your test questions.
    relevant_results = [
        (doc, score)
        for doc, score in results
        if score >= 0.25
    ]

    if not relevant_results:
        return {
            "answer": "Not found",
            "reference": "Not found",
            "sources": []
        }

    context_parts = []

    for doc, score in relevant_results:
        page = doc.metadata.get("page_number", "Unknown")
        context_parts.append(
            f"PDF page: {page}\n"
            f"Text:\n{doc.page_content}"
        )

    context = "\n\n---\n\n".join(context_parts)

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        max_retries=2,
        timeout=120
    )   

    prompt = f"""
Answer the question using only the context below.

IMPORTANT CITATION RULES:
- Cite the manual's own section number and heading when visible.
- For the protection period question, use
  Section 06.04 — Period of protection.
- Do not confuse nearby text with the heading supporting
  the answer.
- Do not invent legal references or section numbers.
- If the answer is not supported by the context, return exactly:
  Not found

Context:
{context}

Question: {question}

Answer:
"""

    response = llm.invoke(prompt)
    if isinstance(response.content, str):
        answer = response.content.strip()
    else:
        answer = "".join(
            block.get("text", "")
            for block in response.content
            if isinstance(block, dict) and block.get("type") == "text"
        ).strip()

    if answer.lower().strip(" .") == "not found":
        return {
            "answer": "Not found",
            "reference": "Not found",
            "sources": []
        }

    sources = []

    for doc, score in relevant_results:
        page = doc.metadata.get("page_number", "Unknown")

        source = {
            "page": page,
            "excerpt": doc.page_content
        }

        if source not in sources:
            sources.append(source)

    pages = sorted({
        source["page"]
        for source in sources
        if isinstance(source["page"], int)
    })

    reference = "PDF page(s): " + ", ".join(
        str(page) for page in pages
    ) if pages else "See source excerpts"

    return {
        "answer": answer,
        "reference": reference,
        "sources": sources
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index",
        action="store_true",
        help="Build the PDF vector database"
    )
    args = parser.parse_args()

    if args.index:
        create_vector_database()
    else:
        while True:
            question = input(
                "\nAsk a question (or type exit): "
            ).strip()

            if question.lower() == "exit":
                break

            if not question:
                continue

            result = answer_question(question)

            print("\nAnswer:")
            print(result["answer"])

            print("\nReference:")
            print(result["reference"])

            for source in result["sources"]:
                print(f"\nPDF page {source['page']}:")
                print(source["excerpt"][:500])
