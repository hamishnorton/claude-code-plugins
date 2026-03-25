# Class Toolkit - Automated Install Script
# Run this in PowerShell as Administrator
# Right-click PowerShell > "Run as administrator", then:
#   Set-ExecutionPolicy Bypass -Scope Process -Force
#   .\install-class-toolkit.ps1

Write-Host ""
Write-Host "=== Class Toolkit Installer ===" -ForegroundColor Cyan
Write-Host "This will install: Pandoc, VS Code, Git, Claude Code, and the Class Toolkit launcher"
Write-Host ""

# Check for admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Please run this script as Administrator." -ForegroundColor Red
    Write-Host "Right-click PowerShell > 'Run as administrator'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if winget is available
$hasWinget = Get-Command winget -ErrorAction SilentlyContinue
if (-not $hasWinget) {
    Write-Host "ERROR: winget is not available on this machine." -ForegroundColor Red
    Write-Host "Install 'App Installer' from the Microsoft Store, then re-run this script." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$failed = @()

# 1. Pandoc
Write-Host ""
Write-Host "[1/5] Installing Pandoc..." -ForegroundColor Yellow
if (Get-Command pandoc -ErrorAction SilentlyContinue) {
    Write-Host "  Already installed: pandoc $(pandoc --version | Select-Object -First 1)" -ForegroundColor Green
} else {
    winget install --id JohnMacFarlane.Pandoc --accept-source-agreements --accept-package-agreements --silent
    if ($LASTEXITCODE -ne 0) { $failed += "Pandoc" }
}

# 2. VS Code
Write-Host ""
Write-Host "[2/5] Installing VS Code..." -ForegroundColor Yellow
if (Get-Command code -ErrorAction SilentlyContinue) {
    Write-Host "  Already installed" -ForegroundColor Green
} else {
    winget install --id Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements --silent
    if ($LASTEXITCODE -ne 0) { $failed += "VS Code" }
}

# 3. Git for Windows
Write-Host ""
Write-Host "[3/5] Installing Git for Windows..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "  Already installed: $(git --version)" -ForegroundColor Green
} else {
    winget install --id Git.Git --accept-source-agreements --accept-package-agreements --silent
    if ($LASTEXITCODE -ne 0) { $failed += "Git" }
}

# 4. Claude Code CLI
Write-Host ""
Write-Host "[4/5] Installing Claude Code..." -ForegroundColor Yellow
if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Host "  Already installed: $(claude --version)" -ForegroundColor Green
} else {
    irm https://claude.ai/install.ps1 | iex
    if ($LASTEXITCODE -ne 0) { $failed += "Claude Code" }
}

# 5. Class Toolkit launcher
Write-Host ""
Write-Host "[5/5] Class Toolkit launcher..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$batSource = Join-Path $scriptDir "class-toolkit.bat"
if (Test-Path $batSource) {
    Write-Host "  Found launcher at: $batSource" -ForegroundColor Green
    Write-Host ""
    Write-Host "  NEXT STEP: Copy the launcher to the teacher's Desktop:" -ForegroundColor Yellow
    Write-Host "    copy `"$batSource`" `"C:\Users\<TeacherUsername>\Desktop\Class Toolkit.bat`"" -ForegroundColor White
} else {
    Write-Host "  class-toolkit.bat not found in script directory - the teacher can download it from the plugin repository." -ForegroundColor Yellow
}

# Results
Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Cyan

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "The following failed to install: $($failed -join ', ')" -ForegroundColor Red
    Write-Host "Try installing them manually - see Admin-Setup-Guide.md" -ForegroundColor Yellow
} else {
    Write-Host "All software installed successfully." -ForegroundColor Green
}

Write-Host ""
Write-Host "IMPORTANT: Restart the computer before handing over to the teacher." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
