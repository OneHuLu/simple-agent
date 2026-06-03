"""
Simple Agent 核心模块

通过 Ollama API 与本地大模型进行交互
"""

import requests

# Ollama API 地址
OLLAMA_URL = "http://localhost:11434/api/generate"
# 使用的模型名称
MODEL_NAME = "llama3"


def run_agent(message: list[dict]) -> str:
    """
    调用 Ollama API 获取 AI 回复

    Args:
        message: 对话消息列表，格式如下：
            [
                {"role": "system", "content": "系统提示词"},
                {"role": "user", "content": "用户消息"},
                {"role": "assistant", "content": "AI 回复"},
                ...
            ]

    Returns:
        str: AI 的回复内容
    """
    # 将消息列表拼接成单个 prompt
    prompt = ""
    for item in message:
        role = item["role"]
        content = item["content"]
        prompt += f"{role}: {content}\n"

    # 构建请求参数
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # 禁用流式输出，直接返回完整结果
    }

    # 发送请求到 Ollama API
    resp = requests.post(OLLAMA_URL, json=payload)
    data = resp.json()

    # 返回 AI 回复内容
    return data["response"]
