import os
import sys
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
base_dir = r'c:\文件\谷歌AI\老百姓\新店型'

font_reg = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 24)
font_bold = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 28)
font_sub = ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc', 20)
font_tag = ImageFont.truetype(r'C:\Windows\Fonts\msyhbd.ttc', 18)

def make_dual_image(path1, title1, sub1, path2, title2, sub2, main_title, out_path):
    im1 = Image.open(path1)
    im2 = Image.open(path2)
    
    # Scale each to width 700 px
    target_w = 700
    target_h = int(im1.height * (target_w / im1.width))
    im1_s = im1.resize((target_w, target_h), Image.Resampling.LANCZOS)
    im2_s = im2.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    gap = 40
    padding = 30
    header_h = 90
    card_header_h = 70
    
    total_w = target_w * 2 + gap + padding * 2
    total_h = target_h + header_h + card_header_h + padding * 2
    
    canvas = Image.new('RGB', (total_w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Main outer border
    draw.rounded_rectangle([0, 0, total_w-1, total_h-1], radius=24, fill=(255, 255, 255), outline=(226, 232, 240), width=3)
    
    # Top banner
    draw.rounded_rectangle([padding, 24, padding + 150, 68], radius=10, fill=(0, 112, 192))
    draw.text((padding + 16, 33), "操作流转原型", font=font_tag, fill=(255, 255, 255))
    draw.text((padding + 170, 28), main_title, font=font_bold, fill=(15, 23, 42))
    draw.line([(padding, header_h), (total_w - padding, header_h)], fill=(226, 232, 240), width=2)
    
    # Card 1
    x1 = padding
    y_card = header_h + 15
    draw.rounded_rectangle([x1, y_card, x1 + target_w, y_card + card_header_h + target_h], radius=16, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((x1 + 20, y_card + 12), title1, font=font_bold, fill=(30, 41, 59))
    draw.text((x1 + 20, y_card + 42), sub1, font=font_sub, fill=(100, 116, 139))
    canvas.paste(im1_s, (x1, y_card + card_header_h))
    
    # Card 2
    x2 = x1 + target_w + gap
    draw.rounded_rectangle([x2, y_card, x2 + target_w, y_card + card_header_h + target_h], radius=16, fill=(248, 250, 252), outline=(203, 213, 225), width=2)
    draw.text((x2 + 20, y_card + 12), title2, font=font_bold, fill=(30, 41, 59))
    draw.text((x2 + 20, y_card + 42), sub2, font=font_sub, fill=(100, 116, 139))
    canvas.paste(im2_s, (x2, y_card + card_header_h))
    
    canvas.save(out_path, quality=95)
    print(f'Combined {os.path.basename(out_path)}: size={canvas.size}')

# 1. 节点 3.1 扫69码添品与批号选择
make_dual_image(
    os.path.join(base_dir, 'raw_3_1_scan.png'), '3.1 扫69码添品', '扫描商品条形码并识别商品信息',
    os.path.join(base_dir, 'raw_3_1_batch.png'), '3.1.1 选择批号', '半窗选择在库有效批次、库存并调节入车数量',
    '节点 3.1：扫69码添加商品 ──> 选择批号完整操作流转',
    os.path.join(base_dir, '节点3_1_扫69码添品与批号选择.png')
)

# 2. 节点 3.3 提取处方单与追溯码采集
make_dual_image(
    os.path.join(base_dir, 'raw_3_3_rx.png'), '3.3 提取处方单', '展示患者脱敏信息、诊断与处方药品清单',
    os.path.join(base_dir, 'raw_3_3_trace.png'), '3.3.1 1:1强采追溯码', '国家合规逐盒强采集（未采齐强拦截锁定结算）',
    '节点 3.3：提取处方单 ──> 采集追溯码完整操作流转',
    os.path.join(base_dir, '节点3_3_提取处方单与追溯码采集.png')
)

# 3. 节点 6.1 聚合收款与反扫
make_dual_image(
    os.path.join(base_dir, 'raw_6_1_qr.png'), '6.1 聚合收款模式', '展示聚合收款二维码，支持顾客微信/支付宝主扫',
    os.path.join(base_dir, 'raw_6_1_scan_customer.png'), '6.1.1 扫顾客付款码', '唤起后置摄像头反扫顾客付款码，秒级扣款出票',
    '节点 6.1：聚合收款 ──> 扫顾客付款码完成收款操作流转',
    os.path.join(base_dir, '节点6_1_聚合收款与反扫.png')
)

# Clean up temporary raw partial files
for raw_name in ['raw_3_1_scan.png', 'raw_3_1_batch.png', 'raw_3_3_rx.png', 'raw_3_3_trace.png', 'raw_6_1_qr.png', 'raw_6_1_scan_customer.png']:
    p = os.path.join(base_dir, raw_name)
    if os.path.exists(p):
        os.remove(p)

print('ALL LATEST SCREENSHOTS PROCESSED AND COMBINED SUCCESSFULLY!')
