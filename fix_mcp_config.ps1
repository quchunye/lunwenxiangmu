# 修复 MCP 配置中的路径问题
$mcpConfigPath = "$env:APPDATA\Trae CN\User\mcp.json"

Write-Host "正在读取 MCP 配置文件..."
$config = Get-Content $mcpConfigPath -Raw -Encoding UTF8

# 替换旧的 blender 配置为新的配置
$oldConfig = '"blender": {\s+"command": "D:\\\\Trae CN\\\\论文\\\\.venv\\\\Scripts\\\\python.exe",\s+"args": \[\s+"d:\\\\Trae CN\\\\论文\\\\run_blender_mcp.py"\s+\]\s+}'

$newConfig = '"blender": {
    "command": "cmd",
    "args": [
      "/c",
      "\"D:\\Trae CN\\论文\\.venv\\Scripts\\python.exe\" \"d:\\Trae CN\\论文\\run_blender_mcp.py\""
    ]
  }'

$config = $config -replace $oldConfig, $newConfig

# 保存文件
$config | Out-File $mcpConfigPath -Encoding UTF8 -Force

Write-Host "✓ MCP 配置已更新" -ForegroundColor Green
Write-Host ""
Write-Host "新的 blender 配置:" -ForegroundColor Yellow
Write-Host '  "command": "cmd"'
Write-Host '  "args": ["/c", "\"D:\\Trae CN\\论文\\.venv\\Scripts\\python.exe\" \"d:\\Trae CN\\论文\\run_blender_mcp.py\""]'
Write-Host ""
Write-Host "请重启 Trae 编辑器以应用新配置" -ForegroundColor Green
Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
