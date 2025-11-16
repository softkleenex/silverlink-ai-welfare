# 🚀 Streamlit Cloud 배포 가이드

## 📋 사전 준비

1. **GitHub 계정** (이미 있음 ✅)
2. **Streamlit Cloud 계정** (무료)
3. **Gemini API 키** (이미 있음 ✅)

## 🔧 배포 단계

### 1단계: Streamlit Cloud 계정 생성

1. https://share.streamlit.io/ 접속
2. "Sign up" 클릭
3. **GitHub 계정으로 로그인** 선택
4. Streamlit에 GitHub 접근 권한 허용

### 2단계: 앱 배포

1. Streamlit Cloud 대시보드에서 **"New app"** 클릭
2. 다음 정보 입력:
   - **Repository**: `softkleenex/silverlink-ai-welfare`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (선택): 원하는 URL (예: `silverlink-ai-welfare`)

3. **"Advanced settings"** 클릭
4. **"Secrets"** 탭에서 다음 내용 추가:
   ```toml
   GEMINI_API_KEY = "AIzaSyDxy-idLNaEbS7rTUWjLejfTGcnLUYi7Yk"
   ```

5. **"Deploy!"** 클릭

### 3단계: 배포 완료 대기

- 첫 배포는 2-3분 소요
- 로그 화면에서 진행 상황 확인
- 에러 발생 시 로그에서 원인 확인

### 4단계: 배포 URL 확인

배포 완료 후 다음과 같은 URL을 받습니다:
```
https://silverlink-ai-welfare.streamlit.app
```

## ✅ 배포 체크리스트

- [ ] Streamlit Cloud 계정 생성
- [ ] GitHub 저장소 연동
- [ ] Secrets에 GEMINI_API_KEY 설정
- [ ] 앱 배포
- [ ] 배포 URL 테스트
- [ ] 3가지 시나리오 모두 테스트
  - [ ] 텍스트 입력
  - [ ] 실시간 녹음
  - [ ] 음성 파일 업로드

## 🔄 업데이트 방법

코드를 수정한 후:

```bash
git add .
git commit -m "Update: ..."
git push origin main
```

→ Streamlit Cloud가 **자동으로 재배포**합니다!

## ⚠️ 주의사항

1. **API 키 보안**
   - `.env` 파일은 절대 Git에 커밋하지 마세요 (이미 .gitignore에 포함됨 ✅)
   - Streamlit Cloud의 Secrets 기능을 사용하세요

2. **무료 한도**
   - Streamlit Cloud 무료 플랜: 앱 1개, 공개 저장소만 가능
   - Gemini API 무료 할당량: 매일 충분 (RPM 15, RPD 1500)

3. **실시간 녹음 기능**
   - 브라우저 마이크 권한 필요
   - HTTPS에서만 작동 (Streamlit Cloud는 자동으로 HTTPS 제공 ✅)

## 🎯 해커톤 발표용 URL

배포가 완료되면 발표 자료에 다음과 같이 포함:

```
🔗 라이브 데모: https://silverlink-ai-welfare.streamlit.app
📁 GitHub: https://github.com/softkleenex/silverlink-ai-welfare
```

## 🆘 문제 해결

### 문제: 앱이 시작되지 않음
**해결**: Streamlit Cloud 로그 확인 → requirements.txt의 패키지 버전 확인

### 문제: API 키 오류
**해결**: Streamlit Cloud 대시보드 → App settings → Secrets → GEMINI_API_KEY 다시 확인

### 문제: 실시간 녹음이 작동하지 않음
**해결**: 브라우저 마이크 권한 허용 확인 (HTTPS에서만 작동)

---

**💡 팁**: 해커톤 발표 전에 미리 배포해두고 URL을 테스트해보세요!
