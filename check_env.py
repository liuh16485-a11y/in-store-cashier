import shutil
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

git_path = shutil.which('git')
print('git executable path:', git_path)
print('Current dir:', os.getcwd())
print('Subdirs in current dir:', os.listdir('.'))
