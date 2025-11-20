#!/usr/bin/env python3
"""
MCP服务器测试脚本

这个脚本演示了如何通过stdio方式测试MCP服务器。
提供了两种测试方法：
1. 使用MCP Inspector（推荐）
2. 使用Python客户端（需要MCP SDK支持）
"""

import asyncio
import json
import sys
import subprocess
import os


def test_with_inspector():
    """使用MCP Inspector测试服务器（推荐方法）"""
    print("""
╔════════════════════════════════════════════════════════════╗
║      方法1: 使用 MCP Inspector 测试（推荐）                ║
╚════════════════════════════════════════════════════════════╝

MCP Inspector 是一个交互式工具，可以可视化测试MCP服务器。

步骤：
1. 运行以下命令启动 Inspector:
   
   npx @modelcontextprotocol/inspector

2. 在 Inspector 界面中：
   - 选择 "stdio" 连接方式
   - 设置命令为: python
   - 设置参数为: ["-m", "arxiv_mcp_server"]
   - 点击连接

3. 连接成功后，您可以：
   - 查看所有可用的工具
   - 查看所有可用的提示
   - 测试每个工具的功能
   - 查看请求和响应的详细信息

现在启动 Inspector...
    """)
    
    try:
        # 尝试启动 Inspector
        subprocess.run(["npx", "-y", "@modelcontextprotocol/inspector"], check=True)
    except subprocess.CalledProcessError:
        print("❌ 无法启动 Inspector，请手动运行: npx @modelcontextprotocol/inspector")
    except FileNotFoundError:
        print("❌ 未找到 npx，请先安装 Node.js")
        print("   或者访问: https://github.com/modelcontextprotocol/inspector")


async def test_with_python_client():
    """使用Python客户端测试服务器"""
    print("""
╔════════════════════════════════════════════════════════════╗
║      方法2: 使用 Python 客户端测试                        ║
╚════════════════════════════════════════════════════════════╝

注意: 这个方法需要MCP SDK的客户端支持。
如果遇到导入错误，请使用上面的 Inspector 方法。
    """)
    
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
    except ImportError as e:
        print(f"❌ 无法导入MCP客户端库: {e}")
        print("   请使用上面的 Inspector 方法进行测试")
        return
    
    # 配置服务器参数
    server_params = StdioServerParameters(
        command=sys.executable,  # 使用当前Python解释器
        args=["-m", "arxiv_mcp_server"],
        env=os.environ.copy()
    )
    
    print("🚀 启动MCP服务器测试...")
    print("=" * 60)
    
    try:
        # 创建stdio客户端连接
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 初始化服务器
                print("\n1️⃣ 初始化服务器...")
                init_result = await session.initialize()
                init_data = init_result.model_dump()
                server_info = init_data.get("serverInfo", {})
                print("   ✅ 服务器初始化成功")
                if server_info:
                    print(f"   - 服务器名称: {server_info.get('name', '未知')}")
                    print(f"   - 服务器版本: {server_info.get('version', '未知')}")
                else:
                    print(f"   - 初始化返回字段: {list(init_data.keys())}")
                
                # 列出可用工具
                print("\n2️⃣ 列出可用工具...")
                tools = await session.list_tools()
                print(f"   ✅ 找到 {len(tools.tools)} 个工具:")
                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description}")
                
                # 列出可用提示
                print("\n3️⃣ 列出可用提示...")
                prompts = await session.list_prompts()
                print(f"   ✅ 找到 {len(prompts.prompts)} 个提示:")
                for prompt in prompts.prompts:
                    print(f"   - {prompt.name}: {prompt.description}")
                
                # 测试搜索工具
                print("\n4️⃣ 测试搜索工具 (search_papers)...")
                search_result = await session.call_tool(
                    "search_papers",
                    arguments={
                        "query": "transformer",
                        "max_results": 3
                    }
                )
                print(f"   ✅ 搜索完成")
                if search_result.content:
                    # 只显示前500个字符
                    result_text = search_result.content[0].text[:500]
                    print(f"   📄 结果预览: {result_text}...")
                
                # 测试列出已下载的论文
                print("\n5️⃣ 测试列出已下载的论文 (list_papers)...")
                list_result = await session.call_tool(
                    "list_papers",
                    arguments={}
                )
                print(f"   ✅ 列出完成")
                if list_result.content:
                    result_text = list_result.content[0].text[:300]
                    print(f"   📄 结果: {result_text}...")
                
                print("\n" + "=" * 60)
                print("✅ 所有测试完成！")
                
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 提示: 如果遇到问题，建议使用 MCP Inspector 方法")


def show_manual_test():
    """显示手动测试方法"""
    print("""
╔════════════════════════════════════════════════════════════╗
║      方法3: 手动测试服务器启动                             ║
╚════════════════════════════════════════════════════════════╝

您可以手动启动服务器来验证它是否能正常运行：

1. 直接运行服务器:
   python -m arxiv_mcp_server
   或
   arxiv-mcp-server

2. 服务器启动后会等待通过stdin接收JSON-RPC请求。
   如果没有任何输入，服务器会一直运行。

3. 要测试服务器，您需要发送符合MCP协议的JSON-RPC消息。
   这通常由MCP客户端（如Claude Desktop或Inspector）完成。

4. 按 Ctrl+C 可以停止服务器。
    """)


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║          ArXiv MCP 服务器测试工具                           ║
╚════════════════════════════════════════════════════════════╝

请选择测试方法:
1. 使用 MCP Inspector（推荐，交互式界面）
2. 使用 Python 客户端（需要MCP SDK支持）
3. 查看手动测试方法
4. 退出

注意: 确保已经安装了所有依赖:
  uv pip install -e ".[test]"
    """)
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == "1":
        test_with_inspector()
    elif choice == "2":
        asyncio.run(test_with_python_client())
    elif choice == "3":
        show_manual_test()
    elif choice == "4":
        print("退出...")
    else:
        print("无效选择，退出...")

