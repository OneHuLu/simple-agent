"""
Simple Agent 核心模块

通过 Ollama API 与本地大模型进行交互
"""
import json
import requests
from  utils.config import OLLAMA_URL, MODEL_NAME
from agent.tools import TOOLS

def run_agent(messages: list[dict]) -> str:
    """
    普通对话（无工具调用）
    调用 Ollama API 获取 AI 回复

    Args:
        messages: 对话消息列表，格式如下：
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
    for item in messages:
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


def run_agent_with_tool(messages: list[dict]):
    """
       工具调用循环：LLM → 工具 → LLM
    """
    while True:
        prompt = ""
        for item in messages:
            role = item["role"]
            content = item["content"]
            prompt += f"{role}: {content}\n"

        # 工具描述
        tool_desc = "\n可用工具：\n"
        for name, meta in TOOLS.items():
            tool_desc += f"- {name}: {json.dumps(meta['schema'], ensure_ascii=False)}\n"

        prompt += tool_desc

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        resp = requests.post(OLLAMA_URL, json=payload)
        data = resp.json()
        reply = data["response"]

        # 2. 判断 LLM 是否想调用工具
        if reply.startswith("CALL_TOOL"):
            # 格式：CALL_TOOL get_weather {"city": "北京"}
            _, tool_name, args_json = reply.split(" ", 2)
            args = json.loads(args_json)

            tool_fn = TOOLS[tool_name]["function"]
            result = tool_fn(**args)
            # 3. 把工具结果返回给 LLM
            messages.append({
                "role": "tool",
                "content": json.dumps(result, ensure_ascii=False)
            })
            continue

            # 4. 如果不是工具调用，直接返回
        return reply