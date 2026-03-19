# 📖 手动打开 Blender 并安装插件

**时间**: 2026-03-02 02:00

---

## 🚀 打开 Blender

### 方法 1: 使用开始菜单
1. 按 `Windows` 键
2. 输入 "Blender"
3. 点击 Blender 图标

### 方法 2: 桌面快捷方式
- 如果桌面有 Blender 图标，双击打开

### 方法 3: 文件资源管理器
常见位置：
- `C:\Program Files\Blender Foundation\Blender <版本>\blender.exe`
- `C:\Program Files (x86)\Blender Foundation\Blender <版本>\blender.exe`

---

## 🔧 安装 MCP 插件

### 步骤 1: 打开插件管理器

Blender 打开后：
1. 点击菜单栏：`编辑 (Edit)`
2. 选择：`偏好设置 (Preferences)`
3. 在左侧选择：`插件 (Add-ons)`

### 步骤 2: 安装插件

1. 点击 `安装... (Install...)` 按钮
2. 浏览到文件位置：
   ```
   d:\Trae CN\论文\blender_mcp_addon.py
   ```
3. 选择 `blender_mcp_addon.py`
4. 点击 `安装插件 (Install Add-on)`

### 步骤 3: 启用插件

1. 在插件列表中找到：
   - 名称：`Interface: Blender MCP`
   - 或搜索 "Blender MCP"
2. 勾选复选框 ✅ 启用插件

### 步骤 4: 保存设置

1. 点击左下角的 `齿轮图标 ⚙️`
2. 选择 `保存设置 (Save Preferences)`
   或按 `Ctrl + U`

---

## 🔌 启动 MCP 服务

### 在 Blender 中

1. 按 `N` 键打开右侧边栏
2. 找到 `BlenderMCP` 标签
3. （可选）勾选 `Poly haven` 如果需要下载资产
4. 点击 `Connect to Claude` 按钮

状态应该显示为：**已连接** 或 **Running**

---

## 🔄 重启 Claude Desktop

安装完插件并启动 MCP 服务后：

1. 完全退出 Claude Desktop
   - 右键点击任务栏图标
   - 选择 `退出` 或 `Quit`

2. 重新启动 Claude Desktop

---

## ✅ 验证配置

### 在 Claude Desktop 中

1. 打开聊天窗口
2. 查看是否有工具图标（🔨）
3. 点击工具图标，应该看到 blender 相关工具

### 测试命令

尝试发送：
```
创建一个球体
```

或英文：
```
Create a sphere
```

---

## 📊 检查清单

- [ ] 打开 Blender
- [ ] 打开偏好设置 > 插件
- [ ] 安装 blender_mcp_addon.py
- [ ] 启用插件
- [ ] 保存设置
- [ ] 按 N 打开侧边栏
- [ ] 找到 BlenderMCP 标签
- [ ] 点击 "Connect to Claude"
- [ ] 重启 Claude Desktop
- [ ] 测试命令

---

## 💡 故障排除

### 问题：找不到插件
**解决**: 
- 确认文件路径正确
- 文件应该是 `blender_mcp_addon.py`
- 重新下载：https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py

### 问题：无法连接
**解决**:
- 确保已启用插件
- 检查端口 9876 是否被占用
- 重启 Blender

### 问题：Claude 看不到工具
**解决**:
- 确保已重启 Claude Desktop
- 检查配置文件是否正确
- 确认 Blender 中已点击 "Connect to Claude"

---

**完成所有步骤后，告诉我，我会帮你验证！** 🎯
