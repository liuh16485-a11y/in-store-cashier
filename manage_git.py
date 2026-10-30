import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
target_dir = r'c:\文件\谷歌AI\老百姓\新店型'

def run(cmd):
    res = subprocess.run(cmd, cwd=target_dir, shell=True, capture_output=True, text=True)
    print(f'=== CMD: {cmd} ===')
    print('Return code:', res.returncode)
    if res.stdout:
        print('STDOUT:\n', res.stdout.strip())
    if res.stderr:
        print('STDERR:\n', res.stderr.strip())
    return res

run('git --version')
run('git status')
run('git remote -v')
