import evaluate
import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, \
    DataCollatorWithPadding
from transformers.data import data_collator

# 1. 토크나이저 로드
model_id = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 토크나이저 함수 정의
def pre_proc(item):
    return tokenizer(item['text'], truncation = True, max_length = 512)

# 3. 평가함수 정의
accuracy_metric = evaluate.load("accuracy")

def compute_matrics(eval_pred):
    logits, labels = eval_pred
    predict = np.argmax(logits, axis=-1)
    return accuracy_metric.compute(predictions=predict, references=labels)

def main():
    # 1. 데이터 셋 로드
    dataset = load_dataset(
        "stanfordnlp/imdb",
         split={"train" : "train[:2000]", "test" : "test[:500]"}
    )

    # 2. 토크나이징
    print("토크나이징 진행중")
    token_ds = dataset.map(
        # lambda item : tokenizer(item['text'], truncation = True, max_length = 512)
        pre_proc,
        batched = True,
        num_proc = 4,
        remove_columns = ["text"]
    )
    # print(token_ds)

    # 3. 모델 생성
    model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels = 2)

    # 4. 학습 상세정보 지정 (하이퍼 파라미터)
    args = TrainingArguments(
        output_dir = "./results", # 결과와 체크포인트 저장 경로
        num_train_epochs = 2, # 전체 학습 수
        per_device_train_batch_size = 16,   # 학습 당 묶음 수
        per_device_eval_batch_size = 16,    # 평가 당 묶음 수
        learning_rate = 0.00002,            # 2e-5
        eval_strategy = "epoch",            # 평가 기준 - 학습당 (epoch)
        save_strategy = "epoch",            # 저장 시점 - 학습당 (epoch)
        load_best_model_at_end = True,      # 평가가 끝난 시점에서 가장 우수한 모델을 로드
        metric_for_best_model = "accuracy", # 정확도가 높으면 좋은 모델이라고 판단
        logging_steps = 100,                # 100번의 step마다 로그 출력하기
        report_to = "none",                 # 외부 로깅툴 사용 여부
        dataloader_num_workers = 4,          # 데이터 로딩 시 사용할 스레드 수
        ### GPU 메모리 최적화 옵션 ###
        # 1. Gradient Checkpoint
        gradient_checkpointing = True,

        # 2. Mixed precision 설정(GPU 사양에 맞춰서 설정)
        fp16 = True, # T4, V100 등 이전세데 GPU
        # bf16 = True, # A100, RTX3000/4000 시리즈 이상 GPU

        # 3. compile을 이용한 최적화
        torch_compile = True,

        # 4. Gradient Exploding 방지를 위한 cliping
        max_grad_norm = 1.0,

        # 5. Gradient Accumulation으로 큰 배치효과 구현
        gradient_accumulation_steps = 16 # 16번 모아서 한 방에 처리하겠다
    )

    # 5. Trainer API 생성
    trainer = Trainer(
        model = model,
        args = args,
        train_dataset = token_ds['train'],
        eval_dataset = token_ds['test'],
        processing_class = tokenizer,
        data_collator = DataCollatorWithPadding(tokenizer = tokenizer), # 토크나이징 후 패딩설정
        compute_metrics = compute_matrics, # 평가지표함수 지정
    )

    # 6. 학습
    print("모델 학습 ing ...")
    trainer.train()

    # 7. 평가
    eval_result = trainer.evaluate()
    print(f"평가 지표 : {eval_result}")

    # 8. 저장
    save_path = './fine_tuned_model'
    trainer.save_model(save_path)
    tokenizer.save_pretrained(save_path)
    print("모델 저장 완료")

# 메인 프로세서 (스레드)만 진입해서 실행해라
if __name__ == "__main__":
    main()