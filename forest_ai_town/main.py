from forest_ai_town.simulation import Simulation
from forest_ai_town.agents import Agent

def run_simulation():
    sim = Simulation()
    
    agents = [
        Agent("艾米", "经验丰富的探险家", "2.jpg", 
              "冷静智慧，善于决策，对自然和历史有深厚了解，是队伍的领导者"),
        Agent("杰克", "勇敢的退役军人", "3.jpg", 
              "勇敢直率，战斗技能出众，是队伍的保护者，但性格冲动"),
        Agent("莉莉", "细心的考古学家", "4.jpg", 
              "聪明好奇，专注于研究古代文明，观察力强，但有时过于谨慎"),
        Agent("汤姆", "幽默的旅行作家", "5.jpg", 
              "乐观幽默，善于记录，为团队带来欢乐，但有时显得优柔寡断")
    ]
    
    sim.add_agents(agents)
    return sim 