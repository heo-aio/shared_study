# window 경고메시지 지우기 (선택사항)
import os
import shutil
import traceback

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINK_WARING"] = "1"

# 이미지 분류
# uv pip install pillow torchvision
vision = pipeline(model = "google/vit-base-patch16-224")

def file_Upload(file, path):
    success = -1
    try:
        with open(path, "wb") as file_obj:
            shutil.copyfileobj(file, file_obj)
        success = 1
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    return success

def class_img(img_path):
    result = vision(img_path)
    print(result)
    if os.path.exists(img_path):
        os.remove(img_path)
    return result