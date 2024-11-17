from openai import OpenAI
from config.settings import ZHIPU_API_KEY, API_BASE_URL
import json
import re
from prompts import get_dialogue_prompts, get_topic_dialogue_prompt

client = OpenAI(
    api_key=ZHIPU_API_KEY,
    base_url=API_BASE_URL
)

class DialogueService:
    def process_complete_dialogue(self, outline, content, host, expert):
        """处理完整的对话生成流程"""
        try:
            print("\n【开始生成完整对话】")
            print(f"内容长度: {len(content)} 字符")
            print(f"主持人: {host}")
            print(f"专家: {expert}")
            print(f"大纲主题数: {len(outline['topics'])}")
            
            full_script = []
            key_points = []
            
            # 确保至少生成5个知识点
            min_key_points = 5
            print(f"\n【开始生成知识点】目标数量: {min_key_points}")
            
            # 从主题生成知识点
            for i, topic in enumerate(outline['topics'], 1):
                print(f"\n处理主题 {i}/{len(outline['topics'])}: {topic['main']}")
                print(f"子话题数量: {len(topic['subtopics'])}")
                
                # 生成主知识点
                topic_points = {
                    "title": topic['main'],
                    "subtopics": topic['subtopics']
                }
                key_points.append(topic_points)
                print(f"添加主知识点: {topic['main']}")
                
                # 处理子话题
                if len(topic['subtopics']) > 2:
                    print(f"子话题数量大于2，进行拆分...")
                    for i in range(0, len(topic['subtopics']), 2):
                        sub_points = {
                            "title": f"{topic['main']} - 延伸{i//2 + 1}",
                            "subtopics": topic['subtopics'][i:i+2]
                        }
                        key_points.append(sub_points)
                        print(f"添加延伸知识点: {sub_points['title']}")
                        print(f"包含子话题: {', '.join(sub_points['subtopics'])}")
            
            # 如果知识点不够，生成额外的延伸知识点
            if len(key_points) < min_key_points:
                print(f"\n【知识点数量不足】当前: {len(key_points)}, 目标: {min_key_points}")
                print("开始生成额外知识点...")
                
                while len(key_points) < min_key_points:
                    for i, point in enumerate(key_points[:]):
                        if len(key_points) >= min_key_points:
                            break
                        print(f"\n从知识点 '{point['title']}' 生成延伸内容")
                        new_point = {
                            "title": f"{point['title']} - 深入分析",
                            "subtopics": [f"{sub} 的应用" for sub in point['subtopics']]
                        }
                        key_points.append(new_point)
                        print(f"添加深入分析知识点: {new_point['title']}")
                        print(f"包含子话题: {', '.join(new_point['subtopics'])}")
            
            print(f"\n【知识点生成完成】总数: {len(key_points)}")
            
            # 1. 生成开场白
            print("\n【生成开场白】")
            opening = self._generate_opening_closing(content, host, expert, True)
            if opening and isinstance(opening, dict) and 'script' in opening:
                full_script.extend(opening['script'])
                print(f"开场白生成成功，添加 {len(opening['script'])} 段对话")
            else:
                print("开场白生成失败或格式错误")
            
            # 2. 为每个话题生成对话
            print("\n【生成主题对话】")
            for i, topic in enumerate(outline['topics'], 1):
                print(f"\n处理主题 {i}/{len(outline['topics'])}: {topic['main']}")
                
                # 生成主话题对话
                dialogue = self._generate_topic_dialogue(topic, host, expert)
                if dialogue and isinstance(dialogue, dict) and 'script' in dialogue:
                    full_script.extend(dialogue['script'])
                    print(f"主题对话生成成功，添加 {len(dialogue['script'])} 段对话")
                else:
                    print("主题对话生成失败或格式错误")
                
                # 生成过渡对话
                if i < len(outline['topics']):
                    print(f"\n生成从 '{topic['main']}' 到 '{outline['topics'][i]['main']}' 的过渡对话")
                    transition = self._generate_transitions(
                        topic['main'],
                        outline['topics'][i]['main'],
                        host,
                        expert
                    )
                    if transition and isinstance(transition, dict) and 'script' in transition:
                        full_script.extend(transition['script'])
                        print(f"过渡对话生成成功，添加 {len(transition['script'])} 段对话")
                    else:
                        print("过渡对话生成失败或格式错误")
            
            # 3. 生成结束语
            print("\n【生成结束语】")
            closing = self._generate_opening_closing(content, host, expert, False)
            if closing and isinstance(closing, dict) and 'script' in closing:
                full_script.extend(closing['script'])
                print(f"结束语生成成功，添加 {len(closing['script'])} 段对话")
            else:
                print("结束语生成失败或格式错误")
            
            print(f"\n【对话生成完成】")
            print(f"总对话数: {len(full_script)} 段")
            print(f"知识点数: {len(key_points)} 个")
            print(f"平均每个知识点子话题数: {sum(len(point['subtopics']) for point in key_points)/len(key_points):.1f}")
            
            return {
                "script": full_script,
                "key_points": key_points,
                "meta": {
                    "host": host,
                    "expert": expert,
                    "total_dialogues": len(full_script),
                    "topics_count": len(outline['topics'])
                }
            }
            
        except Exception as e:
            print(f"\n【错误】处理对话生成失败")
            print(f"错误类型: {type(e).__name__}")
            print(f"错误详情: {str(e)}")
            print(f"错误位置: {e.__traceback__.tb_frame.f_code.co_filename}:{e.__traceback__.tb_lineno}")
            raise

    def _generate_topic_dialogue(self, topic, host, expert, min_dialogues=8):
        """为单个话题生成对话"""
        try:
            prompts = get_dialogue_prompts()
            strategy = prompts.get('strategy', 'balanced')
            max_dialogues = prompts.get('max_dialogues', min_dialogues * 2)
            
            target_dialogues = min(min_dialogues, max_dialogues // 2)
            
            prompt = get_topic_dialogue_prompt(
                topic, 
                host, 
                expert, 
                target_dialogues,
                strategy=strategy
            )

            # 添加重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.chat.completions.create(
                        model="glm-4-plus",
                        messages=[
                            {"role": "system", "content": "你是一个严格遵守 JSON 格式的对话生成专家。"},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                        max_tokens=40000
                    )
                    
                    content = response.choices[0].message.content.strip()
                    content = self._clean_response(content)
                    
                    result = json.loads(content)
                    self._validate_dialogue_result(result, target_dialogues, max_dialogues)
                    
                    return result
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    continue
                    
        except Exception as e:
            print(f"生成话题对话失败: {str(e)}")
            return self._get_default_dialogue(topic)

    def _generate_transitions(self, prev_topic, next_topic, host, expert):
        """生成话题之间的过渡对话"""
        try:
            expert_surname = expert[0] if expert else '李'
            
            prompt = f"""请生成一段自然的过渡对话，从"{prev_topic}"过渡到"{next_topic}"：

要求：
1. 生成2-3段对话（4-6句话）
2. 过渡要自然流畅
3. 可以用一个案例或故事作为桥梁
4. 保持对话的专业性和趣味性

⚠️ 必须严格按照以下JSON格式返回：
{{
    "script": [
        {{"role": "interviewer", "content": "主持人的对话内容"}},
        {{"role": "expert", "content": "专家的对话内容"}}
    ]
}}"""

            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {"role": "system", "content": "你是一个专业的播客对话生成专家。必须返回正确的JSON格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=10000
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_response(content)
            
            result = json.loads(content)
            self._validate_dialogue_result(result, 2, 6)
            
            return result
            
        except Exception as e:
            print(f"生成过渡对话失败: {str(e)}")
            return self._get_default_transition(prev_topic, next_topic)

    def _generate_opening_closing(self, content, host, expert, is_opening=True):
        """生成开场或结束对话"""
        try:
            expert_surname = expert[0] if expert else '李'
            
            prompt = f"""请生成一段{'开场' if is_opening else '结束'}对话，要求专业性和趣味性兼具！

内容主题：{content}

对话要求：
1. 生成3-4段对话（6-8句话）
2. {'开场要吸引听众注意力' if is_opening else '结束要让听众意犹未尽'}
3. 对话要自然流畅，不做作
4. 要体现主持人和专家的专业性

⚠️ 必须严格按照以下JSON格式返回：
{{
    "script": [
        {{"role": "interviewer", "content": "主持人的对话内容"}},
        {{"role": "expert", "content": "专家的对话内容"}}
    ]
}}"""

            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {"role": "system", "content": "你是一个专业的播客对话生成专家。必须返回正确的JSON格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=20000
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_response(content)
            
            result = json.loads(content)
            self._validate_dialogue_result(result, 3, 8)
            
            return result
            
        except Exception as e:
            print(f"生成{'开场' if is_opening else '结束'}对话失败: {str(e)}")
            return self._get_default_opening_closing(host, expert, is_opening)

    def _optimize_final_dialogue(self, script, content, key_points):
        """优化最终对话内容"""
        try:
            prompt = f"""请优化以下播客对话，使其更加自然流畅：

当前对话：
{json.dumps(script, ensure_ascii=False, indent=2)}

主要知识点：
{json.dumps(key_points, ensure_ascii=False, indent=2)}

要求：
1. 保持原有对话的主要内容和风格
2. 在关键话题处补充更多互动和深度讨论
3. 确保对话自然流畅
4. 适当添加案例和数据支持
5. 保持专业性和趣味性的平衡

请返回优化后的完整对话，必须使用JSON格式。"""

            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=[
                    {"role": "system", "content": "你是一个专业的播客对话优化专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=40000
            )
            
            content = response.choices[0].message.content.strip()
            content = self._clean_response(content)
            
            result = json.loads(content)
            return result
            
        except Exception as e:
            print(f"优化对话失败: {str(e)}")
            return {"script": script}

    def _clean_response(self, content):
        """清理API响应内容"""
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        return content

    def _validate_dialogue_result(self, result, min_dialogues, max_dialogues):
        """验证对话生成结果"""
        if not isinstance(result, dict) or 'script' not in result:
            raise ValueError("返回格式错误：缺少 script 字段")
        
        if not isinstance(result['script'], list):
            raise ValueError("script 必须是数组")
        
        if len(result['script']) < min_dialogues:
            raise ValueError(f"对话数量不足：需要至少{min_dialogues}句")
            
        # 如果超过最大限制，只保留前max_dialogues句对话
        if len(result['script']) > max_dialogues:
            result['script'] = result['script'][:max_dialogues]

    def _get_default_dialogue(self, topic):
        """获取默认对话内容"""
        return {
            "script": [
                {
                    "role": "interviewer",
                    "content": f"让我们来讨论{topic['main']}这个话题。"
                },
                {
                    "role": "expert",
                    "content": f"好的，{topic['main']}确实是一个很重要的话题。"
                }
            ]
        }

    def _get_default_transition(self, prev_topic, next_topic):
        """获取默认过渡对话"""
        return {
            "script": [
                {
                    "role": "interviewer",
                    "content": f"说到{prev_topic}，让我们继续来聊聊{next_topic}。"
                },
                {
                    "role": "expert", 
                    "content": f"是的，{next_topic}确实是一个很有趣的话题。"
                }
            ]
        }

    def _get_default_opening_closing(self, host, expert, is_opening):
        """获取默认开场或结束对话"""
        if is_opening:
            return {
                "script": [
                    {
                        "role": "interviewer",
                        "content": f"大家好，欢迎收听今天的节目。我是{host}，今天我们邀请到了{expert}教授。"
                    },
                    {
                        "role": "expert",
                        "content": f"大家好，我是{expert}，很高兴和大家分享。"
                    }
                ]
            }
        else:
            return {
                "script": [
                    {
                        "role": "interviewer",
                        "content": f"感谢{expert}教授今天的精彩分享。"
                    },
                    {
                        "role": "expert",
                        "content": "谢谢大家的收听，希望今天的分享对大家有帮助。"
                    }
                ]
            }