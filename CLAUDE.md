# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Simple Agent 是一个基于 Ollama 的本地 AI 聊天助手，提供终端交互式聊天界面，支持多轮对话、工具调用和总结记忆功能。

## 开发命令

```bash
# 运行程序
python main.py

# 安装依赖（使用 uv）
uv sync

# 安装依赖（使用 pip）
pip install requests httpx openai pydantic python-dotenv
```

## 前置要求

- Python 3.13+
- [Ollama](https://ollama.ai/) 已安装并运行
- 已下载 llama3 模型：`ollama pull llama3`

## 架构

```
simple-agent/
├── main.py              # 主程序入口
├── agent/
│   ├── core.py          # Ollama API 通信
│   ├── memory.py        # 对话总结记忆
│   ├── tools.py         # 工具注册与实现
│   └── schemas.py       # Pydantic 数据模型
└── utils/
    └── config.py        # 集中配置管理
```

### 核心流程

1. **对话循环** (`main.py`)：用户输入 → 消息列表 → AI 回复 → 历史管理
2. **工具调用** (`agent/core.py:run_agent_with_tool`)：LLM 输出 `CALL_TOOL <tool_name> <args_json>` 时触发工具执行，结果返回 LLM 继续处理
3. **总结记忆** (`agent/memory.py`)：当对话超过 20 条时，调用模型生成 summary，清空历史只保留系统提示词和总结

### 模块职责

| 模块 | 职责 |
|------|------|
| `agent/core.py` | 与 Ollama API 通信，支持普通对话和工具调用两种模式 |
| `agent/tools.py` | 工具注册表 `TOOLS`，包含函数和 JSON Schema |
| `agent/schemas.py` | 工具参数的 Pydantic 模型定义 |
| `agent/memory.py` | `summarize_messages()` 生成对话总结 |

## 关键配置

所有配置集中在 `utils/config.py`：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `MODEL_NAME` | llama3 | Ollama 模型名称 |
| `OLLAMA_URL` | http://localhost:11434/api/generate | Ollama API 地址 |
| `MAX_HISTORY` | 50 | 最大历史消息数量 |
| `SYSTEM_PROMPT` | 你是一个话痨本地AI助手。 | 系统提示词 |
| `CHAT_HISTORY_PATH` | ./chat_history/user_message.json | 聊天记录保存路径 |

## 扩展工具

1. 在 `agent/schemas.py` 定义参数模型
2. 在 `agent/tools.py` 实现函数并添加到 `TOOLS` 字典

## 注意事项

- `chat_history/` 目录在 `.gitignore` 中被忽略
- 工具调用协议：LLM 需输出 `CALL_TOOL <name> <json_args>` 格式
- `utils/logger.py` 已预留但未实现
