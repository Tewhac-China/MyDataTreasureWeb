<div align="center">

# 数据宝库 · MyDataTreasure

**把 B 站收藏夹变成可检索、可追线、可回看的个人知识库**
*Turning Bilibili favorites into a searchable, traceable, re-watchable personal knowledge base*

<br/>

<a href="https://tewhac-china.github.io/MyDataTreasureWeb/">
<img src="https://img.shields.io/badge/🚀_打开数据宝库_Launch_the_UI-2563EB?style=for-the-badge&logo=githubpages&logoColor=white" alt="打开数据宝库 / Launch the UI"/>
</a>

<br/>
<br/>

👆 **点上面这个按钮直接访问在线 UI** · *Click the button above to open the live site*
**无需安装、无需账号、纯静态页面** · *No install, no account, fully static*

[![GitHub Pages](https://img.shields.io/badge/status-live%20on%20GitHub%20Pages-brightgreen)](https://tewhac-china.github.io/MyDataTreasureWeb/)
![Tech](https://img.shields.io/badge/built%20with-Python%20stdlib%20%2B%20vanilla%20JS-blue)
![Runtime deps](https://img.shields.io/badge/runtime%20dependencies-none-informational)

</div>

---

## 这是什么 · What is this

**中文** — 「数据宝库」是一套跑在本地的 B 站知识内容整理流水线，以及它产出的静态阅读界面。收藏夹里的视频先经 ASR 转录 / 硬字幕 OCR 得到整理稿，再用视觉模型逐帧判读关键画面，最后把跨视频反复出现的概念连成一张网。整个界面没有任何后端：四个页面全部自包含，构建脚本只依赖 Python 标准库。

**English** — *MyDataTreasure* is a local pipeline for processing Bilibili content, plus the static reading interface it produces. Videos from my favorites are turned into clean transcripts via ASR (or OCR for burned-in subtitles), their key frames are described by a vision model, and concepts that recur across videos are linked into a force-directed graph. The UI has no backend: every page is self-contained, and the generator uses only the Python standard library.

---

## 四个模块 · Four modules

<a href="https://tewhac-china.github.io/MyDataTreasureWeb/">
<img src="https://img.shields.io/badge/🧭_入口门户_Portal-1f6feb?style=for-the-badge" alt="Portal"/></a>
<a href="https://tewhac-china.github.io/MyDataTreasureWeb/transcripts.html">
<img src="https://img.shields.io/badge/📚_文稿全文库_Transcripts-0891b2?style=for-the-badge" alt="Transcripts"/></a>
<a href="https://tewhac-china.github.io/MyDataTreasureWeb/gallery.html">
<img src="https://img.shields.io/badge/🖼_关键帧画廊_Keyframes-7c3aed?style=for-the-badge" alt="Keyframe gallery"/></a>
<a href="https://tewhac-china.github.io/MyDataTreasureWeb/projects/bilibili-kb/graph/kb_all.html">
<img src="https://img.shields.io/badge/🌐_概念网图浏览器_Graph%20explorer-059669?style=for-the-badge" alt="Concept graph"/></a>

| 模块 · Module | 能做什么 · What it does |
|---|---|
| **🧭 入口门户 · Portal**<br/>[`index.html`](https://tewhac-china.github.io/MyDataTreasureWeb/) | 知识库构成总览、项目与文件清单、文稿速览、使用说明。<br/>Overview of the corpus, file inventory, and a document preview feed. |
| **📚 文稿全文库 · Transcripts**<br/>[`transcripts.html`](https://tewhac-china.github.io/MyDataTreasureWeb/transcripts.html) | 234 篇整理稿全文，按库 / 类型 / UP 主过滤，左侧筛选右侧阅读；每篇带概要、关键帧图说、抽取出的概念与实体。支持 `#q=关键词` 全文检索与 `#id=` 深链。<br/>All 234 cleaned-up transcripts with facet filters, per-document summaries, key-frame captions, extracted concepts/entities. Hash-based full-text search and deep links. |
| **🖼 关键帧画廊 · Keyframe gallery**<br/>[`gallery.html`](https://tewhac-china.github.io/MyDataTreasureWeb/gallery.html) | 1331 张真实画面摊平成一面图墙，可以直接按**画面描述**或**画面里的字幕**搜图，点开翻页、跳回对应文稿。<br/>1,331 real frames on one wall — search by what the picture shows or by the on-screen subtitle text, then jump back to the matching transcript. |
| **🌐 概念网图浏览器 · Graph explorer**<br/>[主库 · opinion](https://tewhac-china.github.io/MyDataTreasureWeb/projects/bilibili-kb/graph/kb.html) · [合并视图 · merged](https://tewhac-china.github.io/MyDataTreasureWeb/projects/bilibili-kb/graph/kb_all.html) · [科普库 · science](https://tewhac-china.github.io/MyDataTreasureWeb/projects/bilibili-kb/kepu/graph/kb.html) | Canvas 力导向图：LSI 语义检索、关键字检索、概念浏览器、二阶邻居高亮、社区着色、拖拽钉住、关键帧灯箱；`#n=BV号` 直达节点。合并视图把两个收藏夹放进同一张网，共享概念自动连边。<br/>Canvas force-directed graph with LSI semantic search, keyword search, concept browser, 2nd-order neighbour highlighting, community colouring, draggable pinning and a keyframe lightbox. The merged view overlays both collections so shared concepts link across them. |

---

## 数据规模 · By the numbers

| | 中文 | English | 数量 · Count |
|---|---|---|---|
| 📄 | 整理稿 | Cleaned transcripts | **234** 篇 |
| ✍️ | 正文字数 | Characters of prose | **51.7 万** · ~517k |
| 🖼 | 关键帧 | Key frames | **1,331** 张 |
| 🎙 | 涉及 UP 主 | UP-loaders covered | **189** 位 |
| 🏷 | 抽取实体 | Extracted entities | **2,623** 个 |
| 🕸 | 概念图节点 / 边 | Graph nodes / edges | 观点集 **176 / 358** · 科普 **64 / 69** · 合并 **240 / 427** |

---

## 技术栈 · Tech stack

**中文** — 生成端：Python 3，只用标准库（`_build/` 下按页面拆模块）。展示端：单文件 HTML + 原生 JS + Canvas，无框架、无打包器、无 CDN、无 runtime 依赖；文稿与元数据直接内联进页面。门户、文稿库、画廊和两张 `kb.html` 完全自包含，`file://` 双击即开；合并视图 `kb_all.html` 与早期轻量只读版（`index.html`/`index_all.html`）靠 `fetch()` 取 `data.json`/`data_all.json`，必须走 HTTP——**部署到 GitHub Pages 后这条约束自动消失**，本地则要起服务。

**English** — Generation: Python 3, standard library only (split per page under `_build/`). Presentation: single-file HTML + vanilla JS + Canvas — no framework, no bundler, no CDN, no runtime dependencies. The portal, transcripts, gallery and the two `kb.html` views are fully self-contained and open straight from `file://`. The merged view `kb_all.html` and the legacy read-only pages (`index.html` / `index_all.html`) pull `data.json` / `data_all.json` via `fetch()`, so they require HTTP — **which goes away automatically once the site is on GitHub Pages**; locally you need a server for those.

---

## 本地运行 · Running it locally

```bash
# 1) 直接双击打开（全部页面都是自包含的）/ Just open these — all self-contained
index.html  transcripts.html  gallery.html
projects/bilibili-kb/graph/kb.html
projects/bilibili-kb/kepu/graph/kb.html

# 2) 少数页面要 fetch JSON，那些页面需要静态服务器
#    Some pages fetch JSON, so they need a server:
#    kb_all.html · graph/index.html · index_all.html · kepu/graph/index.html
cd MyDataTreasureWeb
python -m http.server 8777
# 然后访问 / then open:
# http://localhost:8777/projects/bilibili-kb/graph/kb_all.html
```

Windows 用户可以直接双击仓库里的 `启动本地服务.bat`（它会自动挑一个本机 Python 起服务并打开入口页）。
On Windows, double-click `启动本地服务.bat` — it picks an available Python, serves the folder, and opens the portal.

## 重新生成页面 · Regenerating

```bash
python _build/build_portal.py     # 重建 index / transcripts / gallery
```
数据源与稿件目录登记在 `_build/sources.json`；加一条就多一个分组卡片。
Source directories are registered in `_build/sources.json`.

---

## 仓库里有什么 · What's in this repo

```
index.html · transcripts.html · gallery.html   三个自包含入口页 · self-contained entry pages
projects/bilibili-kb/graph/                    概念网图页面 + data.json / data_all.json
projects/bilibili-kb/kepu/graph/               科普库的网图页面 + data.json
projects/bilibili-kb/raw/                      关键帧图片（画廊与灯箱按相对路径引用）
projects/bilibili-kb/kepu/raw/                 科普库关键帧
_build/  ·  未上传                            页面生成器（本地保留，仓库只放产物）
```

`.gitignore` 采用**白名单**策略：默认忽略全部，只显式放行上面这些站点文件。所以本地那 99 MB 音频、抓取原始数据、Python 依赖目录、后台采集状态文件和个人文档都不可能不小心被推上来。
The `.gitignore` is a **deny-all whitelist** — everything is ignored unless explicitly listed. Raw audio, scraped source dumps, bundled Python libs, the local collector's status files, and private notes can never leak into this repo by accident.

---

## 版权与免责 · Copyright & disclaimer

**中文** — 站内文稿来自 B 站视频的语音转录或硬字幕识别，是**我个人的学习整理**，用于自用检索与回顾。相关视频、画面与观点的著作权归各自 UP 主与原作者所有；本项目不重新声明对这些内容的所有权，也不用于任何商业用途。如果你在页面上看到自己享有版权的内容并希望我下架，开个 issue 或直接联系我，我会处理。本仓库同样**不构成任何观点背书**。

**English** — The transcripts come from speech-to-text or burned-in-subtitle OCR of Bilibili videos and are **my personal study notes**. Copyright of the source videos, frames, and ideas stays with the original UP-loaders and authors; this repository claims no ownership over that material and is not used commercially. If you see your copyrighted content here and want it taken down, open an issue or contact me and I will handle it. Nothing here is an endorsement of any view expressed in the transcripts.

Code in `_build/`-generated pages: provided as-is, no warranty, no license granted for the underlying third-party content.

---

<div align="center">

<a href="https://tewhac-china.github.io/MyDataTreasureWeb/">
<img src="https://img.shields.io/badge/🚀_再点一次_·_Open_the_UI-2563EB?style=for-the-badge&logo=githubpages&logoColor=white" alt="Open the UI"/></a>

<br/>

Made as a personal knowledge tool · 私人知识工具，边用边改

</div>
