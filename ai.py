import whisper
import openai
from openai import OpenAI
from llama_cpp import Llama


local_llm = open("local", "r")
if local_llm == "":
  client = OpenAI(api_key=open("openai", "r").read())
else:
  llm = Llama(local_llm)

model_audio = whisper.load_model("base")

def gpt(system, chat, temperature):
  if local_llm == "":
    response = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      temperature = temperature,
      messages=[
          {"role": "system", "content": system},
          {"role": "user", "content": chat},
      ]
  ).choices[0].message.content
  else:
    response = llm(f"""
System: \n{system}
User: \n{chat}
""")["choices"][0]["text"]
  return response

def trasncribe(video_path):
  return model_audio.transcribe(video_path)