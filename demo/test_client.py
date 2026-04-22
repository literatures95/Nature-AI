"""示例客户端 - 调用 API"""
import httpx
import json
import asyncio


async def test_api():
    """测试 API 端点"""
    
    base_url = "http://localhost:8001"
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 测试健康检查
        print("[1] 健康检查...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"  状态: {response.status_code}")
            print(f"  响应: {response.json()}")
        except Exception as e:
            print(f"  ✗ 健康检查失败: {e}")
            return
        
        print()
        
        # 测试大纲生成
        print("[2] 生成大纲...")
        
        request_data = {
            "idea": "一个年轻的剑客在乱世中寻找自己的信念",
            "detailed": False
        }
        
        print(f"  请求: {json.dumps(request_data, ensure_ascii=False)}")
        
        try:
            response = await client.post(
                f"{base_url}/outline",
                json=request_data,
                timeout=120.0
            )
            print(f"  状态: {response.status_code}")
            
            result = response.json()
            print(f"\n  概念:\n{result['concept']}\n")
            print(f"  大纲:\n{result['outline']}\n")
            print(f"  字数: {result['word_count']}")
            
        except httpx.TimeoutException:
            print("  ✗ 请求超时（vLLM 可能还在加载模型）")
        except Exception as e:
            print(f"  ✗ 错误: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Nature AI Demo - API 客户端测试")
    print("=" * 60)
    print()
    
    asyncio.run(test_api())
