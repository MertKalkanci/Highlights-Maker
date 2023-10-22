from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment
import os
import math
import whisper
import openai
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from time import sleep
from moviepy.config import change_settings
import pysrt
from datetime import datetime
import nextcord

TEMP_MP3 = "/content/video.mp3"
LINK_TEST="https://www.youtube.com/watch?v=3ryID_SwU5E"
SAVE_PATH="/temp/" 

LENTGH=20 
SKIP_RATE=15 
TEMPERATURE = 0.35 

KEY_WORDS = []

MAIN_PROMPT_FIRST_PART = f"""
You are a bot that makes decisions about a youtube shorts or tiktok video. If you think that the communication given below won't get 1 million clicks don't reccomend according to the rules given below
IF a conversation is worth a youtube shorts Highlight just answer YES else say NO
some keywords for it:
"""
MAIN_PROMPT_SECOND_PART = """
Some communication will be given in the bottom, Be aware of this keywords that improves that:
Conversations:

"""