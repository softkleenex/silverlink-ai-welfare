# 🎬 나레이션 생성 스크립트

SilverLink 데모 영상용 나레이션을 ElevenLabs API로 자동 생성합니다.

---

## 📋 사전 준비

### 1. Python 패키지 설치
```bash
pip install requests python-dotenv
```

### 2. ElevenLabs API 키 설정
`.env` 파일에 API 키가 이미 설정되어 있습니다.
```bash
ELEVENLABS_API_KEY=sk_89fa...
```

### 3. Voice ID 확인

**중요**: Voice Library에서 한국어 목소리를 선택하고 Voice ID를 복사해야 합니다.

#### Voice ID 찾는 방법:

1. **Voice Library 접속**
   - https://elevenlabs.io/app/voice-library

2. **Language 필터 적용**
   - 왼쪽 필터에서 "Language" → "Korean" 선택

3. **목소리 선택**
   - 나레이션용: 중년 남성 또는 여성 (차분한 톤)
   - 할머니용: "Old Female" 태그
   - 할아버지용: "Old Male" 태그

4. **Voice ID 복사**
   - 목소리 카드 클릭
   - "Add to My Voices" 또는 직접 사용
   - Voice ID는 URL 또는 목소리 정보에서 확인
   - 예: `21m00Tcm4TlvDq8ikWAM`

**또는 직접 URL에서 확인**:
```
https://elevenlabs.io/app/voice-library
→ 목소리 클릭
→ URL에서 voice_id 확인
```

---

## 🚀 사용법

### 기본 사용 (나레이션만)

```bash
python scripts/generate_narration.py --voice-id YOUR_VOICE_ID
```

예시:
```bash
python scripts/generate_narration.py --voice-id 21m00Tcm4TlvDq8ikWAM
```

### 캐릭터 음성 포함 (할머니/할아버지)

```bash
python scripts/generate_narration.py \
  --voice-id 21m00Tcm4TlvDq8ikWAM \
  --grandma-voice-id GRANDMA_VOICE_ID \
  --grandpa-voice-id GRANDPA_VOICE_ID
```

### 설정값 조정

```bash
python scripts/generate_narration.py \
  --voice-id YOUR_VOICE_ID \
  --stability 0.6 \
  --similarity 0.7 \
  --output-dir my_narration
```

---

## 📂 출력 파일

실행 후 `narration/` 폴더에 다음 파일들이 생성됩니다:

```
narration/
├── 01_intro.mp3                    # 인트로 (30초)
├── 02_service.mp3                  # 서비스 소개 (30초)
├── 03_scenario1_intro.mp3          # 시나리오1 설명
├── 04_scenario1_result.mp3         # 시나리오1 결과
├── 05_scenario2_intro.mp3          # 시나리오2 설명
├── 06_scenario2_result.mp3         # 시나리오2 결과
├── 07_scenario3_intro.mp3          # 시나리오3 설명
├── 08_scenario3_result.mp3         # 시나리오3 결과
├── 09_tech_stack.mp3               # 기술 스택 소개
├── 10_differentiation.mp3          # 차별화 포인트
├── 11_outro.mp3                    # 아웃트로
├── character_grandma.mp3           # 할머니 음성 (선택)
└── character_grandpa.mp3           # 할아버지 음성 (선택)
```

---

## ⚙️ 파라미터 설명

### 필수 파라미터

- `--voice-id`: ElevenLabs Voice ID (나레이션용)

### 선택 파라미터

- `--grandma-voice-id`: 할머니 목소리 Voice ID
- `--grandpa-voice-id`: 할아버지 목소리 Voice ID
- `--output-dir`: 출력 디렉토리 (기본: `narration`)
- `--stability`: 안정성 0.0-1.0 (기본: 0.5)
  - 높음 = 발음 안정, 감정 단조
  - 낮음 = 감정 풍부, 발음 불안정
- `--similarity`: 유사성 0.0-1.0 (기본: 0.6)
  - 높음 = 원본 유사, 억양 단조
  - 낮음 = 변형 많음, 다양성

---

## 🎯 사용 예시

### 예시 1: 빠른 테스트
```bash
# 하나의 목소리로 나레이션만 생성
python scripts/generate_narration.py --voice-id 21m00Tcm4TlvDq8ikWAM
```

### 예시 2: 완전한 세트
```bash
# 나레이션 + 할머니 + 할아버지 모두 생성
python scripts/generate_narration.py \
  --voice-id 21m00Tcm4TlvDq8ikWAM \
  --grandma-voice-id ABC123DEF456 \
  --grandpa-voice-id XYZ789GHI012
```

### 예시 3: 설정 조정
```bash
# 더 안정적인 발음 원할 때
python scripts/generate_narration.py \
  --voice-id 21m00Tcm4TlvDq8ikWAM \
  --stability 0.7 \
  --similarity 0.7
```

---

## 🔧 트러블슈팅

### 에러: "ELEVENLABS_API_KEY가 설정되지 않았습니다"
```bash
# .env 파일 확인
cat .env

# 없으면 추가
echo "ELEVENLABS_API_KEY=your_key" >> .env
```

### 에러: 401 Unauthorized
- API 키가 잘못됨
- ElevenLabs 계정에서 API 키 재확인

### 에러: 429 Too Many Requests
- 무료 플랜 크레딧 초과 (10,000자/월)
- 다음 달까지 대기 또는 유료 플랜 업그레이드

### 발음이 이상함
1. Voice Library에서 "Korean" 필터 적용했는지 확인
2. Model이 "Eleven Multilingual v2"인지 확인
3. Stability 값을 50-60%로 조정
4. 다른 한국어 목소리로 테스트

---

## 💡 Pro Tips

### Tip 1: 목소리 미리 테스트
```bash
# Voice Library에서 샘플 텍스트로 먼저 테스트
"어르신들의 복지 혜택 미신청률이 30%에 달합니다."
```

### Tip 2: 섹션별 재생성
```python
# generate_narration.py 수정
# 특정 섹션만 생성하려면 NARRATIONS 딕셔너리에서 선택
```

### Tip 3: 크레딧 확인
- https://elevenlabs.io/app/usage
- 무료 플랜: 10,000자/월
- 우리 스크립트: ~3,000자

---

## 📋 다음 단계

1. **생성된 파일 확인**
   ```bash
   ls -lh narration/
   ```

2. **품질 확인**
   ```bash
   # Mac
   open narration/01_intro.mp3

   # Linux
   vlc narration/01_intro.mp3
   ```

3. **영상 편집**
   - iMovie, DaVinci Resolve, Kapwing 등에서 import
   - VIDEO_SCRIPT.md의 타임라인에 맞춰 배치

4. **BGM 추가**
   - 나레이션: -3dB ~ 0dB
   - BGM: -18dB ~ -12dB

---

**작성자**: Claude Code
**관련 문서**: `docs/guides/ELEVENLABS_KOREAN_GUIDE.md`
