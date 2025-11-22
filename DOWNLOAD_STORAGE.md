# MCP 文件下载和存储说明

## 📥 如何下载文件

### 方法 1：通过 MCP 工具调用

使用 `download_paper` 工具下载论文：

```python
# 在 MCP 客户端中调用
result = await session.call_tool(
    "download_paper",
    arguments={
        "paper_id": "2401.12345"  # arXiv 论文 ID
    }
)
```

### 方法 2：通过 Prompt 自动下载

当使用 prompts（如 `deep-paper-analysis`）时，AI 会自动调用 `download_paper` 工具来下载需要的论文。

---

## 📂 文件存储位置

### 默认存储路径

**默认情况下，文件存储在：**

```
~/.arxiv-mcp-server/papers/
```

- `~` 表示用户主目录
- 在 macOS/Linux 上通常是：`/Users/你的用户名/.arxiv-mcp-server/papers/`
- 在 Windows 上通常是：`C:\Users\你的用户名\.arxiv-mcp-server\papers\`

### 自定义存储路径

可以通过以下方式自定义存储位置：

#### 方法 1：环境变量

```bash
export ARXIV_STORAGE_PATH="/path/to/your/papers"
```

#### 方法 2：命令行参数

启动 MCP 服务器时指定：

```bash
python -m arxiv_mcp_server --storage-path /path/to/your/papers
```

或在 MCP 客户端配置中：

```json
{
  "mcpServers": {
    "arxiv-mcp-server-cuhksz": {
      "command": "python",
      "args": [
        "-m",
        "arxiv_mcp_server",
        "--storage-path",
        "/path/to/your/papers"
      ]
    }
  }
}
```

---

## 📄 存储的文件格式

### 存储的文件类型

1. **Markdown 文件（.md）**：论文的 Markdown 格式内容
   - 文件名格式：`{paper_id}.md`
   - 例如：`2401.12345.md`
   - **这是最终保存的文件，会被保留**

2. **PDF 文件（.pdf）**：临时下载的 PDF 文件
   - 文件名格式：`{paper_id}.pdf`
   - 例如：`2401.12345.pdf`
   - **转换完成后会被自动删除**

### 下载和转换流程

```
1. 下载 PDF 文件
   └─> 保存到: {storage_path}/{paper_id}.pdf

2. 转换为 Markdown
   └─> 使用 pymupdf4llm 库转换
   └─> 保存到: {storage_path}/{paper_id}.md

3. 删除 PDF 文件
   └─> 转换完成后自动清理 PDF
```

---

## 🔍 文件路径示例

假设论文 ID 是 `2401.12345`，默认存储路径下：

```
~/.arxiv-mcp-server/papers/
├── 2401.12345.md    ← 最终保存的 Markdown 文件
└── (2401.12345.pdf) ← 临时文件，转换后删除
```

### 获取完整路径的方法

在代码中，文件路径通过以下方式获取：

```python
from arxiv_mcp_server.config import Settings

settings = Settings()
storage_path = settings.STORAGE_PATH
# 例如: /Users/liyao/.arxiv-mcp-server/papers

paper_path = storage_path / "2401.12345.md"
# 例如: /Users/liyao/.arxiv-mcp-server/papers/2401.12345.md
```

---

## 📋 下载状态跟踪

### 下载状态类型

下载过程有以下状态：

1. **downloading**：正在下载 PDF
2. **converting**：正在将 PDF 转换为 Markdown
3. **success**：下载和转换完成
4. **error**：下载或转换失败

### 检查下载状态

可以检查论文的下载状态：

```python
result = await session.call_tool(
    "download_paper",
    arguments={
        "paper_id": "2401.12345",
        "check_status": True  # 只检查状态，不下载
    }
)
```

返回的状态信息包括：
- `status`：当前状态
- `started_at`：开始时间
- `completed_at`：完成时间（如果已完成）
- `error`：错误信息（如果有错误）

---

## 🗂️ 文件管理

### 列出已下载的论文

使用 `list_papers` 工具查看所有已下载的论文：

```python
result = await session.call_tool("list_papers", arguments={})
```

这会返回所有已下载论文的 ID 列表。

### 读取论文内容

使用 `read_paper` 工具读取已下载的论文：

```python
result = await session.call_tool(
    "read_paper",
    arguments={
        "paper_id": "2401.12345"
    }
)
```

这会从存储路径读取 `{paper_id}.md` 文件的内容。

---

## 🔧 技术细节

### 存储路径的确定逻辑

代码中的存储路径确定顺序：

1. **首先检查命令行参数**：`--storage-path /path/to/papers`
2. **然后检查环境变量**：`ARXIV_STORAGE_PATH`
3. **最后使用默认路径**：`~/.arxiv-mcp-server/papers`

### 文件命名规则

- 文件名 = `{paper_id}{suffix}`
- `paper_id`：arXiv 论文 ID（例如 "2401.12345"）
- `suffix`：文件扩展名（`.md` 或 `.pdf`）

### 目录自动创建

如果存储目录不存在，代码会自动创建：

```python
storage_path.mkdir(parents=True, exist_ok=True)
```

这意味着会创建所有必要的父目录。

---

## 📝 实际使用示例

### 示例 1：下载一篇论文

```python
# 1. 调用下载工具
result = await session.call_tool(
    "download_paper",
    arguments={"paper_id": "2401.12345"}
)

# 2. 文件会保存在：
# ~/.arxiv-mcp-server/papers/2401.12345.md
```

### 示例 2：使用自定义路径

```bash
# 启动服务器时指定路径
python -m arxiv_mcp_server --storage-path /Users/liyao/my-papers
```

文件会保存在：`/Users/liyao/my-papers/2401.12345.md`

### 示例 3：在 Claude Desktop 中配置

```json
{
  "mcpServers": {
    "arxiv-mcp-server-cuhksz": {
      "command": "python",
      "args": [
        "-m",
        "arxiv_mcp_server",
        "--storage-path",
        "/Users/liyao/Documents/arxiv-papers"
      ],
      "env": {
        "ARXIV_STORAGE_PATH": "/Users/liyao/Documents/arxiv-papers"
      }
    }
  }
}
```

---

## ⚠️ 注意事项

1. **PDF 文件会被删除**：转换完成后，PDF 文件会被自动删除，只保留 Markdown 文件
2. **已存在的文件**：如果论文已经下载过，不会重复下载
3. **并发下载**：如果同一篇论文正在下载，会返回当前状态而不是重新下载
4. **文件权限**：确保存储路径有写入权限
5. **磁盘空间**：Markdown 文件通常比 PDF 小，但仍需注意磁盘空间

---

## 🔗 相关工具

- `download_paper`：下载论文
- `list_papers`：列出已下载的论文
- `read_paper`：读取论文内容
- `search_papers`：搜索论文（不下载）

