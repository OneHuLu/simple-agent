"""
Simple Agent 主程序入口

提供一个基于终端的交互式聊天界面
"""

import json
from agent.core import run_agent, run_agent_with_tool
from utils.config import MAX_HISTORY, CHAT_HISTORY_PATH, SYSTEM_PROMPT
from agent.memory import summarize_messages


def main():
    """
    主函数：启动交互式聊天循环
    """
    print("Agent started. Type something.")

    # 初始化消息列表，包含系统提示词
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # 记忆文案
    summary_memory = ""

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

        # 插入总结记忆
        if summary_memory:
            messages.insert(
                1,
                {
                    "role": "system",
                    "content": f"以下是之前对话的总结，请参考：{summary_memory}",
                },
            )

        # 调用 AI 获取回复
        reply = run_agent_with_tool(messages)
        print(f"\n🤖: {reply}")

        # 添加 AI 回复到对话历史
        messages.append({"role": "assistant", "content": reply})

        # 限制历史消息数量，保留系统提示词 + 最近的消息
        if len(messages) > MAX_HISTORY:
            messages = [messages[0]] + messages[-MAX_HISTORY:]

        # 当对话过长时，生成总结记忆
        if len(messages) > 20:
            summary_memory = summarize_messages(messages)
            print(summary_memory)
            # 清理历史，只保留 system + summary
            messages = [
                messages[0],
                {"role": "system", "content": f"对话总结：{summary_memory}"},
            ]

        # 保存对话记录到文件
        with open(CHAT_HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
