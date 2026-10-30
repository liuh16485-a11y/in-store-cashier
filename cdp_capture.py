import subprocess
import time
import json
import urllib.request
import base64
import os
import websocket
from PIL import Image

edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
temp_user_data = r'C:\Users\HP\AppData\Local\Temp\edge_cdp_profile'
html_url = 'file:///C:/文件/谷歌AI/老百姓/新店型/手机端店内收银.html'

proc = subprocess.Popen([
    edge_path,
    '--headless=new',
    '--remote-debugging-port=9222',
    f'--user-data-dir={temp_user_data}',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1200,1050',
    '--force-device-scale-factor=2',
    html_url
])

time.sleep(2.5)

try:
    with urllib.request.urlopen('http://localhost:9222/json') as resp:
        tabs = json.loads(resp.read().decode())
    print('All tabs:', [(t.get('title'), t.get('url'), t.get('webSocketDebuggerUrl')) for t in tabs])
    
    # Target tab that has 手机端店内收银 or navigate to it
    page_tab = tabs[0]
    ws_url = page_tab['webSocketDebuggerUrl']
    ws = websocket.create_connection(ws_url, suppress_origin=True)
    
    msg_id = 1
    def send_cmd(method, params=None):
        global msg_id
        msg_id += 1
        payload = {'id': msg_id, 'method': method}
        if params:
            payload['params'] = params
        ws.send(json.dumps(payload))
        while True:
            resp = json.loads(ws.recv())
            if resp.get('id') == msg_id:
                return resp

    send_cmd('Page.enable')
    send_cmd('Page.navigate', {'url': html_url})
    time.sleep(1.5)
    
    # Hide top view-toolbar for clean mobile presentation
    send_cmd('Runtime.evaluate', {
        'expression': 'document.querySelector(".view-toolbar").style.display = "none";'
    })
    
    # Get rect of mobileWrapper
    res = send_cmd('Runtime.evaluate', {
        'expression': '''
            (function() {
                var r = document.getElementById("mobileWrapper").getBoundingClientRect();
                return JSON.stringify({x: r.left, y: r.top, width: r.width, height: r.height});
            })()
        ''',
        'returnByValue': True
    })
    print('Evaluate res:', res)
    rect = json.loads(res['result']['result']['value'])
    print('mobileWrapper rect:', rect)
    
    # Capture screenshot
    shot_res = send_cmd('Page.captureScreenshot', {
        'format': 'png',
        'clip': {
            'x': rect['x'],
            'y': rect['y'],
            'width': rect['width'],
            'height': rect['height'],
            'scale': 2
        }
    })
    img_bytes = base64.b64decode(shot_res['result']['data'])
    out_file = r'c:\文件\谷歌AI\老百姓\新店型\test_cdp_shot.png'
    with open(out_file, 'wb') as f:
        f.write(img_bytes)
    
    im = Image.open(out_file)
    print('SUCCESS! Test screenshot size:', im.size)
    ws.close()
finally:
    proc.terminate()
