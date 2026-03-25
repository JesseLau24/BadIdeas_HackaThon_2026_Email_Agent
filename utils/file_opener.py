# utils/file_opener.py

import os
import platform
import subprocess

def open_file(path: str):
    """
    通用跨平台打开文件（支持 mp4 视频等）
    - Windows: 使用 os.startfile
    - macOS: 使用 open
    - Linux: 使用 cvlc (VLC 无界面模式)
    """
    system = platform.system()

    if not os.path.exists(path):
        print(f"❌ File does not exist: {path}")
        return

    try:
        if system == "Windows":
            os.startfile(path)
        elif system == "Darwin":
            subprocess.Popen(["open", path], shell=False)
        else:  # Linux
            # 使用 cvlc 播放视频，避免 GUI 播放器冲突
            subprocess.Popen(["cvlc", "--play-and-exit", path], shell=False)

        print(f"✅ Opened file: {path} on {system}")
    except Exception as e:
        print(f"⚠️ Failed to open file: {path} on {system}. Error: {e}")
