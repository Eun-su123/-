import streamlit as st
import time
import os
import json
from PIL import Image, ImageDraw
import google.generativeai as genai

# --- 이미지 생성 함수 ---
def create_images_if_needed():
    """필요한 이미지 파일이 없으면 생성합니다."""
    image_dir = "images"
    os.makedirs(image_dir, exist_ok=True)

    # 이미지 정보: 파일명, 배경색, 텍스트, 텍스트 색
    images_to_create = {
        "litmus_red.png": ("#FF5733", "붉게 변함", "white"),
        "litmus_blue.png": ("#335BFF", "푸르게 변함", "white"),
        "phenol_colorless.png": ("#E0E0E0", "변화 없음", "black"),
        "phenol_red.png": ("#FF33A1", "붉게 변함", "white"),
    }

    for filename, (color, text, text_color) in images_to_create.items():
        filepath = os.path.join(image_dir, filename)
        if not os.path.exists(filepath):
            img = Image.new('RGB', (200, 200), color=color)
            draw = ImageDraw.Draw(img)
            # 중앙에 텍스트 추가 (폰트 미지정으로 기본 폰트 사용)
            draw.text((50, 90), text, fill=text_color)
            img.save(filepath)

# --- 데이터 저장/로드 함수 ---
RESULTS_FILE = "results.json"

def load_results():
    """JSON 파일에서 실험 결과를 불러옵니다."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"산성": [], "염기성": []}

def save_results(results):
    """실험 결과를 JSON 파일에 저장합니다."""
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

# --- AI 모델 설정 함수 ---
def configure_ai():
    """API 키를 사용하여 Gemini 모델을 설정합니다."""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="당신은 초등학생을 위한 친절하고 이해하기 쉬운 과학 선생님입니다. 모든 답변은 한국어로, 존댓말로 작성해주세요."
        )
        return model
    except Exception as e:
        # st.secrets에 키가 없거나 잘못된 경우
        return None

# --- 1. 페이지 기본 설정 및 초기화 ---
st.set_page_config(
    page_title="AI 산-염기 탐구 실험실",
    page_icon="🧪",
    layout="wide"
)

# AI 모델 설정
ai_model = configure_ai()

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 세션 상태 초기화
if 'current_experiment' not in st.session_state:
    st.session_state.current_experiment = None

# 앱 실행 시 이미지 생성 함수 호출
create_images_if_needed()

# --- AI의 지식 데이터 (간단한 딕셔너리) ---
SOLUTION_DATA = {
    "레몬즙": "산성", "식초": "산성", "사이다": "산성", "탄산수": "산성", "염산": "산성",
    "비눗물": "염기성", "치약": "염기성", "유리세정제": "염기성", "수산화나트륨": "염기성", "석회수": "염기성",
    "물": "중성", "소금물": "중성"
}

# --- 2. 앱 제목 및 설명 ---
st.title("🧪 AI 산-염기 탐구 실험실")
st.markdown("### 궁금한 용액을 AI와 함께 탐구해보고 산성인지 염기성인지 알아봅시다!")

# --- 3. 가상 실험실 화면 구성 ---
st.header("🔬 활동: 가상 실험하기")

# 화면을 두 개로 분할 (왼쪽: 입력, 오른쪽: 결과)
st.markdown("---")
col1, col2 = st.columns([2, 1.5])

with col1:
    st.subheader("📋 실험 준비")
    
    # 1. 용액 이름 입력받기
    solution_name = st.text_input(
        "어떤 용액을 실험해볼까요?",
        placeholder="예: 레몬즙, 비눗물, 사이다"
    )

    # 2. 지시약 선택하기
    indicator = st.selectbox(
        "어떤 지시약을 사용하겠어요?",
        ("리트머스 종이", "페놀프탈레인 용액")
    )

    # 3. 실험 시작 버튼
    start_button = st.button("💧 실험 시작!")

with col2:
    st.subheader("📊 실험 결과")
    
    # 1. '실험 시작' 버튼을 눌렀을 때의 로직
    if start_button:
        if not solution_name:
            st.warning("어떤 용액으로 실험할지 입력해주세요!")
        else:
            with st.spinner(f"'{solution_name}' 용액으로 실험 중... 잠시만 기다려주세요..."):
                time.sleep(1.5) # 실험하는 것처럼 보이게 잠시 대기
            
            # 현재 실험 정보를 세션 상태에 저장
            st.session_state.current_experiment = {
                "name": solution_name,
                "indicator": indicator,
                "property": SOLUTION_DATA.get(solution_name, "알 수 없음")
            }

    # 2. 세션 상태에 저장된 실험 정보가 있으면 결과 표시
    if st.session_state.current_experiment:
        exp = st.session_state.current_experiment
        prop = exp["property"]
        
        st.success(f"'{exp['name']}' 실험 완료!")
        
        # 지시약과 용액 성질에 따라 결과 표시
        if exp["indicator"] == "리트머스 종이":
            if prop == "산성": st.image("images/litmus_red.png", caption="푸른색 리트머스 종이가 붉게 변했어요!")
            elif prop == "염기성": st.image("images/litmus_blue.png", caption="붉은색 리트머스 종이가 푸르게 변했어요!")
            elif prop == "중성": st.info("리트머스 종이의 색이 변하지 않았어요.")
            else: st.error("처음 보는 용액이라 결과를 알 수 없어요! 😥")
        
        elif exp["indicator"] == "페놀프탈레인 용액":
            if prop in ["산성", "중성"]: st.image("images/phenol_colorless.png", caption="페놀프탈레인 용액의 색이 변하지 않았어요.")
            elif prop == "염기성": st.image("images/phenol_red.png", caption="페놀프탈레인 용액이 붉게 변했어요!")
            else: st.error("처음 보는 용액이라 결과를 알 수 없어요! 😥")

        # 3. 학생의 판단 입력받기
        if prop != "알 수 없음":
            st.markdown("---")
            st.subheader("🤔 이 용액은 무엇일까요?")
            
            student_choice = st.radio(
                "실험 결과를 보고 용액의 성질을 선택해주세요.",
                ("산성", "염기성", "중성"), 
                key=f"choice_{exp['name']}" # 용액마다 다른 키를 부여
            )
            
            if st.button("결과 기록하기", key=f"submit_{exp['name']}"):
                if student_choice == prop:
                    st.success(f"정답이에요! '{exp['name']}'은(는) '{prop}'이 맞아요!")
                    st.balloons()
                    
                    # 결과 저장
                    results = load_results()
                    if prop in results and exp['name'] not in results[prop]:
                        results[prop].append(exp['name'])
                        save_results(results)
                        st.info("우리 반 실험 결과에 기록되었어요!")

                else:
                    st.error(f"아쉬워요. 이 용액은 '{prop}'이에요. 다시 한번 생각해볼까요?")
                
                # 현재 실험 초기화
                st.session_state.current_experiment = None
                time.sleep(2)
                st.rerun() # 화면 새로고침
    else:
        st.info("왼쪽에서 실험할 용액을 입력하고 '실험 시작' 버튼을 눌러주세요.")

# --- 4. 우리 반 전체 실험 결과 ---
st.markdown("---")
st.header("📊 우리 반 전체 실험 결과")

results = load_results()

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.subheader("🔴 산성 용액")
    st.dataframe(results["산성"], use_container_width=True)

with res_col2:
    st.subheader("🔵 염기성 용액")
    st.dataframe(results["염기성"], use_container_width=True)

# --- 5. AI 과학자에게 질문하기 ---
st.markdown("---")
st.header("👩‍🔬 AI 과학자에게 질문하기")

if ai_model:
    # 이전 대화 내용 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("과학에 대해 궁금한 점을 물어보세요! (예: 왜 비눗물은 미끌거려요?)"):
        # 사용자 메시지 기록 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI 응답 생성 및 표시
        with st.chat_message("assistant"):
            with st.spinner("AI 과학자 선생님이 답변을 생각하고 있어요..."):
                response = ai_model.generate_content(prompt)
                response_text = response.text
                st.markdown(response_text)
        
        # AI 응답 기록
        st.session_state.messages.append({"role": "assistant", "content": response_text})
else:
    st.warning("AI 모델을 불러올 수 없습니다. `.streamlit/secrets.toml` 파일에 API 키를 올바르게 설정했는지 확인해주세요.")