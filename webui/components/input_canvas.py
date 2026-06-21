# webui/components/input_canvas.py
import gradio as gr

def render_input_canvas():
    """Renders the main image editing field and masking layer."""
    gr.Markdown("#### 📥 Input Layer")
    canvas = gr.ImageEditor(
        label="Canvas (Upload Image & Draw Mask Layer)",
        type="pil",
        crop_size=None,
        transforms=None,
        brush=gr.Brush(colors=["#FF0000"], color_mode="fixed")
    )
    return canvas