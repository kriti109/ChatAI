# ChatAI Project

This repository contains the ChatAI project. Below is the complete setup guide to get started from scratch.

---
Make a folder with the name ChatAI in D drive.
## 1. Setup Python Virtual Environment

Open your terminal or Git Bash and run these commands to create and activate a virtual environment in your project folder located on the D: drive.


# Switch to D drive and navigate to project folder
D:
cd \ChatAI

# Create a virtual environment named ".venv"
python -m venv .venv

# Activate the virtual environment (Git Bash or PowerShell)
source .venv/Scripts/activate

# If you use Windows Command Prompt, activate with:
# .venv\Scripts\activate.bat
Your prompt should now show (.venv) indicating the environment is active.

Run this code in your terminal to set the venv up:
pip install -r requirements.txt

3. Setup FFmpeg
We use FFmpeg for audio/video processing. Instead of installing via package managers, we download and set up a local build in the project folder.

Steps:

Download the FFmpeg essentials build from a trusted source (e.g., gyan.dev).

Extract the downloaded .zip file inside your project directory D:\ChatAI\ffmpeg-7.1.1-essentials_build.

The extracted folder contains the bin directory with executables:

ffmpeg.exe

ffplay.exe

ffprobe.exe

Optionally, add D:\ChatAI\ffmpeg-7.1.1-essentials_build\bin to your system PATH environment variable so FFmpeg commands work globally from any terminal.

Alternatively, reference the full path to ffmpeg.exe in your scripts if you don't want to modify PATH.

ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
