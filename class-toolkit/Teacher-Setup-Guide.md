# Teacher Setup Guide — Class Toolkit

This guide walks you through getting the Class Toolkit ready on your computer.

## Step 1: Ask Your Admin to Install the Software

Before you start, your school admin or IT support needs to install a few programs on your computer. Give them the [Admin Setup Guide](Admin-Setup-Guide.md) — it takes about 10 minutes and they won't need any of your account details.

Once they've confirmed everything is installed and the computer has been restarted, continue with the steps below.

## Step 2: Subscribe to Claude Pro

You need a Claude Pro subscription to use the Class Toolkit.

1. Go to https://claude.ai and create an account (or sign in if you already have one)
2. Subscribe to **Claude Pro** ($20 USD/month) — this is the only ongoing cost
3. Download **Claude Desktop** from https://claude.ai/download
4. Install it and sign in with your account

## Step 3: Set Up Claude Code in VS Code

1. Open **VS Code** (it's already installed on your computer)
2. Click the **Extensions** icon on the left sidebar (it looks like four squares), or press `Ctrl+Shift+X`
3. Search for **Claude Code**
4. Click **Install**
5. The Claude Code panel will appear in the sidebar — click on it
6. Sign in with your Claude account when prompted

## Step 4: Install the Class Toolkit Plugin

In the Claude Code chat panel, type this command and press Enter:

```
/plugin marketplace add hamishnorton/claude-code-plugins
```

Then type this command and press Enter:

```
/plugin install class-toolkit@hamishnorton
```

You only need to do this once.

## Step 5: Configure VS Code Settings

1. In VS Code, go to **File > Preferences > Settings** (or press `Ctrl+,`)
2. Search for **Claude Code**
3. Set the following:
   - **Initial Permission Mode** → `bypassPermissions`
   - **Allow Dangerously Skip Permissions** → tick the checkbox
4. Close the Settings tab

Alternatively, open your VS Code `settings.json` (press `Ctrl+Shift+P`, type **Preferences: Open User Settings (JSON)**) and add:

```json
{
  "claudeCode.initialPermissionMode": "bypassPermissions",
  "claudeCode.allowDangerouslySkipPermissions": true
}
```

## Step 6: Install a Markdown Formatter (Optional)

A formatter keeps your Markdown files (like student profiles) neat and consistent, fixing spacing and alignment automatically every time you save.

1. In VS Code, open **Extensions** (`Ctrl+Shift+X`)
2. Search for **Prettier - Code formatter** (by Prettier)
3. Click **Install**
4. Go to **File > Preferences > Settings** (or press `Ctrl+,`)
5. Search for **Format On Save**
6. Tick the **Editor: Format On Save** checkbox

Now whenever you save a `.md` file, Prettier will tidy it up for you.

## Step 7: Set Up Permissions

The Class Toolkit needs permission to read and write files, run commands, and access your home folder. Without this, Claude will ask you to approve every single action.

### Option A: Use the /permissions command

In the Claude Code chat panel, type:

```
/permissions
```

Then allow the following tools: **Read**, **Edit**, **Write**, **Glob**, **Grep**, **Bash**, **Skill**, **WebFetch**, **WebSearch**

Set the default mode to **bypassPermissions** and add `~/` as an additional directory.

### Option B: Edit settings.json manually

If you prefer, open the file `~/.claude/settings.json` in VS Code and add the following block:

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Write",
      "Glob",
      "Grep",
      "Bash",
      "Skill",
      "WebFetch",
      "WebSearch"
    ],
    "defaultMode": "bypassPermissions"
  }
}
```

If the file already has content, merge the `"permissions"` key into the existing JSON rather than replacing the whole file.

## Step 8: Open Your Class Folder

1. In VS Code, go to **File > Open Folder**
2. Navigate to `Documents > ClassResources`
3. Click **Select Folder**

You should see your student folders in the left sidebar.

## Step 9: Generate Your First Resource

In the Claude Code chat panel, type:

```
/generate-resource Create a 300 word story about kindness
```

Claude will create a personalised Word document for every student. The files appear in each student's folder — open and print them.

---

## Quick Reference

| Command              | What it does                                       |
| -------------------- | -------------------------------------------------- |
| `/generate-resource` | Generate a personalised resource for every student |
| `/init-class`        | Add new students or update the class list          |

- Type `/generate-resource` with no prompt to see saved guides you can reuse
- Word documents are saved in each student's folder inside `ClassResources`
- To change a student's year level, edit the `year-level` value in their `student-profile.md` frontmatter

---

## Windows Shortcut

Your admin may have placed a **Class Toolkit** launcher on your Desktop. Double-click it to open Claude Code directly in your `Documents\ClassResources` folder — it creates the folder automatically if it doesn't exist yet. This lets you skip the "Open Folder" step in VS Code.

---

## Troubleshooting

| Problem                                  | Solution                                                          |
| ---------------------------------------- | ----------------------------------------------------------------- |
| Claude asks to sign in again             | Normal — sign in with the same account                            |
| "pandoc is not installed" warning        | Ask your admin to reinstall Pandoc and restart the computer       |
| Font doesn't look right in Word          | Run `/init-class` again — it installs the correct font            |
| `/generate-resource` doesn't do anything | Make sure student profiles have `active: true` in the frontmatter |
| "git is not recognized"                  | Ask your admin to reinstall Git for Windows and restart           |
