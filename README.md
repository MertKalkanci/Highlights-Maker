# Highlights-Maker

## Description

An application that uses OpenAI's Whisper and ChatGPT API to generate clips from videos dialogues according to the keywords given from the user.

## Give a Star! ⭐

Feel free to request an issue on github if you find bugs or request a new feature. 
If you find this useful, please give it a star to show your support for this project.

## To - Do

- [X] Exporting transcripts as .srt files
- [X] Adding UI selection support to select diffrent ChatGPT & Whisper models
- [X] Adding support of diffrent LLM's such as Llama 2, Mistral, Falcon etc.
- [ ] Automatically burning transcripts as subtitles to the video
- [ ] Optimising prompts
- [ ] More language support
- [ ] Automatic environment manager shell files

## Packages Needed
- openai-whisper 
- pytube 
- moviepy 
- pydub 
- openai 
- pysrt
- gradio

you can install required packages with:

``` 
pip install -r requirements.txt
```

## How To Use

1) Create a virtual environment
2) install required packages
3)
  A) If you plan to use ChatGPT paste your API key into a file named `openai`
  B) If you plan to use an gguf file compatible with llama.cpp, install llama.cpp into `Highlights-Maker` folder and move your .gguf file into the project folder

4) Run main.py from the virtual environment you created
5) Select your AI type and select .gguf file if you are not using OpenAI
6) Upload video file into `Highlights-Maker` to select or download via youtube link on youtube tab
(Use `--share` option to make gradio interface public)


