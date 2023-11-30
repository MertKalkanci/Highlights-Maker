import whisper
import openai
from openai import OpenAI

client = OpenAI(api_key=open("openai", "r").read())

model = whisper.load_model("base")

def gpt(system, chat, temperature):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    temperature = temperature,
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": chat},
    ]
)
  return response.choices[0].message.content

def trasncribe(video_path):
  return model.transcribe(video_path)