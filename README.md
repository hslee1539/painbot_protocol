# painbot protocol module

## 분기

master

develop

## 구현 리스트

### 세팅

9600, 8, N, 1

|   인덱스  |   내용    |   예      |
|   --      |   --      |   --      |
|   0       |   STX     |   0x02    |
|   1       |   초음파모드| 0:Continuous 1: Pulse   |
|   2       |   초음파출력값|   0~3 |
|   3       |   저주파 모드 |   0:Continuos 1: Interval |
|   4       |   저주파출력값|   0~50    |
|   5       |   저주파펄스값|   0:500uS 1: 250uS (182Hz)    |
|   6       |   저주파전류값|   0~100   |

총 7바이트 데이터를 받음.

### 참고


