# BlenderMCP 插件安装脚本
$addonsPath = "C:\Users\曲\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons"
$sourceFile = "d:\Trae CN\论文\blender_mcp_addon.py"

# 检查 addons 目录是否存在，不存在则创建
if (!(Test-Path $addonsPath)) {
    Write-Host "正在创建 addons 目录..."
    New-Item -ItemType Directory -Path $addonsPath -Force | Out-Null
    Write-Host "✓ addons 目录已创建：$addonsPath"
} else {
    Write-Host "✓ addons 目录已存在"
}

# 复制插件文件
Write-Host "正在复制插件文件..."
try {
    Copy-Item $sourceFile -Destination $addonsPath -Force
    Write-Host "✓ 插件已成功安装到：$addonsPath"
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "安装成功！" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步操作："
    Write-Host "1. 打开 Blender"
    Write-Host "2. 点击 Edit → Preferences → Add-ons"
    Write-Host "3. 搜索 'Blender MCP'"
    Write-Host "4. 勾选插件启用"
    Write-Host "5. 在 3D 视图右侧边栏（按 N 键）找到 BlenderMCP 面板"
    Write-Host ""
} catch {
    Write-Host "复制失败：$($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "请手动复制文件：" -ForegroundColor Yellow
    Write-Host "源文件：$sourceFile"
    Write-Host "目标目录：$addonsPath"
}

Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
