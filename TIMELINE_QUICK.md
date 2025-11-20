# ⏱️ 영상 편집 타임라인 (복사용)

**목적**: 영상 편집할 때 이 파일 열어놓고 복사-붙여넣기

---

## 📌 인트로 (30초)
```
00:00-00:30
[나레이션] audio/narration/female/01_intro.mp3
[화면] 슬라이드 1-3 (문제 제기 + SilverLink 소개)
```

## 📌 서비스 소개 (30초)
```
00:30-01:00
[나레이션] audio/narration/female/02_service.mp3
[화면] 배포 URL 화면 (앱 시연)
```

## 📌 시나리오 1: 독거 할머니 (50초)
```
01:00-01:10
[나레이션] audio/narration/female/03_scenario1_intro.mp3
[화면] 시나리오1 슬라이드

01:10-01:15
[무음]
[화면] iPhone 녹화본 - 녹음 버튼 클릭

01:15-01:21
[모의 음성] audio/characters/character_grandma.mp3
[화면] iPhone 녹화본 - 녹음 중
⚠️ Mac 스피커로 이 파일 재생 → iPhone 마이크로 녹음
내용: "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다."

01:21-01:50
[나레이션] audio/narration/female/04_scenario1_result.mp3
[화면] iPhone 녹화본 - 결과 화면 스크롤
```

## 📌 시나리오 2: 저소득 할아버지 (50초)
```
01:50-02:00
[나레이션] audio/narration/female/05_scenario2_intro.mp3
[화면] 시나리오2 슬라이드

02:00-02:10
[무음]
[화면] iPhone 녹화본 - 텍스트 타이핑
타이핑 내용: "68살이고 소득이 적어서 힘들고 일자리를 찾고 싶어요."
💡 참고: audio/characters/character_grandpa.mp3

02:10-02:40
[나레이션] audio/narration/female/06_scenario2_result.mp3
[화면] iPhone 녹화본 - 결과 + 다운로드 버튼
```

## 📌 시나리오 3: 건강 문제 (50초)
```
02:40-02:50
[나레이션] audio/narration/female/07_scenario3_intro.mp3
[화면] 시나리오3 슬라이드

02:50-03:00
[무음]
[화면] iPhone 녹화본 - 음성 파일 업로드
업로드 파일: audio/characters/character_senior.mp3
💡 iPhone에 미리 AirDrop으로 전송 필요

03:00-03:30
[나레이션] audio/narration/female/08_scenario3_result.mp3
[화면] iPhone 녹화본 - 결과 화면
```

## 📌 기술 스택 (20초)
```
03:30-03:50
[나레이션] audio/narration/female/09_tech_stack.mp3
[화면] 기술 스택 슬라이드
```

## 📌 차별화 포인트 (20초)
```
03:50-04:10
[나레이션] audio/narration/female/10_differentiation.mp3
[화면] 차별화 포인트 슬라이드
```

## 📌 아웃트로 (20초)
```
04:10-04:30
[나레이션] audio/narration/female/11_outro.mp3
[화면] QR 코드 + URL 슬라이드
```

---

## 📋 사용 파일 체크리스트

### 나레이션 (11개) - audio/narration/female/
- [ ] 01_intro.mp3
- [ ] 02_service.mp3
- [ ] 03_scenario1_intro.mp3
- [ ] 04_scenario1_result.mp3
- [ ] 05_scenario2_intro.mp3
- [ ] 06_scenario2_result.mp3
- [ ] 07_scenario3_intro.mp3
- [ ] 08_scenario3_result.mp3
- [ ] 09_tech_stack.mp3
- [ ] 10_differentiation.mp3
- [ ] 11_outro.mp3

### 모의 사용자 음성 (3개) - audio/characters/
- [ ] character_grandma.mp3 - 시나리오1 Mac 스피커로 재생
- [ ] character_grandpa.mp3 - 시나리오2 타이핑 내용 참고만
- [ ] character_senior.mp3 - 시나리오3 iPhone에 업로드

---

## 💡 편집 꿀팁

### iMovie 사용 시:
1. 프로젝트 생성 (1920x1080, 30fps)
2. 타임라인에 슬라이드 이미지 드래그
3. 오디오 파일 드래그 (위 순서대로)
4. 각 구간 길이 맞추기 (정확한 초 단위)
5. 전환 효과 추가 (디졸브 0.5초)
6. 렌더링 (MP4 H.264)

### DaVinci Resolve 사용 시:
1. New Project → 1920x1080 30fps
2. Media Pool에 모든 파일 import
3. Timeline에 드래그 (시간 순서대로)
4. Audio track별로 정리 (나레이션/모의음성 분리)
5. Deliver → MP4 H.264 렌더링

### Kapwing (웹) 사용 시:
1. kapwing.com 접속
2. Upload: 슬라이드 + 오디오 파일
3. Timeline에 배치 (드래그앤드롭)
4. Export → MP4 다운로드

---

**작성자**: Claude Code
**전체 가이드**: docs/guides/VIDEO_GUIDE.md
