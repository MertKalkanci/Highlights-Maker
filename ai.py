import whisper
import openai
from openai import OpenAI
from llama_cpp import Llama

model_audio = whisper.load_model("base")

class llm_manager():
  def ___init___(self, llm="OPENAI", path=""):
    if llm == "OPENAI":
      self.client = OpenAI(api_key=open("openai", "r").read())
    else:
      self.llm = Llama(path)

  def generate(self, system, chat, temperature):
    if self.llm == "OPENAI":
      return self.gpt(system, chat, temperature)
    elif self.llm == "LOCAL GGUF":
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