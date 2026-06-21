# webui/components/prompt_panel.py
import gradio as gr

def render_prompt_panel():
    """Renders the chat intent textbox interface."""
    text_input = gr.Textbox(
        label="Chat Intent (Natural Language Directive)",
        placeholder="e.g., 'Replace the old rusted wheel with a clean futuristic cyber tire'",
        lines=3,
        max_lines=5
    )
    return text_input