from code_tasks import perform_task

import gradio as gr

with gr.Blocks() as demo:
    query = gr.Textbox(label="Google search")
    output = gr.Textbox(label="Result")
    search_btn = gr.Button("Go")
    search_btn.click(perform_task, inputs=query, outputs=output)

demo.launch()