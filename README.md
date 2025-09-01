# GoogleSuiteOpener

**GoogleSuiteOpener** is a lightweight Windows utility that bridges the gap between your local files and Google Workspace (Docs, Sheets, Slides).

## ✨ What it does
- Uploads any local file to your Google Drive automatically.  
- Generates a shareable link for the file.  
- Opens it directly in your browser with Google Docs, Sheets, or Slides.  
- Adds an **optional right-click context menu** so you can send files straight to Google Suite with a single click.  
- Offers **optional PATH integration**, so advanced users can run `googlesuiteopener.exe myfile.docx` from the terminal.  

## 🛠 How it works
- Bundles [rclone](https://rclone.org/) in the installer for seamless Google Drive integration.  
- On first use, it sets up a secure `gdrive` remote in rclone (OAuth authentication).  
- Files are uploaded into a designated Google Drive folder, and their link is automatically opened in your default browser.  
- A small, minimal UI with a progress indicator ensures users know the app is working in the background.  

## 💡 Why it’s useful
Google Docs/Sheets/Slides don’t have native “Open with…” integration for local files. Normally you’d have to:
1. Open Google Drive manually,  
2. Upload the file,  
3. Right-click → “Open with” → Choose app.  

**GoogleSuiteOpener compresses that into one simple action.**

## 📦 Installer Features
- Runs without requiring admin rights (`PrivilegesRequired=lowest`).  
- Clean uninstall (removes all added registry entries).  
- Optional tasks:
  - ✅ Add right-click context menu (enabled by default).  
  - ⬜ Add to PATH (requires logout/reboot to take effect).  

## 🚀 Installation
1. Download the latest installer from [Releases](../../releases).  
2. Run the installer and choose your options:
   - Keep context menu enabled for easy right-click access.  
   - Enable PATH integration if you prefer terminal use.  
3. First time you run it, you’ll be prompted to log into your Google account (via rclone).  

## 🔧 Usage
- **Right-click a file → “GoogleSuiteOpener”**  
  → File is uploaded and opened in your browser.  

- **Command line (if PATH enabled):**
  ```bash
  googlesuiteopener.exe myfile.docx
