## Q1) 어떤 task를 선택하셨나요?
> MNLI Task를 사용했습니다.


## Q2) 모델은 어떻게 설계하셨나요? 설계한 모델의 입력과 출력 형태가 어떻게 되나요?
> 1. 입력 데이터
    input_ids
      shape : (batch_size, max_len)
      예 : (64, 400)으로 하였고 이후 Fine-tuning 과정에서 max_len을 128로 수정.
    attention_mask
      shape : (batch_size, max_len) 
      예 : (64, 400)
> 3. 출력 데이터
    logits
     shape : (batch_size, num_labels) 
     예 : (64, 3)


## Q3) 어떤 pre-trained 모델을 활용하셨나요?
> BERT 모델을 사용했습니다
> 조금더 높은 성능과 fine-tuning이 용이하다고 검색후 판단하여 사용


## Q4) 실제로 pre-trained 모델을 fine-tuning했을 때 loss curve은 어떻게 그려지나요? 그리고 pre-train 하지 않은 Transformer를 학습했을 때와 어떤 차이가 있나요? 
> pre-trained 모델을 fine-tuning 한 경우 Loss가 낮고 Accuracy가 높으며, 학습 속도와 일반화 성능이 우수. 하지만 epoch이 더많아지면 과적합 발생 우려가 있습니다.
* fine-tuning 결과 그래프
![fine-tuning](https://github.com/user-attachments/assets/6a20c033-8d1a-4109-97bd-c645e78eef2b)

> pre-train 하지 않은 transformer를 학습했을때는 train loss가 매우 높은 값에서 시작하여 급격히 감소하는게 보이지만 validation loss는 비교적 느리게 감소하거나 일정 수준 정체가 일어납니다.
> 또한 학습 데이터의 패턴은 일부 학습되었지만 fine-tuning 없이 해당 데이터셋에 특화된 일반화 성능이 부족한게 보입니다.

- * pre-training만 학습 결과 그래프
![pre-training](https://github.com/user-attachments/assets/96c9e89c-8eca-464a-8f2b-af7a2edd3400)
-  
-  
- 이미지 첨부시 : ![이미지 설명](경로) / 예시: ![poster](./image.png)
