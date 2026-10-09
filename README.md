# Textual Inversion Reproduction

Reproduction of the paper
"An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion".

## 1. Project Overview

This project reproduces Textual Inversion using Stable Diffusion v1.5
and the Hugging Face Diffusers implementation.

The objective is to learn a new token embedding from a small set
of reference images while keeping the pretrained diffusion model frozen.

## 2. Experimental Setup

- Base model: Stable Diffusion v1.5
- Dataset: `diffusers/cat_toy_example` (6 images)
- Placeholder token: `<cat-toy>`
- Initializer token: `toy`
- Image resolution: 512 × 512
- Training steps: 3000
- Batch size: 1
- Gradient accumulation steps: 4
- Learning rate scheduler: Constant
- Hardware: NVIDIA RTX 5060 Laptop GPU (8 GB VRAM)

Two learning-rate configurations were tested:

| Experiment | Configured LR | Effective LR |
|------------|---------------|--------------|
| Baseline | 5e-4 | 0.002 |
| Lower LR | 1e-4 | 0.0004 |

The effective learning rates account for the `--scale_lr` option.

## 3. Experiments

The experiments investigate:

1. Textual Inversion training and image generation.
2. The effects of learning rate and training checkpoints.
3. Prompt-based editing and generalization to new contexts.
4. CLIP-based image similarity evaluation (in progress).

## 4. Repository Structure

- `scripts/`: Experimental scripts.
- `experiments/`: Experiment logs and observations.
- `results/checkpoint_comparison/`: Learning-rate and checkpoint comparisons.
- `results/prompt_editing/`: Prompt editing results.
- `report/`: Reproduction report.

## 5. Evaluation

Evaluation results will be added after the CLIP similarity experiment.

## 6. References

Gal et al., "An Image is Worth One Word:
Personalizing Text-to-Image Generation using Textual Inversion" (2022).