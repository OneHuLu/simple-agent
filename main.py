from agent.core import run_agent

def main():
    print("Agent started. Type something.")
    while True:
        message = input("请输入命令：")
        user_message = run_agent(message)
        print(user_message)
        if message == "exit":
            print('Bey~')
            break


if __name__ == "__main__":
    main()
