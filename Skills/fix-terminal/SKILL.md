---
name: windows-terminal-fix
description: >
  Diagnose and fix Windows Terminal startup errors caused by missing resource files (icons,
  backgroundImages, etc.) referenced in settings.json. Use this skill whenever the user
  mentions Windows Terminal showing an error like "One or more resources (such as icon or
  backgroundImage) specified in your settings could not be found", or any variant of a
  missing icon/resource warning when opening a terminal or command prompt. Also trigger
  when the user says their Windows Terminal profile has a broken icon, or that a profile
  they deleted (e.g. Multipass, Docker, WSL distro) is still causing errors. Don't wait
  for the user to say "skill" — if the problem sounds like a Windows Terminal settings
  file with broken resource paths, use this skill.
---

# Windows Terminal Settings Resource Fix

## What this skill does

Windows Terminal stores its configuration in a `settings.json` file. Profiles can reference
external files for things like icons and background images. When those external files no longer
exist (e.g. an app was uninstalled, a file was moved), Windows Terminal shows a warning on
every launch. This skill finds and removes those broken references so the warning goes away,
without affecting any other settings.

## Step-by-step workflow

### 1. Access the settings file

The settings.json is almost always at:

```
C:\Users\<username>\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json
```

You already know the username from the mounted folder path — use it. Request access to that
exact path via `request_cowork_directory`. If access fails (e.g. wrong username), ask the user
to select the `LocalState` folder manually.

### 2. Read and parse settings.json

Read the file. Confirm it's valid JSON before proceeding. If parsing fails, stop and tell
the user their settings.json has a syntax error — share the line/column of the issue so
they can fix it manually.

### 3. Find all resource references

Scan every profile in `profiles.list` for these fields:

- `"icon"` — path to an .ico or image file
- `"backgroundImage"` — path to an image file
- Any other field whose value is a string that looks like a file path (starts with `/`, `C:/`, `%`, or similar)

Skip `null` values and empty strings — those are fine and not causing errors.

### 4. Check which paths are broken

The Linux VM cannot directly access the user's Windows filesystem, so you cannot verify
whether a Windows path actually exists. The rule is simple:

**Remove every absolute Windows path** — any value starting with a drive letter like
`C:/`, `D:/`, or a Windows environment variable like `%USERPROFILE%`. This includes:

- Paths into `Program Files` (e.g. installed apps like Multipass, Docker)
- Paths into the user's own folders (e.g. `C:/Users/alice/Pictures/bg.png`)
- OneDrive paths (e.g. `C:/Users/alice/OneDrive/...`)
- Any other absolute Windows path

The reason: you cannot verify these files exist from the VM, and a path that _looks_
plausible may still be broken. The user is asking you to fix the error, so when in
doubt, remove it. They can easily re-add a working path later via Windows Terminal's
settings UI.

**Only leave a path in place if** it maps to one of the user's currently mounted folders
(visible under `/sessions/.../mnt/`) and you can confirm the file exists with `test -f`.

### 5. Fix the broken references

For each broken reference:

- Remove the field entirely (don't set it to `null` — a missing field is cleaner than an
  explicit null, since null can still be interpreted as a resource reference in some versions).

While you're in there, also clean up any `"icon": null` or `"backgroundImage": null` entries,
since these are explicitly setting a resource to nothing and are generally unnecessary clutter.

### 6. Validate and save

Before writing, serialize the modified JSON with the same indentation style as the original
(4 spaces). Do a final parse of the output string to confirm it's still valid JSON — if not,
stop and report the error rather than writing a broken file.

Write the fixed settings.json back to the same path.

### 7. Report the changes

Tell the user:

- Which profiles had broken references removed (name the profile, name the field, and show
  the old path so they understand what was cleaned up)
- Whether any null entries were cleaned up
- That the file has been saved and they should close/reopen Windows Terminal for it to take effect
- That all other settings (keybindings, color schemes, profiles, etc.) are untouched

## Edge cases

**Multiple broken references in one profile:** Fix them all — don't stop after the first one.

**The default profile itself has a broken icon:** That's fine to fix — the default profile will
just use the built-in Windows Terminal icon instead.

**Settings.json doesn't exist at the expected path:** The user may have Windows Terminal
installed differently (e.g. from GitHub releases rather than the Store). Ask them to
navigate to their settings via Windows Terminal → Settings → "Open JSON file" button, then
note the path and ask you to request access to that folder.

**Multipass, Docker Desktop, WSL distros:** These are the most common source of broken icons
when users uninstall or update these tools. Mention this if relevant so the user understands
why the icon was missing.
