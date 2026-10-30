import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

def set_cell_background(cell, hex_color):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, hex_color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}>'
                        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
                        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
                        f'<w:left w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{hex_color}"/>'
                        f'<w:insideV w:val="none"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def build_prd_docx(output_path, base_dir):
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles helper
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0x00, 0x4B, 0x87) # Deep Blue
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(20)
        run = p.add_run(text)
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        return p

    def add_meta_info(data_dict):
        table = doc.add_table(rows=len(data_dict), cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, "E0E0E0")
        for i, (k, v) in enumerate(data_dict.items()):
            row = table.rows[i]
            row.cells[0].width = Inches(1.5)
            row.cells[1].width = Inches(5.0)
            
            p0 = row.cells[0].paragraphs[0]
            p0.add_run(k).bold = True
            p0.runs[0].font.size = Pt(10)
            p0.runs[0].font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            set_cell_background(row.cells[0], "F5F8FA")
            set_cell_margins(row.cells[0], 60, 60, 100, 100)
            
            p1 = row.cells[1].paragraphs[0]
            p1.add_run(v)
            p1.runs[0].font.size = Pt(10)
            p1.runs[0].font.color.rgb = RGBColor(0x44, 0x44, 0x44)
            set_cell_margins(row.cells[1], 60, 60, 100, 100)
        doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0x00, 0x56, 0x96)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x18, 0x90, 0xFF)
        return p

    def add_p(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.2
        if bold_prefix:
            r0 = p.add_run(bold_prefix)
            r0.bold = True
            r0.font.size = Pt(10.5)
            r0.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
        r = p.add_run(text)
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_bullet(text, level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        r = p.add_run(text)
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return p

    def add_figure(img_filename, caption_text, width=Inches(3.3)):
        img_full_path = os.path.join(base_dir, img_filename)
        if os.path.exists(img_full_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            p_img.paragraph_format.keep_with_next = True
            run_img = p_img.add_run()
            run_img.add_picture(img_full_path, width=width)

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.size = Pt(9)
            r_cap.font.color.rgb = RGBColor(0x55, 0x66, 0x77)
            r_cap.italic = True
            return p_img

    # --- Title & Cover ---
    add_title("活力坐标（Vitality Coordinates）移动收银系统")
    add_subtitle("产品需求规格说明书 (PRD - Product Requirement Document)")
    
    add_meta_info({
        "项目名称": "老百姓大药房“活力坐标”新店型移动收银系统",
        "文档版本": "V1.4（附全节点高保真原型操作截图）",
        "最新更新日期": "2026-10-30",
        "文档状态": "正式发布 (Release)",
        "责任人 / 产品经理": "产品设计与研发团队"
    })

    # 1. 文档概述
    add_h1("一、文档概述")
    add_h2("1.1 版本说明")
    
    ver_table = doc.add_table(rows=2, cols=4)
    ver_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(ver_table, "B0C4DE")
    
    headers = ["版本号", "更新日期", "修订状态", "主要修订内容与更新要点"]
    widths = [Inches(1.0), Inches(1.1), Inches(1.0), Inches(3.4)]
    
    for i, h in enumerate(headers):
        cell = ver_table.cell(0, i)
        cell.width = widths[i]
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(cell, "0070C0")
        set_cell_margins(cell, 80, 80, 100, 100)
    
    row1 = ver_table.rows[1]
    row1_data = [
        "V1.4", "2026-10-30", "当前最终版",
        "基于“活力坐标”店内移动收银核心链路构建完整规范：内嵌高清业务流程图与对应 7 步操作流转全套高保真操作界面原型截图；涵盖初始空置装载、会员身份智能路由与胶囊交互、扫69码选批入车、20位国家追溯码一键核验、电子处方突出患者/诊断与多单累加提单、处方药1:1逐盒强合规采集校验、促销套餐默认优选抵扣、聚合后置反扫顾客码、现金找零计算、储值卡自适应扣减及6位安全PIN鉴权等端到端全流程。"
    ]
    for i, d in enumerate(row1_data):
        cell = row1.cells[i]
        cell.width = widths[i]
        p = cell.paragraphs[0]
        p.add_run(d)
        p.runs[0].font.size = Pt(9.5)
        set_cell_margins(cell, 80, 80, 100, 100)
        if i in [0, 2]:
            p.runs[0].bold = True

    add_h2("1.2 产品定位")
    add_p("“活力坐标（Vitality Coordinates）移动智能收银系统”是面向智慧新零售药房手持端（PDA/手机）的一体化移动 POS。它深度融合了“货架旁移动收银”、“电子处方快捷核验”、“国家药品电子追溯码 100% 逐盒合规采集”与“会员储值卡便捷安全支付”，全面助力门店降本增效与合规运营。")

    # 2. 业务流程图
    add_h1("二、业务流程图（核心 7 步操作流转）")
    add_p("系统聚焦店内收银端到端的清晰主干操作链路，包含 7 大核心业务环节：")

    # 插入高保真流程图图片
    add_figure("业务流程图.png", "图 2-1 活力坐标店内移动收银端到端业务流转图", width=Inches(6.2))

    flow_table = doc.add_table(rows=8, cols=4)
    flow_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(flow_table, "C0D0E0")

    flow_headers = ["步骤编号", "流程步骤", "细分操作与业务流转说明", "对应原型截图"]
    flow_widths = [Inches(0.8), Inches(1.5), Inches(3.0), Inches(1.2)]

    for i, h in enumerate(flow_headers):
        cell = flow_table.cell(0, i)
        cell.width = flow_widths[i]
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(cell, "0070C0")
        set_cell_margins(cell, 80, 80, 100, 100)

    flow_rows = [
        ("1", "进入店内收银", "工作台初始为空置态，购物车 0 件、¥0.0，结算按钮灰阶禁用，会员态处于未绑定。", "图 3-1 初始工作台"),
        ("2", "录入会员", "键盘输入 11 位会员手机号，系统完成身份校验并在左上角常驻渲染 [👤 手机号] 胶囊徽标。", "图 3-2 会员录入"),
        ("3", "添品方式", "支持三种核心添药路径：\n• 3.1 扫69码添加商品 -> 3.1.1 选择批号：扫描条码唤起批号半窗，勾选有效批次入车；\n• 3.2 扫追溯码添加商品：一键识别 20 位国家码，秒级自动绑定批次入车；\n• 3.3 提取处方单 -> 3.3.1 采集追溯码：点击悬浮处方单提取单据，按处方药品盒数 1:1 逐盒扫齐追溯码。", "图 3-3 扫码选批\n图 3-4 追溯直通\n图 3-5 处方采集"),
        ("4", "去收银", "处方药采齐追溯码后解锁结算通道，点击底部【去收银】进入收银结算页面。", "图 3-6 购物车去收银"),
        ("5", "选择促销套餐", "结算页默认自动勾选第 1 项最优惠套餐（立减 ¥30.0），支持单选切换或取消，应付总额实时联动抵扣。", "图 3-7 促销套餐首选"),
        ("6", "选择支付方式", "提供三种支付渠道：\n• 6.1 聚合收款 -> 6.1.1 扫顾客付款码完成收款：唤起后置摄像头反扫顾客微信/支付宝条码；\n• 6.2 现金：输入实收现金数额，系统自动大字提示找零；\n• 6.3 会员储值卡 -> 6.3.1 输入支付密码，完成收款：填写扣款金额（自动填充可用上限），调起 6 位 PIN 码键盘鉴权扣款。", "图 3-8 聚合反扫\n图 3-9 现金找零\n图 3-10 储值卡PIN码"),
        ("7", "收款完成，重置回购物车页面", "扣款核销成功即刻生成 18 位收银流水号，系统自动清空购物车、重置已提处方状态并恢复促销首项优选，平滑切回购物车收银第一现场。", "图 3-11 结单与重置")
    ]
    for idx, (c1, c2, c3, c4) in enumerate(flow_rows):
        row = flow_table.rows[idx + 1]
        for col_idx, text in enumerate([c1, c2, c3, c4]):
            cell = row.cells[col_idx]
            cell.width = flow_widths[col_idx]
            p = cell.paragraphs[0]
            p.add_run(text)
            p.runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, 70, 70, 90, 90)
            if col_idx in [0, 1]:
                p.runs[0].bold = True

    # 3. 功能规格详述
    add_h1("三、功能规格详述（附各节点高保真操作界面截图）")
    
    # 3.1
    add_h2("3.1 工作台初始态与场景定位（对应节点 1）")
    add_bullet("场景模式：系统运行模式固定为“活力坐标”（Vitality Coordinates）标准移动收银模式。")
    add_bullet("初始清空原则：购物车商品数初始严格为 0，金额 ¥0.0，底部结算按钮置灰禁用（disabled），会员处于未绑定态。")
    add_bullet("全屏暗黑扫描视口：中央提供 2.4s 循环激光扫描线动效，右上角常驻手电筒补光按键。")
    add_figure("节点1_进入店内收银.png", "图 3-1 节点 1：进入店内收银工作台初始态界面", width=Inches(3.3))

    # 3.2
    add_h2("3.2 会员身份智能识别与胶囊交互（对应节点 2）")
    add_bullet("输入路由控制：店员在数字键盘输入 11 位手机号识别为会员，专门处理身份鉴权，不触发商品批号弹窗。")
    add_bullet("左上角会员胶囊徽标：录入成功后在左上角导航栏右侧常驻渲染 [👤 18510178068] 胶囊徽章，点击可展开会员抽屉查看脱敏姓名、储值卡余额并支持解绑。")
    add_bullet("支付面板动态联动：已录入会员时，结算页展示【会员储值卡】卡片；未录入会员时仅支持聚合收款和现金。")
    add_figure("节点2_录入会员.png", "图 3-2 节点 2：录入会员身份鉴权与九宫格输入操作界面", width=Inches(3.3))

    # 3.3
    add_h2("3.3 药品检索与国家追溯码一键核验（对应节点 3.1 & 3.2）")
    add_bullet("普通条码模式（节点 3.1）：扫入 69 码或键盘输入货号，弹出底部批号选择半窗，供店员核对效期、库存后调节数量添加入车。")
    add_figure("节点3_1_扫69码添品与批号选择.png", "图 3-3 节点 3.1：扫69码添加商品与选择批号完整操作流转", width=Inches(5.8))
    
    add_bullet("【📸 模拟扫追溯码】直通模式（节点 3.2）：数字键盘顶部挂载专属橙色胶囊按钮，点击模拟采集 8430 开头的 20 位国家药品一物一码追溯码；系统在线秒级验真并直接绑定在库唯一批次入车，免二次选批。")
    add_figure("节点3_2_扫追溯码添品.png", "图 3-4 节点 3.2：扫国家药品追溯码直通入车操作界面", width=Inches(3.3))

    # 3.4
    add_h2("3.4 电子处方单智能管理与追溯码 1:1 逐盒合规采集（对应节点 3.3）")
    add_bullet("悬浮入口：扫码页右下角常驻 [💊 处方单] 胶囊按钮，配有待提单数量角标。")
    add_bullet("处方卡片信息结构：首要识别区显著突出【顾客姓名】（加粗加大）、【性别·年龄】浅蓝胶囊、脱敏手机号及独占通栏【处方诊断】（如“急性支气管炎伴支原体感染”）高亮底框；处方单号与科室微缩沉底呈现。")
    add_bullet("多单累加提单：支持收银员连续提取多张处方单，所有处方药品合并累加进购物车合并结算。")
    add_bullet("1:1 逐盒强合规采集：处方提单后自动弹出采集半窗，按盒数逐盒采齐 20 位码；若未采齐，底部主收银按钮高亮橙色警告态并锁定结算通道直至全数采齐。")
    add_figure("节点3_3_提取处方单与追溯码采集.png", "图 3-5 节点 3.3：提取处方单与追溯码 1:1 逐盒强合规采集操作界面", width=Inches(3.3))

    # 3.5
    add_h2("3.5 购物车流转与去收银（对应节点 4）")
    add_bullet("底部购物车抽屉：展示品名、在库批号、追溯码摘要及处方药绿/橙合规状态徽章，支持 + / - 步进器增减及一键清空。")
    add_bullet("通道解锁机制：非处方药或处方药已足额采齐追溯码后，底部【去收银 ¥xx.x】按钮由灰阶禁用变为高亮激活，点击进入结算收银台。")
    add_figure("节点4_去收银.png", "图 3-6 节点 4：购物车明细核验与解锁去收银操作界面", width=Inches(3.3))

    # 3.6
    add_h2("3.6 促销套餐自动化首选机制（对应节点 5）")
    add_bullet("默认自动优选：进入结算页或开启新单时，系统默认勾选第 1 项最优惠套餐（开业盛典全能大礼包 A 立减 ¥30.0）。")
    add_bullet("金额实时联动：应付总额 = Max(0.1, 原价 - 折扣)，顶部待收金额与反扫码金额实时联动抵扣。")
    add_bullet("单选互斥控制：支持单选切换其他套餐或再次点击取消勾选。")
    add_figure("节点5_选择促销套餐.png", "图 3-7 节点 5：选择促销套餐与金额动态抵扣操作界面", width=Inches(3.3))

    # 3.7
    add_h2("3.7 多元支付结算与反扫闭环（对应节点 6）")
    add_bullet("聚合收款（反扫顾客付款码，节点 6.1）：点击【确认收款】唤起全屏摄像头扫码页，对准顾客微信/支付宝付款码条码反向扫码秒级扣款出票。")
    add_figure("节点6_1_聚合收款与反扫.png", "图 3-8 节点 6.1：聚合收款与反扫顾客付款码操作流转", width=Inches(5.8))
    
    add_bullet("现金支付（节点 6.2）：输入实收现金数额后，系统自动精准计算找零金额并大字清晰呈现。")
    add_figure("节点6_2_现金收款与找零.png", "图 3-9 节点 6.2：现金收款实收输入与找零计算操作界面", width=Inches(3.3))

    add_bullet("会员储值卡支付（节点 6.3）：面板清晰展示会员脱敏姓名（赵**）、储值卡可用余额（¥150.00）、扣款金额输入框；自动截断超额；点击扣款调起 6 位数字支付密码键盘进行安全鉴权。")
    add_figure("节点6_3_会员储值卡支付.png", "图 3-10 节点 6.3：会员储值卡扣款与 6 位安全 PIN 码鉴权操作界面", width=Inches(3.3))

    # 3.8
    add_h2("3.8 交易完成与下一单自动化重置（对应节点 7）")
    add_bullet("出票与凭据：结单完成弹出成功卡片，生成唯一的 18 位收银流水单号（898...）。")
    add_bullet("一键重置返回：点击【继续收款】主按钮后，系统自动清空购物车、清除已提处方单状态并恢复促销套餐首项默认勾选，平滑切回扫码收银第一现场，就绪下一单交易。")
    add_figure("节点7_收款完成与重置.png", "图 3-11 节点 7：收款完成凭据与一键重置返回购物车操作界面", width=Inches(3.3))

    # 4. 业务异常矩阵与防御策略
    add_h1("四、业务异常矩阵与防御策略")
    
    exc_table = doc.add_table(rows=7, cols=3)
    exc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(exc_table, "C0D0E0")

    exc_headers = ["业务异常场景 / 边界", "系统防御逻辑与机制", "前端用户感知与反馈"]
    exc_widths = [Inches(1.8), Inches(2.2), Inches(2.5)]

    for i, h in enumerate(exc_headers):
        cell = exc_table.cell(0, i)
        cell.width = exc_widths[i]
        p = cell.paragraphs[0]
        p.add_run(h).bold = True
        p.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_background(cell, "0070C0")
        set_cell_margins(cell, 80, 80, 100, 100)

    exc_rows = [
        ("处方药追溯码未采齐", "硬拦截结算通道，禁止发起去收银支付。", "底部按钮高亮橙色警告态“待采追溯码 (X/Y)”，点击强制唤起采集半窗。"),
        ("储值卡余额小于待收金额", "截断最高可用金额：Min(待付总额, 卡余额)。", "自动预填最大余额，输入超额实时 Toast 提示“扣款金额已自动设为可用上限”。"),
        ("现金实收金额不足", "严格判断【实收金额 < 应付总额】强制拦截。", "收款按钮禁用，Toast 提示“实收金额不足，请核对后重新录入”。"),
        ("未录入会员选储值卡", "支付方式网格中不渲染【会员储值卡】卡片。", "未绑定会员时界面不呈现会员卡卡片，仅支持聚合与现金。"),
        ("处方单重复提取", "处方列表在提单后标记为 PENDING 占用锁定态。", "列表中该单据呈禁用不可点状态，防止重复处方发药出库。"),
        ("空购物车去收款", "底部去收银按钮强行绑定 disabled 属性。", "按钮置灰不可点击，杜绝生成 0 元脏流水单据。")
    ]

    for idx, (c1, c2, c3) in enumerate(exc_rows):
        row = exc_table.rows[idx + 1]
        for col_idx, text in enumerate([c1, c2, c3]):
            cell = row.cells[col_idx]
            cell.width = exc_widths[col_idx]
            p = cell.paragraphs[0]
            p.add_run(text)
            p.runs[0].font.size = Pt(9.5)
            set_cell_margins(cell, 70, 70, 90, 90)
            if col_idx in [0, 1]:
                p.runs[0].bold = True

    try:
        doc.save(output_path)
        print(f"Document successfully created at {output_path}")
    except PermissionError:
        alt_path = output_path.replace(".docx", "_最新.docx")
        doc.save(alt_path)
        print(f"Warning: {output_path} is currently opened/locked by Word/WPS. Saved latest copy to {alt_path}")

if __name__ == '__main__':
    base_directory = os.path.abspath(r'c:\文件\谷歌AI\老百姓\新店型')
    output_docx = os.path.join(base_directory, '店内收银产品需求文档_PRD.docx')
    build_prd_docx(output_docx, base_directory)
