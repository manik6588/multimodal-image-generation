import gradio as gr
from webui.components.input_canvas import render_input_canvas
from webui.components.prompt_panel import render_prompt_panel
from webui.components.output_viewer import render_output_viewer


class FluxStudioUI:
    def __init__(self, pipeline_callback):
        """
        :param pipeline_callback: Central orchestration method mapped from app.py
        """
        self.pipeline_callback = pipeline_callback
        self.interface = self.build_interface()

    def build_interface(self):
        with gr.Blocks(theme=gr.themes.Default(primary_hue="blue", secondary_hue="slate")) as demo:
            gr.Markdown(
                """
                # ⚡ Agentic FLUX Studio
                ### Image ➔ Vision ➔ Prompt Rewriter ➔ Planner ➔ Conditioning ➔ FLUX Fill ➔ Quality Checker
                """
            )
            gr.HTML("<hr style='border: 1px solid #e2e8f0; margin-bottom: 20px;'>")

            with gr.Row():
                # Left Column: Inputs assembling custom components
                with gr.Column(scale=5):
                    input_img = render_input_canvas()
                    chat_input = render_prompt_panel()

                    with gr.Row():
                        clear_btn = gr.ClearButton([input_img, chat_input], variant="stop")
                        submit_btn = gr.Button("Execute Agentic Pipeline", variant="primary")

                # Right Column: Outputs
                with gr.Column(scale=5):
                    output_img, pipeline_logs = render_output_viewer()

            # Centralized Pipeline Interlock Event Mappings
            submit_btn.click(
                fn=self.pipeline_callback,
                inputs=[input_img, chat_input],
                outputs=[output_img, pipeline_logs]
            )
            chat_input.submit(
                fn=self.pipeline_callback,
                inputs=[input_img, chat_input],
                outputs=[output_img, pipeline_logs]
            )

        return demo

    def launch(self, server_name="127.0.0.1", server_port=9860, share=False):
        print(f"Launching Layout System Node on http://{server_name}:{server_port}")
        self.interface.launch(server_name=server_name, server_port=server_port, share=share)