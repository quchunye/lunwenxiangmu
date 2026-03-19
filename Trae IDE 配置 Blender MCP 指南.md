# 🛠️ Trae IDE 配置 Blender MCP 指南

**时间**: 2026-03-02 02:40  
**目标**: 在 Trae IDE 中通过 MCP 连接 Blender

---

## 📋 配置步骤

### 方法 1: Trae IDE 设置界面（推荐）

#### 步骤 1: 打开 Trae 设置
1. 打开 Trae IDE
2. 点击 **设置** (Settings)
3. 找到 **MCP** 或 **AI 助手** 相关设置

#### 步骤 2: 添加 MCP 服务器
点击 **"添加 MCP 服务器"** 或 **"Add MCP Server"**

#### 步骤 3: 填写配置

**服务器名称**: `blender`

**命令**: `cmd`

**参数**: 
```
/c, uvx, blender-mcp
```

**完整配置 JSON**:
```json
{
    "mcpServers": {
        "blender": {
            "command": "cmd",
            "args": ["/c", "uvx", "blender-mcp"]
        },
        "yinxiang": {
            "command": "npx",
            "args": ["-y", "yxbj-mcp"]
        }
    }
}
```

---

### 方法 2: 项目配置文件

如果 Trae 支持项目级 MCP 配置，可以在项目根目录创建：

**文件**: `.trae/mcp.json` 或 `.cursor/mcp.json`

**内容**:
```json
{
    "mcpServers": {
        "blender": {
            "command": "cmd",
            "args": ["/c", "uvx", "blender-mcp"]
        }
    }
}
```

---

## 🚀 完整配置流程

### 1. 准备工作（已完成✅）
- [x] uv 包管理器 (v0.10.7)
- [x] Blender 4.0 安装
- [x] MCP 插件安装到 Blender
- [x] 配置文件准备

### 2. 在 Trae 中配置 MCP
- [ ] 打开 Trae IDE 设置
- [ ] 找到 MCP 配置界面
- [ ] 添加 Blender MCP 服务器
- [ ] 保存配置

### 3. 启动 Blender MCP 服务
- [ ] 打开 Blender
- [ ] 按 N 打开侧边栏
- [ ] 找到 BlenderMCP 标签
- [ ] 点击 "Connect to Claude"

### 4. 重启 Trae IDE
- [ ] 完全退出 Trae
- [ ] 重新启动 Trae

### 5. 测试功能
- [ ] 在 Trae 的 AI 助手对话框中测试
- [ ] 发送命令：`创建一个球体`

---

## 📝 Trae IDE 特定配置

### 查找 MCP 设置位置

Trae IDE 的 MCP 设置通常在：

1. **设置 > AI 助手 > MCP 服务器**
2. **设置 > 扩展 > MCP**
3. **设置 > 开发者工具 > MCP**

如果找不到，可以尝试：
- 在设置中搜索 "MCP"
- 查看 Trae 的文档或更新到最新版本

---

## 🧪 测试命令

配置完成后，在 Trae 的 AI 助手中尝试：

### 基础测试
```
创建一个球体
```

```
Create a sphere
```

### 进阶测试
```
创建一个立方体，然后在它上方创建一个球体
```

```
将球体设为红色
```

```
创建一个简单的场景
```

---

## 💡 故障排除

### 问题 1: 找不到 MCP 设置
**解决**: 
- 更新 Trae IDE 到最新版本
- 查看 Trae 官方文档
- 或在项目中使用 `.cursor/mcp.json`

### 问题 2: Blender 连接失败
**解决**:
- 确保 Blender 中已点击 "Connect to Claude"
- 检查端口 9876 是否被占用
- 重启 Blender 和 Trae

### 问题 3: uvx 找不到命令
**解决**:
- 确认 uv 已安装：`uv --version`
- 确保 uv 在 PATH 中
- 重启 Trae IDE

---

## 🎯 当前状态

### 已完成
- ✅ uv 包管理器 (v0.10.7)
- ✅ Blender 4.0 安装
- ✅ MCP 插件启用
- ✅ 配置文件模板准备

### 待完成
- ⏳ 在 Trae 中添加 MCP 配置
- ⏳ 启动 Blender MCP 服务
- ⏳ 重启 Trae IDE
- ⏳ 测试功能

---

## 📚 参考配置

### 完整配置示例
```json
{
    "mcpServers": {
        "blender": {
            "command": "cmd",
            "args": ["/c", "uvx", "blender-mcp"],
            "env": {
                "BLENDER_HOST": "localhost",
                "BLENDER_PORT": "9876",
                "DISABLE_TELEMETRY": "true"
            }
        },
        "yinxiang": {
            "command": "npx",
            "args": ["-y", "yxbj-mcp"]
        }
    }
}
```

### 环境变量（可选）
- `BLENDER_HOST`: Blender 服务器地址（默认：localhost）
- `BLENDER_PORT`: 端口号（默认：9876）
- `DISABLE_TELEMETRY`: 禁用遥测（true/false）

---

## 🔗 相关链接

- Blender MCP GitHub: https://github.com/ahujasid/blender-mcp
- uv 包管理器：https://github.com/astral-sh/uv
- Trae IDE 文档：查看官方文档

---

**下一步**: 在 Trae IDE 中添加 MCP 配置！🚀
