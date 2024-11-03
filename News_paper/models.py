import os
from langchain_ollama.llms import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

def get_llm(model_name):
    if model_name == "deepseek":
        return ChatOpenAI(
            temperature=1.5,
            model="deepseek-chat",
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            openai_api_base=os.getenv("DEEPSEEK_API_BASE"),
            max_tokens=8000
        )
    elif model_name == "llama3-70b-8192":
        return ChatGroq(
            model="llama3-70b-8192",
            temperature=1,
            max_tokens=10000,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY"),
        )
    elif model_name == "llama-3.1-70b-versatile":
        return ChatGroq(
            model="llama-3.1-70b-versatile",
            temperature=1.5,
            max_tokens=10000,
            timeout=None,
            max_retries=2,
            api_key=os.getenv("GROQ_API_KEY"),
            base_url=os.getenv("GROQ_API_BASE")
        )
    elif model_name == "glm-4-plus":
        return ChatOpenAI(
            temperature=1,
            model="glm-4-plus",
            max_tokens=80000,
            api_key=os.getenv("ChatGLM_API_KEY"),
            base_url=os.getenv("ChatGLM_BASE_URL")
        )
    elif model_name == "glm-4-long":
        return ChatOpenAI(
            temperature=1,
            model="glm-4-long",
            api_key=os.getenv("ChatGLM_API_KEY"),
            base_url=os.getenv("ChatGLM_BASE_URL")
        )
    elif model_name == "glm-4-flash":
        return ChatOpenAI(
            temperature=1,
            model="glm-4-flash",
            max_tokens=None,
            api_key=os.getenv("ChatGLM_API_KEY"),
            base_url=os.getenv("ChatGLM_BASE_URL")
        )
    elif model_name == "llama3-chatqa":
        return OllamaLLM(
            model="llama3-chatqa",
            temperature=1,
            max_tokens=None,
        )
    elif model_name == "llama3.cn":
        return OllamaLLM(
            model="jack/llama3-8b-chinese",
            temperature=1.2,
            max_tokens=None,
        )
    elif model_name == "llama3.1":
        return OllamaLLM(
            model="ollama/llama3.1:latest",
            temperature=1.2,
            max_tokens=None,
        )
    elif model_name == "google":
        return ChatGoogleGenerativeAI(
            model="Gemini-1.5-flash",
            temperature=1,
            max_tokens=None,
            base_url="https://api.google.com",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        raise ValueError(f"Unsupported model: {model_name}")