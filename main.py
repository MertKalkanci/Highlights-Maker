# -*- coding:utf-8 -*-
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
from ai import gpt,trasncribe
import threading
import json
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

LINK="https://www.youtube.com/watch?v=3ryID_SwU5E"
SAVE_PATH="/temp/" 

LENGTH=27 
SKIP_RATE=10
TEMPERATURE = 0.35 
LANGUAGE =  "en"

MAIN_PROMPT_FIRST_PART_EN = """
You are a bot that makes decisions to create clips from video subtitles. If you think that the communication given below is worth to watch or relative to keywords reccomend according to the rules given below
IF a conversation is worth YES else say NO
Crop the video according to the rules given below
Write the start row number and end row number of the conversation you want to crop
Example Answer 1:
####
YES
START: 1
END: 3
####
Example Answer 2:
####
NO
####
Example Answer 3:
####
YES
START: 3
END: 5
####
!!NOTE FIRST ROW IS 1!!
Some keywords for it: 
"""
MAIN_PROMPT_SECOND_PART_EN = """
Some communication will be given in the bottom
Conversations:

"""

PROMPTS_PATH = "prompts/"
OUTPUT_PATH = "output/"

def download(link,save_path):
    yt = YouTube(link)
    try:
        file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').filter(resolution="1080p").first().download(save_path)
    except:
        try:
            file_path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').filter(resolution="720p").first().download(save_path)
        except:
            return 0
    return file_path

def highlight(videopath,temperature=TEMPERATURE,length=LENGTH,language=LANGUAGE, keywords=["viral","funny","highlights"]):
    skiprate = length * 2 / 3
    
    
    #user preferences debug
    print(f"Video path: {videopath}")
    print(f"Keywords: {keywords}")
    print(f"Length: {length}")
    print(f"Skip Rate: {skiprate}")
    print(f"Temperature: {temperature}")
    print(f"Language: {language}")
        
    language = language.lower()
    
    if os.path.isfile(f"{PROMPTS_PATH}start_{language}.txt"):
       with open(f"{PROMPTS_PATH}start_{language}.txt", "r", encoding = 'utf-8') as f:
            MAIN_PROMPT_FIRST_PART = f.read()
       with open(f"{PROMPTS_PATH}end_{language}.txt", "r", encoding = 'utf-8') as f:
            PROMPT_LAST_PART = f.read()
       
       MAIN_PROMPT = MAIN_PROMPT_FIRST_PART + str(keywords) + PROMPT_LAST_PART
       
       
    else:
       MAIN_PROMPT = MAIN_PROMPT_FIRST_PART_EN + str(keywords) + MAIN_PROMPT_SECOND_PART_EN


    

    mp3filepath = f"0.mp3"
    
    video = VideoFileClip(videopath)
    video.audio.write_audiofile(mp3filepath) 


    result = trasncribe(mp3filepath)
    


    try:
        class SubtitleVariable():
            start = 0.0
            end = 0.0
            text = ""

        subtitles = [{}]

        for i in range(0,len(result['segments'])):
          if(os.path.isfile(f"output{i}.mp4") ):
            os.remove(f"output{i}.mp4")

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

          if response.startswith("YES"):
            print(f"Start: {start}\nEnd: {end}")
            
            #part 2, process the start and end position
            crop_result = response
            
            #Process the result result is like:
            #START: 1
            #END: 2
            
            crop_result = crop_result.split("\n")
            
            
            if len(crop_result) >= 3:
               if crop_result[0].startswith("START:"):
                  start = result['segments'][i + int(crop_result[1].split(":")[1]) - 1]['start']
               if crop_result[1].startswith("END:"):
                  end =  result['segments'][i + int(crop_result[1].split(":")[1]) - 1]['start']
             
            #crop the video
            
            ffmpeg_extract_subclip(mp4filepath, start, end, targetname=f"output{i+ + int(crop_result[1].split(':')[1]) - 1}.mp4")
             
            

    except Exception as e:
        print(f"Some Error while creating highlights: {e}")
          
    files = os.listdir()
    for i in range(0,len(result['segments'])):
      if(os.path.isfile(f"output{i}.mp4")):
          min_start = yt.length

          for sub in subtitles[i]:
            if subtitles[i][sub].start < min_start:
              min_start = subtitles[i][sub].start

          file = pysrt.SubRipFile()

          for sub in subtitles[i]:
            sub_out = pysrt.SubRipItem(sub, start={'seconds': (subtitles[i][sub].start - min_start)}, end={'seconds': (subtitles[i][sub].end - min_start)}, text=subtitles[i][sub].text)
            file.append(sub_out)

          file.save(f"output{i}.srt")
    
