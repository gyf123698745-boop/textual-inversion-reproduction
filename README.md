# Textual Inversion Reproduction

A reproduction of **"An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion"** (Gal et al., 2022), using Stable Diffusion 1.5 and Hugging Face Diffusers.

## 1. Project Overview

Textual Inversion learns a new token embedding to represent a specific visual concept using a small number of reference images.

The pretrained diffusion model remains frozen during training. Only the embedding associated with the new placeholder token is optimized.

This project reproduces the method using six images of a cat toy and explores how learning rate and training checkpoints affect concept fidelity and editability.

## 2. Experimental Setup

| Component | Configuration |
|---|---|
| Base model | Stable Diffusion 1.5 |
| Dataset | `diffusers/cat_toy_example` (6 images) |
| Placeholder token | `<cat-toy>` |
| Initializer token | `toy` |
| Training steps | 3000 |
| Batch size | 1 |
| Gradient accumulation | 4 |
| Image resolution | 512 × 512 |
| GPU | NVIDIA RTX 5060 Laptop (8 GB VRAM) |
| Framework | PyTorch + Hugging Face Diffusers |

Two learning-rate configurations were evaluated:

| Configuration | Specified LR | Effective LR |
|---|---:|---:|
| Baseline | 5e-4 | 0.002 |
| Lower LR | 1e-4 | 0.0004 |

The effective learning rates account for the `--scale_lr` option.

Full training configurations and commands are documented in [`experiments/training_config.md`](experiments/training_config.md).

## 3. Experiments and Results

### 3.1 Training and Checkpoint Comparison

Two training runs were completed, each with 3000 optimization steps.

Embeddings saved at steps 500, 1000, 1500, 2000, 2500, and 3000 were evaluated using three prompts:

- `A photo of <cat-toy>`
- `A <cat-toy> backpack`
- `An oil painting of <cat-toy>`

A total of 36 images were generated.

Both learning-rate configurations captured recognizable characteristics of the reference cat toy, although some distinctive details were not consistently preserved.

Prompt-based editing was less reliable, particularly for the backpack prompt.

Comparison figures are available in [`results/checkpoint_comparison/`](results/checkpoint_comparison/).

### 3.2 Prompt Editing

The final embeddings were evaluated using three additional prompts:

- Scene editing: `A photo of <cat-toy> on a beach`
- Style editing: `A watercolor painting of <cat-toy>`
- Attribute editing: `A photo of <cat-toy> wearing a small red hat`

Scene and style modifications were partially successful.

However, neither embedding consistently generated the requested red hat, and some details of the original object were lost.

Generated images are available in [`results/prompt_editing/`](results/prompt_editing/).

### 3.3 CLIP Image Similarity

CLIP image embeddings were used to calculate the mean cosine similarity between each generated image and the six reference images.

Evaluation model: `openai/clip-vit-base-patch32`.

| Prompt | Effective LR = 0.0004 | Effective LR = 0.002 |
|---|---:|---:|
| Beach | 0.6882 | 0.7686 |
| Red hat | 0.7459 | 0.7422 |
| Watercolor | 0.7298 | 0.7045 |
| **Mean** | **0.7213** | **0.7384** |

The higher learning rate achieved a slightly higher mean similarity across the three prompts, with the largest difference observed in the beach scene.

However, CLIP image similarity is only an auxiliary measure of visual similarity. It does not directly evaluate prompt adherence or overall image quality.

The evaluation script is available at [`scripts/evaluate_clip.py`](scripts/evaluate_clip.py).

## 4. Repository Structure

```text
textual-inversion-reproduction/
├── README.md
├── requirements.txt
├── experiments/
│   ├── experiment_log.md
│   └── training_config.md
├── scripts/
│   ├── compare_embeddings.py
│   └── evaluate_clip.py
├── results/
│   ├── checkpoint_comparison/
│   └── prompt_editing/
└── report/
```

Detailed experimental procedures, observations, and limitations are recorded in [`experiments/experiment_log.md`](experiments/experiment_log.md).

## 5. Reproducibility

The experiments were conducted using the Hugging Face Diffusers Textual Inversion training example.

The training configuration and commands are documented in [`experiments/training_config.md`](experiments/training_config.md).

Python dependencies are listed in `requirements.txt`.

The repository contains experimental scripts and generated images. Pretrained model weights and trained Textual Inversion embeddings are not included.

The current scripts depend on local paths and require path adjustments before running on another machine.

## 6. Limitations

- Only two training runs were conducted.
- A common training random seed was not fixed.
- Generated images were evaluated using one inference seed.
- The number of evaluation prompts was limited.
- CLIP image similarity does not measure prompt adherence or editability directly.
- The experiments are exploratory and do not establish a general advantage for either learning rate.

## 7. Reference

Gal et al. (2022).

*An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion.*

arXiv:2208.01618.