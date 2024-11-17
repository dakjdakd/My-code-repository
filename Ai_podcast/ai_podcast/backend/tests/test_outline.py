import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.outline_service import OutlineService

def test_outline():
    service = OutlineService()
    result = service.generate_outline("测试内容", "张三", "李四")
    print(result)

if __name__ == "__main__":
    test_outline() 