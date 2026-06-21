# webui/components/__init__.py
"""
Modular UI Components for the FluxStudio WebUI Layout Layer.
"""

from .input_canvas import render_input_canvas
from .prompt_panel import render_prompt_panel
from .output_viewer import render_output_viewer

__all__ = [
    "render_input_canvas",
    "render_prompt_panel",
    "render_output_viewer",
]