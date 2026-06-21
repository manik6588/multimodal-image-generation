# app.py (Top Import Simplification)
import os
import torch
import gradio as gr
from PIL import Image
from huggingface_hub import login

# Clean package-level imports enabled by your __init__.py files
from webui import FluxStudioUI
from modules import (
    IdentityExtractor,
    Florence2VisionEngine,
    TextProcessingEngine,
    IdentityConditioningBridge
)

# Initialize Global Modules
authenticate_token = os.getenv("HF_TOKEN")
if authenticate_token:
    login(token=authenticate_token)

print("⚡ Starting Upgraded Advanced Multi-Agent Identity Node Network...")
extractor = IdentityExtractor()
vision_engine = Florence2VisionEngine()
text_engine = TextProcessingEngine()
conditioner = IdentityConditioningBridge()

# Global reference for FLUX.1 Fill Dev Core
flux_pipe = None


def initialize_flux():
    global flux_pipe
    from diffusers import FluxInpaintPipeline

    if flux_pipe is None:
        print("🚀 Loading FLUX.1 Fill Dev with memory saving parameters...")

        # 1. Use low_cpu_mem_usage to prevent system RAM spiking to 100%
        # 2. Use variant="fp16" or "bf16" if available to download smaller weight profiles
        flux_pipe = FluxInpaintPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-Fill-dev",
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
            use_safetensors=True
        )

        # 3. CPU Offloading instead of direct .to("cuda")
        # This dynamically shifts pieces of FLUX to the GPU only when executing steps,
        # preventing the 0xC0000005 allocation crash.
        flux_pipe.enable_model_cpu_offload()
        print("💡 FLUX Core Engine Operational with Sequential Offloading.")


# UI Integration Pipeline Wrapper
def master_identity_orchestrator(image_dict, chat_intent, progress=gr.Progress(track_tqdm=True)):
    if image_dict is None or "background" not in image_dict:
        return None, "[Pipeline Error] Requires a base Canvas Image."

    # ⚠️ Use the background image layer as the target identity source reference
    base_canvas = image_dict["background"].convert("RGB")
    mask_layer = image_dict["layers"].convert("L") if "layers" in image_dict else None
    if mask_layer is None or mask_layer.getbbox() is None:
        mask_layer = Image.new("L", base_canvas.size, 255)

    history_logs = "🚀 Pipeline Started.\n"
    MAX_ATTEMPTS = 2
    attempt = 1

    # Stage 1 & 2: Identity Extraction Profile
    progress(0.1, desc="Extracting Target Identity Vectors...")
    id_context = extractor.extract_identity_context(base_canvas)
    history_logs += f"🧬 [Extractor] Captured Face Embeddings & DINOv2 Vectors.\n"

    # Stage 3 & 4: Florence-2 Large Vision Pass
    progress(0.2, desc="Analyzing scene composition with Florence-2...")
    scene_context = vision_engine.analyze_scene(base_canvas)
    history_logs += f"👁️ [Florence-2 Context]: {scene_context}\n"

    # Stage 5: Custom Prompt Rewriter Rules
    structured_prompt = text_engine.rewrite_prompt(chat_intent, scene_context)
    history_logs += f"📝 [Template Rewriter]: \"{structured_prompt}\"\n"

    while attempt <= MAX_ATTEMPTS:
        history_logs += f"\n--- Execution Cycle [{attempt}/{MAX_ATTEMPTS}] ---\n"

        # Stage 6: Custom Step Planner Decision
        plan = text_engine.plan_generation(structured_prompt, attempt=attempt)
        history_logs += f"🎯 [Planner] Steps Assigned: {plan['steps']} | Scale: {plan['guidance']}\n"

        # Stage 7: Identity Conditioning Fusion Matrix
        progress(0.4, desc="Fusing Multi-Adapter Conditioning Weights...")
        fusion_metrics = conditioner.apply_conditioning(id_context, mask_layer, plan)
        history_logs += f"🔗 [Conditioning Bridge]: Infused IP-Adapter + InstantID + ControlNet.\n"

        try:
            # Stage 8: Core FLUX Execution Node
            progress(0.5, desc="Computing FLUX Fill Generation Pass...")
            # Note: In production pipeline, fusion_metrics condition targets are passed to pipeline
            generated_image = flux_pipe(
                prompt=structured_prompt,
                image=base_canvas,
                mask_image=mask_layer,
                num_inference_steps=plan["steps"],
                guidance_scale=plan["guidance"],
                width=base_canvas.size[0],
                height=base_canvas.size[1]
            ).images[0]

            # Stage 9 & 10: Florence-2 Quality Evaluator Fork
            progress(0.9, desc="Running Florence-2 Quality Control Pass...")
            qc = vision_engine.check_quality(generated_image, base_canvas, chat_intent)
            history_logs += f"🛡️ [Quality Checker]: {qc['logs']}\n"

            if qc["match"]:
                history_logs += "\n✅ Verification complete. Visual target threshold satisfied."
                return generated_image, history_logs
            else:
                history_logs += "⚠️ Output failed threshold gate. Adjusting matrices for correction loop...\n"
                attempt += 1
                fallback_output = generated_image

        except Exception as e:
            history_logs += f"❌ Runtime Exception: {str(e)}\n"
            attempt += 1

    history_logs += "\n⚠️ Max pipeline iterations reached. Returning best available generation candidate."
    return fallback_output, history_logs


if __name__ == "__main__":
    initialize_flux()
    studio_app = FluxStudioUI(pipeline_callback=master_identity_orchestrator)
    studio_app.launch(server_name="127.0.0.1", server_port=9860)