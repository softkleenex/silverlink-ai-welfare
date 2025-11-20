# 🎙️ Audio Files

**작성일**: 2025-11-20
**목적**: 데모 영상용 오디오 파일 정리

---

## 📂 폴더 구조

```
audio/
├── narration/           # 나레이션 (영상 설명 음성)
│   ├── female/          # 여자 나이든 목소리 (11개 파일)
│   └── male/            # 남자 나이든 목소리 (11개 파일)
└── characters/          # 모의 사용자 음성 (시연용, 3개 파일)
```

---

## 📢 나레이션 파일 (narration/)

### 용도
영상 전체를 설명하는 내레이터 목소리

### 버전
- **female/** - 여자 나이든 목소리 (친근함) ⭐ 추천
- **male/** - 남자 나이든 목소리 (신뢰감)

### 파일 목록 (11개)

| 파일 | 길이 | 내용 | 영상 시점 |
|------|------|------|-----------|
| 01_intro.mp3 | 30초 | 문제 제기 + SilverLink 소개 | 00:00-00:30 |
| 02_service.mp3 | 30초 | 3가지 입력 방식 설명 | 00:30-01:00 |
| 03_scenario1_intro.mp3 | 10초 | 독거 할머니 도입 | 01:00-01:10 |
| 04_scenario1_result.mp3 | 40초 | 시나리오1 결과 설명 | 01:10-01:50 |
| 05_scenario2_intro.mp3 | 10초 | 저소득 할아버지 도입 | 01:50-02:00 |
| 06_scenario2_result.mp3 | 40초 | 시나리오2 결과 + 다운로드 | 02:00-02:40 |
| 07_scenario3_intro.mp3 | 10초 | 건강 문제 도입 | 02:40-02:50 |
| 08_scenario3_result.mp3 | 40초 | 시나리오3 결과 + 모바일 | 02:50-03:30 |
| 09_tech_stack.mp3 | 20초 | 기술 스택 설명 | 03:30-03:50 |
| 10_differentiation.mp3 | 20초 | 차별화 포인트 | 03:50-04:10 |
| 11_outro.mp3 | 20초 | 마무리 CTA | 04:10-04:30 |

---

## 👥 모의 사용자 음성 (characters/)

### 용도
실제 어르신이 앱을 사용하는 것처럼 시연할 때 사용

### 파일 목록 (3개)

| 파일 | 길이 | 내용 | 시나리오 |
|------|------|------|----------|
| character_grandma.mp3 | 6초 | "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다." | 시나리오1 (실시간 녹음) |
| character_grandpa.mp3 | 4초 | "68살이고 소득이 적어서 힘들고 일자리를 찾고 싶어요." | 시나리오2 (텍스트 입력) - 타이핑 참고용 |
| character_senior.mp3 | 3초 | "70살인데 치아가 안 좋고 건강검진을 받고 싶어요." | 시나리오3 (음성 파일 업로드) |

---

## 🎬 영상 편집 시 사용법

### 1. 나레이션 선택
```
추천: audio/narration/female/ 사용
이유: 어르신들에게 더 친근함
```

### 2. 타임라인 배치 (4분 영상)
```
00:00-00:30  01_intro.mp3
00:30-01:00  02_service.mp3
01:00-01:10  03_scenario1_intro.mp3
01:10-01:50  04_scenario1_result.mp3
01:50-02:00  05_scenario2_intro.mp3
02:00-02:40  06_scenario2_result.mp3
02:40-02:50  07_scenario3_intro.mp3
02:50-03:30  08_scenario3_result.mp3
03:30-03:50  09_tech_stack.mp3
03:50-04:10  10_differentiation.mp3
04:10-04:30  11_outro.mp3
```

### 3. 모의 음성 사용
```
시나리오 1: character_grandma.mp3를 Mac 스피커로 재생 → iPhone 녹음
시나리오 2: character_grandpa.mp3 내용을 타이핑
시나리오 3: character_senior.mp3를 iPhone에 업로드
```

---

## 📋 생성 정보

- **생성 도구**: ElevenLabs TTS API
- **모델**: eleven_multilingual_v2 (한국어 지원)
- **음성 ID**:
  - 남자 나이든 목소리: `6sFKzaJr574YWVu4UuJF`
  - 여자 나이든 목소리: `fNmw8sukfGuvWVOp33Ge`
- **생성 스크립트**: `scripts/generate_narration.py`

---

**관련 문서**: `docs/guides/VIDEO_GUIDE.md`
