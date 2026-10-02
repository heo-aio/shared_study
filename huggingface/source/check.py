# uv pip install torch
import torch
print(f'window : {torch.cuda.is_available()}')
print(torch.__version__)

# CPU버전이 설치되어 있다면 GPU사용이 불가능하다.
# 기존 torch를 제거하고 다시 설치
# pip uninstall torch
# pip cache purge

# CUDA 지원 버전
# uv pip install torch --index-url https://download.pytorch.org/whl/cu126