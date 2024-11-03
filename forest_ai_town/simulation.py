class Simulation:
    def __init__(self):
        self.agents = []
        self.chat_history = []
        self.current_speaker = 0  # 添加说话顺序控制
        
    def add_agents(self, agents):
        self.agents = agents
        
    def step(self):
        agent = self.agents[self.current_speaker]
        content = agent.generate_response(self.chat_history[-5:] if self.chat_history else [])
        
        # 创建标准格式的消息
        message = {
            "speaker": agent.name,
            "content": content
        }
        
        self.chat_history.append(message)
        self.current_speaker = (self.current_speaker + 1) % len(self.agents)
        return self.chat_history

    def generate_message(self):
        # 确保生成的消息包含实际内容
        message = {
            "speaker": self.agent.name,
            "content": self.agent.generate_response()  # 确保这个方法返回实际的聊天内容
        }
        return message