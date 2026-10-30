import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
target_dir = r'c:\文件\谷歌AI\老百姓\新店型'
remote_url = 'https://github.com/liuh16485-a11y/in-store-cashier.git'

def run_git(args):
    cmd = ['git', '--no-pager'] + args
    print(f'Running: {" ".join(cmd)}')
    res = subprocess.run(cmd, cwd=target_dir, capture_output=True, text=True)
    if res.stdout:
        print('STDOUT:\n', res.stdout.strip())
    if res.stderr:
        print('STDERR:\n', res.stderr.strip())
    print('Exit code:', res.returncode)
    return res

# 1. Initialize git
run_git(['init'])

# 2. Config user
run_git(['config', 'user.name', 'liuh16485-a11y'])
run_git(['config', 'user.email', 'liuh16485-a11y@users.noreply.github.com'])

# 3. Rename branch to main
run_git(['branch', '-M', 'main'])

# 4. Set remote
run_git(['remote', 'remove', 'origin'])
run_git(['remote', 'add', 'origin', remote_url])

# 5. Add all files
run_git(['add', '-A'])

# 6. Commit
run_git(['commit', '-m', 'feat: 发布最新版店内移动收银系统与完整产品需求文档'])

# 7. Push
print('\n=== PUSHING TO GITHUB ===')
push_res = run_git(['push', '-u', 'origin', 'main', '--force'])
if push_res.returncode == 0:
    print('\n🎉 PUSH SUCCEEDED!')
else:
    print('\n❌ PUSH FAILED!')
