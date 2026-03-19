# Trae 文件迁移脚本 - 从 C 盘搬到 D 盘
# 目标位置：D:\Trae CN\UserData\

$targetBase = "D:\Trae CN\UserData"
$sourcePaths = @(
    "$env:APPDATA\Trae CN",
    "$env:USERPROFILE\.trae-aicc",
    "$env:USERPROFILE\.trae-cn"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Trae 文件迁移工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否需要关闭 Trae
$traeProcesses = Get-Process -Name "Trae" -ErrorAction SilentlyContinue
if ($traeProcesses) {
    Write-Host "检测到 Trae 正在运行！" -ForegroundColor Yellow
    Write-Host "请先关闭 Trae 编辑器，然后按任意键继续..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # 再次检查
    $traeProcesses = Get-Process -Name "Trae" -ErrorAction SilentlyContinue
    if ($traeProcesses) {
        Write-Host "Trae 仍在运行，无法继续迁移" -ForegroundColor Red
        Write-Host "按任意键退出..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# 创建目标目录
Write-Host "1. 创建目标目录..." -ForegroundColor Yellow
if (!(Test-Path $targetBase)) {
    New-Item -ItemType Directory -Path $targetBase -Force | Out-Null
    Write-Host "   已创建：$targetBase" -ForegroundColor Green
} else {
    Write-Host "   目录已存在：$targetBase" -ForegroundColor Green
}

# 迁移每个目录
foreach ($sourcePath in $sourcePaths) {
    $relativePath = $sourcePath -replace [regex]::Escape("$env:APPDATA\Trae CN"), "AppData\Roaming\Trae CN"
    $relativePath = $relativePath -replace [regex]::Escape($env:USERPROFILE), ""
    $targetPath = Join-Path $targetBase $relativePath
    
    if (!(Test-Path $sourcePath)) {
        Write-Host "   跳过（不存在）: $sourcePath" -ForegroundColor Gray
        continue
    }
    
    Write-Host ""
    Write-Host "2. 处理：$sourcePath" -ForegroundColor Yellow
    
    # 检查是否已经是符号链接
    $item = Get-Item $sourcePath -ErrorAction SilentlyContinue
    if ($item.LinkType) {
        Write-Host "   已是符号链接，跳过" -ForegroundColor Gray
        continue
    }
    
    # 创建目标目录的父目录
    $parentDir = Split-Path $targetPath -Parent
    if (!(Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    
    # 如果目标已存在，先删除
    if (Test-Path $targetPath) {
        Write-Host "   目标已存在，删除中..." -ForegroundColor Yellow
        Remove-Item $targetPath -Recurse -Force -ErrorAction SilentlyContinue
    }
    
    # 移动文件
    Write-Host "   移动文件中 (这可能需要几分钟)..." -ForegroundColor Cyan
    try {
        Move-Item $sourcePath $targetPath -Force
        Write-Host "   移动成功" -ForegroundColor Green
    } catch {
        Write-Host "   移动失败：$($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   尝试使用复制代替..." -ForegroundColor Yellow
        Copy-Item $sourcePath $targetPath -Recurse -Force
        if ($?) {
            Remove-Item $sourcePath -Recurse -Force
            Write-Host "   复制并删除原文件成功" -ForegroundColor Green
        }
    }
    
    # 创建符号链接
    Write-Host "   创建符号链接..." -ForegroundColor Cyan
    try {
        cmd /c mklink /J "`"$sourcePath`"" "`"$targetPath`"" | Out-Null
        if ($?) {
            Write-Host "   符号链接创建成功" -ForegroundColor Green
            Write-Host "     $sourcePath -> $targetPath" -ForegroundColor Gray
        } else {
            Write-Host "   符号链接创建失败" -ForegroundColor Red
        }
    } catch {
        Write-Host "   错误：$($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  迁移完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "所有 Trae 相关文件已迁移到：$targetBase" -ForegroundColor Green
Write-Host ""
Write-Host "符号链接说明：" -ForegroundColor Yellow
Write-Host "- 原路径保持不变，程序仍可通过原路径访问" -ForegroundColor White
Write-Host "- 实际文件存储在 D 盘，节省 C 盘空间" -ForegroundColor White
Write-Host "- 可以随时删除 D 盘的文件（但会导致 Trae 无法使用）" -ForegroundColor White
Write-Host ""
Write-Host "现在可以启动 Trae 编辑器了！" -ForegroundColor Green
Write-Host ""
Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
