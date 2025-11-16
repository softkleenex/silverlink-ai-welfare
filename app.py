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
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    st.info("💡 Google AI Studio에서 API 키를 발급받으세요: https://aistudio.google.com/app/apikey")
    st.stop()

genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel('gemini-2.5-pro')

# 복지 데이터 로드
@st.cache_data
def load_welfare_data():
    with open('welfare_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

welfare_data = load_welfare_data()

# Gemini 프롬프트 생성 (JSON 포맷)
def create_prompt(user_text):
    welfare_info = json.dumps(welfare_data, ensure_ascii=False, indent=2)
    return f"""당신은 대한민국 복지 전문가 AI입니다.

**중요 지침**:
1. 보건복지부 '복지로' 사이트(www.bokjiro.go.kr)와 각 지자체 공식 홈페이지의 2025년 최신 데이터를 기반으로 답변하세요
2. 확실하지 않은 정보는 "가까운 주민센터(☎ 국번없이 129)에 문의가 필요합니다"라고 명시하세요
3. 반드시 아래 JSON 형식으로만 답변하세요 (다른 설명 없이 JSON만 출력)

어르신 상황: {user_text}

참고할 복지 혜택 목록:
{welfare_info}

**반드시 아래 JSON 형식으로 답변하세요**:
{{
  "greeting": "어르신의 상황에 공감하는 따뜻한 인사 (2-3문장)",
  "benefits": [
    {{
      "name": "복지 혜택명",
      "target": "대상 (예: 만 65세 이상, 소득 하위 70%)",
      "amount": "금액 (예: 월 최대 32만원)",
      "description": "혜택에 대한 간단한 설명 (1-2문장)",
      "next_action": "다음 할 일 - 구체적으로 (예: 신분증과 통장사본을 가지고 가까운 주민센터를 방문하여 신청하세요)",
      "documents": ["필요 서류 1", "필요 서류 2"],
      "contact": "문의처 (전화번호 포함)"
    }}
  ],
  "encouragement": "격려와 응원의 말씀 (2-3문장)"
}}

**주의**: 위 JSON 형식을 정확히 지켜주세요. 존댓말을 사용하고 따뜻하게 작성하세요."""

# Gemini 오디오 프롬프트 생성 (JSON 포맷)
def create_audio_prompt():
    welfare_info = json.dumps(welfare_data, ensure_ascii=False, indent=2)
    return f"""이 오디오에서 어르신의 말씀을 듣고 다음을 수행해주세요:

**중요 지침**:
1. 먼저 어르신이 말씀하신 내용을 텍스트로 정확하게 정리하세요
2. 보건복지부 '복지로' 사이트(www.bokjiro.go.kr)와 각 지자체 공식 홈페이지의 2025년 최신 데이터를 기반으로 답변하세요
3. 확실하지 않은 정보는 "가까운 주민센터(☎ 국번없이 129)에 문의가 필요합니다"라고 명시하세요
4. 반드시 아래 JSON 형식으로만 답변하세요 (다른 설명 없이 JSON만 출력)

참고할 복지 혜택 목록:
{welfare_info}

**반드시 아래 JSON 형식으로 답변하세요**:
{{
  "transcript": "어르신이 말씀하신 내용을 텍스트로 정리",
  "greeting": "어르신의 상황에 공감하는 따뜻한 인사 (2-3문장)",
  "benefits": [
    {{
      "name": "복지 혜택명",
      "target": "대상 (예: 만 65세 이상, 소득 하위 70%)",
      "amount": "금액 (예: 월 최대 32만원)",
      "description": "혜택에 대한 간단한 설명 (1-2문장)",
      "next_action": "다음 할 일 - 구체적으로 (예: 신분증과 통장사본을 가지고 가까운 주민센터를 방문하여 신청하세요)",
      "documents": ["필요 서류 1", "필요 서류 2"],
      "contact": "문의처 (전화번호 포함)"
    }}
  ],
  "encouragement": "격려와 응원의 말씀 (2-3문장)"
}}

**주의**: 위 JSON 형식을 정확히 지켜주세요. 존댓말을 사용하고 따뜻하게 작성하세요.
"""

# JSON 파싱 및 UI 표시 함수
def parse_and_display_response(response_text):
    """Gemini 응답을 JSON으로 파싱하고 구조화된 UI로 표시"""
    try:
        # JSON 추출 (```json ... ``` 형태로 올 수 있음)
        response_text = response_text.strip()
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()

        data = json.loads(response_text)

        # 인사말 표시
        if "greeting" in data:
            st.markdown(f'<div class="ai-message">🤖 **AI 복지 도우미**\n\n{data["greeting"]}</div>', unsafe_allow_html=True)

        # 어르신 말씀 (음성 파일의 경우)
        if "transcript" in data:
            st.markdown(f'<div class="user-message">👵 **어르신 말씀**\n\n{data["transcript"]}</div>', unsafe_allow_html=True)

        # 복지 혜택 표시
        if "benefits" in data and len(data["benefits"]) > 0:
            st.markdown("### 📋 추천 복지 혜택")
            for idx, benefit in enumerate(data["benefits"], 1):
                with st.expander(f"**{idx}. {benefit.get('name', '복지 혜택')}** - {benefit.get('amount', '')}"):
                    st.markdown(f"**🎯 대상**: {benefit.get('target', '정보 없음')}")
                    st.markdown(f"**📝 설명**: {benefit.get('description', '')}")

                    # Next Action 강조 표시
                    if "next_action" in benefit:
                        st.markdown(f"**👉 다음 할 일**")
                        st.info(benefit["next_action"])

                    if "documents" in benefit and len(benefit["documents"]) > 0:
                        st.markdown(f"**📄 필요 서류**: {', '.join(benefit['documents'])}")

                    if "contact" in benefit:
                        st.markdown(f"**📞 문의처**: {benefit['contact']}")

        # 격려 메시지
        if "encouragement" in data:
            st.markdown(f'<div class="ai-message">💙 {data["encouragement"]}</div>', unsafe_allow_html=True)

        # 전체 텍스트 생성 (TTS용)
        full_text = ""
        if "greeting" in data:
            full_text += data["greeting"] + "\n\n"

        if "benefits" in data:
            for idx, benefit in enumerate(data["benefits"], 1):
                full_text += f"{idx}. {benefit.get('name', '')}. "
                full_text += f"{benefit.get('description', '')} "
                full_text += f"금액은 {benefit.get('amount', '')}입니다. "
                if "next_action" in benefit:
                    full_text += f"{benefit['next_action']} "
                full_text += "\n\n"

        if "encouragement" in data:
            full_text += data["encouragement"]

        return full_text

    except json.JSONDecodeError as e:
        # JSON 파싱 실패 시 원본 텍스트 표시
        st.warning("⚠️ 응답을 구조화된 형식으로 표시할 수 없어 원본 텍스트로 표시합니다.")
        st.markdown(f'<div class="ai-message">{response_text}</div>', unsafe_allow_html=True)
        return response_text
    except Exception as e:
        st.error(f"응답 처리 중 오류 발생: {str(e)}")
        st.markdown(f'<div class="ai-message">{response_text}</div>', unsafe_allow_html=True)
        return response_text

# Streamlit 페이지 설정
st.set_page_config(
    page_title="SilverLink - AI 복지 도우미",
    page_icon="🎙️",
    layout="wide"
)

# 커스텀 CSS (큰 글씨, 큰 버튼, 모바일 최적화)
st.markdown("""
<style>
    /* 모바일 viewport 설정 */
    @viewport {
        width: device-width;
        zoom: 1.0;
    }

    /* 데스크톱 스타일 */
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
        min-height: 60px;
        width: 100%;
    }
    .user-message {
        font-size: 1.3rem;
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        word-wrap: break-word;
    }
    .ai-message {
        font-size: 1.3rem;
        background-color: #F1F8E9;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        word-wrap: break-word;
    }

    /* 모바일 최적화 (768px 이하) */
    @media only screen and (max-width: 768px) {
        .main-title {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        .sub-title {
            font-size: 1.2rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            font-size: 1.2rem;
            padding: 0.8rem 1.5rem;
            min-height: 50px;
        }
        .user-message, .ai-message {
            font-size: 1.1rem;
            padding: 0.8rem;
        }
        /* 텍스트 영역 크기 조정 */
        .stTextArea textarea {
            font-size: 1.1rem !important;
        }
        /* 탭 크기 조정 */
        .stTabs [data-baseweb="tab"] {
            font-size: 1rem;
            padding: 0.5rem 1rem;
        }
    }

    /* 작은 모바일 (480px 이하) */
    @media only screen and (max-width: 480px) {
        .main-title {
            font-size: 1.5rem;
        }
        .sub-title {
            font-size: 1rem;
        }
        .stButton>button {
            font-size: 1rem;
            padding: 0.6rem 1rem;
        }
        .user-message, .ai-message {
            font-size: 1rem;
            padding: 0.6rem;
        }
    }

    /* 터치 최적화 */
    @media (hover: none) and (pointer: coarse) {
        .stButton>button {
            min-height: 60px;
            touch-action: manipulation;
        }
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="main-title">🎙️ SilverLink</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">어르신을 위한 AI 복지 도우미</div>', unsafe_allow_html=True)

# 설명
st.info("💡 텍스트로 입력하거나 음성 파일을 업로드하시면 받으실 수 있는 복지 혜택을 안내해드립니다!")

# 사용 가이드
with st.expander("📖 사용 방법 보기"):
    st.markdown("""
    ### 🎯 이렇게 사용하세요!

    **1️⃣ 텍스트 입력**
    - 어르신의 상황을 텍스트로 입력하세요
    - 예: "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다"

    **2️⃣ 음성 파일 업로드**
    - 스마트폰 녹음 앱으로 음성을 녹음하세요
    - mp3, wav, m4a 파일을 업로드하세요

    **3️⃣ 실시간 녹음 (가장 쉬움!)**
    - 마이크 버튼을 눌러 바로 녹음하세요
    - 다시 버튼을 눌러 녹음을 완료하세요

    ### 💬 이런 정보를 말씀해주세요
    - 나이 (예: 72살, 68세 등)
    - 거주 상황 (독거, 가족과 동거 등)
    - 건강 상태 (거동 불편, 만성질환 등)
    - 경제 상황 (소득 수준, 일자리 필요 등)
    - 필요한 도움 (생활비, 의료비, 돌봄 등)

    ### ✅ 결과 확인
    - AI가 분석한 복지 혜택을 텍스트로 확인하세요
    - 음성으로도 들어보세요
    - 결과를 다운로드하여 보관하세요
    """)

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

                    # JSON 파싱 및 구조화된 UI 표시
                    ai_text = parse_and_display_response(ai_response)
                except Exception as e:
                    error_msg = str(e)
                    if "API key" in error_msg:
                        st.error("⚠️ API 키 오류: Gemini API 키를 확인해주세요.")
                    elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                        st.error("⚠️ API 할당량 초과: 잠시 후 다시 시도해주세요.")
                    elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                        st.error("⚠️ 네트워크 오류: 인터넷 연결을 확인하고 다시 시도해주세요.")
                    else:
                        st.error(f"⚠️ AI 처리 중 오류가 발생했습니다: {error_msg}")
                    st.info("💡 문제가 계속되면 페이지를 새로고침하거나 다시 시도해주세요.")
                    st.stop()

            # TTS 처리
            with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                try:
                    tts = gTTS(text=ai_text, lang='ko', slow=False)
                    tts.save("response.mp3")
                    st.success("✅ 응답 음성이 준비되었습니다!")
                    st.audio("response.mp3", format='audio/mp3')

                    # 다운로드 버튼
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📄 결과 텍스트 다운로드",
                            data=ai_text,
                            file_name="복지혜택_추천결과.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        with open("response.mp3", "rb") as f:
                            st.download_button(
                                label="🔊 음성 파일 다운로드",
                                data=f,
                                file_name="복지혜택_음성안내.mp3",
                                mime="audio/mp3",
                                use_container_width=True
                            )
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

                # JSON 파싱 및 구조화된 UI 표시
                ai_text = parse_and_display_response(ai_response)

            except Exception as e:
                error_msg = str(e)
                if "API key" in error_msg:
                    st.error("⚠️ API 키 오류: Gemini API 키를 확인해주세요.")
                elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    st.error("⚠️ API 할당량 초과: 잠시 후 다시 시도해주세요.")
                elif "audio" in error_msg.lower() or "file" in error_msg.lower():
                    st.error("⚠️ 음성 파일 처리 오류: 지원되는 형식(mp3, wav, m4a)인지 확인해주세요.")
                elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                    st.error("⚠️ 네트워크 오류: 인터넷 연결을 확인하고 다시 시도해주세요.")
                else:
                    st.error(f"⚠️ 처리 중 오류가 발생했습니다: {error_msg}")
                st.info("💡 다른 음성 파일로 시도하거나 페이지를 새로고침해주세요.")
                st.stop()

        # TTS 처리
        with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
            try:
                tts = gTTS(text=ai_text, lang='ko', slow=False)
                tts.save("response.mp3")

                st.success("✅ 응답 음성이 준비되었습니다!")
                st.audio("response.mp3", format='audio/mp3')

                # 다운로드 버튼
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📄 결과 텍스트 다운로드",
                        data=ai_text,
                        file_name="복지혜택_추천결과.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    with open("response.mp3", "rb") as f:
                        st.download_button(
                            label="🔊 음성 파일 다운로드",
                            data=f,
                            file_name="복지혜택_음성안내.mp3",
                            mime="audio/mp3",
                            use_container_width=True
                        )

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

                # JSON 파싱 및 구조화된 UI 표시
                ai_text = parse_and_display_response(ai_response)

            except Exception as e:
                error_msg = str(e)
                if "API key" in error_msg:
                    st.error("⚠️ API 키 오류: Gemini API 키를 확인해주세요.")
                elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    st.error("⚠️ API 할당량 초과: 잠시 후 다시 시도해주세요.")
                elif "audio" in error_msg.lower() or "file" in error_msg.lower():
                    st.error("⚠️ 녹음 파일 처리 오류: 다시 녹음해주세요.")
                elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                    st.error("⚠️ 네트워크 오류: 인터넷 연결을 확인하고 다시 시도해주세요.")
                else:
                    st.error(f"⚠️ 처리 중 오류가 발생했습니다: {error_msg}")
                st.info("💡 다시 녹음하거나 페이지를 새로고침해주세요.")
                st.stop()

        # TTS 처리
        with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
            try:
                tts = gTTS(text=ai_text, lang='ko', slow=False)
                tts.save("response.mp3")

                st.success("✅ 응답 음성이 준비되었습니다!")
                st.audio("response.mp3", format='audio/mp3')

                # 다운로드 버튼
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📄 결과 텍스트 다운로드",
                        data=ai_text,
                        file_name="복지혜택_추천결과.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    with open("response.mp3", "rb") as f:
                        st.download_button(
                            label="🔊 음성 파일 다운로드",
                            data=f,
                            file_name="복지혜택_음성안내.mp3",
                            mime="audio/mp3",
                            use_container_width=True
                        )

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
