import streamlit as st

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="AI 산-염기 탐구 실험실",
    page_icon="🧪",
    layout="wide"
)

# --- 2. 앱 제목 및 설명 ---
st.title("🧪 AI 산-염기 탐구 실험실")
st.markdown("### 궁금한 용액을 AI와 함께 탐구해보고 산성인지 염기성인지 알아봅시다!")

# --- 3. 가상 실험실 화면 구성 ---
st.markdown("---")
st.header("🔬 활동: 가상 실험하기")

# st.image("images/lab_background.png") # TODO: 나중에 실험실 배경 이미지를 추가할 수 있습니다.

# 화면을 두 개로 분할 (왼쪽: 입력, 오른쪽: 결과)
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
    
    # '실험 시작' 버튼이 눌렸을 때
    if start_button:
        # 용액 이름이 입력되었는지 확인
        if not solution_name:
            st.warning("어떤 용액으로 실험할지 입력해주세요!")
        else:
            # 지금은 실제 로직 대신 간단한 메시지만 보여줍니다.
            st.info(f"'{solution_name}' 용액에 '{indicator}'(으)로 실험을 시작합니다!")
            st.write("결과가 여기에 표시될 예정입니다.")
            
            # TODO: 다음 단계에서 AI를 연동하여 실제 결과를 보여줄 예정입니다.

    else:
        st.info("왼쪽에서 실험할 용액을 입력하고 '실험 시작' 버튼을 눌러주세요.")