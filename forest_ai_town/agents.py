from zhipuai import ZhipuAI
import random

class Agent:
    def __init__(self, name, description, avatar, personality):
        self.name = name
        self.description = description
        self.avatar = avatar
        self.personality = personality
        self.memory = []
        self.client = ZhipuAI(api_key="24cedf8cbdb377acba0b7db47832f7b2.adhp3UgUTilfxMnV")
        
    def generate_response(self, context):
        prompt = f"""
        背景：四个探险家（艾米、杰克、莉莉、汤姆）正在寻找一座神秘的古代遗迹。这座遗迹据说隐藏着能够改变世界的力量。
        他们必须在充满危险的古老森林中探索，解开谜题，同时还要提防其他觊觎遗迹力量的敌对势力。
        
        你是{self.name}，{self.description}，性格特点是{self.personality}。
        
        最近的对话记录：{context}
        
        请根据你的身份和性格，生成一句带有互动性的对话。要求：
        1. 必须要和其他角色进行直接对话，在句子中明确提到对方的名字
        2. 对话要自然，像真实的人在交
        3. 要围绕探险和寻找遗迹的主题
        4. 要体现出你的性格特点
        5. 要对之前的对话有回应或延续
        
        对话示例：
        - 如果你是艾米："杰克，我注意到西边的石壁上有些奇怪的刻痕，你觉得那会是机关吗？"
        - 如果你是杰克："莉莉，这些藤蔓下面好像藏着什么，让我帮你清理一下。"
        - 如果你是莉莉："艾米，这些符号看起来是某种古老的文字，我需要一点时间破译。"
        - 如果你是汤姆："杰克，我在旧笔记里看到过类似的遗迹描述，要小心陷阱。"
        
        请生成一句自然的对话，确保包含其他角色的名字，并且表现出你的性格特点。
        """
        
        try:
            response = self.client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API调用错误: {e}")
            # 备用回复
            fallback_responses = {
                "艾米": [
                    "杰克，先别轻举妄动，这些古老的机关可能很危险。",
                    "莉莉，你能解读这些符号的含义吗？",
                    "汤姆，把这些发现记录下来，可能很重要。"
                ],
                "杰克": [
                    "艾米，我感觉有人在跟踪我们...",
                    "莉莉，让我来搬开这些石块。",
                    "汤姆，保持警惕，我去前面探路。"
                ],
                "莉莉": [
                    "艾米，这些遗迹的年代比我们想象的要古老得多。",
                    "杰克，等等，这个机关可能有特殊的开启方式。",
                    "汤姆，你的笔记里有类似的符号记载吗？"
                ],
                "汤姆": [
                    "米，我觉得我们应该相信自己的直觉。",
                    "杰克，也许我们可以找个更安全的路线？",
                    "莉莉，这个故事让我想起一个古老的传说。"
                ]
            }
            return random.choice(fallback_responses[self.name])