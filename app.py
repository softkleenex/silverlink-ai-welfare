import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import json
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 클라이언트 초기화
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# 복지 데이터 로드
@st.cache_data
def load_welfare_data():
    with open('welfare_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

welfare_data = load_welfare_data()

# Gemini 프롬프트 생성
def create_prompt(user_text):
    welfare_info = json.dumps(welfare_data, ensure_ascii=False, indent=2)
    return f"""당신은 어르신을 위한 따뜻한 복지 안내 AI입니다.

어르신의 상황을 듣고 다음 정보를 파악해주세요:
- 나이
- 거주지
- 소득 수준 (기초생활수급자, 차상위계층, 일반 등)
- 건강 상태
- 가족 상황 (독거, 가족과 동거 등)

아래 복지 혜택 목록에서 어르신께 적합한 혜택을 3-5개 추천해주세요.

복지 혜택 목록:
{welfare_info}

응답 형식:
1. 먼저 어르신의 상황에 공감하는 따뜻한 인사
2. 받으실 수 있는 복지 혜택 3-5가지 추천 (혜택명, 금액, 신청방법 포함)
3. 각 혜택별로 필요한 서류와 담당 기관 안내
4. 격려와 응원의 말씀

반드시 존댓말을 사용하고, 어르신께서 이해하기 쉽게 친절하고 따뜻하게 설명해주세요.

어르신 말씀: {user_text}
"""

# Gemini 오디오 프롬프트 생성
def create_audio_prompt():
    welfare_info = json.dumps(welfare_data, ensure_ascii=False, indent=2)
    return f"""이 오디오에서 어르신의 말씀을 듣고 다음을 수행해주세요:

1. 먼저 어르신이 말씀하신 내용을 텍스트로 정리해주세요.

2. 말씀에서 다음 정보를 파악해주세요:
   - 나이
   - 거주지
   - 소득 수준 (기초생활수급자, 차상위계층, 일반 등)
   - 건강 상태
   - 가족 상황 (독거, 가족과 동거 등)

3. 아래 복지 혜택 목록에서 어르신께 적합한 혜택을 3-5개 추천해주세요.

복지 혜택 목록:
{welfare_info}

응답 형식:
[어르신 말씀]
(어르신이 말씀하신 내용을 텍스트로 정리)

[AI 복지 도우미]
1. 어르신의 상황에 공감하는 따뜻한 인사
2. 받으실 수 있는 복지 혜택 3-5가지 추천 (혜택명, 금액, 신청방법 포함)
3. 각 혜택별로 필요한 서류와 담당 기관 안내
4. 격려와 응원의 말씀

반드시 존댓말을 사용하고, 어르신께서 이해하기 쉽게 친절하고 따뜻하게 설명해주세요.
"""

# Streamlit 페이지 설정
st.set_page_config(
    page_title="SilverLink - AI 복지 도우미",
    page_icon="🎙️",
    layout="wide"
)

# 커스텀 CSS (큰 글씨, 큰 버튼)
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-title {
        font-size: 1.8rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        font-size: 1.5rem;
        padding: 1rem 2rem;
        border-radius: 10px;
    }
    .user-message {
        font-size: 1.3rem;
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .ai-message {
        font-size: 1.3rem;
        background-color: #F1F8E9;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="main-title">🎙️ SilverLink</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">어르신을 위한 AI 복지 도우미</div>', unsafe_allow_html=True)

# 설명
st.info("💡 텍스트로 입력하거나 음성 파일을 업로드하시면 받으실 수 있는 복지 혜택을 안내해드립니다!")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["📝 텍스트 입력", "📁 음성 파일", "🎙️ 실시간 녹음"])

# 탭 1: 텍스트 입력
with tab1:
    st.markdown("### 어르신의 상황을 말씀해주세요")
    user_input = st.text_area(
        "상황 입력",
        placeholder="예: 저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다.",
        height=150,
        label_visibility="collapsed"
    )

    if st.button("🔍 복지 혜택 찾기", type="primary", use_container_width=True):
        if user_input.strip():
            user_text = user_input.strip()
            st.markdown(f'<div class="user-message">👵 어르신 말씀: {user_text}</div>', unsafe_allow_html=True)

            # Gemini AI 처리
            with st.spinner("🤖 복지 혜택을 찾고 있어요..."):
                try:
                    response = gemini_model.generate_content(create_prompt(user_text))
                    ai_response = response.text
                    st.markdown(f'<div class="ai-message">🤖 AI 도우미:\n\n{ai_response}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI 처리 중 오류가 발생했습니다: {str(e)}")
                    st.stop()

            # TTS 처리
            with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                try:
                    tts = gTTS(text=ai_response, lang='ko', slow=False)
                    tts.save("response.mp3")
                    st.success("✅ 응답 음성이 준비되었습니다!")
                    st.audio("response.mp3", format='audio/mp3')
                except Exception as e:
                    st.error(f"음성 변환 중 오류가 발생했습니다: {str(e)}")
        else:
            st.warning("상황을 입력해주세요!")

# 탭 2: 음성 파일 업로드
with tab2:
    st.markdown("### 음성 파일을 업로드해주세요")

    uploaded_file = st.file_uploader(
        "음성 파일을 선택해주세요 (mp3, wav, m4a)",
        type=['mp3', 'wav', 'm4a'],
        help="스마트폰으로 녹음한 음성 파일을 업로드해주세요"
    )

    if uploaded_file is not None:
        # 오디오 파일 표시
        st.audio(uploaded_file, format=f'audio/{uploaded_file.type.split("/")[1]}')

        # Gemini로 오디오 처리 (STT + AI 분석 한 번에!)
        with st.spinner("🎧 어르신 말씀을 듣고 복지 혜택을 찾고 있어요..."):
            try:
                # 임시 파일로 저장
                temp_path = "temp_audio.mp3"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Gemini에 오디오 파일 업로드
                audio_file = genai.upload_file(path=temp_path)

                # Gemini로 오디오 분석 (STT + 복지 매칭 한 번에!)
                response = gemini_model.generate_content([
                    create_audio_prompt(),
                    audio_file
                ])

                ai_response = response.text
                st.markdown(f'<div class="ai-message">{ai_response}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"처리 중 오류가 발생했습니다: {str(e)}")
                st.stop()

        # TTS 처리
        with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
            try:
                tts = gTTS(text=ai_response, lang='ko', slow=False)
                tts.save("response.mp3")

                st.success("✅ 응답 음성이 준비되었습니다!")
                st.audio("response.mp3", format='audio/mp3')

            except Exception as e:
                st.error(f"음성 변환 중 오류가 발생했습니다: {str(e)}")

# 탭 3: 실시간 녹음
with tab3:
    st.markdown("### 🎙️ 버튼을 눌러 직접 녹음해주세요")
    st.info("💡 아래 마이크 버튼을 눌러 녹음을 시작하고, 다시 눌러 녹음을 종료하세요")

    # 실시간 녹음
    audio_bytes = audio_recorder(
        text="녹음 시작/중지",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="3x",
    )

    if audio_bytes:
        st.success("✅ 녹음이 완료되었습니다!")

        # 녹음된 오디오 재생
        st.audio(audio_bytes, format='audio/wav')

        # Gemini로 오디오 처리
        with st.spinner("🎧 어르신 말씀을 듣고 복지 혜택을 찾고 있어요..."):
            try:
                # 임시 파일로 저장
                temp_path = "temp_recorded_audio.wav"
                with open(temp_path, "wb") as f:
                    f.write(audio_bytes)

                # Gemini에 오디오 파일 업로드
                audio_file = genai.upload_file(path=temp_path)

                # Gemini로 오디오 분석
                response = gemini_model.generate_content([
                    create_audio_prompt(),
                    audio_file
                ])

                ai_response = response.text
                st.markdown(f'<div class="ai-message">{ai_response}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"처리 중 오류가 발생했습니다: {str(e)}")
                st.stop()

        # TTS 처리
        with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
            try:
                tts = gTTS(text=ai_response, lang='ko', slow=False)
                tts.save("response.mp3")

                st.success("✅ 응답 음성이 준비되었습니다!")
                st.audio("response.mp3", format='audio/mp3')

            except Exception as e:
                st.error(f"음성 변환 중 오류가 발생했습니다: {str(e)}")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #757575;'>
    <p>💙 SilverLink는 어르신들이 받을 수 있는 복지 혜택을 쉽게 찾도록 도와드립니다.</p>
    <p>문의: AI-conic 해커톤 팀</p>
</div>
""", unsafe_allow_html=True)
