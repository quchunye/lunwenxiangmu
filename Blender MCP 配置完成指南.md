# ✅ Blender MCP 配置完成指南

**配置时间**: 2026-03-02 01:45  
**状态**: 🟡 需要手动完成最后一步

---

## 📋 已完成的工作

### ✅ 1. uv 包管理器安装
- **版本**: uv 0.10.7
- **状态**: 正常工作
- **验证**: `uv --version` ✅

### ✅ 2. Blender 插件下载
- **文件**: `blender_mcp_addon.py`
- **位置**: `d:\Trae CN\论文\blender_mcp_addon.py`
- **来源**: GitHub 官方仓库

### ✅ 3. 配置文件准备
- **模板**: `claude_desktop_config_template.json`
- **位置**: `d:\Trae CN\论文\`
- **内容**: 包含 Blender MCP 和印象笔记 MCP

---

## 🔧 需要手动完成的步骤

### 步骤 1: 复制配置文件

**打开文件位置**:
```
C:\Users\曲\AppData\Roaming\Claude\
```

**操作**:
1. 找到 `claude_desktop_config.json`
2. 用文本编辑器打开（如 Notepad、VS Code）
3. 复制以下内容并替换原有内容：

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
    },
    "preferences": {
        "coworkWebSearchEnabled": true,
        "coworkScheduledTasksEnabled": false,
        "sidebarMode": "chat"
    }
}
```

4. 保存文件

---

### 步骤 2: 安装 Blender 插件

1. **打开 Blender**
   - 启动 Blender 3.0 或更高版本

2. **打开插件管理器**
   - 菜单栏：编辑 (Edit) > 偏好设置 (Preferences)
   - 选择左侧：插件 (Add-ons)

3. **安装插件**
   - 点击 "安装..." (Install...) 按钮
   - 浏览到：`d:\Trae CN\论文\blender_mcp_addon.py`
   - 选择文件并点击 "安装插件"

4. **启用插件**
   - 在插件列表中找到 "Interface: Blender MCP"
   - 勾选复选框启用

5. **保存设置**
   - 点击左下角：齿轮图标 ⚙️
   - 选择 "保存设置" (Save Preferences)

---

### 步骤 3: 启动 Blender MCP 服务

1. **在 Blender 中**
   - 按 `N` 键打开右侧边栏
   - 找到 "BlenderMCP" 标签
   - （可选）勾选 "Poly haven" 如果需要下载资产
   - 点击 "Connect to Claude" 按钮

2. **重启 Claude Desktop**
   - 完全退出 Claude Desktop
   - 重新启动 Claude Desktop

---

### 步骤 4: 验证配置

**在 Claude Desktop 中**:

1. 打开聊天窗口
2. 查看是否有工具图标（锤子🔨）
3. 点击工具图标，应该看到:
   - blender 相关工具
   - 印象笔记相关工具

**测试命令**:
```
创建一个球体并放在立方体上方
```

或者英文:
```
Create a sphere and place it above the cube
```

---

## 📊 配置检查清单

- [x] ✅ uv 已安装并可用
- [x] ✅ Blender 插件已下载
- [x] ✅ 配置文件模板已准备
- [ ] ⏳ 复制配置文件到 Claude 目录
- [ ] ⏳ 在 Blender 中安装插件
- [ ] ⏳ 启用 Blender MCP 插件
- [ ] ⏳ 重启 Claude Desktop
- [ ] ⏳ 测试 Blender MCP 功能

---

## 🎯 快速验证命令

### 验证 uv
```powershell
uv --version
# 应该输出：uv 0.10.7
```

### 验证 Blender MCP 服务器
```powershell
uvx blender-mcp --help
# 应该显示帮助信息
```

### 验证印象笔记 MCP
```powershell
npx -y yxbj-mcp --help
# 应该显示帮助信息
```

---

## 💡 故障排除

### 问题 1: 找不到 uv
**解决**: 
- 确保 uv 已添加到 PATH
- 重启终端/IDE

### 问题 2: Blender 插件不显示
**解决**:
- 确认 Blender 版本 >= 3.0
- 重新安装插件
- 检查是否启用了插件

### 问题 3: 连接失败
**解决**:
- 确保 Blender 中点击了 "Connect to Claude"
- 检查端口 9876 是否被占用
- 重启 Blender 和 Claude Desktop

### 问题 4: 配置文件无法保存
**解决**:
- 确保 Claude Desktop 已完全退出
- 以管理员身份运行文本编辑器
- 或手动复制配置文件

---

## 🎮 使用示例

配置完成后，可以尝试这些命令:

### 基础操作
```
创建一个立方体
创建一个球体
创建一个圆柱体
```

### 对象操作
```
将球体移动到 (2, 0, 0)
旋转立方体 45 度
缩放对象到原来的 2 倍
```

### 材质和颜色
```
将球体设为红色
让这个对象变成金属材质
应用蓝色玻璃材质
```

### 场景创建
```
创建一个简单的房间场景
添加一个光源
设置相机角度
```

### 高级功能
```
从 Poly Haven 下载一个 HDRI
创建一个低多边形场景
生成一个 3D 模型（需要 Hyper3D 账号）
```

---

## 📝 下一步

### 完成配置后
1. ✅ 测试基础功能
2. ✅ 尝试创建简单对象
3. ✅ 探索更多功能

### 需要帮助时
- 查看 GitHub: https://github.com/ahujasid/blender-mcp
- 加入 Discord 社区
- 查看示例视频

---

**配置状态**: 🟡 等待手动完成  
**预计时间**: 5-10 分钟  
**难度**: ⭐⭐ 简单

**完成后告诉我，我会帮你验证！** 🚀
