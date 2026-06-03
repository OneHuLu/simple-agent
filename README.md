# Simple Agent

一个基于 Ollama 的简单本地 AI 聊天助手。

## 功能特点

- 基于终端的交互式聊天界面
- 支持多轮对话，保留上下文
- 自动保存聊天记录
- 历史消息数量限制，防止上下文过长

## 前置要求

- Python 3.10+
- [Ollama](https://ollama.ai/) 已安装并运行
- 已下载 llama3 模型：`ollama pull llama3`

## 安装依赖

```bash
pip install requests
```

## 使用方法

```bash
python main.py
```

启动后即可在终端与 AI 进行对话：

- 输入消息与 AI 交流
- 输入 `exit`、`quit`、`bye` 或 `q` 退出程序

## 项目结构

```
simple-agent/
├── agent/
│   └── core.py        # 核心模块：Ollama API 调用
├── chat_history/      # 聊天记录存储目录（自动忽略提交）
├── main.py            # 主程序入口
└── README.md          # 项目说明文档
```

## 配置说明

可在代码中修改以下配置：

- `MODEL_NAME` (core.py)：使用的 Ollama 模型名称
- `OLLAMA_URL` (core.py)：Ollama API 地址
- `MAX_HISTORY` (main.py)：最大历史消息数量
- `SYSTEM_PROMPT` (main.py)：系统提示词

## 许可证

MIT License
