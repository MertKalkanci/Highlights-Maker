from pytube import YouTube
from moviepy.editor import *
from pydub import AudioSegment
import os
import math
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.editor import VideoFileClip, concatenate_videoclips
from time import sleep
from moviepy.config import change_settings
import pysrt
from datetime import datetime
import nextcord as discord
from discord.ext.commands import Bot
from ai import gpt,trasncribe
from json_ops import load_dict_from_json,save_dict_to_json

TEMP_MP3 = "/content/video.mp3"
LINK_CACHE="https://www.youtube.com/watch?v=3ryID_SwU5E"
SAVE_PATH="/temp/" 

LENTGH=20 
SKIP_RATE=15 
TEMPERATURE = 0.35 

KEY_WORDS = []

MAIN_PROMPT_FIRST_PART = """
You are a bot that makes decisions about a youtube shorts or tiktok video. If you think that the communication given below won't get 1 million clicks don't reccomend according to the rules given below
IF a conversation is worth a youtube shorts Highlight just answer YES else say NO
some keywords for it:
"""
MAIN_PROMPT_SECOND_PART = """
Some communication will be given in the bottom
Conversations:

"""

bot = Bot(command_prefix=".")

@bot.event
async def on_connect():
  print("Bot Connected")


@bot.command(name="highlight",help="Creates highlights from given youtube video")
async def highlight(ctx: discord.message, url: str, *keywords, length=LENTGH, skiprate=SKIP_RATE, temperature=TEMPERATURE):
  if ctx.message.author.guild_permissions.administrator == False:
    await ctx.send("You do not have permission to do that!")
    return

@bot.command(name="adduser",help="Adds user to create highlights from given youtube video")
async def adduser(ctx: discord.message, user: discord.Member):
    if ctx.message.author.guild_permissions.administrator == False or ctx.Message.author.id != load_dict_from_json("creator.json")['1']:
        await ctx.send("You do not have permission to do that!")
        return
      
    users = load_dict_from_json("user.json")  
    users[str(user.id)] = user.id
    
    save_dict_to_json("user.json",users)
    
    await ctx.send(f"User {user.name} added")

@bot.command(name="removeuser",help="Removes user to create highlights from given youtube video")
async def removeuser(ctx: discord.message, user: discord.Member):
    if ctx.message.author.guild_permissions.administrator == False or ctx.Message.author.id != load_dict_from_json("creator.json")['1']:
        await ctx.send("You do not have permission to do that!")
        return
      
    users = load_dict_from_json("user.json")  
    users.pop(str(user.id))
    
    save_dict_to_json("user.json",users)
    
    await ctx.send(f"User {user.name} removed")
  

bot.run(open("discord", "r").read())