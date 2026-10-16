# -*- coding: utf-8 -*-
"""build_portal.py — MyDataTreasureWeb 门户构建入口

用法（在本仓库根目录的上一级无所谓，脚本自己定位根）：
    python _build/build_portal.py

产出（全部自包含，可 file:// 双击打开）：
    index.html          入口门户
    transcripts.html    文稿全文库（内联全部整理稿）
    gallery.html        关键帧画廊（内联全部关键帧元数据 + 相对路径图片）

只依赖标准库。数据源：projects/*/graph/data_all.json（回退 data.json）。
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import kbdata            # noqa: E402
import theme             # noqa: E402
import page_portal       # noqa: E402
import page_transcripts  # noqa: E402
import page_gallery      # noqa: E402

ROOT = kbdata.ROOT

# 页面注册表：键为 graph 目录下的文件名
APP_META = {
    'kb.html': dict(
        icon='🕸', title='网图浏览器 · 主库', key='k1',
        sub='有意思的想法et观点',
        desc='Canvas 力导向网图：语义检索（LSI）、关键字检索、概念浏览器、二阶邻居高亮、社区着色、拖拽钉住、关键帧灯箱。可 <span class="mono">#n=BV号</span> 直达节点。',
        chips=['{opinion} 节点', '{opinion_edges} 条边', '语义索引'],
    ),    'kb_all.html': dict(
        icon='🌐', title='网图浏览器 · 合并视图', key='k2',
        sub='观点 + 好的科普',
        desc='把两个收藏夹放进同一张网：跨库共享概念自动连边，适合追一个概念在两批视频里怎么被反复讲到。',
        chips=['{rawNodes} 节点', '{edges} 条边', '跨库共享概念'],
    ),
    'index.html': dict(
        icon='🧭', title='Canvas 静态图谱', key='k5', server=True,
        sub='轻量只读版（读 data.json）',
        desc='早期静态版：预迭代收敛布局、分级重力、度数半径。需要本地服务才能读取 JSON。',
        chips=['需本地服务', 'data.json'],
    ),
    'index_all.html': dict(
        icon='🗺', title='Canvas 静态图谱 · 全部', key='k5', server=True,
        sub='轻量只读版（读 data_all.json）',
        desc='合并库的静态图谱版本，同样需要本地服务。日常看图建议直接用上面两张自包含页面。',
        chips=['需本地服务', 'data_all.json'],
    ),
}


def build_apps(projects, stats):
    """按优先级拼出入口卡片列表。"""
    order = ['kb.html', 'kb_all.html', None, 'transcripts.html', 'gallery.html', None,
             'ARCHIVE', None, 'index.html', 'index_all.html']
    pages = {}
    proj = projects[0] if projects else None
    if proj:
        for p in proj['pages']:
            pages[os.path.basename(p['file'])] = p
    repl = {
        'docs': stats['docs'], 'edges': stats['edges'], 'kf': stats['kf'],
        'kfAll': stats['kfAll'], 'entities': stats['entities'],
        'chars_wan': '%.1f' % (stats['chars'] / 10000.0), 'uppers': stats['uppers'],
        'opinion': stats['cols'].get('opinion', {}).get('n', 0),
        'kepu': stats['cols'].get('kepu', {}).get('n', 0),
        'opinion_edges': 0, 'kepu_edges': 0, 'rawNodes': stats['rawNodes'],
    }
    # 主库 kb.html / 合并视图的真实规模取自 graph/data.json 与 data_all.json
    try:
        import json
        dj = os.path.join(ROOT, 'projects', 'bilibili-kb', 'graph', 'data.json')
        if os.path.isfile(dj):
            with open(dj, 'r', encoding='utf-8') as f:
                d = json.load(f)
            repl['opinion_edges'] = len(d.get('edges', []))
            if d.get('nodes'):
                repl['opinion'] = len(d['nodes'])
    except Exception:
        pass
    apps = []
    for key in order:
        if key is None:
            continue
        if key == 'transcripts.html':
            apps.append(dict(icon='📚', title='文稿全文库', key='k3', sub='%d 篇整理稿 · 全文可检索' % stats['docs'],
                             desc='左侧按库 / 类型 / UP主 过滤，右侧渲染完整整理稿：概要、正文、关键帧图说、抽取的概念与实体。支持 <span class="mono">#q=关键词</span> 全文检索与深链。',
                             chips=['%d 篇' % stats['docs'], '%.1f 万字' % (stats['chars'] / 10000.0), '全文检索'],
                             href='transcripts.html'))
            continue
        if key == 'gallery.html':
            apps.append(dict(icon='🖼', title='关键帧画廊', key='k4', sub='VLM 逐帧判读的真实画面',
                             desc='把所有视频的关键帧摊平成一整面图墙，按画面描述、字幕内容直接搜画面，点开可翻页、可跳回对应文稿。',
                             chips=['%d 张' % stats['kf'], '%d 个视频' % stats['docs']],
                             href='gallery.html'))
            continue
        if key == 'ARCHIVE':
            n = stats['arch']
            apps.append(dict(
                icon='📥', title='主动归档', key='k4',
                sub=('新转录 / 新整理文稿的投放目录' if n else '投放目录已就位 · 还没有稿件'),
                desc='以后自动转录、自动整理出来的文稿直接丢进 <span class="mono">主动归档/</span> 就会出现在这里：'
                     '可全文检索、可阅读、有目录。收录范围与命名约定见该目录下的说明。',
                chips=(['%d 篇' % n, '%.1f 万字' % (stats['archChars'] / 10000.0), '重跑生成器即收录'] if n
                       else ['0 篇', '目录已建好', '放 md 后重跑生成器']),
                href='transcripts.html#c=archive'))
            continue
        if key not in pages:
            continue
        meta = dict(APP_META[key])
        chips = [c.format(**repl) for c in meta.pop('chips', [])]
        apps.append(dict(href=pages[key]['file'], chips=chips, server=meta.pop('server', False), **meta))
    return apps


def render(tpl, reps):
    """两轮替换：CSS/JS 大块里也可能带占位符（例如 JS 里写 __ARCHDIR__），
    如果只替换一轮，结果就依赖 reps 的键顺序，太脆。两轮保证嵌套占位符都能落地。"""
    out = tpl
    for _ in range(2):
        for k, v in reps.items():
            out = out.replace(k, v)
    return out


def write(path, text):
    p = os.path.join(ROOT, path)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    return p, os.path.getsize(p)


def main():
    t0 = time.time()
    nodes, cols, sources, extra = kbdata.load_nodes()
    if not nodes:
        print('[!] 没找到任何节点数据，检查 projects/*/graph/data_all.json')
        return 1
    import collections
    for c in cols.values():
        c['kind'] = 'fav'
    stats = kbdata.build_stats(nodes, cols, extra)

    # ---- 主动归档：把「主动归档/」里的 md 一并收编 ----
    arch = kbdata.load_archive()
    cols['archive'] = {
        'key': 'archive', 'name': '主动归档', 'color': '#f59e0b', 'n': len(arch),
        'kf': sum(a['nImg'] for a in arch), 'chars': sum(a['chars'] for a in arch),
        'type': {k: int(v) for k, v in collections.Counter(a['type'] for a in arch).items()},
        'kind': 'archive',
    }
    stats['arch'] = len(arch)
    stats['archChars'] = sum(a['chars'] for a in arch)
    stats['archImgs'] = sum(a['nImg'] for a in arch)

    # ---- 额外来源（UP主全转录等）：单独成板块，不与收藏夹分支混算 ----
    srcdocs, srctg, srcprob = kbdata.load_sources()
    src_cols = []
    for g in srctg:
        for it in g['items']:
            keys = [d['coll'] for d in srcdocs]
            grp = [d for d in srcdocs if d['coll'] == it['key']]
            col = {
                'key': it['key'], 'name': it['name'], 'color': it['color'], 'n': len(grp),
                'kf': 0, 'chars': sum(x['chars'] for x in grp),
                'type': {k: int(v) for k, v in collections.Counter(x['type'] for x in grp).items()},
                'kind': 'upfull', 'group': g['key'], 'groupName': g['name'], 'note': it['note'],
                # 构建日志要打印完整路径，这里保留；发布时由 kbdata.dump_json 统一摘除。
                'dir': it['dir'],
            }
            cols[it['key']] = col
            src_cols.append(col)
    stats['src'] = len(srcdocs)
    stats['srcChars'] = sum(d['chars'] for d in srcdocs)
    stats['docsAll'] = stats['docs'] + stats['arch'] + stats['src']
    stats['charsAll'] = stats['chars'] + stats['archChars'] + stats['srcChars']
    allnodes = nodes + arch + srcdocs
    # 门户「知识库构成」只放收藏夹 + 主动归档；UP主全转录走独立板块
    cols_show = collections.OrderedDict((k, v) for k, v in cols.items() if v['kind'] in ('fav', 'archive'))

    projects = kbdata.scan_projects()
    apps = build_apps(projects, stats)

    print('数据源：')
    for f in extra['files']:
        print('  · %-46s %8.2f MB' % (f['path'], f['size'] / 1048576.0))
    print('图谱节点 %d ｜ 边 %d ｜ 关键帧 %d/%d ｜ 概念 %d ｜ 字数 %d ｜ UP %d'
          % (stats['docs'], stats['edges'], stats['kf'], stats['kfAll'], stats['entities'], stats['chars'], stats['uppers']))
    if arch:
        print('主动归档 %d 篇（%d 字 / %d 张图）：' % (len(arch), stats['archChars'], stats['archImgs']))
        for a in arch:
            flag = '' if not a['missingAssets'] else '  ⚠ 缺图 %d 张' % len(a['missingAssets'])
            print('  · %-42s %s%s' % (a['title'][:42], a['date'], flag))
            for mv in a['missingAssets']:
                print('      ! 图片不存在: %s' % mv)
    else:
        print('主动归档 0 篇（把 md 放进 %s/ 后重跑本脚本即会自动收录）' % kbdata.ARCHIVE_DIR)

    if src_cols:
        print('额外来源（%s 板块，不计入收藏夹口径）：' % (srctg[0]['name'] if srctg else '额外来源'))
        for c in src_cols:
            print('  · %-16s %4d 篇  %6.1f 万字  %s' % (c['name'], c['n'], c['chars'] / 10000.0, c['dir']))
    for p in srcprob:
        print('  ⚠ %s' % p)
    print('口径：收藏夹 %d 篇 ｜ 主动归档 %d 篇 ｜ 全转录 %d 篇 ｜ 合计 %d 篇'
          % (stats['docs'], stats['arch'], stats['src'], stats['docsAll']))

    written = []
    # ---------- index.html ----------
    core = kbdata.payload_core(allnodes, stats, apps, projects)
    core['cols'] = cols_show                 # 门户的「知识库构成」只看收藏夹 + 主动归档
    core['srcCols'] = src_cols               # 独立板块：UP主全转录
    core['groups'] = srctg
    core['stats']['docsFav'] = stats['docs']
    html = render(page_portal.PAGE_HTML, {
        '__CSS__': theme.BASE_CSS + page_portal.PAGE_CSS,
        '__JS__': theme.SHARED_JS + page_portal.PAGE_JS,
        '__CORE_JSON__': kbdata.dump_json(core),
        '__BUILT__': stats['built'],
        '__KFTOTAL__': '%d' % stats['kf'],
        '__NODES__': '%d' % stats['docs'],
        '__DUAL__': '%d' % stats['dual'],
        '__ARCH__': '%d' % stats['arch'],
        '__ARCHDIR__': kbdata.ARCHIVE_DIR,
    })
    written.append(write('index.html', html))

    # ---------- transcripts.html ----------
    full = kbdata.payload_full(allnodes, stats, apps, projects)
    html = render(page_transcripts.PAGE_HTML, {
        '__CSS__': theme.BASE_CSS + page_transcripts.PAGE_CSS,
        '__JS__': theme.SHARED_JS + page_transcripts.PAGE_JS,
        '__FULL_JSON__': kbdata.dump_json(full),
        '__N__': '%d' % stats['docsAll'],
        '__CHARS__': '%.1f' % (stats['charsAll'] / 10000.0),
        '__ARCH__': '%d' % stats['arch'],
    })
    written.append(write('transcripts.html', html))

    # ---------- gallery.html ----------
    gal = kbdata.payload_gallery(nodes, stats, cols)
    colcards = [{'k': c['key'], 'n': c['name'], 'color': c['color'], 'cnt': c['n']} for c in cols.values()]
    html = render(page_gallery.PAGE_HTML, {
        '__CSS__': theme.BASE_CSS + page_gallery.PAGE_CSS,
        '__JS__': theme.SHARED_JS + page_gallery.PAGE_JS,
        '__GAL_JSON__': kbdata.dump_json(gal),
        '__COLS_JSON__': kbdata.dump_json(colcards),
        '__N__': '%d' % stats['kf'],
    })
    written.append(write('gallery.html', html))

    print('\n产出：')
    for p, size in written:
        print('  · %-22s %7.2f MB' % (os.path.basename(p), size / 1048576.0))
    print('完成，用时 %.1fs' % (time.time() - t0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
