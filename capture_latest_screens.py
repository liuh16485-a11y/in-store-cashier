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
out_dir = r'c:\文件\谷歌AI\老百姓\新店型'

proc = subprocess.Popen([
    edge_path,
    '--headless=new',
    '--remote-debugging-port=9222',
    f'--user-data-dir={temp_user_data}',
    '--disable-gpu',
    '--no-sandbox',
    '--window-size=1200,1050',
    '--force-device-scale-factor=2',
    'about:blank'
])

time.sleep(2)

try:
    with urllib.request.urlopen('http://localhost:9222/json') as resp:
        tabs = json.loads(resp.read().decode())
    
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
    rect = json.loads(res['result']['result']['value'])
    print('mobileWrapper rect:', rect)
    
    def capture_state(js_code, filename, sleep_time=0.4):
        send_cmd('Runtime.evaluate', {'expression': js_code})
        time.sleep(sleep_time)
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
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(img_bytes)
        im = Image.open(filepath)
        print(f'Captured {filename}: size={im.size}, bytes={len(img_bytes)}')
        return filepath

    # 1. 节点 1：进入店内收银工作台
    capture_state('''
        closeAllModals();
        switchPage('pageHome');
    ''', '节点1_进入店内收银.png')

    # 2. 节点 2：录入会员（输入会员号 + 左上角胶囊徽标）
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
        openKeypad('member');
        document.getElementById('keypadDisplay').innerText = '18510178068';
    ''', '节点2_录入会员.png')

    # 3.1 扫69码添品 - 批号选择抽屉
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
        openBatchModal();
    ''', 'raw_3_1_batch.png')

    # 3.1 扫69码添品 - 扫码扫描取景框
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
    ''', 'raw_3_1_scan.png')

    # 3.2 扫追溯码添加商品
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
        simulateScanTraceCode();
    ''', '节点3_2_扫追溯码添品.png', sleep_time=0.6)

    # 3.3 提取处方单
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
        openRxModal();
    ''', 'raw_3_3_rx.png')

    # 3.3.1 采集追溯码
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
        takePrescription(1);
    ''', 'raw_3_3_trace.png', sleep_time=0.6)

    # 4. 去收银（购物车抽屉）
    capture_state('''
        closeAllModals();
        switchPage('pageScan');
        openCartModal();
    ''', '节点4_去收银.png')

    # 5. 选择促销套餐（结算页）
    capture_state('''
        closeAllModals();
        goToCheckout();
        selectPayMethod('qr');
    ''', '节点5_选择促销套餐.png')

    # 6.1 聚合收款 - 二维码展示
    capture_state('''
        closeAllModals();
        goToCheckout();
        selectPayMethod('qr');
    ''', 'raw_6_1_qr.png')

    # 6.1.1 反扫顾客付款码
    capture_state('''
        closeAllModals();
        goToCheckout();
        confirmPayment();
    ''', 'raw_6_1_scan_customer.png', sleep_time=0.5)

    # 6.2 现金收款与找零
    capture_state('''
        closeAllModals();
        goToCheckout();
        selectPayMethod('cash');
        document.getElementById('cashReceived').value = '50';
        calcChange();
    ''', '节点6_2_现金收款与找零.png')

    # 6.3 会员储值卡扣款与 6 位密码鉴权
    capture_state('''
        closeAllModals();
        currentMember = { name: '赵**', phone: '18510178068', balance: 150.0 };
        updateMemberDisplay();
        goToCheckout();
        selectPayMethod('card');
        openPwdModal();
    ''', '节点6_3_会员储值卡支付.png', sleep_time=0.5)

    # 7. 收款完成与重置
    capture_state('''
        closeAllModals();
        showSuccessModal('聚合扫码收款', 42.9);
    ''', '节点7_收款完成与重置.png', sleep_time=0.5)

    ws.close()
    print('ALL RAW SCREENSHOTS CAPTURED FROM LATEST HTML!')

finally:
    proc.terminate()
