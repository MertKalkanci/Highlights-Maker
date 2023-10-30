# -*- coding:utf-8 -*-
from calendar import c
from numpy import unicode_
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
from flask import Flask, send_file
import threading
import json
import requests
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

IP = f"http://{requests.get('https://checkip.amazonaws.com').text.strip()}:5000"
LINK="https://www.youtube.com/watch?v=3ryID_SwU5E"
SAVE_PATH="/temp/" 

MAX_URL_IN_MESSAGE = 10
LENGTH=20 
SKIP_RATE=15 
TEMPERATURE = 0.35 
LANGUAGE =  "en"

TEMPERATURES = {}
LENGTHS = {}
SKIP_RATES = {}
LANGUAGES = {}

KEY_WORDS = []

MAIN_PROMPT_FIRST_PART_TR = """
Videodaki diyaloglardan yola çıkarak klipler oluşturan bir botsun. Eğer aşağıda verilen diyalog izlenmeye değer ya da anahtar kelimeler ile ilişkiliyse aşağıdaki kurallara göre öneride bulun
Eğer bir diyalog izlenmeye değerse YES degilse NO de
Anahtar kelimeler:
"""
MAIN_PROMPT_SECOND_PART_TR = """
Aşağıda bazı diyaloglar verilecek
Diyaloglar:

"""
MAIN_PROMPT_FIRST_PART_EN = """
You are a bot that makes decisions to create clips from video subtitles. If you think that the communication given below is worth to watch or relative to keywords reccomend according to the rules given below
IF a conversation is worth YES else say NO
Some keywords for it: 
"""
MAIN_PROMPT_SECOND_PART_EN = """
Some communication will be given in the bottom
Conversations:

"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

app = Flask(__name__)
bot = Bot(command_prefix=".", intents=intents)


@bot.event
async def on_connect():
  print("Bot Connected")
  
#print current path (working directory)
print(os.getcwd())


@bot.command()
async def configure(ctx: discord.message, temperature=TEMPERATURE, length=LENGTH, language=LANGUAGE):
    userid = str(ctx.author.id)
    serverid = str(ctx.guild.id)
   
    with open("user.json", "r") as f:
        data = json.load(f)  
        
    if data.get(userid) is None:
        await ctx.send("You do not have permission to do that!")
        return
    
    if str(temperature).lower() == "default":
        temperature = TEMPERATURE
    else:
        temperature = float(temperature)
    
    if str(length).lower() == "default":
        length = LENGTH
    else:
        length = int(length)
        
    if str(language).lower() == "default":
       language = LANGUAGE
       
    skiprate = int(length/2)
    
    TEMPERATURES[serverid] = temperature
    LENGTHS[serverid] = length
    SKIP_RATES[serverid] = skiprate
    LANGUAGES[serverid] = language.lower()
     
    await ctx.send(f"Temperature set to {temperature} and dialogue length set to {length} and language set to {language}")
    

    
    

@bot.command()
async def highlight(ctx: discord.message, url=LINK, *keywords):
    userid = str(ctx.author.id)
    
    with open("user.json", "r") as f:
        data = json.load(f)  
        
    if data.get(userid) is None:
        await ctx.send("You do not have permission to do that!")
        return
    
    if TEMPERATURES.get(str(ctx.guild.id)) is None:
       temperature=TEMPERATURE
    else:
       temperature=TEMPERATURES[str(ctx.guild.id)]
       
    if LENGTHS.get(str(ctx.guild.id)) is None:
       length = LENGTH
    else:
       length = LENGTHS[str(ctx.guild.id)]
       
    if SKIP_RATES.get(str(ctx.guild.id)) is None:
        skiprate = SKIP_RATE
    else:
        skiprate = SKIP_RATES[str(ctx.guild.id)]
    
    if LANGUAGES.get(str(ctx.guild.id)) is None:
       language = LANGUAGE
    else:
       language = LANGUAGES[str(ctx.guild.id)]
    
    
    #user preferences debug
    print(f"User {ctx.author.name} wants to create a highlight with the following preferences:")
    print(f"URL: {url}")
    print(f"Keywords: {keywords}")
    print(f"Length: {length}")
    print(f"Skip Rate: {skiprate}")
    print(f"Temperature: {temperature}")
    print(f"Language: {language}")
        
    language = language.lower()
    
    if language == "tr":
       MAIN_PROMPT = MAIN_PROMPT_FIRST_PART_TR + str(keywords) + MAIN_PROMPT_SECOND_PART_TR
    else:
       MAIN_PROMPT = MAIN_PROMPT_FIRST_PART_EN + str(keywords) + MAIN_PROMPT_SECOND_PART_EN


    sentMessage = await ctx.send(f"Creating Highlights with this settings:\nKeywords: {keywords}\nURL: {url}\nKeywords: {keywords}\nDialogue Length: {length}\nTemperature: {temperature}\nLanguage: {language}")
    sleep(5)
    
    await sentMessage.edit(content="Downloading Video...")

#region download

    try:
    # object creation using YouTube
    # which was imported in the beginning
        yt = YouTube(url)
    except:
        print("Connection Error") #to handle exception
        await sentMessage.edit(content="Connection Error.")
        return

    try:
        # filters out all the files with "mp4" extension
        mp4filepath = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').filter(resolution="720p").first().download(f"{userid}.mp4")

        mp3filepath = f"{userid}.mp3"
    except:
       print("Some Error while downloading video!")
       await sentMessage.edit(content="Some Error while downloading video!")
       return
#endregion

    await sentMessage.edit(content="Seperating Audio...")
    
#region audio
    
    try:
        video = VideoFileClip(mp4filepath)
        video.audio.write_audiofile(mp3filepath)  
    except:
        print("Some Error while seperating audio!")
        await sentMessage.edit(content="Some Error while seperating audio!")
        return
    
#endregion

    await sentMessage.edit(content="Analyzing audio... (this might take some time)")
    
#region analyze

    try:
        result = trasncribe(mp3filepath)
    except:
        print("Some Error while analyzing audio!")
        await sentMessage.edit(content="Some Error while analyzing audio!")
        return
    
#endregion

    await sentMessage.edit(content="Creating Highlight Videos & Subtitle Files...")
    
#region create

    try:
        class SubtitleVariable():
            start = 0.0
            end = 0.0
            text = ""

        subtitles = [{}]

        for i in range(0,len(result['segments'])):
          if(os.path.isfile(f"output{userid}{i}.mp4") ):
            os.remove(f"output{userid}{i}.mp4")

          subtitles.append({})

          if i % skiprate != 0:
            continue

          prompt = ""

          start = 0.0
          end = 0.0


          print("=================")

          if (i + length + 1) < len(result['segments']):
            start = result['segments'][i]['start']

            for j in range (0,LENGTH):
              subtitles[i][str(j)] = SubtitleVariable()

              text = result['segments'][(i + j)]['text']
              subtitles[i][str(j)].text = text

              subtitles[i][str(j)].start = result['segments'][(i + j)]['start']

              sub_end = result['segments'][(i + j)]['end']
              subtitles[i][str(j)].end = sub_end

              print(text)
              prompt = prompt + text
              end = sub_end

          print("\n")
          response = gpt(MAIN_PROMPT,prompt,temperature)
          print(response)
          print("=================")

          sleep(1)
          
          await sentMessage.edit(content=f"Creating Highlights & Subtitle Files...\n%{100*i/len(result['segments'])}")

          if response == "YES":
            print(f"Start: {start}\nEnd: {end}")
            ffmpeg_extract_subclip(mp4filepath, start, end, targetname=f"output{userid}{i}.mp4")
    except Exception as e:
        print(f"Some Error while creating highlights: {e}")
        await sentMessage.edit(content="Some Error while creating highlights list!\nContinuing with the ones generated")


    files = os.listdir()
    for i in range(0,len(result['segments'])):
      if(os.path.isfile(f"output{userid}{i}.srt") ):
        os.remove(f"output{userid}{i}.srt")
      if(os.path.isfile(f"output{userid}{i}.mp4")):
        if(os.path.isfile(f"output{userid}{i + length}.mp4")):
          video_file_list = [f"output{userid}{i}.mp4",f"output{userid}{i + length}.mp4"]

          copy_subtitles = subtitles[i].copy()

          print(copy_subtitles)

          if subtitles[i-length] != {} or subtitles[i-length] != None:
            print("merging subtitles")
            subtitles[i] = subtitles[i-length].copy()

            for key in copy_subtitles:
              subtitles[i + length][str(int(key) + 9)] = copy_subtitles[key]


          print("Merging: " + str(video_file_list))

          loaded_video_list = []

          for video in video_file_list:
              loaded_video_list.append(VideoFileClip(video))

          final_clip = concatenate_videoclips(loaded_video_list)

          merged_video_name = video_file_list[1]


          final_clip.write_videofile(f"{merged_video_name}")

          os.remove(video_file_list[0])
          
    files = os.listdir()
    for i in range(0,len(result['segments'])):
      if(os.path.isfile(f"output{userid}{i}.mp4")):
          min_start = yt.length

          for sub in subtitles[i]:
            if subtitles[i][sub].start < min_start:
              min_start = subtitles[i][sub].start

          file = pysrt.SubRipFile()

          for sub in subtitles[i]:
            sub_out = pysrt.SubRipItem(sub, start={'seconds': (subtitles[i][sub].start - min_start)}, end={'seconds': (subtitles[i][sub].end - min_start)}, text=subtitles[i][sub].text)
            file.append(sub_out)

          file.save(f"output{userid}{i}.srt")
#endregion
    
    await sentMessage.edit(content="Sending Highlight Links...")
    
#region send link
    
    links = []
    linksrt = []
    for i in range(0,len(result['segments'])):
        if(os.path.isfile(f"output{userid}{i}.mp4")):
            links.append(f"{IP}/download/{userid}/{i}/0")
            linksrt.append(f"{IP}/download/{userid}/{i}/1")             
        
    for i in range(0,len(links)):
        if i % MAX_URL_IN_MESSAGE == 0:
            
            await ctx.send("\n".join(links[i:i+MAX_URL_IN_MESSAGE]))
            await ctx.send("\n".join(linksrt[i:i+MAX_URL_IN_MESSAGE]))
            
            
#endregion
    #delete video files called {userid}.mp4 and {userid}.mp3
    
    #delete single file
    
@bot.command()
async def adduser(ctx: discord.message, user: discord.Member):    
    with open("creator.json", "r") as f:
        data = json.load(f)  
        
    if data.get(str(ctx.author.id)) is None:
        await ctx.send("You do not have permission to do that!")
        return
      
    with open("user.json", "r") as f:
        data = json.load(f)  
        
    if data.get(str(ctx.author.id)) is None: 
        data[str(user.id)] = user.id
    
    with open("user.json", "w") as f:
        json.dump(data, f)
    
    await ctx.send(f"User {user.name} added")

@bot.command()
async def removeuser(ctx: discord.message, user: discord.Member):
    with open("creator.json", "r") as f:
        data = json.load(f)  
        
    if data.get(str(ctx.author.id)) is None:
        await ctx.send("You do not have permission to do that!")
        return
      
    with open("user.json", "r") as f:
        data = json.load(f)  
    data.pop(str(user.id))
    
    with open("user.json", "w") as f:
        json.dump(data, f)
    
    await ctx.send(f"User {user.name} removed")
    
@bot.event
async def on_message(message: discord.Message):
  if message.author == bot.user:
    return
  await bot.process_commands(message)
 
@app.route("/download/<string:id>/<string:part>/<int:filed>")
def download(id,part,filed):
   if os.path.exists(f"output{id}{part}.mp4"):
      mp4 = f"output{id}{part}.mp4"
      srt = f"output{id}{part}.srt"
      if filed == 1:
        return send_file(mp4)
      else:
         return send_file(srt)


def runFlask():
  app.run()

threading.Thread(target=runFlask).start()

threading.Thread(bot.run(open("discord", "r").read())).start()
