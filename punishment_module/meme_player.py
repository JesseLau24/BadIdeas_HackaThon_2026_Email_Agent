# punishment_module/meme_player.py

import os
import random
from utils.constants import ALERT_VIDEO_DIR, ALERT_VIDEO_EXT
from utils.file_opener import open_file  # 跨平台播放工具

def list_video_files(directory: str, extension: str) -> list:
    """
    列出指定目录中所有指定扩展名的视频文件（不含子目录）。
    """
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(extension.lower())
    ]

def play_random_alert_video():
    """
    随机播放一个提醒或惩罚视频（统一使用 alerts 文件夹中的 .mp4 文件）。
    """
    video_files = list_video_files(ALERT_VIDEO_DIR, ALERT_VIDEO_EXT)

    if not video_files:
        print(f"⚠️ No alert videos (*{ALERT_VIDEO_EXT}) found in {ALERT_VIDEO_DIR}.")
        return

    selected = random.choice(video_files)
    print(f"🎬 Playing alert video: {os.path.basename(selected)}")
    open_file(selected)
