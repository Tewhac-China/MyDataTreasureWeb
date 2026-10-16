# -*- coding: utf-8 -*-
"""文稿全文库 transcripts.html 的模板。"""

PAGE_CSS = r"""
html,body{height:100%}
body{overflow:hidden}
.lib{display:grid;grid-template-columns:352px 1fr;height:calc(100vh - var(--topH));height:calc(100dvh - var(--topH))}
.side{
  border-right:1px solid var(--line);background:rgba(255,255,255,.72);backdrop-filter:blur(10px);
  display:grid;grid-template-rows:auto auto 1fr;min-height:0
}
.side-top{padding:12px 12px 9px;border-bottom:1px solid var(--line2)}
.side-top .field{min-width:0;width:100%}
.side-meta{display:flex;align-items:center;gap:8px;font-size:12.2px;color:var(--ink3);margin-top:8px;padding:0 2px}
.fl{padding:9px 12px;display:flex;flex-wrap:wrap;gap:6px;border-bottom:1px solid var(--line2)}
.fl .chip{font-size:11.6px;padding:2px 8px}
.flgroup{
  flex-basis:100%;font-size:10.6px;letter-spacing:.6px;color:var(--ink3);margin:4px 0 -1px;font-weight:700
}
.fl select{
  border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:3px 7px;font-size:12px;
  max-width:150px;color:var(--ink2)
}
.list{overflow:auto;padding:7px 8px 20px;min-height:0}
.it{
  display:block;padding:9px 11px;border-radius:11px;cursor:pointer;border:1px solid transparent;color:inherit;
  text-decoration:none;margin-bottom:2px
}
.it:hover{background:var(--panel);border-color:var(--line2);text-decoration:none}
.it.on{background:var(--accent-soft);border-color:rgba(99,102,241,.35)}
.it.on .it-t{color:var(--accent)}
.it-t{font-size:13.7px;font-weight:650;line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.it-m{font-size:11.6px;color:var(--ink3);margin-top:3px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
.it-x{font-size:11.8px;color:var(--ink2);margin-top:4px;line-height:1.6;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.empty{padding:26px 16px;text-align:center;color:var(--ink3);font-size:13px}

.reader{overflow:auto;height:100%;position:relative;scroll-behavior:smooth}
.pbar{position:sticky;top:0;height:3px;background:transparent;z-index:40}
.pbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,#6366f1,#ec4899)}
.docwrap{max-width:920px;margin:0 auto;padding:26px 34px 90px}
.dochead h1{margin:12px 0 12px;font-size:clamp(23px,3vw,31px);line-height:1.32;letter-spacing:-.5px}
.crumbs{font-size:12.4px;color:var(--ink3);display:flex;gap:7px;flex-wrap:wrap;align-items:center}
.crumbs b{color:var(--ink2);font-weight:600}
.meta{display:flex;flex-wrap:wrap;gap:7px;align-items:center;font-size:12.4px;color:var(--ink3);margin-bottom:15px}
.actions{display:flex;flex-wrap:wrap;gap:8px;padding-bottom:18px;border-bottom:1px solid var(--line);margin-bottom:6px}
.toc{display:flex;flex-wrap:wrap;gap:6px;margin:16px 0 6px}
.toc a{
  font-size:12.2px;color:var(--ink2);background:var(--panel);border:1px solid var(--line);border-radius:999px;
  padding:3px 10px;text-decoration:none
}
.toc a:hover{border-color:rgba(99,102,241,.45);color:var(--accent)}
.kfsec{margin-top:34px;border-top:1px solid var(--line);padding-top:20px}
.kfsec>summary{cursor:pointer;font-size:15px;font-weight:700;margin-bottom:12px}
.kfsec h2{font-size:15.5px;margin:0 0 12px;display:flex;align-items:center;gap:9px}
.kfgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:12px}
.kfcard{border:1px solid var(--line);border-radius:13px;overflow:hidden;background:var(--panel);box-shadow:var(--sh1)}
.kfcard img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;cursor:zoom-in;background:var(--panel3)}
.kfcard .c{padding:9px 11px}
.kfcard .t{font-size:11.8px;font-weight:700;color:var(--accent);font-family:var(--mono)}
.kfcard .d{font-size:12.4px;color:var(--ink2);line-height:1.62;margin-top:3px;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.welcome{max-width:920px;margin:0 auto;padding:40px 34px}
.welcome h1{font-size:30px;letter-spacing:-.7px;margin:0 0 10px}
.wgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:11px;margin:22px 0}
.wcard{padding:14px 15px;border-radius:13px;border:1px solid var(--line);background:var(--panel);box-shadow:var(--sh1)}
.wcard .v{font-size:21px;font-weight:800;letter-spacing:-.5px}
.wcard .k{font-size:12px;color:var(--ink3);margin-top:2px}
mark.hit{background:rgba(250,204,21,.55);border-radius:3px;padding:0 1px;box-shadow:0 0 0 1px rgba(250,204,21,.55)}
.mobilebar{display:none}
@media (max-width:900px){
  body{overflow:auto}
  .lib{grid-template-columns:1fr;height:auto}
  .side{border-right:0;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:50;grid-template-rows:auto auto auto}
  .list{max-height:44vh}
  .reader{height:auto}
  .docwrap{padding:18px 16px 70px}
}
"""

PAGE_JS = r"""
var DATA=window.__FULL__||{docs:[],stats:{},cols:{}};
var TYPE_CN={text:'文本型',hybrid:'混合型',visual:'画面型'};
var Q='',FC='all',FT='all',FU='all',LIST=[],CUR=-1,VIEW=[];
var COLMAP={};
(function(){var c=DATA.cols||{};Object.keys(c).forEach(function(k){COLMAP[k]={name:c[k].name,color:c[k].color,kind:c[k].kind}});})();
function tagType(t){return '<span class="tag t-'+t+'">'+(TYPE_CN[t]||t)+'</span>'}
function tagColl(d){var m=COLMAP[d.coll]||{};var col=m.color||'#6366f1';
  return '<span class="tag" style="color:'+col+';background:'+col+'22">'+esc(d.collName)+'</span>'}
function tagDual(d){return (d.dual&&d.dual.length>1)?'<span class="tag d-dual" title="'+esc(d.dual.join(' + '))+'">双库</span>':''}
function hl(s,q){
  s=esc(s); if(!q)return s;
  try{
    var re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');
    return s.replace(re,'<mark class="hit">$1</mark>');
  }catch(e){return s}
}
function excerpt(d,q){
  if(!q)return d.summary?d.summary.slice(0,150)+'…':'';
  var low=d.md.toLowerCase(),i=low.indexOf(q.toLowerCase());
  if(i<0)return (d.summary||'').slice(0,150)+'…';
  return '…'+d.md.slice(Math.max(0,i-52),i+140).replace(/\s+/g,' ')+'…';
}
/* ---------------- 过滤 / 列表 ---------------- */
function applyFilter(){
  var q=Q.trim().toLowerCase();
  LIST=DATA.docs.filter(function(d){
    if(FC!=='all'&&d.coll!==FC)return false;
    if(FT!=='all'&&d.type!==FT)return false;
    if(FU!=='all'&&d.upper!==FU)return false;
    if(!q)return true;
    return (d.title+' '+d.upper+' '+(d.ents||[]).join(' ')+' '+d.summary+' '+d.md).toLowerCase().indexOf(q)>=0;
  });
  renderList();
}
function renderList(){
  var box=$('#list'),q=Q.trim();
  $('#cnt').textContent=LIST.length+' / '+DATA.docs.length+' 篇';
  $('#hint').textContent=q?('命中 '+LIST.length+' 篇 · 点条目阅读，正文内高亮已开启'):'';
  if(!LIST.length){
    box.innerHTML=(FC==='archive')
      ? '<div class="empty">「主动归档」目录里还没有文稿<br><span style="font-size:12px">把整理好的 <b>.md</b> 放进 <b>主动归档/</b>，'
        +'重跑 <b>_build/build_portal.py</b> 就会出现在这里<br>文件名建议 标题_YYYYMMDD.md，写法见该目录下的 _归档说明.txt</span></div>'
      : '<div class="empty">没有匹配的文稿<br><span style="font-size:12px">试试更短的关键词，或清空筛选</span></div>';
    return;
  }
  box.innerHTML=LIST.map(function(d){
    var tail=(d.coll==='archive')
      ? '<span>· '+esc(d.date||'')+'</span>'
      : '<span>· '+esc(d.dur||'')+'</span>';
    return '<a class="it'+(d.id===curId()?' on':'')+'" href="#id='+encodeURIComponent(d.id)+'" data-id="'+esc(d.id)+'">'
      +'<div class="it-t">'+hl(d.title,q)+'</div>'
      +'<div class="it-m">'+tagType(d.type)+tagColl(d)+tagDual(d)+'<span>'+hl(d.upper,q)+'</span>'+tail
      +'<span>· '+(d.chars/1000).toFixed(1)+'k 字</span></div>'
      +(q?'<div class="it-x">'+hl(excerpt(d,q),q)+'</div>':'')
      +'</a>';
  }).join('');
  $$('#list .it').forEach(function(el){
    el.onclick=function(e){e.preventDefault();open(el.dataset.id,true)};
  });
}
function curId(){return CUR>=0&&DATA.docs[CUR]?DATA.docs[CUR].id:''}
/* ---------------- 阅读 ---------------- */
function welcome(){
  var s=DATA.stats;
  $('#page').innerHTML='<div class="welcome">'
    +'<h1>文稿全文库</h1>'
    +'<p class="muted" style="max-width:720px">这里收录 <b>'+(s.docsAll||s.docs)+'</b> 篇文稿，分三类：'
    +'<b>收藏夹整理稿 '+(s.docs||0)+' 篇</b>（ASR 转录经纠错整理，画面型附 VLM 逐帧关键帧图说，每篇抽出概念与实体）'
    +(s.arch?'、<b>主动归档 '+s.arch+' 篇</b>（放在 <code class="mono">主动归档/</code> 里的自建/新转录稿）':'')
    +(s.src?'、<b>UP主全转录 '+s.src+' 篇</b>（按 UP 主/系列整批转录，与收藏夹分开统计）':'')
    +'。左侧可检索，也可用 <code class="mono">#q=关键词</code>、<code class="mono">#c=库名</code> 深链。</p>'
    +'<div class="wgrid">'
    +[['收藏夹文稿',(s.docs||0)+' 篇'],['主动归档',(s.arch||0)+' 篇'],['UP主全转录',(s.src||0)+' 篇'],
      ['总字数',((s.charsAll||s.chars)/10000).toFixed(1)+' 万字'],['关键帧',s.kf+' 张'],['概念/实体',s.entities+' 个']]
      .map(function(x){return '<div class="wcard"><div class="v">'+x[1]+'</div><div class="k">'+x[0]+'</div></div>'}).join('')
    +'</div>'
    +'<p class="muted" style="font-size:13px">按 <b class="mono">/</b> 聚焦搜索框，<b class="mono">↑ ↓</b> 在结果间切换，'
    +'<b class="mono">Esc</b> 清空检索。从列表点开任意一篇即可阅读全文。</p>'
    +'</div>';
}
function open(id,push){
  var i=-1;for(var k=0;k<DATA.docs.length;k++){if(DATA.docs[k].id===id){i=k;break}}
  if(i<0){welcome();return}
  CUR=i;
  var d=DATA.docs[i];VIEW=[];
  var q=Q.trim();
  var body=md2html(d.md);
  if(q){
    try{
      var re=new RegExp('('+q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');
      body=body.replace(/(>)([^<]+)(<)/g,function(m,a,t,b){return a+t.replace(re,'<mark class="hit">$1</mark>')+b});
    }catch(e){}
  }
  var kf=d.kf||[];
  var kfHtml='';
  if(kf.length){
    var grid='<div class="kfgrid">'+kf.map(function(k,idx){
      VIEW.push({img:k.img,cap:'<b>'+esc(k.t||'')+'</b> '+esc(k.desc||'')+'<br><span style="opacity:.8">'+esc(k.note||'')+'</span>',
        title:d.title+' · '+(k.t||'')});
      return '<div class="kfcard"><img loading="lazy" src="'+k.img+'" data-idx="'+idx+'" alt=""><div class="c">'
        +'<div class="t">'+esc(k.t||'关键帧')+'</div><div class="d">'+esc(k.desc||'')+'</div></div></div>';
    }).join('')+'</div>';
    kfHtml=d.hasInlineImg
      ? '<details class="kfsec"><summary>关键帧（'+kf.length+' 张 · 正文表格中已含图说，此处为纯图墙）</summary>'+grid+'</details>'
      : '<div class="kfsec"><h2>关键帧 · '+kf.length+' 张</h2>'+grid+'</div>';
  }
  /* 目录：抓 ## / ### 标题 */
  var toc='',titles=[];
  (d.md||'').replace(/^(#{2,3})\s+(.+)$/gm,function(m,h,t){titles.push([h.length,t.replace(/[*`]/g,'')]);return m});
  if(titles.length>2){
    toc='<div class="toc">'+titles.slice(0,14).map(function(t,i){
      return '<a href="#" data-h="'+esc(t[1])+'">'+esc(t[1])+'</a>'}).join('')+'</div>';
  }
  var isArch=(d.coll==='archive');
  var metaTail=isArch
    ? '<span>来源 · <b>'+esc(d.upper)+'</b></span>'+(d.date?'<span>· 归档 '+esc(d.date)+'</span>':'')
      +'<span>· '+(d.chars/1000).toFixed(1)+'k 字</span>'
      +(d.nImg?'<span>· 插图 '+d.nImg+'</span>':'')+'<span>· 概念 '+(d.ents||[]).length+'</span>'
    : '<span>UP · <b>'+esc(d.upper)+'</b></span><span>· '+(d.dur||'—')+'</span>'
      +'<span>· '+(d.chars/1000).toFixed(1)+'k 字</span><span>· 关键帧 '+kf.length+'</span>'
      +'<span>· 概念 '+(d.ents||[]).length+'</span>';
  $('#page').innerHTML='<div class="docwrap">'
    +'<div class="crumbs"><span>文稿全文库</span><span>/</span><b>'+esc(d.collName)+'</b><span>/</span>'
      +'<span class="mono">'+esc(d.rel||d.file||d.id)+'</span></div>'
    +'<h1>'+hl(d.title,q)+'</h1>'
    +'<div class="meta">'+tagType(d.type)+tagColl(d)+tagDual(d)+metaTail+'</div>'
    +'<div class="actions">'
      +(d.url?'<a class="btn primary" href="'+d.url+'" target="_blank" rel="noopener">在 B 站看原片 ↗</a>':'')
      +'<button class="btn" id="btnCopy">复制全文</button>'
      +'<button class="btn" id="btnRaw">查看原始 MD</button>'
      +(d.graph?'<a class="btn" href="'+d.graph+'">在网图中定位 ↗</a>':'')
      +(isArch?'<a class="btn" href="index.html#archive">主动归档收录规则 ↗</a>':'')
      +'<span class="spacer" style="flex:1"></span>'
      +'<button class="btn" id="btnPrev">← 上一篇</button>'
      +'<button class="btn" id="btnNext">下一篇 →</button>'
    +'</div>'+toc
    +(d.ents&&d.ents.length?'<div class="toc" style="margin-top:6px">'+d.ents.slice(0,16).map(function(e){
        return '<a href="transcripts.html#q='+encodeURIComponent(e)+'">'+esc(e)+'</a>'}).join('')+'</div>':'')
    +'<article class="md" id="body">'+body+'</article>'+kfHtml
    +'</div>';
  $('#reader').scrollTop=0;
  bindDoc(d);
  if(push)history.replaceState(null,'','#id='+id);
  renderList();
  var el=$('#list .it.on'); if(el)el.scrollIntoView({block:'nearest'});
}
function bindDoc(d){
  var pos=function(){return LIST.findIndex(function(x){return x.id===d.id})};
  var p=$('#btnPrev'),n=$('#btnNext');
  var i=pos(); p.disabled=i<=0; n.disabled=i<0||i>=LIST.length-1;
  p.onclick=function(){if(i>0)open(LIST[i-1].id,true)};
  n.onclick=function(){if(i>=0&&i<LIST.length-1)open(LIST[i+1].id,true)};
  $('#btnCopy').onclick=function(){
    var t=d.md; try{navigator.clipboard.writeText(t);toast('已复制《'+esc(d.title)+'》全文（'+t.length+' 字符）')}
    catch(e){var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();
      try{document.execCommand('copy');toast('已复制全文')}catch(x){toast('复制失败，请手动选择文本')}ta.remove()}
  };
  $('#btnRaw').onclick=function(){
    var w=window.open('','_blank'); if(!w){toast('浏览器拦截了弹窗');return}
    w.document.write('<meta charset="utf-8"><title>'+esc(d.title)+' · MD</title>'
      +'<pre style="font:13px/1.7 ui-monospace,Consolas,monospace;white-space:pre-wrap;padding:22px;max-width:920px;margin:auto">'
      +esc(d.md)+'</pre>');
  };
  $$('.docwrap .toc a[data-h]').forEach(function(a){
    a.onclick=function(e){e.preventDefault();var hs=$$('#body h2,#body h3');
      for(var i=0;i<hs.length;i++){if(hs[i].textContent.trim()===a.dataset.h){hs[i].scrollIntoView({block:'start'});break}}};
  });
  $$('#body .mdimg').forEach(function(im){
    im.onclick=function(){lbOpen(VIEW.length?VIEW:[{img:im.src,cap:''}],0,d.title)};
  });
  $$('.kfcard img').forEach(function(im){
    im.onclick=function(){lbOpen(VIEW,+im.dataset.idx,d.title)};
  });
  $('#reader').onscroll=function(){
    var el=$('#reader'),h=el.scrollHeight-el.clientHeight;
    $('#pbar i').style.width=(h>0?(el.scrollTop/h*100):0)+'%';
  };
}
/* ---------------- 启动 ---------------- */
function boot(){
  var f=$('#fColl'),t=$('#fType'),u=$('#fUp');
  /* 库筛选：收藏夹 → 主动归档 → UP主全转录，分组显示（不混在同一堆里） */
  var order=[{kind:'fav',label:'收藏夹'},{kind:'archive',label:'投放目录'},{kind:'upfull',label:'UP主全转录'}];
  var html='<span class="chip on" data-c="all">全部库（'+DATA.docs.length+'）</span>';
  order.forEach(function(g){
    var keys=Object.keys(DATA.cols).filter(function(k){return (DATA.cols[k].kind||'fav')===g.kind});
    if(!keys.length)return;
    var sum=keys.reduce(function(a,k){return a+DATA.cols[k].n},0);
    html+='<span class="flgroup">'+g.label+'</span>';
    html+=keys.map(function(k){
      return '<span class="chip" data-c="'+k+'" title="'+esc(DATA.cols[k].name)+'">'
        +esc(DATA.cols[k].name)+' '+DATA.cols[k].n+'</span>'}).join('');
  });
  f.innerHTML=html;
  t.innerHTML='<span class="chip on" data-t="all">全部类型</span>'+['text','hybrid','visual'].map(function(k){
    return '<span class="chip" data-t="'+k+'">'+TYPE_CN[k]+'</span>'}).join('');
  var ups={};DATA.docs.forEach(function(d){ups[d.upper]=(ups[d.upper]||0)+1});
  u.innerHTML='<option value="all">全部 UP主（'+Object.keys(ups).length+'）</option>'
    +Object.keys(ups).sort(function(a,b){return ups[b]-ups[a]}).map(function(k){
      return '<option value="'+esc(k)+'">'+esc(k)+'（'+ups[k]+'）</option>'}).join('');
  f.onclick=function(e){var c=e.target.closest('.chip');if(!c)return;FC=c.dataset.c;
    $$('#fColl .chip').forEach(function(x){x.classList.toggle('on',x===c)});applyFilter();
    history.replaceState(null,'',FC==='all'?location.pathname:'#c='+FC);};
  t.onclick=function(e){var c=e.target.closest('.chip');if(!c)return;FT=c.dataset.t;
    $$('#fType .chip').forEach(function(x){x.classList.toggle('on',x===c)});applyFilter()};
  u.onchange=function(){FU=u.value;applyFilter()};
  var q=$('#q');
  q.addEventListener('input',debounce(function(){Q=q.value;applyFilter()},150));
  q.addEventListener('keydown',function(e){
    if(e.key==='Escape'){q.value='';Q='';applyFilter();q.blur()}
    else if(e.key==='Enter'){var it=LIST[0];if(it)open(it.id,true)}
    else if(e.key==='ArrowDown'&&LIST.length){e.preventDefault();open(LIST[0].id,true);
      var el=$('#list .it');if(el)el.focus()}
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q&&!/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)){
      e.preventDefault();q.focus();q.select();return}
    if(/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){
      if(!LIST.length)return; e.preventDefault();
      var i=LIST.findIndex(function(x){return x.id===curId()});
      i=e.key==='ArrowDown'?(i<0?0:Math.min(i+1,LIST.length-1)):(i<0?0:Math.max(i-1,0));
      open(LIST[i].id,true);
    }
  });
  window.addEventListener('hashchange',function(){route()});
  route();
  function route(){
    var h=parseHash();
    if(h.q!==undefined){q.value=h.q;Q=h.q}
    if(h.c!==undefined&&(h.c==='all'||DATA.cols[h.c])){FC=h.c;
      $$('#fColl .chip').forEach(function(x){x.classList.toggle('on',x.dataset.c===FC)})}
    applyFilter();
    if(h.id)open(h.id,false); else if(!Q)welcome();
  }
}
window.addEventListener('DOMContentLoaded',boot);
"""

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>文稿全文库 · 数据宝库</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📚</text></svg>">
<style>__CSS__</style>
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="gem">◆</span>数据宝库 <small>__N__ 篇文稿</small></div>
  <nav class="tnav">
    <a href="index.html">入口</a>
    <a href="transcripts.html" class="on">文稿全文库</a>
    <a href="gallery.html">关键帧画廊</a>
    <a href="projects/bilibili-kb/graph/kb.html">网图浏览器</a>
  </nav>
  <span class="spacer"></span>
  <span class="muted" style="font-size:12.4px;white-space:nowrap">共 <b>__N__</b> 篇 · <b>__CHARS__</b> 万字</span>
</header>

<div class="lib">
  <aside class="side">
    <div class="side-top">
      <label class="field"><span class="muted">🔍</span>
        <input id="q" placeholder="全文检索：标题 / UP主 / 概念 / 正文…" autocomplete="off">
        <span class="kbd">/</span>
      </label>
      <div class="side-meta"><span id="cnt"></span><span class="spacer" style="flex:1"></span><span id="hint"></span></div>
    </div>
    <div class="fl" id="fColl"></div>
    <div class="fl" id="fType" style="padding-top:0;border-bottom:0"></div>
    <div class="fl" style="padding-top:0">
      <select id="fUp"></select>
      <span class="spacer" style="flex:1"></span>
      <span class="chip" onclick="location.hash='';location.reload()">重置</span>
    </div>
    <div class="list" id="list"></div>
  </aside>
  <div class="reader" id="reader"><div class="pbar"><i></i></div><div id="page"></div></div>
</div>

<script>window.__FULL__=__FULL_JSON__;</script>
<script>__JS__</script>
</body>
</html>
"""
