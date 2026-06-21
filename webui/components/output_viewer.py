# webui/components/output_viewer.py
import gradio as gr


def render_output_viewer():
    """Renders the execution logs panel along with final checked images."""
    gr.Markdown("#### 📤 Output & Validation Layer")

    viewer = gr.Image(
        label="Verified Pipeline Output",
        type="pil",
        interactive=False
    )

    logs = gr.Textbox(
        label="Agent Execution Logs",
        placeholder="Pipeline idle. Waiting for user intent...",
        lines=8,
        max_lines=14,
        interactive=False
    )
    return viewer, logs