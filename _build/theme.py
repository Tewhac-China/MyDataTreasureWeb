# -*- coding: utf-8 -*-
"""MyDataTreasureWeb 门户构建 · 共享主题（CSS / JS）

所有页面必须保持「单文件自包含」：样式与脚本内联，不引用任何 CDN / 外部 font / fetch。
原因：入口页要支持**双击 file:// 直接打开**，任何 fetch/XHR/module 都会被浏览器 CORS 拦掉。
"""

BASE_CSS = r"""
*,*::before,*::after{box-sizing:border-box}
:root{
  --bg:#f4f6fb; --panel:#ffffff; --panel2:#f8fafc; --panel3:#eef1f8;
  --ink:#131a2b; --ink2:#4b5567; --ink3:#8a93a6;
  --line:rgba(19,26,43,.10); --line2:rgba(19,26,43,.06);
  --accent:#4f46e5; --accent2:#6366f1; --accent-soft:rgba(99,102,241,.10);
  --opinion:#6366f1; --kepu:#10b981;
  --c-text:#f59e0b; --c-hybrid:#0ea5e9; --c-visual:#ec4899;
  --r:16px; --r-sm:10px;
  /* 顶栏高度只在这里定义一次；页面外壳（.lib/.gal 高度、吸附位）一律引用它，
     不要再写像素魔数——历史上 49px 抄了三处，顶栏一变高就全部错位。 */
  --topH:52px;
  --sh1:0 1px 2px rgba(19,26,43,.06),0 1px 3px rgba(19,26,43,.04);
  --sh2:0 6px 24px -10px rgba(19,26,43,.20),0 2px 6px rgba(19,26,43,.05);
  --sh3:0 30px 70px -26px rgba(19,26,43,.42);
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  --mono:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;
}
html,body{margin:0;padding:0}
body{
  font-family:var(--font); color:var(--ink); background:var(--bg);
  background-image:
    radial-gradient(at 12% 4%,rgba(99,102,241,.10) 0,transparent 46%),
    radial-gradient(at 88% 0%,rgba(16,185,129,.08) 0,transparent 42%),
    radial-gradient(at 60% 100%,rgba(236,72,153,.06) 0,transparent 46%);
  background-attachment:fixed;
  -webkit-font-smoothing:antialiased; font-size:15px; line-height:1.65;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}
button,input,select{font:inherit; color:inherit}
::selection{background:rgba(99,102,241,.22)}
::-webkit-scrollbar{width:11px;height:11px}
::-webkit-scrollbar-thumb{background:rgba(19,26,43,.18);border-radius:8px;border:3px solid transparent;background-clip:content-box}
::-webkit-scrollbar-thumb:hover{background:rgba(19,26,43,.32);background-clip:content-box}
::-webkit-scrollbar-track{background:transparent}

/* ---------- 顶栏 ---------- */
.topbar{
  position:sticky; top:0; z-index:60; display:flex; flex-wrap:nowrap; align-items:center; gap:14px;
  height:var(--topH); padding:0 20px; background:rgba(255,255,255,.86); backdrop-filter:saturate(180%) blur(14px);
  border-bottom:1px solid var(--line); box-shadow:0 1px 0 rgba(255,255,255,.6) inset;
}
.brand{display:flex;align-items:center;gap:9px;font-weight:750;letter-spacing:.2px;white-space:nowrap}
.brand .gem{
  width:26px;height:26px;border-radius:9px;display:grid;place-items:center;color:#fff;font-size:14px;
  background:linear-gradient(135deg,#6366f1,#8b5cf6 55%,#ec4899); box-shadow:0 4px 12px -4px rgba(99,102,241,.7)
}
.brand small{font-weight:500;color:var(--ink3);font-size:12px;letter-spacing:.4px}
/* 导航宁可横向可滚，也不许 overflow:hidden 静默裁掉——实测 820px 宽会无声丢掉
   58% 的链接，560px 以下更是整条导航点不到，而页面不产生横向滚动，用户无从得知。 */
.tnav{display:flex;gap:2px;margin-left:6px;flex-wrap:nowrap;overflow-y:hidden;overflow-x:auto;scrollbar-width:thin;-webkit-overflow-scrolling:touch}
.tnav a{padding:6px 11px;border-radius:9px;color:var(--ink2);font-size:13.5px;white-space:nowrap}
.tnav a:hover{background:var(--accent-soft);color:var(--accent);text-decoration:none}
.tnav a.on{background:var(--accent-soft);color:var(--accent);font-weight:600}
.spacer{flex:1 1 auto;min-width:6px}

/* ---------- 窄屏自适应（三页共享；门户页原本一条 @media 都没有）---------- */
/* ≤900px 顶栏折成两行：品牌 + 检索/统计一行，导航独占一行横向可滚。
   此时顶栏不再吸附——两行的吸附栏会长期占掉手机屏的一成高度，把竖直空间
   让给内容更划算；文稿库侧栏因此可以直接吸附在 top:0，无需知道顶栏多高。 */
@media (max-width:900px){
  .topbar{position:static;height:auto;flex-wrap:wrap;align-content:center;gap:8px 12px;padding:9px 14px}
  .topbar .spacer{display:none}
  .topbar .muted{margin-left:auto}
  .brand{flex:0 0 auto}
  .field{min-width:0}
  .searchhost{flex:1 1 140px;min-width:0;order:2}
  .searchhost .field{width:100%;min-width:0}
  .tnav{order:3;flex:1 1 100%;margin-left:0;padding-bottom:0;scrollbar-width:none}
  .tnav::-webkit-scrollbar{display:none}
  /* 本机绝对路径、长英文标识这类不可断 token 不能把整页顶出横向滚动
     （WCAG 1.4.10 Reflow：窄屏不应需要横向滑动才能读到内容）*/
  .mono,.chip,.note code,code,.crumbs{overflow-wrap:anywhere;word-break:break-word}
  /* .chip 自带 white-space:nowrap，它会让上面那条 overflow-wrap 彻底失效。
     基础 .chip 规则在本块之后输出，同特异性会盖掉这里，故用 .chip.mono 提特异性。 */
  .chip.mono,.mono.chip{white-space:normal;overflow-wrap:anywhere}
}
@media (max-width:700px){
  /* 篇数/字数与英文副标题属装饰性信息；窄屏优先把顶栏压回两行，
     腾出横向空间让「品牌 + 检索框」能共处一行 */
  .topbar .muted{display:none}
  .brand small{display:none}
}

/* ---------- 通用控件 ---------- */
.field{
  display:flex;align-items:center;gap:8px;background:var(--panel);border:1px solid var(--line);
  border-radius:11px;padding:6px 11px;box-shadow:var(--sh1);min-width:220px
}
.field input{border:0;outline:0;background:transparent;flex:1;min-width:40px;padding:1px 0}
.field input::placeholder{color:var(--ink3)}
.field .kbd{
  font-family:var(--mono);font-size:10.5px;color:var(--ink3);border:1px solid var(--line);
  border-radius:5px;padding:1px 5px;background:var(--panel2)
}
.chip{
  display:inline-flex;align-items:center;gap:5px;padding:3px 9px;border-radius:999px;font-size:12px;
  border:1px solid var(--line);background:var(--panel);color:var(--ink2);cursor:pointer;white-space:nowrap
}
.chip:hover{border-color:rgba(99,102,241,.45);color:var(--accent)}
.chip.on{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}
.chip.ghost{cursor:default}
.chip.ghost:hover{border-color:var(--line);color:var(--ink2)}
.btn{
  display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:11px;border:1px solid var(--line);
  background:var(--panel);cursor:pointer;font-size:13.5px;font-weight:600;color:var(--ink2);box-shadow:var(--sh1)
}
.btn:hover{border-color:rgba(99,102,241,.5);color:var(--accent);text-decoration:none;transform:translateY(-1px)}
.btn.primary{background:linear-gradient(135deg,#4f46e5,#6366f1);border-color:transparent;color:#fff}
.btn.primary:hover{color:#fff;box-shadow:0 10px 24px -10px rgba(79,70,229,.9)}
.btn[disabled]{opacity:.45;cursor:not-allowed;transform:none}
.tag{display:inline-block;padding:1px 8px;border-radius:6px;font-size:11.5px;font-weight:600;line-height:1.7}
.tag.t-text{color:#8a5a00;background:rgba(245,158,11,.16)}
.tag.t-hybrid{color:#075985;background:rgba(14,165,233,.16)}
.tag.t-visual{color:#9d174d;background:rgba(236,72,153,.16)}
.tag.c-opinion{color:#3730a3;background:rgba(99,102,241,.15)}
.tag.c-kepu{color:#065f46;background:rgba(16,185,129,.16)}
.tag.c-archive{color:#92400e;background:rgba(245,158,11,.20)}
.tag.d-dual{color:#9a3412;background:rgba(251,146,60,.20)}
.muted{color:var(--ink3)}
.mono{font-family:var(--mono)}
.hl{background:linear-gradient(180deg,transparent 58%,rgba(250,204,21,.65) 58%);border-radius:2px}

/* ---------- 图表容器 ---------- */
.wrap{max-width:1280px;margin:0 auto;padding:26px 20px 70px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--sh2)}
.sect-title{display:flex;align-items:baseline;gap:10px;margin:34px 0 14px}
.sect-title h2{margin:0;font-size:19px;letter-spacing:.2px}
.sect-title p{margin:0;color:var(--ink3);font-size:13px}

/* ---------- 轻提示 ---------- */
.toast{
  position:fixed;left:50%;bottom:26px;transform:translate(-50%,14px);z-index:300;max-width:min(680px,92vw);
  background:rgba(17,22,38,.96);color:#eef1f8;border-radius:13px;padding:12px 16px;font-size:13.4px;line-height:1.7;
  box-shadow:var(--sh3);opacity:0;pointer-events:none;transition:opacity .2s,transform .2s
}
.toast.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
.toast code{font-family:var(--mono);font-size:12.4px;background:rgba(255,255,255,.14);padding:1px 6px;border-radius:5px}
.toast b{color:#fff}

/* ---------- 灯箱 ---------- */
.lb{
  position:fixed;inset:0;z-index:200;display:none;background:rgba(8,11,20,.9);backdrop-filter:blur(6px);
  padding:34px 26px
}
.lb.on{display:grid;grid-template-columns:1fr;grid-template-rows:auto 1fr auto;gap:12px}
.lb .lbtop{display:flex;align-items:center;gap:10px;color:#e7ebf5;font-size:13.5px}
.lb .lbtop .spacer{flex:1}
.lb img{max-width:100%;max-height:100%;margin:auto;display:block;border-radius:10px;box-shadow:var(--sh3);background:#000}
.lb .cap{color:#c9d2e3;font-size:13px;max-width:1100px;margin:0 auto;line-height:1.6}
.lb .cap b{color:#fff}
.lb .x,.lb .nav{
  border:1px solid rgba(255,255,255,.24);background:rgba(255,255,255,.08);color:#fff;border-radius:9px;
  padding:5px 11px;cursor:pointer;font-size:13px
}
.lb .x:hover,.lb .nav:hover{background:rgba(255,255,255,.2)}
.lb .nav[disabled]{opacity:.35;cursor:not-allowed}

/* ---------- Markdown 正文 ---------- */
.md{font-size:15.6px;line-height:1.82;color:#1b2233;word-wrap:break-word}
.md h1{font-size:26px;line-height:1.35;margin:0 0 14px;letter-spacing:-.2px}
.md h2{
  font-size:18.5px;margin:34px 0 12px;padding-left:11px;border-left:4px solid var(--accent2);line-height:1.4
}
.md h3{font-size:16.4px;margin:26px 0 9px;color:#2b3550}
.md h4{font-size:15px;margin:20px 0 7px;color:#374160}
.md p{margin:0 0 14px}
.md ul,.md ol{margin:0 0 15px;padding-left:24px}
.md li{margin:5px 0}
.md li::marker{color:var(--accent2)}
.md strong{color:#111827;font-weight:700}
.md blockquote{
  margin:0 0 16px;padding:11px 15px;border-left:3px solid rgba(99,102,241,.5);border-radius:0 10px 10px 0;
  background:var(--accent-soft);color:#3c4560;font-size:14.2px;line-height:1.75
}
.md blockquote a{word-break:break-all}
.md code{font-family:var(--mono);font-size:13px;background:var(--panel3);padding:1.5px 5px;border-radius:5px}
.md hr{border:0;border-top:1px solid var(--line);margin:26px 0}
.md img{max-width:100%;border-radius:9px;border:1px solid var(--line);background:#fff;cursor:zoom-in;display:block;margin:6px 0}
.md .tblwrap{overflow-x:auto;margin:0 0 18px;border:1px solid var(--line);border-radius:12px;background:var(--panel)}
.md table{border-collapse:collapse;width:100%;font-size:13.6px;min-width:520px}
.md th,.md td{border-bottom:1px solid var(--line2);padding:9px 12px;text-align:left;vertical-align:top;line-height:1.7}
.md thead th{background:var(--panel2);font-weight:700;color:#2b3550;white-space:nowrap;position:sticky;top:0}
.md tbody tr:last-child td{border-bottom:0}
.md tbody tr:hover{background:rgba(99,102,241,.035)}
.md td img{min-width:190px;max-width:300px}
"""

SHARED_JS = r"""
/* ===== 工具 ===== */
function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fmt(n){return String(n).replace(/\B(?=(\d{3})+(?!\d))/g,',')}
function debounce(fn,ms){var t;return function(){var a=arguments,c=this;clearTimeout(t);t=setTimeout(function(){fn.apply(c,a)},ms||160)}}
function kv(obj){return Object.keys(obj).map(function(k){return k+'='+encodeURIComponent(obj[k])}).join('&')}
function parseHash(){var h=location.hash.replace(/^#/,'');var o={};if(!h)return o;
  h.split('&').forEach(function(p){var i=p.indexOf('=');if(i<0)return;
    try{o[p.slice(0,i)]=decodeURIComponent(p.slice(i+1))}catch(e){o[p.slice(0,i)]=p.slice(i+1)}});return o}

/* ===== 极简 Markdown 渲染器（无依赖，够用于本库文稿） ===== */
var MD_STASH=[];
function mdInline(t){
  t=esc(t);
  /* 图片 */
  t=t.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g,function(m,a,p){
    return '\u0001I'+ (MD_STASH.push('<img class="mdimg" loading="lazy" src="'+p+'" alt="'+a+'">')-1) +'\u0001';});
  /* 链接（先抽出，避免正文裸链重复包裹） */
  t=t.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g,function(m,a,h){
    return '\u0001L'+(MD_STASH.push('<a href="'+h+'" target="_blank" rel="noopener">'+a+'</a>')-1)+'\u0001';});
  /* 裸链接 */
  t=t.replace(/(https?:\/\/[^\s<)）】]+)/g,function(u){
    return '\u0001U'+(MD_STASH.push('<a href="'+u+'" target="_blank" rel="noopener">'+u+'</a>')-1)+'\u0001';});
  t=t.replace(/`([^`]+)`/g,'<code>$1</code>');
  t=t.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
  t=t.replace(/(^|[^*\w])\*([^*\n]+)\*/g,'$1<em>$2</em>');
  t=t.replace(/&lt;br\s*\/?&gt;/gi,'<br>');
  t=t.replace(/&lt;(\/?(?:em|strong|code|sub|sup|b|i|br))\s*\/?&gt;/gi,'<$1>');
  t=t.replace(/\u0001([ILU])(\d+)\u0001/g,function(m,k,i){return MD_STASH[+i]});
  return t;
}
function isBlockStart(l){
  return /^\s*$/.test(l)||/^#{1,6}\s/.test(l)||/^\s*>\s?/.test(l)||/^\s*[-*+]\s+/.test(l)
    ||/^\s*\d+[.)]\s+/.test(l)||/^\s*\|/.test(l)||/^\s*([-*_])\s*\1\s*\1/.test(l);
}
function md2html(md){
  MD_STASH=[];
  var L=String(md||'').split(/\r?\n/),out=[],i=0,m;
  while(i<L.length){
    var l=L[i];
    if(/^\s*$/.test(l)){i++;continue}
    /* 表格：表头 + 分隔行 */
    if(/^\s*\|/.test(l)&&i+1<L.length&&/^\s*\|?[\s:|-]*-[\s:|-]*\|/.test(L[i+1])){
      var cells=function(s){return s.trim().replace(/^\||\|$/g,'').split('|').map(function(x){return mdInline(x.trim())})};
      var head=cells(l); i+=2; var rows=[];
      while(i<L.length&&/^\s*\|/.test(L[i])){rows.push(cells(L[i]));i++}
      out.push('<div class="tblwrap"><table><thead><tr>'+head.map(function(c){return '<th>'+c+'</th>'}).join('')
        +'</tr></thead><tbody>'+rows.map(function(r){return '<tr>'+r.map(function(c){return '<td>'+c+'</td>'}).join('')+'</tr>'}).join('')
        +'</tbody></table></div>');
      continue;
    }
    if((m=l.match(/^(#{1,6})\s+(.*)$/))){var lv=m[1].length;out.push('<h'+lv+'>'+mdInline(m[2])+'</h'+lv+'>');i++;continue}
    if(/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(l)){out.push('<hr>');i++;continue}
    if(/^\s*>\s?/.test(l)){var q=[];while(i<L.length&&/^\s*>\s?/.test(L[i])){q.push(L[i].replace(/^\s*>\s?/,''));i++}
      out.push('<blockquote>'+q.map(mdInline).join('<br>')+'</blockquote>');continue}
    if(/^\s*[-*+]\s+/.test(l)){var ul=[];while(i<L.length&&/^\s*[-*+]\s+/.test(L[i])){ul.push(L[i].replace(/^\s*[-*+]\s+/,''));i++}
      out.push('<ul>'+ul.map(function(x){return '<li>'+mdInline(x)+'</li>'}).join('')+'</ul>');continue}
    if(/^\s*\d+[.)]\s+/.test(l)){var ol=[];while(i<L.length&&/^\s*\d+[.)]\s+/.test(L[i])){ol.push(L[i].replace(/^\s*\d+[.)]\s+/,''));i++}
      out.push('<ol>'+ol.map(function(x){return '<li>'+mdInline(x)+'</li>'}).join('')+'</ol>');continue}
    var para=[];while(i<L.length&&!isBlockStart(L[i])){para.push(L[i]);i++}
    if(para.length)out.push('<p>'+para.map(mdInline).join('<br>')+'</p>'); else i++;
  }
  return out.join('\n');
}

/* ===== 轻提示 ===== */
var __toastT=null;
function toast(html,ms){
  var el=$('#toast');
  if(!el){el=document.createElement('div');el.id='toast';el.className='toast';document.body.appendChild(el)}
  el.innerHTML=html; el.classList.add('on');
  clearTimeout(__toastT); __toastT=setTimeout(function(){el.classList.remove('on')},ms||6200);
}

/* ===== 灯箱（含 ←/→ 翻页、Esc 关闭） ===== */
var LB={items:[],idx:0};
function lbInit(){
  if($('#lb'))return;
  var d=document.createElement('div');d.id='lb';d.className='lb';
  d.innerHTML='<div class="lbtop"><span id="lbTitle"></span><span class="spacer"></span>'
    +'<button class="nav" id="lbPrev">← 上一张</button><button class="nav" id="lbNext">下一张 →</button>'
    +'<span id="lbIdx" class="mono" style="opacity:.7"></span><button class="x" id="lbX">关闭 Esc</button></div>'
    +'<img id="lbImg" alt=""><div class="cap" id="lbCap"></div>';
  document.body.appendChild(d);
  $('#lbX').onclick=lbClose;
  $('#lbPrev').onclick=function(){lbGo(LB.idx-1)};
  $('#lbNext').onclick=function(){lbGo(LB.idx+1)};
  d.addEventListener('click',function(e){if(e.target===d)lbClose()});
  document.addEventListener('keydown',function(e){
    if(!$('#lb').classList.contains('on'))return;
    if(e.key==='Escape')lbClose(); else if(e.key==='ArrowLeft')lbGo(LB.idx-1); else if(e.key==='ArrowRight')lbGo(LB.idx+1);
  });
}
function lbOpen(items,idx,title){LB.items=items;lbInit();lbGo(idx,title)}
function lbGo(i,title){
  if(!LB.items.length)return;
  i=(i+LB.items.length)%LB.items.length;LB.idx=i;
  var it=LB.items[i];
  $('#lbImg').src=it.img; $('#lbTitle').textContent=title||it.title||'';
  $('#lbCap').innerHTML=(it.cap||''); $('#lbIdx').textContent=(i+1)+' / '+LB.items.length;
  $('#lbPrev').disabled=false; $('#lbNext').disabled=LB.items.length<2;
  $('#lb').classList.add('on');
}
function lbClose(){var d=$('#lb');if(d){d.classList.remove('on');$('#lbImg').src=''}}
function bindZoom(root,getItems,getTitle){
  (root||document).addEventListener('click',function(e){
    var im=e.target.closest('.mdimg, img[data-zoom]'); if(!im)return;
    var items=getItems(im); if(!items||!items.length)return;
    var idx=0; for(var i=0;i<items.length;i++){if(items[i].img===im.getAttribute('src')){idx=i;break}}
    lbOpen(items,idx,typeof getTitle==='function'?getTitle(im):'');
  },false);
}
"""
