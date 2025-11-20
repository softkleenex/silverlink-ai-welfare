# 📁 SilverLink 프로젝트 구조

**작성일**: 2025-11-20
**목적**: 프로젝트 파일/폴더 구조 정리 및 설명

---

## 🌳 전체 구조

```
ai-conic/
├── 📄 app.py                      # Streamlit 메인 애플리케이션
├── 📄 welfare_data.json           # 복지 혜택 데이터 (20개)
├── 📄 requirements.txt            # Python 패키지 의존성
├── 📄 README.md                   # 프로젝트 메인 문서
├── 📄 CLAUDE.md                   # Claude Code 가이드
├── 📄 STRUCTURE.md                # 이 파일 (프로젝트 구조)
├── 📄 TIMELINE_FINAL.md           # 영상 제작 타임라인
├── 🎬 aiconic_demo_final.mp4      # 완성된 데모 영상
│
├── 🎙️ audio/                      # 오디오 파일 (영상 제작용)
│   ├── final_audio/               # ⭐ 최종 나레이션 (14개, 영상에 사용)
│   │   ├── 01_intro.mp3
│   │   ├── 02_service.mp3
│   │   ├── 03~08_scenario*.mp3   # 시나리오 1~3 (인트로/캐릭터/결과)
│   │   ├── 09_tech_stack.mp3
│   │   ├── 10_differentiation.mp3
│   │   └── 11_outro.mp3
│   ├── narration/                 # 이전 나레이션 (백업)
│   │   ├── female/                # 여자 나이든 목소리
│   │   └── male/                  # 남자 나이든 목소리
│   └── characters/                # 캐릭터 음성 (시연용)
│
├── 📊 slides/                     # HTML 프레젠테이션 슬라이드
│   ├── 01_tech_stack.html         # 기술 스택 슬라이드
│   ├── 02_differentiation.html    # 차별화 포인트 슬라이드
│   ├── 03_outro.html              # 아웃트로 (QR코드 포함)
│   ├── logo.svg                   # SilverLink 로고 (SVG)
│   ├── logo.png                   # 로고 (PNG)
│   ├── logo_centered.png          # 로고 (중앙 배치)
│   └── qr_code.png                # 앱 QR 코드
│
├── 📚 docs/                       # 문서 모음
│   ├── guides/                    # 가이드 문서
│   │   ├── VIDEO_GUIDE.md         # 영상 제작 완벽 가이드 ⭐
│   │   ├── FILMING_GUIDE.md       # iPhone 미러링 촬영 가이드
│   │   ├── AUDIO_GUIDE.md         # 오디오 파일 정리
│   │   ├── ELEVENLABS_GUIDE.md    # ElevenLabs TTS 사용법
│   │   ├── DEPLOYMENT.md          # Streamlit Cloud 배포 가이드
│   │   └── FINAL_CHECKLIST.md     # 해커톤 제출 전 체크리스트
│   │
│   ├── hackathon/                 # 해커톤 제출 자료
│   │   ├── silverlink_logo_*.svg  # 로고 파일 (가로/아이콘)
│   │   └── *.pdf                  # 신청서, 기획서, 계획안
│   │
│   ├── strategy/                  # 전략 문서
│   │   ├── WINNING_STRATEGY.md    # 수상 전략
│   │   ├── HACKATHON_ANALYSIS.md  # 해커톤 분석
│   │   ├── HARSH_EVALUATION.md    # 냉정한 평가
│   │   └── ACTION_PLAN.md         # 실행 계획
│   │
│   ├── development/               # 개발 관련 문서
│   │   ├── PROJECT_STATUS.md      # 프로젝트 상태
│   │   ├── NEXT_STEPS.md          # 다음 단계
│   │   ├── AI_IMPROVEMENTS.md     # AI 개선사항
│   │   └── SESSION_REPORT_*.md    # 세션 리포트
│   │
│   └── NOTION_IMPORT.md           # Notion import용 통합 문서
│
└── 🔧 scripts/                    # 스크립트 모음
    ├── generate_narration.py      # 나레이션 생성 (ElevenLabs)
    ├── age_voice.py               # 음성 후처리 (사용 안 함)
    └── README.md                  # 스크립트 설명
```

---

## 📂 폴더별 설명

### 🎙️ audio/
**목적**: 데모 영상 제작용 오디오 파일

- `final_audio/` - ⭐ **최종 나레이션 (14개 파일, 영상에 사용)**
  - ElevenLabs로 생성된 고품질 한국어 나레이션
  - 시나리오 순서가 앱 탭 순서와 일치하도록 조정됨
  - 숫자 표현 제거하여 AI 출력과 유연하게 대응
- `narration/` - 이전 나레이션 (백업용)
  - `female/` - 여자 목소리 버전
  - `male/` - 남자 목소리 버전
- `characters/` - 캐릭터 음성 (시연용)

**자세한 설명**: `audio/README.md`

---

### 📊 slides/
**목적**: 영상에 사용되는 HTML 프레젠테이션 슬라이드

- `01_tech_stack.html` - 기술 스택 소개 슬라이드
- `02_differentiation.html` - 차별화 포인트 슬라이드
- `03_outro.html` - 아웃트로 (QR코드, GitHub 링크 포함)
- `logo.svg` - SilverLink 로고 (SVG, 고품질)
- `logo.png` - 로고 PNG 버전
- `logo_centered.png` - 로고 중앙 배치 버전
- `qr_code.png` - 앱 배포 URL QR 코드

**특징**:
- 반응형 디자인 (viewport 단위 사용)
- 통일된 브랜드 컬러 (파란색 그라데이션)
- HTML 슬라이드가 logo.svg, qr_code.png를 참조 (파일 이동 금지!)

**자세한 설명**: `slides/README.md`

---

### 📚 docs/guides/
**목적**: 프로젝트 가이드 문서

#### 영상 제작 가이드 (우선순위 높음)
| 파일 | 설명 |
|------|------|
| `VIDEO_GUIDE.md` | ⭐ 영상 제작 완벽 가이드 (All-in-One) |
| `FILMING_GUIDE.md` | iPhone 미러링 촬영 가이드 |
| `AUDIO_GUIDE.md` | 오디오 파일 내용 정리 |

#### 기술 가이드
| 파일 | 설명 |
|------|------|
| `ELEVENLABS_GUIDE.md` | ElevenLabs TTS 한국어 사용법 |
| `DEPLOYMENT.md` | Streamlit Cloud 배포 가이드 |
| `FINAL_CHECKLIST.md` | 해커톤 제출 전 최종 체크리스트 |

---

### 📚 docs/hackathon/
**목적**: 해커톤 제출 자료

- `silverlink_logo_horizontal.svg` - 로고 (가로형)
- `silverlink_logo_icon.svg` - 로고 (아이콘)
- `아이디어기획서.pdf` - 제출한 기획서
- `참가신청서.pdf` - 참가 신청서
- `개인정보동의서.pdf` - 개인정보 동의서
- `2025 해커톤 실시계획안(외부공개용).pdf` - 해커톤 계획안

---

### 📚 docs/strategy/
**목적**: 해커톤 전략 및 분석 문서

| 파일 | 설명 |
|------|------|
| `WINNING_STRATEGY.md` | 수상을 위한 전략 분석 |
| `HACKATHON_ANALYSIS.md` | 해커톤 요구사항 분석 |
| `HARSH_EVALUATION.md` | 현재 서비스 냉정한 평가 |
| `ACTION_PLAN.md` | D-3 실행 계획 |

---

### 📚 docs/development/
**목적**: 개발 관련 문서

| 파일 | 설명 |
|------|------|
| `PROJECT_STATUS.md` | 현재 프로젝트 상태 |
| `NEXT_STEPS.md` | 다음에 해야 할 작업 |
| `AI_IMPROVEMENTS.md` | AI 기능 개선 아이디어 |
| `SESSION_REPORT_*.md` | 작업 세션 리포트 |

---

### 🔧 scripts/
**목적**: 자동화 스크립트

| 파일 | 설명 | 사용 여부 |
|------|------|-----------|
| `generate_narration.py` | ElevenLabs로 나레이션 생성 | ✅ 사용 |
| `age_voice.py` | 음성 후처리 (pitch/tempo) | ❌ 사용 안 함 |
| `README.md` | 스크립트 사용법 | - |

---

## 🎯 핵심 파일 Quick Reference

### 개발/실행
```bash
app.py                        # 메인 애플리케이션 실행
welfare_data.json             # 복지 혜택 데이터
requirements.txt              # 패키지 설치
```

### 영상 제작
```bash
aiconic_demo_final.mp4        # ✅ 완성된 데모 영상
TIMELINE_FINAL.md             # 영상 타임라인
docs/guides/VIDEO_GUIDE.md    # ⭐ 영상 제작 가이드
docs/guides/FILMING_GUIDE.md  # iPhone 촬영 방법
docs/guides/AUDIO_GUIDE.md    # 사용할 음성 파일 정리
audio/final_audio/            # 최종 나레이션 (14개)
audio/characters/             # 시연용 음성
slides/                       # HTML 슬라이드 (3개)
```

### 해커톤 제출
```bash
docs/guides/FINAL_CHECKLIST.md   # 제출 전 체크리스트
docs/hackathon/                   # 제출 자료
README.md                         # 프로젝트 설명 (GitHub)
```

---

## 📋 변경 이력

### 2025-11-20 (저녁): 영상 제작 완료 및 최종 정리
- ✅ **데모 영상 제작 완료**: `aiconic_demo_final.mp4`
- ✅ **HTML 슬라이드 추가**: `slides/` 폴더 생성 (3개 슬라이드)
- ✅ **최종 나레이션 확정**: `audio/male 복사본/` (14개 파일)
- ✅ **YouTube 링크 준비**: README에 섹션 추가
- ✅ **프로젝트 구조 문서화**: README, STRUCTURE 최신 상태 반영

**새로 추가된 파일**:
- `aiconic_demo_final.mp4` - 완성된 데모 영상
- `slides/01_tech_stack.html` - 기술 스택 슬라이드
- `slides/02_differentiation.html` - 차별화 슬라이드
- `slides/03_outro.html` - 아웃트로 슬라이드
- `slides/logo.svg` - 로고 SVG
- `slides/qr_code.png` - QR 코드

### 2025-11-20 (오전): 대규모 재구조화
- ✅ 오디오 파일 재정리: `audio/narration/`, `audio/characters/`
- ✅ 중복 문서 삭제: 5개 가이드 파일 제거
- ✅ 파일명 간소화: `*_IPHONE`, `*_KOREAN` 등 제거
- ✅ 폴더 구조 단순화: 3레벨 → 2레벨

**삭제된 파일**:
- `docs/guides/DEPLOYMENT_GUIDE.md` (중복)
- `docs/guides/PPT_GUIDE.md` (iPhone으로 변경)
- `docs/guides/VIDEO_PRODUCTION_QUICK.md` (VIDEO_GUIDE로 통합)
- `docs/guides/VIDEO_SCRIPT.md` (사용 안 함)
- `docs/guides/AUDIO_FILES_USAGE.md` (AUDIO_GUIDE로 통합)
- `audio_samples/` (테스트용)
- `character_voices/` (audio/로 이동)
- `narration_old_female/` (audio/narration/female/로 이동)
- `narration_old_male/` (audio/narration/male/로 이동)

---

## 🔍 파일 찾기

### 특정 기능 찾기
```bash
# 복지 혜택 데이터
welfare_data.json

# AI 프롬프트
app.py (line ~100-200)

# 음성 생성
scripts/generate_narration.py

# 배포 설정
.streamlit/config.toml
```

### 문서 찾기
```bash
# 영상 제작 방법
docs/guides/VIDEO_GUIDE.md

# 촬영 방법
docs/guides/FILMING_GUIDE.md

# 배포 방법
docs/guides/DEPLOYMENT.md
```

---

**작성자**: Claude Code
**마지막 업데이트**: 2025-11-20 (저녁)

**다음 작업**:
1. ✅ 영상 제작 완료 (`aiconic_demo_final.mp4`)
2. 🎬 YouTube 업로드 및 README 링크 추가
3. 📝 해커톤 제출 준비 (`docs/guides/FINAL_CHECKLIST.md` 참고)
