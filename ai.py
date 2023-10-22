import whisper
import openai

openai.api_key = open("openai", "r").read()

model = whisper.load_model("base")

def gpt(system, chat, temperature):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = temperature,
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": chat},
    ]
)
  return response['choices'][0]['message']['content']

def trasncribe(video_path):
  return model.transcribe(video_path)