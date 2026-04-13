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

# =====================================================================
# 전체 CSS
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');

:root {
    --black:   #000000;
    --dark:    #0a0a0a;
    --dark2:   #111111;
    --dark3:   #1a1a1a;
    --gray1:   #f5f5f5;
    --gray2:   #e8e8e8;
    --gray3:   #999999;
    --gray4:   #666666;
    --white:   #ffffff;
    --red:     #C8001E;
    --red2:    #e8001c;
    --blue:    #0057FF;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'Plus Jakarta Sans', -apple-system, sans-serif;
    background: var(--black);
    color: var(--white);
    scroll-behavior: smooth;
}

.stApp { background: var(--black) !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.stButton > button {
    background: transparent !important;
    color: var(--white) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
    letter-spacing: 0.5px;
}
.stButton > button:hover {
    background: var(--white) !important;
    color: var(--black) !important;
    border-color: var(--white) !important;
}
.stTabs [data-baseweb="tab-list"] { display:none !important; }
.stTabs [data-baseweb="tab-panel"] { padding:0 !important; background:transparent !important; border:none !important; }
textarea { background: #1a1a1a !important; color: var(--white) !important; border: 1px solid #333 !important; border-radius: 4px !important; }

/* ── 글로벌 네비게이션 ── */
.gnb {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 64px;
    background: rgba(0,0,0,0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 48px;
    z-index: 9999;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    transition: background 0.3s;
}
.gnb-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 1.15rem;
    color: var(--white);
    letter-spacing: -0.3px;
    text-decoration: none;
}
.gnb-logo-icon {
    width: 28px; height: 28px;
    background: var(--red);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
}
.gnb-menu {
    display: flex;
    gap: 36px;
    font-size: 0.82rem;
    font-weight: 500;
    color: rgba(255,255,255,0.7);
    list-style: none;
}
.gnb-menu li { cursor: pointer; transition: color 0.2s; letter-spacing: 0.3px; }
.gnb-menu li:hover { color: var(--white); }
.gnb-right {
    display: flex;
    align-items: center;
    gap: 20px;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.5);
}

/* ── HERO 섹션 ── */
.hero-section {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 700px;
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    background: var(--black);
}
.hero-video-wrap {
    position: absolute;
    inset: 0;
    overflow: hidden;
}
.hero-video-wrap iframe {
    width: 100%;
    height: 100%;
    pointer-events: none;
}
.hero-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to bottom,
        rgba(0,0,0,0.2) 0%,
        rgba(0,0,0,0.1) 40%,
        rgba(0,0,0,0.7) 80%,
        rgba(0,0,0,1) 100%
    );
}
.hero-content {
    position: relative;
    z-index: 2;
    padding: 0 72px 80px;
    max-width: 860px;
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.hero-eyebrow::before {
    content: '';
    display: block;
    width: 32px;
    height: 1px;
    background: var(--red);
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 800;
    color: var(--white);
    line-height: 1.1;
    letter-spacing: -1.5px;
    margin-bottom: 20px;
}
.hero-title span { color: var(--red); }
.hero-desc {
    font-size: 1rem;
    color: rgba(255,255,255,0.65);
    font-weight: 300;
    line-height: 1.7;
    margin-bottom: 36px;
    max-width: 560px;
}
.hero-cta {
    display: flex;
    gap: 14px;
    align-items: center;
}
.btn-primary {
    background: var(--red) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 14px 32px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    cursor: pointer;
    transition: background 0.2s;
    text-decoration: none;
    display: inline-block;
}
.btn-outline {
    background: transparent !important;
    color: var(--white) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 2px !important;
    padding: 13px 32px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    display: inline-block;
}
.hero-scroll {
    position: absolute;
    bottom: 30px;
    right: 48px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    z-index: 2;
}
.hero-scroll-line {
    width: 1px;
    height: 48px;
    background: linear-gradient(to bottom, rgba(255,255,255,0.4), transparent);
    animation: scrollPulse 2s ease-in-out infinite;
}
@keyframes scrollPulse {
    0%, 100% { opacity: 0.4; transform: scaleY(1); }
    50% { opacity: 1; transform: scaleY(0.7); }
}

/* ── SECTION 공통 ── */
.section {
    padding: 120px 72px;
}
.section-dark  { background: var(--black); }
.section-dark2 { background: var(--dark2); }
.section-dark3 { background: var(--dark3); }
.section-light { background: var(--gray1); color: var(--black); }

.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::before {
    content: '';
    display: block;
    width: 24px;
    height: 1px;
    background: var(--red);
}
.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -1px;
    margin-bottom: 20px;
}
.section-desc {
    font-size: 1rem;
    color: rgba(255,255,255,0.55);
    font-weight: 300;
    line-height: 1.8;
    max-width: 560px;
}
.section-desc.dark { color: rgba(0,0,0,0.55); }

/* ── WHY 섹션 ── */
.why-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    margin-top: 72px;
    align-items: center;
}
.why-img {
    border-radius: 4px;
    overflow: hidden;
    position: relative;
}
.why-img img {
    width: 100%;
    height: 480px;
    object-fit: cover;
    display: block;
    filter: brightness(0.85);
}
.why-img-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 50%;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
}
.why-points {
    display: flex;
    flex-direction: column;
    gap: 40px;
}
.why-point {
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 28px;
    display: flex;
    gap: 24px;
    align-items: flex-start;
    transition: all 0.2s;
}
.why-point:hover { border-top-color: var(--red); }
.why-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--red);
    opacity: 0.6;
    line-height: 1;
    min-width: 40px;
}
.why-point-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--white);
    margin-bottom: 8px;
    letter-spacing: -0.2px;
}
.why-point-desc {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.5);
    line-height: 1.7;
    font-weight: 300;
}

/* ── STATS 배너 ── */
.stats-banner {
    background: var(--red);
    padding: 60px 72px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 40px;
}
.stat-item { text-align: center; }
.stat-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    color: var(--white);
    letter-spacing: -2px;
    line-height: 1;
    margin-bottom: 8px;
}
.stat-num span { font-size: 1.8rem; }
.stat-label {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.75);
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* ── TECH 섹션 — LG 에너지솔루션 스타일 ── */
.tech-intro {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    margin-bottom: 72px;
    align-items: end;
}
/* 분할 패널 그리드 */
.tech-panels {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
}
.tech-panel {
    position: relative;
    height: 480px;
    overflow: hidden;
    display: flex;
    align-items: flex-end;
}
.tech-panel-img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
    filter: brightness(0.55);
}
.tech-panel:hover .tech-panel-img { transform: scale(1.04); filter: brightness(0.65); }
.tech-panel-bg {
    position: absolute;
    inset: 0;
}
.tech-panel-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to top,
        rgba(0,0,0,0.85) 0%,
        rgba(0,0,0,0.3) 50%,
        rgba(0,0,0,0.05) 100%
    );
}
.tech-panel-content {
    position: relative;
    z-index: 2;
    padding: 36px 40px;
    width: 100%;
}
.tech-panel-num {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 10px;
}
.tech-panel-num span { color: var(--red); }
.tech-panel-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1.2;
    letter-spacing: -0.5px;
    margin-bottom: 10px;
}
.tech-panel-subtitle {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.55);
    font-weight: 400;
    margin-bottom: 14px;
}
.tech-panel-desc {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.45);
    line-height: 1.7;
    font-weight: 300;
    display: none;
    max-width: 380px;
}
.tech-panel:hover .tech-panel-desc { display: block; }
.tech-panel:hover .tech-panel-subtitle { display: none; }
.tech-panel-arrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    color: rgba(255,255,255,0.4);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 16px;
    transition: color 0.2s;
}
.tech-panel:hover .tech-panel-arrow { color: var(--white); }
.tech-panel-line {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--red);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}
.tech-panel:hover .tech-panel-line { transform: scaleX(1); }

/* ── NEWS 섹션 ── */
.news-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 48px;
}
.news-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 1px;
    background: rgba(255,255,255,0.06);
}
.news-card {
    background: var(--dark2);
    overflow: hidden;
    transition: background 0.2s;
    cursor: pointer;
}
.news-card:hover { background: var(--dark3); }
.news-card-img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    display: block;
    filter: brightness(0.7);
    transition: filter 0.3s, transform 0.4s;
}
.news-card:hover .news-card-img {
    filter: brightness(0.85);
    transform: scale(1.02);
}
.news-card-img-wrap { overflow: hidden; }
.news-card.featured .news-card-img { height: 320px; }
.news-card-body { padding: 24px 28px 28px; }
.news-card-tag {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.news-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--white);
    line-height: 1.45;
    margin-bottom: 10px;
    letter-spacing: -0.2px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.news-card.featured .news-card-title { font-size: 1.2rem; -webkit-line-clamp: 4; }
.news-card-title a { color: var(--white); text-decoration: none; }
.news-card-title a:hover { color: rgba(255,255,255,0.7); }
.news-card-meta {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.35);
    font-weight: 400;
}

/* ── TOPIC EXPLORER ── */
.explorer-section { background: var(--dark2); padding: 100px 72px; }
.topic-list {
    margin-top: 56px;
    display: flex;
    flex-direction: column;
    gap: 0;
}
.topic-row {
    display: flex;
    align-items: center;
    gap: 32px;
    padding: 22px 0;
    border-top: 1px solid rgba(255,255,255,0.07);
    cursor: pointer;
    transition: all 0.2s;
    text-decoration: none;
    color: var(--white);
}
.topic-row:last-child { border-bottom: 1px solid rgba(255,255,255,0.07); }
.topic-row:hover { padding-left: 12px; }
.topic-row:hover .topic-row-arrow { opacity: 1; transform: translateX(0); }
.topic-row:hover .topic-row-title { color: var(--red); }
.topic-row-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    color: rgba(255,255,255,0.25);
    min-width: 32px;
    letter-spacing: 1px;
}
.topic-row-title {
    font-size: 1rem;
    font-weight: 600;
    flex: 1;
    transition: color 0.2s;
    letter-spacing: -0.2px;
}
.topic-row-en {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.3);
    font-weight: 300;
    min-width: 300px;
    text-align: right;
}
.topic-row-arrow {
    color: var(--red);
    font-size: 1.1rem;
    opacity: 0;
    transform: translateX(-8px);
    transition: all 0.2s;
}

/* ── 상세 페이지 ── */
.detail-hero {
    padding: 140px 72px 80px;
    background: var(--black);
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.detail-breadcrumb {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.3);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.detail-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 800;
    color: var(--white);
    letter-spacing: -1px;
    line-height: 1.15;
    margin-bottom: 12px;
}
.detail-en {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.3);
    font-weight: 300;
    margin-bottom: 24px;
}
.detail-kws {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.detail-kw {
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.6);
    border-radius: 2px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* 디테일 탭 */
.dtab-wrap {
    background: var(--dark2);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    padding: 0 72px;
    overflow-x: auto;
}
.dtab {
    padding: 16px 24px;
    font-size: 0.82rem;
    font-weight: 500;
    color: rgba(255,255,255,0.4);
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
    letter-spacing: 0.3px;
}
.dtab.active { color: var(--white); border-bottom-color: var(--red); }
.dtab:hover  { color: var(--white); }

/* 뉴스 리스트 */
.nitem {
    padding: 24px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    display: flex;
    gap: 20px;
    align-items: flex-start;
}
.nitem:hover .nitem-title { color: var(--red); }
.nidx {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: rgba(255,255,255,0.1);
    min-width: 28px;
    line-height: 1;
    padding-top: 3px;
}
.nflag { font-size: 0.72rem; color: rgba(255,255,255,0.3); margin-bottom: 4px; }
.nitem-title { font-size: 0.92rem; font-weight: 600; color: var(--white); line-height: 1.45; margin-bottom: 5px; transition: color 0.2s; }
.nitem-title a { color: inherit; text-decoration: none; }
.nmeta { font-size: 0.72rem; color: rgba(255,255,255,0.3); }

/* 논문 아이템 */
.pitem {
    padding: 24px 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.pbadge {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 3px 8px;
    border-radius: 2px;
    margin-bottom: 8px;
}
.pbadge-a { background: rgba(200,0,30,0.2); color: #ff6b6b; border: 1px solid rgba(200,0,30,0.3); }
.pbadge-s { background: rgba(0,87,255,0.2); color: #7eb8ff; border: 1px solid rgba(0,87,255,0.3); }
.ptitle { font-size: 0.88rem; font-weight: 600; color: rgba(255,255,255,0.9); line-height: 1.45; margin-bottom: 5px; }
.ptitle a { color: inherit; text-decoration: none; }
.ptitle a:hover { color: var(--red); }
.pauth  { font-size: 0.74rem; color: rgba(255,255,255,0.35); margin-bottom: 6px; }
.pabs   { font-size: 0.78rem; color: rgba(255,255,255,0.4); line-height: 1.65; }

/* 선택 박스 */
.selbox {
    background: rgba(200,0,30,0.08);
    border: 1px solid rgba(200,0,30,0.2);
    border-left: 2px solid var(--red);
    padding: 10px 16px;
    font-size: 0.82rem;
    color: rgba(255,255,255,0.7);
    margin-bottom: 16px;
    border-radius: 0 2px 2px 0;
}

/* 액션 버튼 */
.abtn {
    background: var(--red) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: background 0.2s !important;
}
.abtn:hover { background: #a0001a !important; }

/* 보고서 */
.report-out {
    background: var(--dark2);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 2px;
    padding: 40px 44px;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.8);
    line-height: 1.9;
}
.report-out h1, .report-out h2, .report-out h3 {
    color: var(--white);
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.report-out h2 {
    border-left: 2px solid var(--red);
    padding-left: 12px;
    margin: 28px 0 12px;
    font-size: 0.98rem;
}

/* 푸터 */
.footer {
    background: var(--dark2);
    border-top: 1px solid rgba(255,255,255,0.07);
    padding: 48px 72px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.footer-logo {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 1rem;
    color: rgba(255,255,255,0.5);
}
.footer-copy {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.25);
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 주제 데이터
# =====================================================================
TOPICS = [
    ("01","배터리 건강 추정의 필요성","Battery State of Health Estimation",
     "배터리 SOH는 전기차·에너지 저장 시스템의 안전성과 성능 관리에 핵심적이다.",
     ["SOH","배터리 열화","RUL","EV","BMS"]),
    ("02","음극 노화","Lithium-ion Battery Anode Aging",
     "리튬 도금, SEI 성장, 구조적 균열 등으로 발생하는 음극 열화 메커니즘.",
     ["SEI","리튬 도금","흑연 음극","용량 손실","사이클 열화"]),
    ("03","양극 노화","Lithium-ion Battery Cathode Aging",
     "NMC·LFP 등 양극 소재별 열화 메커니즘과 성능 저하 원인 분석.",
     ["NMC/LFP","구조 열화","전이금속 용해","상변이","캘린더 노화"]),
    ("04","R₀에 대한 전압 감도","Battery Internal Resistance Voltage Sensitivity",
     "내부 저항 R₀와 SOH의 상관관계 및 전압 감도 분석 방법론.",
     ["내부 저항","전압 강하","등가 회로","임피던스","열화 진단"]),
    ("05","R₀를 추정하기 위한 코드","Battery Internal Resistance Estimation Algorithm",
     "전류 펄스, EIS, 최소제곱법 기반 실시간 R₀ 추정 알고리즘.",
     ["최소제곱법","EIS","전류 펄스","실시간 추정","Python"]),
    ("06","전체 용량에 대한 전압의 민감도 Q","Battery Voltage Sensitivity Total Capacity",
     "OCV-SOC 곡선 기반 전체 용량 Q 추정 방법 및 민감도 분석.",
     ["용량 Q","OCV-SOC","활물질 손실","쿨롱 카운팅","용량 추정"]),
    ("07","칼만 필터를 통한 파라미터 추정","Kalman Filter Battery Parameter Estimation",
     "노이즈 환경에서 배터리 상태변수를 최적 추정하는 재귀 알고리즘.",
     ["칼만 필터","상태 추정","공분산","예측-수정","재귀 알고리즘"]),
    ("08","EKF 파라미터 추정","Extended Kalman Filter Battery SOH",
     "야코비안 선형화로 비선형 배터리 모델에 칼만 필터를 적용하는 방법.",
     ["EKF","야코비안","비선형 시스템","SOC 추정","선형화"]),
    ("09","SPKF 파라미터 추정","Sigma-Point Kalman Filter Battery",
     "시그마 포인트 통계 전파로 EKF보다 높은 정확도를 달성하는 필터.",
     ["SPKF/UKF","시그마 포인트","무향 변환","비선형 추정","통계 근사"]),
    ("10","조인트 추정과 듀얼 추정","Joint Dual Estimation Battery State",
     "상태변수와 파라미터를 단일 또는 이중 필터로 동시 추정하는 기법.",
     ["조인트 추정","듀얼 추정","이중 필터","적응형 추정","동시 추정"]),
    ("11","견고성과 속도","Robustness Speed Battery Estimation",
     "노이즈·불확실성에 강인하면서 실시간 BMS에 적합한 알고리즘 설계.",
     ["견고성","계산 복잡도","실시간 처리","노이즈 민감도","수렴 속도"]),
    ("12","선형 회귀를 통한 전체 용량의 비편향 추정값","Unbiased Battery Capacity Linear Regression",
     "측정 데이터 기반 선형 회귀로 배터리 전체 용량을 편향 없이 추정.",
     ["비편향 추정","선형 회귀","쿨롱 카운팅","OLS","용량 추정"]),
    ("13","가중 일반 최소제곱법","Weighted Generalized Least Squares Battery",
     "불균일 노이즈 분산 환경에서 가중치 부여로 추정 정확도를 향상.",
     ["WGLS","이분산성","가중 행렬","최적 추정","노이즈 모델링"]),
    ("14","총 가중 최소제곱법","Weighted Total Least Squares Battery",
     "입출력 양방향 노이즈를 고려한 EIV 모델 기반 용량 추정 기법.",
     ["TWLS","EIV","양방향 노이즈","총 최소제곱","용량 추정"]),
    ("15","모델 적합도의 우수성","Goodness of Fit Battery Equivalent Circuit",
     "RMSE·R²·AIC 기반 등가 회로 모델 적합도 평가 및 최적 모델 선택.",
     ["RMSE","R²","AIC/BIC","등가 회로 모델","모델 검증"]),
    ("16","신뢰 구간","Confidence Interval Battery Estimation",
     "추정 불확실성을 정량화하여 배터리 안전 마진을 설정하는 방법.",
     ["신뢰 구간","불확실성","공분산","오차 한계","통계 추론"]),
    ("17","단순화된 총 최소제곱","Simplified Total Least Squares Battery",
     "계산 복잡도를 줄이면서 EIV 모델의 장점을 유지하는 경량 알고리즘.",
     ["단순화 TLS","근사 알고리즘","계산 효율","실시간 BMS","EIV"]),
    ("18","근사 전체 솔루션","Approximate Total Solution Battery",
     "닫힌 형태 근사로 복잡한 최적화 문제의 계산 효율을 높이는 방법.",
     ["근사 해","계산 최적화","파라미터 추정","수치 안정성","실시간 구현"]),
    ("19","방법별 시뮬레이션 코드","Battery SOH Estimation Simulation Code",
     "Python·MATLAB 기반 EKF·SPKF·OLS 알고리즘 성능 비교 시뮬레이션.",
     ["시뮬레이션","Python/MATLAB","알고리즘 비교","성능 평가","데이터셋"]),
    ("20","HEV 시뮬레이션 예시","Hybrid Electric Vehicle Battery Simulation",
     "UDDS·HWFET 주행 사이클 적용 HEV 배터리 SOH 추정 시뮬레이션.",
     ["HEV","주행 사이클","UDDS/HWFET","동적 부하","SOH 추정"]),
    ("21","EV 시뮬레이션 예시","Electric Vehicle EV Battery Simulation",
     "WLTP·EPA 표준 사이클 기반 EV 배터리 에너지 관리 및 SOH 분석.",
     ["EV","주행거리","WLTP/EPA","에너지 관리","충전 전략"]),
    ("22","시뮬레이션에 대한 논의","Battery Simulation Discussion Results",
     "다양한 추정 방법의 시뮬레이션 결과 비교 및 실차 적용 고려사항.",
     ["결과 비교","실차 적용","온도 영향","센서 오차","검증"]),
    ("23","결론 및 향후 방향","Battery Health Estimation Future Research",
     "머신러닝·디지털 트윈·클라우드 BMS 등 미래 SOH 추정 연구 방향.",
     ["머신러닝 SOH","디지털 트윈","차세대 배터리","클라우드 BMS","연구 과제"]),
    ("24","비선형 칼만 필터 알고리즘","Nonlinear Kalman Filter Algorithm Battery",
     "EKF·UKF·CKF·파티클 필터의 이론과 배터리 SOH 추정 적용 비교.",
     ["비선형 칼만","UKF/CKF","파티클 필터","비선형 추정","알고리즘 비교"]),
]

# 주요 기술 6개 (TECH 섹션용) — (num, title, subtitle, desc, 배경색, 이미지URL)
TECH_HIGHLIGHTS = [
    (
        "01", "배터리 건강 추정의 필요성",
        "안전한 배터리 운용의 시작",
        "SOH(State of Health) 추정은 배터리의 현재 용량을 초기 정격 용량 대비 비율로 나타냅니다. 과충전·과방전 방지, 잔여 수명 예측, 교체 시점 결정에 필수적인 기술입니다.",
        "linear-gradient(135deg, #005C4B 0%, #007A5E 100%)",
        "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=900&h=600&fit=crop&auto=format"
    ),
    (
        "07", "칼만 필터 파라미터 추정",
        "노이즈 속에서도 정확한 추정",
        "칼만 필터는 센서 노이즈가 있는 환경에서 배터리 SOC·SOH를 최적으로 추정하는 재귀 알고리즘입니다. 예측(Predict)과 업데이트(Update) 두 단계를 반복하며 실시간 추정을 수행합니다.",
        "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=900&h=600&fit=crop&auto=format"
    ),
    (
        "08", "EKF 파라미터 추정",
        "비선형 모델을 위한 확장 칼만 필터",
        "배터리의 OCV-SOC 특성은 비선형입니다. EKF는 야코비안(Jacobian) 행렬로 비선형 함수를 순간적으로 선형화하여 칼만 필터를 적용합니다. SOC·내부 저항의 동시 추정이 가능합니다.",
        "linear-gradient(135deg, #0f2027 0%, #203a43 100%)",
        "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=900&h=600&fit=crop&auto=format"
    ),
    (
        "09", "SPKF 파라미터 추정",
        "시그마 포인트로 더 높은 정확도",
        "SPKF(Sigma-Point Kalman Filter)는 UKF라고도 불리며, 비선형 변환을 시그마 포인트의 통계적 전파로 근사합니다. 야코비안 계산 없이 EKF보다 높은 추정 정확도를 달성합니다.",
        "linear-gradient(135deg, #200122 0%, #6f0000 100%)",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=900&h=600&fit=crop&auto=format"
    ),
    (
        "10", "조인트·듀얼 추정",
        "SOC와 SOH를 동시에 추정",
        "조인트 추정(Joint Estimation)은 SOC와 SOH를 단일 확장 상태 벡터로 묶어 하나의 필터로 추정합니다. 듀얼 추정(Dual Estimation)은 두 개의 분리된 필터를 병렬로 운용합니다.",
        "linear-gradient(135deg, #134E5E 0%, #71B280 100%)",
        "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=900&h=600&fit=crop&auto=format"
    ),
    (
        "20", "HEV·EV 시뮬레이션",
        "실제 주행 환경에서의 검증",
        "HEV는 UDDS·HWFET, EV는 WLTP·EPA 표준 주행 사이클을 적용하여 실제 차량 운행 환경을 재현합니다. 시뮬레이션을 통해 각 추정 알고리즘의 실차 적용 성능을 비교·검증합니다.",
        "linear-gradient(135deg, #0f3460 0%, #16213e 100%)",
        "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=900&h=600&fit=crop&auto=format"
    ),
]

# 뉴스 이미지 (주제별)
NEWS_IMGS = [
    "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=400&fit=crop",
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
        results = []
        for e in feed.entries:
            title   = e.get("title","").replace("\n"," ").strip()
            summary = e.get("summary","")[:400].replace("\n"," ").strip()
            pub     = e.get("published","")[:10]
            link    = e.get("id","") or e.get("link","")
            ar      = e.get("authors",[])
            authors = ", ".join(a.get("name","") for a in ar[:3]) if ar else e.get("author","")
            if title:
                results.append({"title":title,"authors":authors,"abstract":summary,"url":link,"published":pub})
        return results
    except: return []

def fetch_scholar(keyword, n=4):
    results = []
    try:
        gen = scholarly.search_pubs(keyword)
        for _ in range(n):
            try:
                pub = next(gen); bib = pub.get("bib",{})
                results.append({"title":bib.get("title","No title"),"authors":bib.get("author","Unknown"),
                                "year":bib.get("pub_year",""),"journal":bib.get("venue",""),
                                "abstract":bib.get("abstract",""),"url":pub.get("pub_url","")})
            except StopIteration: break
    except: pass
    return results

def build_report(num,ko,en,bg,kw,news_ko,news_en,papers,arxiv):
    today = datetime.now().strftime("%Y-%m-%d")
    kw_str = " / ".join(kw)
    n_news=len(news_ko)+len(news_en); n_p=len(papers)+len(arxiv)
    ref_num=1; refs=[]
    for p in papers:
        r=f"[{ref_num}] {p['authors']} ({p['year']}). {p['title']}."
        if p.get('journal'): r+=f" {p['journal']}."
        if p.get('url'):     r+=f" {p['url']}"
        refs.append(r); ref_num+=1
    for p in arxiv:
        refs.append(f"[{ref_num}] {p['authors']} ({p['published'][:4]}). {p['title']}. arXiv. {p['url']}")
        ref_num+=1
    for n in news_ko+news_en:
        refs.append(f"[{ref_num}] {n['title']}. {n['source']} ({n['published']}). {n['link']}")
        ref_num+=1
    sb="".join([f"\n**[{i}] {p['title']}** ({p['year']}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(papers,1)]) or "(없음)"
    ab="".join([f"\n**[{i}] [{p['title']}]({p['url']})** ({p['published'][:7]}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(arxiv,len(papers)+1)]) or "(없음)"
    return f"""# {num}. {ko}\n## 연구 분석 보고서 — BatteryIQ\n\n**작성일:** {today} | **키워드:** {kw_str}\n**기준 문헌:** Gregory Plett - *Battery Management Systems*\n**수집 자료:** 뉴스 {n_news}건 · 논문 {n_p}편\n\n---\n\n## 초록\n\n{ko}은(는) 배터리 건강 상태(SOH) 추정의 핵심 주제이다. {bg} 본 보고서는 뉴스 {n_news}건, 논문 {n_p}편을 분석하여 현황과 연구 동향을 정리한다.\n\n**키워드:** {kw_str}\n\n---\n\n## 1. 서론\n\n### 1.1 연구 배경\n{bg}\n\n### 1.2 연구 목적\n{ko}({en})에 관한 최신 연구 동향과 기술 현황을 체계적으로 분석한다.\n\n---\n\n## 2. 이론적 배경\n\n{bg}\n\n| 핵심 개념 | 설명 |\n|----------|------|\n{"".join([f"| **{k}** | {ko} 분야 핵심 요소 |\n" for k in kw])}\n\n---\n\n## 3. 최신 기술 동향\n\n### 3.1 국내 동향\n{"".join([f"**[뉴스]** [{n['title']}]({n['link']})\n> {n['source']} | {n['published']}\n\n" for n in news_ko]) or "(없음)"}\n\n### 3.2 해외 동향\n{"".join([f"**[News]** [{n['title']}]({n['link']})\n> {n['source']} | {n['published']}\n\n" for n in news_en]) or "(없음)"}\n\n---\n\n## 4. 핵심 선행 연구 검토\n\n### 4.1 Google Scholar\n{sb}\n\n### 4.2 arXiv 최신 연구\n{ab}\n\n---\n\n## 5. 기술적 분석\n\n| 구분 | 주요 방법 | 특징 | 적용 분야 |\n|------|----------|------|----------|\n| 모델 기반 | 등가 회로 모델 | 구현 용이, 실시간 | BMS 내장 |\n| 필터 기반 | EKF / UKF | 높은 정확도 | 전기차 |\n| 데이터 기반 | 머신러닝 / DL | 대용량 데이터 | 클라우드 BMS |\n\n---\n\n## 6. 결론 및 향후 연구 방향\n\n- {ko}은(는) BMS 핵심 기능으로 연구 수요 지속 증가\n- 칼만 필터 계열 + 데이터 기반 융합 연구 트렌드\n- AI/ML 융합, 디지털 트윈, 차세대 배터리 적용이 향후 과제\n\n---\n\n## 참고문헌\n\n{"".join([f"{r}  \n" for r in refs]) or "(없음)"}\n\n---\n*BatteryIQ 연구 포털 | Gregory Plett, Battery Management Systems Vol.2 (2015)*"""

# =====================================================================
# 세션 초기화
# =====================================================================
for k,v in [("page","home"),("sel_idx",0),
            ("news_ko",[]),("news_en",[]),("papers",[]),("arxiv",[]),
            ("sel_news",[]),("sel_papers",[]),("sel_arxiv",[]),
            ("report",""),("tab","news"),("step",0)]:
    if k not in st.session_state: st.session_state[k]=v

# =====================================================================
# 네비게이션 (항상 표시)
# =====================================================================
st.markdown("""
<div class="gnb">
    <div class="gnb-logo">
        <div class="gnb-logo-icon">🔋</div>
        BatteryIQ
    </div>
    <ul class="gnb-menu">
        <li>연구 개요</li>
        <li>핵심 기술</li>
        <li>최신 뉴스</li>
        <li>24개 주제</li>
    </ul>
    <div class="gnb-right">
        <span>Gregory Plett · Chapter 2-04</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# HOME 페이지
# =====================================================================
if st.session_state["page"] == "home":

    # ── HERO (GitHub 호스팅 영상) ──
    st.markdown("""
    <div class="hero-section" style="background:#000;">
        <div class="hero-video-wrap">
            <video
                autoplay muted loop playsinline
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

    # ── WHY 섹션 ──
    st.markdown("""
    <div class="section section-dark">
        <div class="section-label">왜 배터리 건강 추정인가</div>
        <div class="why-grid">
            <div class="why-img">
                <img src="https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=900&h=600&fit=crop" alt="Battery">
                <div class="why-img-overlay"></div>
            </div>
            <div class="why-points">
                <div style="margin-bottom:36px;">
                    <div class="section-title">배터리 수명과<br>안전을 결정하는<br>핵심 기술</div>
                    <div class="section-desc">배터리 건강 상태(SOH) 추정은 전기차 주행거리 예측부터<br>에너지 저장 시스템의 안전 운용까지 전 분야에 영향을 미칩니다.</div>
                </div>
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
    """, unsafe_allow_html=True)

    # ── STATS 배너 ──
    st.markdown("""
    <div class="stats-banner">
        <div class="stat-item">
            <div class="stat-num">24<span>개</span></div>
            <div class="stat-label">핵심 연구 주제</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">6<span>종</span></div>
            <div class="stat-label">추정 알고리즘</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">2<span>개</span></div>
            <div class="stat-label">논문 데이터베이스</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">∞</div>
            <div class="stat-label">최신 뉴스 수집</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 주요 기술 섹션 (클릭 가능한 LG 스타일 패널) ──
    st.markdown("""
    <div class="section section-dark2" style="padding-bottom:0;">
        <div class="tech-intro">
            <div>
                <div class="section-label">주요 기술</div>
                <div class="section-title">배터리 건강 추정에<br>필요한 핵심 기술</div>
            </div>
            <div>
                <div class="section-desc">칼만 필터부터 EV 시뮬레이션까지 — 6가지 핵심 기술을 탐색하세요.<br>패널을 클릭하면 관련 뉴스와 논문을 바로 확인할 수 있습니다.</div>
            </div>
        </div>
    </div>
    <style>
    /* 패널 위 버튼 완전 투명 오버레이 */
    .panel-btn-wrap { position: relative; }
    .panel-btn-wrap .stButton { position: absolute; inset: 0; z-index: 10; }
    .panel-btn-wrap .stButton > button {
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        border-radius: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 패널 인덱스 → TOPICS 리스트 인덱스 매핑
    TECH_TOPIC_IDX = {
        "01": 0,  "07": 6,  "08": 7,
        "09": 8,  "10": 9,  "20": 19,
    }

    # 2열씩 나눠서 패널 렌더링
    panels_per_row = 2
    panel_list = list(TECH_HIGHLIGHTS)

    for row_start in range(0, len(panel_list), panels_per_row):
        row = panel_list[row_start:row_start + panels_per_row]
        cols = st.columns(panels_per_row)
        for col, (num, title, subtitle, desc, bg_grad, img_url) in zip(cols, row):
            with col:
                # 패널 HTML
                st.markdown(f"""
                <div class="tech-panel" style="width:100%;cursor:pointer;">
                    <div class="tech-panel-line"></div>
                    <img class="tech-panel-img" src="{img_url}" alt="{title}">
                    <div class="tech-panel-overlay"></div>
                    <div class="tech-panel-content">
                        <div class="tech-panel-num">TOPIC <span>{num}</span></div>
                        <div class="tech-panel-title">{title}</div>
                        <div class="tech-panel-subtitle">{subtitle}</div>
                        <div class="tech-panel-desc">{desc}</div>
                        <div class="tech-panel-arrow">자세히 보기 →</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # 투명 클릭 버튼
                if st.button(f"열기_{num}", key=f"tech_panel_{num}", use_container_width=True):
                    tidx = TECH_TOPIC_IDX.get(num, 0)
                    st.session_state["page"] = "detail"
                    st.session_state["sel_idx"] = tidx
                    st.session_state["tab"] = "news"
                    st.session_state["step"] = 0
                    for k2 in ["news_ko","news_en","papers","arxiv","sel_news","sel_papers","sel_arxiv","report"]:
                        st.session_state[k2] = [] if k2 != "report" else ""
                    # 뉴스 자동 수집 트리거
                    st.session_state["auto_fetch_news"] = True
                    st.rerun()

    st.markdown("<div style='height:1px;'></div>", unsafe_allow_html=True)

    # ── 최신 뉴스 섹션 (자동 수집 + LG 뉴스룸 스타일) ──

    # 최초 진입 시 자동 수집
    if not st.session_state.get("home_news_ko") and not st.session_state.get("home_news_en"):
        with st.spinner("최신 뉴스를 불러오는 중..."):
            raw_ko = fetch_news("배터리 건강 추정 SOH BMS","ko","KR","KR:ko", 4)
            st.session_state["home_news_ko"] = [
                {"title":e.title,"link":e.link,"published":getattr(e,'published',''),
                 "source":(e.get('source') or {}).get('title','Google News')}
                for e in raw_ko
            ]
            raw_en = fetch_news("Battery State of Health Estimation","en","US","US:en", 4)
            st.session_state["home_news_en"] = [
                {"title":e.title,"link":e.link,"published":getattr(e,'published',''),
                 "source":(e.get('source') or {}).get('title','Google News')}
                for e in raw_en
            ]

    home_ko = st.session_state.get("home_news_ko", [])
    home_en = st.session_state.get("home_news_en", [])
    all_home = home_ko + home_en

    # 뉴스룸 섹션 헤더
    st.markdown("""
    <div class="section section-dark" style="padding-bottom:60px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:48px;">
            <div>
                <div class="section-label">최신 뉴스</div>
                <div class="section-title" style="font-size:2.2rem;">뉴스룸</div>
            </div>
            <div style="font-size:0.8rem;color:rgba(255,255,255,0.35);letter-spacing:0.5px;">
                배터리 SOH 관련 최신 뉴스
            </div>
        </div>
    """, unsafe_allow_html=True)

    # LG 스타일 4열 뉴스 카드
    TOPIC_IMGS_NEWS = [
        "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=360&fit=crop",
        "https://images.unsplash.com/photo-1543286386-713bdd548da4?w=600&h=360&fit=crop",
    ]

    if all_home:
        # 상단 대형 피처드 카드 + 우측 서브카드
        feat = all_home[0]
        feat_flag = "🇰🇷" if feat in home_ko else "🌍"
        feat_date = feat['published'][:10] if feat['published'] else ""

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1.4fr 1fr;gap:1px;background:rgba(255,255,255,0.05);margin-bottom:1px;">
            <!-- 피처드 카드 -->
            <div style="background:#0a0a0a;overflow:hidden;position:relative;">
                <div style="overflow:hidden;height:320px;">
                    <img src="{TOPIC_IMGS_NEWS[0]}"
                         style="width:100%;height:320px;object-fit:cover;filter:brightness(0.5);
                                transition:transform 0.4s ease;"
                         onmouseover="this.style.transform='scale(1.03)'"
                         onmouseout="this.style.transform='scale(1)'">
                </div>
                <div style="padding:24px 28px 28px;">
                    <div style="font-size:0.68rem;color:#C8001E;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;">
                        {feat_flag} · {feat_date}
                    </div>
                    <div style="font-size:1.05rem;font-weight:700;color:#fff;line-height:1.5;margin-bottom:14px;letter-spacing:-0.2px;">
                        <a href="{feat['link']}" target="_blank"
                           style="color:#fff;text-decoration:none;"
                           onmouseover="this.style.color='#C8001E'"
                           onmouseout="this.style.color='#fff'">{feat['title']}</a>
                    </div>
                    <div style="font-size:0.72rem;color:rgba(255,255,255,0.35);">{feat['source']}</div>
                </div>
            </div>
            <!-- 우측 서브 카드 -->
            <div style="display:flex;flex-direction:column;gap:1px;">
        """, unsafe_allow_html=True)

        for i, item in enumerate(all_home[1:3]):
            flag = "🇰🇷" if item in home_ko else "🌍"
            date = item['published'][:10] if item['published'] else ""
            img = TOPIC_IMGS_NEWS[i+1]
            st.markdown(f"""
            <div style="background:#0a0a0a;display:flex;gap:0;flex:1;overflow:hidden;">
                <div style="overflow:hidden;width:160px;flex-shrink:0;">
                    <img src="{img}" style="width:160px;height:100%;object-fit:cover;filter:brightness(0.55);min-height:120px;">
                </div>
                <div style="padding:18px 20px;flex:1;">
                    <div style="font-size:0.62rem;color:#C8001E;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">{flag} · {date}</div>
                    <div style="font-size:0.88rem;font-weight:600;color:rgba(255,255,255,0.9);line-height:1.45;margin-bottom:8px;">
                        <a href="{item['link']}" target="_blank"
                           style="color:rgba(255,255,255,0.9);text-decoration:none;">{item['title'][:65]}{'...' if len(item['title'])>65 else ''}</a>
                    </div>
                    <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);">{item['source']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

        # 하단 4열 카드 그리드
        bottom_items = all_home[3:7]
        if bottom_items:
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:repeat({len(bottom_items)},1fr);gap:1px;background:rgba(255,255,255,0.05);margin-top:1px;">
            """, unsafe_allow_html=True)
            for i, item in enumerate(bottom_items):
                flag = "🇰🇷" if item in home_ko else "🌍"
                date = item['published'][:10] if item['published'] else ""
                img = TOPIC_IMGS_NEWS[(i+3) % len(TOPIC_IMGS_NEWS)]
                st.markdown(f"""
                <div style="background:#0a0a0a;overflow:hidden;">
                    <div style="overflow:hidden;height:180px;">
                        <img src="{img}"
                             style="width:100%;height:180px;object-fit:cover;filter:brightness(0.5);
                                    transition:transform 0.4s;"
                             onmouseover="this.style.transform='scale(1.04)'"
                             onmouseout="this.style.transform='scale(1)'">
                    </div>
                    <div style="padding:18px 20px 22px;">
                        <div style="font-size:0.6rem;color:#C8001E;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">{flag} · {date}</div>
                        <div style="font-size:0.88rem;font-weight:600;color:rgba(255,255,255,0.88);line-height:1.45;margin-bottom:8px;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;">
                            <a href="{item['link']}" target="_blank"
                               style="color:rgba(255,255,255,0.88);text-decoration:none;">{item['title']}</a>
                        </div>
                        <div style="font-size:0.7rem;color:rgba(255,255,255,0.28);">{item['source']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center;padding:60px;border:1px solid rgba(255,255,255,0.06);color:rgba(255,255,255,0.3);">
            <div style="font-size:2rem;margin-bottom:12px;">📰</div>
            <div>뉴스를 불러오는 중입니다...</div>
        </div>
        """, unsafe_allow_html=True)

    # 새로고침 버튼
    _, rc, _ = st.columns([4,2,4])
    with rc:
        if st.button("🔄 뉴스 새로고침", key="home_refresh", use_container_width=True):
            st.session_state["home_news_ko"] = []
            st.session_state["home_news_en"] = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # ── 24개 주제 탐색 ──
    st.markdown("""
    <div class="explorer-section">
        <div class="section-label">연구 주제</div>
        <div class="section-title">24개 핵심 주제</div>
        <div class="section-desc" style="margin-bottom:0;">각 주제를 선택하면 최신 뉴스, 논문 검색, 전문 보고서 자동 생성을 시작합니다.</div>
        <div class="topic-list">
    """, unsafe_allow_html=True)

    for i, (num, ko, en, desc, kw) in enumerate(TOPICS):
        st.markdown(f"""
        <div class="topic-row">
            <div class="topic-row-num">{num}</div>
            <div class="topic-row-title">{ko}</div>
            <div class="topic-row-en">{en}</div>
            <div class="topic-row-arrow">→</div>
        </div>
        """, unsafe_allow_html=True)
        # 실제 클릭 버튼 (투명하게 오버레이)
        if st.button(f"탐색: {ko}", key=f"tp_{i}", use_container_width=True):
            st.session_state["page"]="detail"; st.session_state["sel_idx"]=i
            for k2 in ["news_ko","news_en","papers","arxiv","sel_news","sel_papers","sel_arxiv","report"]:
                st.session_state[k2]=[] if k2!="report" else ""
            st.session_state["step"]=0; st.session_state["tab"]="news"
            st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🔋 BatteryIQ</div>
        <div class="footer-copy">Battery Management Systems · Gregory Plett · Chapter 2-04 · 배터리 건강 추정 연구 포털</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# DETAIL 페이지
# =====================================================================
else:
    tidx = st.session_state["sel_idx"]
    num, ko, en, bg, kw = TOPICS[tidx]

    # 히어로
    kw_chips = "".join([f'<span class="detail-kw">{k}</span>' for k in kw])
    st.markdown(f"""
    <div class="detail-hero">
        <div class="detail-breadcrumb">
            <span>BatteryIQ</span> <span>›</span> <span>연구 주제</span> <span>›</span> <span style="color:rgba(255,255,255,0.6);">{ko}</span>
        </div>
        <div class="detail-title">{ko}</div>
        <div class="detail-en">{en}</div>
        <div class="detail-kws">{kw_chips}</div>
    </div>
    """, unsafe_allow_html=True)

    # 뒤로가기
    bc, _ = st.columns([2,8])
    with bc:
        if st.button("← 홈으로"):
            st.session_state["page"]="home"; st.rerun()

    # 탭
    tabs = [("news","뉴스 수집"),("papers","논문 검색"),("select","자료 선택"),("report","보고서"),("save","다운로드")]
    tab_html = '<div class="dtab-wrap">'
    for tk,tl in tabs:
        cls = "active" if st.session_state["tab"]==tk else ""
        tab_html += f'<span class="dtab {cls}">{tl}</span>'
    tab_html += "</div>"
    st.markdown(tab_html, unsafe_allow_html=True)

    tc = st.columns(len(tabs))
    for i,(tk,tl) in enumerate(tabs):
        with tc[i]:
            if st.button(tl, key=f"t_{tk}", use_container_width=True):
                st.session_state["tab"]=tk; st.rerun()

    # 컨텐츠 + 사이드
    mc, sc = st.columns([7,3], gap="medium")

    with sc:
        step = st.session_state["step"]
        step_items = [("뉴스 수집",1),("논문 검색",2),("자료 선택",3),("보고서 생성",4)]
        ph = '<div style="background:#111;border:1px solid rgba(255,255,255,0.07);padding:20px;border-radius:2px;margin-bottom:16px;">'
        ph += '<div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:10px;">진행 상태</div>'
        for sl,st_n in step_items:
            done = step>=st_n
            ph += f'<div style="display:flex;align-items:center;gap:10px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.05);font-size:0.8rem;color:{"#C8001E" if done else "rgba(255,255,255,0.25)"};font-weight:{"600" if done else "400"};">{"●" if done else "○"} {sl}</div>'
        ph += "</div>"
        st.markdown(ph, unsafe_allow_html=True)

        nc_s = len(st.session_state["news_ko"])+len(st.session_state["news_en"])
        pc_s = len(st.session_state["papers"])+len(st.session_state["arxiv"])
        sc_s = len(st.session_state["sel_news"])+len(st.session_state["sel_papers"])+len(st.session_state["sel_arxiv"])
        st.markdown(f"""
        <div style="background:#111;border:1px solid rgba(255,255,255,0.07);padding:20px;border-radius:2px;margin-bottom:16px;">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:10px;">수집 현황</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
                <div style="background:#1a1a1a;padding:12px 4px;border-radius:2px;">
                    <div style="font-size:1.4rem;font-weight:800;color:#C8001E;font-family:'Plus Jakarta Sans',sans-serif;">{nc_s}</div>
                    <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);margin-top:2px;">뉴스</div>
                </div>
                <div style="background:#1a1a1a;padding:12px 4px;border-radius:2px;">
                    <div style="font-size:1.4rem;font-weight:800;color:#C8001E;font-family:'Plus Jakarta Sans',sans-serif;">{pc_s}</div>
                    <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);margin-top:2px;">논문</div>
                </div>
                <div style="background:#1a1a1a;padding:12px 4px;border-radius:2px;">
                    <div style="font-size:1.4rem;font-weight:800;color:#C8001E;font-family:'Plus Jakarta Sans',sans-serif;">{sc_s}</div>
                    <div style="font-size:0.65rem;color:rgba(255,255,255,0.3);margin-top:2px;">선택</div>
                </div>
            </div>
        </div>
        <div style="background:#111;border:1px solid rgba(255,255,255,0.07);padding:20px;border-radius:2px;">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:2px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:12px;">검색 키워드</div>
            <div style="font-size:0.82rem;color:rgba(255,255,255,0.7);line-height:1.6;font-weight:300;">{en}</div>
        </div>
        """, unsafe_allow_html=True)

    with mc:
        active = st.session_state["tab"]

        # 패널 클릭 시 뉴스 자동 수집
        if st.session_state.get("auto_fetch_news") and active == "news":
            st.session_state["auto_fetch_news"] = False
            with st.spinner("뉴스 자동 수집 중..."):
                raw_ko = fetch_news(ko+" 배터리","ko","KR","KR:ko",8)
                st.session_state["news_ko"] = [{"title":e.title,"link":e.link,"lang":"ko","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_ko]
                raw_en = fetch_news(en,"en","US","US:en",8)
                st.session_state["news_en"] = [{"title":e.title,"link":e.link,"lang":"en","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_en]
                if st.session_state["step"] < 1: st.session_state["step"] = 1

        st.markdown('<div style="padding:28px 0;">', unsafe_allow_html=True)

        if active=="news":
            # ── 표지 화면: 대표 뉴스 카드 ──
            all_items = [("🇰🇷",i) for i in st.session_state["news_ko"]] + [("🌍",i) for i in st.session_state["news_en"]]

            if all_items:
                # 대표 뉴스 (첫 번째) 표지 카드
                feat_flag, feat = all_items[0]
                # 주제별 대표 이미지 (TECH_HIGHLIGHTS에서 찾기)
                cover_img = next((img for n,_,_,_,_,img in TECH_HIGHLIGHTS if n==num), "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=1200&h=500&fit=crop")

                st.markdown(f"""
                <div style="position:relative;width:100%;height:320px;border-radius:4px;overflow:hidden;margin-bottom:28px;cursor:pointer;">
                    <img src="{cover_img}" style="width:100%;height:320px;object-fit:cover;filter:brightness(0.45);">
                    <div style="position:absolute;inset:0;background:linear-gradient(to right, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.3) 60%, transparent 100%);"></div>
                    <div style="position:absolute;bottom:0;left:0;padding:32px 36px;max-width:65%;">
                        <div style="font-size:0.62rem;font-weight:700;letter-spacing:3px;color:#C8001E;text-transform:uppercase;margin-bottom:10px;">
                            {feat_flag} 주요 뉴스 · TOPIC {num}
                        </div>
                        <div style="font-size:1.15rem;font-weight:700;color:#fff;line-height:1.45;margin-bottom:10px;letter-spacing:-0.3px;">
                            <a href="{feat['link']}" target="_blank" style="color:#fff;text-decoration:none;">{feat['title']}</a>
                        </div>
                        <div style="font-size:0.72rem;color:rgba(255,255,255,0.45);">
                            {feat['source']} &nbsp;·&nbsp; {feat['published'][:16]}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # 나머지 뉴스 그리드 (2~4번째)
                if len(all_items) > 1:
                    sub_items = all_items[1:4]
                    cols_news = st.columns(len(sub_items))
                    for col_n, (flag, item) in zip(cols_news, sub_items):
                        with col_n:
                            st.markdown(f"""
                            <div style="background:#111;border:1px solid rgba(255,255,255,0.07);border-radius:4px;overflow:hidden;margin-bottom:16px;">
                                <div style="padding:18px 18px 16px;">
                                    <div style="font-size:0.6rem;font-weight:700;color:#C8001E;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">{flag} 뉴스</div>
                                    <div style="font-size:0.85rem;font-weight:600;color:rgba(255,255,255,0.9);line-height:1.45;margin-bottom:8px;">
                                        <a href="{item['link']}" target="_blank" style="color:rgba(255,255,255,0.9);text-decoration:none;">{item['title'][:80]}{'...' if len(item['title'])>80 else ''}</a>
                                    </div>
                                    <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);">{item['source']} · {item['published'][:10]}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:20px 0;'>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:0.75rem;color:rgba(255,255,255,0.3);margin-bottom:14px;'>전체 뉴스 {len(all_items)}건</div>", unsafe_allow_html=True)

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

            # 전체 뉴스 리스트
            if all_items:
                for idx,(flag,item) in enumerate(all_items,1):
                    st.markdown(f'<div class="nitem"><div class="nidx">{idx:02d}</div><div><div class="nflag">{flag} {item["source"]}</div><div class="nitem-title"><a href="{item["link"]}" target="_blank">{item["title"]}</a></div><div class="nmeta">📅 {item["published"]}</div></div></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:50px;color:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.06);">위 버튼을 클릭해 뉴스를 수집하세요</div>', unsafe_allow_html=True)

        elif active=="papers":
            st.markdown('<div style="background:rgba(200,0,30,0.08);border-left:2px solid #C8001E;padding:10px 16px;font-size:0.82rem;color:rgba(255,255,255,0.6);margin-bottom:16px;">💡 arXiv — 무료·안정적·최신 프리프린트 논문</div>', unsafe_allow_html=True)
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
                st.markdown(f'<div class="pitem"><span class="pbadge pbadge-a">arXiv</span><div class="ptitle"><a href="{p["url"]}" target="_blank">{p["title"]}</a></div><div class="pauth">👤 {p["authors"]} | 📅 {p["published"]}</div><div class="pabs">{abs_t}</div></div>', unsafe_allow_html=True)
            st.markdown('<hr style="border-color:rgba(255,255,255,0.06);margin:20px 0;">', unsafe_allow_html=True)
            st.markdown('<div style="background:rgba(255,255,255,0.04);border-left:2px solid rgba(255,255,255,0.15);padding:10px 16px;font-size:0.82rem;color:rgba(255,255,255,0.4);margin-bottom:16px;">⚠️ Google Scholar — 잦은 요청 시 일시 차단 가능</div>', unsafe_allow_html=True)
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
                lh=f"<a href='{p['url']}' target='_blank' style='color:#C8001E;font-size:0.72rem;'>원문 →</a>" if p.get('url') else ""
                st.markdown(f'<div class="pitem"><span class="pbadge pbadge-s">Scholar</span><div class="ptitle">{p["title"]} ({p["year"]}) {lh}</div><div class="pauth">👤 {p["authors"]}{(" | 📔 "+p["journal"]) if p.get("journal") else ""}</div><div class="pabs">{abs_t}</div></div>', unsafe_allow_html=True)

        elif active=="select":
            an=st.session_state["news_ko"]+st.session_state["news_en"]
            ax=st.session_state["arxiv"]; asc=st.session_state["papers"]
            if not an and not ax and not asc:
                st.info("먼저 뉴스와 논문을 수집해주세요.")
            else:
                sn=[]; sa=[]; ss=[]
                if an:
                    st.markdown('<div class="selbox">📰 보고서에 포함할 뉴스를 선택하세요</div>', unsafe_allow_html=True)
                    c1,c2=st.columns(2)
                    for i,item in enumerate(an):
                        flag="🇰🇷" if item.get("lang")=="ko" else "🌍"
                        with (c1 if i%2==0 else c2):
                            if st.checkbox(f"{flag} {item['title'][:50]}{'...' if len(item['title'])>50 else ''}",key=f"sn_{i}"): sn.append(item)
                if ax or asc:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="selbox">📚 보고서에 포함할 논문을 선택하세요</div>', unsafe_allow_html=True)
                    if ax:
                        st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#C8001E;margin:8px 0 4px;letter-spacing:1px;'>arXiv</div>", unsafe_allow_html=True)
                        for i,p in enumerate(ax):
                            if st.checkbox(f"[arXiv] {p['title'][:58]}{'...' if len(p['title'])>58 else ''} ({p['published'][:7]})",key=f"sa_{i}"): sa.append(p)
                    if asc:
                        st.markdown("<div style='font-size:0.75rem;font-weight:700;color:#7eb8ff;margin:8px 0 4px;letter-spacing:1px;'>Google Scholar</div>", unsafe_allow_html=True)
                        for i,p in enumerate(asc):
                            if st.checkbox(f"[Scholar] {p['title'][:58]}{'...' if len(p['title'])>58 else ''} ({p['year']})",key=f"ss_{i}"): ss.append(p)
                st.session_state["sel_news"]=sn; st.session_state["sel_papers"]=ss; st.session_state["sel_arxiv"]=sa
                total=len(sn)+len(sa)+len(ss)
                st.markdown("<br>", unsafe_allow_html=True)
                if total>0:
                    st.success(f"✅ 뉴스 {len(sn)}건 + arXiv {len(sa)}편 + Scholar {len(ss)}편 선택됨")
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
                st.markdown('<div style="text-align:center;padding:60px;color:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.06);">자료 선택 탭에서 보고서를 생성하세요</div>', unsafe_allow_html=True)

        elif active=="save":
            rpt=st.session_state["report"]
            if rpt:
                st.success("✅ 보고서 준비 완료")
                edited=st.text_area("✏️ 최종 수정",value=rpt,height=360,key=f"e_{num}")
                st.session_state["report"]=edited
                fb=f"BatteryIQ_{num}_{datetime.now().strftime('%Y%m%d')}"
                c1,c2,c3=st.columns(3)
                with c1: st.download_button("📄 TXT",data=edited,file_name=f"{fb}.txt",mime="text/plain",type="primary",use_container_width=True)
                with c2: st.download_button("📋 Markdown",data=edited,file_name=f"{fb}.md",mime="text/markdown",type="primary",use_container_width=True)
                with c3:
                    if st.button("🖨️ 인쇄/PDF",use_container_width=True): st.info("Ctrl+P → PDF")
            else:
                st.markdown('<div style="text-align:center;padding:60px;color:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.06);">보고서를 먼저 생성해주세요</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # 푸터
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">🔋 BatteryIQ</div>
        <div class="footer-copy">Battery Management Systems · Gregory Plett · Chapter 2-04</div>
    </div>
    """, unsafe_allow_html=True)
