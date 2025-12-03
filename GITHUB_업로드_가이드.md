# GitHub 업로드 가이드

## 📋 사전 준비

1. **GitHub 계정이 있어야 합니다**
   - https://github.com 에서 계정 생성

2. **Git이 설치되어 있어야 합니다**
   - https://git-scm.com/download/win 에서 다운로드
   - 설치 시 "Add Git to PATH" 옵션 체크

## 🚀 업로드 단계

### 1단계: GitHub에 새 저장소 만들기

1. GitHub에 로그인
2. 우측 상단 `+` 버튼 클릭 → `New repository`
3. 저장소 이름 입력 (예: `teacher-portfolio-system`)
4. `Public` 또는 `Private` 선택
5. `Create repository` 클릭
6. **중요**: README, .gitignore, license는 추가하지 마세요 (이미 있으므로)

### 2단계: 터미널에서 Git 명령어 실행

**Git Bash** 또는 **새 터미널**을 열고 다음 명령어를 순서대로 실행:

```bash
# 1. 프로젝트 폴더로 이동
cd "C:\Users\장은수\OneDrive\Desktop\앱프로그래밍"

# 2. Git 저장소 초기화
git init

# 3. 모든 파일 추가
git add .

# 4. 커밋 메시지 작성
git commit -m "교사 포트폴리오 관리 시스템 최종 버전"

# 5. GitHub 저장소 연결 (본인의 저장소 URL로 변경!)
git remote add origin https://github.com/사용자명/저장소명.git

# 6. 메인 브랜치 설정
git branch -M main

# 7. GitHub에 푸시
git push -u origin main
```

### 3단계: 인증

첫 푸시 시 GitHub 로그인을 요구할 수 있습니다:
- 사용자명: GitHub 사용자명
- 비밀번호: GitHub Personal Access Token (비밀번호가 아닙니다!)

**Personal Access Token 생성 방법:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. `Generate new token` 클릭
3. `repo` 권한 체크
4. 토큰 생성 후 복사해서 비밀번호 대신 사용

## ✅ 확인

GitHub 저장소 페이지를 새로고침하면 파일들이 업로드된 것을 확인할 수 있습니다!

## 🔄 이후 업데이트 방법

코드를 수정한 후 다시 업로드하려면:

```bash
git add .
git commit -m "업데이트 내용 설명"
git push
```

## 💡 문제 해결

### Git이 인식되지 않을 때
- 새 터미널을 열어보세요
- Git Bash를 사용해보세요
- Git이 PATH에 추가되었는지 확인하세요

### 푸시가 안 될 때
- GitHub 저장소 URL이 맞는지 확인하세요
- Personal Access Token을 사용하고 있는지 확인하세요
- 인터넷 연결을 확인하세요
