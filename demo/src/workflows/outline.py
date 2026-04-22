"""灵感到大纲的工作流"""
from typing import Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from src.models.llm import get_llm


class OutlineGenerator:
    """大纲生成器 - 使用 Langchain + vLLM"""
    
    def __init__(self):
        self.llm = get_llm()
        self._setup_chains()
    
    def _setup_chains(self):
        """设置 Langchain 链"""
        
        # 链 1: 概念扩展 - 从短创意扩展到核心概念
        self.concept_prompt = PromptTemplate(
            input_variables=["idea"],
            template="""你是一个专业的小说编剧。用户给了一个创意灵感，你需要将其扩展成 200 字的核心概念说明。

灵感: {idea}

请从以下几个维度阐述这个故事：
1. 核心冲突：故事的主要矛盾点是什么？
2. 主角背景：主角是谁？面临什么困境？
3. 世界观：故事发生在什么背景下？
4. 终局：这个故事的结局会是什么？

核心概念："""
        )
        self.concept_chain = LLMChain(llm=self.llm, prompt=self.concept_prompt)
        
        # 链 2: 大纲生成 - 生成五幕式大纲
        self.outline_prompt = PromptTemplate(
            input_variables=["concept"],
            template="""基于以下书籍概念，生成一个五幕式的故事大纲（每幕 50-100 字）：

概念：{concept}

请按照这个格式生成大纲：

第一幕 (起) - 引入设定与主角：
[内容]

第二幕 (承) - 冲突升级：
[内容]

第三幕 (转) - 高潮：
[内容]

第四幕 (合) - 反转：
[内容]

第五幕 (结) - 落笔：
[内容]

"""
        )
        self.outline_chain = LLMChain(llm=self.llm, prompt=self.outline_prompt)
    
    async def generate(self, idea: str, detailed: bool = False) -> dict:
        """
        生成大纲
        
        Args:
            idea: 用户输入的创意灵感
            detailed: 是否生成详细大纲
        
        Returns:
            包含概念和大纲的字典
        """
        # 第一步：扩展概念
        concept = await self.concept_chain.arun(idea=idea)
        
        # 第二步：生成大纲
        outline = await self.outline_chain.arun(concept=concept)
        
        return {
            "idea": idea,
            "concept": concept,
            "outline": outline,
            "status": "success",
            "word_count": len(outline)
        }
    
    def generate_sync(self, idea: str) -> dict:
        """同步版本（用于简单演示）"""
        concept = self.concept_chain.run(idea=idea)
        outline = self.outline_chain.run(concept=concept)
        
        return {
            "idea": idea,
            "concept": concept,
            "outline": outline,
            "status": "success",
            "word_count": len(outline)
        }


def get_outline_generator() -> OutlineGenerator:
    """工厂函数"""
    return OutlineGenerator()
