# Setting up the studio on your Mac

About 15–20 minutes, most of it downloading. Nothing is bought, and every tool is free.
Open **Terminal** (Applications → Utilities → Terminal) and paste each block in order.

## 1. Install Homebrew (skip if you already have it)
Homebrew is the standard free installer for developer tools on a Mac. Go to **https://brew.sh**, copy the one-line command on that page, paste it into Terminal and follow its prompts. It asks for your Mac password once. If it ends by printing "Next steps" commands (`echo ... >> ~/.zprofile` and `eval ...`), run those too.

## 2. Sign in to GitHub (the repository is private)
```bash
brew install gh
gh auth login
```
Choose **GitHub.com → HTTPS → Yes → Login with a web browser**, then paste the code it shows into the browser page that opens.

## 3. Get the project onto your Mac
```bash
mkdir -p ~/Projects && cd ~/Projects
gh repo clone localsaintt/faceless-3d-studio
cd faceless-3d-studio
```
The project lives in `~/Projects`, which iCloud does **not** sync. Keep it there.

## 4. Run the setup script
```bash
bash setup/mac_setup.sh
```
This installs ffmpeg (video tool), uv (Python manager), Python 3.13 and Blender 5.2.3 inside the project folder. It then runs a **doctor check** and a **speed test** that renders one frame of the prototype beach.

The last lines should say `ALL GOOD`. The speed test prints how long a frame took and an estimate for a full 70-second video. **Send that output to Claude.**

## 5. Render the prototype yourself (optional)
```bash
.venv/bin/python -m studio.render_shot shots/proto/s01_beach_establishing.yaml --profile preview
open output/proto/s01_beach_establishing/s01_beach_establishing_preview.mp4
```

## Let Claude drive it
Run Claude Code in this folder: open the Claude Desktop app's Claude Code tab and choose this folder, or type `claude` in Terminal here. To let a cloud session use this Mac, run `claude remote-control` in this folder. Claude asks before running commands.

## Getting updates later
```bash
cd ~/Projects/faceless-3d-studio && git pull
```

## Tips while rendering
- Keep the Mac plugged in, on a hard surface. It will get warm and the fans may run, which is normal.
- Renders keep the Mac awake automatically (`caffeinate`).
- Close Chrome and other heavy apps during long renders (8 GB memory).
- To remove everything: delete the `faceless-3d-studio` folder (and optionally `brew uninstall ffmpeg uv gh`).
