"""
실시간 파일 동기화 및 GitHub 자동 푸시 스크립트
acid_alkaline.py가 변경되면 자동으로 최종_기말_과제.py로 복사하고 GitHub에 푸시합니다.
"""
import time
import shutil
import subprocess
import os
from datetime import datetime
from pathlib import Path

SOURCE_FILE = "acid_alkaline.py"
TARGET_FILE = "최종_기말_과제.py"
CHECK_INTERVAL = 2  # 2초마다 확인

def sync_file():
    """acid_alkaline.py를 최종_기말_과제.py로 복사"""
    if os.path.exists(SOURCE_FILE):
        try:
            shutil.copy2(SOURCE_FILE, TARGET_FILE)
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} - {SOURCE_FILE} → {TARGET_FILE} 복사 완료!")
            return True
        except Exception as e:
            print(f"❌ 파일 복사 오류: {e}")
            return False
    return False

def git_push():
    """변경사항을 GitHub에 푸시"""
    try:
        # Git 저장소인지 확인
        if not os.path.exists('.git'):
            print("⚠️ Git 저장소가 초기화되지 않았습니다. 'git init'을 먼저 실행하세요.")
            return False
        
        # 변경사항 확인
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.stdout.strip():
            # 변경사항이 있으면 커밋 및 푸시
            subprocess.run(['git', 'add', '.'], check=True)
            commit_message = f"자동 동기화: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            
            # remote가 설정되어 있는지 확인
            remote_check = subprocess.run(['git', 'remote', '-v'], 
                                        capture_output=True, text=True)
            if remote_check.stdout.strip():
                subprocess.run(['git', 'push'], check=True)
                print(f"🚀 GitHub에 푸시 완료!")
            else:
                print("⚠️ GitHub remote가 설정되지 않았습니다.")
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 오류: {e}")
        return False
    except FileNotFoundError:
        print("❌ Git이 설치되어 있지 않거나 PATH에 없습니다.")
        return False

def watch_and_sync():
    """파일 변경을 감지하고 자동으로 동기화"""
    last_modified = 0
    
    print("=" * 60)
    print("🔄 실시간 파일 동기화 시작!")
    print(f"📁 감시 파일: {SOURCE_FILE}")
    print(f"📁 대상 파일: {TARGET_FILE}")
    print("=" * 60)
    print("💡 Ctrl+C를 눌러 종료할 수 있습니다.\n")
    
    while True:
        try:
            if os.path.exists(SOURCE_FILE):
                current_modified = os.path.getmtime(SOURCE_FILE)
                
                # 파일이 수정되었는지 확인
                if current_modified > last_modified:
                    last_modified = current_modified
                    
                    # 파일 복사
                    if sync_file():
                        # GitHub에 푸시 (선택적)
                        time.sleep(1)  # 파일 쓰기 완료 대기
                        git_push()
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n👋 동기화를 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    watch_and_sync()
