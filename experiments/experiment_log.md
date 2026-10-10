# Textual Inversion Reproduction — Experiment Log

## 1. Project Overview and Environment

**Paper:** Gal et al., *An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion* (2022).

**Objective:** Reproduce Textual Inversion with Stable Diffusion 1.5 and explore concept fidelity and prompt-based editability across two learning-rate configurations and training checkpoints.

**Hardware:** NVIDIA RTX 5060 Laptop GPU (8 GB VRAM), 16 GB RAM, Windows 11.

**Software:** Python 3.12.9; PyTorch 2.14.1+cu132; Diffusers 0.41.0.dev0; Transformers 5.19.0; Accelerate 1.15.0.

**Model/data:** Stable Diffusion 1.5; `diffusers/cat_toy_example` (six reference images); placeholder token `<cat-toy>` initialized from `toy`; learnable property `object`.

The pretrained diffusion model was frozen during training. The new placeholder-token embedding was optimized. Full training commands are documented in [`training_config.md`](training_config.md).

## 2. Experiment 01 — Baseline Training

**Objective:** Learn a token embedding for the specific cat toy.

| Parameter | Value |
|---|---|
| Training steps | 3000 |
| Batch size / gradient accumulation | 1 / 4 |
| Effective batch size | 4 |
| Configured LR / effective LR | 0.0005 / 0.002 |
| LR scheduler | Constant |
| Resolution | 512 × 512 |
| Gradient checkpointing | Enabled |
| Initializer token | `toy` |

The effective learning rate reflects `--scale_lr`. Training completed successfully; embeddings were saved at steps 500, 1000, 1500, 2000, 2500, and 3000, including the final `.safetensors` embedding.

**Local output directory:** `textual_inversion_cat_3000/`.

## 3. Experiment 02 — Initial Generation Test

**Objective:** Check whether the learned embedding works in a new prompt.

**Setup:** Baseline 3000-step embedding; prompt `A <cat-toy> backpack`; 50 inference steps.

**Observation:** The image retained some recognizable toy characteristics, but the backpack concept was not clearly represented. A single generated image cannot establish editability.

## 4. Experiment 03 — Lower Learning Rate Training

**Objective:** Explore a lower configured learning rate while retaining the main training settings.

| Parameter | Baseline | Lower LR |
|---|---:|---:|
| Configured LR | 0.0005 | 0.0001 |
| Effective LR (`--scale_lr`) | 0.002 | 0.0004 |
| Training steps | 3000 | 3000 |
| Effective batch size | 4 | 4 |
| Dataset / model | Cat toy / SD 1.5 | Cat toy / SD 1.5 |

Training completed successfully and intermediate and final embeddings were saved.

**Local output directory:** `textual_inversion_cat_lr0001_3000/`.

## 5. Experiment 04 — Learning Rate × Checkpoint Comparison

**Objective:** Explore how learning rate and training progress relate to concept fidelity and editability.

**Design:** Two completed training runs, each evaluated at six checkpoints (500, 1000, 1500, 2000, 2500, 3000 steps). This gives **12 checkpoint conditions, not 12 independent training runs**.

**Prompts:**

1. `A photo of <cat-toy>`
2. `A <cat-toy> backpack`
3. `An oil painting of <cat-toy>`

**Inference:** 30 steps; CFG 7.5; seed 42; 512 × 512. Total: 36 generated images.

**Figures:** [`Photo.png`](../results/checkpoint_comparison/Photo.png), [`Backpack.png`](../results/checkpoint_comparison/Backpack.png), [`Oil_painting.png`](../results/checkpoint_comparison/Oil_painting.png).

**Observations:** Both configurations generated recognizable features of the cat toy, including its blue-gray head, pointed ears, and colorful striped body. Details such as the curved tail and facial features were inconsistent. The backpack prompt often failed to produce a clear backpack, and the oil-painting style was inconsistent. A higher LR appeared to preserve the target concept more consistently in some samples, but the limited comparisons do not support a general conclusion.

**Safety-checker note:** At least one image was replaced by a black image after a safety-checker warning; this should be marked as filtered/invalid rather than scored as a generation-quality failure.

## 6. Experiment 05 — Prompt Editing Evaluation

**Objective:** Test scene, style, and attribute editing with the final 3000-step embeddings.

**Design:** Two effective learning rates (0.002 and 0.0004), three prompts, six generated images. The same pretrained model and inference settings were used (30 steps, CFG 7.5, seed 42, 512 × 512).

| Editing type | Prompt | Observation |
|---|---|---|
| Scene | `A photo of <cat-toy> on a beach` | Beach environments appeared, but stripes and curved tail were not always preserved. |
| Style | `A watercolor painting of <cat-toy>` | Watercolor style appeared, with some loss of object structure and facial detail. |
| Attribute | `A photo of <cat-toy> wearing a small red hat` | Neither image clearly satisfied the red-hat request; one red accessory was ambiguous. |

**Figures:** [`results/prompt_editing/`](../results/prompt_editing/).

**Interpretation:** Some scene and style edits were possible in these examples, while the tested attribute edit was less successful. No consistent overall advantage for either LR was established.

## 7. Experiment 06 — CLIP Image Similarity Evaluation

**Objective:** Provide an auxiliary quantitative comparison of generated images against the six reference images.

**Evaluation model:** `openai/clip-vit-base-patch32`.

**Method:** For each of the six images from Experiment 05, extract a CLIP image embedding and compute its mean cosine similarity against the six reference-image embeddings. Embeddings are normalized before similarity calculation. The images use the 3000-step checkpoints and Experiment 05 inference settings.

| Prompt | Effective LR = 0.0004 | Effective LR = 0.002 |
|---|---:|---:|
| Beach | 0.6882 | 0.7686 |
| Red hat | 0.7459 | 0.7422 |
| Watercolor | 0.7298 | 0.7045 |
| **Mean** | **0.7213** | **0.7384** |

**Observations:** The 0.002 embedding had a slightly higher three-prompt mean, mainly due to the beach result. The 0.0004 embedding scored higher on the other two prompts. These scores describe similarity in CLIP image-feature space, **not** prompt adherence, editability, or overall quality.

**Script:** [`scripts/evaluate_clip.py`](../scripts/evaluate_clip.py).

## 8. Overall Limitations

- Only two training runs were completed, without a controlled common training seed; LR is therefore confounded with training randomness.
- All comparisons used a single inference seed and a small number of prompts; results are exploratory rather than statistically established.
- The six checkpoints within each run are correlated snapshots, not independent replications.
- Some prompts are ambiguous; visual judgments are qualitative and may be subjective.
- CLIP image similarity measures feature-space proximity to reference images and cannot independently establish concept fidelity or prompt compliance.
- Safety-filtered black images are invalid for visual-quality comparison.
- The repository does not include pretrained model weights or learned embedding files; local paths in scripts need adaptation for other machines.

## 9. Preliminary Conclusion

The reproduction successfully trained a new token embedding for a specific cat toy using a frozen Stable Diffusion 1.5 model. Generated images exhibited recognizable features of the reference object, while prompt-based editing was uneven, particularly for the backpack and red-hat prompts.

Comparisons across two learning-rate settings and six checkpoints, together with CLIP image-similarity measurements, provide exploratory evidence about fidelity and editability in this setup. They do not establish a general learning-rate optimum or a causal effect of learning rate. Further controlled seeds, prompts, and complementary prompt-alignment metrics would be required for stronger conclusions.
