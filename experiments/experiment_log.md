# Textual Inversion Reproduction — Experiment Log

## Project Overview

**Original Paper:** An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion

**Objective:** Reproduce Textual Inversion using Stable Diffusion 1.5 and investigate how learning rate and training steps affect concept fidelity and editability.

**Status:** Initial reproduction and exploratory comparison completed.

---

## 1. Experimental Environment

### Hardware
- GPU: NVIDIA GeForce RTX 5060 Laptop GPU (8 GB VRAM)
- System RAM: 16 GB
- Operating System: Windows 11

### Software
- Python: 3.12.9
- PyTorch: 2.14.1+cu132
- Diffusers: 0.41.0.dev0
- Transformers: 5.19.0
- Accelerate: 1.15.0

### Model and Dataset
- Pretrained model: Stable Diffusion 1.5
- Dataset: `diffusers/cat_toy_example`
- Number of training images: 6
- Placeholder token: `<cat-toy>`
- Initializer token: `toy`
- Learnable property: `object`

The pretrained diffusion model was frozen during training.
Only the embedding associated with the placeholder token was optimized.

---

## 2. Experiment 01 — Baseline Training

### Objective

Train a Textual Inversion embedding for a specific cat toy using a pretrained Stable Diffusion model.

### Training Configuration

| Parameter | Value |
|---|---|
| Pretrained Model | Stable Diffusion 1.5 |
| Training Steps | 3000 |
| Batch Size | 1 |
| Gradient Accumulation Steps | 4 |
| Effective Batch Size | 4 |
| Configured Learning Rate | 0.0005 |
| Effective Learning Rate | 0.002 |
| Learning Rate Scheduler | Constant |
| Resolution | 512 × 512 |
| Gradient Checkpointing | Enabled |
| Initializer Token | toy |

The effective learning rate was scaled by the training script using the `--scale_lr` option.

### Results

- Training completed successfully after 3000 steps.
- The learned embedding was saved as a `.safetensors` file.
- Intermediate embeddings were saved at steps 500, 1000, 1500, 2000, 2500, and 3000.

### Output Directory

`textual_inversion_cat_3000/`

---

## 3. Experiment 02 — Initial Generation Test

### Objective

Verify whether the learned embedding can be used to generate images with a new text prompt.

### Inference Configuration

- Model: Stable Diffusion 1.5
- Embedding: Baseline, 3000 steps
- Prompt: `A <cat-toy> backpack`
- Inference Steps: 50

### Observations

The generated image retained some visual characteristics of the target cat toy.

However, the backpack concept was not clearly represented.

### Preliminary Interpretation

The embedding appeared to capture some features of the target concept, but this single image was insufficient to evaluate editability.

### Limitations

Only one image was generated in this initial test.

---

## 4. Experiment 03 — Lower Learning Rate Training

### Objective

Investigate the effect of reducing the learning rate while keeping the main training configuration unchanged.

### Modification

| Parameter | Baseline | Experiment 03 |
|---|---|---|
| Configured Learning Rate | 0.0005 | 0.0001 |
| Effective Learning Rate | 0.002 | 0.0004 |
| Training Steps | 3000 | 3000 |
| Effective Batch Size | 4 | 4 |
| Dataset | Cat Toy | Cat Toy |
| Pretrained Model | SD 1.5 | SD 1.5 |

### Results

- Training completed successfully after 3000 steps.
- Intermediate embeddings were saved for comparison.
- The final embedding was saved successfully.

### Output Directory

`textual_inversion_cat_lr0001_3000/`

---

## 5. Experiment 04 — Learning Rate × Training Steps Comparison

### Objective

Compare the effects of learning rate and training steps on concept fidelity and editability.

### Experimental Design

Two learning rates and six training checkpoints were evaluated.

| Learning Rate / Steps | 500 | 1000 | 1500 | 2000 | 2500 | 3000 |
|---|---|---|---|---|---|---|
| 0.002 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 0.0004 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

This resulted in 12 experimental conditions.

### Evaluation Prompts

1. `A photo of <cat-toy>`
2. `A <cat-toy> backpack`
3. `An oil painting of <cat-toy>`

Each condition was evaluated using all three prompts.

Total generated images: 36.

### Inference Configuration

- Base Model: Stable Diffusion 1.5
- Inference Steps: 30
- Guidance Scale: 7.5
- Random Seed: 42
- Image Resolution: 512 × 512

The same inference settings and random seed were used across all conditions.

### Generated Figures

- `Photo.png`
- `Backpack.png`
- `Oil_painting.png`

### Qualitative Observations

**Concept Fidelity**

Both learning rates produced images containing recognizable characteristics of the original cat toy.

The generated images often preserved:
- Blue-gray cat head
- Pointed ears
- Colorful striped body

However, some distinctive details, particularly the curved tail and facial features, were not consistently reproduced.

The higher learning rate appeared to preserve the target concept more consistently in some samples, but this observation requires further evaluation.

**Editability**

The backpack prompt often produced images resembling the original toy rather than clearly identifiable backpacks.

The oil painting prompt did not consistently produce an obvious painting style.

These observations suggest that the tested prompts did not consistently produce the intended edits.

However, prompt ambiguity and other factors prevent a definitive conclusion about the learned embedding's editability.

**Safety Checker**

At least one generated image was replaced with a black image following a safety-checker warning.

This sample should be marked as safety-filtered rather than treated as a generation-quality failure.

---

## 6. Limitations

The current evaluation has several limitations:

1. Only one inference random seed was used.
2. The two training runs did not use a strictly controlled common training seed.
3. Evaluation was primarily qualitative.
4. No quantitative fidelity or text-alignment metrics were calculated.
5. Some evaluation prompts were ambiguous.
6. Checkpoints from the same training run are not independent training replicates.

Therefore, the results should be interpreted as exploratory observations rather than statistically established conclusions.

---

## 7. Experiment 05 — Improved Prompt Evaluation

### Objective

Evaluate the editability of the learned cat-toy concept using
scene, style, and attribute editing prompts.

### Experimental Setup

Two embeddings trained for 3000 steps were compared:

- Effective learning rate: 0.002
- Effective learning rate: 0.0004

The same pretrained model and inference settings were used.

### Evaluation Prompts

1. Scene editing: A photo of <cat-toy> on a beach
2. Style editing: A watercolor painting of <cat-toy>
3. Attribute editing: A photo of <cat-toy> wearing a small red hat

A total of six images were generated.

### Results

**Scene Editing**

Both embeddings successfully generated beach environments.

However, several distinctive features of the original cat toy,
including its colorful vertical stripes and curved tail,
were not consistently preserved.

**Style Editing**

Both embeddings produced recognizable watercolor-style images.

The learned concept was partially preserved, although facial
features and object structure differed from the reference images.

**Attribute Editing**

Neither embedding clearly satisfied the instruction to place
a small red hat on the cat toy.

The lower-learning-rate result contained a red accessory,
but its relationship to the requested hat was ambiguous.

### Discussion

The results suggest that the learned embeddings can respond
to some scene and style modifications.

Attribute editing was less successful in the tested examples.

No consistent overall advantage of either learning rate
was established from these six images.

### Limitations

The evaluation used only one random seed and three prompts.
Additional prompts and seeds are required for more reliable conclusions.

### Status

Completed.

---

## 8. Preliminary Conclusion

The Textual Inversion reproduction successfully learned a new token embedding representing a specific cat toy.

The initial experiments demonstrate that the learned embedding can reproduce several recognizable visual features of the target concept.

A preliminary comparison across two learning rates and six training checkpoints has been completed.

Further evaluation is required to determine how learning rate and training duration affect the tradeoff between concept fidelity and editability.

## Experiment 06: CLIP Image Similarity Evaluation

### Objective
Quantitatively compare the visual similarity between generated images
and the six reference images using CLIP image embeddings.

### Setup
- Model: openai/clip-vit-base-patch32
- Reference images: 6
- Generated images: 6
- Training checkpoint: 3000 steps
- Effective learning rates: 0.002 and 0.0004
- Prompts: Beach, Red hat, Watercolor
- Metric: Mean cosine similarity between each generated image embedding
  and the six reference image embeddings.

### Results

| Prompt | LR = 0.0004 | LR = 0.002 |
|---|---:|---:|
| Beach | 0.6882 | 0.7686 |
| Red hat | 0.7459 | 0.7422 |
| Watercolor | 0.7298 | 0.7045 |
| Average | 0.7213 | 0.7384 |

### Observations
The higher learning rate achieved a slightly higher average CLIP image
similarity across the three prompts. However, the lower learning rate
performed better on the Red hat and Watercolor prompts.

### Limitations
CLIP image similarity measures visual feature similarity rather than
prompt adherence or overall generation quality. Only one inference seed
was evaluated, and the two training runs did not use a controlled
common training seed. Therefore, these results are exploratory and do
not establish that either learning rate is generally superior.