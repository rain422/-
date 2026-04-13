import streamlit as st
import feedparser
from scholarly import scholarly
from datetime import datetime
import time
import urllib.parse

st.set_page_config(
    page_title="BatteryIQ — 배터리 건강 추정 연구 포털",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

:root {
    --teal:    #00B4A0;
    --teal2:   #009688;
    --teal3:   #00796B;
    --navy:    #0D1B2A;
    --navy2:   #1C2E40;
    --gray1:   #F7F8FA;
    --gray2:   #EEF0F3;
    --gray3:   #D4D8DE;
    --gray4:   #9EA5AF;
    --gray5:   #6B7280;
    --white:   #FFFFFF;
    --black:   #0D1B2A;
    --red:     #E8002A;
}

*, *::before, *::after { box-sizing: border-box; margin:0; padding:0; }

html, body, [class*="css"] {
    font-family: 'Noto Sans KR','Plus Jakarta Sans',-apple-system,sans-serif;
    background: var(--white);
    color: var(--black);
}

.stApp { background: var(--white) !important; }
section[data-testid="stSidebar"] { display:none !important; }
[data-testid="stAppViewBlockContainer"] { padding:0 !important; max-width:100% !important; }
.block-container { padding:0 !important; max-width:100% !important; }
#MainMenu, footer, header { visibility:hidden; }
.stDeployButton { display:none; }

/* ── 버튼 공통 ── */
.stButton > button {
    background: transparent !important;
    color: var(--navy) !important;
    border: 1px solid var(--gray3) !important;
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--teal) !important;
    color: var(--white) !important;
    border-color: var(--teal) !important;
}
.stTabs [data-baseweb="tab-list"] { display:none !important; }
.stTabs [data-baseweb="tab-panel"] { padding:0 !important; background:transparent !important; border:none !important; }
textarea {
    background: var(--gray1) !important;
    color: var(--black) !important;
    border: 1px solid var(--gray3) !important;
    border-radius: 4px !important;
    font-size: 0.85rem !important;
}

/* ══════════════════════════════
   GNB (상단 네비)
══════════════════════════════ */
.gnb {
    position: fixed; top:0; left:0; right:0;
    height: 68px;
    background: rgba(255,255,255,0.96);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--gray3);
    display: flex; align-items: center;
    justify-content: space-between;
    padding: 0 52px;
    z-index: 9999;
}
.gnb-logo {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800; font-size: 1.1rem;
    color: var(--navy); letter-spacing: -0.3px;
}
.gnb-logo-mark {
    width: 32px; height: 32px;
    background: var(--teal);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; color: white;
}
.gnb-menu {
    display: flex; gap: 36px; list-style: none;
    font-size: 0.82rem; font-weight: 500; color: var(--gray5);
}
.gnb-menu li { cursor: pointer; transition: color 0.2s; }
.gnb-menu li:hover { color: var(--teal); }
.gnb-right { font-size: 0.75rem; color: var(--gray4); }

/* ══════════════════════════════
   HERO
══════════════════════════════ */
.hero-wrap {
    position: relative; width: 100%;
    height: 100vh; min-height: 680px;
    overflow: hidden;
    background: var(--navy);
}
.hero-video-wrap { position: absolute; inset: 0; overflow: hidden; }
.hero-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(
        to bottom,
        rgba(13,27,42,0.25) 0%,
        rgba(13,27,42,0.1) 40%,
        rgba(13,27,42,0.65) 80%,
        rgba(13,27,42,0.95) 100%
    );
}
.hero-content {
    position: absolute; bottom: 80px; left: 72px;
    z-index: 2; max-width: 760px;
}
.hero-eyebrow {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: var(--teal); margin-bottom: 18px;
}
.hero-eyebrow::before {
    content: ''; display: block;
    width: 28px; height: 1px; background: var(--teal);
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.4rem,5vw,4rem);
    font-weight: 800; color: var(--white);
    line-height: 1.1; letter-spacing: -1.5px;
    margin-bottom: 18px;
}
.hero-title span { color: var(--teal); }
.hero-desc {
    font-size: 1rem; color: rgba(255,255,255,0.65);
    font-weight: 300; line-height: 1.75;
    margin-bottom: 32px; max-width: 520px;
}
.hero-cta {
    display: flex; gap: 12px; flex-wrap: wrap;
}
.btn-teal {
    display: inline-block;
    background: var(--teal);
    color: var(--white);
    padding: 13px 30px;
    font-size: 0.84rem; font-weight: 600;
    letter-spacing: 0.3px;
    border: none; border-radius: 2px;
    cursor: pointer; text-decoration: none;
    transition: background 0.2s;
}
.btn-teal:hover { background: var(--teal2); }
.btn-outline-w {
    display: inline-block;
    background: transparent;
    color: var(--white);
    padding: 12px 30px;
    font-size: 0.84rem; font-weight: 500;
    border: 1px solid rgba(255,255,255,0.45);
    border-radius: 2px; cursor: pointer;
    text-decoration: none; transition: all 0.2s;
}
.btn-outline-w:hover { background: rgba(255,255,255,0.1); }
.hero-scroll {
    position: absolute; bottom: 32px; right: 52px;
    display: flex; flex-direction: column;
    align-items: center; gap: 6px; z-index: 2;
    font-size: 0.62rem; letter-spacing: 2px;
    color: rgba(255,255,255,0.4); text-transform: uppercase;
}
.hero-scroll-line {
    width: 1px; height: 44px;
    background: linear-gradient(to bottom, rgba(255,255,255,0.4), transparent);
    animation: scrollLine 2s ease-in-out infinite;
}
@keyframes scrollLine {
    0%,100% { opacity:0.4; transform:scaleY(1); }
    50%      { opacity:1;   transform:scaleY(0.6); }
}

/* ══════════════════════════════
   섹션 공통
══════════════════════════════ */
.sec { padding: 100px 72px; }
.sec-white  { background: var(--white); }
.sec-gray   { background: var(--gray1); }
.sec-navy   { background: var(--navy); color: var(--white); }
.sec-teal   { background: var(--teal); color: var(--white); }

.sec-label {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: var(--teal); margin-bottom: 16px;
}
.sec-label::before {
    content:''; display:block;
    width:24px; height:1px; background: var(--teal);
}
.sec-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(1.8rem,4vw,3rem);
    font-weight: 800; line-height: 1.15;
    letter-spacing: -0.8px; margin-bottom: 16px;
    color: var(--navy);
}
.sec-title.white { color: var(--white); }
.sec-desc {
    font-size: 0.95rem; color: var(--gray5);
    font-weight: 300; line-height: 1.8;
    max-width: 520px;
}
.sec-desc.white { color: rgba(255,255,255,0.65); }

/* ══════════════════════════════
   WHY 섹션
══════════════════════════════ */
.why-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 80px; margin-top: 64px; align-items: center;
}
.why-img-wrap {
    border-radius: 4px; overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,180,160,0.12);
}
.why-img-wrap img {
    width: 100%; height: 460px;
    object-fit: cover; display: block;
    transition: transform 0.5s ease;
}
.why-img-wrap:hover img { transform: scale(1.03); }
.why-points { display: flex; flex-direction: column; gap: 36px; }
.why-point {
    display: flex; gap: 22px; align-items: flex-start;
    padding-bottom: 36px;
    border-bottom: 1px solid var(--gray2);
    transition: border-color 0.2s;
}
.why-point:hover { border-bottom-color: var(--teal); }
.why-point:last-child { border-bottom: none; padding-bottom: 0; }
.why-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.8rem; font-weight: 800;
    color: var(--teal); opacity: 0.5;
    min-width: 36px; line-height: 1;
}
.why-point-title {
    font-size: 1rem; font-weight: 700;
    color: var(--navy); margin-bottom: 7px;
    letter-spacing: -0.2px;
}
.why-point-desc {
    font-size: 0.84rem; color: var(--gray5);
    line-height: 1.7; font-weight: 300;
}

/* ══════════════════════════════
   STATS
══════════════════════════════ */
.stats-row {
    background: var(--teal);
    padding: 56px 72px;
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 40px;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.8rem; font-weight: 800;
    color: var(--white); letter-spacing: -2px;
    line-height: 1; margin-bottom: 8px;
}
.stat-num span { font-size: 1.6rem; }
.stat-label { font-size: 0.78rem; color: rgba(255,255,255,0.75); letter-spacing: 0.3px; }

/* ══════════════════════════════
   TECH 패널
══════════════════════════════ */
.tech-intro {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 80px; margin-bottom: 56px; align-items: end;
}
.tech-panel {
    position: relative; overflow: hidden;
    height: 420px; cursor: pointer;
    background: var(--navy2);
}
.tech-panel img {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover; filter: brightness(0.45);
    transition: transform 0.5s ease, filter 0.3s;
}
.tech-panel:hover img { transform: scale(1.04); filter: brightness(0.55); }
.tech-panel-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(13,27,42,0.92) 0%, rgba(13,27,42,0.2) 60%, transparent 100%);
}
.tech-panel-top {
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px; background: var(--teal);
    transform: scaleX(0); transform-origin: left;
    transition: transform 0.4s ease;
}
.tech-panel:hover .tech-panel-top { transform: scaleX(1); }
.tech-panel-body {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 32px 36px; z-index: 2;
}
.tech-panel-num {
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: var(--teal); margin-bottom: 10px;
}
.tech-panel-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.3rem; font-weight: 800;
    color: var(--white); line-height: 1.2;
    letter-spacing: -0.3px; margin-bottom: 8px;
}
.tech-panel-sub {
    font-size: 0.8rem; color: rgba(255,255,255,0.5);
    margin-bottom: 6px; transition: all 0.2s;
}
.tech-panel-desc {
    font-size: 0.78rem; color: rgba(255,255,255,0.45);
    line-height: 1.7; display: none;
}
.tech-panel:hover .tech-panel-sub { display: none; }
.tech-panel:hover .tech-panel-desc { display: block; }
.tech-panel-arrow {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 0.72rem; font-weight: 600;
    color: rgba(255,255,255,0.35); letter-spacing: 1px;
    text-transform: uppercase; margin-top: 14px;
    transition: color 0.2s;
}
.tech-panel:hover .tech-panel-arrow { color: var(--teal); }

/* ══════════════════════════════
   뉴스룸
══════════════════════════════ */
.newsroom-header {
    display: flex; justify-content: space-between;
    align-items: flex-end; margin-bottom: 40px;
}
.newsroom-link {
    font-size: 0.8rem; font-weight: 600;
    color: var(--teal); letter-spacing: 0.3px;
    border: 1px solid var(--teal); border-radius: 20px;
    padding: 7px 20px; cursor: pointer;
    transition: all 0.2s; text-decoration: none;
}
.newsroom-link:hover { background: var(--teal); color: var(--white); }

/* 뉴스 카드 */
.news-card-lg {
    background: var(--white);
    border: 1px solid var(--gray2);
    border-radius: 4px; overflow: hidden;
    transition: all 0.25s; cursor: pointer;
    height: 100%;
}
.news-card-lg:hover {
    box-shadow: 0 8px 32px rgba(0,180,160,0.12);
    border-color: var(--teal); transform: translateY(-3px);
}
.news-card-img {
    width: 100%; height: 200px;
    object-fit: cover; display: block;
    filter: brightness(0.9);
    transition: filter 0.3s, transform 0.4s;
}
.news-card-lg:hover .news-card-img { filter: brightness(1); transform: scale(1.02); }
.news-card-img-wrap { overflow: hidden; }
.news-card-body { padding: 20px 22px 24px; }
.news-card-date {
    font-size: 0.72rem; font-weight: 600;
    color: var(--teal); margin-bottom: 10px;
    letter-spacing: 0.5px;
}
.news-card-title {
    font-size: 0.92rem; font-weight: 700;
    color: var(--navy); line-height: 1.5;
    margin-bottom: 10px; letter-spacing: -0.2px;
    display: -webkit-box; -webkit-line-clamp: 3;
    -webkit-box-orient: vertical; overflow: hidden;
}
.news-card-title a { color: var(--navy); text-decoration: none; }
.news-card-title a:hover { color: var(--teal); }
.news-card-source { font-size: 0.72rem; color: var(--gray4); }

/* 피처드 카드 */
.news-card-feat {
    background: var(--white);
    border: 1px solid var(--gray2);
    border-radius: 4px; overflow: hidden;
    transition: all 0.25s; cursor: pointer;
}
.news-card-feat:hover {
    box-shadow: 0 8px 32px rgba(0,180,160,0.12);
    border-color: var(--teal);
}
.news-feat-img {
    width: 100%; height: 260px;
    object-fit: cover; display: block;
    transition: transform 0.4s;
}
.news-card-feat:hover .news-feat-img { transform: scale(1.02); }
.news-feat-img-wrap { overflow: hidden; }
.news-feat-body { padding: 24px 26px 28px; }
.news-feat-date { font-size:0.72rem; font-weight:600; color: var(--teal); margin-bottom:10px; letter-spacing:0.5px; }
.news-feat-title { font-size:1.1rem; font-weight:700; color: var(--navy); line-height:1.5; margin-bottom:10px; letter-spacing:-0.3px; }
.news-feat-title a { color: var(--navy); text-decoration:none; }
.news-feat-title a:hover { color: var(--teal); }
.news-feat-source { font-size:0.72rem; color: var(--gray4); }

/* ══════════════════════════════
   주제 리스트
══════════════════════════════ */
.topic-list-wrap { margin-top: 48px; }
.topic-row {
    display: flex; align-items: center; gap: 28px;
    padding: 20px 0;
    border-top: 1px solid var(--gray2);
    cursor: pointer; transition: all 0.2s;
    color: var(--navy);
}
.topic-row:last-child { border-bottom: 1px solid var(--gray2); }
.topic-row:hover { padding-left: 10px; }
.topic-row:hover .t-num { color: var(--teal); }
.topic-row:hover .t-title { color: var(--teal); }
.topic-row:hover .t-arrow { opacity:1; transform:translateX(0); color: var(--teal); }
.t-num { font-family:'Plus Jakarta Sans',sans-serif; font-size:0.72rem; font-weight:700; color: var(--gray3); min-width:30px; letter-spacing:1px; transition:color 0.2s; }
.t-title { font-size:0.95rem; font-weight:600; flex:1; transition:color 0.2s; letter-spacing:-0.2px; }
.t-en { font-size:0.78rem; color: var(--gray4); font-weight:300; min-width:280px; text-align:right; }
.t-arrow { color: var(--teal); font-size:1rem; opacity:0; transform:translateX(-8px); transition:all 0.2s; }

/* ══════════════════════════════
   DETAIL
══════════════════════════════ */
.detail-hero {
    background: var(--navy);
    padding: 130px 72px 72px;
    position: relative; overflow: hidden;
}
.detail-hero::after {
    content: attr(data-num);
    position: absolute; right:72px; top:50%;
    transform: translateY(-50%);
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size:9rem; font-weight:800;
    color: rgba(255,255,255,0.04); line-height:1;
}
.detail-crumb {
    font-size:0.72rem; color: rgba(255,255,255,0.3);
    margin-bottom:18px; display:flex; align-items:center; gap:8px;
}
.detail-title {
    font-family:'Plus Jakarta Sans',sans-serif;
    font-size: clamp(1.8rem,4vw,2.8rem);
    font-weight:800; color: var(--white);
    letter-spacing:-1px; line-height:1.15; margin-bottom:10px;
}
.detail-en { font-size:0.88rem; color:rgba(255,255,255,0.35); margin-bottom:22px; }
.detail-kws { display:flex; flex-wrap:wrap; gap:8px; }
.d-kw {
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.55);
    border-radius:20px; padding:4px 14px;
    font-size:0.72rem; font-weight:400;
}

/* 디테일 탭 */
.dtab-bar {
    background: var(--white);
    border-bottom: 1px solid var(--gray2);
    display:flex; padding:0 72px; overflow-x:auto;
}
.dtab {
    padding:16px 22px; font-size:0.82rem; font-weight:500;
    color: var(--gray5); border-bottom:2px solid transparent;
    margin-bottom:-1px; cursor:pointer; white-space:nowrap;
    transition:all 0.2s; letter-spacing:0.2px;
}
.dtab.on { color: var(--teal); border-bottom-color: var(--teal); font-weight:700; }
.dtab:hover { color: var(--navy); }

/* 사이드 위젯 */
.side-w {
    background: var(--gray1); border:1px solid var(--gray2);
    border-radius:4px; padding:22px; margin-bottom:14px;
}
.side-w-title {
    font-size:0.65rem; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color: var(--teal);
    border-bottom:1px solid var(--gray2); padding-bottom:10px; margin-bottom:14px;
}
.kw-chip {
    display:inline-block; background: var(--white);
    border:1px solid var(--gray3); color: var(--navy);
    border-radius:20px; padding:3px 12px;
    font-size:0.73rem; font-weight:500; margin:3px;
    transition:all 0.15s; cursor:default;
}
.kw-chip:hover { background: var(--teal); color: var(--white); border-color: var(--teal); }
.prog-item {
    display:flex; align-items:center; gap:10px;
    padding:7px 0; border-bottom:1px solid var(--gray2);
    font-size:0.8rem;
}
.prog-item:last-child { border-bottom:none; }
.prog-dot { width:8px; height:8px; border-radius:50%; background: var(--gray3); flex-shrink:0; }
.prog-dot.on { background: var(--teal); }

/* 뉴스 리스트 아이템 */
.ni {
    padding:20px 0; border-bottom:1px solid var(--gray2);
    display:flex; gap:18px; align-items:flex-start;
}
.ni:hover .ni-title { color: var(--teal); }
.ni-idx { font-family:'Plus Jakarta Sans',sans-serif; font-size:1.2rem; font-weight:800; color: var(--gray2); min-width:28px; line-height:1; }
.ni-flag { font-size:0.72rem; color: var(--gray4); margin-bottom:4px; }
.ni-title { font-size:0.9rem; font-weight:600; color: var(--navy); line-height:1.45; margin-bottom:5px; transition:color 0.15s; }
.ni-title a { color:inherit; text-decoration:none; }
.ni-meta  { font-size:0.72rem; color: var(--gray4); }

/* 논문 아이템 */
.pi { padding:20px 0; border-bottom:1px solid var(--gray2); }
.pbadge {
    display:inline-block; font-size:0.6rem; font-weight:700;
    letter-spacing:1px; padding:2px 8px; border-radius:2px; margin-bottom:8px;
}
.pb-a { background:#FEF3C7; color:#92400E; border:1px solid #FDE68A; }
.pb-s { background:#E0F2FE; color:#0369A1; border:1px solid #BAE6FD; }
.pi-title { font-size:0.88rem; font-weight:600; color: var(--navy); line-height:1.45; margin-bottom:5px; }
.pi-title a { color:inherit; text-decoration:none; }
.pi-title a:hover { color: var(--teal); }
.pi-auth { font-size:0.74rem; color: var(--gray4); margin-bottom:5px; }
.pi-abs  { font-size:0.78rem; color: var(--gray5); line-height:1.65; }

/* 선택 박스 */
.sel-box {
    background: #E6F7F5; border:1px solid #99DDD7;
    border-left:3px solid var(--teal);
    border-radius:0 4px 4px 0; padding:10px 16px;
    font-size:0.82rem; color: var(--teal2); font-weight:500;
    margin-bottom:16px;
}

/* 보고서 */
.report-out {
    background: var(--gray1); border:1px solid var(--gray2);
    border-radius:4px; padding:36px 40px;
    font-size:0.88rem; color: var(--gray5); line-height:1.9;
}
.report-out h1,.report-out h2,.report-out h3 { color: var(--navy); font-family:'Plus Jakarta Sans',sans-serif; }
.report-out h2 { border-left:3px solid var(--teal); padding-left:12px; margin:24px 0 10px; font-size:0.98rem; }

/* 표지 뉴스 */
.cover-card {
    position:relative; width:100%; height:300px;
    border-radius:4px; overflow:hidden; margin-bottom:24px;
}
.cover-card img { width:100%; height:100%; object-fit:cover; filter:brightness(0.4); }
.cover-overlay {
    position:absolute; inset:0;
    background:linear-gradient(to right, rgba(13,27,42,0.9) 0%, rgba(13,27,42,0.3) 60%, transparent 100%);
}
.cover-body { position:absolute; bottom:0; left:0; padding:28px 32px; max-width:65%; }
.cover-tag  { font-size:0.62rem; font-weight:700; letter-spacing:3px; text-transform:uppercase; color: var(--teal); margin-bottom:10px; }
.cover-title { font-size:1.1rem; font-weight:700; color: var(--white); line-height:1.45; margin-bottom:8px; }
.cover-title a { color: var(--white); text-decoration:none; }
.cover-title a:hover { color: var(--teal); }
.cover-meta { font-size:0.72rem; color:rgba(255,255,255,0.45); }

/* sub-news 3열 */
.sub-news-card {
    background: var(--gray1); border:1px solid var(--gray2);
    border-radius:4px; padding:18px 18px 16px; height:100%;
    transition:all 0.2s; cursor:pointer;
}
.sub-news-card:hover { border-color: var(--teal); background: var(--white); box-shadow:0 4px 16px rgba(0,180,160,0.1); }
.sub-news-tag   { font-size:0.6rem; font-weight:700; color: var(--teal); letter-spacing:2px; text-transform:uppercase; margin-bottom:8px; }
.sub-news-title { font-size:0.85rem; font-weight:600; color: var(--navy); line-height:1.5; margin-bottom:8px; }
.sub-news-title a { color: var(--navy); text-decoration:none; }
.sub-news-title a:hover { color: var(--teal); }
.sub-news-meta  { font-size:0.7rem; color: var(--gray4); }

/* 푸터 */
.footer {
    background: var(--navy); padding:52px 72px;
    display:flex; justify-content:space-between; align-items:center;
    border-top:3px solid var(--teal);
}
.footer-logo { font-family:'Plus Jakarta Sans',sans-serif; font-weight:800; font-size:1rem; color: var(--white); }
.footer-logo span { color: var(--teal); }
.footer-copy { font-size:0.72rem; color:rgba(255,255,255,0.3); }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 데이터
# =====================================================================
TOPICS = [
    ("01","배터리 건강 추정의 필요성","Battery State of Health Estimation","배터리 SOH는 전기차·에너지 저장 시스템의 안전성과 성능 관리에 핵심적이다.",["SOH","배터리 열화","RUL","EV","BMS"]),
    ("02","음극 노화","Lithium-ion Battery Anode Aging","리튬 도금, SEI 성장, 구조적 균열 등으로 발생하는 음극 열화 메커니즘.",["SEI","리튬 도금","흑연 음극","용량 손실","사이클 열화"]),
    ("03","양극 노화","Lithium-ion Battery Cathode Aging","NMC·LFP 등 양극 소재별 열화 메커니즘과 성능 저하 원인 분석.",["NMC/LFP","구조 열화","전이금속 용해","상변이","캘린더 노화"]),
    ("04","R₀에 대한 전압 감도","Battery Internal Resistance Voltage Sensitivity","내부 저항 R₀와 SOH의 상관관계 및 전압 감도 분석 방법론.",["내부 저항","전압 강하","등가 회로","임피던스","열화 진단"]),
    ("05","R₀를 추정하기 위한 코드","Battery Internal Resistance Estimation Algorithm","전류 펄스, EIS, 최소제곱법 기반 실시간 R₀ 추정 알고리즘.",["최소제곱법","EIS","전류 펄스","실시간 추정","Python"]),
    ("06","전체 용량에 대한 전압의 민감도 Q","Battery Voltage Sensitivity Total Capacity","OCV-SOC 곡선 기반 전체 용량 Q 추정 방법 및 민감도 분석.",["용량 Q","OCV-SOC","활물질 손실","쿨롱 카운팅","용량 추정"]),
    ("07","칼만 필터를 통한 파라미터 추정","Kalman Filter Battery Parameter Estimation","노이즈 환경에서 배터리 상태변수를 최적 추정하는 재귀 알고리즘.",["칼만 필터","상태 추정","공분산","예측-수정","재귀 알고리즘"]),
    ("08","EKF 파라미터 추정","Extended Kalman Filter Battery SOH","야코비안 선형화로 비선형 배터리 모델에 칼만 필터를 적용하는 방법.",["EKF","야코비안","비선형 시스템","SOC 추정","선형화"]),
    ("09","SPKF 파라미터 추정","Sigma-Point Kalman Filter Battery","시그마 포인트 통계 전파로 EKF보다 높은 정확도를 달성하는 필터.",["SPKF/UKF","시그마 포인트","무향 변환","비선형 추정","통계 근사"]),
    ("10","조인트 추정과 듀얼 추정","Joint Dual Estimation Battery State","상태변수와 파라미터를 단일 또는 이중 필터로 동시 추정하는 기법.",["조인트 추정","듀얼 추정","이중 필터","적응형 추정","동시 추정"]),
    ("11","견고성과 속도","Robustness Speed Battery Estimation","노이즈·불확실성에 강인하면서 실시간 BMS에 적합한 알고리즘 설계.",["견고성","계산 복잡도","실시간 처리","노이즈 민감도","수렴 속도"]),
    ("12","선형 회귀를 통한 전체 용량의 비편향 추정값","Unbiased Battery Capacity Linear Regression","측정 데이터 기반 선형 회귀로 배터리 전체 용량을 편향 없이 추정.",["비편향 추정","선형 회귀","쿨롱 카운팅","OLS","용량 추정"]),
    ("13","가중 일반 최소제곱법","Weighted Generalized Least Squares Battery","불균일 노이즈 분산 환경에서 가중치 부여로 추정 정확도를 향상.",["WGLS","이분산성","가중 행렬","최적 추정","노이즈 모델링"]),
    ("14","총 가중 최소제곱법","Weighted Total Least Squares Battery","입출력 양방향 노이즈를 고려한 EIV 모델 기반 용량 추정 기법.",["TWLS","EIV","양방향 노이즈","총 최소제곱","용량 추정"]),
    ("15","모델 적합도의 우수성","Goodness of Fit Battery Equivalent Circuit","RMSE·R²·AIC 기반 등가 회로 모델 적합도 평가 및 최적 모델 선택.",["RMSE","R²","AIC/BIC","등가 회로 모델","모델 검증"]),
    ("16","신뢰 구간","Confidence Interval Battery Estimation","추정 불확실성을 정량화하여 배터리 안전 마진을 설정하는 방법.",["신뢰 구간","불확실성","공분산","오차 한계","통계 추론"]),
    ("17","단순화된 총 최소제곱","Simplified Total Least Squares Battery","계산 복잡도를 줄이면서 EIV 모델의 장점을 유지하는 경량 알고리즘.",["단순화 TLS","근사 알고리즘","계산 효율","실시간 BMS","EIV"]),
    ("18","근사 전체 솔루션","Approximate Total Solution Battery","닫힌 형태 근사로 복잡한 최적화 문제의 계산 효율을 높이는 방법.",["근사 해","계산 최적화","파라미터 추정","수치 안정성","실시간 구현"]),
    ("19","방법별 시뮬레이션 코드","Battery SOH Estimation Simulation Code","Python·MATLAB 기반 EKF·SPKF·OLS 알고리즘 성능 비교 시뮬레이션.",["시뮬레이션","Python/MATLAB","알고리즘 비교","성능 평가","데이터셋"]),
    ("20","HEV 시뮬레이션 예시","Hybrid Electric Vehicle Battery Simulation","UDDS·HWFET 주행 사이클 적용 HEV 배터리 SOH 추정 시뮬레이션.",["HEV","주행 사이클","UDDS/HWFET","동적 부하","SOH 추정"]),
    ("21","EV 시뮬레이션 예시","Electric Vehicle EV Battery Simulation","WLTP·EPA 표준 사이클 기반 EV 배터리 에너지 관리 및 SOH 분석.",["EV","주행거리","WLTP/EPA","에너지 관리","충전 전략"]),
    ("22","시뮬레이션에 대한 논의","Battery Simulation Discussion Results","다양한 추정 방법의 시뮬레이션 결과 비교 및 실차 적용 고려사항.",["결과 비교","실차 적용","온도 영향","센서 오차","검증"]),
    ("23","결론 및 향후 방향","Battery Health Estimation Future Research","머신러닝·디지털 트윈·클라우드 BMS 등 미래 SOH 추정 연구 방향.",["머신러닝 SOH","디지털 트윈","차세대 배터리","클라우드 BMS","연구 과제"]),
    ("24","비선형 칼만 필터 알고리즘","Nonlinear Kalman Filter Algorithm Battery","EKF·UKF·CKF·파티클 필터의 이론과 배터리 SOH 추정 적용 비교.",["비선형 칼만","UKF/CKF","파티클 필터","비선형 추정","알고리즘 비교"]),
]

TECH_HIGHLIGHTS = [
    ("01","배터리 건강 추정의 필요성","안전한 배터리 운용의 시작","SOH 추정은 전기차·ESS 안전 운용의 핵심으로, 과충전·과방전 방지와 잔여 수명(RUL) 예측에 필수적입니다.","https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800&h=500&fit=crop"),
    ("07","칼만 필터 파라미터 추정","노이즈 속 최적 추정","칼만 필터는 센서 노이즈 환경에서 배터리 SOC·SOH를 최적으로 추정하는 재귀적 베이지안 프레임워크입니다.","https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&h=500&fit=crop"),
    ("08","EKF 파라미터 추정","비선형 모델 대응","배터리 OCV-SOC 특성은 비선형입니다. EKF는 야코비안으로 순간 선형화하여 칼만 필터를 적용합니다.","https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=500&fit=crop"),
    ("09","SPKF 파라미터 추정","더 높은 추정 정확도","SPKF/UKF는 시그마 포인트 통계 전파로 야코비안 없이 EKF보다 높은 정확도를 달성합니다.","https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=800&h=500&fit=crop"),
    ("10","조인트·듀얼 추정","SOC와 SOH 동시 추정","조인트 추정은 단일 확장 상태 벡터로, 듀얼 추정은 이중 병렬 필터로 SOC·SOH를 동시에 추정합니다.","https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=800&h=500&fit=crop"),
    ("20","HEV·EV 시뮬레이션","실제 주행 환경 검증","UDDS·WLTP 등 표준 주행 사이클로 실제 차량 환경을 재현하여 각 알고리즘 성능을 비교·검증합니다.","https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=500&fit=crop"),
]

TECH_IDX = {"01":0,"07":6,"08":7,"09":8,"10":9,"20":19}

NEWS_IMGS = [
    "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1543286386-713bdd548da4?w=600&h=300&fit=crop",
    "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&h=300&fit=crop",
]

# =====================================================================
# 수집 함수
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news(keyword, hl, gl, ceid, n=8):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(keyword)}&hl={hl}&gl={gl}&ceid={ceid}"
    try: return feedparser.parse(url).entries[:n]
    except: return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_arxiv(keyword, n=6):
    try:
        q = urllib.parse.quote(keyword)
        url = f"https://export.arxiv.org/api/query?search_query=all:{q}&start=0&max_results={n}&sortBy=submittedDate&sortOrder=descending"
        feed = feedparser.parse(url)
        out = []
        for e in feed.entries:
            title = e.get("title","").replace("\n"," ").strip()
            summary = e.get("summary","")[:400].replace("\n"," ").strip()
            pub = e.get("published","")[:10]
            link = e.get("id","") or e.get("link","")
            ar = e.get("authors",[])
            authors = ", ".join(a.get("name","") for a in ar[:3]) if ar else e.get("author","")
            if title: out.append({"title":title,"authors":authors,"abstract":summary,"url":link,"published":pub})
        return out
    except: return []

def fetch_scholar(keyword, n=4):
    out=[]
    try:
        gen = scholarly.search_pubs(keyword)
        for _ in range(n):
            try:
                pub=next(gen); bib=pub.get("bib",{})
                out.append({"title":bib.get("title","No title"),"authors":bib.get("author","Unknown"),
                            "year":bib.get("pub_year",""),"journal":bib.get("venue",""),
                            "abstract":bib.get("abstract",""),"url":pub.get("pub_url","")})
            except StopIteration: break
    except: pass
    return out

def build_report(num,ko,en,bg,kw,nko,nen,papers,arxiv):
    today=datetime.now().strftime("%Y-%m-%d")
    kw_str=" / ".join(kw)
    n_news=len(nko)+len(nen); n_p=len(papers)+len(arxiv)
    ref_num=1; refs=[]
    for p in papers:
        r=f"[{ref_num}] {p['authors']} ({p['year']}). {p['title']}."
        if p.get('journal'): r+=f" {p['journal']}."
        if p.get('url'):     r+=f" {p['url']}"
        refs.append(r); ref_num+=1
    for p in arxiv:
        refs.append(f"[{ref_num}] {p['authors']} ({p['published'][:4]}). {p['title']}. arXiv. {p['url']}")
        ref_num+=1
    for n in nko+nen:
        refs.append(f"[{ref_num}] {n['title']}. {n['source']} ({n['published']}). {n['link']}")
        ref_num+=1
    sb="".join([f"\n**[{i}] {p['title']}** ({p['year']}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(papers,1)]) or "(없음)"
    ab="".join([f"\n**[{i}] [{p['title']}]({p['url']})** ({p['published'][:7]}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(arxiv,len(papers)+1)]) or "(없음)"
    return f"""# {num}. {ko}\n## 연구 분석 보고서 — BatteryIQ\n\n**작성일:** {today} | **키워드:** {kw_str}\n**기준 문헌:** Gregory Plett - *Battery Management Systems*\n**수집 자료:** 뉴스 {n_news}건 · 논문 {n_p}편\n\n---\n\n## 초록\n\n{ko}은(는) 배터리 건강 상태(SOH) 추정의 핵심 주제이다. {bg}\n\n**키워드:** {kw_str}\n\n---\n\n## 1. 서론\n\n### 1.1 연구 배경\n{bg}\n\n### 1.2 연구 목적\n{ko}({en})에 관한 최신 연구 동향과 기술 현황을 체계적으로 분석한다.\n\n---\n\n## 2. 이론적 배경\n\n| 핵심 개념 | 설명 |\n|----------|------|\n{"".join([f"| **{k}** | {ko} 분야 핵심 요소 |\n" for k in kw])}\n\n---\n\n## 3. 최신 기술 동향\n\n### 3.1 국내 동향\n{"".join([f"**[뉴스]** [{n['title']}]({n['link']})\n> {n['source']} | {n['published']}\n\n" for n in nko]) or "(없음)"}\n\n### 3.2 해외 동향\n{"".join([f"**[News]** [{n['title']}]({n['link']})\n> {n['source']} | {n['published']}\n\n" for n in nen]) or "(없음)"}\n\n---\n\n## 4. 핵심 선행 연구\n\n### 4.1 Google Scholar\n{sb}\n\n### 4.2 arXiv 최신 연구\n{ab}\n\n---\n\n## 5. 기술적 분석\n\n| 구분 | 주요 방법 | 특징 | 적용 분야 |\n|------|----------|------|----------|\n| 모델 기반 | 등가 회로 모델 | 구현 용이, 실시간 | BMS 내장 |\n| 필터 기반 | EKF / UKF | 높은 정확도 | 전기차 |\n| 데이터 기반 | 머신러닝 | 대용량 데이터 | 클라우드 BMS |\n\n---\n\n## 6. 결론\n\n- {ko}은(는) BMS 핵심 기능으로 연구 수요 지속 증가\n- 칼만 필터 + 데이터 기반 융합 연구 트렌드\n- AI/ML 융합, 디지털 트윈, 차세대 배터리 적용이 향후 과제\n\n---\n\n## 참고문헌\n\n{"".join([f"{r}  \n" for r in refs]) or "(없음)"}\n\n---\n*BatteryIQ 연구 포털 | Gregory Plett, Battery Management Systems Vol.2 (2015)*"""

# =====================================================================
# 세션
# =====================================================================
for k,v in [("page","home"),("sel_idx",0),
            ("news_ko",[]),("news_en",[]),("papers",[]),("arxiv",[]),
            ("sel_news",[]),("sel_papers",[]),("sel_arxiv",[]),
            ("report",""),("tab","news"),("step",0),
            ("auto_fetch",False),("home_ko",[]),("home_en",[]),
            ("show_topic_nav",False),("overview_tab","competitiveness")]:
    if k not in st.session_state: st.session_state[k]=v

# =====================================================================
# GNB
# =====================================================================
nc=len(st.session_state["news_ko"])+len(st.session_state["news_en"])
pc=len(st.session_state["papers"])+len(st.session_state["arxiv"])

st.markdown(f"""
<div class="gnb">
    <div class="gnb-logo">
        <div class="gnb-logo-mark">🔋</div>
        BatteryIQ
    </div>
    <ul class="gnb-menu">
        <li id="nav-overview">연구 개요</li>
        <li>핵심 기술</li>
        <li>뉴스룸</li>
        <li>24개 주제</li>
    </ul>
    <div class="gnb-right">Gregory Plett · Chapter 2-04 &nbsp;|&nbsp; 📰{nc}건 📚{pc}편</div>
</div>
""", unsafe_allow_html=True)

# GNB 실제 클릭 버튼 (투명 오버레이)
gnb_cols = st.columns([2,1,1,1,1,3])
with gnb_cols[1]:
    if st.button("연구 개요", key="gnb_overview"):
        st.session_state["page"] = "overview"
        st.rerun()
with gnb_cols[2]:
    if st.button("핵심 기술", key="gnb_tech"):
        st.session_state["page"] = "home"
        st.rerun()
with gnb_cols[3]:
    if st.button("뉴스룸", key="gnb_news"):
        st.session_state["page"] = "home"
        st.rerun()
with gnb_cols[4]:
    if st.button("24개 주제", key="gnb_topics"):
        st.session_state["page"] = "home"
        st.session_state["show_topic_nav"] = True
        st.rerun()

# =====================================================================
# HOME
# =====================================================================
if st.session_state["page"] == "home":

    # HERO
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-video-wrap">
            <video autoplay muted loop playsinline
                style="position:absolute;top:50%;left:50%;min-width:100%;min-height:100%;
                       width:auto;height:auto;transform:translate(-50%,-50%);object-fit:cover;">
                <source src="https://raw.githubusercontent.com/rain422/-/main/13814690_1920_1080_100fps.mp4" type="video/mp4">
            </video>
        </div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-eyebrow">Battery Management Systems · Chapter 2-04</div>
            <div class="hero-title">배터리<br><span>건강 추정</span><br>연구 포털</div>
            <div class="hero-desc">
                Battery State of Health(SOH) 추정은 전기차와 에너지 저장 시스템의<br>
                안전한 운용과 수명 예측을 위한 핵심 기술입니다.
            </div>
        </div>
        <div class="hero-scroll">
            <div class="hero-scroll-line"></div>
            <span>SCROLL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # WHY 섹션
    st.markdown("""
    <div class="sec sec-white">
        <div class="sec-label">왜 배터리 건강 추정인가</div>
        <div class="why-grid">
            <div class="why-img-wrap" style="position:relative;overflow:hidden;border-radius:4px;box-shadow:0 20px 60px rgba(0,180,160,0.12);">
                <video autoplay muted loop playsinline
                    style="width:100%;height:460px;object-fit:cover;display:block;">
                    <source src="https://raw.githubusercontent.com/rain422/-/main/KakaoTalk_20260413_165858691.mp4" type="video/mp4">
                </video>
            </div>
            <div>
                <div class="sec-title" style="margin-bottom:36px;">배터리 수명과 안전을<br>결정하는 핵심 기술</div>
                <div class="why-points">
                    <div class="why-point">
                        <div class="why-num">01</div>
                        <div>
                            <div class="why-point-title">안전성 확보</div>
                            <div class="why-point-desc">과충전·과방전을 실시간으로 방지하여 배터리 열폭주 등 위험 상황을 사전에 예방합니다.</div>
                        </div>
                    </div>
                    <div class="why-point">
                        <div class="why-num">02</div>
                        <div>
                            <div class="why-point-title">수명 예측 (RUL)</div>
                            <div class="why-point-desc">잔여 유용 수명을 정확히 예측하여 배터리 교체 시점을 최적화하고 유지보수 비용을 절감합니다.</div>
                        </div>
                    </div>
                    <div class="why-point">
                        <div class="why-num">03</div>
                        <div>
                            <div class="why-point-title">성능 최적화</div>
                            <div class="why-point-desc">실시간 SOH 데이터를 활용한 에너지 관리 전략으로 EV 주행거리와 충전 효율을 극대화합니다.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # STATS
    st.markdown("""
    <div class="stats-row">
        <div class="stat-item"><div class="stat-num">24<span>개</span></div><div class="stat-label">핵심 연구 주제</div></div>
        <div class="stat-item"><div class="stat-num">6<span>종</span></div><div class="stat-label">추정 알고리즘</div></div>
        <div class="stat-item"><div class="stat-num">2<span>개</span></div><div class="stat-label">논문 데이터베이스</div></div>
        <div class="stat-item"><div class="stat-num">∞</div><div class="stat-label">최신 뉴스 수집</div></div>
    </div>
    """, unsafe_allow_html=True)

    # TECH 패널
    st.markdown("""
    <div class="sec sec-gray" style="padding-bottom:0;">
        <div class="tech-intro">
            <div>
                <div class="sec-label">주요 기술</div>
                <div class="sec-title">배터리 건강 추정<br>핵심 기술</div>
            </div>
            <div>
                <div class="sec-desc">칼만 필터부터 EV 시뮬레이션까지 — 6가지 핵심 기술을 탐색하세요.<br>패널을 클릭하면 관련 뉴스와 논문을 바로 확인할 수 있습니다.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for row_start in range(0, len(TECH_HIGHLIGHTS), 2):
        row = TECH_HIGHLIGHTS[row_start:row_start+2]
        cols = st.columns(2)
        for col, (num,title,sub,desc,img) in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="tech-panel">
                    <div class="tech-panel-top"></div>
                    <img src="{img}" alt="{title}">
                    <div class="tech-panel-overlay"></div>
                    <div class="tech-panel-body">
                        <div class="tech-panel-num">TOPIC {num}</div>
                        <div class="tech-panel-title">{title}</div>
                        <div class="tech-panel-sub">{sub}</div>
                        <div class="tech-panel-desc">{desc}</div>
                        <div class="tech-panel-arrow">자세히 보기 →</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"기술_{num}", key=f"tp_{num}", use_container_width=True):
                    tidx = TECH_IDX.get(num,0)
                    st.session_state.update({"page":"detail","sel_idx":tidx,"tab":"news","step":0,"auto_fetch":True})
                    for k2 in ["news_ko","news_en","papers","arxiv","sel_news","sel_papers","sel_arxiv","report"]:
                        st.session_state[k2]=[] if k2!="report" else ""
                    st.rerun()

    st.markdown("<div style='height:8px;background:#f7f8fa;'></div>", unsafe_allow_html=True)

    # 뉴스룸 (자동 수집)
    if not st.session_state.get("home_ko") and not st.session_state.get("home_en"):
        with st.spinner("뉴스를 불러오는 중..."):
            raw_ko = fetch_news("배터리 건강 추정 SOH BMS","ko","KR","KR:ko",4)
            st.session_state["home_ko"] = [{"title":e.title,"link":e.link,"published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News'),"lang":"ko"} for e in raw_ko]
            raw_en = fetch_news("Battery State of Health Estimation","en","US","US:en",4)
            st.session_state["home_en"] = [{"title":e.title,"link":e.link,"published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News'),"lang":"en"} for e in raw_en]

    home_all = st.session_state.get("home_ko",[]) + st.session_state.get("home_en",[])

    st.markdown(f"""
    <div class="sec sec-white">
        <div class="newsroom-header">
            <div>
                <div class="sec-label">최신 뉴스</div>
                <div class="sec-title">뉴스룸</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if home_all:
        # 4열 카드 그리드
        cols4 = st.columns(4, gap="small")
        for i, item in enumerate(home_all[:4]):
            flag = "🇰🇷" if item.get("lang")=="ko" else "🌍"
            date = item['published'][:10] if item['published'] else ""
            img  = NEWS_IMGS[i % len(NEWS_IMGS)]
            with cols4[i]:
                st.markdown(f"""
                <div class="news-card-lg">
                    <div class="news-card-img-wrap">
                        <img class="news-card-img" src="{img}" alt="news">
                    </div>
                    <div class="news-card-body">
                        <div class="news-card-date">{date}</div>
                        <div class="news-card-title">
                            <a href="{item['link']}" target="_blank">{item['title']}</a>
                        </div>
                        <div class="news-card-source">{flag} {item['source']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # 새로고침
        st.markdown("<br>", unsafe_allow_html=True)
        _, rc, _ = st.columns([4,2,4])
        with rc:
            if st.button("🔄 뉴스 새로고침", key="nr", use_container_width=True):
                st.session_state["home_ko"]=[]
                st.session_state["home_en"]=[]
                st.rerun()
    else:
        st.info("뉴스를 불러오는 중입니다...")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── LG 스타일 다크 배너 (영상 배경) ──
    st.markdown("""
    <style>
    .dark-banner {
        position: relative;
        width: 100%;
        min-height: 520px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--navy);
    }
    .dark-banner video {
        position: absolute;
        inset: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        filter: brightness(0.28);
    }
    .dark-banner-overlay {
        position: absolute; inset: 0;
        background: radial-gradient(ellipse at center, rgba(0,180,160,0.08) 0%, rgba(13,27,42,0.6) 70%);
    }
    .dark-banner-body {
        position: relative; z-index: 2;
        text-align: center;
        padding: 100px 48px;
        max-width: 900px;
    }
    .dark-banner-label {
        font-size: 0.68rem; font-weight: 700;
        letter-spacing: 3px; text-transform: uppercase;
        color: var(--teal); margin-bottom: 24px;
        display: flex; align-items: center;
        justify-content: center; gap: 10px;
    }
    .dark-banner-label::before,
    .dark-banner-label::after {
        content: ''; display: block;
        width: 32px; height: 1px; background: var(--teal);
    }
    .dark-banner-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: clamp(1.8rem, 4vw, 3rem);
        font-weight: 800; color: var(--white);
        line-height: 1.25; letter-spacing: -1px;
        margin-bottom: 20px;
    }
    .dark-banner-title span { color: var(--teal); }
    .dark-banner-desc {
        font-size: 1rem; color: rgba(255,255,255,0.55);
        font-weight: 300; line-height: 1.8;
        margin-bottom: 40px;
    }
    .topic-nav-btn {
        display: inline-flex; align-items: center; gap: 10px;
        background: transparent;
        color: var(--white);
        border: 1px solid rgba(255,255,255,0.4);
        border-radius: 2px;
        padding: 14px 36px;
        font-size: 0.88rem; font-weight: 600;
        cursor: pointer; letter-spacing: 0.5px;
        transition: all 0.2s; text-decoration: none;
    }
    .topic-nav-btn:hover {
        background: var(--teal);
        border-color: var(--teal);
        color: var(--white);
    }
    /* 주제 네비게이터 그리드 */
    .topic-nav-grid {
        background: var(--navy);
        padding: 72px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background-color: rgba(255,255,255,0.06);
    }
    .topic-nav-cell {
        background: var(--navy2);
        padding: 24px 22px;
        cursor: pointer;
        transition: background 0.2s, border-left 0.2s;
        position: relative;
    }
    .topic-nav-cell:hover { background: #243548; }
    .topic-nav-cell:hover .tnc-title { color: var(--teal); }
    .tnc-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.65rem; font-weight: 700;
        color: var(--teal); letter-spacing: 2px;
        margin-bottom: 8px; text-transform: uppercase;
    }
    .tnc-title {
        font-size: 0.88rem; font-weight: 600;
        color: var(--white); line-height: 1.4;
        transition: color 0.2s;
    }
    .tnc-arrow {
        position: absolute; right: 18px; top: 50%;
        transform: translateY(-50%);
        color: rgba(255,255,255,0.15);
        font-size: 0.9rem; transition: all 0.2s;
    }
    .topic-nav-cell:hover .tnc-arrow {
        color: var(--teal);
        transform: translateY(-50%) translateX(3px);
    }
    </style>
    """, unsafe_allow_html=True)

    # 배너 표시 (버튼 배너 안에 포함)
    st.markdown("""
    <style>
    .pill-btn {
        display: inline-flex; align-items: center; gap: 10px;
        background: rgba(255,255,255,0.05);
        color: rgba(255,255,255,0.55);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 50px;
        padding: 13px 36px;
        font-size: 0.88rem; font-weight: 400;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        backdrop-filter: blur(4px);
    }
    .pill-btn:hover {
        background: rgba(255,255,255,0.15) !important;
        color: var(--white) !important;
        border-color: rgba(255,255,255,0.55) !important;
        transform: translateY(-2px);
    }
    </style>
    <div class="dark-banner">
        <video autoplay muted loop playsinline
            style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(0.55);">
            <source src="https://raw.githubusercontent.com/rain422/-/main/15254965_1920_1080_24fps.mp4" type="video/mp4">
        </video>
        <div style="position:absolute;inset:0;
            background:linear-gradient(to bottom, rgba(13,27,42,0.15) 0%, rgba(13,27,42,0.4) 100%);">
        </div>
        <div class="dark-banner-overlay"></div>
        <div class="dark-banner-body">
            <div class="dark-banner-label">Battery Intelligence Research</div>
            <div class="dark-banner-title">
                배터리의 <span>건강 상태</span>를 알면<br>
                미래 에너지를 설계할 수 있습니다
            </div>
            <div class="dark-banner-desc">
                SOH 추정 기술은 전기차 안전과 에너지 효율의 핵심입니다.<br>
                24개 핵심 주제를 통해 배터리 건강 추정의 모든 것을 탐구하세요.
            </div>
            <span class="pill-btn">핵심 주제 바로가기 &nbsp;→</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 실제 클릭 버튼 (배너 바로 아래, 스트림릿 동작용 — 최소화)
    if "show_topic_nav" not in st.session_state:
        st.session_state["show_topic_nav"] = False

    # 24개 주제 그리드 (펼치면 보임)
    if st.session_state["show_topic_nav"]:
        st.markdown('<div style="background:#0D1B2A;padding:56px 72px 72px;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-bottom:48px;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
                        color:#00B4A0;margin-bottom:14px;display:flex;align-items:center;
                        justify-content:center;gap:10px;">
                <span style="display:block;width:32px;height:1px;background:#00B4A0;"></span>
                24개 핵심 주제
                <span style="display:block;width:32px;height:1px;background:#00B4A0;"></span>
            </div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.8rem;font-weight:800;
                        color:#fff;letter-spacing:-0.5px;">
                배터리 건강 추정 연구 주제 전체 보기
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4열 그리드
        cols_per_row = 4
        for row_start in range(0, len(TOPICS), cols_per_row):
            row_topics = TOPICS[row_start:row_start+cols_per_row]
            cols = st.columns(cols_per_row, gap="small")
            for col, (num,ko,en,desc,kw) in zip(cols, row_topics):
                i = TOPICS.index((num,ko,en,desc,kw))
                with col:
                    st.markdown(f"""
                    <div class="topic-nav-cell">
                        <div class="tnc-num">TOPIC {num}</div>
                        <div class="tnc-title">{ko}</div>
                        <div class="tnc-arrow">→</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"이동_{num}", key=f"tnav_{num}", use_container_width=True):
                        st.session_state.update({"page":"detail","sel_idx":i,"tab":"news","step":0,"auto_fetch":True,"show_topic_nav":False})
                        for k2 in ["news_ko","news_en","papers","arxiv","sel_news","sel_papers","sel_arxiv","report"]:
                            st.session_state[k2]=[] if k2!="report" else ""
                        st.rerun()
            st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🔋 Battery<span>IQ</span></div>
        <div class="footer-copy">Battery Management Systems · Gregory Plett · Chapter 2-04 · 배터리 건강 추정 연구 포털</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# DETAIL
# =====================================================================
elif st.session_state["page"] == "detail":
    tidx = st.session_state["sel_idx"]
    num,ko,en,bg,kw = TOPICS[tidx]

    kw_chips = "".join([f'<span class="d-kw">{k}</span>' for k in kw])
    st.markdown(f"""
    <div class="detail-hero" data-num="{num}">
        <div class="detail-crumb">BatteryIQ › 연구 주제 › <span style="color:rgba(255,255,255,0.6);">{ko}</span></div>
        <div class="detail-title">{ko}</div>
        <div class="detail-en">{en}</div>
        <div class="detail-kws">{kw_chips}</div>
    </div>
    """, unsafe_allow_html=True)

    bc,_ = st.columns([2,8])
    with bc:
        if st.button("← 홈으로"):
            st.session_state["page"]="home"; st.rerun()

    tabs=[("news","뉴스 수집"),("papers","논문 검색"),("select","자료 선택"),("report","보고서"),("save","다운로드")]
    tab_html='<div class="dtab-bar">'
    for tk,tl in tabs:
        cls="on" if st.session_state["tab"]==tk else ""
        tab_html+=f'<span class="dtab {cls}">{tl}</span>'
    tab_html+="</div>"
    st.markdown(tab_html, unsafe_allow_html=True)
    tc=st.columns(len(tabs))
    for i,(tk,tl) in enumerate(tabs):
        with tc[i]:
            if st.button(tl,key=f"dt_{tk}",use_container_width=True):
                st.session_state["tab"]=tk; st.rerun()

    mc,sc=st.columns([7,3],gap="medium")

    with sc:
        step=st.session_state["step"]
        ph='<div class="side-w"><div class="side-w-title">진행 상태</div>'
        for sl,sn in [("뉴스 수집",1),("논문 검색",2),("자료 선택",3),("보고서 생성",4)]:
            done=step>=sn
            ph+=f'<div class="prog-item"><div class="prog-dot {"on" if done else ""}"></div><span style="color:{"#00B4A0" if done else "#9EA5AF"};font-weight:{"600" if done else "400"};">{"✓" if done else "○"} {sl}</span></div>'
        ph+="</div>"
        st.markdown(ph, unsafe_allow_html=True)

        nc_s=len(st.session_state["news_ko"])+len(st.session_state["news_en"])
        pc_s=len(st.session_state["papers"])+len(st.session_state["arxiv"])
        sc_s=len(st.session_state["sel_news"])+len(st.session_state["sel_papers"])+len(st.session_state["sel_arxiv"])
        st.markdown(f"""
        <div class="side-w">
            <div class="side-w-title">수집 현황</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
                <div style="background:#E6F7F5;padding:12px 4px;border-radius:4px;">
                    <div style="font-size:1.4rem;font-weight:800;color:#00B4A0;font-family:'Plus Jakarta Sans',sans-serif;">{nc_s}</div>
                    <div style="font-size:0.65rem;color:#9EA5AF;margin-top:2px;">뉴스</div>
                </div>
                <div style="background:#E6F7F5;padding:12px 4px;border-radius:4px;">
                    <div style="font-size:1.4rem;font-weight:800;color:#00B4A0;font-family:'Plus Jakarta Sans',sans-serif;">{pc_s}</div>
                    <div style="font-size:0.65rem;color:#9EA5AF;margin-top:2px;">논문</div>
                </div>
                <div style="background:#E6F7F5;padding:12px 4px;border-radius:4px;">
                    <div style="font-size:1.4rem;font-weight:800;color:#00B4A0;font-family:'Plus Jakarta Sans',sans-serif;">{sc_s}</div>
                    <div style="font-size:0.65rem;color:#9EA5AF;margin-top:2px;">선택</div>
                </div>
            </div>
        </div>
        <div class="side-w">
            <div class="side-w-title">Topic Overview</div>
            <div style="font-size:0.82rem;color:#6B7280;line-height:1.7;font-weight:300;">{bg}</div>
        </div>
        """, unsafe_allow_html=True)

        kw_c = "".join([f'<span class="kw-chip">{k}</span>' for k in kw])
        st.markdown(f'<div class="side-w"><div class="side-w-title">Keywords</div>{kw_c}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="side-w"><div class="side-w-title">Search Keyword</div><div style="font-size:0.8rem;color:#00B4A0;font-weight:600;background:#E6F7F5;padding:8px 12px;border-radius:4px;">{en}</div></div>', unsafe_allow_html=True)

    with mc:
        active=st.session_state["tab"]

        # 자동 수집
        if st.session_state.get("auto_fetch") and active=="news":
            st.session_state["auto_fetch"]=False
            with st.spinner("뉴스 자동 수집 중..."):
                raw_ko=fetch_news(ko+" 배터리","ko","KR","KR:ko",8)
                st.session_state["news_ko"]=[{"title":e.title,"link":e.link,"lang":"ko","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_ko]
                raw_en=fetch_news(en,"en","US","US:en",8)
                st.session_state["news_en"]=[{"title":e.title,"link":e.link,"lang":"en","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_en]
                if st.session_state["step"]<1: st.session_state["step"]=1

        st.markdown('<div style="padding:28px 0;">', unsafe_allow_html=True)

        if active=="news":
            all_items=[("🇰🇷",i) for i in st.session_state["news_ko"]]+[("🌍",i) for i in st.session_state["news_en"]]
            if all_items:
                # 표지 카드
                feat_flag,feat=all_items[0]
                cover_img=next((img for n,_,_,_,img in TECH_HIGHLIGHTS if n==num),NEWS_IMGS[0])
                st.markdown(f"""
                <div class="cover-card">
                    <img src="{cover_img}" alt="cover">
                    <div class="cover-overlay"></div>
                    <div class="cover-body">
                        <div class="cover-tag">{feat_flag} 주요 뉴스 · TOPIC {num}</div>
                        <div class="cover-title"><a href="{feat['link']}" target="_blank">{feat['title']}</a></div>
                        <div class="cover-meta">{feat['source']} · {feat['published'][:16]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if len(all_items)>1:
                    sub_cols=st.columns(min(3,len(all_items)-1))
                    for ci,(flag,item) in enumerate(all_items[1:4]):
                        with sub_cols[ci]:
                            st.markdown(f"""
                            <div class="sub-news-card">
                                <div class="sub-news-tag">{flag} 뉴스</div>
                                <div class="sub-news-title"><a href="{item['link']}" target="_blank">{item['title'][:70]}{'...' if len(item['title'])>70 else ''}</a></div>
                                <div class="sub-news-meta">{item['source']} · {item['published'][:10]}</div>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("<hr style='border-color:#EEF0F3;margin:20px 0;'>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.75rem;color:#9EA5AF;margin-bottom:14px;'>전체 뉴스 {len(all_items)}건</div>", unsafe_allow_html=True)

            c1,c2=st.columns([4,1])
            with c1: run_news=st.button("🔄 뉴스 새로고침",type="primary",use_container_width=True)
            with c2:
                if st.button("초기화",use_container_width=True):
                    st.session_state["news_ko"]=[]; st.session_state["news_en"]=[]; st.rerun()
            if run_news:
                p=st.progress(0)
                p.progress(20)
                raw_ko=fetch_news(ko+" 배터리","ko","KR","KR:ko",8)
                st.session_state["news_ko"]=[{"title":e.title,"link":e.link,"lang":"ko","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_ko]
                p.progress(65)
                raw_en=fetch_news(en,"en","US","US:en",8)
                st.session_state["news_en"]=[{"title":e.title,"link":e.link,"lang":"en","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_en]
                p.progress(100); p.empty()
                if st.session_state["step"]<1: st.session_state["step"]=1
                st.rerun()

            all_items=[("🇰🇷",i) for i in st.session_state["news_ko"]]+[("🌍",i) for i in st.session_state["news_en"]]
            if all_items:
                for idx,(flag,item) in enumerate(all_items,1):
                    st.markdown(f'<div class="ni"><div class="ni-idx">{idx:02d}</div><div><div class="ni-flag">{flag} {item["source"]}</div><div class="ni-title"><a href="{item["link"]}" target="_blank">{item["title"]}</a></div><div class="ni-meta">📅 {item["published"]}</div></div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:50px;color:#9EA5AF;border:1px solid #EEF0F3;border-radius:4px;">위 버튼을 클릭해 뉴스를 수집하세요</div>', unsafe_allow_html=True)

        elif active=="papers":
            st.markdown('<div style="background:#E6F7F5;border-left:2px solid #00B4A0;padding:10px 16px;border-radius:0 4px 4px 0;font-size:0.82rem;color:#00796B;margin-bottom:16px;">💡 arXiv — 무료·안정적·최신 프리프린트 논문</div>', unsafe_allow_html=True)
            ca1,ca2=st.columns([4,1])
            with ca1: run_ax=st.button("🔍 arXiv 검색",type="primary",use_container_width=True)
            with ca2:
                if st.button("초기화 ",use_container_width=True):
                    st.session_state["arxiv"]=[]; st.rerun()
            if run_ax:
                with st.spinner("arXiv 검색 중..."):
                    results=fetch_arxiv(en,6)
                if results: st.session_state["arxiv"]=results; st.session_state["step"]=max(st.session_state["step"],2); st.rerun()
                else: st.error("결과 없음. 잠시 후 재시도하세요.")
            for p in st.session_state["arxiv"]:
                abs_t=(p['abstract'][:200]+"...") if len(p['abstract'])>200 else p['abstract']
                st.markdown(f'<div class="pi"><span class="pbadge pb-a">arXiv</span><div class="pi-title"><a href="{p["url"]}" target="_blank">{p["title"]}</a></div><div class="pi-auth">👤 {p["authors"]} | 📅 {p["published"]}</div><div class="pi-abs">{abs_t}</div></div>', unsafe_allow_html=True)

            st.markdown('<hr style="border-color:#EEF0F3;margin:20px 0;">', unsafe_allow_html=True)
            st.markdown('<div style="background:#FEF3C7;border-left:2px solid #D97706;padding:10px 16px;border-radius:0 4px 4px 0;font-size:0.82rem;color:#92400E;margin-bottom:16px;">⚠️ Google Scholar — 잦은 요청 시 일시 차단 가능</div>', unsafe_allow_html=True)
            cs1,cs2=st.columns([4,1])
            with cs1: run_sc=st.button("🔍 Google Scholar 검색",type="primary",use_container_width=True)
            with cs2:
                if st.button("초기화  ",use_container_width=True):
                    st.session_state["papers"]=[]; st.rerun()
            if run_sc:
                with st.spinner("Google Scholar 조회 중..."):
                    sch=fetch_scholar(en,4)
                st.session_state["papers"]=sch; st.session_state["step"]=max(st.session_state["step"],2); st.rerun()
            for p in st.session_state["papers"]:
                abs_t=(p['abstract'][:200]+"...") if len(p['abstract'])>200 else p['abstract']
                lh=f"<a href='{p['url']}' target='_blank' style='color:#00B4A0;font-size:0.75rem;'>원문 →</a>" if p.get('url') else ""
                st.markdown(f'<div class="pi"><span class="pbadge pb-s">Scholar</span><div class="pi-title">{p["title"]} ({p["year"]}) {lh}</div><div class="pi-auth">👤 {p["authors"]}{(" | 📔 "+p["journal"]) if p.get("journal") else ""}</div><div class="pi-abs">{abs_t}</div></div>', unsafe_allow_html=True)

        elif active=="select":
            an=st.session_state["news_ko"]+st.session_state["news_en"]
            ax=st.session_state["arxiv"]; asc=st.session_state["papers"]
            if not an and not ax and not asc:
                st.info("먼저 뉴스와 논문을 수집해주세요.")
            else:
                sn=[]; sa=[]; ss=[]
                if an:
                    st.markdown('<div class="sel-box">📰 보고서에 포함할 뉴스를 선택하세요</div>', unsafe_allow_html=True)
                    c1,c2=st.columns(2)
                    for i,item in enumerate(an):
                        flag="🇰🇷" if item.get("lang")=="ko" else "🌍"
                        with (c1 if i%2==0 else c2):
                            if st.checkbox(f"{flag} {item['title'][:50]}{'...' if len(item['title'])>50 else ''}",key=f"sn_{i}"): sn.append(item)
                if ax or asc:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="sel-box">📚 보고서에 포함할 논문을 선택하세요</div>', unsafe_allow_html=True)
                    if ax:
                        st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#B45309;margin:8px 0 4px;'>arXiv</div>", unsafe_allow_html=True)
                        for i,p in enumerate(ax):
                            if st.checkbox(f"[arXiv] {p['title'][:58]}{'...' if len(p['title'])>58 else ''} ({p['published'][:7]})",key=f"sa_{i}"): sa.append(p)
                    if asc:
                        st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#0369A1;margin:8px 0 4px;'>Google Scholar</div>", unsafe_allow_html=True)
                        for i,p in enumerate(asc):
                            if st.checkbox(f"[Scholar] {p['title'][:58]}{'...' if len(p['title'])>58 else ''} ({p['year']})",key=f"ss_{i}"): ss.append(p)

                st.session_state["sel_news"]=sn; st.session_state["sel_papers"]=ss; st.session_state["sel_arxiv"]=sa
                total=len(sn)+len(sa)+len(ss)
                if total>0:
                    st.success(f"✅ 뉴스 {len(sn)}건 + arXiv {len(sa)}편 + Scholar {len(ss)}편")
                    if st.session_state["step"]<3: st.session_state["step"]=3
                gen=st.button("📄 전문 보고서 자동 생성",type="primary",use_container_width=True,disabled=(total==0))
                if gen and total>0:
                    with st.spinner("보고서 생성 중..."):
                        nko=[n for n in sn if n.get("lang")=="ko"]
                        nen=[n for n in sn if n.get("lang")=="en"]
                        rpt=build_report(num,ko,en,bg,kw,nko,nen,ss,sa)
                        st.session_state["report"]=rpt
                        if st.session_state["step"]<4: st.session_state["step"]=4
                    st.success("✅ 보고서 생성 완료!")

        elif active=="report":
            rpt=st.session_state["report"]
            if rpt:
                st.markdown(f'<div class="report-out">', unsafe_allow_html=True)
                st.markdown(rpt)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:60px;color:#9EA5AF;border:1px solid #EEF0F3;border-radius:4px;">자료 선택 탭에서 보고서를 생성하세요</div>', unsafe_allow_html=True)

        elif active=="save":
            rpt=st.session_state["report"]
            if rpt:
                st.success("✅ 보고서 준비 완료")
                edited=st.text_area("✏️ 최종 수정",value=rpt,height=380,key=f"e_{num}")
                st.session_state["report"]=edited
                fb=f"BatteryIQ_{num}_{datetime.now().strftime('%Y%m%d')}"
                c1,c2,c3=st.columns(3)
                with c1: st.download_button("📄 TXT",data=edited,file_name=f"{fb}.txt",mime="text/plain",type="primary",use_container_width=True)
                with c2: st.download_button("📋 Markdown",data=edited,file_name=f"{fb}.md",mime="text/markdown",type="primary",use_container_width=True)
                with c3:
                    if st.button("🖨️ 인쇄/PDF",use_container_width=True): st.info("Ctrl+P → PDF")
            else:
                st.markdown('<div style="text-align:center;padding:60px;color:#9EA5AF;border:1px solid #EEF0F3;border-radius:4px;">보고서를 먼저 생성해주세요</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🔋 Battery<span>IQ</span></div>
        <div class="footer-copy">Battery Management Systems · Gregory Plett · Chapter 2-04</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# OVERVIEW — 연구 개요 페이지
# =====================================================================

# =====================================================================
# OVERVIEW — LG에너지솔루션 46시리즈 스타일 연구 개요
# =====================================================================
elif st.session_state["page"] == "overview":

    st.markdown("""
    <style>
    /* ── 전체 레이아웃 ── */
    .ov-wrap { background: var(--white); }

    /* ── 페이지 히어로 ── */
    .ov-page-hero {
        background: var(--navy);
        padding: 120px 72px 60px;
    }
    .ov-page-hero-crumb {
        font-size: 0.72rem; color: rgba(255,255,255,0.35);
        margin-bottom: 20px; display: flex; align-items: center; gap: 8px;
    }
    .ov-page-hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: clamp(2rem,4vw,3rem); font-weight: 800;
        color: var(--white); letter-spacing: -1px; line-height: 1.15;
    }

    /* ── 좌측 고정 사이드 네비 ── */
    .ov-layout {
        display: flex;
        min-height: 100vh;
    }
    .ov-sidenav {
        width: 220px;
        flex-shrink: 0;
        background: var(--white);
        border-right: 1px solid var(--gray2);
        padding: 36px 0;
        position: sticky;
        top: 68px;
        height: fit-content;
        align-self: flex-start;
    }
    .ov-sidenav-title {
        font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: var(--teal);
        padding: 0 28px; margin-bottom: 16px;
    }
    .ov-sidenav-item {
        display: block; padding: 12px 28px;
        font-size: 0.88rem; font-weight: 500;
        color: var(--gray4); cursor: pointer;
        border-left: 2px solid transparent;
        transition: all 0.15s;
    }
    .ov-sidenav-item.on {
        color: var(--navy); font-weight: 700;
        border-left-color: var(--teal);
        background: #F7F8FA;
    }
    .ov-sidenav-item:hover { color: var(--navy); }

    .ov-content { flex: 1; padding: 0; }

    /* ── 탭 바 (서브 탭) ── */
    .ov-tab-bar {
        display: flex; gap: 0;
        border-bottom: 2px solid var(--gray2);
        padding: 0 56px;
        background: var(--white);
        position: sticky; top: 68px; z-index: 80;
    }
    .ov-tab {
        padding: 16px 22px; font-size: 0.85rem; font-weight: 500;
        color: var(--gray4); border-bottom: 2px solid transparent;
        margin-bottom: -2px; cursor: pointer; white-space: nowrap;
        transition: all 0.15s; letter-spacing: 0.2px;
    }
    .ov-tab.on { color: var(--navy); border-bottom-color: var(--navy); font-weight: 700; }

    /* ── 섹션 공통 ── */
    .ov-sec { padding: 60px 56px; }
    .ov-sec-gray { background: #F0F4F8; }
    .ov-sec-white { background: var(--white); }
    .ov-sec-navy { background: var(--navy); color: var(--white); }

    .ov-sec-label {
        font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;
        text-transform: uppercase; color: var(--teal); margin-bottom: 12px;
    }
    .ov-sec-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.7rem; font-weight: 800;
        color: var(--navy); letter-spacing: -0.5px;
        line-height: 1.25; margin-bottom: 14px;
    }
    .ov-sec-title.white { color: var(--white); }
    .ov-sec-desc {
        font-size: 0.88rem; color: var(--gray5);
        line-height: 1.8; font-weight: 300; max-width: 600px;
        margin-bottom: 36px;
    }
    .ov-sec-desc.white { color: rgba(255,255,255,0.6); }

    /* ── 경쟁력 카드 ── */
    .ov-comp-box {
        background: var(--white); border-radius: 12px;
        padding: 28px 24px; border: 1px solid var(--gray2);
        transition: all 0.2s; height: 100%;
    }
    .ov-comp-box:hover {
        box-shadow: 0 8px 28px rgba(0,180,160,0.12);
        border-color: var(--teal); transform: translateY(-3px);
    }
    .ov-comp-num {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.5rem; font-weight: 800;
        color: var(--teal); opacity: 0.2;
        line-height: 1; margin-bottom: 12px;
    }
    .ov-comp-title { font-size: 0.95rem; font-weight: 700; color: var(--navy); margin-bottom: 8px; }
    .ov-comp-desc { font-size: 0.8rem; color: var(--gray5); line-height: 1.7; }

    /* ── 배터리 종류 타입탭 ── */
    .bt-type-tabs {
        display: flex; gap: 0; border-bottom: 2px solid var(--gray2);
        margin-bottom: 40px;
    }
    .bt-type-tab {
        padding: 12px 28px; font-size: 0.9rem; font-weight: 600;
        color: var(--gray4); border-bottom: 3px solid transparent;
        margin-bottom: -2px; cursor: pointer; transition: all 0.15s;
    }
    .bt-type-tab.on {
        color: var(--navy); border-bottom-color: var(--navy);
        background: rgba(0,0,0,0.03);
    }

    /* ── 성능 지표 바 ── */
    .ov-bar-row {
        display: flex; align-items: center; gap: 16px;
        padding: 14px 0; border-bottom: 1px solid var(--gray2);
    }
    .ov-bar-label { font-size: 0.82rem; color: var(--navy); font-weight: 500; min-width: 160px; }
    .ov-bar-bg { flex: 1; background: var(--gray2); border-radius: 20px; height: 8px; }
    .ov-bar-fill { height: 8px; border-radius: 20px; background: var(--teal); }
    .ov-bar-val { font-size: 0.8rem; font-weight: 700; color: var(--teal); min-width: 36px; text-align: right; }

    /* ── 공정 단계 ── */
    .ov-process-row {
        display: flex; gap: 0; align-items: stretch;
        margin-bottom: 2px;
    }
    .ov-process-step {
        flex: 1; background: var(--white);
        border: 1px solid var(--gray2); padding: 28px 22px;
        text-align: center; transition: all 0.2s; position: relative;
    }
    .ov-process-step:hover { border-color: var(--teal); }
    .ov-process-step:hover .ov-ps-icon { background: var(--teal); color: white; }
    .ov-ps-icon {
        width: 56px; height: 56px; border-radius: 50%;
        background: #E6F7F5; display: flex; align-items: center;
        justify-content: center; font-size: 1.4rem;
        margin: 0 auto 14px; transition: all 0.2s;
    }
    .ov-ps-title { font-size: 0.85rem; font-weight: 700; color: var(--navy); margin-bottom: 6px; }
    .ov-ps-desc { font-size: 0.74rem; color: var(--gray4); line-height: 1.55; }
    .ov-process-arrow {
        display: flex; align-items: center; padding: 0;
        color: var(--gray3); font-size: 1.2rem;
        background: #F7F8FA; border-top: 1px solid var(--gray2);
        border-bottom: 1px solid var(--gray2);
        padding: 0 6px;
    }

    /* ── 혁신 기술 카드 ── */
    .ov-innov-card {
        background: var(--white); border: 1px solid var(--gray2);
        border-radius: 8px; padding: 24px;
        display: flex; gap: 18px;
        transition: all 0.2s; margin-bottom: 12px;
    }
    .ov-innov-card:hover { border-color: var(--teal); box-shadow: 0 4px 16px rgba(0,180,160,0.1); }
    .ov-innov-icon {
        width: 52px; height: 52px; border-radius: 10px;
        background: #E6F7F5; display: flex; align-items: center;
        justify-content: center; font-size: 1.4rem; flex-shrink: 0;
    }
    .ov-innov-title { font-size: 0.92rem; font-weight: 700; color: var(--navy); margin-bottom: 6px; }
    .ov-innov-desc { font-size: 0.8rem; color: var(--gray5); line-height: 1.65; }
    .ov-innov-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
    .ov-innov-tag {
        background: #E6F7F5; color: #00796B; border-radius: 20px;
        padding: 2px 10px; font-size: 0.72rem; font-weight: 500;
    }

    /* ── 산업별 카드 ── */
    .ov-ind-card {
        background: #F0F4F8; border: 1px solid var(--gray2);
        border-radius: 16px; padding: 28px;
        display: flex; justify-content: space-between;
        align-items: flex-end; min-height: 180px;
        transition: all 0.25s; cursor: default;
        position: relative; overflow: hidden;
    }
    .ov-ind-card:hover {
        border-color: var(--teal);
        box-shadow: 0 8px 32px rgba(0,180,160,0.12);
    }
    .ov-ind-card:hover .ov-ind-arrow { color: var(--teal); }
    .ov-ind-name { font-size: 1.1rem; font-weight: 800; color: var(--navy); margin-bottom: 6px; }
    .ov-ind-desc { font-size: 0.78rem; color: var(--gray5); line-height: 1.6; max-width: 200px; }
    .ov-ind-arrow { font-size: 0.8rem; color: var(--gray4); font-weight: 600; transition: color 0.2s; margin-top: 8px; display: block; }
    .ov-ind-icon { font-size: 3.5rem; opacity: 0.7; }

    /* ── 비교 테이블 ── */
    .ov-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; margin-top: 28px; }
    .ov-table thead tr { background: var(--navy); color: white; }
    .ov-table th { padding: 14px 16px; text-align: left; font-weight: 600; }
    .ov-table td { padding: 13px 16px; border-bottom: 1px solid #EEF0F3; color: var(--gray5); }
    .ov-table tr:nth-child(even) td { background: #F7F8FA; }
    .ov-table tr.highlight td { color: var(--navy); font-weight: 600; }
    .ov-table .teal { color: var(--teal); font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

    # 페이지 히어로
    st.markdown("""
    <div class="ov-page-hero">
        <div class="ov-page-hero-crumb">BatteryIQ <span>›</span> 연구 개요</div>
        <div class="ov-page-hero-title">배터리 건강 추정<br>연구 개요</div>
    </div>
    """, unsafe_allow_html=True)

    # 사이드네비 + 콘텐츠 2단 레이아웃
    side_col, content_col = st.columns([2, 8], gap="small")

    ov_nav_items = [
        ("competitiveness", "경쟁력"),
        ("performance",     "알고리즘 성능"),
        ("process",         "핵심 공정"),
        ("innovation",      "혁신 기술"),
        ("industry",        "산업별 적용"),
    ]

    # 현재 탭이 삭제된 battery_type이면 competitiveness로 리셋
    if st.session_state["overview_tab"] == "battery_type":
        st.session_state["overview_tab"] = "competitiveness"

    with side_col:
        # LG 스타일 사이드 네비 + 스크롤 자동 하이라이트 JS
        nav_ids = [tk for tk, _ in ov_nav_items]
        active_idx = next((i for i,(_tk,_) in enumerate(ov_nav_items) if _tk == st.session_state["overview_tab"]), 0)
        nav_html = '<div class="ov-sidenav" id="ov-sidenav"><div class="ov-sidenav-title">연구 개요</div>'
        for tk, tl in ov_nav_items:
            cls = "on" if st.session_state["overview_tab"] == tk else ""
            nav_html += f'<div class="ov-sidenav-item {cls}" data-section="{tk}" id="nav-{tk}">{tl}</div>'
        nav_html += '</div>'

        # 스크롤 감지 JS — 섹션 위치 기반으로 사이드바 자동 하이라이트
        scroll_js = f"""
        <script>
        (function() {{
            const sectionIds = {nav_ids};
            function updateNav() {{
                const scrollY = window.scrollY || document.documentElement.scrollTop;
                const winH = window.innerHeight;
                let current = sectionIds[0];
                sectionIds.forEach(id => {{
                    const el = document.getElementById('sec-' + id);
                    if (el) {{
                        const rect = el.getBoundingClientRect();
                        if (rect.top <= winH * 0.4) current = id;
                    }}
                }});
                document.querySelectorAll('.ov-sidenav-item').forEach(item => {{
                    item.classList.remove('on');
                    if (item.getAttribute('data-section') === current) {{
                        item.classList.add('on');
                    }}
                }});
            }}
            window.addEventListener('scroll', updateNav, {{passive: true}});
            updateNav();
        }})();
        </script>
        """
        st.markdown(nav_html + scroll_js, unsafe_allow_html=True)

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        if st.button("← 홈으로", key="ov_back"):
            st.session_state["page"] = "home"; st.rerun()
        # 탭 전환용 실제 버튼 (사이드 네비 아래 투명하게)
        st.markdown('<style>.stButton>button{font-size:0.82rem;text-align:left;padding:10px 16px;border-radius:4px;}</style>', unsafe_allow_html=True)
        for tk, tl in ov_nav_items:
            if st.button(tl, key=f"ovnav_{tk}", use_container_width=True):
                st.session_state["overview_tab"] = tk; st.rerun()

    ov = st.session_state["overview_tab"]

    with content_col:

        # ── 탭 바 (경쟁력 → 세부 항목)
        if ov == "competitiveness":
            comp_tabs = [("overview","핵심 경쟁력"), ("compare","알고리즘 비교")]
            tb_html = '<div class="ov-tab-bar">'
            for tk, tl in comp_tabs:
                cls2 = "on" if st.session_state.get("comp_sub","overview") == tk else ""
                tb_html += f'<span class="ov-tab {cls2}">{tl}</span>'
            tb_html += "</div>"
            st.markdown(tb_html, unsafe_allow_html=True)
            tc2 = st.columns(len(comp_tabs))
            for i,(tk,tl) in enumerate(comp_tabs):
                with tc2[i]:
                    if st.button(tl, key=f"csub_{tk}", use_container_width=True):
                        st.session_state["comp_sub"] = tk; st.rerun()

        # 섹션 ID 마커 (스크롤 감지용)
        st.markdown(f'<div id="sec-{ov}" style="height:0;"></div>', unsafe_allow_html=True)

        # ────────────────────────────────────
        # 1. 경쟁력
        # ────────────────────────────────────
        if ov == "competitiveness":
            comp_sub = st.session_state.get("comp_sub","overview")

            if comp_sub == "overview":
                st.markdown("""
                <div class="ov-sec ov-sec-white">
                    <div class="ov-sec-label">Core Competitiveness</div>
                    <div class="ov-sec-title">핵심 경쟁력</div>
                    <div class="ov-sec-desc">배터리 건강 상태(SOH) 추정은 고에너지·고안전성 배터리 시스템 구현의 핵심 기술로,
                    과충전·과방전 방지와 잔여 수명 예측에 필수적입니다.</div>
                </div>
                <style>
                .comp-photo-card {
                    background: var(--white);
                    border: 1px solid var(--gray2);
                    border-radius: 12px;
                    overflow: hidden;
                    margin-bottom: 14px;
                    transition: all 0.25s;
                }
                .comp-photo-card:hover {
                    box-shadow: 0 12px 36px rgba(0,180,160,0.14);
                    border-color: var(--teal);
                    transform: translateY(-4px);
                }
                .comp-photo-card:hover .comp-photo-img { transform: scale(1.05); filter: brightness(0.95); }
                .comp-photo-img-wrap { overflow: hidden; height: 160px; }
                .comp-photo-img {
                    width: 100%; height: 160px;
                    object-fit: cover; display: block;
                    filter: brightness(0.88);
                    transition: transform 0.4s ease, filter 0.3s;
                }
                .comp-photo-body { padding: 20px 20px 22px; }
                .comp-photo-num {
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    font-size: 2rem; font-weight: 800;
                    color: var(--teal); opacity: 0.18;
                    line-height: 1; margin-bottom: 8px;
                }
                .comp-photo-title {
                    font-size: 0.92rem; font-weight: 700;
                    color: var(--navy); margin-bottom: 8px;
                    letter-spacing: -0.2px;
                }
                .comp-photo-desc {
                    font-size: 0.78rem; color: var(--gray5); line-height: 1.7;
                }
                /* 배터리 적용 범위 고급 카드 */
                .range-card {
                    background: var(--white);
                    border: 1px solid var(--gray2);
                    border-radius: 12px;
                    overflow: hidden;
                    transition: all 0.25s;
                    flex: 1;
                }
                .range-card:hover {
                    box-shadow: 0 12px 40px rgba(0,180,160,0.13);
                    border-color: var(--teal);
                }
                .range-card-img-wrap {
                    background: #F8FFFE;
                    display: flex; align-items: center;
                    justify-content: center;
                    height: 200px; padding: 24px;
                    border-bottom: 1px solid var(--gray2);
                }
                .range-card-img {
                    max-width: 100%; max-height: 160px;
                    object-fit: contain; display: block;
                    transition: transform 0.4s ease;
                }
                .range-card:hover .range-card-img { transform: scale(1.06); }
                .range-card-body { padding: 22px 22px 24px; }
                .range-card-title {
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    font-size: 1.05rem; font-weight: 800;
                    color: var(--navy); margin-bottom: 6px;
                    letter-spacing: -0.3px;
                }
                .range-card-sub {
                    font-size: 0.75rem; color: var(--teal);
                    font-weight: 600; margin-bottom: 10px;
                    letter-spacing: 0.5px;
                }
                .range-card-desc { font-size: 0.78rem; color: var(--gray5); line-height: 1.65; }
                </style>
                """, unsafe_allow_html=True)

                # 경쟁력 6개 — 사진 포함 카드
                comps = [
                    ("01", "안전성 확보",
                     "과충전·과방전 실시간 방지로 배터리 열폭주 위험을 사전 예방합니다.",
                     "https://images.unsplash.com/photo-1597852074816-d933c7d2b988?w=600&h=320&fit=crop&auto=format"),
                    ("02", "수명 예측 (RUL)",
                     "잔여 유용 수명을 정확히 예측하여 교체 시점을 최적화합니다.",
                     "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&h=320&fit=crop&auto=format"),
                    ("03", "성능 최적화",
                     "실시간 SOH로 에너지 관리 전략을 최적화, 주행거리를 극대화합니다.",
                     "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=320&fit=crop&auto=format"),
                    ("04", "배터리 재사용",
                     "2차 활용 가능 배터리를 정밀 선별하여 순환경제를 실현합니다.",
                     "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&h=320&fit=crop&auto=format"),
                    ("05", "비용 절감",
                     "불필요한 조기 교체 방지로 총 소유 비용(TCO)을 절감합니다.",
                     "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=320&fit=crop&auto=format"),
                    ("06", "실시간 모니터링",
                     "주행 중에도 배터리 상태를 실시간 추정하여 즉각 대응합니다.",
                     "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=320&fit=crop&auto=format"),
                ]

                c1, c2, c3 = st.columns(3, gap="small")
                for i, (num, title, desc, img) in enumerate(comps):
                    with [c1, c2, c3][i % 3]:
                        st.markdown(f"""
                        <div class="comp-photo-card">
                            <div class="comp-photo-img-wrap">
                                <img class="comp-photo-img" src="{img}" alt="{title}">
                            </div>
                            <div class="comp-photo-body">
                                <div class="comp-photo-num">{num}</div>
                                <div class="comp-photo-title">{title}</div>
                                <div class="comp-photo-desc">{desc}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)


            else:  # compare
                st.markdown("""
                <div class="ov-sec ov-sec-white">
                    <div class="ov-sec-label">Algorithm Comparison</div>
                    <div class="ov-sec-title">알고리즘 비교</div>
                    <div class="ov-sec-desc">SOH 추정 방법별 정확도·실시간성·계산량을 비교하여 최적 알고리즘을 선택하세요.</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div style="padding:0 56px 56px;">
                <table class="ov-table">
                <thead><tr>
                    <th>방법</th><th>정확도</th><th>실시간성</th>
                    <th>계산량</th><th>노이즈 강인성</th><th>주요 적용</th>
                </tr></thead><tbody>
                <tr><td>쿨롱 카운팅</td><td>⭐⭐</td><td>✅</td><td class="teal">낮음</td><td>❌</td><td>간단한 BMS</td></tr>
                <tr><td>OCV 기반</td><td>⭐⭐⭐</td><td>❌</td><td class="teal">낮음</td><td>✅</td><td>초기화 시점</td></tr>
                <tr><td>최소제곱법 (OLS)</td><td>⭐⭐⭐</td><td>✅</td><td class="teal">낮음</td><td>보통</td><td>용량 추정</td></tr>
                <tr><td>WLS / TLS</td><td>⭐⭐⭐⭐</td><td>✅</td><td>보통</td><td>✅</td><td>정밀 용량 추정</td></tr>
                <tr><td>EKF</td><td>⭐⭐⭐⭐</td><td>✅</td><td>보통</td><td>✅</td><td>EV BMS</td></tr>
                <tr class="highlight"><td><b style="color:#00B4A0;">SPKF / UKF ★</b></td><td>⭐⭐⭐⭐⭐</td><td>✅</td><td>보통</td><td>✅✅</td><td>고성능 EV</td></tr>
                <tr><td>머신러닝</td><td>⭐⭐⭐⭐⭐</td><td>보통</td><td style="color:#EF4444;">높음</td><td>✅✅</td><td>클라우드 BMS</td></tr>
                </tbody></table>
                </div>
                """, unsafe_allow_html=True)

        # ────────────────────────────────────
        # 2. 배터리 종류
        # ────────────────────────────────────
        # ────────────────────────────────────
        # 2. 알고리즘 성능
        # ────────────────────────────────────
        elif ov == "performance":
            st.markdown("""
            <div class="ov-sec ov-sec-white">
                <div class="ov-sec-label">Algorithm Performance</div>
                <div class="ov-sec-title">알고리즘 성능 비교</div>
                <div class="ov-sec-desc">Gregory Plett Chapter 2-04에서 다루는 핵심 SOH 추정 알고리즘의 성능을 5가지 지표로 비교합니다.
                EV BMS 실적용을 위한 알고리즘 선택의 기준이 됩니다.</div>
            </div>
            """, unsafe_allow_html=True)

            methods = [
                ("칼만 필터 (KF)", [("정확도",72),("실시간성",95),("노이즈 강인성",80),("계산 효율",92),("수렴 속도",85)]),
                ("확장 칼만 필터 (EKF)", [("정확도",84),("실시간성",88),("노이즈 강인성",85),("계산 효율",80),("수렴 속도",82)]),
                ("SPKF / UKF", [("정확도",93),("실시간성",82),("노이즈 강인성",92),("계산 효율",72),("수렴 속도",88)]),
                ("머신러닝 기반", [("정확도",96),("실시간성",75),("노이즈 강인성",90),("계산 효율",55),("수렴 속도",70)]),
            ]
            for method, bars in methods:
                st.markdown(f"""
                <div style="background:#F7F8FA;border:1px solid #EEF0F3;border-radius:8px;
                            padding:22px 26px;margin-bottom:16px;">
                    <div style="font-size:0.92rem;font-weight:700;color:#0D1B2A;margin-bottom:16px;">{method}</div>
                """, unsafe_allow_html=True)
                for label, val in bars:
                    clr = "#00B4A0" if val>=88 else ("#F59E0B" if val>=72 else "#EF4444")
                    st.markdown(f"""
                    <div class="ov-bar-row">
                        <div class="ov-bar-label">{label}</div>
                        <div class="ov-bar-bg"><div class="ov-bar-fill" style="width:{val}%;background:{clr};"></div></div>
                        <div class="ov-bar-val" style="color:{clr};">{val}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ────────────────────────────────────
        # 4. 핵심 공정
        # ────────────────────────────────────
        elif ov == "process":
            st.markdown("""
            <div class="ov-sec ov-sec-white">
                <div class="ov-sec-label">Estimation Process</div>
                <div class="ov-sec-title">SOH 추정 핵심 공정</div>
                <div class="ov-sec-desc">센서 수집부터 검증까지 — 배터리 건강 추정의 5단계 공정을 탐색하세요.</div>
            </div>
            """, unsafe_allow_html=True)

            steps = [
                ("📡","센서 데이터 수집","전압·전류·온도 고정밀 실시간 수집"),
                ("🔧","등가 회로 모델링","R₀·R₁C₁·OCV 파라미터 정의"),
                ("📐","파라미터 식별","OLS·WLS·TLS로 파라미터 추정"),
                ("🎯","상태 추정 (필터)","EKF·SPKF로 SOC·SOH 실시간 추정"),
                ("✅","검증 및 보정","RMSE·MAE 평가 및 모델 업데이트"),
            ]
            step_html = '<div class="ov-process-row">'
            for i, (icon, title, desc) in enumerate(steps):
                step_html += f"""
                <div class="ov-process-step">
                    <div class="ov-ps-icon">{icon}</div>
                    <div class="ov-ps-title">{title}</div>
                    <div class="ov-ps-desc">{desc}</div>
                </div>"""
                if i < len(steps)-1:
                    step_html += '<div class="ov-process-arrow">›</div>'
            step_html += "</div>"
            st.markdown(f'<div style="padding:0 56px 40px;">{step_html}</div>', unsafe_allow_html=True)

            # 상세
            details = [
                ("등가 회로 모델 (ECM)", "배터리를 RC 회로로 모델링하여 실시간 계산을 가능하게 합니다.",
                 ["R₀ : 순수 내부 저항 — 즉각 전압 강하","R₁C₁ : 전기화학 분극 — 시정수 τ=R₁C₁",
                  "OCV : 개방 회로 전압 — SOC의 비선형 함수","V = OCV - I·R₀ - V_RC"]),
                ("칼만 필터 추정 공정", "예측-업데이트 반복으로 노이즈를 제거하며 최적 추정합니다.",
                 ["예측: x̂⁻ = f(x̂, u) — 상태 전파","예측: P⁻ = F·P·Fᵀ + Q — 오차 공분산",
                  "업데이트: K = P⁻Hᵀ(HP⁻Hᵀ+R)⁻¹ — 칼만 이득","업데이트: x̂ = x̂⁻ + K(y - h(x̂⁻)) — 상태 보정"]),
            ]
            for d_title, d_desc, d_items in details:
                items_html = "".join([f'<div style="font-size:0.79rem;color:#334155;padding:5px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ {it}</div>' for it in d_items])
                st.markdown(f"""
                <div style="padding:0 56px;margin-bottom:16px;">
                <div style="background:#F0F4F8;border-left:3px solid #00B4A0;
                            border-radius:0 8px 8px 0;padding:22px 24px;">
                    <div style="font-size:0.92rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">{d_title}</div>
                    <div style="font-size:0.8rem;color:#6B7280;margin-bottom:12px;">{d_desc}</div>
                    {items_html}
                </div></div>
                """, unsafe_allow_html=True)

        # ────────────────────────────────────
        # 5. 혁신 기술
        # ────────────────────────────────────
        elif ov == "innovation":
            st.markdown("""
            <div class="ov-sec ov-sec-white">
                <div class="ov-sec-label">Innovation Technology</div>
                <div class="ov-sec-title">혁신 기술</div>
                <div class="ov-sec-desc">AI·디지털 트윈·클라우드와 결합한 차세대 SOH 추정 기술을 탐색하세요.</div>
            </div>
            """, unsafe_allow_html=True)

            innovations = [
                ("🤖","AI / 머신러닝 기반 SOH","딥러닝(LSTM·Transformer)과 물리 기반 모델을 결합한 하이브리드 방식으로 정확도를 대폭 향상시킵니다.",["LSTM 시계열 예측","Physics-Informed NN","온라인 학습","이상 탐지"]),
                ("🌐","디지털 트윈","실제 배터리와 동기화된 가상 모델로 SOH 추정 정확도와 예측 범위를 혁신적으로 확장합니다.",["실시간 물리 모델","가속 열화 시뮬","수명 예측 정밀화","가상 환경 테스트"]),
                ("☁️","클라우드 BMS","차량 군집 빅데이터를 통합 분석하여 집단 지성형 SOH 모델을 지속 개선합니다.",["OTA 모델 업데이트","Fleet 데이터 분석","엣지-클라우드 분산","개인화 보정"]),
                ("⚡","전고체 배터리 대응","차세대 전고체 배터리의 새로운 열화 메커니즘에 특화된 SOH 추정 방법론을 개발합니다.",["계면 저항 추적","덴드라이트 감지","고온 내구성","새 ECM 파라미터"]),
                ("📡","EIS 기반 진단","전기화학 임피던스 분광법으로 배터리 내부 상태를 비침습적으로 정밀 진단합니다.",["주파수 대역 분리","온라인 EIS 측정","SOH·SOP 동시 추정","열화 메커니즘 분석"]),
                ("🔗","조인트·듀얼 추정 고도화","SOC·SOH 동시 추정 필터를 고도화하여 파라미터 식별 정확도를 극대화합니다.",["적응형 노이즈","다중 모델 전환","강인한 초기화","실시간 파라미터 업데이트"]),
            ]
            c1, c2 = st.columns(2, gap="small")
            for i,(icon,title,desc,tags) in enumerate(innovations):
                tag_html = "".join([f'<span class="ov-innov-tag">{t}</span>' for t in tags])
                with (c1 if i%2==0 else c2):
                    st.markdown(f"""
                    <div class="ov-innov-card">
                        <div class="ov-innov-icon">{icon}</div>
                        <div>
                            <div class="ov-innov-title">{title}</div>
                            <div class="ov-innov-desc">{desc}</div>
                            <div class="ov-innov-tags">{tag_html}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # ────────────────────────────────────
        # 6. 산업별 적용
        # ────────────────────────────────────
        elif ov == "industry":
            st.markdown("""
            <div class="ov-sec ov-sec-white">
                <div class="ov-sec-label">Industry Solutions</div>
                <div class="ov-sec-title">산업별 솔루션</div>
                <div class="ov-sec-desc">배터리 건강 추정 기술은 다양한 산업에 핵심 기술로 적용됩니다. 각 분야를 클릭하여 자세한 내용을 확인하세요.</div>
            </div>
            """, unsafe_allow_html=True)

            industries = [
                ("승용 EV","🚗","#E6F7F5","주행거리 보장과 충전 최적화에 SOH 추정이 직접 활용됩니다.","자세히 보기 →"),
                ("상용 EV","🚛","#EFF6FF","대용량 배터리팩의 SOH를 정밀 관리하여 안정적 운행을 보장합니다.","자세히 보기 →"),
                ("ESS (에너지저장)","🏭","#F0FDF4","재생에너지 연계 ESS에서 SOH 기반 충방전 전략으로 효율을 극대화합니다.","자세히 보기 →"),
                ("LEV (경량 모빌리티)","🛵","#FFF7ED","경량화된 SOH 알고리즘으로 전동 킥보드·자전거를 관리합니다.","자세히 보기 →"),
                ("로봇·중장비","🤖","#FDF2F8","극한 환경의 산업용 배터리를 안전하게 실시간 관리합니다.","자세히 보기 →"),
                ("항공·드론","✈️","#F0F9FF","비행 중 실시간 SOH 추정으로 안전 귀환을 보장합니다.","자세히 보기 →"),
            ]

            c1, c2 = st.columns(2, gap="small")
            for i, (name, icon, bg, desc, link) in enumerate(industries):
                with (c1 if i%2==0 else c2):
                    st.markdown(f"""
                    <div class="ov-ind-card" style="background:{bg};margin-bottom:14px;">
                        <div>
                            <div class="ov-ind-name">{name}</div>
                            <div class="ov-ind-desc">{desc}</div>
                            <span class="ov-ind-arrow">{link}</span>
                        </div>
                        <div class="ov-ind-icon">{icon}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🔋 Battery<span>IQ</span></div>
        <div class="footer-copy">Battery Management Systems · Gregory Plett · Chapter 2-04</div>
    </div>
    """, unsafe_allow_html=True)
