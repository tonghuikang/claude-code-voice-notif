#!/usr/bin/env python3
"""
Reads transcript path from stdin hook and launches audio player
"""

import sys
import json
import subprocess
import tempfile
import shutil
import os


def main():
    # Read transcript path from stdin (Claude hook format)
    # https://docs.anthropic.com/en/docs/claude-code/hooks
    hook_data = json.load(sys.stdin)
    transcript_path = hook_data["transcript_path"]
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp(prefix="claude_audio_")
    
    # Copy the transcript file to the temporary directory
    temp_transcript_path = os.path.join(temp_dir, os.path.basename(transcript_path))
    shutil.copy2(transcript_path, temp_transcript_path)
    
    # Launch audio player as detached subprocess with the temp path
    subprocess.Popen(
        ["uv", "run", "python3", ".claude/audio_player.py", temp_transcript_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        start_new_session=True  # Detach from parent process
    )


if __name__ == "__main__":
    main()