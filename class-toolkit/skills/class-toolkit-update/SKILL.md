---
name: class-toolkit-update
description: "Update the class-toolkit plugin to the latest version. Use when the user wants to update, upgrade, or get the latest version of the class-toolkit plugin. Also use when the user says things like 'update the plugin', 'check for updates', 'get the latest version', or 'upgrade class-toolkit'."
---

# Update Plugin

Update the class-toolkit plugin to the latest version.

## Instructions

### Step 1: Refresh the Marketplace Cache

Run the following command to fetch the latest plugin versions:

```bash
claude plugin marketplace update hamishnorton
```

### Step 2: Update the Plugin

Run the following command to update the plugin:

```bash
claude plugin update class-toolkit@hamishnorton --scope user
```

### Step 3: Migrate File Structure

After updating, check if the teacher has any classes set up. Use Glob to search for `**/student-profile.md` in the working directory. If none are found, skip to Step 4 — this is a fresh install with nothing to migrate.

If student profiles are found, run through each migration check below **in order**. Report each migration performed. If nothing needs migrating, skip silently to Step 4.

#### 3a: Unwrap `class-agent/` nesting

Check if a `class-agent/` directory exists in the working directory.

**If it exists:**

1. Move all contents of `class-agent/` up one level into the working directory (e.g., `class-agent/year-5-blue/` → `year-5-blue/`)
   - **Linux/macOS:** `mv class-agent/* . && rmdir class-agent`
   - **Windows:** `Move-Item -Path "class-agent\*" -Destination "." && Remove-Item "class-agent"`
2. Tell the teacher: "Moved class folders out of the old `class-agent/` directory."

#### 3b: Wrap in `ClassResources/`

Check if the current working directory's basename is **not** `ClassResources`, and class folders (directories containing `*/student-profile.md`) exist at the working directory root.

**If class folders are at the root without a ClassResources wrapper:**

1. Create `ClassResources/` if it does not exist
2. Move each class folder into `ClassResources/`
3. Also move `templates/`, `guides/`, `progressions/`, and `CLAUDE.md` into `ClassResources/` if they exist at the root
   - **Linux/macOS:** `mv {folder} ClassResources/`
   - **Windows:** `Move-Item -Path "{folder}" -Destination "ClassResources\"`
4. Tell the teacher: "Moved class folders and supporting directories into `ClassResources/` to match the current layout."

After this step, determine the **base directory** using the same logic as init-class: if the working directory's basename is `ClassResources`, use `.`; otherwise use `ClassResources/`. All subsequent steps use `{base}`.

#### 3c: Provision templates directory

Check if `{base}/templates/year-1-ref.docx` exists.

**If it does not exist:**

1. Use Glob to find `**/class-toolkit/templates/year-1-ref.docx` under `~/.claude/` to locate the plugin's installed directory
2. Derive the **plugin directory** from the matched path (two levels up from `templates/year-1-ref.docx`)
3. Create `{base}/templates/` if it does not exist
4. Copy templates:
   - **Linux/macOS:**
     ```bash
     cp {plugin-dir}/templates/year-*-ref.docx {base}/templates/
     cp {plugin-dir}/templates/student-profile-template.md {base}/templates/
     ```
   - **Windows:**
     ```powershell
     Copy-Item -Path "{plugin-dir}\templates\year-*-ref.docx" -Destination "{base}\templates\"
     Copy-Item -Path "{plugin-dir}\templates\student-profile-template.md" -Destination "{base}\templates\"
     ```
5. Tell the teacher: "Added formatting templates — Word documents will now use age-appropriate fonts and spacing."

#### 3d: Clean up old student-profile-template.md copies

Use Glob to find any `{base}/*/student-profile-template.md` files (i.e., template copies inside class folders — the old location).

**If any are found:**

1. Delete each one:
   - **Linux/macOS:** `rm {path}`
   - **Windows:** `Remove-Item "{path}"`
2. Tell the teacher: "Removed old template copies from class folders — the template now lives in `{base}/templates/`."

#### 3e: Add missing `year-level` to student profiles

Read each `student-profile.md` found under `{base}`. Check if the YAML frontmatter contains a `year-level` field.

**If any profiles are missing `year-level`:**

1. Group the affected students by class folder
2. For each class with missing values, use AskUserQuestion to ask: "Some students in {class name} don't have a year level set. What year level should they default to? (1–8)"
3. For each affected profile, add `year-level: {value}` to the YAML frontmatter (after the last existing field, before the closing `---`)
4. Tell the teacher how many profiles were updated

#### 3f: Install Andika font

Check if the Andika font is already installed by looking for `Andika-Regular.ttf` in the user's font directory:

- **Linux:** `~/.local/share/fonts/`
- **macOS:** `~/Library/Fonts/`
- **Windows:** `%LOCALAPPDATA%\Microsoft\Windows\Fonts\`

**If not installed:**

1. Use the **plugin directory** (find it via Glob for `**/class-toolkit/fonts/andika/Andika-Regular.ttf` under `~/.claude/` if not already known)
2. Copy fonts and refresh cache:
   - **Linux:**
     ```bash
     mkdir -p ~/.local/share/fonts
     cp {plugin-dir}/fonts/andika/Andika-*.ttf ~/.local/share/fonts/
     fc-cache -f
     ```
   - **macOS:**
     ```bash
     cp {plugin-dir}/fonts/andika/Andika-*.ttf ~/Library/Fonts/
     ```
   - **Windows:**
     ```powershell
     $fontDir = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
     New-Item -ItemType Directory -Force -Path $fontDir | Out-Null
     Copy-Item -Path "{plugin-dir}\fonts\andika\Andika-*.ttf" -Destination $fontDir
     ```
3. Tell the teacher: "Installed the Andika font for Word document formatting."

#### 3g: Nest flat progression files

Check if `{base}/progressions/` exists and contains `.md` files directly (not inside a framework subfolder). Ignore `source-*.md` files in this check — look for progression content files like `bsla-taumata-1.md` at the top level of `progressions/`.

**If flat progression files are found:**

1. Attempt to group the files by their filename prefix (the part before the first level identifier). For example, `bsla-taumata-1.md` and `bsla-taumata-2.md` share the prefix `bsla`.
2. For each group, derive a framework slug from the common prefix
3. Create `{base}/progressions/{framework-slug}/` and move the files into it
4. Also move any matching `source-*.md` file into the subfolder
5. Tell the teacher: "Reorganised progression files into framework subfolders."

### Step 4: Report the Result

Tell the teacher the outcome:

- Whether the plugin was updated or was already at the latest version
- A summary of any migrations performed in Step 3 (if any)
- If no migrations were needed, just report the update result

## Reference Commands

If the teacher needs help with other plugin management tasks, here are the relevant commands:

- **Install:** `claude plugin install class-toolkit@hamishnorton --scope user`
- **Uninstall:** `claude plugin uninstall class-toolkit@hamishnorton --scope user`
