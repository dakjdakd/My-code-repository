import os
from datetime import datetime
from langchain_openai import ChatOpenAI

# 选择要使用的模型名称
MODEL_NAME = os.getenv("MODEL_NAME", "glm-4-plus")

# 获取当前的日期和时间，格式化为"月日时分"
now = datetime.now()
OUTPUT_BASE_NAME = f"{now.strftime('%m月%d日%H时%M分')}的Reddit_report"

# 根据选择的模型名称加载相应的配置
if MODEL_NAME == "glm-4-plus":
    llm = ChatOpenAI(
        temperature=1,
        model="glm-4-plus",
        openai_api_key="a39b3c2caa4c20edfc35d5e8cd8a9bc5.ZTuD0GCrVaS9n9BE",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
        max_tokens=80000,
        request_timeout=6000,
    )
elif MODEL_NAME == "deepseek":
    llm = ChatOpenAI(
            temperature=1.5,
            model="deepseek-chat",
            openai_api_key="sk-edc5e724b8bd45ebb1437d0331e09711",
            openai_api_base="https://api.deepseek.com/beta",
            max_tokens=5000
        )
    
elif MODEL_NAME == "openai":
    llm = ChatOpenAI(
            temperature=1,
            model="gpt-4o-mini",
            openai_api_key="sk-wAVdbeJ959cS1X3a5nAqt2mcI4EiGvrU6fy666AZ7bHn76Vp",
            openai_api_base="https://api.agicto.cn/v1")
else:
    raise ValueError(f"Unsupported model: {MODEL_NAME}")