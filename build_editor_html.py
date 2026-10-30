# -*- coding: utf-8 -*-
import json
import os

md_path = r'c:\文件\谷歌AI\老百姓\新店型\店内收银产品需求文档_PRD.md'
out_path = r'c:\文件\谷歌AI\老百姓\新店型\店内收银产品需求文档_在线编辑.html'

with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>活力坐标移动收银 - PRD在线交互编辑器</title>
  <style>
    :root {
      --primary: #0070c0;
      --primary-hover: #005a9e;
      --bg-dark: #1e1e1e;
      --border: #e1e4e8;
      --text: #24292e;
      --success: #52c41a;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      height: 100vh;
      display: flex;
      flex-direction: column;
      background: #f8f9fa;
      color: var(--text);
      overflow: hidden;
    }
    .header-bar {
      height: 52px;
      background: #fff;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      flex-shrink: 0;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      z-index: 10;
    }
    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-badge {
      background: var(--primary);
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }
    .doc-title {
      font-size: 15px;
      font-weight: 600;
      color: #333;
    }
    .status-pill {
      font-size: 12px;
      color: #52c41a;
      background: #f6ffed;
      border: 1px solid #b7eb8f;
      padding: 2px 8px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .header-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn {
      padding: 6px 13px;
      font-size: 13px;
      font-weight: 500;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: #fff;
      color: #333;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn:hover { background: #f0f2f5; border-color: #c0c4cc; }
    .btn-primary {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }
    .btn-primary:hover {
      background: var(--primary-hover);
      border-color: var(--primary-hover);
    }
    .view-toggle-group {
      display: flex;
      border: 1px solid var(--border);
      border-radius: 6px;
      overflow: hidden;
    }
    .view-toggle-btn {
      border: none;
      padding: 6px 12px;
      font-size: 12px;
      background: #fff;
      cursor: pointer;
      color: #666;
    }
    .view-toggle-btn.active {
      background: var(--primary);
      color: #fff;
      font-weight: 600;
    }
    .workspace {
      flex: 1;
      display: flex;
      overflow: hidden;
    }
    .pane {
      flex: 1;
      height: 100%;\n      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .pane-header {
      height: 34px;
      background: #f1f3f6;
      border-bottom: 1px solid var(--border);
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      font-size: 12px;
      font-weight: 600;
      color: #666;
    }
    .editor-pane {
      border-right: 1px solid var(--border);
      background: #fff;
    }
    .md-textarea {
      flex: 1;
      width: 100%;
      border: none;
      outline: none;
      padding: 16px 20px;
      font-family: Consolas, "Fira Code", Monaco, monospace;
      font-size: 14px;
      line-height: 1.6;
      color: #24292e;
      background: #fff;
      resize: none;
      tab-size: 2;
    }
    .preview-pane {
      background: #fff;
    }
    .preview-content {
      flex: 1;
      padding: 24px 36px 60px;
      overflow-y: auto;
      font-size: 14.5px;
      line-height: 1.7;
      color: #2c3e50;
    }
    .preview-content h1 {
      font-size: 22px;
      font-weight: 700;
      color: #005090;
      border-bottom: 2px solid #e1e4e8;
      padding-bottom: 8px;
      margin: 20px 0 14px;
    }
    .preview-content h2 {
      font-size: 17px;
      font-weight: 600;
      color: #0070c0;
      border-bottom: 1px solid #eaecef;
      padding-bottom: 6px;
      margin: 18px 0 12px;
    }
    .preview-content h3 {
      font-size: 14.5px;
      font-weight: 600;
      color: #333;
      margin: 14px 0 8px;
    }
    .preview-content p {
      margin-bottom: 12px;
    }
    .preview-content ul, .preview-content ol {
      margin: 0 0 14px 24px;
    }
    .preview-content li {
      margin-bottom: 5px;
    }
    .preview-content blockquote {
      border-left: 4px solid #0070c0;
      background: #f4f8fb;
      padding: 10px 16px;
      margin: 12px 0;
      color: #555;
      border-radius: 0 6px 6px 0;
    }
    .preview-content table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 13.5px;
    }
    .preview-content th, .preview-content td {
      border: 1px solid #d0d7de;
      padding: 8px 12px;
      text-align: left;
    }
    .preview-content th {
      background: #f0f5fa;
      font-weight: 600;
      color: #004b87;
    }
    .preview-content tr:nth-child(even) td {
      background: #fafbfc;
    }
    .preview-content pre {
      background: #f6f8fa;
      border: 1px solid #e1e4e8;
      border-radius: 6px;
      padding: 14px;
      overflow-x: auto;
      margin: 12px 0;
      font-family: Consolas, Monaco, monospace;
      font-size: 13px;
      line-height: 1.5;
    }
    .preview-content code {
      background: #f0f2f5;
      padding: 2px 5px;
      border-radius: 3px;
      font-family: Consolas, Monaco, monospace;
      font-size: 12.5px;
      color: #d14;
    }
    .preview-content pre code {
      background: transparent;
      padding: 0;
      color: #24292e;
    }
    .toast {
      position: fixed;
      top: 65px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.85);
      color: #fff;
      padding: 8px 20px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 500;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s;
      z-index: 1000;
    }
    .toast.show { opacity: 1; }
  </style>
</head>
<body>
  <header class="header-bar">
    <div class="header-left">
      <span class="logo-badge">活力坐标 POS</span>
      <span class="doc-title">店内收银产品需求文档 (PRD) · 在线直接编辑</span>
      <span class="status-pill" id="saveStatusIndicator">● 本地已自动同步</span>
    </div>
    <div class="header-right">
      <div class="view-toggle-group">
        <button class="view-toggle-btn active" id="btnSplit" onclick="setViewMode('split')">左右分栏</button>
        <button class="view-toggle-btn" id="btnEdit" onclick="setViewMode('edit')">仅编辑</button>
        <button class="view-toggle-btn" id="btnPreview" onclick="setViewMode('preview')">仅预览</button>
      </div>
      <button class="btn" onclick="copyMarkdown()" title="复制全部Markdown源码">📋 复制源码</button>
      <button class="btn btn-primary" onclick="downloadMarkdown()" title="保存并下载 .md 文件到本地">💾 保存下载 MD</button>
      <button class="btn" onclick="openWordPrompt()" title="查看已生成的 Word 文档">📄 查看 Word 文档</button>
      <button class="btn" onclick="window.print()" title="打印或另存为 PDF">🖨️ 打印/PDF</button>
      <button class="btn" onclick="resetInitial()" style="color:#f5222d;" title="恢复为系统初始标准PRD">🔄 重置文档</button>
    </div>
  </header>

  <div class="workspace" id="workspace">
    <div class="pane editor-pane" id="editorPane">
      <div class="pane-header">
        <span>📝 MARKDOWN 源码实时编辑器 (支持键盘自由键入/修改)</span>
        <span id="charCountText">0 字符</span>
      </div>
      <textarea class="md-textarea" id="mdEditor" oninput="onEditorInput()" placeholder="在此直接编辑Markdown文本..."></textarea>
    </div>
    <div class="pane preview-pane" id="previewPane">
      <div class="pane-header">
        <span>👁️ 实时排版预览视口 (随左侧输入同步动态更新)</span>
        <span>可双击或滚动浏览</span>
      </div>
      <div class="preview-content" id="previewContent"></div>
    </div>
  </div>

  <div class="toast" id="toast">已同步保存</div>

  <script>
    const DEFAULT_MD = __DEFAULT_MD_JSON__;
    const STORAGE_KEY = "VITALITY_POS_PRD_MD_V1";
    const editor = document.getElementById("mdEditor");
    const preview = document.getElementById("previewContent");
    const charCount = document.getElementById("charCountText");
    const saveStatus = document.getElementById("saveStatusIndicator");

    function init() {
      const saved = localStorage.getItem(STORAGE_KEY);
      editor.value = saved || DEFAULT_MD;
      renderPreview();
    }

    function onEditorInput() {
      localStorage.setItem(STORAGE_KEY, editor.value);
      saveStatus.textContent = "● 已实时保存至浏览器缓存";
      saveStatus.style.color = "#52c41a";
      renderPreview();
    }

    function escapeHtml(str) {
      return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function renderMarkdown(md) {
      // 提取代码块
      const codeBlocks = [];
      let text = md.replace(/```([a-zA-Z0-9_-]*)\\n([\\s\\S]*?)```/g, function(match, lang, code) {
        const id = "CODEBLOCK_" + codeBlocks.length + "_PLACEHOLDER";
        codeBlocks.push('<pre><code class="language-' + lang + '">' + escapeHtml(code.trim()) + '</code></pre>');
        return id;
      });

      // 转义普通文本
      text = escapeHtml(text);

      // 行内代码
      text = text.replace(/`([^`]+)`/g, "<code>$1</code>");

      // 标题
      text = text.replace(/^### (.*$)/gim, "<h3>$1</h3>");
      text = text.replace(/^## (.*$)/gim, "<h2>$1</h2>");
      text = text.replace(/^# (.*$)/gim, "<h1>$1</h1>");

      // 粗体和斜体
      text = text.replace(/\\*\\*([^\\*]+)\\*\\*/g, "<strong>$1</strong>");
      text = text.replace(/\\*([^\\*]+)\\*/g, "<em>$1</em>");

      // 引用
      text = text.replace(/^\\> (.*$)/gim, "<blockquote>$1</blockquote>");

      // 列表
      text = text.replace(/^\\- (.*$)/gim, "<li>$1</li>");
      text = text.replace(/(<li>.*<\\/li>)/s, "<ul>$1</ul>");

      // 表格简易渲染
      const lines = text.split("\\n");
      let inTable = false;
      let tableHtml = "";
      let newLines = [];

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith("|") && line.endsWith("|")) {
          if (!inTable) {
            inTable = true;
            tableHtml = "<table>";
          }
          const cells = line.split("|").slice(1, -1).map(c => c.trim());
          if (cells.every(c => c.match(/^:?-+:?$/))) {
            continue;
          }
          const isHeader = !tableHtml.includes("<tr>");
          const tag = isHeader ? "th" : "td";
          tableHtml += "<tr>" + cells.map(c => "<" + tag + ">" + c + "</" + tag + ">").join("") + "</tr>";
        } else {
          if (inTable) {
            tableHtml += "</table>";
            newLines.push(tableHtml);
            inTable = false;
          }
          newLines.push(lines[i]);
        }
      }
      if (inTable) {
        tableHtml += "</table>";
        newLines.push(tableHtml);
      }
      text = newLines.join("\\n");

      // 段落换行
      text = text.replace(/\\n\\n+/g, "</p><p>");
      let res = "<p>" + text + "</p>";

      // 还原代码块
      codeBlocks.forEach(function(block, idx) {
        res = res.replace("CODEBLOCK_" + idx + "_PLACEHOLDER", block);
      });

      return res;
    }

    function renderPreview() {
      charCount.textContent = editor.value.length + " 字符";
      preview.innerHTML = renderMarkdown(editor.value);
    }

    function setViewMode(mode) {
      const editorPane = document.getElementById("editorPane");
      const previewPane = document.getElementById("previewPane");
      document.querySelectorAll(".view-toggle-btn").forEach(b => b.classList.remove("active"));

      if (mode === "split") {
        editorPane.style.display = "flex";
        previewPane.style.display = "flex";
        editorPane.style.flex = "1";
        previewPane.style.flex = "1";
        document.getElementById("btnSplit").classList.add("active");
      } else if (mode === "edit") {
        editorPane.style.display = "flex";
        previewPane.style.display = "none";
        editorPane.style.flex = "1";
        document.getElementById("btnEdit").classList.add("active");
      } else if (mode === "preview") {
        editorPane.style.display = "none";
        previewPane.style.display = "flex";
        previewPane.style.flex = "1";
        document.getElementById("btnPreview").classList.add("active");
      }
    }

    function showToast(msg) {
      const t = document.getElementById("toast");
      t.textContent = msg;
      t.classList.add("show");
      setTimeout(() => t.classList.remove("show"), 2000);
    }

    function copyMarkdown() {
      navigator.clipboard.writeText(editor.value).then(() => {
        showToast("已成功复制全部 Markdown 文本！");
      });
    }

    function downloadMarkdown() {
      const blob = new Blob([editor.value], { type: "text/markdown;charset=utf-8" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "店内收银产品需求文档_PRD.md";
      a.click();
      showToast("已触发保存最新【店内收银产品需求文档_PRD.md】！");
    }

    function openWordPrompt() {
      alert("Word 格式文档已在本地生成！文件名为：\\n【店内收银产品需求文档_PRD.docx】\\n\\n可直接双击使用 Microsoft Word 或 WPS Office 打开自由编辑。");
    }

    function resetInitial() {
      if (confirm("确定要将文档重置为系统初始标准 PRD 吗？")) {
        editor.value = DEFAULT_MD;
        localStorage.removeItem(STORAGE_KEY);
        renderPreview();
        showToast("已重置为初始标准 PRD！");
      }
    }

    window.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        localStorage.setItem(STORAGE_KEY, editor.value);
        showToast("已快捷保存至本地缓存！点击【保存下载 MD】可另存文件");
      }
    });

    init();
  </script>
</body>
</html>
"""

full_html = template.replace("__DEFAULT_MD_JSON__", json.dumps(md_content))

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print("Successfully written HTML editor to:", out_path)
