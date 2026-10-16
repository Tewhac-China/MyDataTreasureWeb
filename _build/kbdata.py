# -*- coding: utf-8 -*-
"""MyDataTreasureWeb 门户构建 · 数据装载层

把 projects/*/graph/*.json 里的节点数据统一规范化，供门户 / 文稿库 / 关键帧画廊复用。
对外只暴露一个 build_payload()，返回 (core, full, gallery, stats, apps)。
"""
import ast
import collections
import datetime
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TYPE_CN = {'text': '文本型', 'hybrid': '混合型', 'visual': '画面型'}
TYPE_ORDER = ['text', 'hybrid', 'visual']


def _posix(p):
    return p.replace('\\', '/')


def _load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _as_list(v):
    """data.json 里 entities/keyframes 曾被序列化成 python repr 字符串，这里做兼容。"""
    if isinstance(v, list):
        return v
    if isinstance(v, str) and v.strip():
        try:
            got = ast.literal_eval(v)
            return got if isinstance(got, list) else []
        except Exception:
            return []
    return []


# ---------------------------------------------------------------- 项目扫描
def scan_projects():
    """扫描 projects/*/，返回每个项目可用的可视化入口与数据文件。"""
    out = []
    base = os.path.join(ROOT, 'projects')
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        pdir = os.path.join(base, name)
        if not os.path.isdir(pdir):
            continue
        gdir = os.path.join(pdir, 'graph')
        data_files = {}
        for fn in ('data_all.json', 'data.json'):
            fp = os.path.join(gdir, fn)
            if os.path.isfile(fp):
                data_files[fn] = fp
        pages = []
        for fn, label, needs_server in (
            ('kb_all.html', '合并视图网图浏览器', False),
            ('kb.html', '网图浏览器', False),
            ('index_all.html', 'Canvas 静态图谱（全部）', True),
            ('index.html', 'Canvas 静态图谱', True),
        ):
            fp = os.path.join(gdir, fn)
            if os.path.isfile(fp):
                pages.append({
                    'file': _posix(os.path.relpath(fp, ROOT)),
                    'label': label,
                    'size': os.path.getsize(fp),
                    'server': needs_server,
                })
        if not data_files and not pages:
            continue
        out.append({
            'key': name,
            'dir': _posix(os.path.relpath(pdir, ROOT)),
            'name': name,
            'data': {k: _posix(os.path.relpath(v, ROOT)) for k, v in data_files.items()},
            'pages': pages,
        })
    return out


# ---------------------------------------------------------------- 节点规范化
def load_nodes():
    """以 projects/*/graph/data_all.json 为主源（含 collection 字段与全文 md），
    缺失时回退 data.json。返回 (nodes, collections, sources, extra)。"""
    sources = []
    books = {}          # nid -> 记录（保持插入顺序）
    extra = {'edges': 0, 'files': [], 'raw_nodes': 0, 'dual': []}
    for proj in scan_projects():
        picked = proj['data'].get('data_all.json') or proj['data'].get('data.json')
        if not picked:
            continue
        sources.append(picked)
        extra['files'].append({'path': picked, 'size': os.path.getsize(os.path.join(ROOT, picked.replace('/', os.sep)))})
        d = _load_json(os.path.join(ROOT, picked.replace('/', os.sep)))
        extra['edges'] += len(d.get('edges', []))
        coll_dir = os.path.dirname(picked)          # projects/<p>/graph
        pdir = os.path.dirname(coll_dir)            # projects/<p>
        default_coll = os.path.basename(pdir)
        for raw in d.get('nodes', []):
            nid = raw.get('id') or raw.get('bvid')
            if not nid:
                continue
            extra['raw_nodes'] += 1
            coll = raw.get('collection') or default_coll
            coll_name = raw.get('collectionName') or coll
            coll_color = raw.get('collColor') or ('#6366f1' if coll == 'opinion' else '#10b981')
            # 关键帧图片：原始路径相对该库的 nodes/ 目录（..\raw\x.jpg），这里改写成相对仓库根
            img_base = os.path.join(pdir, 'raw') if coll not in ('kepu',) else os.path.join(pdir, 'kepu', 'raw')
            alt_base = os.path.join(pdir, 'kepu', 'raw') if coll not in ('kepu',) else os.path.join(pdir, 'raw')
            kfs = []
            for k in _as_list(raw.get('keyframes')):
                if not isinstance(k, dict):
                    continue
                src = _posix(k.get('img') or '')
                bn = os.path.basename(src)
                rel = ''
                if bn:
                    for b in (img_base, alt_base):
                        fp = os.path.join(b, bn)
                        if os.path.isfile(fp):
                            rel = _posix(os.path.relpath(fp, ROOT))
                            break
                kfs.append({
                    't': (k.get('t') or '').strip(),
                    'desc': (k.get('desc') or '').strip(),
                    'note': (k.get('note') or '').strip(),
                    'img': rel,
                })
            imgs_ok = [k for k in kfs if k['img']]
            # 正文里的图片引用（..\raw\ / ../raw/ / ..\raw_thumb\）改写成仓库根相对
            md = raw.get('md') or ''
            md_base = _posix(os.path.relpath(img_base, ROOT))
            md = re.sub(r'\.\.[\\/]raw[\\/]', md_base + '/', md)
            md_thumb = os.path.join(pdir, 'raw_thumb')
            if os.path.isdir(md_thumb):
                md = re.sub(r'\.\.[\\/]raw_thumb[\\/]', _posix(os.path.relpath(md_thumb, ROOT)) + '/', md)
            ents = [str(x).strip() for x in _as_list(raw.get('entities')) if str(x).strip()]
            # 深链：kb.html 只含主库，kb_all.html 含合并库 —— 用 #n=BVxxx 直接定位节点
            gbase = os.path.join(pdir, 'graph')
            gpage = 'kb_all.html' if (coll == 'kepu' and os.path.isfile(os.path.join(gbase, 'kb_all.html'))) else 'kb.html'
            if not os.path.isfile(os.path.join(gbase, gpage)):
                gpage = 'index.html'
            graph_link = _posix(os.path.relpath(os.path.join(gbase, gpage), ROOT)) + '#n=' + nid
            rec = {
                'id': nid,
                'title': (raw.get('title') or nid).strip(),
                'upper': (raw.get('upper') or '未知UP主').strip(),
                'duration': (raw.get('duration') or '').strip(),
                'url': (raw.get('url') or ('https://www.bilibili.com/video/%s/' % nid)).strip(),
                'type': (raw.get('type') or 'text').lower(),
                'coll': coll,
                'collName': coll_name,
                'collColor': coll_color,
                'status': raw.get('status') or 'archived',
                'summary': (raw.get('summary') or '').strip(),
                'entities': ents,
                'keyframes': kfs,
                'nImg': len(imgs_ok),
                'nKf': len(kfs),
                'md': md,
                'mdLen': len(md),
                'hasInlineImg': 'class="mdimg"' in md or '![' in md,
                'chars': len(re.sub(r'\s', '', md)),
                'graph': graph_link,
                'dual': [],
            }
            # 同一视频可能同时躺在两个收藏夹里：合并为一条，保留正文更完整的那份
            old = books.get(nid)
            if old is None:
                books[nid] = rec
            else:
                names = sorted(set(old['dual'] + [old['collName'], rec['collName']]))
                keep, drop = (rec, old) if rec['mdLen'] > old['mdLen'] else (old, rec)
                keep['dual'] = names
                keep['nImg'] = max(keep['nImg'], drop['nImg'])
                keep['nKf'] = max(keep['nKf'], drop['nKf'])
                books[nid] = keep
                extra['dual'].append(nid)
    nodes = list(books.values())
    # 合集元信息
    cols = collections.OrderedDict()
    for n in nodes:
        c = cols.setdefault(n['coll'], {
            'key': n['coll'], 'name': n['collName'], 'color': n['collColor'], 'n': 0,
            'kf': 0, 'chars': 0, 'type': collections.Counter(),
        })
        c['n'] += 1
        c['kf'] += n['nImg']
        c['chars'] += n['chars']
        c['type'][n['type']] += 1
    for c in cols.values():
        c['type'] = {k: int(v) for k, v in c['type'].items()}
    return nodes, cols, sources, extra


def build_stats(nodes, cols, extra=None):
    ups = collections.Counter(n['upper'] for n in nodes)
    types = collections.Counter(n['type'] for n in nodes)
    return {
        'docs': len(nodes),
        'kf': sum(n['nImg'] for n in nodes),
        'kfAll': sum(n['nKf'] for n in nodes),
        'kfMiss': sum(n['nKf'] - n['nImg'] for n in nodes),
        'entities': sum(len(n['entities']) for n in nodes),
        'chars': sum(n['chars'] for n in nodes),
        'uppers': len(ups),
        'edges': int((extra or {}).get('edges', 0)),
        'types': {k: int(types.get(k, 0)) for k in TYPE_ORDER},
        'topUps': ups.most_common(12),
        'withMd': sum(1 for n in nodes if n['mdLen'] > 400),
        'dual': int(len((extra or {}).get('dual', []))),
        'rawNodes': int((extra or {}).get('raw_nodes', len(nodes))),
        'cols': cols,
        'built': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
    }


# ---------------------------------------------------------------- 三份载荷
def payload_core(nodes, stats, apps, projects):
    """入口门户用：轻量索引（不含 md 全文）。"""
    return {
        'built': stats['built'],
        'stats': {k: v for k, v in stats.items() if k not in ('cols', 'topUps')},
        'cols': stats['cols'],
        'apps': apps,
        'projects': projects,
        'docs': [{
            'id': n['id'], 'title': n['title'], 'upper': n['upper'], 'dur': n['duration'],
            'type': n['type'], 'coll': n['coll'], 'collName': n['collName'],
            'ents': n['entities'], 'nImg': n['nImg'], 'nKf': n['nKf'], 'chars': n['chars'],
            'url': n['url'], 'dual': n['dual'], 'date': n.get('date', ''),
            'ex': re.sub(r'[*`>#\[\]]|!\[[^\]]*\]\([^)]*\)', '', n['summary'])[:230],
        } for n in nodes],
    }


def payload_full(nodes, stats, apps, projects):
    """文稿全文库用：完整 md 全文 + 关键帧。"""
    return {
        'built': stats['built'],
        'stats': {k: v for k, v in stats.items() if k not in ('topUps',)},
        'cols': stats['cols'],
        'apps': apps,
        'docs': [{
            'id': n['id'], 'title': n['title'], 'upper': n['upper'], 'dur': n['duration'],
            'type': n['type'], 'coll': n['coll'], 'collName': n['collName'],
            'ents': n['entities'], 'nImg': n['nImg'], 'nKf': n['nKf'], 'chars': n['chars'],
            'url': n['url'], 'md': n['md'], 'hasInlineImg': n['hasInlineImg'], 'dual': n['dual'],
            'summary': n['summary'], 'date': n.get('date', ''), 'file': n.get('file', ''),
            'rel': n.get('rel', ''),
            'assets': n.get('assets', []),
            'kf': [{'t': k['t'], 'desc': k['desc'], 'note': k['note'], 'img': k['img']}
                   for k in n['keyframes'] if k['img']],
            'graph': n['graph'],
        } for n in nodes],
    }


def payload_gallery(nodes, stats, cols):
    """关键帧画廊用：只保留有图的帧。"""
    items = []
    for n in nodes:
        for k in n['keyframes']:
            if not k['img']:
                continue
            items.append({
                'img': k['img'], 't': k['t'], 'desc': k['desc'], 'note': k['note'],
                'id': n['id'], 'title': n['title'], 'upper': n['upper'],
                'coll': n['coll'], 'type': n['type'],
            })
    return {'built': stats['built'], 'total': len(items), 'stats': {
        'docs': stats['docs'], 'kf': len(items), 'miss': stats['kfMiss'],
        'uppers': stats['uppers'], 'chars': stats['chars']}, 'items': items}


# 发布载荷里一律不带本机绝对路径：sources.json 的 dir 属于「只在这台机器上
# 有意义」的私密配置，内联进 HTML 就是公开（页面上不显示 ≠ 源码里不存在）。
# 四个内联载荷都走 dump_json，所以在这一处统一摘掉，防止以后新增字段又漏。
# 只做序列化期过滤，不改调用方数据，构建日志仍可打印完整路径。
_DROP_ON_PUBLISH = frozenset({'dir'})


def _public(obj):
    if isinstance(obj, dict):
        return {k: _public(v) for k, v in obj.items() if k not in _DROP_ON_PUBLISH}
    if isinstance(obj, list):
        return [_public(v) for v in obj]
    return obj


def dump_json(obj):
    """安全内联到 <script> 的 JSON。"""
    s = json.dumps(_public(obj), ensure_ascii=False, separators=(',', ':'))
    return s.replace('</', '<\\/').replace('<!--', '<\\!--')


# ---------------------------------------------------------------- 主动归档
ARCHIVE_DIR = '主动归档'


def _first_h1(text, fallback):
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('# '):
            return s[2:].strip()
        if s and not s.startswith('>') and not s.startswith('!'):
            break
    return fallback


def _header_meta(text):
    """从文稿头部抓 来源名 / 外链。返回 (source_name, url)。"""
    name, url = '', ''
    for line in text.splitlines()[:14]:
        s = line.strip()
        if not s:
            continue
        m = re.search(r'\[(https?://[^\]]+)\]\((https?://[^)]+)\)', s)
        if m and not url:
            url = m.group(2)
        m2 = re.search(r'【B站up主】\s*([^【\[\]]+)', s)
        if m2 and not name:
            name = m2.group(1).strip()
            continue
        m3 = re.search(r'来源[：:]\s*(.+)', s)
        if m3 and not name:
            name = re.sub(r'[\[\(].*', '', m3.group(1)).strip(' |·—-')
    return name, url


def _first_para(text):
    """跳过标题/引用/分隔线，取第一段正文做摘要。"""
    cur = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('#') or s.startswith('>') or re.match(r'^-{3,}$', s):
            if cur:
                break
            continue
        if not s:
            if cur:
                break
            continue
        cur.append(s)
    raw = ' '.join(cur)
    raw = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', raw)
    return re.sub(r'[*`#\[\]]', '', raw)[:400]


def _entities_from_md(text):
    """复用整理稿里的 `## 抽取概念 / 实体` 章节。"""
    m = re.search(r'^#{2,3}\s*抽取概念\s*/?\s*实体\s*$(.*?)(?=^#{1,3}\s|\Z)', text, re.S | re.M)
    if not m:
        return []
    out = []
    for line in m.group(1).splitlines():
        mm = re.match(r'\s*[-*]\s*\*\*(.+?)\*\*', line)
        if mm:
            out.append(mm.group(1).strip().rstrip('：:').strip())
    return out[:24]


def _parse_md_doc(fp, coll, coll_name, coll_color, prefix, base_for_rel):
    """把一份整理稿 md 解析成与图谱节点同构的记录（主动归档 / UP主全转录共用）。

    - 标题取首个 `# `；来源名读 `【B站up主】xxx`（退 `来源：`）；外链读 `[文字](url)`
    - 摘要取首段；概念读 `## 抽取概念 / 实体`
    - 正文内联图片按 md 所在目录解析 → 改写成仓库根相对路径，并逐张校验存在性
    - base_for_rel 用来算可读的 file / rel（用于面包屑）
    """
    try:
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            md = f.read()
    except OSError:
        return None
    d = os.path.dirname(fp)
    stem = os.path.splitext(os.path.basename(fp))[0]
    nid = prefix + re.sub(r'[&=#\s]+', '_', stem)
    assets, missing = [], []
    for m in re.finditer(r'!\[[^\]]*\]\(([^)\s]+)\)', md):
        ref = _posix(m.group(1))
        if ref.startswith(('http://', 'https://', 'data:')):
            continue
        target = os.path.normpath(os.path.join(d, ref.replace('/', os.sep)))
        if os.path.isfile(target):
            rel = _posix(os.path.relpath(target, ROOT))
            md = md.replace(m.group(1), rel)
            assets.append(rel)
        else:
            missing.append(ref)
    if '关键帧图说' in md:
        t = 'hybrid'
    elif assets:
        t = 'visual'
    else:
        t = 'text'
    try:
        mt = datetime.datetime.fromtimestamp(os.path.getmtime(fp)).strftime('%Y-%m-%d')
    except OSError:
        mt = ''
    src, url = _header_meta(md)
    return {
        'id': nid,
        'title': _first_h1(md, stem),
        'upper': src or '自建文稿',
        'duration': '',
        'url': url,
        'type': t,
        'coll': coll,
        'collName': coll_name,
        'collColor': coll_color,
        'status': 'archived',
        'summary': _first_para(md),
        'entities': _entities_from_md(md),
        'keyframes': [],
        'nImg': len(assets),
        'nKf': len(assets),
        'md': md,
        'mdLen': len(md),
        'hasInlineImg': bool(assets),
        'chars': len(re.sub(r'\s', '', md)),
        'graph': '',
        'dual': [],
        'file': _posix(os.path.relpath(fp, ROOT)),
        'rel': _posix(os.path.relpath(fp, base_for_rel)),
        'date': mt,
        'assets': assets,
        'missingAssets': missing,
    }


def _walk_md(root, skip_names=()):
    """递归列出目录下的 .md（跳过 `_`/`.` 开头与 skip_names）。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(('.', '_'))]
        for fn in sorted(filenames):
            if not fn.lower().endswith('.md') or fn.startswith(('.', '_')):
                continue
            if fn in skip_names:
                continue
            yield os.path.join(dirpath, fn)


def load_archive():
    """扫描「主动归档」目录里的 md 文稿。

    约定见 `主动归档/_归档说明.txt`：以后自动转录/整理出来的文稿直接放这里，
    重跑 build_portal.py 即自动收录。
    """
    root = os.path.join(ROOT, ARCHIVE_DIR)
    if not os.path.isdir(root):
        return []
    docs = []
    for fp in _walk_md(root):
        doc = _parse_md_doc(fp, 'archive', '主动归档', '#f59e0b', 'AR-', root)
        if doc:
            docs.append(doc)
    return docs


# ------------------------------------------------- 额外来源（UP主全转录等）
SOURCES_FILE = os.path.join('_build', 'sources.json')


def load_sources():
    """按 `_build/sources.json` 配置扫描额外的「全转录」来源目录。

    返回 (docs, groups, problems)：
      docs     规范化后的稿件（coll=source.key，group=source.group）
      groups   板块分组元信息，供门户单独成板块（不与收藏夹分支混算）
      problems 目录不存在 / 通配无命中等，交由构建日志提示
    """
    cfg_path = os.path.join(ROOT, SOURCES_FILE)
    if not os.path.isfile(cfg_path):
        return [], [], []
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except Exception as e:
        return [], [], ['sources.json 解析失败: %s' % e]
    skip = set(cfg.get('skipFiles') or [])
    docs, groups, problems = [], collections.OrderedDict(), []
    for s in cfg.get('sources', []):
        if not s.get('dir'):
            continue
        pat = s['dir'].replace('\\', '/')
        if not os.path.isabs(pat):
            pat = _posix(os.path.join(ROOT, pat))
        root, found = '', []
        if '*' in pat:
            import glob as _glob
            hits = sorted(_glob.glob(pat))
            if hits:
                root = os.path.commonpath(hits)
                for h in hits:
                    for fp in _walk_md(h, skip):
                        found.append(fp)
            else:
                problems.append('通配无命中: %s' % pat)
        else:
            root = pat.rstrip('/')
            if os.path.isdir(root):
                found = list(_walk_md(root, skip))
            else:
                problems.append('目录不存在: %s' % root)
        key = s.get('key') or 'src'
        name = s.get('name') or key
        color = s.get('color') or '#0ea5e9'
        group = s.get('group') or 'upfull'
        gname = s.get('groupName') or '额外来源'
        n0 = len(docs)
        for fp in found:
            doc = _parse_md_doc(fp, key, name, color, 'SR-%s-' % key, root)
            if doc:
                doc['group'] = group
                doc['src'] = key
                docs.append(doc)
        groups.setdefault(group, {'key': group, 'name': gname, 'items': []})
        groups[group]['items'].append({
            'key': key, 'name': name, 'color': color, 'dir': _posix(root),
            'note': s.get('note', ''), 'n': len(docs) - n0,
            'chars': sum(x['chars'] for x in docs[n0:]),
            'group': group, 'groupName': gname,
        })
    return docs, list(groups.values()), problems
