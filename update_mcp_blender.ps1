$mcpConfigPath = "$env:APPDATA\Trae CN\User\mcp.json"

Write-Host "正在读取 MCP 配置文件..." -ForegroundColor Cyan
$config = Get-Content $mcpConfigPath -Raw -Encoding UTF8

Write-Host "正在更新 blender 配置..." -ForegroundColor Yellow

# 替换 blender 配置
$oldConfig = '"blender": {\s+"command": "D:\\\\Trae CN\\\\论文\\\\.venv\\\\Scripts\\\\python.exe",\s+"args": \[\s+"d:\\\\Trae CN\\\\论文\\\\run_blender_mcp.py"\s+\]\s+}'

$newConfig = '"blender": {
    "command": "cmd",
    "args": [
      "/c",
      "\"D:\\Trae CN\\论文\\.venv\\Scripts\\python.exe\" \"d:\\Trae CN\\论文\\run_blender_mcp.py\""
    ]
  }'

$config = $config -replace $oldConfig, $newConfig

Write-Host "正在保存配置..." -ForegroundColor Cyan
$config | Out-File $mcpConfigPath -Encoding UTF8 -Force

Write-Host ""
Write-Host "✅ MCP 配置已成功更新!" -ForegroundColor Green
Write-Host ""
Write-Host "修改内容:" -ForegroundColor Yellow
Write-Host '  旧配置：'
Write-Host '    "command": "D:\Trae CN\论文\.venv\Scripts\python.exe"'
Write-Host '  新配置：'
Write-Host '    "command": "cmd"'
Write-Host '    "args": ["/c", "python.exe 路径 run_blender_mcp.py 路径"]'
Write-Host ""
Write-Host "请重启 Trae 编辑器以应用更改" -ForegroundColor Green
Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
