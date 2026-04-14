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

/* -- 버튼 공통 -- */
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

st.markdown("""
<style>
/* -- GNB 전체 스타일 -- */
.stApp > div > div > div > div:first-child [data-testid="stHorizontalBlock"] {
    position: fixed !important;
    top: 0 !important; left: 0 !important; right: 0 !important;
    z-index: 9999 !important;
    background: rgba(255,255,255,0.97) !important;
    backdrop-filter: blur(10px) !important;
    border-bottom: 1px solid #E2E8F0 !important;
    padding: 0 !important;
    margin: 0 !important;
    height: 64px !important;
    align-items: center !important;
    gap: 0 !important;
}
/* 모든 GNB 버튼 초기화 */
[data-testid="stHorizontalBlock"]:first-of-type button {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    color: #6B7280 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 0 20px !important;
    height: 64px !important;
    width: 100% !important;
    letter-spacing: 0.2px !important;
    transition: color 0.15s !important;
}
[data-testid="stHorizontalBlock"]:first-of-type button:hover {
    color: #00B4A0 !important;
    background: transparent !important;
    border-bottom: 2px solid #00B4A0 !important;
}
/* 로고 컬럼 */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    color: #0D1B2A !important;
    justify-content: flex-start !important;
    padding-left: 28px !important;
}
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:first-child button:hover {
    color: #0D1B2A !important;
    border-bottom: none !important;
}
/* 우측 빈 컬럼 */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:last-child {
    flex: 2 !important;
}
/* 페이지 상단 여백 */
.main-spacer { height: 8px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# -- GNB — 단일 컬럼 행 --
logo_col, nav1, nav2, nav3, nav4, right_col = st.columns([3, 1.2, 1.2, 1, 1.4, 2])

with logo_col:
    st.button("🟩 BatteryIQ", key="gnb_logo")

with nav1:
    if st.button("연구 개요", key="gnb_ov"):
        st.session_state["page"] = "overview"; st.rerun()

with nav2:
    if st.button("핵심 기술", key="gnb_tech"):
        st.session_state["page"] = "home"; st.rerun()

with nav3:
    if st.button("뉴스룸", key="gnb_news"):
        st.session_state["page"] = "home"; st.rerun()

with nav4:
    if st.button("24개 주제", key="gnb_topics"):
        st.session_state["page"] = "home"
        st.session_state["show_topic_nav"] = True; st.rerun()

with right_col:
    st.markdown(
        '<div style="height:64px;display:flex;align-items:center;'
        'justify-content:flex-end;padding-right:24px;'
        f'font-size:0.74rem;color:#9EA5AF;">Gregory Plett · Ch 2-04 &nbsp;|&nbsp; 📰{nc}건 📚{pc}편</div>',
        unsafe_allow_html=True
    )

st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

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

    # -- LG 스타일 다크 배너 (영상 배경) --
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
# OVERVIEW — LG 스타일 단일 스크롤 페이지
# =====================================================================

# =====================================================================
# OVERVIEW — 단일 HTML 블록 (sticky 사이드바 완전 지원)
# =====================================================================

elif st.session_state["page"] == "overview":

    bc, _ = st.columns([2, 8])
    with bc:
        if st.button("← 홈으로", key="ov_back"):
            st.session_state["page"] = "home"; st.rerun()

    # 개요 히어로
    st.markdown("""
    <div style="background:#0D1B2A;padding:110px 72px 56px;">
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.3);margin-bottom:18px;">BatteryIQ › 연구 개요</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);
                    font-weight:800;color:#fff;letter-spacing:-1px;line-height:1.15;">
            배터리 건강 추정<br>연구 개요
        </div>
    </div>
    """, unsafe_allow_html=True)

    import streamlit.components.v1 as components


    full_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#fff;color:#0D1B2A;}
.root{display:flex;align-items:flex-start;min-height:100vh;}
.sidebar{width:220px;flex-shrink:0;position:sticky;top:0;height:100vh;overflow-y:auto;
    background:#fff;border-right:1px solid #E2E8F0;padding:32px 0;}
.sidebar-label{font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
    color:#00B4A0;padding:0 24px;margin-bottom:16px;}
.nav-a{display:block;padding:12px 24px;font-size:0.88rem;font-weight:400;color:#9EA5AF;
    text-decoration:none;border-left:2px solid transparent;border-bottom:1px solid #F1F5F9;
    cursor:pointer;transition:all 0.15s;}
.nav-a:last-child{border-bottom:none;}
.nav-a:hover{color:#0D1B2A;padding-left:30px;}
.nav-a.on{color:#0D1B2A;font-weight:700;border-left-color:#00B4A0;background:#F7F8FA;}
.body{flex:1;overflow:hidden;}
.sec{padding:64px 60px;border-bottom:1px solid #E2E8F0;scroll-margin-top:10px;}
.sec-w{background:#fff;}
.sec-g{background:#F0F4F8;}
.sec-lbl{font-size:0.62rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
    color:#00B4A0;margin-bottom:10px;display:flex;align-items:center;gap:8px;}
.sec-lbl::before{content:'';display:block;width:18px;height:1px;background:#00B4A0;}
.sec-ttl{font-family:'Plus Jakarta Sans',sans-serif;font-size:1.7rem;font-weight:800;
    color:#0D1B2A;letter-spacing:-0.5px;line-height:1.2;margin-bottom:12px;}
.sec-dsc{font-size:0.84rem;color:#6B7280;line-height:1.8;max-width:620px;}
</style>
</head>
<body>
<div class="root">
<div class="sidebar">
    <div class="sidebar-label">연구 개요</div>
    <a class="nav-a on" id="nav-c" onclick="go('c')">경쟁력</a>
    <a class="nav-a" id="nav-p" onclick="go('p')">알고리즘 성능</a>
    <a class="nav-a" id="nav-pr" onclick="go('pr')">핵심 공정</a>
    <a class="nav-a" id="nav-i" onclick="go('i')">혁신 기술</a>
    <a class="nav-a" id="nav-d" onclick="go('d')">산업별 적용</a>
</div>
<div class="body" id="body">

<div class="sec sec-w" id="s-c">
<div class="sec-lbl">Core Competitiveness</div>
<div class="sec-ttl">경쟁력</div>
<div class="sec-dsc">배터리 건강 상태(SOH) 추정은 전기차·ESS 안전 운용의 핵심 기술입니다. 정확한 SOH 추정은 안전성·수명·성능·비용 모든 면에서 경쟁력을 결정합니다.</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:28px;"><div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;"><div style="overflow:hidden;height:140px;"><img src="https://images.unsplash.com/photo-1597852074816-d933c7d2b988?w=600&h=260&fit=crop" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.85);display:block;"></div><div style="padding:16px 18px;"><div style="font-size:1.8rem;font-weight:800;color:#00B4A0;opacity:0.18;line-height:1;margin-bottom:6px;">01</div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">안전성 확보</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.65;">과충전·과방전 실시간 방지로 배터리 열폭주 위험을 사전 예방합니다.</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;"><div style="overflow:hidden;height:140px;"><img src="https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&h=260&fit=crop" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.85);display:block;"></div><div style="padding:16px 18px;"><div style="font-size:1.8rem;font-weight:800;color:#00B4A0;opacity:0.18;line-height:1;margin-bottom:6px;">02</div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">수명 예측 (RUL)</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.65;">잔여 유용 수명을 정확히 예측하여 교체 시점을 최적화합니다.</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;"><div style="overflow:hidden;height:140px;"><img src="https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=260&fit=crop" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.85);display:block;"></div><div style="padding:16px 18px;"><div style="font-size:1.8rem;font-weight:800;color:#00B4A0;opacity:0.18;line-height:1;margin-bottom:6px;">03</div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">성능 최적화</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.65;">실시간 SOH로 에너지 관리 전략을 최적화, 주행거리를 극대화합니다.</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;"><div style="overflow:hidden;height:140px;"><img src="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=600&h=260&fit=crop" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.85);display:block;"></div><div style="padding:16px 18px;"><div style="font-size:1.8rem;font-weight:800;color:#00B4A0;opacity:0.18;line-height:1;margin-bottom:6px;">04</div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">배터리 재사용</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.65;">2차 활용 가능 배터리를 정밀 선별하여 순환경제를 실현합니다.</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;"><div style="overflow:hidden;height:140px;"><img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=260&fit=crop" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.85);display:block;"></div><div style="padding:16px 18px;"><div style="font-size:1.8rem;font-weight:800;color:#00B4A0;opacity:0.18;line-height:1;margin-bottom:6px;">05</div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">비용 절감</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.65;">불필요한 조기 교체 방지로 총 소유 비용(TCO)을 절감합니다.</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden;"><div style="overflow:hidden;height:140px;"><img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=260&fit=crop" style="width:100%;height:140px;object-fit:cover;filter:brightness(0.85);display:block;"></div><div style="padding:16px 18px;"><div style="font-size:1.8rem;font-weight:800;color:#00B4A0;opacity:0.18;line-height:1;margin-bottom:6px;">06</div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">실시간 모니터링</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.65;">주행 중에도 배터리 상태를 실시간 추정하여 즉각 대응합니다.</div></div></div></div>
</div>

<div class="sec sec-g">
<div class="sec-lbl">Algorithm Comparison</div>
<div class="sec-ttl">알고리즘 비교</div>
<div class="sec-dsc">SOH 추정 방법별 정확도·실시간성·계산량을 비교하여 최적 알고리즘을 선택하세요.</div>
<table style="width:100%;border-collapse:collapse;font-size:0.8rem;margin-top:24px;">
<thead><tr style="background:#0D1B2A;color:#fff;">
<th style="padding:12px 14px;text-align:left;">방법</th>
<th style="padding:12px 14px;text-align:center;">정확도</th>
<th style="padding:12px 14px;text-align:center;">실시간성</th>
<th style="padding:12px 14px;text-align:center;">계산량</th>
<th style="padding:12px 14px;text-align:center;">노이즈 강인성</th>
<th style="padding:12px 14px;text-align:left;">주요 적용</th>
</tr></thead><tbody>
<tr style="border-bottom:1px solid #EEF0F3;"><td style="padding:11px 14px;color:#6B7280;">쿨롱 카운팅</td><td style="text-align:center;">⭐⭐</td><td style="text-align:center;">✅</td><td style="text-align:center;color:#00B4A0;font-weight:600;">낮음</td><td style="text-align:center;">❌</td><td style="padding:11px 14px;color:#6B7280;">간단한 BMS</td></tr>
<tr style="border-bottom:1px solid #EEF0F3;background:#F7F8FA;"><td style="padding:11px 14px;color:#6B7280;">OCV 기반</td><td style="text-align:center;">⭐⭐⭐</td><td style="text-align:center;">❌</td><td style="text-align:center;color:#00B4A0;font-weight:600;">낮음</td><td style="text-align:center;">✅</td><td style="padding:11px 14px;color:#6B7280;">초기화 시점</td></tr>
<tr style="border-bottom:1px solid #EEF0F3;"><td style="padding:11px 14px;color:#6B7280;">OLS / WLS / TLS</td><td style="text-align:center;">⭐⭐⭐</td><td style="text-align:center;">✅</td><td style="text-align:center;color:#00B4A0;font-weight:600;">낮음</td><td style="text-align:center;">보통</td><td style="padding:11px 14px;color:#6B7280;">용량 추정</td></tr>
<tr style="border-bottom:1px solid #EEF0F3;background:#F7F8FA;"><td style="padding:11px 14px;color:#6B7280;">EKF</td><td style="text-align:center;">⭐⭐⭐⭐</td><td style="text-align:center;">✅</td><td style="text-align:center;color:#F59E0B;font-weight:600;">보통</td><td style="text-align:center;">✅</td><td style="padding:11px 14px;color:#6B7280;">EV BMS</td></tr>
<tr style="border-bottom:1px solid #EEF0F3;background:#E6F7F5;"><td style="padding:11px 14px;color:#0D1B2A;font-weight:700;">SPKF / UKF ★</td><td style="text-align:center;">⭐⭐⭐⭐⭐</td><td style="text-align:center;">✅</td><td style="text-align:center;color:#F59E0B;font-weight:600;">보통</td><td style="text-align:center;color:#00B4A0;font-weight:700;">✅✅</td><td style="padding:11px 14px;color:#00B4A0;font-weight:700;">고성능 EV</td></tr>
<tr><td style="padding:11px 14px;color:#6B7280;">머신러닝</td><td style="text-align:center;">⭐⭐⭐⭐⭐</td><td style="text-align:center;">보통</td><td style="text-align:center;color:#EF4444;font-weight:600;">높음</td><td style="text-align:center;color:#00B4A0;font-weight:700;">✅✅</td><td style="padding:11px 14px;color:#6B7280;">클라우드 BMS</td></tr>
</tbody></table>
</div>

<div class="sec sec-w" id="s-p">
<div class="sec-lbl">Algorithm Performance</div>
<div class="sec-ttl">알고리즘 성능</div>
<div class="sec-dsc">Gregory Plett Chapter 2-04의 핵심 SOH 추정 알고리즘을 5가지 지표로 비교합니다.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:28px;"><div style="background:#fff;border:1px solid #E2E8F0;border-top:3px solid #94A3B8;border-radius:8px;padding:20px 22px;"><div style="font-size:0.9rem;font-weight:700;color:#0D1B2A;margin-bottom:12px;">칼만 필터 (KF)</div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">정확도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:72%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">72%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">실시간성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:95%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">95%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">노이즈 강인성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:80%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">80%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">계산 효율</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:92%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">92%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">수렴 속도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:85%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">85%</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-top:3px solid #F59E0B;border-radius:8px;padding:20px 22px;"><div style="font-size:0.9rem;font-weight:700;color:#0D1B2A;margin-bottom:12px;">확장 칼만 필터 (EKF)</div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">정확도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:84%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">84%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">실시간성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:88%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">88%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">노이즈 강인성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:85%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">85%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">계산 효율</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:80%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">80%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">수렴 속도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:82%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">82%</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-top:3px solid #00B4A0;border-radius:8px;padding:20px 22px;"><div style="font-size:0.9rem;font-weight:700;color:#0D1B2A;margin-bottom:12px;">SPKF / UKF</div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">정확도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:93%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">93%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">실시간성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:82%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">82%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">노이즈 강인성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:92%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">92%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">계산 효율</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:72%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">72%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">수렴 속도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:88%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">88%</div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-top:3px solid #3B82F6;border-radius:8px;padding:20px 22px;"><div style="font-size:0.9rem;font-weight:700;color:#0D1B2A;margin-bottom:12px;">머신러닝 기반</div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">정확도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:96%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">96%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">실시간성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:75%;height:6px;background:#F59E0B;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#F59E0B;min-width:28px;text-align:right;">75%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">노이즈 강인성</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:90%;height:6px;background:#00B4A0;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#00B4A0;min-width:28px;text-align:right;">90%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">계산 효율</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:55%;height:6px;background:#EF4444;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#EF4444;min-width:28px;text-align:right;">55%</div></div><div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #F1F5F9;"><div style="font-size:0.75rem;color:#334155;min-width:100px;">수렴 속도</div><div style="flex:1;background:#E2E8F0;border-radius:20px;height:6px;"><div style="width:70%;height:6px;background:#EF4444;border-radius:20px;"></div></div><div style="font-size:0.75rem;font-weight:700;color:#EF4444;min-width:28px;text-align:right;">70%</div></div></div></div>
</div>

<div class="sec sec-g" id="s-pr">
<div class="sec-lbl">Estimation Process</div>
<div class="sec-ttl">핵심 공정</div>
<div class="sec-dsc">센서 데이터 수집부터 검증까지 - SOH 추정의 5단계 공정을 탐색하세요.</div>
<div style="display:flex;gap:0;margin-top:32px;border:1px solid #E2E8F0;border-radius:8px;overflow:hidden;"><div style="flex:1;background:#fff;border:1px solid #E2E8F0;padding:28px 16px 24px;text-align:center;transition:all 0.2s;" onmouseover="this.style.borderColor='#00B4A0';this.style.boxShadow='0 4px 20px rgba(0,180,160,0.12)'" onmouseout="this.style.borderColor='#E2E8F0';this.style.boxShadow='none'"><div style="width:100%;height:160px;overflow:hidden;border-radius:6px;margin-bottom:16px;background:#F7F8FA;"><img src="data:image/png;base64,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" style="width:100%;height:160px;object-fit:contain;display:block;padding:8px;"></div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">센서 데이터 수집</div><div style="font-size:0.74rem;color:#9EA5AF;line-height:1.55;">전압·전류·온도를 고정밀 센서로 실시간 수집합니다.</div></div><div style="display:flex;align-items:center;justify-content:center;width:28px;flex-shrink:0;background:#F0F4F8;border-top:1px solid #E2E8F0;border-bottom:1px solid #E2E8F0;"><span style="color:#00B4A0;font-size:1.3rem;font-weight:700;">›</span></div><div style="flex:1;background:#fff;border:1px solid #E2E8F0;padding:28px 16px 24px;text-align:center;transition:all 0.2s;" onmouseover="this.style.borderColor='#00B4A0';this.style.boxShadow='0 4px 20px rgba(0,180,160,0.12)'" onmouseout="this.style.borderColor='#E2E8F0';this.style.boxShadow='none'"><div style="width:100%;height:160px;overflow:hidden;border-radius:6px;margin-bottom:16px;background:#F7F8FA;"><img src="data:image/png;base64,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" style="width:100%;height:160px;object-fit:contain;display:block;padding:8px;"></div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">등가 회로 모델링</div><div style="font-size:0.74rem;color:#9EA5AF;line-height:1.55;">배터리를 R₀·R₁C₁·OCV 등가 회로로 모델링합니다.</div></div><div style="display:flex;align-items:center;justify-content:center;width:28px;flex-shrink:0;background:#F0F4F8;border-top:1px solid #E2E8F0;border-bottom:1px solid #E2E8F0;"><span style="color:#00B4A0;font-size:1.3rem;font-weight:700;">›</span></div><div style="flex:1;background:#fff;border:1px solid #E2E8F0;padding:28px 16px 24px;text-align:center;transition:all 0.2s;" onmouseover="this.style.borderColor='#00B4A0';this.style.boxShadow='0 4px 20px rgba(0,180,160,0.12)'" onmouseout="this.style.borderColor='#E2E8F0';this.style.boxShadow='none'"><div style="width:100%;height:160px;overflow:hidden;border-radius:6px;margin-bottom:16px;background:#F7F8FA;"><img src="data:image/png;base64,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" style="width:100%;height:160px;object-fit:contain;display:block;padding:8px;"></div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">파라미터 식별</div><div style="font-size:0.74rem;color:#9EA5AF;line-height:1.55;">OLS·WLS·TLS 최소제곱법으로 모델 파라미터를 추정합니다.</div></div><div style="display:flex;align-items:center;justify-content:center;width:28px;flex-shrink:0;background:#F0F4F8;border-top:1px solid #E2E8F0;border-bottom:1px solid #E2E8F0;"><span style="color:#00B4A0;font-size:1.3rem;font-weight:700;">›</span></div><div style="flex:1;background:#fff;border:1px solid #E2E8F0;padding:28px 16px 24px;text-align:center;transition:all 0.2s;" onmouseover="this.style.borderColor='#00B4A0';this.style.boxShadow='0 4px 20px rgba(0,180,160,0.12)'" onmouseout="this.style.borderColor='#E2E8F0';this.style.boxShadow='none'"><div style="width:100%;height:160px;overflow:hidden;border-radius:6px;margin-bottom:16px;background:#F7F8FA;"><img src="data:image/png;base64,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" style="width:100%;height:160px;object-fit:contain;display:block;padding:8px;"></div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">상태 추정 (필터)</div><div style="font-size:0.74rem;color:#9EA5AF;line-height:1.55;">EKF·SPKF 칼만 필터로 SOC·SOH를 실시간 추정합니다.</div></div><div style="display:flex;align-items:center;justify-content:center;width:28px;flex-shrink:0;background:#F0F4F8;border-top:1px solid #E2E8F0;border-bottom:1px solid #E2E8F0;"><span style="color:#00B4A0;font-size:1.3rem;font-weight:700;">›</span></div><div style="flex:1;background:#fff;border:1px solid #E2E8F0;padding:28px 16px 24px;text-align:center;transition:all 0.2s;" onmouseover="this.style.borderColor='#00B4A0';this.style.boxShadow='0 4px 20px rgba(0,180,160,0.12)'" onmouseout="this.style.borderColor='#E2E8F0';this.style.boxShadow='none'"><div style="width:100%;height:160px;overflow:hidden;border-radius:6px;margin-bottom:16px;background:#F7F8FA;"><img src="data:image/png;base64,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" style="width:100%;height:160px;object-fit:contain;display:block;padding:8px;"></div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:6px;">검증 및 보정</div><div style="font-size:0.74rem;color:#9EA5AF;line-height:1.55;">RMSE·MAE로 정확도를 평가하고 모델을 지속 업데이트합니다.</div></div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:24px;"><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;border-top:3px solid #00B4A0;padding:22px 24px;"><div style="font-size:0.9rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">등가 회로 모델 (ECM)</div><div style="font-size:0.78rem;color:#6B7280;margin-bottom:12px;">배터리를 전기 회로로 단순화하여 실시간 BMS 계산을 가능하게 합니다.</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ R₀ : 순수 내부 저항 — 즉각 전압 강하</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ R₁C₁ : 전기화학 분극 — 시정수 τ = R₁C₁</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ OCV : 개방 회로 전압 — SOC의 비선형 함수</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ V = OCV - I·R₀ - V_RC</div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;border-top:3px solid #00B4A0;padding:22px 24px;"><div style="font-size:0.9rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">칼만 필터 추정 공정</div><div style="font-size:0.78rem;color:#6B7280;margin-bottom:12px;">예측(Predict)과 업데이트(Update) 두 단계를 반복하여 최적 추정합니다.</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ 예측: x̂⁻ = f(x̂, u) — 상태 전파</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ 예측: P⁻ = F·P·Fᵀ + Q — 오차 공분산</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ 업데이트: K = P⁻Hᵀ(HP⁻Hᵀ+R)⁻¹ — 칼만 이득</div><div style="font-size:0.75rem;color:#334155;padding:7px 0;border-bottom:1px solid #EEF0F3;font-family:monospace;">▸ 업데이트: x̂ = x̂⁻ + K(y - h(x̂⁻)) — 상태 보정</div></div></div>
</div>

<div class="sec sec-w" id="s-i">
<div class="sec-lbl">Innovation Technology</div>
<div class="sec-ttl">혁신 기술</div>
<div class="sec-dsc">AI·디지털 트윈·클라우드와 결합한 차세대 SOH 추정 기술을 탐색하세요.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:28px;"><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:20px;display:flex;gap:14px;"><div style="width:44px;height:44px;border-radius:10px;background:#E6F7F5;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🤖</div><div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">AI / 머신러닝 기반 SOH</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">딥러닝과 물리 기반 모델을 결합한 하이브리드 방식으로 정확도를 대폭 향상.</div><div><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">LSTM 시계열 예측</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">Physics-Informed NN</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">온라인 학습</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">이상 탐지</span></div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:20px;display:flex;gap:14px;"><div style="width:44px;height:44px;border-radius:10px;background:#E6F7F5;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🌐</div><div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">디지털 트윈</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">실제 배터리와 동기화된 가상 모델로 SOH 추정 정확도를 혁신적으로 확장.</div><div><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">실시간 물리 모델</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">가속 열화 시뮬</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">수명 예측 정밀화</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">가상 환경 테스트</span></div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:20px;display:flex;gap:14px;"><div style="width:44px;height:44px;border-radius:10px;background:#E6F7F5;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">☁️</div><div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">클라우드 BMS</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">차량 군집 빅데이터를 통합 분석하여 집단 지성형 SOH 모델을 개선.</div><div><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">OTA 모델 업데이트</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">Fleet 데이터 분석</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">엣지-클라우드 분산</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">개인화 보정</span></div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:20px;display:flex;gap:14px;"><div style="width:44px;height:44px;border-radius:10px;background:#E6F7F5;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">⚡</div><div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">전고체 배터리 대응</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">차세대 전고체 배터리의 새로운 열화 메커니즘에 특화된 SOH 추정.</div><div><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">계면 저항 추적</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">덴드라이트 감지</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">고온 내구성</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">새 ECM 파라미터</span></div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:20px;display:flex;gap:14px;"><div style="width:44px;height:44px;border-radius:10px;background:#E6F7F5;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">📡</div><div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">EIS 기반 진단</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">전기화학 임피던스 분광법으로 내부 상태를 비침습적으로 정밀 진단.</div><div><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">주파수 대역 분리</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">온라인 EIS 측정</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">SOH·SOP 동시 추정</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">열화 메커니즘 분석</span></div></div></div><div style="background:#fff;border:1px solid #E2E8F0;border-radius:8px;padding:20px;display:flex;gap:14px;"><div style="width:44px;height:44px;border-radius:10px;background:#E6F7F5;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;">🔗</div><div><div style="font-size:0.88rem;font-weight:700;color:#0D1B2A;margin-bottom:5px;">조인트·듀얼 추정 고도화</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;margin-bottom:8px;">SOC·SOH 동시 추정 필터를 고도화하여 파라미터 식별 정확도 극대화.</div><div><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">적응형 노이즈</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">다중 모델 전환</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">강인한 초기화</span><span style="background:#E6F7F5;color:#00796B;border-radius:20px;padding:2px 9px;font-size:0.68rem;font-weight:500;margin:2px 2px 0 0;display:inline-block;">실시간 업데이트</span></div></div></div></div>
</div>

<div class="sec sec-g" id="s-d">
<div class="sec-lbl">Industry Solutions</div>
<div class="sec-ttl">산업별 적용</div>
<div class="sec-dsc">배터리 건강 추정 기술은 전기차부터 항공까지 다양한 산업에 핵심 기술로 적용됩니다.</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:28px;"><div style="background:#E6F7F5;border:1px solid #E2E8F0;border-radius:14px;padding:26px;display:flex;justify-content:space-between;align-items:flex-end;min-height:160px;"><div><div style="font-size:1.05rem;font-weight:800;color:#0D1B2A;margin-bottom:7px;">승용 EV</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;max-width:190px;">주행거리 보장과 충전 최적화에 SOH 추정이 직접 활용됩니다.</div><div style="font-size:0.76rem;color:#9EA5AF;font-weight:600;margin-top:10px;">자세히 보기 →</div></div><div style="font-size:3.2rem;opacity:0.65;">🚗</div></div><div style="background:#EFF6FF;border:1px solid #E2E8F0;border-radius:14px;padding:26px;display:flex;justify-content:space-between;align-items:flex-end;min-height:160px;"><div><div style="font-size:1.05rem;font-weight:800;color:#0D1B2A;margin-bottom:7px;">상용 EV (트럭·버스)</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;max-width:190px;">대용량 배터리팩 SOH를 정밀 관리하여 안정적 운행을 보장합니다.</div><div style="font-size:0.76rem;color:#9EA5AF;font-weight:600;margin-top:10px;">자세히 보기 →</div></div><div style="font-size:3.2rem;opacity:0.65;">🚛</div></div><div style="background:#F0FDF4;border:1px solid #E2E8F0;border-radius:14px;padding:26px;display:flex;justify-content:space-between;align-items:flex-end;min-height:160px;"><div><div style="font-size:1.05rem;font-weight:800;color:#0D1B2A;margin-bottom:7px;">ESS (에너지 저장)</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;max-width:190px;">재생에너지 연계 ESS에서 SOH 기반 충방전으로 효율을 극대화합니다.</div><div style="font-size:0.76rem;color:#9EA5AF;font-weight:600;margin-top:10px;">자세히 보기 →</div></div><div style="font-size:3.2rem;opacity:0.65;">🏭</div></div><div style="background:#FFF7ED;border:1px solid #E2E8F0;border-radius:14px;padding:26px;display:flex;justify-content:space-between;align-items:flex-end;min-height:160px;"><div><div style="font-size:1.05rem;font-weight:800;color:#0D1B2A;margin-bottom:7px;">LEV (경량 모빌리티)</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;max-width:190px;">경량화된 SOH 알고리즘으로 전동 킥보드·자전거를 관리합니다.</div><div style="font-size:0.76rem;color:#9EA5AF;font-weight:600;margin-top:10px;">자세히 보기 →</div></div><div style="font-size:3.2rem;opacity:0.65;">🛵</div></div><div style="background:#FDF2F8;border:1px solid #E2E8F0;border-radius:14px;padding:26px;display:flex;justify-content:space-between;align-items:flex-end;min-height:160px;"><div><div style="font-size:1.05rem;font-weight:800;color:#0D1B2A;margin-bottom:7px;">로봇·중장비</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;max-width:190px;">극한 환경의 산업용 배터리를 안전하게 실시간 관리합니다.</div><div style="font-size:0.76rem;color:#9EA5AF;font-weight:600;margin-top:10px;">자세히 보기 →</div></div><div style="font-size:3.2rem;opacity:0.65;">🤖</div></div><div style="background:#F0F9FF;border:1px solid #E2E8F0;border-radius:14px;padding:26px;display:flex;justify-content:space-between;align-items:flex-end;min-height:160px;"><div><div style="font-size:1.05rem;font-weight:800;color:#0D1B2A;margin-bottom:7px;">항공·드론</div><div style="font-size:0.76rem;color:#6B7280;line-height:1.6;max-width:190px;">비행 중 실시간 SOH 추정으로 안전 귀환을 보장합니다.</div><div style="font-size:0.76rem;color:#9EA5AF;font-weight:600;margin-top:10px;">자세히 보기 →</div></div><div style="font-size:3.2rem;opacity:0.65;">✈️</div></div></div>
</div>

</div>
</div>
<script>
function go(id) {
  document.getElementById('s-' + id).scrollIntoView({behavior:'smooth', block:'start'});
}
(function() {
  var secs = [['c','s-c'],['p','s-p'],['pr','s-pr'],['i','s-i'],['d','s-d']];
  var body = document.getElementById('body');
  body.addEventListener('scroll', function() {
    var cur = secs[0][0];
    secs.forEach(function(s) {
      var el = document.getElementById(s[1]);
      if (el && el.getBoundingClientRect().top <= window.innerHeight * 0.45) cur = s[0];
    });
    secs.forEach(function(s) {
      var nav = document.getElementById('nav-' + s[0]);
      if (nav) nav.className = 'nav-a' + (s[0] === cur ? ' on' : '');
    });
  }, {passive:true});
})();
</script>
</body>
</html>
    """
    components.html(full_html, height=900, scrolling=True)

    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🔋 Battery<span>IQ</span></div>
        <div class="footer-copy">Battery Management Systems · Gregory Plett · Chapter 2-04</div>
    </div>
    """, unsafe_allow_html=True)
