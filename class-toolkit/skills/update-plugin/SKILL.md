---
name: update-plugin
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

### Step 3: Report the Result

Tell the teacher the outcome — whether the plugin was updated or was already at the latest version.

## Reference Commands

If the teacher needs help with other plugin management tasks, here are the relevant commands:

- **Install:** `claude plugin install class-toolkit@hamishnorton --scope user`
- **Uninstall:** `claude plugin uninstall class-toolkit@hamishnorton --scope user`
