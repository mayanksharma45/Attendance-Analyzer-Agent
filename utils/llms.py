import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"]=GROQ_API_KEY
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]

class LLMModel1:
    def __init__(self, model_name="deepseek-r1-distill-llama-70b"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name = model_name
        self.groq_model=ChatGroq(model=self.model_name)
        
    def get_model1(self):
        return self.groq_model
    

class LLMModel2:
    def __init__(self, model_name="gemini-1.5-flash"):
        if not model_name:
            raise ValueError("Model is not defined.")
        self.model_name = model_name
        self.gemini_model=ChatGoogleGenerativeAI(model=self.model_name)
        
    def get_model2(self):
        return self.gemini_model