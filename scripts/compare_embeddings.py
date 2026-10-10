
import os
import torch
from PIL import Image, ImageDraw
from safetensors.torch import load_file
from diffusers import StableDiffusionPipeline

MODEL = "stable-diffusion-v1-5/stable-diffusion-v1-5"
TOKEN = "<cat-toy>"

from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--embeddings_dir",
    type=Path,
    required=True,
    help="Directory containing the two training output folders",
)
args = parser.parse_args()

EXPERIMENTS = [
    ("LR 0.002", str(args.embeddings_dir / "textual_inversion_cat_3000")),
    ("LR 0.0004", str(args.embeddings_dir / "textual_inversion_cat_lr0001_3000")),
]

STEPS = [3000]

PROMPTS = {
    "Beach": "A photo of <cat-toy> on a beach",
    "Watercolor": "A watercolor painting of <cat-toy>",
    "Red_hat": "A photo of <cat-toy> wearing a small red hat",
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = PROJECT_ROOT / "results" / "prompt_editing"
OUTPUT.mkdir(parents=True, exist_ok=True)

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL,
    torch_dtype=torch.float16,
).to("cuda")

pipe.set_progress_bar_config(disable=True)

# 首次注册新 Token，之后只替换其向量
first_path = os.path.join(
    EXPERIMENTS[0][1],
    "learned_embeds-steps-3000.safetensors",
)
pipe.load_textual_inversion(first_path, token=TOKEN)

token_id = pipe.tokenizer.convert_tokens_to_ids(TOKEN)
embedding_weights = pipe.text_encoder.get_input_embeddings().weight

for prompt_name, prompt in PROMPTS.items():
    canvas = Image.new("RGB", (512, 550 * 2), "white")
    draw = ImageDraw.Draw(canvas)

    for row, (experiment_name, folder) in enumerate(EXPERIMENTS):
        for col, step in enumerate(STEPS):
            path = os.path.join(
                folder,
                f"learned_embeds-steps-{step}.safetensors",
            )

            # 加载对应训练阶段的词向量
            learned = load_file(path)
            vector = learned[TOKEN].squeeze(0)

            with torch.no_grad():
                embedding_weights[token_id].copy_(
                    vector.to(
                        device=embedding_weights.device,
                        dtype=embedding_weights.dtype,
                    )
                )

            # 所有实验使用相同随机种子
            generator = torch.Generator(
                device="cuda"
            ).manual_seed(42)

            with torch.inference_mode():
                image = pipe(
                    prompt,
                    num_inference_steps=30,
                    guidance_scale=7.5,
                    generator=generator,
                ).images[0]
                image.save(OUTPUT/f"{prompt_name}_{experiment_name}_{step}.png")

            x = col * 512
            y = row * 550

            draw.text(
                (x + 12, y + 12),
                f"{experiment_name} | {step} steps",
                fill="black",
            )
            canvas.paste(image, (x, y + 38))

            print(f"Completed: {prompt_name}, {experiment_name}, {step}")

    output_path = OUTPUT / f"{prompt_name}.png"
    canvas.save(output_path, format="PNG")
    print(f"Saved: {output_path}")

print("All comparisons finished!")

