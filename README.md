# 🎙️ SilverLink - AI 복지 도우미

> 어르신을 위한 AI 음성 기반 복지 정보 제공 서비스

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.51.0-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Pro-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Live-success.svg)

## 🌐 라이브 데모

**배포 URL**: https://silverlink-ai-welfare-6kn44w2jypeuce5d9zrsfg.streamlit.app

**지금 바로 체험해보세요!** (모바일 지원 ✅)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://silverlink-ai-welfare-6kn44w2jypeuce5d9zrsfg.streamlit.app)

---

## 📋 프로젝트 소개

**SilverLink**는 디지털 소외 어르신들이 받을 수 있는 복지 혜택을 쉽게 찾고 신청할 수 있도록 돕는 AI 음성 서비스입니다.

### 해결하고자 하는 문제
- 복지 혜택 미신청률 약 30% (매년 수조원의 복지 예산 미집행)
- 복잡한 온라인 신청 절차
- 어르신들의 디지털 기기 사용 어려움
- 본인이 받을 수 있는 혜택을 모름

### 핵심 기능
1. 📝 **텍스트 입력**: 키보드로 상황 입력 (가장 간단)
2. 🎙️ **실시간 녹음**: 버튼 클릭으로 바로 녹음 (가장 편리!)
3. 📁 **음성 파일 업로드**: 미리 녹음한 파일 업로드
4. 🤖 **AI 분석**: Google Gemini AI가 상황을 파악하고 적합한 복지 혜택 추천
5. 🔊 **음성 출력**: 추천 결과를 음성으로 친절하게 안내
6. 📥 **결과 다운로드**: 텍스트/음성 파일로 저장 가능

## 🔧 기술 스택

- **Frontend/Backend**: Streamlit (Python 웹 프레임워크)
- **AI**: Google Gemini 2.5 Pro (STT + 복지 매칭 통합!)
- **TTS**: Google Text-to-Speech (gTTS)
- **Data**: JSON (20개 주요 복지 혜택)
- **Deployment**: Streamlit Cloud (무료)

### 🌟 특징: Gemini 하나로 모든 AI 처리!
- **음성 인식 (STT)**: Gemini 멀티모달
- **AI 분석**: Gemini
- **음성 출력 (TTS)**: gTTS
- **필요한 API 키**: GEMINI_API_KEY 하나만!

## 📦 설치 방법

### 1. 레포지토리 클론
```bash
git clone <repository-url>
cd ai-conic
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API 키를 입력하세요.

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

#### API 키 발급 방법
- **Google Gemini API**: https://aistudio.google.com/app/apikey
  - **완전 무료!** (무료 할당량으로 충분)
  - 이 키 하나로 모든 기능 사용 가능 (STT + AI + 모든 처리)

## 🚀 실행 방법

```bash
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501`이 열립니다.

## 💡 사용 방법

### 방법 1: 텍스트 입력 (가장 간단)
1. "📝 텍스트 입력" 탭 선택
2. 어르신의 상황을 텍스트로 입력
   - 예: "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다."
3. "🔍 복지 혜택 찾기" 버튼 클릭
4. 결과 확인 및 다운로드

### 방법 2: 실시간 녹음 (가장 편리!) ⭐
1. "🎙️ 실시간 녹음" 탭 선택
2. 마이크 버튼 클릭 → 녹음 시작
3. 상황을 말씀하신 후 다시 버튼 클릭 → 녹음 종료
4. AI가 자동으로 분석하여 복지 혜택 추천
5. 음성으로 결과를 들어보세요
6. 필요시 텍스트/음성 파일로 다운로드

### 방법 3: 음성 파일 업로드
1. "📁 음성 파일" 탭 선택
2. 스마트폰 녹음 앱으로 미리 녹음한 파일 업로드
   - 지원 형식: mp3, wav, m4a
3. AI가 자동으로 분석
4. 결과 확인 및 다운로드

### 📥 결과 활용
- **텍스트 다운로드**: 복지혜택_추천결과.txt
- **음성 다운로드**: 복지혜택_음성안내.mp3
- 가족과 공유하거나 주민센터 방문 시 참고자료로 활용

## 📊 포함된 복지 혜택 (10개)

1. 기초연금 (월 최대 32만원)
2. 노인 장기요양보험
3. 기초생활수급 (월 50~150만원)
4. 에너지바우처 (연 9~36만원)
5. 통신요금 감면 (월 최대 1.1만원)
6. 치매 검진 지원
7. 독거노인 돌봄 서비스
8. 노인 일자리 지원 (월 27~71만원)
9. 임플란트 지원
10. 안경 구입비 지원 (3년 1회 5만원)

## 🎯 데모 시나리오

### 시나리오 1: 독거 할머니 (72세)
**입력**: "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다."

**AI 추천**:
- 기초연금
- 독거노인 돌봄 서비스
- 노인 장기요양보험

### 시나리오 2: 저소득 할아버지 (68세)
**입력**: "소득이 적어서 힘들고 일자리를 찾고 싶어요."

**AI 추천**:
- 기초생활수급
- 노인 일자리 지원
- 에너지바우처

### 시나리오 3: 일반 어르신 (70세)
**입력**: "건강검진과 치아 문제가 있어요."

**AI 추천**:
- 치매 검진 지원
- 임플란트 지원
- 노인 장기요양보험

## 📁 프로젝트 구조

```
ai-conic/
├── app.py                  # 메인 Streamlit 앱
├── welfare_data.json       # 복지 데이터 (10개)
├── requirements.txt        # Python 의존성
├── .env                    # API 키 (git에 미포함)
├── .env.example           # 환경 변수 템플릿
├── .gitignore             # Git 제외 파일
└── README.md              # 프로젝트 문서
```

## 🌟 주요 특징

### 1. 1인 개발자 최적화
- 단일 파일 구조로 간결함
- 약 390줄의 코드로 완성도 높은 기능 구현
- 복잡한 DB 없이 JSON 활용
- 3가지 입력 방식 모두 지원

### 2. 어르신 친화적 UI
- 큰 글씨 (1.3~3rem)
- 큰 버튼
- 파란색/흰색 중심의 편안한 색상
- 명확한 안내 메시지
- 상세한 사용 가이드 (접을 수 있는 형태)
- 에러 발생 시 친절한 설명 및 해결 방법 제시

### 3. 실시간 녹음 기능 (해커톤 차별화 포인트!) 🎙️
- **버튼 클릭 한 번**으로 녹음 시작/종료
- 파일 업로드 과정 불필요 → **사용자 경험 대폭 향상**
- 브라우저에서 즉시 처리 → 빠른 응답
- **시연 시 강력한 임팩트**: "지금 바로 말씀해보세요!"

### 4. Google Gemini AI 활용 (멀티모달)
- **하나의 API로 모든 처리**: STT + AI 분석 통합
- 뛰어난 한국어 이해 (사투리, 비표준 표현)
- 오디오를 직접 이해하여 더 정확한 분석
- 긴 컨텍스트로 전체 복지 데이터 포함 가능
- 안전하고 친절한 응답
- **완전 무료 API** (개발 단계에서 비용 부담 없음)

### 5. 결과 활용성
- 텍스트 파일 다운로드 → 가족과 공유
- 음성 파일 다운로드 → 반복해서 듣기
- 주민센터 방문 시 참고자료로 활용

## 💰 사회적 가치

- **연간 10만 명** 어르신에게 복지 혜택 전달
- **1인당 평균 50만원** × 10만 명 = **500억원** 복지 효과
- 디지털 격차 해소
- 복지 예산 집행률 향상

## 🎤 발표 자료

본 프로젝트는 **AI-conic 해커톤**을 위해 개발되었습니다.

- **주제**: C타입 - 복지의 사각지대에 놓인 사람들을 위한 서비스
- **개발 기간**: 3일 (1인 개발)
- **목표**: 복지 사각지대 해소 및 디지털 소외 어르신 지원

## 📞 문의

AI-conic 해커톤 팀

---

**💙 SilverLink는 기술로 복지 사각지대를 없애고, 모든 어르신이 받을 수 있는 혜택을 받을 수 있도록 돕습니다.**
