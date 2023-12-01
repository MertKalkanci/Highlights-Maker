# Highlights-Maker

## Description

An application that uses OpenAI's Whisper and ChatGPT API to generate clips from videos dialogues according to the keywords given from the user.

## To - Do

- [X] Exporting transcripts as .srt files
- [ ] Adding UI selection support to select diffrent ChatGPT & Whisper models
- [ ] Adding support of diffrent LLM's such as Llama 2, Mistral, Falcon etc.
- [ ] Automatically buning transcripts as subtitles to the video
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
3) run main.py from the virtual environment you created
(Use `--share` option to make gradio interface public)


