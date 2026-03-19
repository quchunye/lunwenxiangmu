# ✅ Blender MCP 配置指南

**项目**: BlenderMCP - Blender Model Context Protocol Integration  
**GitHub**: https://github.com/ahujasid/blender-mcp  
**版本**: 1.5.5  
**配置时间**: 2026-03-02

---

## 📋 项目说明

**BlenderMCP** 连接 Blender 到 Claude AI，通过 MCP 协议让 AI 可以直接控制 Blender：

### 功能
- ✅ 双向通信：Claude ↔ Blender
- ✅ 对象操作：创建、修改、删除 3D 对象
- ✅ 材质控制：应用和修改材质/颜色
- ✅ 场景检查：获取详细场景信息
- ✅ 代码执行：在 Blender 中运行任意 Python 代码
- ✅ 资产下载：Poly Haven 模型/纹理/HDRI
- ✅ AI 生成 3D 模型：Hyper3D Rodin

---

## 🔧 安装步骤

### 前提条件

1. ✅ **Blender 3.0+** - 已安装
2. ⚠️ **Python 3.10+** - 需要确认
3. ❌ **uv 包管理器** - 需要安装

---

### 步骤 1: 安装 uv（必需！）

#### Windows 安装

**方法 A: 使用 PowerShell 脚本（推荐）**

打开 PowerShell，运行：
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

然后添加到用户 PATH：
```powershell
$localBin = "$env:USERPROFILE\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
[Environment]::SetEnvironmentVariable("Path", "$userPath;$localBin", "User")
```

**方法 B: 手动下载**

1. 访问：https://github.com/astral-sh/uv/releases
2. 下载：`uv-x86_64-pc-windows-msvc.zip`
3. 解压到：`C:\Users\曲\AppData\Local\uv\`
4. 添加到 PATH

**验证安装**：
```bash
uv --version
```

---

### 步骤 2: 安装 Blender 插件

1. 下载 `addon.py` 文件：
   - GitHub: https://github.com/ahujasid/blender-mcp/blob/main/addon.py
   - 或直接下载：https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py

2. 在 Blender 中安装：
   - 打开 Blender
   - 编辑 > 偏好设置 > 插件
   - 点击"安装..."
   - 选择 `addon.py`
   - 勾选启用 "Interface: Blender MCP"

---

### 步骤 3: 配置 MCP 服务器

#### 在 IDE 中配置

**编辑配置文件**（Claude Desktop 或 Cursor）：

**Windows 用户**（Cursor）：
```json
{
    "mcpServers": {
        "blender": {
            "command": "cmd",
            "args": [
                "/c",
                "uvx",
                "blender-mcp"
            ]
        }
    }
}
```

**通用配置**：
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": [
                "blender-mcp"
            ]
        }
    }
}
```

**禁用遥测**（可选）：
```json
{
    "mcpServers": {
        "blender": {
            "command": "uvx",
            "args": ["blender-mcp"],
            "env": {
                "DISABLE_TELEMETRY": "true"
            }
        }
    }
}
```

---

### 步骤 4: 启动服务

#### 在 Blender 中
1. 打开 Blender
2. 按 `N` 打开侧边栏
3. 找到 "BlenderMCP" 标签
4. 点击 "Connect to Claude"
5. （可选）勾选 "Poly haven" 如果需要资产下载

#### 在 IDE 中
- 重启 IDE（Claude Desktop 或 Cursor）
- MCP 服务器会自动启动

---

## 🎯 使用示例

### 示例命令

**创建场景**：
```
"Create a low poly scene in a dungeon, with a dragon guarding a pot of gold"
```

**添加对象**：
```
"Create a sphere and place it above the cube"
```

**修改材质**：
```
"Make this car red and metallic"
```

**设置灯光**：
```
"Make the lighting like a studio"
```

**相机设置**：
```
"Point the camera at the scene, and make it isometric"
```

**下载资产**：
```
"Create a beach vibe using HDRIs, textures, and models like rocks and vegetation from Poly Haven"
```

**AI 生成 3D 模型**：
```
"Generate a 3D model of a garden gnome through Hyper3D"
```

---

## ⚙️ 环境变量

可以通过环境变量配置连接：

```bash
# Blender 服务器地址
export BLENDER_HOST='localhost'  # 默认：localhost
export BLENDER_PORT=9876  # 默认：9876

# 禁用遥测
export DISABLE_TELEMETRY=true
```

**远程主机**：
```bash
export BLENDER_HOST='host.docker.internal'
export BLENDER_PORT=9876
```

---

## 🔍 故障排除

### 连接问题
- ✅ 确保 Blender 插件服务器已启动
- ✅ 确保 MCP 服务器已配置
- ✅ 不要同时在 Cursor 和 Claude Desktop 中运行
- ⚠️ 第一个命令可能失败，重试即可

### 超时错误
- 简化请求
- 分步骤执行复杂操作

### Poly Haven 问题
- 如果不需要，请在 Blender 中关闭 Poly haven 复选框

### uv 未找到
- 确保 uv 已安装并添加到 PATH
- 重启 IDE

---

## 📊 技术细节

### 组件
1. **Blender 插件** (`addon.py`): 在 Blender 中创建 socket 服务器
2. **MCP 服务器** (`server.py`): 实现 MCP 协议

### 通信协议
- JSON-based 协议 over TCP sockets
- 命令：`{"type": "...", "params": {...}}`
- 响应：`{"status": "...", "result": {...}}`

### 安全考虑
⚠️ `execute_blender_code` 工具可以运行任意 Python 代码，使用前请保存工作！

---

## 🎮 下一步

### 立即可做
1. ⚠️ **安装 uv** - 使用 PowerShell 脚本
2. 📥 **下载 addon.py** - 从 GitHub
3. 🔌 **安装 Blender 插件** - 在 Blender 中
4. ⚙️ **配置 MCP** - 编辑配置文件
5. 🚀 **启动服务** - 连接测试

### 需要确认
- ✅ Python 版本是否 3.10+
- ⏳ uv 是否安装成功
- ⏳ Blender 版本是否 3.0+

---

## 📝 配置检查清单

- [ ] 安装 uv 包管理器
- [ ] 下载 addon.py 文件
- [ ] 在 Blender 中安装插件
- [ ] 启用插件
- [ ] 配置 MCP 服务器（IDE 设置）
- [ ] 重启 IDE
- [ ] 在 Blender 中启动连接
- [ ] 测试简单命令

---

**项目状态**: 🟢 活跃维护  
**最后更新**: 2026-03-02  
**配置难度**: ⭐⭐⭐ 中等（需要安装 uv）  
**推荐指数**: ⭐⭐⭐⭐⭐ 强烈推荐
