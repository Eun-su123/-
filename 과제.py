import streamlit as st
import pandas as pd
import os
import shutil
from datetime import datetime
import json
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="교사 포트폴리오 관리 시스템",
    page_icon="📚",
    layout="wide"
)

# 데이터 저장 경로
DATA_DIR = "teacher_data"
FILES_DIR = os.path.join(DATA_DIR, "files")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")

# 디렉토리 생성
os.makedirs(FILES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# 메타데이터 로드/저장 함수
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_metadata(metadata):
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

# 세션 상태 초기화
if 'metadata' not in st.session_state:
    st.session_state.metadata = load_metadata()

# 메인 타이틀
st.title("📚 교사 포트폴리오 관리 시스템")
st.markdown("**과목_학년군_영역_단원_차시별로 학습 자료를 체계적으로 관리하세요!**")

# 사이드바 - 필터링 옵션
st.sidebar.header("🔍 검색 및 필터")

# 과목 선택
subjects = ["국어", "수학", "사회", "과학", "영어", "체육", "음악", "미술", "도덕", "기타"]
selected_subject = st.sidebar.selectbox("과목", ["전체"] + subjects)

# 학년군 선택
grade_groups = ["1-2학년", "3-4학년", "5-6학년", "중학교", "고등학교"]
selected_grade = st.sidebar.selectbox("학년군", ["전체"] + grade_groups)

# 영역 선택
areas = ["듣기", "말하기", "읽기", "쓰기", "수와 연산", "도형", "측정", "자료와 가능성", "기타"]
selected_area = st.sidebar.selectbox("영역", ["전체"] + areas)

# 검색어
search_term = st.sidebar.text_input("검색어", placeholder="제목, 단원, 키워드로 검색...")

# 메인 컨텐츠
tab1, tab2, tab3 = st.tabs(["📁 자료 업로드", "📋 자료 목록", "📊 통계 및 분석"])

# 탭 1: 자료 업로드
with tab1:
    st.header("📁 새로운 학습 자료 업로드")
    
    with st.form("upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("과목", subjects, key="upload_subject")
            grade_group = st.selectbox("학년군", grade_groups, key="upload_grade")
            area = st.selectbox("영역", areas, key="upload_area")
            
        with col2:
            unit = st.text_input("단원", placeholder="예: 1. 소중한 우리")
            lesson = st.text_input("차시", placeholder="예: 1/4차시")
            title = st.text_input("자료 제목", placeholder="예: 소중한 우리 학습지")
        
        description = st.text_area("자료 설명", placeholder="자료에 대한 상세한 설명을 입력하세요...")
        keywords = st.text_input("키워드 (쉼표로 구분)", placeholder="예: 소중함, 가족, 감사")
        
        uploaded_file = st.file_uploader(
            "파일 업로드", 
            type=['pdf', 'docx', 'pptx', 'hwp', 'jpg', 'png', 'mp4', 'mp3'],
            help="PDF, Word, PowerPoint, 한글, 이미지, 동영상, 음성 파일을 업로드할 수 있습니다."
        )
        
        submitted = st.form_submit_button("📤 자료 업로드")
        
        if submitted and uploaded_file is not None:
            # 파일 정보 저장
            file_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
            file_path = os.path.join(FILES_DIR, file_id)
            
            # 파일 저장
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 메타데이터 생성
            file_metadata = {
                "id": file_id,
                "original_name": uploaded_file.name,
                "title": title,
                "subject": subject,
                "grade_group": grade_group,
                "area": area,
                "unit": unit,
                "lesson": lesson,
                "description": description,
                "keywords": [kw.strip() for kw in keywords.split(",") if kw.strip()],
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file_size": uploaded_file.size,
                "file_type": uploaded_file.type
            }
            
            # 메타데이터 저장
            st.session_state.metadata.append(file_metadata)
            save_metadata(st.session_state.metadata)
            
            st.success(f"✅ '{title}' 자료가 성공적으로 업로드되었습니다!")
            st.balloons()

# 탭 2: 자료 목록
with tab2:
    st.header("📋 학습 자료 목록")
    
    # 필터링된 데이터
    filtered_data = st.session_state.metadata.copy()
    
    # 필터 적용
    if selected_subject != "전체":
        filtered_data = [item for item in filtered_data if item['subject'] == selected_subject]
    
    if selected_grade != "전체":
        filtered_data = [item for item in filtered_data if item['grade_group'] == selected_grade]
    
    if selected_area != "전체":
        filtered_data = [item for item in filtered_data if item['area'] == selected_area]
    
    if search_term:
        filtered_data = [item for item in filtered_data if 
                        search_term.lower() in item['title'].lower() or 
                        search_term.lower() in item['unit'].lower() or 
                        search_term.lower() in item['description'].lower() or
                        any(search_term.lower() in kw.lower() for kw in item['keywords'])]
    
    # 결과 표시
    if filtered_data:
        st.write(f"**총 {len(filtered_data)}개의 자료를 찾았습니다.**")
        
        for i, item in enumerate(filtered_data):
            with st.expander(f"📄 {item['title']} ({item['subject']} {item['grade_group']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**과목:** {item['subject']}")
                    st.write(f"**학년군:** {item['grade_group']}")
                    st.write(f"**영역:** {item['area']}")
                    st.write(f"**단원:** {item['unit']}")
                    st.write(f"**차시:** {item['lesson']}")
                    st.write(f"**설명:** {item['description']}")
                    st.write(f"**키워드:** {', '.join(item['keywords'])}")
                    st.write(f"**업로드일:** {item['upload_date']}")
                
                with col2:
                    # 파일 다운로드 버튼
                    file_path = os.path.join(FILES_DIR, item['id'])
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="📥 다운로드",
                                data=f.read(),
                                file_name=item['original_name'],
                                mime=item['file_type']
                            )
                    
                    # 삭제 버튼
                    if st.button("🗑️ 삭제", key=f"delete_{i}"):
                        # 파일 삭제
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        # 메타데이터에서 제거
                        st.session_state.metadata.remove(item)
                        save_metadata(st.session_state.metadata)
                        st.rerun()
    else:
        st.info("📝 아직 업로드된 자료가 없습니다. '자료 업로드' 탭에서 첫 번째 자료를 업로드해보세요!")

# 탭 3: 통계 및 분석
with tab3:
    st.header("📊 학습 자료 통계")
    
    if st.session_state.metadata:
        # 기본 통계
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 자료 수", len(st.session_state.metadata))
        
        with col2:
            subjects_count = len(set(item['subject'] for item in st.session_state.metadata))
            st.metric("활용 과목 수", subjects_count)
        
        with col3:
            total_size = sum(item['file_size'] for item in st.session_state.metadata)
            st.metric("총 용량", f"{total_size / (1024*1024):.1f} MB")
        
        with col4:
            recent_uploads = len([item for item in st.session_state.metadata 
                                if datetime.strptime(item['upload_date'], "%Y-%m-%d %H:%M:%S").date() == datetime.now().date()])
            st.metric("오늘 업로드", recent_uploads)
        
        # 과목별 분포
        st.subheader("📈 과목별 자료 분포")
        subject_counts = pd.Series([item['subject'] for item in st.session_state.metadata]).value_counts()
        st.bar_chart(subject_counts)
        
        # 학년군별 분포
        st.subheader("📈 학년군별 자료 분포")
        grade_counts = pd.Series([item['grade_group'] for item in st.session_state.metadata]).value_counts()
        st.bar_chart(grade_counts)
        
        # 키워드 분석
        st.subheader("🔍 자주 사용되는 키워드")
        all_keywords = []
        for item in st.session_state.metadata:
            all_keywords.extend(item['keywords'])
        
        if all_keywords:
            keyword_counts = pd.Series(all_keywords).value_counts().head(10)
            st.bar_chart(keyword_counts)
        
        # 연계 추천 (간단한 키워드 기반)
        st.subheader("🔗 연계 추천")
        st.write("**동일한 키워드를 가진 다른 자료들:**")
        
        # 모든 키워드 수집
        keyword_to_files = {}
        for item in st.session_state.metadata:
            for keyword in item['keywords']:
                if keyword not in keyword_to_files:
                    keyword_to_files[keyword] = []
                keyword_to_files[keyword].append(item)
        
        # 키워드별 연계 자료 표시
        for keyword, files in keyword_to_files.items():
            if len(files) > 1:  # 2개 이상의 자료가 있는 키워드만
                with st.expander(f"🔑 '{keyword}' 키워드 ({len(files)}개 자료)"):
                    for file in files:
                        st.write(f"• {file['title']} ({file['subject']} {file['grade_group']})")
    else:
        st.info("📊 업로드된 자료가 있어야 통계를 볼 수 있습니다.")

# 푸터
st.markdown("---")
st.markdown("💡 **팁:** 키워드를 잘 설정하면 나중에 연계 자료를 쉽게 찾을 수 있어요!")




