#!/usr/bin/env python3
"""
ElevenLabs API를 사용하여 SilverLink 데모 영상 나레이션 자동 생성

사용법:
1. Voice Library에서 한국어 목소리 선택 후 voice_id 복사
2. .env 파일에 ELEVENLABS_API_KEY 설정
3. python scripts/generate_narration.py --voice-id YOUR_VOICE_ID

출력:
- narration/01_intro.mp3
- narration/02_service.mp3
- narration/03_scenario1_grandma.mp3
- narration/04_scenario2_grandpa.mp3
- narration/05_scenario3_health.mp3
- narration/06_tech_stack.mp3
- narration/07_outro.mp3
"""

import os
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 설정
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
API_BASE_URL = "https://api.elevenlabs.io/v1"

# 나레이션 스크립트 (VIDEO_SCRIPT.md에서 추출)
NARRATIONS = {
    "01_intro": """
어르신들의 복지 혜택 미신청률이 30%에 달합니다.
매년 수조원의 복지 예산이 집행되지 못하고 있습니다.

복잡한 온라인 신청 절차는
디지털 소외 어르신들에게 너무 어렵습니다.

SilverLink는 버튼 한 번으로
모든 복지 혜택을 찾아드립니다.
""",

    "02_service": """
SilverLink는 3가지 방식으로 복지 혜택을 찾을 수 있습니다.

첫째, 텍스트로 입력하거나
둘째, 버튼 한 번으로 바로 녹음하거나
셋째, 미리 녹음한 파일을 업로드할 수 있습니다.

Google Gemini 2.5 Pro AI가
음성 인식부터 복지 매칭까지 모든 과정을 처리합니다.
""",

    "03_scenario1_intro": """
72세 독거 할머니의 사례를 보여드리겠습니다.
혼자 사시면서 거동이 불편하신 상황입니다.
""",

    "04_scenario1_result": """
AI가 어르신의 상황을 분석하여
여러가지 복지 혜택을 추천했습니다.

독거노인 돌봄 서비스가 가장 적합한 것으로 분석되었습니다.

추천 이유와 신청 방법까지
음성으로 친절하게 안내해드립니다.
""",

    "05_scenario2_intro": """
68세 저소득 어르신의 사례입니다.
소득이 적어 힘들고 일자리를 찾고 계십니다.
""",

    "06_scenario2_result": """
텍스트로 입력하셔도 됩니다.

AI가 상황을 분석하여
일자리 지원과 생활비 지원을 추천했습니다.

결과를 텍스트와 음성 파일로 다운로드하여
가족과 공유하거나 주민센터에 가져갈 수 있습니다.
""",

    "07_scenario3_intro": """
70세 어르신의 건강 관련 사례입니다.
치아가 안 좋고 건강검진을 받고 싶으십니다.
""",

    "08_scenario3_result": """
스마트폰으로 미리 녹음한 파일도 사용할 수 있습니다.

치아 관련 지원과 건강검진을
우선순위에 따라 추천합니다.

스마트폰에서도 완벽하게 작동합니다.
""",

    "09_tech_stack": """
Google Gemini 2.5 Pro를 활용하여
음성 인식부터 AI 분석까지 통합 처리했습니다.

할루시네이션 방지 시스템으로
정확한 복지 정보만 제공합니다.

현재 Streamlit Cloud에 배포 완료되어
지금 바로 사용하실 수 있습니다.
""",

    "10_differentiation": """
SilverLink의 핵심 차별점은 세 가지입니다.

첫째, 실시간 녹음으로 버튼 한 번에 모든 과정이 끝납니다.
둘째, Gemini AI로 음성부터 분석까지 통합 처리합니다.
셋째, 즉시 사용 가능한 배포 완료 서비스입니다.
""",

    "11_outro": """
지금 바로 체험해보세요!

SilverLink는 기술로 복지 사각지대를 없앱니다.
"""
}

# 할머니/할아버지 음성 입력용 스크립트
CHARACTER_SCRIPTS = {
    "grandma": "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다.",
    "grandpa": "68살이고 소득이 적어서 힘들고 일자리를 찾고 싶어요.",
    "senior": "70살인데 치아가 안 좋고 건강검진을 받고 싶어요."
}


def generate_speech(text: str, voice_id: str, output_path: Path,
                   stability: float = 0.5, similarity: float = 0.6, style: float = 0.0):
    """
    ElevenLabs API를 사용하여 음성 생성

    Args:
        text: 변환할 텍스트
        voice_id: ElevenLabs voice ID
        output_path: 출력 파일 경로
        stability: 안정성 (0.0-1.0, 권장: 0.4-0.6)
        similarity: 유사성 (0.0-1.0, 권장: 0.5-0.7)
        style: 스타일 과장 (0.0-1.0, 권장: 0.0-0.2)
    """
    url = f"{API_BASE_URL}/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text.strip(),
        "model_id": "eleven_multilingual_v2",  # 한국어 지원 모델
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True
        }
    }

    print(f"🎙️  생성 중: {output_path.name}...")
    print(f"   텍스트: {text[:50]}...")

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        output_path.write_bytes(response.content)
        print(f"✅ 완료: {output_path}")
        return True
    else:
        print(f"❌ 실패: {response.status_code}")
        print(f"   에러: {response.text}")
        return False


def main():
    parser = argparse.ArgumentParser(description="SilverLink 나레이션 자동 생성")
    parser.add_argument("--voice-id", required=True, help="ElevenLabs Voice ID (나레이션용)")
    parser.add_argument("--grandma-voice-id", help="할머니 목소리 Voice ID (선택)")
    parser.add_argument("--grandpa-voice-id", help="할아버지 목소리 Voice ID (선택)")
    parser.add_argument("--output-dir", default="narration", help="출력 디렉토리")
    parser.add_argument("--stability", type=float, default=0.5, help="Stability (0.0-1.0)")
    parser.add_argument("--similarity", type=float, default=0.6, help="Similarity (0.0-1.0)")

    args = parser.parse_args()

    # API 키 확인
    if not ELEVENLABS_API_KEY:
        print("❌ 에러: ELEVENLABS_API_KEY가 .env 파일에 설정되지 않았습니다.")
        print("   .env 파일에 다음을 추가하세요:")
        print("   ELEVENLABS_API_KEY=your_api_key_here")
        return

    # 출력 디렉토리 생성
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("🎬 SilverLink 나레이션 생성 시작")
    print("=" * 60)
    print(f"Voice ID: {args.voice_id}")
    print(f"출력 디렉토리: {output_dir}")
    print(f"설정: Stability={args.stability}, Similarity={args.similarity}")
    print("=" * 60)
    print()

    # 나레이션 생성
    success_count = 0
    total_count = len(NARRATIONS)

    for filename, text in NARRATIONS.items():
        output_path = output_dir / f"{filename}.mp3"
        if generate_speech(text, args.voice_id, output_path,
                          args.stability, args.similarity):
            success_count += 1
        print()

    # 캐릭터 음성 생성 (선택)
    if args.grandma_voice_id:
        print("👵 할머니 목소리 생성...")
        output_path = output_dir / "character_grandma.mp3"
        generate_speech(CHARACTER_SCRIPTS["grandma"], args.grandma_voice_id,
                       output_path, stability=0.5, similarity=0.5, style=0.1)
        print()

    if args.grandpa_voice_id:
        print("👴 할아버지 목소리 생성...")
        output_path = output_dir / "character_grandpa.mp3"
        generate_speech(CHARACTER_SCRIPTS["grandpa"], args.grandpa_voice_id,
                       output_path, stability=0.5, similarity=0.5, style=0.1)
        print()

    # 결과 요약
    print("=" * 60)
    print(f"✅ 생성 완료: {success_count}/{total_count}")
    print(f"📁 출력 위치: {output_dir.absolute()}")
    print("=" * 60)
    print()
    print("📋 다음 단계:")
    print("1. narration/ 폴더에서 생성된 MP3 파일 확인")
    print("2. 각 파일 재생하여 품질 확인")
    print("3. 영상 편집 툴에서 타임라인에 배치")
    print()
    print("💡 Tip: 품질이 이상하면 --stability, --similarity 값 조정")
    print("   예: python scripts/generate_narration.py --voice-id XXX --stability 0.6 --similarity 0.7")


if __name__ == "__main__":
    main()
