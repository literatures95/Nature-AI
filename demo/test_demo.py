"""测试脚本"""
import asyncio
from src.workflows.outline import get_outline_generator
from src.models.llm import get_llm


async def test_llm():
    """测试 LLM 连接"""
    print("[测试 1] LLM 基础连接...")
    llm = get_llm()
    print(f"  LLM 类型: {llm._llm_type}")
    print(f"  模型: {llm.model_name}")
    print("  ✓ LLM 已初始化")


async def test_outline_generator():
    """测试大纲生成器"""
    print("\n[测试 2] 大纲生成器...")
    
    generator = get_outline_generator()
    
    test_ideas = [
        "一个少年在魔法学院的冒险",
        "穿越到古代成为名妓的女主",
        "机器人获得意识后的觉醒",
    ]
    
    for idea in test_ideas:
        print(f"\n  输入: {idea}")
        try:
            result = await generator.generate(idea)
            print(f"  ✓ 大纲生成成功")
            print(f"  概念:\n{result['concept'][:100]}...")
            print(f"  字数: {result['word_count']}")
        except Exception as e:
            print(f"  ✗ 错误: {e}")


async def main():
    print("=" * 50)
    print("Nature AI Demo - 本地测试")
    print("=" * 50)
    
    try:
        await test_llm()
        await test_outline_generator()
        print("\n" + "=" * 50)
        print("所有测试完成！")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
