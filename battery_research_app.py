import streamlit as st
import feedparser
from scholarly import scholarly
from datetime import datetime
import time
import urllib.parse

# =====================================================================
# 페이지 설정
# =====================================================================
st.set_page_config(
    page_title="BatteryIQ — 배터리 건강 추정 연구 포털",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# 각 주제별 Unsplash 이미지 URL (무료, 직접 링크)
# =====================================================================
TOPIC_IMAGES = [
    "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=600&h=220&fit=crop",  # 01 배터리/EV
    "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=600&h=220&fit=crop",  # 02 음극/실험실
    "https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=600&h=220&fit=crop",  # 03 양극/전자현미경
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=220&fit=crop",  # 04 회로/전압
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=600&h=220&fit=crop",  # 05 코드/프로그래밍
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=220&fit=crop",     # 06 데이터/그래프
    "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&h=220&fit=crop",  # 07 칼만필터/수식
    "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600&h=220&fit=crop",  # 08 EKF/신호
    "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=220&fit=crop",    # 09 SPKF/파형
    "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=600&h=220&fit=crop", # 10 조인트추정
    "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=600&h=220&fit=crop",  # 11 견고성/테스트
    "https://images.unsplash.com/photo-1543286386-713bdd548da4?w=600&h=220&fit=crop",    # 12 선형회귀
    "https://images.unsplash.com/photo-1526628953301-3cd20f514094?w=600&h=220&fit=crop", # 13 통계/최소제곱
    "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=600&h=220&fit=crop", # 14 총 최소제곱
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600&h=220&fit=crop", # 15 모델적합도
    "https://images.unsplash.com/photo-1473091534298-04dcbce3278c?w=600&h=220&fit=crop", # 16 신뢰구간
    "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=600&h=220&fit=crop",   # 17 단순화
    "https://images.unsplash.com/photo-1518770660439-4636190af475?w=600&h=220&fit=crop", # 18 근사해
    "https://images.unsplash.com/photo-1607799279861-4dd421887fb3?w=600&h=220&fit=crop", # 19 시뮬레이션코드
    "https://images.unsplash.com/photo-1549317661-cf369843aba2?w=600&h=220&fit=crop",   # 20 HEV
    "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=600&h=220&fit=crop",   # 21 EV
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&h=220&fit=crop", # 22 논의/회의
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=220&fit=crop", # 23 미래방향
    "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=600&h=220&fit=crop", # 24 비선형필터
]

# =====================================================================
# CSS
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;900&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

:root {
    --primary:  #1D4ED8;
    --primary-dark: #1E3A8A;
    --accent:   #0EA5E9;
    --green:    #10B981;
    --red:      #EF4444;
    --bg:       #F1F5F9;
    --white:    #FFFFFF;
    --gray1:    #F8FAFC;
    --gray2:    #E2E8F0;
    --gray3:    #94A3B8;
    --gray4:    #64748B;
    --dark:     #0F172A;
    --card-shadow: 0 2px 12px rgba(15,23,42,0.08);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'Plus Jakarta Sans', sans-serif;
    background: var(--bg) !important;
    color: var(--dark);
}
.stApp { background: var(--bg) !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── 네비바 ── */
.nav {
    background: var(--dark);
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 36px;
    position: sticky;
    top: 0;
    z-index: 999;
}
.nav-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 1.25rem;
    color: var(--white);
    letter-spacing: -0.5px;
}
.nav-logo-badge {
    background: var(--primary);
    color: var(--white);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.nav-links {
    display: flex;
    gap: 24px;
    font-size: 0.8rem;
    font-weight: 500;
    color: #94A3B8;
}

/* ── 히어로 ── */
.hero {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 60%, var(--accent) 100%);
    padding: 40px 36px 32px;
}
.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6);
    margin-bottom: 10px;
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: var(--white);
    line-height: 1.15;
    margin-bottom: 10px;
    letter-spacing: -1px;
}
.hero-title span { color: #7DD3FC; }
.hero-sub {
    font-size: 0.92rem;
    color: rgba(255,255,255,0.7);
    font-weight: 400;
    margin-bottom: 24px;
}
.hero-stats {
    display: flex;
    gap: 28px;
}
.hero-stat-num {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #7DD3FC;
    line-height: 1;
}
.hero-stat-label {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── 섹션 헤더 ── */
.sec-header {
    background: var(--white);
    border-bottom: 1px solid var(--gray2);
    padding: 18px 36px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.sec-header-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--primary);
}
.sec-header-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--dark);
    letter-spacing: -0.3px;
}
.sec-header-sub {
    font-size: 0.78rem;
    color: var(--gray3);
    margin-left: auto;
}

/* ── 카드 그리드 ── */
.grid-wrap {
    padding: 20px 32px 40px;
    background: var(--bg);
}

/* ── 주제 카드 ── */
.topic-card {
    background: var(--white);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--card-shadow);
    border: 1px solid var(--gray2);
    transition: all 0.22s cubic-bezier(0.4,0,0.2,1);
    cursor: pointer;
    height: 100%;
}
.topic-card:hover {
    box-shadow: 0 12px 36px rgba(29,78,216,0.18);
    border-color: var(--primary);
    transform: translateY(-3px);
}
.card-img-wrap {
    position: relative;
    overflow: hidden;
    height: 160px;
}
.card-img-wrap img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    display: block;
    transition: transform 0.4s ease;
}
.topic-card:hover .card-img-wrap img { transform: scale(1.05); }
.card-num {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--primary);
    color: var(--white);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 0.8rem;
    padding: 3px 9px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}
.card-img-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 60px;
    background: linear-gradient(to top, rgba(15,23,42,0.5), transparent);
}
.card-body {
    padding: 14px 16px 16px;
}
.card-topic-label {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--primary);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.card-title {
    font-size: 0.98rem;
    font-weight: 700;
    color: var(--dark);
    line-height: 1.35;
    margin-bottom: 6px;
}
.card-desc {
    font-size: 0.76rem;
    color: var(--gray4);
    line-height: 1.55;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 0;
}

/* ── 버튼 ── */
.stButton > button {
    background: var(--primary) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.3px !important;
    padding: 9px 16px !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: var(--primary-dark) !important;
    box-shadow: 0 4px 16px rgba(29,78,216,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── 디테일 히어로 ── */
.detail-hero {
    background: linear-gradient(135deg, var(--primary-dark) 0%, #1E3A8A 100%);
    padding: 28px 36px 24px;
    position: relative;
    overflow: hidden;
}
.detail-hero::after {
    content: attr(data-num);
    position: absolute;
    right: 36px; top: 50%;
    transform: translateY(-50%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9rem;
    font-weight: 800;
    color: rgba(255,255,255,0.04);
    line-height: 1;
}
.detail-eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7DD3FC;
    margin-bottom: 8px;
}
.detail-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--white);
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 6px;
}
.detail-en {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.5);
}
.detail-kw-wrap {
    margin-top: 14px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}
.detail-kw {
    background: rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.8);
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.72rem;
    font-weight: 500;
}

/* ── 탭 ── */
.ptab-wrap {
    background: var(--white);
    border-bottom: 2px solid var(--gray2);
    display: flex;
    gap: 0;
    padding: 0 36px;
    overflow-x: auto;
}
.ptab {
    padding: 12px 20px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--gray4);
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    white-space: nowrap;
    cursor: pointer;
    letter-spacing: 0.2px;
    transition: color 0.15s;
}
.ptab.active { color: var(--primary); border-bottom-color: var(--primary); }
.ptab:hover  { color: var(--dark); }

/* ── 메인/사이드 레이아웃 ── */
.detail-body {
    background: var(--bg);
    padding: 24px 36px;
}

/* ── 뉴스 아이템 ── */
.news-item {
    background: var(--white);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    border: 1px solid var(--gray2);
    display: flex;
    gap: 14px;
    align-items: flex-start;
    box-shadow: 0 1px 4px rgba(15,23,42,0.04);
    transition: all 0.15s;
}
.news-item:hover { border-color: var(--primary); box-shadow: 0 4px 16px rgba(29,78,216,0.1); }
.news-idx {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--gray2);
    min-width: 30px;
    line-height: 1;
    padding-top: 2px;
}
.news-flag { font-size: 0.72rem; color: var(--gray3); margin-bottom: 3px; }
.news-title { font-size: 0.9rem; font-weight: 600; color: var(--dark); line-height: 1.4; margin-bottom: 4px; }
.news-title a { color: var(--dark); text-decoration: none; }
.news-title a:hover { color: var(--primary); }
.news-meta  { font-size: 0.72rem; color: var(--gray3); }

/* ── 논문 아이템 ── */
.paper-item {
    background: var(--white);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    border: 1px solid var(--gray2);
    border-left: 4px solid var(--accent);
    box-shadow: 0 1px 4px rgba(15,23,42,0.04);
}
.arxiv-item  { border-left-color: #F59E0B; }
.scholar-item { border-left-color: var(--primary); }
.paper-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}
.badge-arxiv   { background: #FEF3C7; color: #B45309; }
.badge-scholar { background: #EFF6FF; color: #1D4ED8; }
.paper-title { font-size: 0.88rem; font-weight: 600; color: #1D4ED8; line-height: 1.4; margin-bottom: 4px; }
.paper-title a { color: #1D4ED8; text-decoration: none; }
.paper-title a:hover { text-decoration: underline; }
.paper-author { font-size: 0.75rem; color: var(--gray4); margin-bottom: 5px; }
.paper-abs    { font-size: 0.78rem; color: var(--gray4); line-height: 1.65; }

/* ── 사이드 위젯 ── */
.widget {
    background: var(--white);
    border-radius: 12px;
    padding: 18px;
    border: 1px solid var(--gray2);
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(15,23,42,0.04);
}
.widget-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--dark);
    letter-spacing: 1px;
    text-transform: uppercase;
    border-bottom: 2px solid var(--primary);
    padding-bottom: 8px;
    margin-bottom: 12px;
}
.kw-chip {
    display: inline-block;
    background: #EFF6FF;
    color: var(--primary);
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 3px 11px;
    font-size: 0.73rem;
    font-weight: 500;
    margin: 3px;
}
.progress-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0;
    border-bottom: 1px solid var(--gray2);
    font-size: 0.8rem;
}
.progress-item:last-child { border-bottom: none; }
.pi-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--gray2);
    flex-shrink: 0;
}
.pi-dot.done { background: var(--green); }

/* ── 선택 박스 ── */
.sel-box {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-left: 3px solid var(--primary);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #1D4ED8;
    font-weight: 500;
    margin-bottom: 14px;
}

/* ── 보고서 ── */
.report-wrap {
    background: var(--white);
    border-radius: 12px;
    padding: 28px 32px;
    border: 1px solid var(--gray2);
    box-shadow: var(--card-shadow);
    line-height: 1.85;
    font-size: 0.88rem;
    color: #334155;
}

/* 탭 패널 숨김 (커스텀 탭 사용) */
.stTabs [data-baseweb="tab-list"] { display:none !important; }
.stTabs [data-baseweb="tab-panel"] { padding:0 !important; background:transparent !important; border:none !important; }

textarea {
    background: var(--gray1) !important;
    color: var(--dark) !important;
    border: 1px solid var(--gray2) !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
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
     ["내부 저항","전압 강하","등가 회로 모델","임피던스","열화 진단"]),
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
     ["신뢰 구간","불확실성 정량화","공분산","오차 한계","통계 추론"]),
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

# =====================================================================
# 수집 함수
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news(keyword, hl, gl, ceid, max_results=8):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(keyword)}&hl={hl}&gl={gl}&ceid={ceid}"
    try:
        return feedparser.parse(url).entries[:max_results]
    except:
        return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_arxiv(keyword, max_results=6):
    try:
        query = urllib.parse.quote(keyword)
        url = (f"https://export.arxiv.org/api/query"
               f"?search_query=all:{query}&start=0&max_results={max_results}"
               f"&sortBy=submittedDate&sortOrder=descending")
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries:
            title   = entry.get("title","").replace("\n"," ").strip()
            summary = entry.get("summary","")[:400].replace("\n"," ").strip()
            pub     = entry.get("published","")[:10]
            link    = entry.get("id","") or entry.get("link","")
            ar      = entry.get("authors",[])
            authors = ", ".join(a.get("name","") for a in ar[:3]) if ar else entry.get("author","")
            if title:
                results.append({"title":title,"authors":authors,"abstract":summary,"url":link,"published":pub,"source":"arXiv"})
        return results
    except:
        return []

def fetch_scholar(keyword, max_results=4):
    results = []
    try:
        gen = scholarly.search_pubs(keyword)
        for _ in range(max_results):
            try:
                pub = next(gen)
                bib = pub.get("bib",{})
                results.append({"title":bib.get("title","No title"),"authors":bib.get("author","Unknown"),
                                 "year":bib.get("pub_year",""),"journal":bib.get("venue",""),
                                 "abstract":bib.get("abstract",""),"url":pub.get("pub_url","")})
            except StopIteration:
                break
    except:
        pass
    return results

def build_report(num, ko, en, bg, kw, sel_news_ko, sel_news_en, sel_papers, sel_arxiv):
    today = datetime.now().strftime("%Y-%m-%d")
    kw_str = " / ".join(kw)
    n_news = len(sel_news_ko)+len(sel_news_en); n_p = len(sel_papers)+len(sel_arxiv)
    ref_num=1; refs=[]
    for p in sel_papers:
        r=f"[{ref_num}] {p['authors']} ({p['year']}). {p['title']}."
        if p.get('journal'): r+=f" {p['journal']}."
        if p.get('url'):     r+=f" {p['url']}"
        refs.append(r); ref_num+=1
    for p in sel_arxiv:
        refs.append(f"[{ref_num}] {p['authors']} ({p['published'][:4]}). {p['title']}. arXiv. {p['url']}")
        ref_num+=1
    for n in sel_news_ko+sel_news_en:
        refs.append(f"[{ref_num}] {n['title']}. {n['source']} ({n['published']}). {n['link']}")
        ref_num+=1

    scholar_body="".join([f"\n**[{i}] {p['title']}** ({p['year']}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(sel_papers,1)]) or "(없음)"
    arxiv_body  ="".join([f"\n**[{i}] [{p['title']}]({p['url']})** ({p['published'][:7]}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(sel_arxiv,len(sel_papers)+1)]) or "(없음)"

    return f"""# {num}. {ko}
## 연구 분석 보고서 — BatteryIQ

**작성일:** {today} | **키워드:** {kw_str}
**기준 문헌:** Gregory Plett - *Battery Management Systems*
**수집 자료:** 뉴스 {n_news}건 · 논문 {n_p}편

---

## 초록 (Abstract)

{ko}은(는) 배터리 건강 상태(SOH) 추정의 핵심 주제이다. {bg} 본 보고서는 뉴스 {n_news}건, 논문 {n_p}편을 분석하여 현황과 연구 동향을 정리한다.

**키워드:** {kw_str}

---

## 1. 서론

### 1.1 연구 배경
{bg}

### 1.2 연구 목적
{ko}({en})에 관한 최신 연구 동향과 기술 현황을 체계적으로 분석한다.

### 1.3 구성
이론적 배경(2장) → 최신 동향(3장) → 선행 연구(4장) → 기술 분석(5장) → 결론(6장)

---

## 2. 이론적 배경

{bg}

| 핵심 개념 | 설명 |
|----------|------|
{"".join([f'| **{k}** | {ko} 분야 핵심 요소 |\n' for k in kw])}

---

## 3. 최신 기술 동향

### 3.1 국내 동향
{"".join([f'**[뉴스]** [{n["title"]}]({n["link"]})\n> {n["source"]} | {n["published"]}\n\n' for n in sel_news_ko]) or "(없음)"}

### 3.2 해외 동향
{"".join([f'**[News]** [{n["title"]}]({n["link"]})\n> {n["source"]} | {n["published"]}\n\n' for n in sel_news_en]) or "(없음)"}

---

## 4. 핵심 선행 연구 검토

### 4.1 Google Scholar
{scholar_body}

### 4.2 arXiv 최신 연구
{arxiv_body}

---

## 5. 기술적 분석 및 고찰

| 구분 | 주요 방법 | 특징 | 적용 분야 |
|------|----------|------|----------|
| 모델 기반 | 등가 회로 모델 | 구현 용이, 실시간 | BMS 내장 |
| 필터 기반 | EKF / UKF | 높은 정확도 | 전기차 |
| 데이터 기반 | 머신러닝 / DL | 대용량 데이터 | 클라우드 BMS |

---

## 6. 결론 및 향후 연구 방향

- {ko}은(는) BMS 핵심 기능으로 연구 수요 지속 증가
- 칼만 필터 계열 + 데이터 기반 융합 연구 트렌드
- AI/ML 융합, 디지털 트윈, 차세대 배터리 적용이 향후 과제

---

## 참고문헌

{"".join([f'{r}  \n' for r in refs]) or "(없음)"}

---
*BatteryIQ 연구 포털 | Gregory Plett, Battery Management Systems Vol.2 (2015)*
"""

# =====================================================================
# 세션 초기화
# =====================================================================
for k,v in [("page","home"),("sel_idx",0),
            ("news_ko",[]),("news_en",[]),("papers",[]),("arxiv",[]),
            ("sel_news",[]),("sel_papers",[]),("sel_arxiv",[]),
            ("report",""),("tab","news"),("step",0)]:
    if k not in st.session_state: st.session_state[k]=v

# =====================================================================
# 네비바
# =====================================================================
nc = len(st.session_state["news_ko"])+len(st.session_state["news_en"])
pc = len(st.session_state["papers"])+len(st.session_state["arxiv"])
st.markdown(f"""
<div class="nav">
    <div class="nav-logo">
        🔋 BatteryIQ
        <span class="nav-logo-badge">RESEARCH PORTAL</span>
    </div>
    <div class="nav-links">
        <span>배터리 건강 추정</span>
        <span>Gregory Plett · Chapter 2-04</span>
        <span style="color:#7DD3FC;">📰 {nc}건 &nbsp;📚 {pc}편</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# HOME
# =====================================================================
if st.session_state["page"] == "home":

    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Battery Management Systems · Chapter 2-04</div>
        <div class="hero-title">배터리 <span>건강 추정</span><br>연구 포털</div>
        <div class="hero-sub">Battery State of Health Estimation — 24개 핵심 주제 · 최신 논문 · 뉴스 · 전문 보고서 자동 생성</div>
        <div class="hero-stats">
            <div><div class="hero-stat-num">24</div><div class="hero-stat-label">Topics</div></div>
            <div><div class="hero-stat-num">2</div><div class="hero-stat-label">News Sources</div></div>
            <div><div class="hero-stat-num">2</div><div class="hero-stat-label">Paper DBs</div></div>
            <div><div class="hero-stat-num">Free</div><div class="hero-stat-label">No API Key</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sec-header">
        <div class="sec-header-dot"></div>
        <div class="sec-header-title">전체 연구 주제</div>
        <div class="sec-header-sub">주제를 클릭하면 뉴스·논문 수집 및 보고서 생성을 시작합니다</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="grid-wrap">', unsafe_allow_html=True)

    cols_per_row = 4
    for row_start in range(0, len(TOPICS), cols_per_row):
        row_topics = TOPICS[row_start:row_start+cols_per_row]
        cols = st.columns(cols_per_row, gap="small")
        for ci, (col, topic) in enumerate(zip(cols, row_topics)):
            tidx = row_start + ci
            num, ko, en, desc, kw = topic
            img_url = TOPIC_IMAGES[tidx] if tidx < len(TOPIC_IMAGES) else ""
            with col:
                st.markdown(f"""
                <div class="topic-card">
                    <div class="card-img-wrap">
                        <img src="{img_url}" alt="{ko}" onerror="this.style.background='linear-gradient(135deg,#1E3A8A,#1D4ED8)';this.style.height='160px';this.remove();">
                        <div class="card-img-overlay"></div>
                        <div class="card-num">{num}</div>
                    </div>
                    <div class="card-body">
                        <div class="card-topic-label">TOPIC {num}</div>
                        <div class="card-title">{ko}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"자세히 보기 →", key=f"c_{tidx}", use_container_width=True):
                    st.session_state["page"] = "detail"
                    st.session_state["sel_idx"] = tidx
                    for k2 in ["news_ko","news_en","papers","arxiv","sel_news","sel_papers","sel_arxiv","report"]:
                        st.session_state[k2] = [] if k2!="report" else ""
                    st.session_state["step"] = 0
                    st.session_state["tab"] = "news"
                    st.rerun()
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# DETAIL
# =====================================================================
else:
    tidx = st.session_state["sel_idx"]
    num, ko, en, bg, kw = TOPICS[tidx]
    img_url = TOPIC_IMAGES[tidx] if tidx < len(TOPIC_IMAGES) else ""

    st.markdown(f"""
    <div class="detail-hero" data-num="{num}">
        <div class="detail-eyebrow">BatteryIQ Research Portal · Topic {num} / 24</div>
        <div class="detail-title">{ko}</div>
        <div class="detail-en">{en}</div>
        <div class="detail-kw-wrap">
            {"".join([f'<span class="detail-kw">{k}</span>' for k in kw])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 뒤로가기
    bc, _ = st.columns([2,8])
    with bc:
        if st.button("← 홈으로 돌아가기"):
            st.session_state["page"] = "home"
            st.rerun()

    # 탭 버튼
    tabs = [("news","📡 뉴스 수집"),("papers","📚 논문 검색"),
            ("select","✅ 자료 선택"),("report","📄 보고서"),("save","💾 다운로드")]
    tab_html = '<div class="ptab-wrap">'
    for tk, tl in tabs:
        cls = "active" if st.session_state["tab"]==tk else ""
        tab_html += f'<span class="ptab {cls}">{tl}</span>'
    tab_html += "</div>"
    st.markdown(tab_html, unsafe_allow_html=True)

    tcols = st.columns(len(tabs))
    for i,(tk,tl) in enumerate(tabs):
        with tcols[i]:
            if st.button(tl, key=f"t_{tk}", use_container_width=True):
                st.session_state["tab"]=tk; st.rerun()

    # 메인 + 사이드
    main_col, side_col = st.columns([7,3], gap="medium")

    # ── 사이드 ──
    with side_col:
        step = st.session_state["step"]
        steps_def = [("뉴스 수집",1),("논문 검색",2),("자료 선택",3),("보고서 생성",4)]
        prog_html = '<div class="widget"><div class="widget-title">진행 상태</div>'
        for sl,st_n in steps_def:
            done = step>=st_n
            prog_html += f'<div class="progress-item"><div class="pi-dot {"done" if done else ""}"></div><span style="color:{"#10B981" if done else "#94A3B8"};font-weight:{"600" if done else "400"};">{"✓" if done else "○"} {sl}</span></div>'
        prog_html += "</div>"
        st.markdown(prog_html, unsafe_allow_html=True)

        kw_chips = "".join([f'<span class="kw-chip">{k}</span>' for k in kw])
        kw_html = f'<div class="widget"><div class="widget-title">Keywords</div>{kw_chips}</div>'
        st.markdown(kw_html, unsafe_allow_html=True)

        st.markdown(f'<div class="widget"><div class="widget-title">Topic Overview</div><div style="font-size:0.82rem;color:#64748B;line-height:1.7;">{bg}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="widget"><div class="widget-title">Search Keyword</div><div style="font-size:0.8rem;color:#1D4ED8;font-weight:600;background:#EFF6FF;padding:8px 12px;border-radius:6px;">{en}</div></div>', unsafe_allow_html=True)

        nc_s = len(st.session_state["news_ko"])+len(st.session_state["news_en"])
        pc_s = len(st.session_state["papers"])+len(st.session_state["arxiv"])
        sc_s = len(st.session_state["sel_news"])+len(st.session_state["sel_papers"])+len(st.session_state["sel_arxiv"])
        st.markdown(f"""
        <div class="widget">
            <div class="widget-title">수집 현황</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
                <div style="background:#EFF6FF;border-radius:8px;padding:10px 4px;">
                    <div style="font-size:1.3rem;font-weight:800;color:#1D4ED8;">{nc_s}</div>
                    <div style="font-size:0.66rem;color:#94A3B8;">뉴스</div>
                </div>
                <div style="background:#F0FDF4;border-radius:8px;padding:10px 4px;">
                    <div style="font-size:1.3rem;font-weight:800;color:#10B981;">{pc_s}</div>
                    <div style="font-size:0.66rem;color:#94A3B8;">논문</div>
                </div>
                <div style="background:#FEF3C7;border-radius:8px;padding:10px 4px;">
                    <div style="font-size:1.3rem;font-weight:800;color:#D97706;">{sc_s}</div>
                    <div style="font-size:0.66rem;color:#94A3B8;">선택</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── 메인 ──
    with main_col:
        active = st.session_state["tab"]

        # ── 뉴스 ──
        if active == "news":
            st.markdown("**Google News에서 국내·해외 최신 뉴스를 수집합니다.**")
            c1,c2 = st.columns([4,1])
            with c1: run_news = st.button("🔄 뉴스 수집 시작", type="primary", use_container_width=True)
            with c2:
                if st.button("초기화", use_container_width=True):
                    st.session_state["news_ko"]=[]; st.session_state["news_en"]=[]; st.rerun()

            if run_news:
                prog=st.progress(0)
                prog.progress(20)
                raw_ko = fetch_news(ko+" 배터리","ko","KR","KR:ko",8)
                st.session_state["news_ko"]=[{"title":e.title,"link":e.link,"lang":"ko","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_ko]
                prog.progress(65)
                raw_en = fetch_news(en,"en","US","US:en",8)
                st.session_state["news_en"]=[{"title":e.title,"link":e.link,"lang":"en","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_en]
                prog.progress(100); prog.empty()
                if st.session_state["step"]<1: st.session_state["step"]=1
                st.rerun()

            ko_list=st.session_state["news_ko"]; en_list=st.session_state["news_en"]
            if ko_list or en_list:
                st.success(f"✅ 총 {len(ko_list)+len(en_list)}건 수집 완료")
                all_items=[("🇰🇷",i) for i in ko_list]+[("🌍",i) for i in en_list]
                for idx,(flag,item) in enumerate(all_items,1):
                    st.markdown(f"""<div class="news-item">
                        <div class="news-idx">{idx:02d}</div>
                        <div>
                            <div class="news-flag">{flag} {item['source']}</div>
                            <div class="news-title"><a href="{item['link']}" target="_blank">{item['title']}</a></div>
                            <div class="news-meta">📅 {item['published']}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:50px;color:#94A3B8;border:2px dashed #E2E8F0;border-radius:12px;margin-top:16px;"><div style="font-size:2.5rem;margin-bottom:8px;">📰</div><div>위 버튼을 클릭해 뉴스를 수집하세요</div></div>', unsafe_allow_html=True)

        # ── 논문 ──
        elif active == "papers":
            st.markdown('<div style="background:#FFFBEB;border-left:3px solid #F59E0B;padding:8px 14px;border-radius:0 8px 8px 0;font-size:0.82rem;color:#92400E;margin-bottom:14px;">💡 <b>arXiv</b> — 무료·차단없음·최신 프리프린트 논문</div>', unsafe_allow_html=True)
            ca1,ca2=st.columns([4,1])
            with ca1: run_arxiv=st.button("🔍 arXiv 논문 검색",type="primary",use_container_width=True)
            with ca2:
                if st.button("초기화 ",use_container_width=True):
                    st.session_state["arxiv"]=[]; st.rerun()

            if run_arxiv:
                with st.spinner("arXiv 검색 중..."):
                    results=fetch_arxiv(en,6)
                if results:
                    st.session_state["arxiv"]=results
                    if st.session_state["step"]<2: st.session_state["step"]=2
                    st.rerun()
                else:
                    st.error("arXiv 검색 결과 없음. 잠시 후 재시도하세요.")

            for p in st.session_state["arxiv"]:
                abs_t=(p['abstract'][:200]+"...") if len(p['abstract'])>200 else p['abstract']
                st.markdown(f"""<div class="paper-item arxiv-item">
                    <span class="paper-badge badge-arxiv">arXiv</span>
                    <div class="paper-title"><a href="{p['url']}" target="_blank">{p['title']}</a></div>
                    <div class="paper-author">👤 {p['authors']} | 📅 {p['published']}</div>
                    <div class="paper-abs">{abs_t}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("<hr style='margin:20px 0;'>", unsafe_allow_html=True)
            st.markdown('<div style="background:#FEF2F2;border-left:3px solid #EF4444;padding:8px 14px;border-radius:0 8px 8px 0;font-size:0.82rem;color:#7F1D1D;margin-bottom:14px;">⚠️ <b>Google Scholar</b> — 잦은 요청 시 일시 차단될 수 있음</div>', unsafe_allow_html=True)
            cs1,cs2=st.columns([4,1])
            with cs1: run_scholar=st.button("🔍 Google Scholar 검색",type="primary",use_container_width=True)
            with cs2:
                if st.button("초기화  ",use_container_width=True):
                    st.session_state["papers"]=[]; st.rerun()

            if run_scholar:
                with st.spinner("Google Scholar 조회 중..."):
                    sch=fetch_scholar(en,4)
                st.session_state["papers"]=sch
                if st.session_state["step"]<2: st.session_state["step"]=2
                st.rerun()

            for p in st.session_state["papers"]:
                abs_t=(p['abstract'][:200]+"...") if len(p['abstract'])>200 else p['abstract']
                lh=f"<a href='{p['url']}' target='_blank' style='color:#1D4ED8;font-size:0.75rem;'>원문 →</a>" if p.get('url') else ""
                st.markdown(f"""<div class="paper-item scholar-item">
                    <span class="paper-badge badge-scholar">Scholar</span>
                    <div class="paper-title">{p['title']} ({p['year']}) {lh}</div>
                    <div class="paper-author">👤 {p['authors']}{(' | 📔 '+p['journal']) if p.get('journal') else ''}</div>
                    <div class="paper-abs">{abs_t}</div>
                </div>""", unsafe_allow_html=True)

        # ── 자료 선택 ──
        elif active == "select":
            all_news=st.session_state["news_ko"]+st.session_state["news_en"]
            all_ax=st.session_state["arxiv"]; all_sc=st.session_state["papers"]
            if not all_news and not all_ax and not all_sc:
                st.info("먼저 뉴스와 논문을 수집해주세요.")
            else:
                sn=[]; sa=[]; ss=[]
                if all_news:
                    st.markdown('<div class="sel-box">📰 보고서에 포함할 뉴스를 선택하세요</div>', unsafe_allow_html=True)
                    c1,c2=st.columns(2)
                    for i,item in enumerate(all_news):
                        flag="🇰🇷" if item.get("lang")=="ko" else "🌍"
                        with (c1 if i%2==0 else c2):
                            if st.checkbox(f"{flag} {item['title'][:50]}{'...' if len(item['title'])>50 else ''}",key=f"sn_{i}"):
                                sn.append(item)

                if all_ax or all_sc:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="sel-box">📚 보고서에 포함할 논문을 선택하세요</div>', unsafe_allow_html=True)
                    if all_ax:
                        st.markdown("<div style='font-size:0.8rem;font-weight:700;color:#B45309;margin:8px 0 4px;'>arXiv</div>", unsafe_allow_html=True)
                        for i,p in enumerate(all_ax):
                            if st.checkbox(f"[arXiv] {p['title'][:58]}{'...' if len(p['title'])>58 else ''} ({p['published'][:7]})",key=f"sa_{i}"):
                                sa.append(p)
                    if all_sc:
                        st.markdown("<div style='font-size:0.8rem;font-weight:700;color:#1D4ED8;margin:8px 0 4px;'>Google Scholar</div>", unsafe_allow_html=True)
                        for i,p in enumerate(all_sc):
                            if st.checkbox(f"[Scholar] {p['title'][:58]}{'...' if len(p['title'])>58 else ''} ({p['year']})",key=f"ss_{i}"):
                                ss.append(p)

                st.session_state["sel_news"]=sn; st.session_state["sel_papers"]=ss; st.session_state["sel_arxiv"]=sa
                total=len(sn)+len(sa)+len(ss)
                st.markdown("<br>", unsafe_allow_html=True)
                if total>0:
                    st.success(f"✅ 선택: 뉴스 {len(sn)}건 + arXiv {len(sa)}편 + Scholar {len(ss)}편")
                    if st.session_state["step"]<3: st.session_state["step"]=3

                gen=st.button("📄 전문 보고서 자동 생성",type="primary",use_container_width=True,disabled=(total==0))
                if gen and total>0:
                    with st.spinner("보고서 생성 중..."):
                        time.sleep(0.3)
                        news_ko_sel=[n for n in sn if n.get("lang")=="ko"]
                        news_en_sel=[n for n in sn if n.get("lang")=="en"]
                        rpt=build_report(num,ko,en,bg,kw,news_ko_sel,news_en_sel,ss,sa)
                        st.session_state["report"]=rpt
                        if st.session_state["step"]<4: st.session_state["step"]=4
                    st.success("✅ 보고서 생성 완료! '보고서' 탭에서 확인하세요.")

        # ── 보고서 ──
        elif active == "report":
            rpt=st.session_state["report"]
            if rpt:
                st.markdown(f'<div class="report-wrap">', unsafe_allow_html=True)
                st.markdown(rpt)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;padding:50px;color:#94A3B8;border:2px dashed #E2E8F0;border-radius:12px;"><div style="font-size:2.5rem;margin-bottom:8px;">📄</div><div>자료 선택 탭에서 보고서를 생성하세요</div></div>', unsafe_allow_html=True)

        # ── 다운로드 ──
        elif active == "save":
            rpt=st.session_state["report"]
            if rpt:
                st.success("✅ 보고서 준비 완료")
                edited=st.text_area("✏️ 최종 수정",value=rpt,height=400,key=f"e_{num}")
                st.session_state["report"]=edited
                st.markdown("<br>", unsafe_allow_html=True)
                fb=f"BatteryIQ_{num}_{datetime.now().strftime('%Y%m%d')}"
                c1,c2,c3=st.columns(3)
                with c1: st.download_button("📄 TXT 다운로드",data=edited,file_name=f"{fb}.txt",mime="text/plain",type="primary",use_container_width=True)
                with c2: st.download_button("📋 Markdown",data=edited,file_name=f"{fb}.md",mime="text/markdown",type="primary",use_container_width=True)
                with c3:
                    if st.button("🖨️ 인쇄/PDF",use_container_width=True):
                        st.info("Ctrl+P → PDF로 저장")
            else:
                st.markdown('<div style="text-align:center;padding:50px;color:#94A3B8;border:2px dashed #E2E8F0;border-radius:12px;"><div style="font-size:2.5rem;margin-bottom:8px;">💾</div><div>보고서를 먼저 생성해주세요</div></div>', unsafe_allow_html=True)
