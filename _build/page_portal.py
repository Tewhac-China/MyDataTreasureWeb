# -*- coding: utf-8 -*-
"""入口门户页 index.html 的模板。"""

PAGE_CSS = r"""
.hero{padding:34px 0 6px}
.hero .kicker{
  display:inline-flex;align-items:center;gap:7px;font-size:12.5px;letter-spacing:.6px;text-transform:uppercase;
  color:var(--accent);background:var(--accent-soft);border:1px solid rgba(99,102,241,.20);
  padding:4px 11px;border-radius:999px;font-weight:700
}
.hero h1{
  margin:14px 0 10px;font-size:clamp(30px,4.6vw,46px);line-height:1.14;letter-spacing:-1.2px;font-weight:800;
  background:linear-gradient(120deg,#1e1b4b 0%,#4f46e5 42%,#7c3aed 66%,#db2777 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent
}
.hero .lead{margin:0;max-width:760px;color:var(--ink2);font-size:16px;line-height:1.8}
.hero .lead b{color:var(--ink);font-weight:700}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(126px,1fr));gap:10px;margin:24px 0 6px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:13px 15px;box-shadow:var(--sh1)}
.stat .v{font-size:23px;font-weight:800;letter-spacing:-.6px;line-height:1.2}
.stat .k{font-size:12px;color:var(--ink3);margin-top:3px}
.stat.acc .v{color:var(--accent)}
.stat.g .v{color:var(--kepu)}
.stat.a .v{color:#d97706}
.stat.s .v{color:#0284c7}

.grid{display:grid;gap:14px}
.g-apps{grid-template-columns:repeat(auto-fit,minmax(258px,1fr))}
.app{
  position:relative;display:flex;flex-direction:column;gap:9px;padding:19px 19px 16px;border-radius:var(--r);
  background:var(--panel);border:1px solid var(--line);box-shadow:var(--sh2);cursor:pointer;overflow:hidden;
  transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;text-decoration:none;color:inherit
}
.app::after{
  content:"";position:absolute;inset:0;border-radius:var(--r);pointer-events:none;
  background:radial-gradient(120% 90% at 100% 0%,rgba(99,102,241,.10),transparent 60%);opacity:0;transition:opacity .2s
}
.app:hover{transform:translateY(-3px);box-shadow:var(--sh3);border-color:rgba(99,102,241,.42);text-decoration:none}
.app:hover::after{opacity:1}
.app .ico{
  width:42px;height:42px;border-radius:13px;display:grid;place-items:center;font-size:20px;color:#fff;
  background:linear-gradient(135deg,#6366f1,#8b5cf6);box-shadow:0 8px 20px -9px rgba(99,102,241,.95)
}
.app.k2 .ico{background:linear-gradient(135deg,#10b981,#0ea5e9);box-shadow:0 8px 20px -9px rgba(16,185,129,.95)}
.app.k3 .ico{background:linear-gradient(135deg,#f59e0b,#ef4444);box-shadow:0 8px 20px -9px rgba(245,158,11,.95)}
.app.k4 .ico{background:linear-gradient(135deg,#ec4899,#8b5cf6);box-shadow:0 8px 20px -9px rgba(236,72,153,.95)}
.app h3{margin:2px 0 0;font-size:17px;letter-spacing:-.2px}
.app .sub{font-size:12.5px;color:var(--ink3)}
.app p{margin:0;font-size:13.4px;color:var(--ink2);line-height:1.7;flex:1}
.app .go{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:700;color:var(--accent);margin-top:2px}
.app .go span.arw{transition:transform .18s}
.app:hover .go span.arw{transform:translateX(4px)}
.app .warn{font-size:11.5px;color:#b45309;background:rgba(245,158,11,.12);border-radius:7px;padding:3px 8px;display:inline-block}

.cols{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.colcard{padding:17px 18px}
.colcard .hd{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.dot{width:10px;height:10px;border-radius:50%;flex:0 0 auto}
.colcard h3{margin:0;font-size:16px}
.colcard .n{margin-left:auto;font-size:12.5px;color:var(--ink3)}
.bar{display:flex;height:9px;border-radius:99px;overflow:hidden;background:var(--panel3);margin:10px 0 9px}
.bar i{display:block;height:100%}
.legend{display:flex;flex-wrap:wrap;gap:12px;font-size:12.3px;color:var(--ink2)}
.legend s{width:9px;height:9px;border-radius:3px;display:inline-block;margin-right:5px;text-decoration:none}
.kvrow{display:flex;flex-wrap:wrap;gap:8px;margin-top:11px}
.kvrow .chip{cursor:default;font-size:12px;background:var(--panel2)}
.kvrow .chip:hover{border-color:var(--line);color:var(--ink2)}

.dgrid{grid-template-columns:repeat(auto-fill,minmax(264px,1fr))}
.doc{
  padding:14px 15px;border-radius:14px;background:var(--panel);border:1px solid var(--line);box-shadow:var(--sh1);
  cursor:pointer;display:flex;flex-direction:column;gap:7px;transition:transform .16s,border-color .16s,box-shadow .16s;
  text-decoration:none;color:inherit
}
.doc:hover{transform:translateY(-2px);border-color:rgba(99,102,241,.4);box-shadow:var(--sh2);text-decoration:none}
.doc .t{font-weight:700;font-size:14.4px;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.doc .m{font-size:12.2px;color:var(--ink3);display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.doc .ex{font-size:12.8px;color:var(--ink2);line-height:1.68;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.filters{display:flex;gap:7px;flex-wrap:wrap;align-items:center;margin:0 0 13px}

.sugbox{
  position:absolute;top:calc(100% + 7px);right:0;width:min(560px,86vw);background:var(--panel);
  border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh3);padding:7px;display:none;z-index:90;
  max-height:66vh;overflow:auto
}
.sugbox.on{display:block}
.sug{display:flex;gap:10px;align-items:flex-start;padding:9px 10px;border-radius:10px;cursor:pointer}
.sug:hover,.sug.on{background:var(--accent-soft)}
.sug .st{font-weight:650;font-size:13.6px;line-height:1.5}
.sug .sm{font-size:11.8px;color:var(--ink3);margin-top:2px}
.sugbox .foot{padding:8px 10px;font-size:12.2px;color:var(--ink3);border-top:1px solid var(--line2);margin-top:5px}
.searchhost{position:relative}
/* 搜索框的尺寸只在桌面区间约束。写成无条件规则会盖过 theme.py 断点里的
   min-width:0（页面 CSS 在主题 CSS 之后输出），390px 上会把顶栏挤成三行。 */
@media (min-width:901px){
  .searchhost .field{min-width:220px;max-width:290px}
}

.note{padding:16px 18px;border-radius:var(--r);background:var(--panel);border:1px solid var(--line);box-shadow:var(--sh1);
  font-size:13.6px;color:var(--ink2);line-height:1.85}
.note h3{margin:0 0 8px;font-size:15px;color:var(--ink)}
.note ol{margin:0;padding-left:21px}
.note code{font-family:var(--mono);font-size:12.4px;background:var(--panel3);padding:1px 6px;border-radius:5px}
.note .warn{color:#b45309}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:14px}
footer{margin:44px 0 0;padding-top:18px;border-top:1px solid var(--line);font-size:12.6px;color:var(--ink3);
  display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center}
"""

PAGE_JS = r"""
var CORE=window.__CORE__||{docs:[],stats:{},cols:{},apps:[],projects:[]};
var TYPE_CN={text:'文本型',hybrid:'混合型',visual:'画面型'};
/* 合集配色表：收藏夹 + 主动归档 + 各额外来源，用于标签着色 */
var COLMAP={};
(function(){var c=CORE.cols||{},s=CORE.srcCols||[];
  Object.keys(c).forEach(function(k){COLMAP[k]={name:c[k].name,color:c[k].color}});
  s.forEach(function(x){COLMAP[x.key]={name:x.name,color:x.color}});})();
function tagType(t){return '<span class="tag t-'+t+'">'+(TYPE_CN[t]||t)+'</span>'}
function tagColl(n){var m=COLMAP[n.coll]||{};var col=m.color||'#6366f1';
  return '<span class="tag" style="color:'+col+';background:'+col+'22">'+esc(n.collName||n.coll)+'</span>'}
function tagDual(d){return (d.dual&&d.dual.length>1)?'<span class="tag d-dual" title="'+esc(d.dual.join(' + '))+'">双库</span>':''}

function renderStats(){
  var s=CORE.stats,box=$('#stats');if(!box)return;
  var items=[['收藏夹文稿',fmt(s.docsFav||s.docs),'篇整理稿','acc']];
  if(s.kf)items.push(['关键帧',fmt(s.kf),'张 VLM 判读','g']);
  if(s.arch)items.push(['主动归档',fmt(s.arch),'篇投放文稿','a']);
  if(s.src)items.push(['UP主全转录',fmt(s.src),'篇批量稿','s']);
  items=items.concat([
    ['概念/实体',fmt(s.entities),'个',''],
    ['关联边',fmt(s.edges),'条',''],
    ['总字数',((s.charsAll||s.chars)/10000).toFixed(1),'万字',''],
    ['UP主',fmt(s.uppers),'位','']
  ]);
  box.innerHTML=items.map(function(x){
    return '<div class="stat '+x[3]+'"><div class="v">'+x[1]+'</div><div class="k">'+x[0]+' · '+x[2]+'</div></div>'
  }).join('');
}

function renderApps(){
  var box=$('#apps');if(!box)return;
  box.innerHTML=CORE.apps.map(function(a,i){
    var chips=(a.chips||[]).map(function(c){return '<span class="chip ghost">'+esc(c)+'</span>'}).join('');
    return '<a class="app k'+((i%4)+1)+'" href="'+a.href+'"'+(a.server?' data-server="1"':'')+'>'
      +'<div class="ico">'+a.icon+'</div>'
      +'<h3>'+esc(a.title)+'</h3><div class="sub">'+esc(a.sub||'')+'</div>'
      +'<p>'+a.desc+'</p>'
      +(chips?'<div class="kvrow" style="margin:0">'+chips+'</div>':'')
      +(a.server?'<div><span class="warn">需先双击「启动本地服务.bat」（浏览器不允许 file:// 读取 JSON）</span></div>':'')
      +'<div class="go">'+(a.server?'查看启动说明':'进入')+' <span class="arw">→</span></div></a>';
  }).join('');
  $$('.app[data-server]').forEach(function(el){
    el.addEventListener('click',function(e){
      e.preventDefault();
      toast('<b>这一页需要本地服务</b><br>它要读取 <code>graph/data.json</code>，浏览器禁止 <code>file://</code> 页面发起这种请求。'
        +'请双击根目录的 <code>启动本地服务.bat</code>，再访问 <code>http://localhost:8777/projects/bilibili-kb/graph/'
        +el.getAttribute('href').split('/').pop()+'</code>。<br>'
        +'（纯浏览文稿 / 关键帧 / 网图浏览器都不受影响，可直接双击打开。）',9000);
    });
  });
}

function renderCols(){
  var box=$('#cols');if(!box)return;
  var ks=Object.keys(CORE.cols);
  box.innerHTML=ks.map(function(k){
    var c=CORE.cols[k],t=c.type||{};
    var label={text:'文本型',hybrid:'混合型',visual:'画面型'};
    var colors={text:'var(--c-text)',hybrid:'var(--c-hybrid)',visual:'var(--c-visual)'};
    var order=['text','hybrid','visual'],tot=0;
    order.forEach(function(o){tot+=(t[o]||0)});
    var bar=order.map(function(o){var v=t[o]||0;if(!v)return '';
      return '<i style="width:'+(v/Math.max(tot,1)*100).toFixed(1)+'%;background:'+colors[o]+'"></i>'}).join('');
    var leg=order.map(function(o){var v=t[o]||0;
      return '<span><s style="background:'+colors[o]+'"></s>'+label[o]+' '+v+' 篇</span>'}).join('');
    var mid=(c.n>0)
      ? '<div class="bar">'+bar+'</div><div class="legend">'+leg+'</div>'
      : '<div class="muted" style="font-size:13px;margin:10px 0 4px">还没有文稿 —— 把整理好的 <code>.md</code> 放进 '
        +'<code>主动归档/</code>，重跑一次生成器就会出现在这里。</div>';
    return '<div class="card colcard"><div class="hd">'
      +'<span class="dot" style="background:'+c.color+'"></span><h3>'+esc(c.name)+'</h3>'
      +'<span class="n">'+c.n+' 篇 · 约 '+(c.chars/10000).toFixed(1)+' 万字</span></div>'
      +mid
      +'<div class="kvrow"><span class="chip ghost">'+(k==='archive'?'本地图片 ':'关键帧 ')+c.kf+' 张</span>'
      +(k==='archive'
        ? '<span class="chip ghost">投放目录 主动归档/</span><a class="chip" href="#archive">收录规则 ↓</a>'
        : '<span class="chip ghost">图谱页 projects/bilibili-kb/graph/'+(k==='kepu'?'kb_all.html':'kb.html')+'</span>')
      +'</div></div>';
  }).join('');
}

var DOCS=CORE.docs.slice(),DFILTER='all',DLIMIT=24;
function docCard(d){
  var meta=d.coll==='archive'
    ? '<span>'+esc(d.upper)+'</span><span>· '+esc(d.date||'')+'</span><span>· '+(d.chars/1000).toFixed(1)+'k 字</span>'
    : '<span>'+esc(d.upper)+'</span><span>· '+esc(d.dur||'')+'</span><span>· 图 '+d.nImg+'</span>';
  return '<a class="doc" href="transcripts.html#id='+encodeURIComponent(d.id)+'" title="'+esc(d.title)+'">'
    +'<div class="t">'+esc(d.title)+'</div>'
    +'<div class="m">'+tagType(d.type)+tagColl(d)+tagDual(d)+meta+'</div>'
    +'<div class="ex">'+esc(d.ex)+'…</div></a>';
}
function renderDocs(){
  var box=$('#docs');if(!box)return;
  var list=DOCS.filter(function(d){return DFILTER==='all'||d.coll===DFILTER});
  var shown=list.slice(0,DLIMIT);
  box.innerHTML=shown.map(docCard).join('')
    ||(DFILTER==='archive'
      ? '<div class="note">「主动归档」目录里还没有文稿。把整理好的 <code>.md</code> 放进 '
        +'<code>__ARCHDIR__/</code>，重跑 <code>python _build/build_portal.py</code> 即可自动收录。</div>'
      : '<div class="muted">没有匹配的文稿</div>');
  $('#dcount').textContent=list.length;
  $('#dmore').style.display=list.length>DLIMIT?'inline-flex':'none';
  $('#dmore').textContent='展开剩余 '+(list.length-DLIMIT)+' 篇 →';
  $$('#dfilters .chip').forEach(function(c){c.classList.toggle('on',c.dataset.c===DFILTER)});
}
/* ---- UP主全转录：独立板块，不并入收藏夹 ---- */
function renderSrcCols(){
  var box=$('#srcs');if(!box)return;
  var list=CORE.srcCols||[];
  if(!list.length){box.innerHTML='<div class="muted">（sources.json 里没有配置来源目录）</div>';return}
  box.innerHTML=list.map(function(c){
    return '<div class="card colcard"><div class="hd">'
      +'<span class="dot" style="background:'+c.color+'"></span><h3>'+esc(c.name)+'</h3>'
      +'<span class="n">'+c.n+' 篇 · 约 '+(c.chars/10000).toFixed(1)+' 万字</span></div>'
      +(c.note?'<div class="muted" style="font-size:13px;margin:8px 0 2px">'+esc(c.note)+'</div>':'')
      +'<div class="kvrow">'
      +'<a class="chip" href="transcripts.html#c='+c.key+'">在文稿库中检索 '+c.n+' 篇 →</a></div></div>';
  }).join('');
}
function renderSrcList(){
  var box=$('#srclist');if(!box)return;
  var keys=(CORE.srcCols||[]).map(function(c){return c.key});
  var list=DOCS.filter(function(d){return keys.indexOf(d.coll)>=0});
  $('#srccount').textContent=list.length;
  box.innerHTML=list.slice(0,16).map(function(d){
    return '<a class="doc" href="transcripts.html#id='+encodeURIComponent(d.id)+'" title="'+esc(d.title)+'">'
      +'<div class="t">'+esc(d.title)+'</div>'
      +'<div class="m">'+tagType(d.type)+tagColl(d)+'<span>'+esc(d.upper)+'</span>'
      +'<span>· '+(d.chars/1000).toFixed(1)+'k 字</span></div>'
      +'<div class="ex">'+esc(d.ex)+'…</div></a>';
  }).join('');
}
/* ---- 主动归档：投放目录里的文稿 ---- */
function renderArch(){
  var box=$('#arch');if(!box)return;
  var list=DOCS.filter(function(d){return d.coll==='archive'});
  list.sort(function(a,b){return String(b.date||'').localeCompare(String(a.date||''))});
  if($('#archcount'))$('#archcount').textContent=list.length;
  if(!list.length){
    box.innerHTML='<div class="note"><h3>投放目录已就位，还没有稿件</h3>'
      +'把整理好的 <code>.md</code> 放进 <code>主动归档/</code>，然后重跑 <code>python _build/build_portal.py</code>，'
      +'它就会出现在这里、并进入全文检索。<br>命名与头部写法见 <code>主动归档/_归档说明.txt</code>。</div>';
    return;
  }
  box.innerHTML=list.slice(0,24).map(function(d){
    return '<a class="doc" href="transcripts.html#id='+encodeURIComponent(d.id)+'" title="'+esc(d.title)+'">'
      +'<div class="t">'+esc(d.title)+'</div>'
      +'<div class="m">'+tagType(d.type)+'<span>'+esc(d.upper)+'</span>'
      +'<span>· '+esc(d.date||'')+'</span><span>· '+(d.chars/1000).toFixed(1)+'k 字</span>'
      +(d.nImg?'<span>· 图 '+d.nImg+'</span>':'')+'</div>'
      +'<div class="ex">'+esc(d.ex)+'…</div></a>';
  }).join('');
}

/* ---- 顶栏即时搜索 ---- */
function suggestions(q){
  q=q.trim().toLowerCase(); if(!q)return [];
  var out=[];
  DOCS.forEach(function(d){
    var score=0,t=d.title.toLowerCase();
    if(t.indexOf(q)>=0)score+=8;
    if((d.upper||'').toLowerCase().indexOf(q)>=0)score+=4;
    if((d.ents||[]).some(function(e){return e.toLowerCase().indexOf(q)>=0}))score+=3;
    if((d.ex||'').toLowerCase().indexOf(q)>=0)score+=1;
    if(score)out.push([score,d]);
  });
  out.sort(function(a,b){return b[0]-a[0]});
  return out.slice(0,9).map(function(x){return x[1]});
}
var SUG=[],SUGI=-1;
function sugRender(q){
  var box=$('#sug');SUG=suggestions(q);SUGI=-1;
  if(!SUG.length){box.classList.remove('on');return}
  box.innerHTML=SUG.map(function(d,i){
    return '<div class="sug" data-i="'+i+'"><div><div class="st">'+esc(d.title)+'</div>'
      +'<div class="sm">'+esc(d.upper)+' · '+TYPE_CN[d.type]+' · '+esc(d.collName)+' · 图 '+d.nImg+' 张</div></div></div>'
  }).join('')+'<div class="foot">回车 → 在文稿库中全文检索「'+esc(q.trim())+'」</div>';
  box.classList.add('on');
  $$('#sug .sug').forEach(function(el){
    el.onmouseenter=function(){SUGI=+el.dataset.i;$$('#sug .sug').forEach(function(x){x.classList.remove('on')});el.classList.add('on')};
    el.onclick=function(){location.href='transcripts.html#id='+SUG[+el.dataset.i].id};
  });
}
function boot(){
  renderStats();renderApps();renderCols();renderArch();renderSrcCols();renderSrcList();renderDocs();
  var q=$('#q');
  q.addEventListener('input',debounce(function(){sugRender(q.value)},110));
  q.addEventListener('focus',function(){if(q.value.trim())sugRender(q.value)});
  q.addEventListener('keydown',function(e){
    if(e.key==='Enter'){
      var t=q.value.trim(); if(!t)return;
      if(SUGI>=0&&SUG[SUGI]){location.href='transcripts.html#id='+SUG[SUGI].id;return}
      location.href='transcripts.html#q='+encodeURIComponent(t);
    }else if(e.key==='ArrowDown'&&SUG.length){SUGI=Math.min(SUGI+1,SUG.length-1);
      $$('#sug .sug').forEach(function(x,i){x.classList.toggle('on',i===SUGI)});e.preventDefault()}
    else if(e.key==='ArrowUp'&&SUG.length){SUGI=Math.max(SUGI-1,-1);
      $$('#sug .sug').forEach(function(x,i){x.classList.toggle('on',i===SUGI)});e.preventDefault()}
    else if(e.key==='Escape'){$('#sug').classList.remove('on')}
  });
  document.addEventListener('click',function(e){if(!e.target.closest('.searchhost'))$('#sug').classList.remove('on')});
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)){e.preventDefault();q.focus();q.select()}
  });
  renderFilters();
  $('#dmore').onclick=function(){DLIMIT=9999;renderDocs()};
  lit();
}
function renderFilters(){
  var box=$('#dfilters');if(!box)return;
  var ks=Object.keys(CORE.cols);
  box.innerHTML='<span class="chip on" data-c="all">全部</span>'
    +ks.map(function(k){return '<span class="chip" data-c="'+k+'">'+esc(CORE.cols[k].name)+'</span>'}).join('');
  $$('#dfilters .chip').forEach(function(c){c.onclick=function(){DFILTER=c.dataset.c;renderDocs()}});
}
function lit(){
  try{
    if(location.protocol!=='file:'&&window.fetch){
      fetch('projects/bilibili-kb/.kb_status/state.json').then(function(r){return r.ok?r.json():null}).then(function(j){
        if(j&&j.done&&j.done.length)$('#live').textContent='归档流水线状态：done '+j.done.length;
      }).catch(function(){});
    }
  }catch(e){}
}
window.addEventListener('DOMContentLoaded',boot);
"""

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>数据宝库 · MyDataTreasure 入口</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>◆</text></svg>">
<style>__CSS__</style>
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="gem">◆</span>数据宝库 <small>MyDataTreasure</small></div>
  <nav class="tnav">
    <a href="index.html" class="on">入口</a>
    <a href="transcripts.html">文稿全文库</a>
    <a href="gallery.html">关键帧画廊</a>
    <a href="#upfull">UP主全转录</a>
    <a href="#archive">主动归档</a>
    <a href="#projects">项目</a>
    <a href="#help">使用说明</a>
  </nav>
  <span class="spacer"></span>
  <div class="searchhost">
    <label class="field">
      <span class="muted">🔍</span>
      <input id="q" placeholder="搜索标题 / UP主 / 概念，或在全体文稿中检索…" autocomplete="off">
      <span class="kbd">/</span>
    </label>
    <div class="sugbox" id="sug"></div>
  </div>
</header>

<div class="wrap">
  <section class="hero">
    <span class="kicker">本地自包含 · 双击即用 · 无需服务器</span>
    <h1>我的数据宝库</h1>
    <p class="lead">把值得反复看的视频与长讨论，变成<b>可检索、可成网、可回溯原文</b>的个人知识库：
      收藏夹走「ASR 转录 + VLM 逐帧判读 + 概念抽取 → 整理稿 + 观点网图」；
      UP 主全量转录与自建文稿另成板块、分开统计。以后自动转录出来的文稿，丢进 <b>主动归档/</b> 就会自动进库。</p>
    <div class="stats" id="stats"></div>
  </section>

  <div class="sect-title"><h2>进入</h2><p>点卡片直接打开对应可视化应用</p></div>
  <div class="grid g-apps" id="apps"></div>

  <div class="sect-title"><h2>知识库构成</h2><p>两个收藏夹 + 主动归档；UP 主全量转录另成板块，不并入收藏夹</p></div>
  <div class="grid cols" id="cols"></div>

  <div class="sect-title" id="upfull"><h2>UP主全转录 · <b id="srccount">0</b> 篇</h2>
    <p>按 UP 主/系列整批转录的稿件，来源目录由 <code>_build/sources.json</code> 配置</p></div>
  <div class="grid cols" id="srcs"></div>
  <div class="grid dgrid" id="srclist" style="margin-top:14px"></div>
  <div class="note" style="margin-top:14px">
    <h3>这一板块怎么用</h3>
    <ol>
      <li>这些是<b>整批全转录稿</b>（职场类 193 篇、法政讲坛 148 篇），与收藏夹那 232 篇观点/科普稿<b>分开统计、分开筛选</b>，不会混进收藏夹分支。</li>
      <li>稿件本体仍在原项目目录里（不搬文件）；重跑生成器即可让改动生效，也可在 <code>_build/sources.json</code> 增删来源目录。</li>
      <li>想搜这批内容：点上面任意来源卡片的「在文稿库中检索」，或直接用 <code>transcripts.html#c=&lt;来源key&gt;</code> 深链。</li>
    </ol>
  </div>

  <div class="sect-title" id="archive"><h2>主动归档 · <b id="archcount">__ARCH__</b> 篇</h2>
    <p>以后自动转录 / 自动整理出来的文稿，直接丢进 <code>主动归档/</code> 目录即可</p></div>
  <div class="grid dgrid" id="arch"></div>
  <div class="note" style="margin-top:14px">
    <h3>归档规则（约定俗成，照着放就行）</h3>
    <ol>
      <li><b>放什么</b>：B 站视频转录整理稿、微信群聊/会议结构化总结、任何自己整理好的长文笔记。</li>
      <li><b>放哪里</b>：<code>D:\PythonProject\MyDataTreasureWeb\__ARCHDIR__\</code>（可再建子文件夹，会递归扫描）。</li>
      <li><b>什么格式</b>：Markdown（<code>.md</code>）。文件名建议 <code>标题_YYYYMMDD.md</code>；
        第一行用 <code># 标题</code>，下一行加来源行（转录稿格式：<code>【B站up主】xxx 【视频标题】[链接](链接)</code>）。</li>
      <li><b>怎么生效</b>：放好后执行一次 <code>python _build\build_portal.py</code>（或告诉我「重建门户」），
        文稿即进入本页列表与全文检索；<code>_归档说明.txt</code> 里有完整说明。</li>
    </ol>
  </div>

  <div class="sect-title" id="projects"><h2>项目与文件</h2><p>Web 之外的原始素材与工具链位置</p></div>
  <div class="two">
    <div class="note">
      <h3>原始素材（projects/bilibili-kb）</h3>
      <ol>
        <li><code>nodes/*.md</code> — 238 篇节点整理稿（正文与网页同源）</li>
        <li><code>transcripts/*.txt</code> — ASR 原始转录文本</li>
        <li><code>raw/ · kepu/raw/</code> — __KFTOTAL__ 张关键帧原图</li>
        <li><code>graph/data_all.json</code> — 图谱数据（节点/边/语义索引）</li>
        <li><code>classification.json · favorites_meta.json</code> — 分类与元数据</li>
      </ol>
    </div>
    <div class="note">
      <h3>本入口的生成方式</h3>
      <ol>
        <li>页面全部<b>自包含</b>：数据内联，不联网、不依赖 CDN，<span class="warn">file:// 双击即可打开</span>。</li>
        <li>重建命令：<code>python _build/build_portal.py</code>（新增/修改节点后重跑即可）。</li>
        <li><b>归档投放目录</b>：<code>__ARCHDIR__/</code> —— 新转录 / 新整理的 <code>.md</code> 放这里，重跑生成器即自动收录。</li>
        <li>图谱页面里带 <b>Canvas 静态图谱</b> 的两张需读 JSON，浏览器限制必须走本地服务 → 双击 <code>启动本地服务.bat</code>。</li>
      </ol>
    </div>
  </div>

  <div class="sect-title"><h2>文稿速览</h2><p>共 <b id="dcount">0</b> 篇（__DUAL__ 个视频同时躺在两个收藏夹里，已合并为一条）</p></div>
  <div class="filters" id="dfilters">
    <span class="spacer" style="flex:1"></span>
    <a class="btn" href="transcripts.html">打开文稿全文库 →</a>
  </div>
  <div class="grid dgrid" id="docs"></div>
  <div style="text-align:center;margin-top:16px">
    <button class="btn" id="dmore">展开更多 →</button>
  </div>

  <div class="sect-title" id="help"><h2>使用说明</h2><p>四条路径，按需取用</p></div>
  <div class="two">
    <div class="note">
      <h3>① 新转录的稿子往哪放</h3>
      <ol>
        <li>把整理好的 <code>.md</code> 丢进 <code>__ARCHDIR__/</code> → 重跑 <code>python _build/build_portal.py</code>
          → 自动出现在首页「主动归档」与全文检索里。</li>
        <li>首行写 <code># 标题</code>；转录稿再加一行来源：<code>【B站up主】xxx 【视频标题】[链接](链接)</code>。</li>
        <li>文件名建议 <code>标题_YYYYMMDD.md</code>，同名覆盖即更新。完整约定见 <code>_归档说明.txt</code>。</li>
      </ol>
    </div>
    <div class="note">
      <h3>② 只想读文稿</h3>
      <ol>
        <li>打开 <code>transcripts.html</code>：左边列表 + 全文检索，右侧渲染完整整理稿（含概要、关键帧图说、概念实体）。</li>
        <li>支持深链：<code>transcripts.html#id=BV1fqJw6WEXC</code> 直接定位某篇；<code>#q=关键词</code> 全文检索。</li>
        <li>快捷键：<code>/</code> 聚焦搜索、<code>↑ ↓</code> 选条目、<code>Esc</code> 清空。</li>
      </ol>
    </div>
    <div class="note">
      <h3>③ 想看图 / 找画面</h3>
      <ol>
        <li>打开 <code>gallery.html</code>：__KFTOTAL__ 张关键帧瀑布墙，可按库 / UP主 / 视频筛选。</li>
        <li>点任意图放大，<code>← →</code> 翻页，可直接跳到对应文稿。</li>
      </ol>
    </div>
    <div class="note">
      <h3>④ 想看观点如何连成网</h3>
      <ol>
        <li>打开 <code>projects/bilibili-kb/graph/kb.html</code>：Canvas 网图，支持语义检索、概念浏览器、拖拽钉住、关键帧灯箱。</li>
        <li>用 <code>#n=BV号</code> 可从任何页面直达某个节点。</li>
        <li>合并视图 <code>kb_all.html</code> 覆盖两个收藏夹（__NODES__ 节点）。</li>
      </ol>
    </div>
  </div>

  <footer>
    <span>生成时间 <b id="built">__BUILT__</b></span>
    <span id="live">数据源 data_all.json · 全量内联</span>
    <span class="spacer" style="flex:1"></span>
    <span>MyDataTreasureWeb · 双击 index.html 即可进入</span>
  </footer>
</div>

<script>window.__CORE__=__CORE_JSON__;</script>
<script>__JS__</script>
</body>
</html>
"""
