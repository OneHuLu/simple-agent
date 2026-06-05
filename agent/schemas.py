from pydantic import BaseModel,Field

class WeatherQuery(BaseModel):
    """
    天气查询模型定义
    """
    city: str = Field(..., description="城市名称")
    unit: str = Field("celsius", description="温度单位，可选：celsius 或 fahrenheit")