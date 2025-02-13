
* LoRa Rank 8
   - train loss 그래프
   - https://api.wandb.ai/links/duhyeon/9h0mi2fv
 
   - 속도, 메모리
***** train metrics *****
  epoch                    =        3.0
  total_flos               = 10377654GF
  train_loss               =     1.5841
  train_runtime            = 0:08:09.32
  train_samples_per_second =     98.198
  train_steps_per_second   =      12.28
Max Alloc: 4.1 GB
  - 결과
    가장 빠른 학습 속도, 메모리 사용량 적음
    학습 성능이 떨어질 가능성이 큼

    
* LoRa Rank 128
  - train loss 그래프
 https://wandb.ai/duhyeon/Hanghae99-8_basic/reports/train-loss-25-02-13-15-52-52---VmlldzoxMTMzMzI3Mg?accessToken=zmp6bcn0bwfyd4mhjt5fg7vp50o27ppnc1ghq1jgj8snv2asu4435h9g4gk3kvyo
   - 속도, 메모리
***** train metrics *****
  epoch                    =        3.0
  total_flos               = 12171285GF
  train_loss               =     1.5762
  train_runtime            = 0:08:34.72
  train_samples_per_second =     93.353
  train_steps_per_second   =     11.674
Max Alloc: 4.8 GB
  - 결과
    적당한 성능과 속도
    성능과 속도를 동시에 고려할 때 적합할것 같음
    
* LoRa Rank 256

  - train loss 그래프
   https://wandb.ai/duhyeon/Hanghae99-8_basic/reports/train-loss-25-02-13-16-14-55---VmlldzoxMTMzMzYxMw?accessToken=gp6iyy1q6nckxdlyicjwmx1ug65d21dptsuq41kmijce7w8rjgdbr07ehuyefpvn
 - 속도, 메모리
   ***** train metrics *****
    epoch                    =        3.0
    total_flos               = 14113937GF
    train_loss               =     1.5685
    train_runtime            = 0:10:09.75
    train_samples_per_second =     78.804
    train_steps_per_second   =      9.855
    Max Alloc: 5.5 GB
   - 결과
     Loss가 가장 낮아 학습 성능이 좋음
     연산 자원이 충분해야함


최종 결과
Rank가 너무 낮으면 성능이 떨어짐, Rank 8처럼 너무 작으면 표현력이 부족하여 Loss가 높아질 가능성이 있음.
Rank를 높이면 Full Fine-Tuning과 큰 차이 없음, Rank 256에서는 연산량과 메모리 사용량이 급격히 증가해서 일반 Full Fine-Tuning과 비슷해질 수 있음
