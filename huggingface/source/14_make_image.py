# uv pup install diffusers transformers accelerate torch
import torch
from diffusers import StableDiffusionPipeline

model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, dtype =torch.float32,
                                               safety_checker = None)
pipe = pipe.to("cuda")

prompt = "바다를 뛰어다니는 야생호랑이"
image = pipe(prompt).images[0]

image.save("image.png")