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
        temperature = gr.Slider(minimum=0, maximum=2,value=0.35, step=0.05, label="Temperature")
        length = gr.Slider(minimum=30, maximum=60, step=3, label="Dialogue Length", value=30, info="How many sentences AI will process at once (higher = faster generation & less chance of getting rate limited by openai)")
        language = gr.Dropdown(languages, label="Language")
        keywords = gr.Textbox(label="Keywords", placeholder="viral, funny, highlights", info="write diffrent keywords comma separated")
        generate_button = gr.Button(value="Generate")
    with gr.Tab(label="Download"):
        link = gr.Textbox(label="Link")
        download_button = gr.Button(value="Download")
    
    download_button.click(fn=download, inputs=link)
    generate_button.click(fn=highlight, inputs=[file_path, temperature, length, language, keywords])

is_shared = len(sys.argv) > 1 and sys.argv[1] == "--share"

interface.launch(share=is_shared)