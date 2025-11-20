import streamlit as st
import google.generativeai as genai
from gtts import gTTS
# from audio_recorder_streamlit import audio_recorder  # 자동 중지 문제로 제거
import json
import os
import hashlib
import re
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

# 금액 파싱 함수 (웹 검색 결과에서 금액 추출)
def extract_amount_from_text(text):
    """
    텍스트에서 금액을 파싱합니다.
    예: "34만 2,510원" → "342510원"
        "월 32만원" → "320000원"
    """
    # 패턴 1: "34만 2,510원" 형식
    pattern1 = r'(\d+)만\s*(\d{1},)?(\d{3})원'
    match = re.search(pattern1, text)
    if match:
        man = int(match.group(1))  # 만 단위
        cheon = match.group(3)  # 천 단위
        return f"{man * 10000 + int(cheon)}원"

    # 패턴 2: "32만원" 형식
    pattern2 = r'(\d+)만\s*원'
    match = re.search(pattern2, text)
    if match:
        man = int(match.group(1))
        return f"{man * 10000}원"

    # 패턴 3: "320000원", "32만" 등
    pattern3 = r'(\d+)원'
    match = re.search(pattern3, text)
    if match:
        return match.group(0)

    return None

# 최신 복지 정보 (2025년 기준)
# 웹 검색 에이전트로 확인한 최신 금액 (2025.11.20 기준)
# 커버리지: 20개 전체 (100%)
LATEST_WELFARE_INFO_2025 = {
    "기초연금": {
        "amount": "월 최대 34만 2,510원 (단독가구)",
        "source": "보건복지부",
        "date": "2025",
        "note": "2024년 33만 4,810원에서 2.3% 인상. 선정기준 단독가구 월 228만원 이하"
    },
    "노인 장기요양보험": {
        "amount": "서비스 종류별 월 50~150만원 상당",
        "source": "국민건강보험공단",
        "date": "2025",
        "note": "방문요양, 방문목욕, 주야간보호 등 서비스별 차등 지원"
    },
    "기초생활수급": {
        "amount": "1인 월 76만 5,444원, 2인 125만 8,451원, 3인 160만 8,113원, 4인 195만 1,287원",
        "source": "보건복지부",
        "date": "2025",
        "note": "생계급여 기준 중위소득 32%. 의료·주거·교육급여 별도"
    },
    "에너지바우처": {
        "amount": "가구원 수에 따라 연 9만~36만원",
        "source": "산업통상자원부",
        "date": "2025",
        "note": "전기·가스·난방비 등 에너지 비용 지원. 매년 5~6월 신청"
    },
    "치매 검진 지원": {
        "amount": "검사 비용 전액 지원 (소득 기준 충족 시)",
        "source": "보건복지부",
        "date": "2025",
        "note": "만 60세 이상 선별·진단·감별검사 무료"
    },
    "독거노인 돌봄 서비스": {
        "amount": "무료",
        "source": "보건복지부",
        "date": "2025",
        "note": "안전 확인, 생활 교육, 서비스 연계 등 제공"
    },
    "통신요금 감면": {
        "amount": "월 최대 1만 1천원 (이동전화) + 인터넷 할인",
        "source": "과학기술정보통신부",
        "date": "2025",
        "note": "만 65세 이상 기초연금 수급자 대상"
    },
    "노인 일자리 지원": {
        "amount": "공익활동 월 27~60만원, 시장형 월 최대 71만원",
        "source": "보건복지부",
        "date": "2025",
        "note": "2025년 총 109.8만개 일자리 제공 (공익활동 69.2만개)"
    },
    "임플란트 지원": {
        "amount": "본인 부담금 30% (개당 약 50만원 수준)",
        "source": "국민건강보험공단",
        "date": "2025",
        "note": "만 65세 이상, 평생 2개까지 건강보험 적용"
    },
    "노인 틀니 지원": {
        "amount": "본인 부담금 30% (완전틀니 약 40만원, 부분틀니 약 30만원)",
        "source": "국민건강보험공단",
        "date": "2025",
        "note": "만 65세 이상, 7년에 1회 건강보험 적용"
    },
    "주거급여": {
        "amount": "1인가구 월 20만~35만원 (지역별 차등)",
        "source": "국토교통부",
        "date": "2025",
        "note": "소득인정액 기준 중위소득 48% 이하. 1급지(서울) 35.2만원, 4급지 20.1만원"
    },
    "재가 노인 식사 배달 서비스": {
        "amount": "무료 또는 식사당 1,000~3,000원",
        "source": "보건복지부",
        "date": "2025",
        "note": "만 65세 이상 거동 불편 어르신 대상"
    },
    "긴급복지 지원": {
        "amount": "생계비 1인 월 62만원, 의료비 300만원 한도",
        "source": "보건복지부",
        "date": "2025",
        "note": "갑작스러운 위기상황 발생 시 신속 지원"
    },
    "노인 교통비 지원": {
        "amount": "지하철 무료, 시내버스 무료 또는 할인 (지역별 상이)",
        "source": "지자체",
        "date": "2025",
        "note": "만 65세 이상 자동 적용. 신분증 제시"
    },
    "저소득 노인 냉난방비 지원": {
        "amount": "하절기 4만원, 동절기 6만원",
        "source": "보건복지부",
        "date": "2025",
        "note": "기초생활수급자, 차상위계층 중 만 65세 이상. 자동 지급"
    },
    "노인 건강진단 지원": {
        "amount": "일반검진 무료, 암 검진 본인부담 10% (약 1~3만원)",
        "source": "국민건강보험공단",
        "date": "2025",
        "note": "만 66세 이상 건강보험 가입자, 2년에 1회"
    },
    "독감 예방접종 지원": {
        "amount": "무료 (연 1회)",
        "source": "질병관리청",
        "date": "2025",
        "note": "만 65세 이상, 매년 9~11월 접종 가능"
    },
    "치매치료 관리비 지원": {
        "amount": "월 최대 3만원 (연 36만원)",
        "source": "보건복지부",
        "date": "2025",
        "note": "치매 진단 만 60세 이상, 소득 기준 충족 시 치매약 처방 본인부담금 지원"
    },
    "안경 구입비 지원": {
        "amount": "3년에 1회, 최대 5만원",
        "source": "보건복지부",
        "date": "2025",
        "note": "기초생활수급자, 차상위계층 중 만 65세 이상"
    },
    "노인 안검하수 수술 지원": {
        "amount": "본인 부담금 30~60% (약 30~50만원)",
        "source": "국민건강보험공단",
        "date": "2025",
        "note": "만 60세 이상, 시야장애 시 건강보험 적용"
    }
}

def get_latest_welfare_info():
    """
    2025년 최신 복지 정보를 반환합니다.
    실제 배포 환경에서는 공공 API 연동 예정.
    """
    enable_latest_info = os.getenv("SHOW_LATEST_INFO", "true") == "true"

    if not enable_latest_info:
        return {}

    return LATEST_WELFARE_INFO_2025

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

**분석 방법 (단계별):**
1단계: 사용자 정보 추출 (나이, 거주 형태, 건강 상태, 경제 상황)
2단계: 각 복지 혜택의 대상 조건과 매칭
3단계: 적합도 점수 산정 (조건 충족률 기반)
4단계: 상위 3-5개 혜택 추천

**좋은 추천 예시:**

예시 1:
입력: "72살 독거노인, 다리 불편, 소득 월 80만원"
분석: 나이(72) → 노인복지 O, 독거 → 돌봄필요 O, 다리불편 → 장기요양 가능, 저소득 → 기초연금 O
추천: 기초연금(95점), 독거노인 돌봄 서비스(92점), 노인 장기요양보험(85점)

예시 2:
입력: "68살, 치아 안 좋음, 건강검진 받고 싶어요"
분석: 나이(68) → 노인건강 O, 치아 → 틀니/임플란트 O, 검진 → 무료검진 O
추천: 노인 틀니 지원(98점), 노인 건강진단(95점), 임플란트 지원(90점)

예시 3:
입력: "75살, 일자리 찾습니다"
분석: 나이(75) → 노인일자리 O, 일 의욕 O
추천: 노인 일자리 지원(100점), 기초연금(80점 - 일자리 병행 가능)

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

**분석 방법 (단계별):**
1단계: 음성 텍스트 변환 (transcript)
2단계: 사용자 정보 추출 (나이, 거주, 건강, 경제)
3단계: 조건 매칭 및 적합도 점수 산정
4단계: 상위 3-5개 혜택 추천

**좋은 추천 예시:**

예시 1:
음성: "72살 독거노인, 다리 불편, 소득 월 80만원"
분석: 나이(72) → 노인복지, 독거 → 돌봄, 다리불편 → 장기요양, 저소득 → 기초연금
추천: 기초연금(95점), 독거노인 돌봄 서비스(92점), 노인 장기요양보험(85점)

예시 2:
음성: "68살, 치아 안 좋음, 건강검진 받고 싶어요"
분석: 나이(68) → 노인건강, 치아 → 틀니/임플란트, 검진 → 무료검진
추천: 노인 틀니 지원(98점), 노인 건강진단(95점), 임플란트 지원(90점)

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

                    # 2025년 최신 정보 표시
                    latest_info = get_latest_welfare_info()
                    benefit_name = benefit.get('name', '')
                    if benefit_name in latest_info:
                        latest = latest_info[benefit_name]
                        st.success(f"✨ **2025년 최신 정보**: {latest['amount']}")
                        if 'note' in latest:
                            st.caption(f"📌 {latest['note']} (출처: {latest['source']})")

        # 격려 메시지
        if "encouragement" in data:
            st.markdown(f'<div class="ai-message">💙 {data["encouragement"]}</div>', unsafe_allow_html=True)

        # 전체 텍스트 생성 (TTS용)
        full_text = ""
        if "greeting" in data:
            full_text += data["greeting"] + "\n\n"

        if "benefits" in data and len(data["benefits"]) > 0:
            for idx, benefit in enumerate(data["benefits"], 1):
                full_text += f"{idx}번. {benefit.get('name', '')}. "
                full_text += f"{benefit.get('description', '')} "
                full_text += f"금액은 {benefit.get('amount', '')}입니다. "
                if "next_action" in benefit:
                    full_text += f"{benefit['next_action']} "
                full_text += "\n\n"
        else:
            # 추천 혜택이 없을 경우 기본 메시지
            full_text += "정확히 매칭되는 복지 혜택을 찾지 못했습니다. 가까운 주민센터 129번에 문의해주세요.\n\n"

        if "encouragement" in data:
            full_text += data["encouragement"]

        # 빈 텍스트 방지: 최소 메시지 보장
        if not full_text or len(full_text.strip()) < 10:
            full_text = "복지 혜택 분석이 완료되었습니다. 자세한 내용은 주민센터에 문의해주세요."

        return full_text.strip()

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

# 로고 및 제목
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("docs/hackathon/silverlink_logo_horizontal.svg", use_container_width=True)

st.markdown('<div class="sub-title" style="text-align: center; margin-top: -10px;">어르신을 위한 AI 복지 도우미</div>', unsafe_allow_html=True)

# 설명
st.info("💡 텍스트로 입력하거나 음성 파일을 업로드하시면 받으실 수 있는 복지 혜택을 안내해드립니다!")

# 사용 가이드
with st.expander("📖 사용 방법 보기"):
    st.markdown("""
    ### 🎯 이렇게 사용하세요!

    **1️⃣ 텍스트 입력**
    - 어르신의 상황을 텍스트로 입력하세요
    - 예: "저는 72살이고 혼자 살고 있어요. 다리가 아파서 거동이 불편합니다"

    **2️⃣ 실시간 녹음 (가장 쉬움!)**
    - 마이크 버튼을 눌러 바로 녹음하세요
    - 다시 버튼을 눌러 녹음을 완료하세요

    **3️⃣ 음성 파일 업로드**
    - 스마트폰 녹음 앱으로 음성을 녹음하세요
    - mp3, wav, m4a 파일을 업로드하세요

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
tab1, tab2, tab3 = st.tabs(["📝 텍스트 입력", "🎙️ 실시간 녹음", "📁 음성 파일"])

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
            if ai_text and len(ai_text.strip()) > 0:
                with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                    try:
                        # TTS를 위한 텍스트 정리 (이모지 제거)
                        clean_text = re.sub(r'[^\w\s가-힣.,!?。、\n]', '', ai_text)

                        if len(clean_text.strip()) < 5:
                            raise ValueError("텍스트가 너무 짧습니다")

                        tts = gTTS(text=clean_text, lang='ko', slow=False)
                        tts.save("response.mp3")

                        st.success("✅ 응답 음성이 준비되었습니다!")
                        st.info("💡 아래 버튼을 눌러 음성 파일을 다운로드한 후 재생하세요")

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
                        error_type = type(e).__name__
                        st.error(f"⚠️ 음성 변환 중 오류가 발생했습니다 ({error_type})")
                        st.info(f"상세 정보: {str(e)}")
                        st.info("💡 결과는 위에서 확인하실 수 있습니다. 음성 파일은 생성되지 않았습니다.")
            else:
                st.warning("⚠️ 음성 변환할 텍스트가 없습니다.")
        else:
            st.warning("상황을 입력해주세요!")

# 탭 2: 실시간 녹음
with tab2:
    st.markdown("### 🎙️ 버튼을 눌러 직접 녹음해주세요")
    st.info("💡 아래 녹음 버튼을 눌러 시작하고, 다시 눌러 중지하세요")

    # 세션 상태 초기화
    if "processed_audio_hash" not in st.session_state:
        st.session_state.processed_audio_hash = None
    if "recording_result" not in st.session_state:
        st.session_state.recording_result = None

    # 실시간 녹음 (Streamlit 네이티브)
    audio_file = st.audio_input("🎙️ 녹음하기", key="audio_recorder")

    # audio_file을 bytes로 변환
    audio_bytes = audio_file.getvalue() if audio_file is not None else None

    if audio_bytes:
        # 오디오 해시 생성 (중복 처리 방지)
        audio_hash = hashlib.md5(audio_bytes).hexdigest()

        # 이미 처리한 오디오인지 확인
        if audio_hash != st.session_state.processed_audio_hash:
            st.success("✅ 녹음이 완료되었습니다!")

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
            if st.session_state.recording_result and len(st.session_state.recording_result.strip()) > 0:
                with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                    try:
                        # TTS를 위한 텍스트 정리 (이모지 제거)
                        clean_text = re.sub(r'[^\w\s가-힣.,!?。、\n]', '', st.session_state.recording_result)

                        if len(clean_text.strip()) < 5:
                            raise ValueError("텍스트가 너무 짧습니다")

                        tts = gTTS(text=clean_text, lang='ko', slow=False)
                        tts.save("response.mp3")

                        st.success("✅ 응답 음성이 준비되었습니다!")
                        st.info("💡 아래 버튼을 눌러 음성 파일을 다운로드한 후 재생하세요")

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
                        error_type = type(e).__name__
                        st.error(f"⚠️ 음성 변환 중 오류가 발생했습니다 ({error_type})")
                        st.info(f"상세 정보: {str(e)}")
                        st.info("💡 결과는 위에서 확인하실 수 있습니다. 음성 파일은 생성되지 않았습니다.")
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
# 탭 3: 음성 파일 업로드
with tab3:
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
            if st.session_state.upload_result and len(st.session_state.upload_result.strip()) > 0:
                with st.spinner("🔊 음성으로 말씀드리고 있어요..."):
                    try:
                        # TTS를 위한 텍스트 정리 (이모지 제거)
                        clean_text = re.sub(r'[^\w\s가-힣.,!?。、\n]', '', st.session_state.upload_result)

                        if len(clean_text.strip()) < 5:
                            raise ValueError("텍스트가 너무 짧습니다")

                        tts = gTTS(text=clean_text, lang='ko', slow=False)
                        tts.save("response.mp3")

                        st.success("✅ 응답 음성이 준비되었습니다!")
                        st.info("💡 아래 버튼을 눌러 음성 파일을 다운로드한 후 재생하세요")

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
                        error_type = type(e).__name__
                        st.error(f"⚠️ 음성 변환 중 오류가 발생했습니다 ({error_type})")
                        st.info(f"상세 정보: {str(e)}")
                        st.info("💡 결과는 위에서 확인하실 수 있습니다. 음성 파일은 생성되지 않았습니다.")
        else:
            # 이미 처리된 파일
            st.info("✅ 이미 분석이 완료되었습니다. 다른 파일을 업로드하거나 페이지를 새로고침해주세요.")

