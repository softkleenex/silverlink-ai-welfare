# 🎙️ ElevenLabs 한국어 나레이션 최적화 가이드

**작성일**: 2025-11-20
**목적**: SilverLink 데모 영상용 고품질 한국어 나레이션 생성

---

## 📋 요금제 선택

### 무료 플랜 (추천!)
```
크레딧: 월 10,000자 (약 10분 분량)
우리 스크립트: ~3,000자 → 충분!
상업적 이용: 불가 (해커톤은 OK)
제한: 보이스 클로닝 일부 제한
```

### 유료 플랜 (필요시)
```
Starter: $5/월 (30,000자 - 30분)
Creator: $22/월 (100,000자 - 2시간)
→ 무료로 충분하면 업그레이드 불필요
```

**결론**: 무료 플랜으로 시작! 부족하면 Starter($5) 고려

---

## 🎯 한국어 최적화 3단계

### 1단계: 한국어 PVC 선택 (가장 중요!)

**방법**:
1. ElevenLabs 로그인
2. **Voice Library** 클릭
3. **Language 필터** → **Korean (한국어)** 선택
4. 목소리 미리듣기 (Preview)
5. 영상 톤에 맞는 목소리 선택

**추천 목소리 타입**:
- 나레이션: 중년 남성/여성 (차분하고 명확한 목소리)
- 할머니: "Old Female" 또는 나이든 여성 목소리
- 할아버지: "Old Male" 또는 나이든 남성 목소리

**팁**:
- 한국어 PVC 리스트: https://elevenlabs.io/app/voice-library?sort=usage_character_count_1y&required_languages=ko
- Usage Count가 높은 목소리 = 검증된 품질

---

### 2단계: 모델 선택

**Speech Synthesis 화면에서**:
```
Model: Eleven Multilingual v2 (필수!)
```

**절대 하지 말아야 할 것**:
```
❌ Eleven English v1 → 한국어 발음 엉망
❌ Eleven Turbo v2 (영어 전용) → 지원 안 됨
```

**모델 설명**:
- **Eleven Multilingual v2**: 29개 언어 지원, 고품질, 감정 풍부
- **Eleven v3 (alpha)**: 70개 언어, 더 풍부하지만 불안정 (비추천)

---

### 3단계: 설정값(Settings) 조절

**기본 설정 (권장)**:
```
Stability: 50%
Similarity: 60%
Style Exaggeration: 0% (기본)
```

**설정값 의미**:
- **Stability (안정성)**:
  - 높음 (70-80%) = 발음 안정, 감정 단조
  - 낮음 (30-40%) = 감정 풍부, 발음 불안정
  - **권장: 40-60%** (균형)

- **Similarity (유사성)**:
  - 높음 (70-80%) = 원본 목소리와 유사, 억양 단조
  - 낮음 (40-50%) = 변형 많음, 다양성 증가
  - **권장: 50-70%**

- **Style Exaggeration (스타일 과장)**:
  - 높음 (30-50%) = 목소리 특색 강조
  - 낮음 (0-10%) = 자연스러움
  - **권장: 0-20%** (나레이션은 자연스럽게)

---

## 🎭 목소리별 추천 설정

### 나레이션 (설명하는 목소리)
```yaml
Voice Type: 중년 남성 또는 여성 (차분한 톤)
Model: Eleven Multilingual v2
Settings:
  Stability: 60% (안정적으로)
  Similarity: 60% (명확하게)
  Style: 0% (자연스럽게)
```

### 할머니 (72세 독거 할머니)
```yaml
Voice Type: Old Female (나이든 여성)
Model: Eleven Multilingual v2
Settings:
  Stability: 50% (약간 떨리는 목소리)
  Similarity: 50% (자연스럽게)
  Style: 10% (나이든 특색 살짝)
```

### 할아버지 (68세 저소득 할아버지)
```yaml
Voice Type: Old Male (나이든 남성)
Model: Eleven Multilingual v2
Settings:
  Stability: 50%
  Similarity: 50%
  Style: 10%
```

---

## ⚠️ 자주 하는 실수

### 실수 1: 영어 모델로 한국어 생성
```
❌ Eleven English v1 선택
❌ 한국어 입력
→ 결과: 외국인 억양, 발음 이상함
```
**해결**: Eleven Multilingual v2 선택!

### 실수 2: 한국어 PVC 미사용
```
❌ Voice Library에서 영어 목소리 선택
❌ 한국어 텍스트 입력
→ 결과: 영어 억양으로 한국어 읽음
```
**해결**: Language 필터 Korean으로!

### 실수 3: Stability 너무 낮게
```
❌ Stability: 20%
→ 결과: 발음 뭉개짐, "ㄱ", "ㄷ" 발음 부정확
```
**해결**: 최소 40% 이상 유지

---

## 🚀 실전 사용 순서

### Step 1: Voice Library에서 한국어 목소리 찾기
1. https://elevenlabs.io/app/voice-library 접속
2. Language: Korean 필터
3. 목소리 미리듣기
4. "Add to My Voices" 클릭 (또는 직접 사용)

### Step 2: Speech Synthesis에서 생성
1. https://elevenlabs.io/app/speech-synthesis 접속
2. Voice: 선택한 한국어 목소리
3. Model: **Eleven Multilingual v2**
4. Settings: Stability 50%, Similarity 60%
5. 텍스트 입력
6. "Generate" 클릭

### Step 3: 다운로드
1. 생성 완료 후 재생 확인
2. 만족하면 Download 클릭 (MP3)
3. 파일명: `01_intro.mp3`, `02_grandma.mp3` 등으로 정리

---

## 💡 Pro Tips

### Tip 1: 문장 단위로 나누기
```
❌ 전체 스크립트 한 번에 입력
   → 너무 길면 억양 불안정

✅ 섹션별로 나누어 생성
   → 인트로, 시나리오1, 시나리오2 각각 생성
   → 나중에 영상 편집에서 결합
```

### Tip 2: 쉼표와 마침표 활용
```
✅ "어르신들의 복지 혜택 미신청률이 30%에 달합니다."
   (마침표로 명확한 끊김)

✅ "첫째, 텍스트로 입력하거나"
   (쉼표로 자연스러운 호흡)
```

### Tip 3: 숫자 표기
```
❌ "72세" → "칠이세"로 읽을 수 있음
✅ "72살" → "일흔두살"로 읽음
✅ "72세 (일흔두 세)" → 괄호로 명시
```

### Tip 4: 테스트 먼저
```
1. 짧은 문장 1개로 먼저 테스트
   예: "어르신들의 복지 혜택 미신청률이 30%에 달합니다."
2. 발음 확인
3. 설정 조정
4. 전체 생성
```

---

## 📊 크레딧 계산

**우리 스크립트 예상 크레딧**:
```
인트로: ~300자
서비스 소개: ~400자
시나리오 1: ~500자
시나리오 2: ~500자
시나리오 3: ~500자
기술 스택: ~400자
아웃트로: ~200자
-------------------
합계: ~2,800자

무료 플랜: 10,000자
→ 3배 여유 (재생성 여유 충분!)
```

---

## ✅ 최종 체크리스트

**생성 전**:
- [ ] Language 필터: Korean 확인
- [ ] Model: Eleven Multilingual v2 확인
- [ ] Settings: Stability 40-60%, Similarity 50-70%
- [ ] 짧은 테스트 문장으로 발음 확인

**생성 중**:
- [ ] 섹션별로 나누어 생성 (인트로, 시나리오1, 시나리오2...)
- [ ] 각 파일 재생하여 품질 확인
- [ ] 이상하면 설정 조정 후 재생성

**생성 후**:
- [ ] 파일명 정리 (01_intro.mp3, 02_service.mp3...)
- [ ] 영상 편집 툴에서 타임라인에 배치
- [ ] 볼륨 레벨 조정 (너무 크거나 작지 않게)

---

## 🎬 영상 편집 팁

**나레이션 + BGM 볼륨 밸런스**:
```
나레이션: -3dB ~ 0dB (명확하게)
BGM: -18dB ~ -12dB (배경으로 조용히)
```

**페이드 인/아웃**:
```
각 섹션 시작: 0.5초 페이드 인
각 섹션 끝: 0.5초 페이드 아웃
→ 매끄러운 전환
```

---

**작성자**: Claude Code
**다음 단계**: ElevenLabs 가입 완료 → Voice Library에서 한국어 목소리 선택 → 테스트 생성

**화이팅!** 🎙️
