# modules/text_engine.py
class TextProcessingEngine:
    def rewrite_prompt(self, user_instruction, scene_context):
        """Applies programmatic layout templates and token injection rules."""
        base_template = f"High-fidelity modification, {user_instruction}. Matching ambient profile: {scene_context}."
        return base_template

    def plan_generation(self, prompt, attempt=1):
        """Custom Python planner managing dynamic steps."""
        steps = 24 if len(prompt) > 100 else 18
        if attempt > 1:
            steps = min(steps + (attempt * 4), 45)
        return {"steps": steps, "guidance": 28.0}