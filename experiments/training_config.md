# Training Configuration

## Base Model and Dataset

- Base model: `stable-diffusion-v1-5/stable-diffusion-v1-5`
- Dataset: `diffusers/cat_toy_example`
- Training images: 6
- Placeholder token: `<cat-toy>`
- Initializer token: `toy`
- Learnable property: `object`

## Common Training Settings

- Resolution: 512
- Batch size: 1
- Gradient accumulation steps: 4
- Maximum training steps: 3000
- Learning rate scheduler: constant
- Warmup steps: 0
- Gradient checkpointing: enabled
- Learning rate scaling: enabled (`--scale_lr`)

## Experiment A: Baseline

Configured learning rate: `5e-4`

Effective learning rate: `0.002`

```powershell
accelerate launch textual_inversion.py `
  --pretrained_model_name_or_path="stable-diffusion-v1-5/stable-diffusion-v1-5" `
  --train_data_dir="./cat" `
  --learnable_property="object" `
  --placeholder_token="<cat-toy>" `
  --initializer_token="toy" `
  --resolution=512 `
  --train_batch_size=1 `
  --gradient_accumulation_steps=4 `
  --max_train_steps=3000 `
  --learning_rate=5e-4 `
  --scale_lr `
  --lr_scheduler="constant" `
  --lr_warmup_steps=0 `
  --gradient_checkpointing `
  --output_dir="./textual_inversion_cat_3000"
```

## Experiment B: Lower Learning Rate

Configured learning rate: `1e-4`

Effective learning rate: `0.0004`

Same settings as Experiment A, except:

```powershell
--learning_rate=1e-4
--output_dir="./textual_inversion_cat_lr0001_3000"
```

## Notes

- Training used the Hugging Face Diffusers Textual Inversion example script.
- The effective learning rate accounts for `--scale_lr`.
- No common random seed was fixed for the two training runs.
- Generated images were evaluated separately using a fixed inference seed of 42.