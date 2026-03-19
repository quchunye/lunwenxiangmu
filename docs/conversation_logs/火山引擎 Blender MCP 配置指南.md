# 火山引擎 Blender MCP 配置指南

**配置时间**: 2026-03-02  
**来源**: 火山引擎智能体工具商店（ATS）
**链接**: https://www.volcengine.com/ats/mcp_detail?name=blender

---

## 📋 服务信息

**名称**: Blender MCP  
**平台**: 火山引擎智能体工具商店（ATS）  
**状态**: ⚠️ 页面显示"暂无该服务的内容"

---

## 🔧 配置步骤

### 方法 1: 通过火山引擎 ATS 平台

#### 步骤 1: 访问平台
打开浏览器访问：
```
https://www.volcengine.com/ats/
```

#### 步骤 2: 登录/注册
- 需要火山引擎账号
- 如果没有账号，需要先注册
- 可能需要企业认证

#### 步骤 3: 查找 Blender MCP
- 在 ATS 商店中搜索 "blender"
- 查看是否有可用的 MCP 服务

#### 步骤 4: 安装和配置
根据平台提供的指引进行配置

---

### 方法 2: 使用 npm 安装（如果有）

如果火山引擎提供了 npm 包，可能是：

```bash
# 可能的包名（需要确认）
npm install -g @volcengine/mcp-blender
# 或
npm install -g @ats/mcp-blender
# 或
npm install -g volcengine-blender-mcp
```

**注意**: 以上包名是猜测，需要官方文档确认

---

### 方法 3: 使用 SSE 或 HTTP 连接

如果 Blender MCP 是远程服务：

**配置示例**（在 IDE 的 MCP 设置中）：

```json
{
  "mcpServers": {
    "volcengine-blender": {
      "type": "sse",
      "url": "https://ats.volcengine.com/mcp/blender/sse"
    }
  }
}
```

或

```json
{
  "mcpServers": {
    "volcengine-blender": {
      "type": "http",
      "url": "https://ats.volcengine.com/mcp/blender"
    }
  }
}
```

---

## ⚠️ 当前问题

### 页面显示"暂无该服务的内容"

**可能原因**:
1. 服务已下架或暂停
2. 需要特殊权限才能访问
3. 链接已失效
4. 服务名称不正确

---

## 💡 解决方案

### 1. 联系火山引擎
- **业务咨询**: service@volcengine.com
- **电话**: 400-850-0030
- **地址**: 北京市海淀区北三环西路甲 18 号院大钟寺广场 1 号楼

### 2. 查找替代方案

**类似的 MCP 服务**:
- **3D 建模类**: 搜索其他 3D 工具 MCP
- **文档管理类**: @aindreyway/mcp-codex-keeper（需要 uv）
- **文件操作类**: 各种文件管理 MCP

### 3. 使用已可用的 MCP

**当前可用**:
- ✅ 印象笔记 MCP（yxbj-mcp）- 正常工作

---

## 📝 需要的信息

为了帮你正确配置，需要：

1. **确认服务状态**
   - Blender MCP 是否还在运营？
   - 是否需要特殊权限？

2. **获取正确的配置方式**
   - 官方文档链接
   - 安装命令
   - 配置参数

3. **或者考虑替代方案**
   - 放弃 Blender MCP
   - 使用其他可用的 MCP 服务

---

## 🎯 下一步建议

### 选项 A: 继续尝试配置
1. 联系火山引擎客服确认
2. 获取正确的安装方式
3. 配置并测试

### 选项 B: 使用其他 MCP
1. 专注于印象笔记 MCP（已可用）
2. 安装 uv 修复 aindrey MCP
3. 寻找其他开源 MCP 服务

### 选项 C: 等待
1. 等待 Blender MCP 恢复服务
2. 等待官方发布新文档

---

**当前状态**: ⏳ 等待更多信息或确认  
**可用替代**: 印象笔记 MCP ✅  
**记录时间**: 2026-03-02 01:20
