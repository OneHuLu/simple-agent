"""
Simple Agent 主程序入口

提供一个基于终端的交互式聊天界面
"""

import json
from agent.core import run_agent

# 最大历史消息数量（防止上下文过长）
MAX_HISTORY = 50
# 聊天记录保存路径
CHAT_HISTORY_PATH = "./chat_history/user_message.json"
# 系统提示词
SYSTEM_PROMPT = "你是一个话痨本地AI助手。"


def main():
    """
    主函数：启动交互式聊天循环
    """
    print("Agent started. Type something.")

    # 初始化消息列表，包含系统提示词
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        # 获取用户输入
        user_input = input("\n你: ")

        # 检查退出命令
        if user_input.lower() in ["exit", "quit", "bye", "q"]:
            print("Bye~")
            break

        # 添加用户消息到对话历史
        messages.append({
            "role": "user",
            "content": user_input
        })

        # 调用 AI 获取回复
        reply = run_agent(messages)
        print(f"\n🤖: {reply}")

        # 添加 AI 回复到对话历史
        messages.append({"role": "assistant", "content": reply})

        # 限制历史消息数量，保留系统提示词 + 最近的消息
        if len(messages) > MAX_HISTORY:
            messages = [messages[0]] + messages[-MAX_HISTORY:]

        # 保存对话记录到文件
        with open(CHAT_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
