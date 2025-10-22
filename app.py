import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('My First Streamlit App')

# CSS와 JavaScript를 추가하여 풍선 애니메이션 효과 만들기
st.markdown("""
<style>
.balloon {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 30px;
    transition: all 3s ease-out;
    z-index: 1000;
    opacity: 1;
}

.balloon.fly {
    bottom: 100vh;
    opacity: 0;
}

.balloon-container {
    position: relative;
    height: 200px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# 풍선 애니메이션을 위한 JavaScript
st.markdown("""
<script>
function createBalloon() {
    const balloon = document.createElement('div');
    balloon.className = 'balloon';
    balloon.innerHTML = '🎈';
    balloon.style.left = Math.random() * 80 + 10 + '%';
    document.body.appendChild(balloon);
    
    setTimeout(() => {
        balloon.classList.add('fly');
    }, 100);
    
    setTimeout(() => {
        balloon.remove();
    }, 3000);
}
</script>
""", unsafe_allow_html=True)

st.write('Here\'s our first attempt at using data to create a table.')
st.write(pd.DataFrame({
    'first column':[1, 2, 3, 4],
    'second column':[10, 20, 30, 40]
}))

# 곰돌이 효과를 위한 CSS 추가
st.markdown("""
<style>
.bear-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1000;
}

.bear {
    position: absolute;
    font-size: 40px;
    animation: bearFall 3s linear forwards;
    pointer-events: none;
}

@keyframes bearFall {
    0% {
        top: -50px;
        transform: rotate(0deg);
    }
    50% {
        transform: rotate(180deg);
    }
    100% {
        top: 100vh;
        transform: rotate(360deg);
    }
}

.bear-bounce {
    animation: bearBounce 0.5s ease-in-out;
}

@keyframes bearBounce {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.2); }
}
</style>
""", unsafe_allow_html=True)

# 곰돌이 생성 JavaScript
st.markdown("""
<script>
function createBears() {
    const bearContainer = document.createElement('div');
    bearContainer.className = 'bear-container';
    document.body.appendChild(bearContainer);
    
    // 여러 마리의 곰돌이 생성
    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            const bear = document.createElement('div');
            bear.className = 'bear';
            bear.innerHTML = '🐻';
            bear.style.left = Math.random() * 90 + 5 + '%';
            bear.style.animationDelay = Math.random() * 0.5 + 's';
            bearContainer.appendChild(bear);
        }, i * 100);
    }
    
    // 3초 후 곰돌이들 제거
    setTimeout(() => {
        bearContainer.remove();
    }, 4000);
}
</script>
""", unsafe_allow_html=True)

# 꿀 찾기 게임을 위한 세션 상태 초기화
if 'honey_found' not in st.session_state:
    st.session_state.honey_found = False
if 'honey_position' not in st.session_state:
    st.session_state.honey_position = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'clicked_cells' not in st.session_state:
    st.session_state.clicked_cells = []

# 꿀 찾기 게임 함수
def create_honey_game():
    import random
    st.session_state.honey_position = random.randint(1, 60)
    st.session_state.honey_found = False
    st.session_state.game_started = True
    st.session_state.clicked_cells = []

# 버튼들
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('🎈 풍선 날리기!', key='balloon_button'):
        st.balloons()
        st.success('풍선이 날아갔습니다! 🎈✨')

with col2:
    if st.button('🐻 곰돌이 대방출!', key='bear_button'):
        # 곰돌이 효과 JavaScript 실행
        st.markdown("""
        <script>
        createBears();
        </script>
        """, unsafe_allow_html=True)
        
        # 곰돌이 이모지로 채우기
        st.markdown("🐻 " * 20)
        st.markdown("🐻 " * 20)
        st.markdown("🐻 " * 20)
        
        st.success('곰돌이들이 쏟아졌습니다! 🐻🐻🐻')
        st.balloons()  # 추가 효과

with col3:
    if st.button('🍯 꿀 찾기 게임!', key='honey_button'):
        create_honey_game()
        st.success('곰돌이들 사이에 꿀이 숨어있어요! 찾아보세요! 🍯🐻')
        st.rerun()

# 꿀 찾기 게임
if st.session_state.game_started and st.session_state.honey_position is not None:
    st.markdown("### 🍯 꿀 찾기 게임")
    st.markdown("곰돌이들 사이에 숨어있는 꿀을 찾아보세요!")
    
    # 6x10 그리드로 곰돌이들 표시
    st.markdown("**곰돌이들을 클릭해서 꿀을 찾아보세요!**")
    
    # 그리드 생성
    for row in range(6):
        cols = st.columns(10)
        for col in range(10):
            cell_num = row * 10 + col + 1
            with cols[col]:
                if cell_num == st.session_state.honey_position:
                    if st.button('🍯', key=f'honey_{cell_num}', help='꿀을 찾았어요!'):
                        st.session_state.honey_found = True
                        st.session_state.game_started = False
                        st.rerun()
                else:
                    if st.button('🐻', key=f'bear_{cell_num}', help='곰돌이입니다'):
                        if cell_num not in st.session_state.clicked_cells:
                            st.session_state.clicked_cells.append(cell_num)
                            st.warning('곰돌이를 찾았어요! 꿀을 계속 찾아보세요! 🐻')
                            st.rerun()
                        else:
                            st.info('이미 확인한 곳이에요! 다른 곳을 찾아보세요!')

# 꿀을 찾았을 때의 칭찬 효과
if st.session_state.honey_found:
    st.markdown("---")
    st.markdown("## 🎉 축하합니다! 꿀을 찾았어요! 🍯✨")
    
    # 칭찬 메시지들
    praise_messages = [
        "와! 꿀을 찾았어요! 🍯✨",
        "대단해요! 곰돌이가 좋아할 거예요! 🐻💕", 
        "꿀을 찾는 실력이 최고예요! 🏆",
        "곰돌이들이 당신을 칭찬하고 있어요! 🐻👏",
        "꿀 찾기 마스터! 🍯🎉"
    ]
    
    import random
    selected_message = random.choice(praise_messages)
    st.success(f"**{selected_message}**")
    
    # 풍선 효과
    st.balloons()
    
    # 다시 게임하기 버튼
    if st.button('🔄 다시 게임하기', key='reset_game'):
        create_honey_game()
        st.rerun()
