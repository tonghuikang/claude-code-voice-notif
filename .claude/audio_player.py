#!/usr/bin/env python3
"""
Reads transcript from file and streams audio via OpenAI TTS
"""

import sys
import json
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer


def parse_transcript(transcript_path: str) -> str:
    """Parse the transcript to extract text from the latest message"""
    with open(transcript_path, "r") as f:
        lines = f.readlines()
    
    if not lines:
        return "No transcript found"

    try:
        data = json.loads(lines[-1].strip())
        return str(data)

    except (json.JSONDecodeError, KeyError):
        return "Invalid transcript format"


openai = AsyncOpenAI()

language = "English"

system_prompt = """
You will be given a piece of log from the coding agent.

Your reply will be in {language}.

For logs requiring tool use `"content":[{{"type":"tool_use","`, you will be requesting permission
- You will reply in this format - "Requesting permissions for ..."
- For bash commands, mention what are you doing directly
    - Being your statement with Requesting permission to ...
        - In Japanese: 許可を求める
- Be as concise as possible.
    - There is no need to mention the name of the tool. Just mention what are you doing
        - Instead of - Requesting permissions to use the Bash tool to remove <file>
        - Say - Requesting permissions to remove <file>

For logs not requiring tool use, summarize the content appearing in `"content":[{{"type":"text","text":"`.
- Be as concise as possible.
    - There is no need to deliver the full information.
        - For example
            - You only need to mention the file name, NOT the entire filepath
            - You only need to mention the date or the time, NOT both
    - Use as few words as possible.
""".strip()


user_prompt = """
Please process the following log according to the system instructions.

Your reply will be in {language}.

These are the logs.

{action_text}

Reminder: Your reply should NEVER exceed 15 words.
"""


async def summarize_action(action_text: str) -> str:
    """Generate a brief summary of the last action"""
    response = await openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt.format(language=language)},
            {"role": "user", "content": user_prompt.format(language=language, action_text=action_text)}
        ],
        max_tokens=50,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()


voice_instructions = """
Speak with cuteness and energy.
""".strip()


async def generate_audio(transcript: str) -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="sage",
        input=transcript,
        instructions=voice_instructions,
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


async def main():
    if len(sys.argv) < 2:
        print("Usage: python audio_player.py <transcript_path>", file=sys.stderr)
        sys.exit(1)
    
    transcript_path = sys.argv[1]
    
    # Parse transcript to get text
    text_to_speak = parse_transcript(transcript_path)
    
    if text_to_speak:
        # Summarize the action
        summary = await summarize_action(text_to_speak)
        
        # Generate and play audio of the summary
        await generate_audio(summary)


if __name__ == "__main__":
    asyncio.run(main())