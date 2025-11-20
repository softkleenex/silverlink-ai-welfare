# 📊 영상 슬라이드

영상 제작용 HTML 슬라이드입니다.

## 📁 파일 목록

1. **01_tech_stack.html** - 기술 스택 (03:30-03:50)
2. **02_differentiation.html** - 차별화 포인트 (03:50-04:10)
3. **03_outro.html** - 아웃트로 (04:10-04:30)

## 🎨 스크린샷 찍는 방법

### Mac

```bash
# 1. 브라우저에서 HTML 파일 열기
open slides/01_tech_stack.html

# 2. 전체 화면 (⌘+Shift+F)
# 3. 스크린샷 (⌘+Shift+4 → 스페이스 → 클릭)
```

### 또는 브라우저에서:

1. HTML 파일을 Chrome/Safari에서 열기
2. 개발자 도구 (F12) → Device Toolbar (⌘+Shift+M)
3. 해상도: 1920x1080 설정
4. 스크린샷 캡처

## 📋 QR 코드 생성

아웃트로 슬라이드의 QR 코드는 직접 생성해야 합니다:

1. https://www.qr-code-generator.com/ 접속
2. URL 입력: `https://silverlink-ai.streamlit.app`
3. QR 코드 다운로드
4. 이미지 편집기로 슬라이드에 삽입

## 🎬 iMovie에서 사용

1. 위 방법으로 3개 슬라이드 스크린샷
2. iMovie에 Import
3. 타임라인에 배치:
   - 03:30-03:50: 01_tech_stack.png
   - 03:50-04:10: 02_differentiation.png
   - 04:10-04:30: 03_outro.png
4. 나레이션 오디오와 동기화

## 🎨 디자인 특징

- **해상도**: 1920x1080 (Full HD)
- **폰트**: Pretendard (시스템 폰트 fallback)
- **색상 테마**:
  - 기술 스택: 보라색 그라데이션
  - 차별화: 핑크 그라데이션
  - 아웃트로: 블루 그라데이션
- **반응형**: 브라우저 크기에 맞게 자동 조정

## 💡 Tip

- 브라우저 확대/축소 (⌘+/-) 로 크기 조정 가능
- PNG로 저장 시 고화질 유지
- 배경 투명도 필요하면 CSS 수정
