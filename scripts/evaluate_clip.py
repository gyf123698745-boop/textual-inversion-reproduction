import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

MODEL_ID = "openai/clip-vit-base-patch32"

model = CLIPModel.from_pretrained(MODEL_ID, use_safetensors=False)
processor = CLIPProcessor.from_pretrained(MODEL_ID)

model.eval()

print("CLIP model loaded successfully!")

from pathlib import Path
import torch.nn.functional as F

# Reference images
REFERENCE_DIR = Path(
    r"C:\Users\G\Desktop\diffusers\examples\textual_inversion\cat"
)

# Generated images
GENERATED_DIR = Path(
    r"C:\Users\G\Desktop\paper representation\results\prompt_editing"
)

# Only evaluate individual generated images, not comparison grids
generated_files = sorted(
    p for p in GENERATED_DIR.glob("*.png")
    if "_LR " in p.name
)

reference_files = sorted(REFERENCE_DIR.glob("*.jpeg"))

print(f"Reference images: {len(reference_files)}")
print(f"Generated images: {len(generated_files)}")


def encode_image(path):
    image = Image.open(path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        features = model.get_image_features(**inputs).pooler_output

    features = F.normalize(features, dim=-1)

    return features


reference_features = torch.cat(
    [encode_image(path) for path in reference_files],
    dim=0
)

print("\nCLIP Image Similarity Results")

for path in generated_files:
    generated_features = encode_image(path)

    similarities = generated_features @ reference_features.T

    mean_similarity = similarities.mean().item()

    print(f"{path.name}: {mean_similarity:.4f}")