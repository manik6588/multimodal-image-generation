# modules/__init__.py
"""
Backend Processing Nodes for the Agentic FLUX Studio.
Contains extraction, vision processing, prompt text generation, and conditioning bridges.
"""

from .extractors import IdentityExtractor
from .vision import Florence2VisionEngine
from .text_engine import TextProcessingEngine
from .conditioners import IdentityConditioningBridge

__all__ = [
    "IdentityExtractor",
    "Florence2VisionEngine",
    "TextProcessingEngine",
    "IdentityConditioningBridge",
]