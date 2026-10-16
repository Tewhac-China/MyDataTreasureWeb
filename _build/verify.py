# -*- coding: utf-8 -*-
"""verify.py — 门户产物自检

检查项：
1. 模板占位符是否全部替换（不应残留 __XXX__）
2. 内联 <script> 的 JS 语法（调用 node --check）
3. 页面内引用的本地资源（img src / href）是否真实存在
4. 是否误引外部资源（CDN / http 资源），file:// 下会失败

用法：python _build/verify.py
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PAGES = ['index.html', 'transcripts.html', 'gallery.html']
NODE = os.environ.get('NODE_BIN') or r'C:\Users\11305\.workbuddy\binaries\node\versions\22.22.2\node.exe'

fails = []
warns = []


def check_placeholders(name, text):
    # 排除 JS 全局量（window.__CORE__ 之类），只认模板占位符
    left = set(re.findall(r'(?<![.\w])__[A-Z][A-Z0-9_]{2,}__', text))
    if left:
        fails.append('%s 残留占位符: %s' % (name, ', '.join(sorted(left))))
    return not left


def check_script(name, text):
    blocks = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', text, re.S)
    if not blocks:
        warns.append('%s 没有内联 script' % name)
        return
    for i, b in enumerate(blocks):
        tmp = os.path.join(tempfile.gettempdir(), '_chk_%s_%d.js' % (name.replace('.html', ''), i))
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            f.write(b)
        try:
            p = subprocess.run([NODE, '--check', tmp], capture_output=True, text=True, timeout=60)
            if p.returncode != 0:
                fails.append('%s 第%d个script JS 语法错误:\n%s' % (name, i + 1, (p.stderr or '').strip()[:700]))
            else:
                print('  · %s script#%d 语法 OK (%.1f KB)' % (name, i + 1, len(b) / 1024.0))
        except FileNotFoundError:
            warns.append('找不到 node，跳过语法检查')
            return
        finally:
            try:
                os.remove(tmp)
            except OSError:
                pass


def check_assets(name, text):
    """检查静态 HTML 属性里的本地路径（JS 里运行时拼接的忽略）。"""
    miss, ok = [], 0
    for m in re.finditer(r'\b(?:src|href)="([^"#]+?)"', text):
        u = m.group(1)
        if u.startswith(('http:', 'https:', 'data:', 'mailto:', 'javascript:')) or u in ('', '#'):
            continue
        if os.path.splitext(u)[1] == '':      # 形如 '+u+' 的运行时拼接，跳过
            continue
        if "'" in u or '+' in u:              # JS 字符串拼接片段，非静态路径
            continue
        u = u.split('#')[0].split('?')[0]
        if os.path.exists(os.path.join(ROOT, u.replace('/', os.sep))):
            ok += 1
        else:
            miss.append(u)
    if miss:
        uniq = sorted(set(miss))
        fails.append('%s 有 %d 个静态路径不存在: %s' % (name, len(uniq), ', '.join(uniq[:6])))
    print('  · %s 静态属性资源 %d 处，缺失 %d 处' % (name, ok, len(set(miss))))


def check_inline_data(name, text):
    """把内联 JSON 里的图片路径全部落盘校验（最关键的 file:// 可用性检查）。"""
    import json
    imgs, bad = [], []
    for key in ('__CORE__', '__FULL__', '__GAL__'):
        m = re.search(r'window\.%s\s*=\s*(\{.*?\});\s*</script>' % key, text, re.S)
        if not m:
            continue
        raw = m.group(1).replace('<\\/', '</')
        try:
            obj = json.loads(raw)
        except Exception as e:
            fails.append('%s 内联 %s JSON 解析失败: %s' % (name, key, e))
            continue
        stack = [obj]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                for k, v in cur.items():
                    if k in ('img', 'src') and isinstance(v, str) and v:
                        imgs.append(v)
                    elif k == 'assets' and isinstance(v, list):
                        imgs.extend([x for x in v if isinstance(x, str) and x])
                    elif isinstance(v, (dict, list)):
                        stack.append(v)
            elif isinstance(cur, list):
                stack.extend(x for x in cur if isinstance(x, (dict, list)))
    for u in imgs:
        if not os.path.exists(os.path.join(ROOT, u.replace('/', os.sep))):
            bad.append(u)
    print('  · %s 内联数据含图片路径 %d 条，缺失 %d 条' % (name, len(imgs), len(set(bad))))
    if bad:
        fails.append('%s 内联图片路径缺失 %d 条，例如: %s' % (name, len(set(bad)), ', '.join(sorted(set(bad))[:5])))


def check_external(name, text):
    ext = set(re.findall(r'<(?:script|link|img|iframe)[^>]*\b(?:src|href)="(https?://[^"]+)"', text))
    if ext:
        fails.append('%s 引用了外部资源（file:// 下可能挂）: %s' % (name, ', '.join(sorted(ext)[:4])))
    else:
        print('  · %s 无外部资源依赖 ✔' % name)


def main():
    print('产物自检：')
    for name in PAGES:
        p = os.path.join(ROOT, name)
        if not os.path.isfile(p):
            fails.append('%s 不存在' % name)
            continue
        size = os.path.getsize(p)
        with open(p, 'r', encoding='utf-8') as f:
            t = f.read()
        print('\n[%s] %.2f MB' % (name, size / 1048576.0))
        check_placeholders(name, t)
        check_external(name, t)
        check_assets(name, t)
        check_inline_data(name, t)
        check_script(name, t)
    print('\n' + '=' * 60)
    for w in warns:
        print('[警告] ' + w)
    if fails:
        for f in fails:
            print('[失败] ' + f)
        print('\n自检未通过：%d 项失败 / %d 项警告' % (len(fails), len(warns)))
        return 1
    print('自检通过 ✔ （警告 %d 项）' % len(warns))
    return 0


if __name__ == '__main__':
    sys.exit(main())
