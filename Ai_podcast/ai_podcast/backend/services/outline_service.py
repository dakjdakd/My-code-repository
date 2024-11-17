import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from config.settings import ZHIPU_API_KEY, API_BASE_URL
import json
import re
from prompts import get_dialogue_prompts, get_outline_prompt

print(f"\n【初始化】API密钥: {ZHIPU_API_KEY[:8]}...")
print(f"【初始化】API基础URL: {API_BASE_URL}")

client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url=API_BASE_URL
)

class OutlineService:
    def generate_outline(self, content, host, expert, dialogue_length='long'):
        """生成播客大纲"""
        try:
            print(f"\n【开始生成大纲】")
            print(f"内容长度: {len(content)} 字符")
            print(f"主持人: {host}")
            print(f"专家: {expert}")
            print(f"对话长度类型: {dialogue_length}")

            prompts = get_dialogue_prompts(dialogue_length)
            prompt = get_outline_prompt(content, host, expert, dialogue_length)

            print("\n【生成提示词】")
            print(f"对话要求: {prompts['description']}")
            print(f"最小对话数: {prompts['min_dialogues']}")
            print(f"主题数量: {prompts['topic_count']}")

            print("\n【调用API】")
            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一个JSON生成助手。你必须只返回纯JSON格式数据，不要包含任何其他内容。"
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200000
            )
                    
            content = response.choices[0].message.content.strip()
            print("\n【API响应】")
            print(f"原始响应长度: {len(content)} 字符")
            
            result = self._parse_outline_response(content)
            print("\n【解析结果】")
            print(f"主题数量: {len(result['topics'])}")
            for i, topic in enumerate(result['topics'], 1):
                print(f"\n主题 {i}:")
                print(f"  - 主题: {topic['main']}")
                print(f"  - 子话题数量: {len(topic['subtopics'])}")
                for j, subtopic in enumerate(topic['subtopics'], 1):
                    print(f"    {j}. {subtopic}")

            self._validate_outline(result, prompts)
            print("\n【验证通过】大纲生成成功！")
            
            return result
                    
        except Exception as e:
            print(f"\n【错误】生成大纲失败: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误详情: {str(e)}")
            return None

    def _parse_outline_response(self, content):
        """解析API返回的大纲内容"""
        try:
            print("\n【开始解析响应】")
            # 清理非JSON内容
            content = re.sub(r'^[^{]*', '', content)
            content = re.sub(r'[^}]*$', '', content)
            print("JSON清理完成")
            
            result = json.loads(content)
            print("JSON解析成功")
            return result
            
        except json.JSONDecodeError as e:
            print(f"\n【错误】JSON解析失败")
            print(f"错误位置: {e.pos}")
            print(f"错误行: {e.lineno}")
            print(f"错误列: {e.colno}")
            raise ValueError(f"JSON解析失败: {str(e)}")

    def _validate_outline(self, result, prompts):
        """验证大纲结构和内容"""
        print("\n【开始验证大纲】")
        
        if not isinstance(result, dict) or 'topics' not in result:
            raise ValueError("返回格式错误：缺少 topics 字段")
        print("基本结构验证通过")
        
        required_topics = prompts['topic_count']
        actual_topics = len(result['topics'])
        print(f"需要的主题数量: {required_topics}")
        print(f"实际的主题数量: {actual_topics}")
        
        if actual_topics < required_topics:
            raise ValueError(f"话题数量不足：需要至少{required_topics}个，当前有{actual_topics}个")

        # 验证每个话题的结构
        for i, topic in enumerate(result['topics'], 1):
            print(f"\n验证主题 {i}:")
            if not isinstance(topic, dict) or 'main' not in topic or 'subtopics' not in topic:
                raise ValueError(f"主题 {i} 格式错误：缺少必要字段")
            
            subtopic_count = len(topic['subtopics'])
            required_subtopics = prompts['subtopic_count']
            print(f"  主题: {topic['main']}")
            print(f"  子话题数量: {subtopic_count}/{required_subtopics}")
            
            if subtopic_count < required_subtopics:
                raise ValueError(f"主题 {i} 的子话题数量不足：需要至少{required_subtopics}个")

    def generate_expert_name(self, content):
        """根据内容智能推荐专家名字"""
        try:
            print("\n【开始生成专家名字】")
            print(f"内容长度: {len(content)} 字符")
            
            prompt = f"""请根据以下内容推荐一个合适的专家名字：

内容：{content}

要求：
1. 使用常见的中文姓名
2. 名字要符合内容领域
3. 只返回姓名，不要其他内容
4. 名字要显得专业可信"""

            print("\n【调用API生成专家名字】")
            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {"role": "system", "content": "你是一个专家推荐助手，只返回一个合适的专家名字。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            expert_name = response.choices[0].message.content.strip()
            print(f"\n【生成的专家名字】: {expert_name}")
            return expert_name
            
        except Exception as e:
            print(f"\n【错误】生成专家名字失败: {str(e)}")
            return "李明智"  # 默认名字