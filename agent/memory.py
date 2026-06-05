# 用于管理对话的“总结记忆”（summary memory）
import requests
from typing import List, Dict
from utils.config import OLLAMA_URL, MODEL_NAME


def summarize_messages(messages: List[Dict]) -> str:
    """
       使用本地模型对对话进行总结，生成 summary memory。
    """
    convo_text = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        convo_text += f"{role}: {content}\n"
    prompt = f"""
    下面是一段用户和助手的对话，请你用中文总结关键内容：
    - 只保留对后续对话有帮助的信息
    - 不要逐句复述
    - 控制在 100 字以内

    对话内容：
    {convo_text}
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(OLLAMA_URL, json=payload)
    data = resp.json()
    return data["response"]
