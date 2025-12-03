"""
GitHub 자동 푸시 스크립트
파일이 변경되면 자동으로 GitHub에 푸시합니다.
"""
import subprocess
import os
from datetime import datetime

def git_push():
    """변경사항을 GitHub에 푸시"""
    try:
        # Git 상태 확인
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.stdout.strip():
            # 변경사항이 있으면 커밋 및 푸시
            subprocess.run(['git', 'add', '.'], check=True)
            commit_message = f"자동 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            subprocess.run(['git', 'push'], check=True)
            print(f"✅ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - GitHub에 푸시 완료!")
            return True
        else:
            print("변경사항이 없습니다.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {e}")
        return False
    except FileNotFoundError:
        print("❌ Git이 설치되어 있지 않거나 PATH에 없습니다.")
        return False

if __name__ == "__main__":
    git_push()
