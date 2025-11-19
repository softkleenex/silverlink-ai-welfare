import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import json
import os
import hashlib
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

# Gemini 프롬프트 생성 (JSON 포맷) - AI 강화 버전
def create_prompt(user_text):
    welfare_info = json.dumps(welfare_data, ensure_ascii=False, indent=2)
    valid_names = [b["name"] for b in welfare_data]

    return f"""당신은 대한민국 복지 전문가 AI입니다.

**절대 준수 사항** (위반 시 잘못된 응답):
1. 오직 아래 제공된 {len(welfare_data)}개 복지 혜택만 추천하세요
   허용된 혜택: {', '.join(valid_names)}
   ⚠️ 위 목록에 없는 다른 혜택은 절대 언급 금지

2. 금액과 대상 조건은 아래 데이터와 정확히 일치해야 합니다
   ❌ 추측 금지 | ❌ 변경 금지 | ✅ 원본 그대로 복사

3. 각 혜택의 적합도를 0-100점으로 평가하세요 (relevance_score)
   - 90-100점: 완벽히 부합
   - 75-89점: 대부분 부합
   - 70-74점: 일부 부합
   - 70점 미만: 추천하지 마세요

4. 확실하지 않은 정보는 "가까운 주민센터(☎ 129)에 문의가 필요합니다"라고 명시

어르신 상황: {user_text}

복지 혜택 데이터베이스 ({len(welfare_data)}개):
{welfare_info}

**응답 예시** (반드시 이 형식을 따르세요):
{{
  "greeting": "어르신 안녕하세요. 혼자 생활하시면서 거동이 불편하신 상황이 정말 힘드실 것 같습니다. 받으실 수 있는 복지 혜택을 찾아보겠습니다.",
  "benefits": [
    {{
      "name": "독거노인 돌봄 서비스",
      "relevance_score": 95,
      "relevance_reason": "혼자 사시는 만 65세 이상 어르신을 위한 서비스",
      "target": "만 65세 이상 독거노인",
      "amount": "무료",
      "description": "정기적으로 안전을 확인하고 필요한 서비스를 연계해드립니다",
      "next_action": "주민센터를 방문하거나 국번없이 129에 전화하여 신청하세요",
      "documents": ["신분증"],
      "contact": "보건복지상담센터 129"
    }}
  ],
  "encouragement": "어르신께서 받으실 수 있는 혜택이 많습니다. 주민센터에 방문하시면 자세히 안내받으실 수 있습니다."
}}

**JSON 형식** (다른 설명 없이 JSON만 출력):
{{
  "greeting": "string (2-3문장, 존댓말)",
  "benefits": [
    {{
      "name": "string (위 {len(welfare_data)}개 중 정확히 하나)",
      "relevance_score": number (70-100),
      "relevance_reason": "string (왜 적합한지 구체적으로)",
      "target": "string (원본 데이터 그대로)",
      "amount": "string (원본 데이터 그대로)",
      "description": "string (1-2문장)",
      "next_action": "string (구체적 행동 지침)",
      "documents": ["string"],
      "contact": "string"
    }}
  ],
  "encouragement": "string (2-3문장, 따뜻하게)"
}}"""

# Gemini 오디오 프롬프트 생성 (JSON 포맷) - AI 강화 버전
def create_audio_prompt():
    welfare_info = json.dumps(welfare_data, ensure_ascii=False, indent=2)
    valid_names = [b["name"] for b in welfare_data]

    return f"""이 오디오에서 어르신의 말씀을 듣고 다음을 수행해주세요:

**절대 준수 사항** (위반 시 잘못된 응답):
1. 먼저 어르신이 말씀하신 내용을 텍스트로 정확하게 정리하세요 (transcript 필드)

2. 오직 아래 제공된 {len(welfare_data)}개 복지 혜택만 추천하세요
   허용된 혜택: {', '.join(valid_names)}
   ⚠️ 위 목록에 없는 다른 혜택은 절대 언급 금지

3. 금액과 대상 조건은 아래 데이터와 정확히 일치해야 합니다
   ❌ 추측 금지 | ❌ 변경 금지 | ✅ 원본 그대로 복사

4. 각 혜택의 적합도를 0-100점으로 평가하세요 (relevance_score)
   - 90-100점: 완벽히 부합
   - 75-89점: 대부분 부합
   - 70-74점: 일부 부합
   - 70점 미만: 추천하지 마세요

5. 확실하지 않은 정보는 "가까운 주민센터(☎ 129)에 문의가 필요합니다"라고 명시

복지 혜택 데이터베이스 ({len(welfare_data)}개):
{welfare_info}

**JSON 형식** (다른 설명 없이 JSON만 출력):
{{
  "transcript": "string (어르신이 말씀하신 내용 텍스트로)",
  "greeting": "string (2-3문장, 존댓말)",
  "benefits": [
    {{
      "name": "string (위 {len(welfare_data)}개 중 정확히 하나)",
      "relevance_score": number (70-100),
      "relevance_reason": "string (왜 적합한지 구체적으로)",
      "target": "string (원본 데이터 그대로)",
      "amount": "string (원본 데이터 그대로)",
      "description": "string (1-2문장)",
      "next_action": "string (구체적 행동 지침)",
      "documents": ["string"],
      "contact": "string"
    }}
  ],
  "encouragement": "string (2-3문장, 따뜻하게)"
}}"""

# 복지 혜택 검증 및 자동 수정 함수
def validate_and_fix_benefits(data):
    """AI가 추천한 혜택이 실제 데이터에 있는지 검증하고 자동 보정"""
    # 유효한 혜택명 딕셔너리 (이름 → 원본 데이터)
    valid_benefits = {b["name"]: b for b in welfare_data}

    if "benefits" not in data or not isinstance(data["benefits"], list):
        st.warning("⚠️ 복지 혜택 정보를 찾을 수 없습니다.")
        data["benefits"] = []
        return data

    validated = []
    for benefit in data["benefits"]:
        benefit_name = benefit.get("name", "")

        # 혜택명이 실제 데이터에 있는지 확인
        if benefit_name in valid_benefits:
            original = valid_benefits[benefit_name]

            # 금액과 대상을 원본 데이터로 강제 보정 (AI가 변경했을 수 있음)
            benefit["amount"] = original["amount"]
            benefit["target"] = original["target"]

            # documents와 contact도 원본으로 보정
            if "documents" not in benefit or not benefit["documents"]:
                benefit["documents"] = original["documents"]
            if "contact" not in benefit or not benefit["contact"]:
                benefit["contact"] = original["contact"]

            validated.append(benefit)
        else:
            # 존재하지 않는 혜택 발견 (Hallucination)
            st.warning(f"⚠️ '{benefit_name}'는 데이터베이스에 없는 혜택입니다. AI가 잘못된 정보를 제공했으므로 제외합니다.")

    data["benefits"] = validated

    # 유효한 혜택이 하나도 없으면 안내
    if len(validated) == 0:
        st.info("💡 정확히 매칭되는 혜택을 찾지 못했습니다. 가까운 주민센터(☎ 129)에 직접 문의해주세요.")

    return data

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

        # ✅ AI 응답 검증 및 보정 (Hallucination 방지)
        data = validate_and_fix_benefits(data)

        # 인사말 표시
        if "greeting" in data:
            st.markdown(f'<div class="ai-message">🤖 **AI 복지 도우미**\n\n{data["greeting"]}</div>', unsafe_allow_html=True)

        # 어르신 말씀 (음성 파일의 경우)
        if "transcript" in data:
            st.markdown(f'<div class="user-message">👵 **어르신 말씀**\n\n{data["transcript"]}</div>', unsafe_allow_html=True)

        # 복지 혜택 표시 (적합도 순으로 정렬)
        if "benefits" in data and len(data["benefits"]) > 0:
            # 적합도 점수로 정렬 (높은 순)
            sorted_benefits = sorted(
                data["benefits"],
                key=lambda x: x.get("relevance_score", 0),
                reverse=True
            )

            st.markdown("### 📋 추천 복지 혜택")
            for idx, benefit in enumerate(sorted_benefits, 1):
                # 적합도 점수 표시 (색상 구분)
                score = benefit.get("relevance_score", 0)
                if score >= 80:
                    score_color = "🟢"  # 매우 적합
                elif score >= 60:
                    score_color = "🟡"  # 적합
                else:
                    score_color = "🟠"  # 참고용

                with st.expander(f"**{idx}. {benefit.get('name', '복지 혜택')}** {score_color} (적합도 {score}점) - {benefit.get('amount', '')}"):
                    # 적합도 이유 표시
                    if "relevance_reason" in benefit:
                        st.info(f"**💡 추천 이유**: {benefit['relevance_reason']}")

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
                    response = gemini_model.generate_content(
                        create_prompt(user_text),
                        generation_config=genai.GenerationConfig(temperature=0.2)
                    )
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

    # 세션 상태 초기화
    if "processed_file_hash" not in st.session_state:
        st.session_state.processed_file_hash = None
    if "upload_result" not in st.session_state:
        st.session_state.upload_result = None

    uploaded_file = st.file_uploader(
        "음성 파일을 선택해주세요 (mp3, wav, m4a)",
        type=['mp3', 'wav', 'm4a'],
        help="스마트폰으로 녹음한 음성 파일을 업로드해주세요",
        key="file_uploader"
    )

    if uploaded_file is not None:
        # 파일 해시 생성 (중복 처리 방지)
        file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()

        # 이미 처리한 파일인지 확인
        if file_hash != st.session_state.processed_file_hash:
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
                    response = gemini_model.generate_content(
                        [create_audio_prompt(), audio_file],
                        generation_config=genai.GenerationConfig(temperature=0.2)
                    )

                    ai_response = response.text

                    # JSON 파싱 및 구조화된 UI 표시
                    ai_text = parse_and_display_response(ai_response)

                    # 처리 완료 표시 및 해시 저장
                    st.session_state.processed_file_hash = file_hash
                    st.session_state.upload_result = ai_text

                except Exception as e:
                    error_msg = str(e)
                    if "API key" in error_msg:
                        st.error("⚠️ API 키 오류: Gemini API 키를 확인해주세요.")
                    elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                        st.error("⚠️ API 할당량 초과: 잠시 후 다시 시도해주세요.")
                        st.info("💡 Gemini API 무료 할당량은 분당 15회입니다. 1분 정도 기다렸다가 다시 시도해주세요.")
                    elif "audio" in error_msg.lower() or "file" in error_msg.lower():
                        st.error("⚠️ 음성 파일 처리 오류: 지원되는 형식(mp3, wav, m4a)인지 확인해주세요.")
                    elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                        st.error("⚠️ 네트워크 오류: 인터넷 연결을 확인하고 다시 시도해주세요.")
                    else:
                        st.error(f"⚠️ 처리 중 오류가 발생했습니다: {error_msg}")
                    st.info("💡 다른 음성 파일로 시도하거나 페이지를 새로고침해주세요.")
                    st.session_state.processed_file_hash = None  # 에러 시 해시 초기화
                    st.stop()

            # TTS 처리
            if st.session_state.upload_result:
                with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                    try:
                        tts = gTTS(text=st.session_state.upload_result, lang='ko', slow=False)
                        tts.save("response.mp3")

                        st.success("✅ 응답 음성이 준비되었습니다!")
                        st.audio("response.mp3", format='audio/mp3')

                        # 다운로드 버튼
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                label="📄 결과 텍스트 다운로드",
                                data=st.session_state.upload_result,
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
            # 이미 처리된 파일
            st.info("✅ 이미 분석이 완료되었습니다. 다른 파일을 업로드하거나 페이지를 새로고침해주세요.")

# 탭 3: 실시간 녹음
with tab3:
    st.markdown("### 🎙️ 버튼을 눌러 직접 녹음해주세요")
    st.info("💡 아래 마이크 버튼을 눌러 녹음을 시작하고, 다시 눌러 녹음을 종료하세요")

    # 세션 상태 초기화
    if "processed_audio_hash" not in st.session_state:
        st.session_state.processed_audio_hash = None
    if "recording_result" not in st.session_state:
        st.session_state.recording_result = None

    # 실시간 녹음
    audio_bytes = audio_recorder(
        text="녹음 시작/중지",
        recording_color="#e74c3c",
        neutral_color="#3498db",
        icon_name="microphone",
        icon_size="3x",
        key="audio_recorder"  # 고유 키 추가
    )

    if audio_bytes:
        # 오디오 해시 생성 (중복 처리 방지)
        audio_hash = hashlib.md5(audio_bytes).hexdigest()

        # 이미 처리한 오디오인지 확인
        if audio_hash != st.session_state.processed_audio_hash:
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
                    response = gemini_model.generate_content(
                        [create_audio_prompt(), audio_file],
                        generation_config=genai.GenerationConfig(temperature=0.2)
                    )

                    ai_response = response.text

                    # JSON 파싱 및 구조화된 UI 표시
                    ai_text = parse_and_display_response(ai_response)

                    # 처리 완료 표시 및 해시 저장
                    st.session_state.processed_audio_hash = audio_hash
                    st.session_state.recording_result = ai_text

                except Exception as e:
                    error_msg = str(e)
                    if "API key" in error_msg:
                        st.error("⚠️ API 키 오류: Gemini API 키를 확인해주세요.")
                    elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                        st.error("⚠️ API 할당량 초과: 잠시 후 다시 시도해주세요.")
                        st.info("💡 Gemini API 무료 할당량은 분당 15회입니다. 1분 정도 기다렸다가 다시 시도해주세요.")
                    elif "audio" in error_msg.lower() or "file" in error_msg.lower():
                        st.error("⚠️ 녹음 파일 처리 오류: 다시 녹음해주세요.")
                    elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                        st.error("⚠️ 네트워크 오류: 인터넷 연결을 확인하고 다시 시도해주세요.")
                    else:
                        st.error(f"⚠️ 처리 중 오류가 발생했습니다: {error_msg}")
                    st.info("💡 다시 녹음하거나 페이지를 새로고침해주세요.")
                    st.session_state.processed_audio_hash = None  # 에러 시 해시 초기화
                    st.stop()

            # TTS 처리
            if st.session_state.recording_result:
                with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                    try:
                        tts = gTTS(text=st.session_state.recording_result, lang='ko', slow=False)
                        tts.save("response.mp3")

                        st.success("✅ 응답 음성이 준비되었습니다!")
                        st.audio("response.mp3", format='audio/mp3')

                        # 다운로드 버튼
                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                label="📄 결과 텍스트 다운로드",
                                data=st.session_state.recording_result,
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
            # 이미 처리된 오디오 - 이전 결과 표시
            if st.session_state.recording_result:
                st.info("✅ 이미 분석이 완료되었습니다. 새로운 녹음을 하려면 다시 녹음 버튼을 눌러주세요.")
                # 이전 결과를 다시 표시할 수도 있음 (선택사항)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #757575;'>
    <p>💙 SilverLink는 어르신들이 받을 수 있는 복지 혜택을 쉽게 찾도록 도와드립니다.</p>
    <p>문의: AI-conic 해커톤 팀</p>
</div>
""", unsafe_allow_html=True)
