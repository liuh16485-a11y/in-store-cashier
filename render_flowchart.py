# -*- coding: utf-8 -*-
"""
Render a high-resolution, professional business flowchart image for Word PRD.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def draw_arrow(draw, start, end, color="#1890ff", width=3, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    
    # Arrowhead pointing towards end
    if x1 == x2: # vertical
        if y2 > y1: # down
            draw.polygon([(x2, y2), (x2 - arrow_size//2, y2 - arrow_size), (x2 + arrow_size//2, y2 - arrow_size)], fill=color)
        else: # up
            draw.polygon([(x2, y2), (x2 - arrow_size//2, y2 + arrow_size), (x2 + arrow_size//2, y2 + arrow_size)], fill=color)
    elif y1 == y2: # horizontal
        if x2 > x1: # right
            draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size//2), (x2 - arrow_size, y2 + arrow_size//2)], fill=color)
        else: # left
            draw.polygon([(x2, y2), (x2 + arrow_size, y2 - arrow_size//2), (x2 + arrow_size, y2 + arrow_size//2)], fill=color)

def draw_elbow_down(draw, start, end, color="#1890ff", width=3, arrow_size=10):
    """Draw line from start down, then horizontal, then down to end with arrow."""
    x1, y1 = start
    x2, y2 = end
    mid_y = y1 + (y2 - y1) // 2
    draw.line([(x1, y1), (x1, mid_y)], fill=color, width=width)
    draw.line([(x1, mid_y), (x2, mid_y)], fill=color, width=width)
    draw.line([(x2, mid_y), (x2, y2)], fill=color, width=width)
    draw_arrow(draw, (x2, y2 - arrow_size), (x2, y2), color, width, arrow_size)

def draw_flowchart():
    # 2x scale for crisp rendering
    width = 1600
    height = 2100
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_path_regular = r"C:\Windows\Fonts\msyh.ttc"
    font_path_bold = r"C:\Windows\Fonts\msyhbd.ttc"

    font_title = ImageFont.truetype(font_path_bold, 36)
    font_large_bold = ImageFont.truetype(font_path_bold, 28)
    font_med_bold = ImageFont.truetype(font_path_bold, 24)
    font_regular = ImageFont.truetype(font_path_regular, 22)
    font_small = ImageFont.truetype(font_path_regular, 20)

    center_x = width // 2

    # Draw diagram border container
    draw.rounded_rectangle([40, 30, width - 40, height - 30], radius=20, outline="#e8e8e8", width=2, fill="#fafbfc")

    # Diagram Header Banner
    draw.text((center_x, 70), "活力坐标移动收银 · 业务操作流转图", font=font_title, fill="#005090", anchor="mm")
    draw.line([(center_x - 300, 105), (center_x + 300, 105)], fill="#0070c0", width=3)

    # 1. Start Node: 1. 进入店内收银 (Pill)
    y1 = 160
    pill_w, pill_h = 420, 70
    box1 = [center_x - pill_w//2, y1, center_x + pill_w//2, y1 + pill_h]
    draw.rounded_rectangle(box1, radius=35, fill="#0070c0", outline="#004b87", width=3)
    draw.text((center_x, y1 + pill_h//2), "1. 进入店内收银", font=font_large_bold, fill="#ffffff", anchor="mm")

    # Arrow 1 -> 2
    draw_arrow(draw, (center_x, y1 + pill_h), (center_x, y1 + pill_h + 50), color="#1890ff", width=4)

    # 2. 录入会员 (Card)
    y2 = y1 + pill_h + 50
    card_w, card_h = 420, 64
    box2 = [center_x - card_w//2, y2, center_x + card_w//2, y2 + card_h]
    draw.rounded_rectangle(box2, radius=12, fill="#ffffff", outline="#1890ff", width=3)
    draw.text((center_x, y2 + card_h//2), "2. 录入会员", font=font_med_bold, fill="#003a8c", anchor="mm")

    # Arrow 2 -> 3
    draw_arrow(draw, (center_x, y2 + card_h), (center_x, y2 + card_h + 50), color="#1890ff", width=4)

    # 3. 添品方式 (Diamond / Card)
    y3 = y2 + card_h + 50
    box3 = [center_x - card_w//2, y3, center_x + card_w//2, y3 + card_h]
    draw.rounded_rectangle(box3, radius=12, fill="#e6f7ff", outline="#1890ff", width=3)
    draw.text((center_x, y3 + card_h//2), "3. 添品方式 (3条路径)", font=font_med_bold, fill="#003a8c", anchor="mm")

    # 3 Columns for 3.1, 3.2, 3.3
    col1_x = 280
    col2_x = center_x
    col3_x = width - 280

    sub_y = y3 + card_h + 70
    sub_w, sub_h = 360, 64

    # Connect from 3 to 3 columns
    branch_y = y3 + card_h + 35
    draw.line([(center_x, y3 + card_h), (center_x, branch_y)], fill="#1890ff", width=4)
    draw.line([(col1_x, branch_y), (col3_x, branch_y)], fill="#1890ff", width=4)
    draw_arrow(draw, (col1_x, branch_y), (col1_x, sub_y), color="#1890ff", width=4)
    draw_arrow(draw, (col2_x, branch_y), (col2_x, sub_y), color="#1890ff", width=4)
    draw_arrow(draw, (col3_x, branch_y), (col3_x, sub_y), color="#1890ff", width=4)

    # Branch labels
    draw.text((col1_x - 10, branch_y - 18), "3.1 扫69码", font=font_small, fill="#0050b3", anchor="rm")
    draw.text((col2_x + 12, branch_y + 18), "3.2 扫追溯码", font=font_small, fill="#0050b3", anchor="lm")
    draw.text((col3_x + 10, branch_y - 18), "3.3 提取处方单", font=font_small, fill="#0050b3", anchor="lm")

    # Col 1: 3.1 扫69码添加商品 -> 3.1.1 选择批号
    box3_1 = [col1_x - sub_w//2, sub_y, col1_x + sub_w//2, sub_y + sub_h]
    draw.rounded_rectangle(box3_1, radius=10, fill="#ffffff", outline="#91d5ff", width=2)
    draw.text((col1_x, sub_y + sub_h//2), "扫69码添加商品", font=font_regular, fill="#003a8c", anchor="mm")

    y_sub2 = sub_y + sub_h + 45
    draw_arrow(draw, (col1_x, sub_y + sub_h), (col1_x, y_sub2), color="#1890ff", width=3)
    box3_1_1 = [col1_x - sub_w//2, y_sub2, col1_x + sub_w//2, y_sub2 + sub_h]
    draw.rounded_rectangle(box3_1_1, radius=10, fill="#f0f7ff", outline="#69c0ff", width=2)
    draw.text((col1_x, y_sub2 + sub_h//2), "3.1.1 选择批号", font=font_med_bold, fill="#0050b3", anchor="mm")

    # Col 2: 3.2 扫追溯码添加商品
    box3_2 = [col2_x - sub_w//2, sub_y, col2_x + sub_w//2, sub_y + sub_h]
    draw.rounded_rectangle(box3_2, radius=10, fill="#ffffff", outline="#91d5ff", width=2)
    draw.text((col2_x, sub_y + sub_h//2), "扫追溯码添加商品", font=font_regular, fill="#003a8c", anchor="mm")

    # Col 3: 3.3 提取处方单 -> 3.3.1 采集追溯码
    box3_3 = [col3_x - sub_w//2, sub_y, col3_x + sub_w//2, sub_y + sub_h]
    draw.rounded_rectangle(box3_3, radius=10, fill="#ffffff", outline="#91d5ff", width=2)
    draw.text((col3_x, sub_y + sub_h//2), "提取处方单", font=font_regular, fill="#003a8c", anchor="mm")

    draw_arrow(draw, (col3_x, sub_y + sub_h), (col3_x, y_sub2), color="#1890ff", width=3)
    box3_3_1 = [col3_x - sub_w//2, y_sub2, col3_x + sub_w//2, y_sub2 + sub_h]
    draw.rounded_rectangle(box3_3_1, radius=10, fill="#f0f7ff", outline="#69c0ff", width=2)
    draw.text((col3_x, y_sub2 + sub_h//2), "3.3.1 采集追溯码", font=font_med_bold, fill="#0050b3", anchor="mm")

    # Convergence line to Step 4: 去收银
    y_conv1 = y_sub2 + sub_h + 40
    draw.line([(col1_x, y_sub2 + sub_h), (col1_x, y_conv1)], fill="#1890ff", width=3)
    draw.line([(col2_x, sub_y + sub_h), (col2_x, y_conv1)], fill="#1890ff", width=3)
    draw.line([(col3_x, y_sub2 + sub_h), (col3_x, y_conv1)], fill="#1890ff", width=3)
    draw.line([(col1_x, y_conv1), (col3_x, y_conv1)], fill="#1890ff", width=3)

    y4 = y_conv1 + 45
    draw_arrow(draw, (center_x, y_conv1), (center_x, y4), color="#1890ff", width=4)

    # 4. 去收银
    box4 = [center_x - card_w//2, y4, center_x + card_w//2, y4 + card_h]
    draw.rounded_rectangle(box4, radius=12, fill="#ffffff", outline="#1890ff", width=3)
    draw.text((center_x, y4 + card_h//2), "4. 去收银", font=font_med_bold, fill="#003a8c", anchor="mm")

    # Arrow 4 -> 5
    draw_arrow(draw, (center_x, y4 + card_h), (center_x, y4 + card_h + 45), color="#1890ff", width=4)

    # 5. 选择促销套餐
    y5 = y4 + card_h + 45
    box5 = [center_x - card_w//2, y5, center_x + card_w//2, y5 + card_h]
    draw.rounded_rectangle(box5, radius=12, fill="#ffffff", outline="#1890ff", width=3)
    draw.text((center_x, y5 + card_h//2), "5. 选择促销套餐 (默认首选立减¥30)", font=font_med_bold, fill="#003a8c", anchor="mm")

    # Arrow 5 -> 6
    draw_arrow(draw, (center_x, y5 + card_h), (center_x, y5 + card_h + 45), color="#1890ff", width=4)

    # 6. 选择支付方式
    y6 = y5 + card_h + 45
    box6 = [center_x - card_w//2, y6, center_x + card_w//2, y6 + card_h]
    draw.rounded_rectangle(box6, radius=12, fill="#fff7e6", outline="#fa8c16", width=3)
    draw.text((center_x, y6 + card_h//2), "6. 选择支付方式 (3种通道)", font=font_med_bold, fill="#873800", anchor="mm")

    # 3 Columns for 6.1, 6.2, 6.3
    pay_y = y6 + card_h + 70
    branch_y2 = y6 + card_h + 35
    draw.line([(center_x, y6 + card_h), (center_x, branch_y2)], fill="#fa8c16", width=4)
    draw.line([(col1_x, branch_y2), (col3_x, branch_y2)], fill="#fa8c16", width=4)
    draw_arrow(draw, (col1_x, branch_y2), (col1_x, pay_y), color="#fa8c16", width=4)
    draw_arrow(draw, (col2_x, branch_y2), (col2_x, pay_y), color="#fa8c16", width=4)
    draw_arrow(draw, (col3_x, branch_y2), (col3_x, pay_y), color="#fa8c16", width=4)

    draw.text((col1_x - 10, branch_y2 - 18), "6.1 聚合收款", font=font_small, fill="#873800", anchor="rm")
    draw.text((col2_x + 12, branch_y2 + 18), "6.2 现金", font=font_small, fill="#873800", anchor="lm")
    draw.text((col3_x + 10, branch_y2 - 18), "6.3 会员储值卡", font=font_small, fill="#873800", anchor="lm")

    # Col 1: 6.1 聚合收款: 唤起扫码摄像头 -> 6.1.1 扫顾客付款码完成收款
    box6_1 = [col1_x - sub_w//2, pay_y, col1_x + sub_w//2, pay_y + sub_h]
    draw.rounded_rectangle(box6_1, radius=10, fill="#ffffff", outline="#ffd591", width=2)
    draw.text((col1_x, pay_y + sub_h//2), "唤起扫码摄像头", font=font_regular, fill="#873800", anchor="mm")

    draw_arrow(draw, (col1_x, pay_y + sub_h), (col1_x, pay_y + sub_h + 45), color="#fa8c16", width=3)
    y_pay2 = pay_y + sub_h + 45
    box6_1_1 = [col1_x - sub_w//2, y_pay2, col1_x + sub_w//2, y_pay2 + sub_h]
    draw.rounded_rectangle(box6_1_1, radius=10, fill="#fffbe6", outline="#ffa940", width=2)
    draw.text((col1_x, y_pay2 + sub_h//2), "6.1.1 扫顾客付款码完成收款", font=font_med_bold, fill="#873800", anchor="mm")

    # Col 2: 6.2 现金: 填写支付金额
    box6_2 = [col2_x - sub_w//2, pay_y, col2_x + sub_w//2, pay_y + sub_h]
    draw.rounded_rectangle(box6_2, radius=10, fill="#ffffff", outline="#ffd591", width=2)
    draw.text((col2_x, pay_y + sub_h//2), "填写支付金额并找零", font=font_regular, fill="#873800", anchor="mm")

    # Col 3: 6.3 会员储值卡: 填写支付金额 -> 6.3.1 输入支付密码完成收款
    box6_3 = [col3_x - sub_w//2, pay_y, col3_x + sub_w//2, pay_y + sub_h]
    draw.rounded_rectangle(box6_3, radius=10, fill="#ffffff", outline="#ffd591", width=2)
    draw.text((col3_x, pay_y + sub_h//2), "填写扣款金额 (预填上限)", font=font_regular, fill="#873800", anchor="mm")

    draw_arrow(draw, (col3_x, pay_y + sub_h), (col3_x, y_pay2), color="#fa8c16", width=3)
    box6_3_1 = [col3_x - sub_w//2, y_pay2, col3_x + sub_w//2, y_pay2 + sub_h]
    draw.rounded_rectangle(box6_3_1, radius=10, fill="#fffbe6", outline="#ffa940", width=2)
    draw.text((col3_x, y_pay2 + sub_h//2), "6.3.1 输入支付密码完成收款", font=font_med_bold, fill="#873800", anchor="mm")

    # Convergence line to Step 7
    y_conv2 = y_pay2 + sub_h + 40
    draw.line([(col1_x, y_pay2 + sub_h), (col1_x, y_conv2)], fill="#fa8c16", width=3)
    draw.line([(col2_x, pay_y + sub_h), (col2_x, y_conv2)], fill="#fa8c16", width=3)
    draw.line([(col3_x, y_pay2 + sub_h), (col3_x, y_conv2)], fill="#fa8c16", width=3)
    draw.line([(col1_x, y_conv2), (col3_x, y_conv2)], fill="#fa8c16", width=3)

    y7 = y_conv2 + 45
    draw_arrow(draw, (center_x, y_conv2), (center_x, y7), color="#52c41a", width=4)

    # 7. 收款完成，重置回购物车页面 (Green Pill)
    pill7_w, pill7_h = 560, 72
    box7 = [center_x - pill7_w//2, y7, center_x + pill7_w//2, y7 + pill7_h]
    draw.rounded_rectangle(box7, radius=36, fill="#1b803a", outline="#0d5924", width=3)
    draw.text((center_x, y7 + pill7_h//2), "7. 收款完成，重置回购物车页面", font=font_large_bold, fill="#ffffff", anchor="mm")

    # Save
    out_img = r"c:\文件\谷歌AI\老百姓\新店型\业务流程图.png"
    img.save(out_img, "PNG", dpi=(200, 200))
    print("Flowchart image successfully rendered to:", out_img)

if __name__ == "__main__":
    draw_flowchart()
