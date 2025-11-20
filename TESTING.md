# MCP 服务器测试指南

## 📚 什么是 stdio_server？

`stdio_server` 是 MCP (Model Context Protocol) 服务器的一种通信方式，它使用**标准输入输出（Standard Input/Output，简称 stdio）**进行进程间通信。

### stdio 通信方式的工作原理

1. **标准输入（stdin）**: 服务器通过 `stdin` 接收来自客户端的 JSON-RPC 请求
2. **标准输出（stdout）**: 服务器通过 `stdout` 发送 JSON-RPC 响应给客户端
3. **标准错误（stderr）**: 用于日志输出，不会干扰协议通信

### 为什么使用 stdio？

- ✅ **简单**: 无需配置网络端口或套接字
- ✅ **安全**: 进程间直接通信，不暴露网络接口
- ✅ **跨平台**: 所有操作系统都支持标准输入输出
- ✅ **适合本地服务**: 特别适合在同一台机器上运行的客户端和服务器

### 代码中的实现

在 `server.py` 中：

```67:81:src/arxiv_mcp_server/server.py
async def main():
    """Run the server async context."""
    async with stdio_server() as streams:
        await server.run(
            streams[0],
            streams[1],
            InitializationOptions(
                server_name=settings.APP_NAME,
                server_version=settings.APP_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(resources_changed=True),
                    experimental_capabilities={},
                ),
            ),
        )
```

- `stdio_server()` 创建了 stdin/stdout 流
- `streams[0]` 是读取流（stdin）
- `streams[1]` 是写入流（stdout）
- 服务器通过这两个流与客户端进行 JSON-RPC 通信

## 🧪 如何测试 MCP 服务器

### 方法 1: 使用 MCP Inspector（推荐）⭐

MCP Inspector 是一个交互式工具，可以可视化测试 MCP 服务器。

#### 步骤：

1. **安装并启动 Inspector**:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

2. **配置连接**:
   - 在 Inspector 界面中选择 "stdio" 连接方式
   - **Command**: `python` (或 `python3`)
   - **Args**: `["-m", "arxiv_mcp_server"]`
   - 如果需要设置环境变量，可以添加 `env` 字段

3. **连接并测试**:
   - 点击 "Connect" 按钮
   - 连接成功后，您可以：
     - 查看所有可用的工具（Tools）
     - 查看所有可用的提示（Prompts）
     - 测试每个工具的功能
     - 查看请求和响应的 JSON 数据

#### Inspector 配置示例：

```json
{
  "command": "python",
  "args": ["-m", "arxiv_mcp_server"],
  "env": {
    "ARXIV_STORAGE_PATH": "/path/to/papers"
  }
}
```

### 方法 2: 使用 Python 测试脚本

运行提供的测试脚本：

```bash
python test_mcp_server.py
```

脚本会提供交互式菜单，让您选择测试方法。

### 方法 3: 在 Claude Desktop 中测试

如果您使用 Claude Desktop，可以在配置文件中添加服务器：

1. **找到配置文件**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **添加配置**:
   ```json
   {
     "mcpServers": {
       "arxiv-mcp-server": {
         "command": "python",
         "args": [
           "-m",
           "arxiv_mcp_server"
         ],
         "env": {
           "ARXIV_STORAGE_PATH": "~/.arxiv-mcp-server/papers"
         }
       }
     }
   }
   ```

3. **重启 Claude Desktop**，服务器会自动连接

### 方法 4: 手动验证服务器启动

验证服务器是否能正常启动：

```bash
# 运行服务器（会等待stdin输入）
python -m arxiv_mcp_server
```

如果服务器正常启动，它会：
- 等待通过 stdin 接收 JSON-RPC 请求
- 不会输出任何内容到 stdout（因为还没有收到请求）
- 日志会输出到 stderr

按 `Ctrl+C` 可以停止服务器。

## 🔍 测试服务器功能

### 可用的工具

1. **search_papers**: 搜索 arXiv 论文
   ```json
   {
     "query": "transformer",
     "max_results": 10,
     "date_from": "2023-01-01",
     "categories": ["cs.AI"]
   }
   ```

2. **download_paper**: 下载论文
   ```json
   {
     "paper_id": "2401.12345"
   }
   ```

3. **list_papers**: 列出已下载的论文
   ```json
   {}
   ```

4. **read_paper**: 读取论文内容
   ```json
   {
     "paper_id": "2401.12345"
   }
   ```

### 可用的提示

- **deep-paper-analysis**: 深度论文分析提示

## 🐛 调试技巧

### 查看服务器日志

服务器会将日志输出到 stderr。在 Inspector 中，您可以看到这些日志。

### 常见问题

1. **服务器无法启动**
   - 检查 Python 环境是否正确
   - 确认所有依赖已安装: `uv pip install -e ".[test]"`
   - 检查是否有语法错误

2. **连接失败**
   - 确认命令和参数正确
   - 检查环境变量设置
   - 查看 stderr 中的错误信息

3. **工具调用失败**
   - 检查参数格式是否正确
   - 查看服务器返回的错误消息
   - 确认网络连接（对于搜索和下载功能）

## 📖 更多资源

- [MCP 协议文档](https://modelcontextprotocol.io/)
- [MCP Inspector GitHub](https://github.com/modelcontextprotocol/inspector)
- [Claude Desktop MCP 配置](https://claude.ai/docs/mcp)

