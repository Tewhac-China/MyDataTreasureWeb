# -*- coding: utf-8 -*-
"""关键帧画廊 gallery.html 的模板。"""

PAGE_CSS = r"""
body{overflow:hidden}
.gal{display:grid;grid-template-rows:auto 1fr;height:calc(100vh - var(--topH));height:calc(100dvh - var(--topH))}
.gbar{
  display:flex;flex-wrap:wrap;gap:7px;align-items:center;padding:11px 18px;border-bottom:1px solid var(--line);
  background:rgba(255,255,255,.7);backdrop-filter:blur(10px)
}
.gbar .field{min-width:210px;padding:4px 10px}
.gbar .chip{font-size:12px;padding:2px 9px}
.gbar select{border:1px solid var(--line);background:var(--panel);border-radius:9px;padding:4px 8px;font-size:12.2px;
  color:var(--ink2);max-width:190px}
.gbar .cnt{font-size:12.4px;color:var(--ink3);white-space:nowrap}
.scroll{overflow:auto;padding:16px 18px 60px;min-height:0}
.mason{columns:6 226px;column-gap:12px}
.kf{
  break-inside:avoid;margin:0 0 12px;border:1px solid var(--line);border-radius:13px;overflow:hidden;background:var(--panel);
  box-shadow:var(--sh1);cursor:zoom-in;position:relative;transition:transform .16s,box-shadow .16s,border-color .16s
}
.kf:hover{transform:translateY(-2px);box-shadow:var(--sh2);border-color:rgba(99,102,241,.42)}
.kf img{width:100%;display:block;background:var(--panel3);min-height:110px}
.kf .ov{
  position:absolute;inset:0 0 auto 0;display:flex;gap:6px;align-items:center;padding:7px 9px;
  background:linear-gradient(180deg,rgba(8,11,20,.62),transparent);opacity:0;transition:opacity .18s
}
.kf:hover .ov{opacity:1}
.kf .ov .mono{font-size:11px;color:#fff;background:rgba(0,0,0,.45);padding:1px 7px;border-radius:6px}
.kf .ov .b{font-size:11px;color:#fff;background:rgba(99,102,241,.85);padding:1px 7px;border-radius:6px;font-weight:600}
.kf .c{padding:8px 10px 9px}
.kf .d{font-size:12.2px;color:var(--ink2);line-height:1.6;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.kf .n{font-size:11.4px;color:var(--ink3);margin-top:5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sentinel{padding:22px;text-align:center;color:var(--ink3);font-size:13px}
@media (max-width:900px){html,body{overflow:auto}.gal{height:auto}.scroll{overflow:visible;padding:12px 12px 60px}.mason{columns:2 140px}}
"""

PAGE_JS = r"""
var G=window.__GAL__||{items:[],stats:{}};
var TYPE_CN={text:'文本型',hybrid:'混合型',visual:'画面型'};
var FILT=[],SHOWN=0,BATCH=240,FC='all',FT='all',FV='all',FQ='';
function tagType(t){return '<span class="tag t-'+t+'">'+(TYPE_CN[t]||t)+'</span>'}
function apply(){
  var q=FQ.trim().toLowerCase();
  FILT=G.items.filter(function(x){
    if(FC!=='all'&&x.coll!==FC)return false;
    if(FT!=='all'&&x.type!==FT)return false;
    if(FV!=='all'&&x.id!==FV)return false;
    if(!q)return true;
    return (x.title+' '+x.upper+' '+(x.desc||'')+' '+(x.note||'')+' '+x.t).toLowerCase().indexOf(q)>=0;
  });
  SHOWN=0; $('#mason').innerHTML=''; $('#cnt').textContent=FILT.length+' / '+G.items.length+' 张';
  $('#empty').style.display=FILT.length?'none':'block';
  more();
}
function card(x,i){
  return '<figure class="kf" data-i="'+i+'">'
    +'<img loading="lazy" src="'+x.img+'" alt="" decoding="async">'
    +'<div class="ov">'+(x.t?'<span class="mono">'+esc(x.t)+'</span>':'')+'<span class="b">'+esc(x.coll==='kepu'?'科普':'观点')+'</span></div>'
    +'<figcaption class="c"><div class="d">'+esc(x.desc||'（无图说）')+'</div>'
    +'<div class="n">'+esc(x.title)+'</div></figcaption></figure>';
}
function more(){
  var box=$('#mason');
  if(SHOWN>=FILT.length){$('#sent').textContent=FILT.length?('已到底部 · 共 '+FILT.length+' 张'):'';return}
  var end=Math.min(SHOWN+BATCH,FILT.length),html='';
  for(var i=SHOWN;i<end;i++)html+=card(FILT[i],i);
  box.insertAdjacentHTML('beforeend',html);
  SHOWN=end;
  $('#sent').textContent=SHOWN<FILT.length?('继续下滑加载剩余 '+(FILT.length-SHOWN)+' 张…'):('已到底部 · 共 '+FILT.length+' 张');
}
function boot(){
  var cols=Object.keys(G.stats.cols||{});
  $('#fColl').innerHTML='<span class="chip on" data-c="all">全部库</span>'
    +(window.__COLS__||[]).map(function(c){return '<span class="chip" data-c="'+c.k+'">'+esc(c.n)+'</span>'}).join('');
  $('#fType').innerHTML='<span class="chip on" data-t="all">全部</span>'+['text','hybrid','visual'].map(function(t){
    return '<span class="chip" data-t="'+t+'">'+TYPE_CN[t]+'</span>'}).join('');
  var vids={},order=[];
  G.items.forEach(function(x){if(!vids[x.id]){vids[x.id]={t:x.title,u:x.upper,n:0};order.push(x.id)}vids[x.id].n++});
  $('#fVid').innerHTML='<option value="all">全部视频（'+order.length+'）</option>'
    +order.map(function(k){return '<option value="'+k+'">'+esc(vids[k].t)+'（'+vids[k].n+'）</option>'}).join('');
  $('#fColl').onclick=function(e){var c=e.target.closest('.chip');if(!c)return;FC=c.dataset.c;
    $$('#fColl .chip').forEach(function(x){x.classList.toggle('on',x===c)});apply()};
  $('#fType').onclick=function(e){var c=e.target.closest('.chip');if(!c)return;FT=c.dataset.t;
    $$('#fType .chip').forEach(function(x){x.classList.toggle('on',x===c)});apply()};
  $('#fVid').onchange=function(){FV=this.value;apply()};
  var q=$('#q');
  q.addEventListener('input',debounce(function(){FQ=q.value;apply()},170));
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q&&!/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName)){e.preventDefault();q.focus();q.select()}});
  var sc=$('#scroll');
  sc.addEventListener('scroll',debounce(function(){
    if(sc.scrollTop+sc.clientHeight>=sc.scrollHeight-900)more()},120));
  $('#mason').addEventListener('click',function(e){
    var f=e.target.closest('.kf'); if(!f)return;
    var i=+f.dataset.i, x=FILT[i]; if(!x)return;
    lbOpen(FILT.map(function(y){return {img:y.img,cap:'<b>'+esc(y.t||'')+'</b> '+esc(y.desc||'')
      +(y.note?'<br><span style="opacity:.82">'+esc(y.note)+'</span>':'')
      +'<br><span style="opacity:.7">'+esc(y.title)+' · '+esc(y.upper)+'</span>'}}),i,x.title+' · '+(x.t||''));
  });
  apply();
}
window.addEventListener('DOMContentLoaded',boot);
"""

PAGE_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>关键帧画廊 · 数据宝库</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🖼</text></svg>">
<style>__CSS__</style>
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="gem">◆</span>数据宝库 <small>关键帧 __N__ 张</small></div>
  <nav class="tnav">
    <a href="index.html">入口</a>
    <a href="transcripts.html">文稿全文库</a>
    <a href="gallery.html" class="on">关键帧画廊</a>
    <a href="projects/bilibili-kb/graph/kb.html">网图浏览器</a>
  </nav>
  <span class="spacer"></span>
  <span class="muted" style="font-size:12.4px;white-space:nowrap">VLM 逐帧判读 · 画面即证据</span>
</header>

<div class="gal">
  <div class="gbar">
    <span id="fColl" style="display:flex;gap:6px;flex-wrap:wrap"></span>
    <span id="fType" style="display:flex;gap:6px;flex-wrap:wrap"></span>
    <select id="fVid"></select>
    <label class="field" style="flex:1;max-width:330px;margin-left:auto">
      <span class="muted">🔍</span>
      <input id="q" placeholder="在画面描述里搜：字幕 / 场景 / 人物…" autocomplete="off">
      <span class="kbd">/</span>
    </label>
    <span class="cnt" id="cnt"></span>
  </div>
  <div class="scroll" id="scroll">
    <div class="empty" id="empty" style="display:none;padding:60px;text-align:center;color:var(--ink3)">没有匹配的关键帧</div>
    <div class="mason" id="mason"></div>
    <div class="sentinel" id="sent"></div>
  </div>
</div>

<script>window.__GAL__=__GAL_JSON__;window.__COLS__=__COLS_JSON__;</script>
<script>__JS__</script>
</body>
</html>
"""
