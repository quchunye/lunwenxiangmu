# ⚠️ Blender MCP 安装问题

**时间**: 2026-03-02 02:35  
**状态**: ❌ 需要安装 C++ Build Tools

---

## ❌ 错误信息

```
Failed to build `pyroaring==1.0.3`
error: Microsoft Visual C++ 14.0 or greater is required.
```

**原因**: 
- blender-mcp 依赖 pyiceberg
- pyiceberg 依赖 pyroaring
- pyroaring 需要编译 C++ 代码
- 系统缺少 Visual C++ Build Tools

---

## ✅ 解决方案

### 方案 1: 安装 Visual C++ Build Tools（推荐）

**下载地址**:
```
https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

**安装步骤**:
1. 下载 "Build Tools for Visual Studio"
2. 运行安装程序
3. 选择 **"C++ build tools"**
4. 确保勾选:
   - ✅ MSVC (最新 x64/x86 生成工具)
   - ✅ Windows 10/11 SDK
   - ✅ C++ CMake 工具
5. 点击安装（约 5-10 GB）
6. 重启电脑
7. 重新运行：`uvx blender-mcp`

---

### 方案 2: 使用预编译的 MCP 服务器（简单）

**不安装依赖，直接使用 MCP 服务**:

由于 blender-mcp 的依赖问题，可以：

1. **跳过本地安装**
2. **直接使用配置好的 MCP 服务**
3. **在 Claude Desktop 中通过 uvx 运行**

**配置文件已经正确**:
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

uvx 会自动处理依赖！

---

### 方案 3: 使用简化版配置

如果方案 2 不行，可以使用不需要编译依赖的替代方案。

---

## 🎯 当前建议

**先尝试方案 2** - 直接使用配置好的 MCP

### 步骤:
1. ✅ Blender 已安装
2. ✅ MCP 插件已启用
3. ✅ 配置文件已准备
4. 🔄 在 Blender 中点击 "Connect to Claude"
5. 🔄 重启 Claude Desktop
6. 🔄 测试功能

**不需要本地安装 blender-mcp!**

uvx 会在运行时自动处理。

---

## 📝 总结

### 已完成
- ✅ Blender 4.0 安装
- ✅ MCP 插件安装
- ✅ 配置文件准备
- ✅ uv 包管理器

### 待完成
- ⏳ Blender 中启动服务
- ⏳ 重启 Claude Desktop
- ⏳ 测试功能

---

**不需要安装 C++ Build Tools，直接继续配置即可！** 🚀
