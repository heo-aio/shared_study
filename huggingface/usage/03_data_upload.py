from datasets import load_dataset

# split = 'train[:200]' : train의 0 ~199까지
dataset = load_dataset("cornell-movie-review-data/rotten_tomatoes", split = "train[:200]")

# label, text
# 1. label = 1, 0 -> positive, negative
def add_label_text(item):
    if item['label'] == 1:
        item['label_text'] = 'positive'
    else:
        item['label_text'] = 'negative'

    # return lambda item : "positive" if item['label'] == 1 else "negative"

    return item

ds = dataset.map(add_label_text)

# 2. text -> review 컬럼명 변경
ds = ds.rename_column("text", "review")

# 3. 10자 미만의 리뷰는 거름
ds = ds.filter(
    lambda item : len(item['review']) >= 10
)

print(f"ds col : {ds.column_names}")
print(f"data : {ds[0]}")

# HF에 업로드
REPO_ID = "HeoJungMo/hf_study_upload_test"
ds.push_to_hub(REPO_ID, split = "train")
print(f"업로드 완료 https://huggingface.co/datasets/{REPO_ID}")

# DOWNLOAD
# dataset = load_dataset(REPO_ID, split = "train")