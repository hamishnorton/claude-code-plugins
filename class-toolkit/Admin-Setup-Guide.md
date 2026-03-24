# Admin Setup Guide — Class Toolkit on Windows

This guide is for the school admin/IT support. It covers the software installations only — the teacher will handle the subscription and plugin setup themselves.

## Automated Install (Recommended)

Run the install script to do everything at once:

1. Open **PowerShell as Administrator** (right-click PowerShell > "Run as administrator")
2. Run these two commands:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   .\install-class-toolkit.ps1
   ```
3. Restart the computer when it finishes

The script installs Git, Pandoc, Claude Code, and VS Code. It skips anything already installed. At the end it will print a command to copy the Class Toolkit launcher to the teacher's Desktop — run that command before restarting. If it succeeds, skip to the [Verification Checklist](#verification-checklist) below.

---

## Manual Install (If the Script Doesn't Work)

There are four programs to install, plus the launcher. Do them in order.

### 1. Git for Windows

Claude Code needs Git to run commands.

1. Go to https://git-scm.com/downloads/win
2. Download the installer
3. Run the installer — click Next through the defaults

### 2. Pandoc

Pandoc converts generated content into Word documents.

1. Go to https://pandoc.org/installing.html
2. Click the **Windows installer** (the `.msi` file)
3. Run the installer — click Next through the defaults

### 3. Claude Code (CLI)

This is the AI assistant that powers the class toolkit.

1. Open **PowerShell** (press `Win+R`, type `powershell`, press Enter)
2. Paste this command and press Enter:
   ```
   irm https://claude.ai/install.ps1 | iex
   ```
3. Wait for it to finish installing

### 4. VS Code

VS Code gives the teacher a visual file explorer alongside the chat.

1. Download from https://code.visualstudio.com
2. Run the installer — click Next through the defaults

### 5. Class Toolkit Launcher

A `class-toolkit.bat` file is included alongside this guide. Copy it to the teacher's Desktop so they can double-click it to open the toolkit:

```powershell
copy "class-toolkit.bat" "C:\Users\<TeacherUsername>\Desktop\Class Toolkit.bat"
```

Replace `<TeacherUsername>` with the teacher's Windows username. The launcher creates the `Documents\ClassResources` folder automatically on first run.

### 6. Restart the Computer

Restart so the system recognises all the new programs.

---

## Verification Checklist

After restarting, confirm everything is working:

1. Open **PowerShell** and run each command below — each should print a version number:
   ```
   git --version
   pandoc --version
   claude --version
   ```
2. Open **VS Code** and confirm it launches

If any command says "not recognized", reinstall that program and restart again.

---

## Summary of Installs

| Software        | What it does                | Download / Source                            |
| --------------- | --------------------------- | -------------------------------------------- |
| Git for Windows | Required by Claude Code     | https://git-scm.com/downloads/win            |
| Pandoc          | Creates Word documents      | https://pandoc.org/installing.html           |
| Claude Code     | AI assistant (CLI)          | `irm https://claude.ai/install.ps1 \| iex`  |
| VS Code         | Code editor with UI         | https://code.visualstudio.com                |
| class-toolkit.bat | Desktop launcher for teacher | Included alongside this guide              |

---

The teacher will handle signing in, subscribing, and setting up the plugin themselves using the main [Teacher Setup Guide](Teacher-Setup-Guide.md).
