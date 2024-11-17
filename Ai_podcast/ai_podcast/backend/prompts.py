"""
提供各种提示词模板的模块
"""

def get_dialogue_prompts(length_type='long'):
    """获取不同长度的对话提示词配置"""
    base_prompts = {
        'short': {
            'min_dialogues': 15,     # 总共30句对话
            'description': '简短精炼的对话',
            'topic_count': 3,        # 3个主题
            'subtopic_count': 2,     # 每个主题2个子话题
            'dialogues_per_topic': 4, # 每个主题4段对话(8句)
            'strategy': 'concise',    # 简洁策略
            'max_dialogues': 20      # 最大对话数量限制(40句)
        },
        'medium': {
            'min_dialogues': 30,     # 总共60句对话
            'description': '中等深度的对话',
            'topic_count': 4,        # 4个主题
            'subtopic_count': 2,     # 每个主题2个子话题
            'dialogues_per_topic': 6, # 每个主题6段对话(12句)
            'strategy': 'balanced',   # 平衡策略
            'max_dialogues': 35      # 最大对话数量限制(70句)
        },
        'long': {
            'min_dialogues': 60,     # 总共120句对话
            'description': '完整深入的对话',
            'topic_count': 6,        # 6个主题
            'subtopic_count': 3,     # 每个主题3个子话题
            'dialogues_per_topic': 8, # 每个主题8段对话(16句)
            'strategy': 'detailed',   # 详细策略
            'max_dialogues': 70      # 最大对话数量限制(140句)
        }
    }
    return base_prompts.get(length_type, base_prompts['long'])

def get_outline_prompt(content, host, expert, dialogue_length='long'):
    """生成大纲提示词"""
    prompts = get_dialogue_prompts(dialogue_length)
    
    return f"""请根据以下内容生成一个播客大纲，严格按照对话长度要求设计：

内容：{content}

对话长度要求：{prompts['description']}（总共{prompts['min_dialogues']}段对话）
具体要求：
1. 必须生成{prompts['topic_count']}个主要话题
2. 每个话题必须包含{prompts['subtopic_count']}个子话题
3. 每个主话题将产生约{prompts['dialogues_per_topic']}段对话
4. 话题必须紧扣输入内容的核心知识点
5. 确保话题层次分明，由浅入深展开

⚠️ 重要提示：
1. 只返回JSON格式数据
2. 不要包含任何其他内容
3. 确保每个话题都能充分展开讨论
4. 话题数量必须严格符合要求

返回格式：
{{
    "topics": [
        {{
            "main": "主话题1",
            "subtopics": [
                "子话题1",
                "子话题2",
                ...
            ]
        }},
        ...更多话题...
    ]
}}"""

def get_topic_dialogue_prompt(topic, host, expert, min_dialogues, strategy='balanced'):
    """根据不同策略生成话题对话提示词"""
    expert_surname = expert[0] if expert else '李'
    
    base_prompt = f"""请生成一段自然流畅的播客对话。

主题：{topic['main']}
子话题：{', '.join(topic['subtopics'])}

对话结构示例：
1. 主持人引入话题：
   "说到[话题]，我很好奇..."
   "最近很多人都在关注[话题]..."
   "我们来聊聊[话题]这个有趣的问题..."

2. 专家首次回应：
   "这个问题很有意思，让我从[角度]来说明..."
   "确实，[话题]最近备受关注，主要是因为..."
   "从专业角度来看，[话题]其实涉及几个方面..."

3. 主持人追问：
   "听您这么说，我想到一个问题..."
   "这太有意思了！那[具体问题]呢？"
   "您刚才提到[关键词]，能具体解释一下吗？"

4. 专家展开论述：
   "让我举个例子..."
   "根据我的研究经验..."
   "从实践来看..."

5. 主持人总结过渡：
   "您的解释让我对[话题]有了新的认识..."
   "听完您的分享，我想到另一个相关的问题..."

对话要求：
1. 严格按照上述结构模板展开对话
2. 每个话题必须包含案例或数据支持
3. 确保对话有起承转合的节奏感
4. 适当加入口语化表达和情感互动
5. 避免生硬的知识灌输
6. 保持对话的连贯性和自然性

注意事项：
1. 不要使用"说到这个"、"确实"等过渡词
2. 每个回答要有具体的例子或数据
3. 保持对话的趣味性和启发性
4. 让专家展现个人见解而不是教科书式回答

请按照以下JSON格式返回：
{{
    "script": [
        {{"role": "interviewer", "content": "主持人的对话内容"}},
        {{"role": "expert", "content": "专家的对话内容"}}
    ]
}}"""

    # 根据不同策略添加特定要求
    strategy_prompts = {
        'concise': """
额外要求：
1. 对话要简洁明了
2. 直击话题核心
3. 避免过多铺垫
4. 每个观点用1-2句话说明即可""",

        'balanced': """
额外要求：
1. 平衡知识性和趣味性
2. 适度展开重要观点
3. 保持对话节奏流畅
4. 适当加入生动案例""",

        'detailed': """
额外要求：
1. 深入探讨每个观点
2. 多角度分析问题
3. 提供丰富的案例和数据
4. 充分展开专业见解"""
    }
    
    return base_prompt + strategy_prompts.get(strategy, strategy_prompts['balanced'])

def get_system_prompt():
    """获取系统提示词"""
    return """你是一个专业的播客对话生成专家。
1. 严格遵守JSON格式要求
2. 确保内容专业且易懂
3. 保持对话自然流畅
4. 紧扣主题不偏离
5. 平衡知识性和趣味性
6. 确保对话数量符合要求"""

def get_final_review_prompt(script, content, dialogue_length):
    """生成最终审查和优化的提示词"""
    return f"""请对以下播客对话进行优化和补充。主题内容：{content}

当前对话：
{json.dumps(script, ensure_ascii=False, indent=2)}

要求：
1. 保持原有对话的主要内容和风格
2. 在关键话题处补充更多互动和深度讨论
3. 确保对话自然流畅
4. 适当添加案例和数据支持
5. 保持专业性和趣味性的平衡

请返回优化后的完整对话，必须使用以下JSON格式：
{{
    "script": [
        {{"role": "interviewer", "content": "..."}},
        {{"role": "expert", "content": "..."}}
    ],
    "key_points": ["关键点1", "关键点2", ...]
}}""" 