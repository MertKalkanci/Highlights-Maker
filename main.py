import sys
import gradio as gr
from highlight import highlight
from youtube import download

languages = ["EN","TR"]
download_status = 0
generation_status = 0

with gr.Blocks() as interface:
    with gr.Tab(label="Highlight"):
        file_path = gr.FileExplorer(label="Video",file_count="single", glob="*/*.mp4")
        temperature = gr.Slider(minimum=0, maximum=2,value=0.35, step=0.05, label="AI Temperature")
        length = gr.Slider(minimum=18, maximum=60, step=3, label="Dialogue Length", value=30, info="How many sentences AI will process at once (higher = faster generation & less chance of getting rate limited by openai)")
        language = gr.Dropdown(languages, label="Language")
        keywords = gr.Textbox(label="Keywords", placeholder="viral, funny, highlights", info="write diffrent keywords comma separated")
        ai = gr.Dropdown(["OPENAI","LOCAL GGUF"], label="AI to interpret the video script")
        ai_path = gr.FileExplorer(label="Local AI Model",file_count="single", glob="*/*.gguf")
        generate_button = gr.Button(value="Generate")
        is_generated = gr.Textbox(label="Is Generated?", interactive=False)
    with gr.Tab(label="Download"):
        link = gr.Textbox(label="Link")
        download_button = gr.Button(value="Download")
        out_video = gr.Video(label="Video")
    
    download_button.click(fn=download, inputs=link, outputs=out_video)
    generate_button.click(fn=highlight, inputs=[file_path, temperature, length, language, keywords, ai, ai_path], outputs=is_generated)

is_shared = len(sys.argv) > 1 and sys.argv[1] == "--share"

interface.launch(share=is_shared)