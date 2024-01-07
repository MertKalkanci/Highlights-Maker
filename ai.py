import whisper
import openai
from openai import OpenAI
from llama_cpp import Llama

model_audio = whisper.load_model("base")

class llm_manager():
  def __init__(self, llm="OPENAI", path=""):
    if llm == "OPENAI":
      self.client = OpenAI(api_key=open("openai", "r").read())
      self.type = "OPENAI"
    else:
      self.llm = Llama(path)
      self.type = "LOCAL GGUF"

  def generate(self, system, chat, temperature):
    if self.type == "OPENAI":
      return self.gpt(system, chat, temperature)
    elif self.type == "LOCAL GGUF":
      return self.llama(system, chat)

  def gpt(self, system, chat, temperature):
    return self.client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      temperature = temperature,
      messages=[
          {"role": "system", "content": system},
          {"role": "user", "content": chat},
      ]
      ).choices[0].message.content

  def llama(self, system, chat):
    return self.llm(f"System: \n{system}\nUser: \n{chat}")["choices"][0]["text"]

def trasncribe(video_path):
  return model_audio.transcribe(video_path)