#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." && uv run python3 "$SCRIPT_DIR/audio_player.py" "$SCRIPT_DIR/sample-request-permission.jsonl"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.." && uv run python3 "$SCRIPT_DIR/audio_player.py" "$SCRIPT_DIR/sample-request-completion.jsonl"
