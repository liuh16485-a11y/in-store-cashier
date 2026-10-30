import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')

clean_dir = r'c:\文件\谷歌AI\老百姓\新店型\screenshots_clean'
out_dir = r'c:\文件\谷歌AI\老百姓\新店型'

font_reg = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 15)
font_bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 17)
font_title = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 20)
font_sub = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 13)
font_small = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 12)

def frame_screen(im, title_text, subtitle_text=""):
    """Puts a single screen inside a clean mobile frame with card header."""
    target_w = 330
    target_h = int(im.height * (target_w / im.width))
    im_scaled = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    header_h = 52
    padding = 12
    card_w = target_w + padding * 2
    card_h = target_h + header_h + padding * 2
    
    canvas = Image.new('RGBA', (card_w, card_h), (255, 255, 255, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Outer rounded card
    draw.rounded_rectangle([0, 0, card_w-1, card_h-1], radius=14, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    
    # Header bar
    draw.rounded_rectangle([0, 0, card_w-1, header_h], radius=14, fill=(241, 245, 249))
    draw.rectangle([0, header_h-12, card_w-1, header_h], fill=(241, 245, 249))
    draw.line([(0, header_h), (card_w-1, header_h)], fill=(203, 213, 225), width=1)
    
    # Badge pill
    draw.rounded_rectangle([padding, 12, padding + 24, 38], radius=6, fill=(0, 112, 192))
    draw.text((padding + 7, 16), "UI", font=font_small, fill=(255, 255, 255))
    
    # Header text
    draw.text((padding + 34, 10), title_text, font=font_bold, fill=(15, 23, 42))
    if subtitle_text:
        draw.text((padding + 34, 30), subtitle_text, font=font_sub, fill=(100, 116, 139))
        
    # Paste phone screen
    canvas.paste(im_scaled, (padding, header_h + padding))
    # Border around screen
    draw.rounded_rectangle([padding, header_h + padding, padding + target_w, header_h + padding + target_h], radius=6, outline=(203, 213, 225), width=1)
    
    return canvas.convert('RGB')

def combine_two_screens(im1, title1, sub1, im2, title2, sub2, main_title, main_subtitle=""):
    """Combines two screens side by side into a dual-screen mockup card."""
    card1 = frame_screen(im1, title1, sub1)
    card2 = frame_screen(im2, title2, sub2)
    
    gap = 20
    top_bar = 54
    total_w = card1.width + card2.width + gap + 30
    total_h = max(card1.height, card2.height) + top_bar + 20
    
    canvas = Image.new('RGB', (total_w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Outer card
    draw.rounded_rectangle([0, 0, total_w-1, total_h-1], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    
    # Title
    draw.rounded_rectangle([15, 12, 100, 38], radius=6, fill=(0, 112, 192))
    draw.text((22, 16), "操作界面流转", font=font_small, fill=(255, 255, 255))
    draw.text((112, 14), main_title, font=font_title, fill=(15, 23, 42))
    if main_subtitle:
        draw.text((112, 36), main_subtitle, font=font_sub, fill=(100, 116, 139))
    draw.line([(15, top_bar), (total_w-15, top_bar)], fill=(226, 232, 240), width=1)
    
    # Paste cards
    canvas.paste(card1, (15, top_bar + 10))
    canvas.paste(card2, (15 + card1.width + gap, top_bar + 10))
    
    return canvas

def create_synthetic_phone_screen(screen_title, card_elements):
    """Creates a pixel-perfect mobile screen mock for specific nodes."""
    w, h = 330, 720
    im = Image.new('RGB', (w, h), (245, 247, 250))
    draw = ImageDraw.Draw(im)
    
    # Status bar
    draw.rectangle([0, 0, w, 36], fill=(0, 0, 0))
    draw.text((20, 10), "09:41", font=font_small, fill=(255, 255, 255))
    draw.text((w-55, 10), "5G  100%", font=font_small, fill=(255, 255, 255))
    
    # Navigation bar
    draw.rectangle([0, 36, w, 82], fill=(255, 255, 255))
    draw.line([(0, 82), (w, 82)], fill=(226, 232, 240), width=1)
    draw.text((16, 48), "‹", font=font_title, fill=(30, 41, 59))
    draw.text((45, 50), screen_title, font=font_bold, fill=(15, 23, 42))
    
    y = 94
    for elem in card_elements:
        elem_type = elem.get('type')
        if elem_type == 'card':
            title = elem.get('title', '')
            desc = elem.get('desc', '')
            tag = elem.get('tag', '')
            tag_color = elem.get('tag_color', (0, 112, 192))
            card_h = elem.get('height', 100)
            
            draw.rounded_rectangle([14, y, w-14, y + card_h], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
            if tag:
                draw.rounded_rectangle([26, y+14, 26 + len(tag)*14 + 12, y+34], radius=6, fill=tag_color)
                draw.text((32, y+17), tag, font=font_small, fill=(255, 255, 255))
                draw.text((26 + len(tag)*14 + 20, y+15), title, font=font_bold, fill=(15, 23, 42))
            else:
                draw.text((26, y+15), title, font=font_bold, fill=(15, 23, 42))
                
            if desc:
                draw.text((26, y+45), desc, font=font_sub, fill=(100, 116, 139))
            
            for line_idx, extra in enumerate(elem.get('extra_lines', [])):
                draw.text((26, y + 68 + line_idx*22), extra, font=font_sub, fill=(51, 65, 85))
            y += card_h + 12
            
        elif elem_type == 'button':
            btn_text = elem.get('text', '确定')
            btn_color = elem.get('color', (0, 159, 232))
            btn_h = elem.get('height', 44)
            draw.rounded_rectangle([14, y, w-14, y + btn_h], radius=8, fill=btn_color)
            tw = len(btn_text) * 16
            draw.text(((w - tw)//2, y + 12), btn_text, font=font_bold, fill=(255, 255, 255))
            y += btn_h + 12
            
        elif elem_type == 'dialog':
            diag_title = elem.get('title', '验证')
            diag_sub = elem.get('desc', '')
            diag_h = elem.get('height', 160)
            # Mask
            draw.rectangle([0, 82, w, h], fill=(0, 0, 0, 120))
            # Popup
            py = (h - diag_h) // 2
            draw.rounded_rectangle([25, py, w-25, py + diag_h], radius=14, fill=(255, 255, 255))
            draw.text((40, py + 18), diag_title, font=font_bold, fill=(15, 23, 42))
            draw.text((40, py + 45), diag_sub, font=font_sub, fill=(100, 116, 139))
            # 6-dot pin boxes
            box_w = 34
            box_gap = 10
            start_x = (w - (6 * box_w + 5 * box_gap)) // 2
            for i in range(6):
                bx = start_x + i * (box_w + box_gap)
                draw.rounded_rectangle([bx, py + 80, bx + box_w, py + 80 + 38], radius=6, outline=(203, 213, 225), width=1)
                if i < 4:
                    draw.ellipse([bx + 13, py + 95, bx + 21, py + 103], fill=(30, 41, 59))
            y = py + diag_h + 20
            
    return im

print('Building screenshot cards...')

# 1. 节点 1: 进入店内收银
im1_2 = Image.open(os.path.join(clean_dir, 'screen_1_2.png'))
card1 = frame_screen(im1_2, "节点 1：进入店内收银工作台", "冷启动初始态 · 购物车空置 · 默认禁用空单去收款")
card1.save(os.path.join(out_dir, "节点1_进入店内收银.png"))

# 2. 节点 2: 录入会员
im1_5 = Image.open(os.path.join(clean_dir, 'screen_1_5.png'))
card2 = frame_screen(im1_5, "节点 2：录入会员（九宫格输入）", "11位手机号识别鉴权 · 屏幕左上角常驻胶囊徽标")
card2.save(os.path.join(out_dir, "节点2_录入会员.png"))

# 3. 节点 3.1: 扫69码添加商品与选择批号
im1_4 = Image.open(os.path.join(clean_dir, 'screen_1_4.png'))
im1_6 = Image.open(os.path.join(clean_dir, 'screen_1_6.png'))
card3_1 = combine_two_screens(
    im1_4, "3.1 扫69码添品", "摄像头取景框识别商品条码",
    im1_6, "3.1.1 选择批号", "半窗选择在库有效批次/库存/调节数量",
    "节点 3.1：扫69码添加商品 ──> 选择批号",
    "标准流通药品扫码流转：扫码识别商品详情 ──> 勾选在库批号入车"
)
card3_1.save(os.path.join(out_dir, "节点3_1_扫69码添品与批号选择.png"))

# 4. 节点 3.2: 扫追溯码添加商品
screen3_2 = create_synthetic_phone_screen("扫码添品 - 国家追溯码", [
    {'type': 'card', 'tag': '追溯码直通', 'tag_color': (250, 140, 22), 'title': '8430 国家药品追溯码一键核验', 
     'desc': '已扫描国家 20 位药品一物一码追溯码', 
     'extra_lines': ['追溯码：84300298883275088608', '药品名称：阿莫西林胶囊 0.25g*24粒', '自动绑定在库批次：20260312 (库存 45 盒)'], 
     'height': 150},
    {'type': 'card', 'tag': '自动入车', 'tag_color': (52, 199, 89), 'title': '无需二次选批号，秒级自动入车', 
     'desc': '系统在线验真并锁定唯一实体码，核验合规通过', 
     'extra_lines': ['单价：¥19.80  |  数量：1 盒', '追溯码状态：已采集已核验 (1/1)'], 
     'height': 130},
    {'type': 'button', 'text': '完成添品，查看购物车 (1 件 ¥19.8)', 'color': (0, 159, 232), 'height': 46}
])
card3_2 = frame_screen(screen3_2, "节点 3.2：扫国家追溯码添加商品", "20位一物一码直通核验 · 自动关联批次入车 · 免二次选批")
card3_2.save(os.path.join(out_dir, "节点3_2_扫追溯码添品.png"))

# 5. 节点 3.3: 提取处方单与采集追溯码
screen3_3 = create_synthetic_phone_screen("电子处方单 - 提取与追溯码采集", [
    {'type': 'card', 'tag': '电子处方单', 'tag_color': (0, 112, 192), 'title': '顾客处方提取 (王*明 男·46岁)', 
     'desc': '联系电话：185****8068  |  科室：呼吸内科', 
     'extra_lines': ['处方诊断：急性支气管炎伴支原体感染', '处方单号：Rx20261029008892', '处方药品：磷酸奥司他韦颗粒 15mg*10袋 x2 盒'], 
     'height': 160},
    {'type': 'card', 'tag': '1:1强采集', 'tag_color': (250, 140, 22), 'title': '处方药品追溯码合规采集半窗', 
     'desc': '国家合规要求：处方药必须逐盒扫码，1:1采齐', 
     'extra_lines': ['[已采集] 84300298883275088608 (第 1/2 盒)', '[待采集] 请扫描第 2 盒国家追溯码...', '合规拦截：未采齐追溯码前锁定去收银通道'], 
     'height': 160},
    {'type': 'button', 'text': '📸 扫描第 2 盒追溯码 (进度 1/2)', 'color': (250, 140, 22), 'height': 46}
])
card3_3 = frame_screen(screen3_3, "节点 3.3：提取处方单 ──> 采集追溯码", "全流程强合规拦截 · 逐盒1:1逐一核对采集 · 采齐方可解锁收银")
card3_3.save(os.path.join(out_dir, "节点3_3_提取处方单与追溯码采集.png"))

# 6. 节点 4: 去收银
im2_1 = Image.open(os.path.join(clean_dir, 'screen_2_1.png'))
card4 = frame_screen(im2_1, "节点 4：购物车明细与去收银", "药品清单核验 · 数量步进调节 · 点击【去收款】通道解锁")
card4.save(os.path.join(out_dir, "节点4_去收银.png"))

# 7. 节点 5: 选择促销套餐
im2_2 = Image.open(os.path.join(clean_dir, 'screen_2_2.png'))
card5 = frame_screen(im2_2, "节点 5：选择促销套餐", "默认首选项优选立减 ¥30.0 · 支持单选切换/取消 · 应付金额实时扣减")
card5.save(os.path.join(out_dir, "节点5_选择促销套餐.png"))

# 8. 节点 6.1: 聚合收款与反扫
im2_5 = Image.open(os.path.join(clean_dir, 'screen_2_5.png'))
im2_6 = Image.open(os.path.join(clean_dir, 'screen_2_6.png'))
card6_1 = combine_two_screens(
    im2_5, "6.1 聚合收款模式", "展示聚合二维码，支持顾客主扫",
    im2_6, "6.1.1 扫付款码反扫", "唤起后置摄像头，对准顾客微信/支付宝条码",
    "节点 6.1：聚合收款 ──> 扫顾客付款码完成收款",
    "移动收银高频支付链路：聚合模式展示收款码 ──> 唤起摄像头对准顾客付款码秒级扣减出票"
)
card6_1.save(os.path.join(out_dir, "节点6_1_聚合收款与反扫.png"))

# 9. 节点 6.2: 现金收款与找零
im2_3 = Image.open(os.path.join(clean_dir, 'screen_2_3.png'))
card6_2 = frame_screen(im2_3, "节点 6.2：现金收款与找零", "填写实收现金金额 · 自动精准计算并大字提示找零")
card6_2.save(os.path.join(out_dir, "节点6_2_现金收款与找零.png"))

# 10. 节点 6.3: 会员储值卡支付
screen6_3 = create_synthetic_phone_screen("结算收银 - 会员储值卡支付", [
    {'type': 'card', 'tag': '储值账户', 'tag_color': (0, 112, 192), 'title': '会员储值卡账户信息', 
     'desc': '会员姓名：赵**  |  卡号：VIP880192', 
     'extra_lines': ['储值卡可用余额：¥150.00', '当前应付总额：¥42.90', '扣款金额：¥42.90 (自动填充可用上限)'], 
     'height': 140},
    {'type': 'dialog', 'title': '请输入会员支付密码', 'desc': '为保障资金安全，扣款 ¥42.90 请输入 6 位数字 PIN 码', 'height': 160},
    {'type': 'button', 'text': '确认扣款 ¥42.90', 'color': (52, 199, 89), 'height': 46}
])
card6_3 = frame_screen(screen6_3, "节点 6.3：会员储值卡 ──> 输入支付密码完成收款", "脱敏姓名余额展示 · 自动填充扣款限额 · 6位密码安全鉴权")
card6_3.save(os.path.join(out_dir, "节点6_3_会员储值卡支付.png"))

# 11. 节点 7: 收款完成，重置回购物车页面
im3_1 = Image.open(os.path.join(clean_dir, 'screen_3_1.png'))
card7 = frame_screen(im3_1, "节点 7：收款完成，重置回购物车页面", "生成18位收银流水单号 · 清空当前单据 · 自动重置回归收银主界面")
card7.save(os.path.join(out_dir, "节点7_收款完成与重置.png"))

print('ALL 11 SCREENSHOT ARTIFACTS CREATED SUCCESSFULLY!')
