from agent.schemas import WeatherQuery

def get_weather(city: str, unit: str = "celsius") -> dict:
    """
    示例工具：获取天气（模拟）
    """
    # 这里先用模拟数据，后面可以接真实 API
    return {
        "city": city,
        "temperature": 28,
        "unit": unit,
        "condition": "晴朗"
    }

# 工具注册表（LLM 会从这里选择工具）
TOOLS = {
    "get_weather": {
        "function": get_weather,
        "schema": WeatherQuery.model_json_schema()
    }
}