import os
import sys

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import main
from dotenv import load_dotenv

def select_model():
    print("请选择要使用的模型：")
    print("1. deepseek")
    print("2. llama3-70b-8192")
    print("3. llama-3.1-70b-versatile")
    print("4. glm-4-plus")
    print("5. glm-4-long")
    print("6. glm-4-flash")
    print("7. llama3-chatqa")
    print("8. llama3.cn")
    print("9. llama3.1")
    print("10. google")
    
    choice = input("请输入选项编号 (1-10): ")
    
    model_map = {
        "1": "deepseek",
        "2": "llama3-70b-8192",
        "3": "llama-3.1-70b-versatile",
        "4": "glm-4-plus",
        "5": "glm-4-long",
        "6": "glm-4-flash",
        "7": "llama3-chatqa",
        "8": "llama3.cn",
        "9": "llama3.1",
        "10": "google"
    }
    
    selected_model = model_map.get(choice)
    if selected_model is None:
        print("无效的选择，将使用默认模型 glm-4-plus")
        selected_model = "glm-4-plus"
    return selected_model

if __name__ == "__main__":
    load_dotenv()  # 加载 .env 文件中的环境变量
    
    selected_model = select_model()
    print(f"您选择了 {selected_model} 模型")
    
    # 更新环境变量
    os.environ["MODEL_NAME"] = selected_model
    
    # 运行主程序，传递选择的模型
    main(selected_model)