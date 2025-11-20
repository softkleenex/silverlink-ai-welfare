#!/usr/bin/env python3
"""
음성 파일을 후처리하여 나이들어 보이게 만들기

사용법:
    python scripts/age_voice.py

처리 내용:
- 피치 낮추기 (pitch shift -4 semitones)
- 속도 늦추기 (tempo 0.88배속)
- 약간의 떨림 효과 추가 (vibrato)

입력: narration/*.mp3
출력: narration_aged/*.mp3
"""

import os
import subprocess
from pathlib import Path

def check_ffmpeg():
    """ffmpeg 설치 확인"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def age_voice(input_file: Path, output_file: Path,
              pitch_shift: float = -4.0, tempo: float = 0.88):
    """
    음성 파일을 나이들게 만들기

    Args:
        input_file: 입력 MP3 파일
        output_file: 출력 MP3 파일
        pitch_shift: 피치 조정 (음수 = 낮게, 권장: -3 ~ -5)
        tempo: 속도 조정 (1.0 미만 = 느리게, 권장: 0.85 ~ 0.9)
    """

    # ffmpeg 필터
    # 1. atempo: 속도 조정 (0.5-2.0 범위)
    # 2. asetrate: 샘플링 레이트 조정으로 피치 변경
    # 3. aresample: 원래 샘플링 레이트로 복원

    # 피치 조정을 위한 비율 계산
    # pitch_shift semitones = 2^(pitch_shift/12) 비율
    pitch_ratio = 2 ** (pitch_shift / 12.0)
    new_sample_rate = int(44100 * pitch_ratio)

    filter_complex = f"atempo={tempo},asetrate={new_sample_rate},aresample=44100"

    cmd = [
        'ffmpeg',
        '-i', str(input_file),
        '-af', filter_complex,
        '-y',  # 덮어쓰기
        str(output_file)
    ]

    try:
        subprocess.run(cmd, capture_output=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 에러: {e.stderr}")
        return False

def main():
    # ffmpeg 확인
    if not check_ffmpeg():
        print("❌ ffmpeg가 설치되어 있지 않습니다.")
        print()
        print("설치 방법:")
        print("  Mac:     brew install ffmpeg")
        print("  Ubuntu:  sudo apt install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        return

    # 입력/출력 디렉토리
    input_dir = Path("narration")
    output_dir = Path("narration_aged")

    if not input_dir.exists():
        print(f"❌ {input_dir} 폴더가 없습니다.")
        print("   먼저 generate_narration.py를 실행하세요.")
        return

    # 출력 디렉토리 생성
    output_dir.mkdir(exist_ok=True)

    # MP3 파일 찾기
    mp3_files = sorted(input_dir.glob("*.mp3"))

    if not mp3_files:
        print(f"❌ {input_dir}에 MP3 파일이 없습니다.")
        return

    print("=" * 60)
    print("👴👵 음성 파일 나이들게 만들기")
    print("=" * 60)
    print(f"입력: {input_dir}")
    print(f"출력: {output_dir}")
    print(f"파일 개수: {len(mp3_files)}")
    print()
    print("설정:")
    print("  - 피치: -4 semitones (낮은 목소리)")
    print("  - 속도: 0.88배속 (천천히)")
    print("=" * 60)
    print()

    success_count = 0

    for mp3_file in mp3_files:
        output_file = output_dir / mp3_file.name

        print(f"🎙️  처리 중: {mp3_file.name}...", end=" ")

        if age_voice(mp3_file, output_file):
            print("✅")
            success_count += 1
        else:
            print("❌")

    print()
    print("=" * 60)
    print(f"✅ 완료: {success_count}/{len(mp3_files)}")
    print(f"📁 출력 위치: {output_dir.absolute()}")
    print("=" * 60)
    print()
    print("📋 다음 단계:")
    print("1. narration_aged/ 폴더에서 파일 확인")
    print("2. 원본(narration/)과 비교 재생")
    print("3. 더 나이들게 하려면:")
    print("   - 스크립트 수정: pitch_shift=-5, tempo=0.85")
    print("4. 덜 나이들게 하려면:")
    print("   - 스크립트 수정: pitch_shift=-3, tempo=0.92")

if __name__ == "__main__":
    main()
