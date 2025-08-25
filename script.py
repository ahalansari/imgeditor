import os
from PIL import Image
import torch
from diffusers import QwenImageEditPipeline

assert torch.backends.mps.is_available(), "MPS not available. Update macOS/Xcode/PyTorch."

device = "mps"

pipe = QwenImageEditPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit"  # <- no `variant=` here
)
# MPS prefers float16 for speed/memory
pipe.to(device)
pipe.to(dtype=torch.float16)

img = Image.open("input.jpg").convert("RGB")
prompt = "Replace background with a field of floweers."

out = pipe(
    image=img,
    prompt=prompt,
    guidance_scale=7.5,
    num_inference_steps=10,  # start low on MPS
    generator=torch.manual_seed(0),
).images[0]

out.save("out.jpg")
print("Saved:", os.path.abspath("out.jpg"))