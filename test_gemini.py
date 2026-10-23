
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

print("Loading environment...", flush=True)
load_dotenv()

print("Connecting to Gemini...", flush=True)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_retries=2,
    timeout=120
)

print("Sending test message...", flush=True)

response = llm.invoke(
    "Reply with exactly: Gemini connected successfully"
)

print("Response:", response.content, flush=True)
