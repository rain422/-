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
    page_title="BATTERYSIM — Battery Research Hub",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================================
# 전역 CSS — 포털/매거진 스타일
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Bebas+Neue&family=Barlow:wght@400;600;700;900&display=swap');

:root {
    --red:    #e8001c;
    --black:  #111111;
    --white:  #ffffff;
    --gray1:  #f4f4f4;
    --gray2:  #e0e0e0;
    --gray3:  #888888;
    --accent: #ff2d44;
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'Barlow', sans-serif;
    background: #f4f4f4 !important;
    color: var(--black);
}

/* 전체 앱 배경 */
.stApp { background: #f4f4f4 !important; }

/* 사이드바 숨김 */
section[data-testid="stSidebar"] { display: none !important; }
.stAppViewContainer { padding: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding: 0 !important; max-width: 100% !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── 상단 네비 ── */
.portal-nav {
    background: var(--black);
    padding: 0 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 3px solid var(--red);
}
.portal-logo {
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 1.6rem;
    color: var(--white);
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.portal-logo span { color: var(--red); font-style: italic; }
.portal-nav-links {
    display: flex;
    gap: 28px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #aaaaaa;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.portal-nav-links a { color: #aaaaaa; text-decoration: none; }
.portal-nav-links a:hover { color: var(--white); }
.portal-nav-links a.active { color: var(--white); }

/* ── 히어로 배너 ── */
.portal-hero {
    background: var(--black);
    padding: 36px 40px 28px;
    border-bottom: 1px solid #222;
}
.portal-hero-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.portal-hero-title {
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 3.2rem;
    color: var(--white);
    letter-spacing: 2px;
    line-height: 1;
    margin-bottom: 10px;
}
.portal-hero-sub {
    font-size: 0.9rem;
    color: #888;
    font-weight: 400;
}
.portal-hero-stats {
    display: flex;
    gap: 32px;
    margin-top: 20px;
}
.portal-stat {
    text-align: center;
}
.portal-stat-num {
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 2rem;
    color: var(--red);
    line-height: 1;
}
.portal-stat-label {
    font-size: 0.72rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── 섹션 헤더 ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 22px 40px 14px;
    background: var(--white);
    border-bottom: 2px solid var(--gray2);
    margin-bottom: 0;
}
.section-header-line {
    width: 4px;
    height: 22px;
    background: var(--red);
    border-radius: 2px;
}
.section-header-title {
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 1px;
    color: var(--black);
}
.section-header-count {
    font-size: 0.78rem;
    color: var(--gray3);
    font-weight: 500;
    margin-left: auto;
}

/* ── 카드 그리드 ── */
.card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    background: var(--gray2);
    border: 1px solid var(--gray2);
}

/* ── 주제 카드 ── */
.topic-card {
    background: var(--white);
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid var(--gray2);
    position: relative;
    overflow: hidden;
}
.topic-card:hover { box-shadow: 0 8px 32px rgba(0,0,0,0.15); z-index: 2; transform: translateY(-2px); }
.topic-card:hover .card-overlay { opacity: 1; }

.card-thumb {
    width: 100%;
    height: 180px;
    object-fit: cover;
    display: block;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    position: relative;
    overflow: hidden;
}

/* 썸네일 — 번호별 그라데이션 색상 */
.card-thumb-inner {
    width: 100%;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem;
    color: rgba(255,255,255,0.08);
    letter-spacing: 4px;
    position: relative;
}
.card-thumb-inner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: inherit;
}
.card-num-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: var(--red);
    color: var(--white);
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
    letter-spacing: 0;
    z-index: 2;
}
.card-overlay {
    position: absolute;
    inset: 0;
    background: rgba(232,0,28,0.08);
    opacity: 0;
    transition: opacity 0.2s;
}

.card-body {
    padding: 16px 18px 18px;
}
.card-round-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--black);
    line-height: 1.35;
    margin-bottom: 7px;
}
.card-desc {
    font-size: 0.78rem;
    color: var(--gray3);
    line-height: 1.55;
    margin-bottom: 12px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.card-link {
    font-size: 0.73rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 1px;
    text-transform: uppercase;
    text-decoration: none;
}

/* ── 디테일 뷰 ── */
.detail-wrap { background: var(--white); min-height: 100vh; }
.detail-hero {
    background: var(--black);
    padding: 32px 40px 28px;
    position: relative;
    overflow: hidden;
}
.detail-hero::before {
    content: attr(data-num);
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 10rem;
    color: rgba(255,255,255,0.04);
    line-height: 1;
    pointer-events: none;
}
.detail-back {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
    margin-bottom: 16px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: none;
    border: none;
    padding: 0;
}
.detail-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--red);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.detail-title {
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 2.6rem;
    color: var(--white);
    letter-spacing: 1px;
    line-height: 1.1;
    margin-bottom: 8px;
}
.detail-en {
    font-size: 0.88rem;
    color: #666;
    font-weight: 400;
}

/* ── 콘텐츠 영역 ── */
.detail-content {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 0;
    min-height: calc(100vh - 200px);
}
.detail-main { padding: 28px 36px; border-right: 1px solid var(--gray2); }
.detail-side { padding: 24px 24px; background: var(--gray1); }

/* 탭 */
.portal-tabs {
    display: flex;
    gap: 0;
    border-bottom: 2px solid var(--gray2);
    margin-bottom: 24px;
}
.portal-tab {
    padding: 10px 22px;
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--gray3);
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    background: none;
    border-top: none;
    border-left: none;
    border-right: none;
    transition: color 0.15s;
}
.portal-tab.active { color: var(--red); border-bottom-color: var(--red); }
.portal-tab:hover  { color: var(--black); }

/* 뉴스 아이템 */
.news-row {
    display: flex;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid var(--gray2);
    cursor: pointer;
    transition: background 0.15s;
}
.news-row:hover { background: #fafafa; margin: 0 -14px; padding: 14px; }
.news-row:last-child { border-bottom: none; }
.news-row-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: var(--gray2);
    min-width: 32px;
    line-height: 1;
    padding-top: 2px;
}
.news-row-content { flex: 1; }
.news-row-flag { font-size: 0.75rem; margin-bottom: 3px; }
.news-row-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--black);
    line-height: 1.4;
    margin-bottom: 4px;
}
.news-row-title a { color: var(--black); text-decoration: none; }
.news-row-title a:hover { color: var(--red); }
.news-row-meta { font-size: 0.72rem; color: var(--gray3); }

/* 논문 아이템 */
.paper-row {
    padding: 14px 0;
    border-bottom: 1px solid var(--gray2);
}
.paper-row:last-child { border-bottom: none; }
.paper-badge {
    display: inline-block;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 2px;
    margin-bottom: 5px;
    letter-spacing: 1px;
}
.paper-badge.arxiv   { background: #fff3e0; color: #e8710a; border: 1px solid #ffcc80; }
.paper-badge.scholar { background: #e8f0fe; color: #1a73e8; border: 1px solid #aecbfa; }
.paper-row-title { font-size: 0.88rem; font-weight: 600; color: #1a0dab; line-height: 1.4; margin-bottom: 4px; }
.paper-row-title a { color: #1a0dab; text-decoration: none; }
.paper-row-title a:hover { text-decoration: underline; }
.paper-row-author { font-size: 0.75rem; color: var(--gray3); margin-bottom: 5px; }
.paper-row-abs { font-size: 0.78rem; color: #444; line-height: 1.6; }

/* 사이드 위젯 */
.side-widget { margin-bottom: 24px; }
.side-widget-title {
    font-family: 'Bebas Neue', 'Barlow', sans-serif;
    font-size: 1rem;
    letter-spacing: 1px;
    color: var(--black);
    border-bottom: 2px solid var(--red);
    padding-bottom: 6px;
    margin-bottom: 12px;
}
.kw-tag {
    display: inline-block;
    background: var(--white);
    border: 1px solid var(--gray2);
    border-radius: 2px;
    padding: 4px 10px;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--black);
    margin: 3px;
}
.kw-tag:hover { background: var(--red); color: var(--white); border-color: var(--red); cursor: pointer; }

/* 보고서 섹션 */
.report-section {
    background: var(--white);
    border: 1px solid var(--gray2);
    border-top: 3px solid var(--red);
    padding: 24px 28px;
    margin-top: 24px;
    border-radius: 0 0 4px 4px;
}
.report-section h2 {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--black);
    border-left: 3px solid var(--red);
    padding-left: 10px;
    margin: 20px 0 8px;
}

/* 선택 체크박스 컨테이너 */
.select-box {
    background: #fffbe6;
    border: 1px solid #ffe082;
    border-left: 3px solid #f59e0b;
    padding: 10px 14px;
    border-radius: 0 4px 4px 0;
    font-size: 0.82rem;
    color: #7c5a00;
    margin-bottom: 14px;
}

/* 액션 버튼 */
.stButton > button {
    background: var(--red) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #c0001a !important; }

/* 탭 패널 */
.stTabs [data-baseweb="tab-list"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; background: transparent !important; border: none !important; }

/* textarea */
textarea {
    background: #fafafa !important;
    color: var(--black) !important;
    border: 1px solid var(--gray2) !important;
    border-radius: 2px !important;
    font-size: 0.85rem !important;
}

/* 숨김 처리 */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 주제 데이터
# =====================================================================
THUMB_COLORS = [
    "linear-gradient(135deg,#1a1a2e,#e8001c)",
    "linear-gradient(135deg,#0f3460,#e94560)",
    "linear-gradient(135deg,#1b262c,#0f3460)",
    "linear-gradient(135deg,#16213e,#1a1a2e)",
    "linear-gradient(135deg,#2d132c,#ee4540)",
    "linear-gradient(135deg,#0d0d0d,#434343)",
    "linear-gradient(135deg,#141e30,#243b55)",
    "linear-gradient(135deg,#1f1c18,#c94b4b)",
    "linear-gradient(135deg,#0f2027,#203a43)",
    "linear-gradient(135deg,#373b44,#4286f4)",
    "linear-gradient(135deg,#200122,#6f0000)",
    "linear-gradient(135deg,#1a1a1a,#e8001c)",
    "linear-gradient(135deg,#0d1b2a,#1b4332)",
    "linear-gradient(135deg,#2c3e50,#4ca1af)",
    "linear-gradient(135deg,#1a1a2e,#e8001c)",
    "linear-gradient(135deg,#0f3460,#e94560)",
    "linear-gradient(135deg,#1b262c,#0f3460)",
    "linear-gradient(135deg,#16213e,#1a1a2e)",
    "linear-gradient(135deg,#2d132c,#ee4540)",
    "linear-gradient(135deg,#0d0d0d,#434343)",
    "linear-gradient(135deg,#141e30,#243b55)",
    "linear-gradient(135deg,#1f1c18,#c94b4b)",
    "linear-gradient(135deg,#0f2027,#203a43)",
    "linear-gradient(135deg,#373b44,#4286f4)",
]

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
# 데이터 수집 함수
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news(keyword, hl, gl, ceid, max_results=6):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(keyword)}&hl={hl}&gl={gl}&ceid={ceid}"
    try:
        return feedparser.parse(url).entries[:max_results]
    except:
        return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_arxiv(keyword, max_results=5):
    try:
        query = urllib.parse.quote(keyword)
        url = (f"https://export.arxiv.org/api/query"
               f"?search_query=all:{query}&start=0&max_results={max_results}"
               f"&sortBy=submittedDate&sortOrder=descending")
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries:
            title   = entry.get("title", "").replace("\n", " ").strip()
            summary = entry.get("summary", "")[:400].replace("\n", " ").strip()
            pub     = entry.get("published", "")[:10]
            link    = entry.get("id", "") or entry.get("link", "")
            authors_raw = entry.get("authors", [])
            authors = ", ".join(a.get("name","") for a in authors_raw[:3]) if authors_raw else entry.get("author","")
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
                bib = pub.get("bib", {})
                results.append({
                    "title":    bib.get("title","No title"),
                    "authors":  bib.get("author","Unknown"),
                    "year":     bib.get("pub_year",""),
                    "journal":  bib.get("venue",""),
                    "abstract": bib.get("abstract",""),
                    "url":      pub.get("pub_url",""),
                })
            except StopIteration:
                break
    except:
        pass
    return results

def build_report(num, ko, en, bg, kw, news_ko, news_en, papers, arxiv):
    today = datetime.now().strftime("%Y-%m-%d")
    kw_str = " / ".join(kw)
    n_news = len(news_ko)+len(news_en); n_p = len(papers)+len(arxiv)

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

    scholar_body="".join([f"\n**[{i}] {p['title']}** ({p['year']}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(papers,1)]) or "(없음)"
    arxiv_body  ="".join([f"\n**[{i}] [{p['title']}]({p['url']})** ({p['published'][:7]}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n" for i,p in enumerate(arxiv,len(papers)+1)]) or "(없음)"
    ko_body ="".join([f"\n**[뉴스]** [{n['title']}]({n['link']})\n> {n['source']} | {n['published']}\n" for n in news_ko])
    en_body ="".join([f"\n**[News]** [{n['title']}]({n['link']})\n> {n['source']} | {n['published']}\n" for n in news_en])

    return f"""# {num}. {ko}
## 연구 분석 보고서

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
{"".join([f'**[뉴스]** [{n["title"]}]({n["link"]})\n> {n["source"]} | {n["published"]}\n\n' for n in news_ko]) or "(국내 뉴스 없음)"}

### 3.2 해외 동향
{"".join([f'**[News]** [{n["title"]}]({n["link"]})\n> {n["source"]} | {n["published"]}\n\n' for n in news_en]) or "(해외 뉴스 없음)"}

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

**성능 지표:** RMSE, MAE, 수렴 속도, 노이즈 민감도

---

## 6. 결론 및 향후 연구 방향

- {ko}은(는) BMS 핵심 기능으로 연구 수요 지속 증가
- 칼만 필터 계열 + 데이터 기반 융합 연구 트렌드
- AI/ML 융합, 디지털 트윈, 차세대 배터리 적용이 향후 과제

---

## 참고문헌

{"".join([f'{r}  \n' for r in refs]) or "(없음)"}

---
*Gregory Plett, Battery Management Systems Vol.2 (2015) 기준*
"""

# =====================================================================
# 세션 초기화
# =====================================================================
for k, v in [
    ("page","home"), ("sel_topic_idx", 0),
    ("news_ko",[]),("news_en",[]),("papers",[]),("arxiv",[]),
    ("sel_news",[]),("sel_papers",[]),("sel_arxiv",[]),
    ("report",""),("active_tab","news"),("step",0)
]:
    if k not in st.session_state: st.session_state[k] = v

# =====================================================================
# 상단 네비 (항상 표시)
# =====================================================================
num_collected = len(st.session_state["news_ko"])+len(st.session_state["news_en"])
num_papers    = len(st.session_state["papers"])+len(st.session_state["arxiv"])

st.markdown(f"""
<div class="portal-nav">
    <div class="portal-logo">🔋 <span>BATTERY</span>SIM</div>
    <div class="portal-nav-links">
        <a href="#" class="{'active' if st.session_state['page']=='home' else ''}">HOME</a>
        <a href="#">RESEARCH HUB</a>
        <a href="#">ABOUT</a>
        <span style="color:#444;font-size:0.75rem;">📰 {num_collected}건 · 📚 {num_papers}편 수집됨</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# HOME — 카드 그리드
# =====================================================================
if st.session_state["page"] == "home":

    # 히어로
    st.markdown("""
    <div class="portal-hero">
        <div class="portal-hero-label">Battery Management Systems · Chapter 2-04</div>
        <div class="portal-hero-title">BATTERY HEALTH<br>ESTIMATION HUB</div>
        <div class="portal-hero-sub">배터리 건강 추정 24개 핵심 주제 · 최신 논문 · 뉴스 · 전문 보고서 자동 생성</div>
        <div class="portal-hero-stats">
            <div class="portal-stat"><div class="portal-stat-num">24</div><div class="portal-stat-label">Research Topics</div></div>
            <div class="portal-stat"><div class="portal-stat-num">2</div><div class="portal-stat-label">News Sources</div></div>
            <div class="portal-stat"><div class="portal-stat-num">2</div><div class="portal-stat-label">Paper DBs</div></div>
            <div class="portal-stat"><div class="portal-stat-num">4</div><div class="portal-stat-label">Languages</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 섹션 헤더
    st.markdown("""
    <div class="section-header">
        <div class="section-header-line"></div>
        <div class="section-header-title">ALL RESEARCH TOPICS</div>
        <div class="section-header-count">총 24개 주제 · 주제를 클릭하면 자료 수집을 시작합니다</div>
    </div>
    """, unsafe_allow_html=True)

    # 카드 그리드 — 4열 × 6행
    cols_per_row = 4
    for row_start in range(0, len(TOPICS), cols_per_row):
        row_topics = TOPICS[row_start:row_start+cols_per_row]
        cols = st.columns(cols_per_row, gap="small")
        for col_idx, (col, topic) in enumerate(zip(cols, row_topics)):
            t_idx = row_start + col_idx
            num, ko, en, desc, kw = topic
            color = THUMB_COLORS[t_idx % len(THUMB_COLORS)]
            icon_map = {
                "01":"⚡","02":"🔬","03":"🔋","04":"📊","05":"💻","06":"📈",
                "07":"🎯","08":"🔄","09":"🌀","10":"🔗","11":"⚙️","12":"📐",
                "13":"⚖️","14":"📏","15":"✅","16":"📉","17":"🔧","18":"💡",
                "19":"🖥️","20":"🚗","21":"⚡","22":"💬","23":"🔭","24":"🌊",
            }
            icon = icon_map.get(num, "🔋")
            with col:
                st.markdown(f"""
                <div class="topic-card">
                    <div class="card-thumb-inner" style="background:{color}; height:160px;">
                        <div style="font-size:3.5rem; opacity:0.15; font-family:'Bebas Neue',sans-serif; letter-spacing:4px; color:white;">{icon}</div>
                        <div class="card-num-badge">{num}</div>
                        <div class="card-overlay"></div>
                    </div>
                    <div class="card-body">
                        <div class="card-round-label">TOPIC {num}</div>
                        <div class="card-title">{ko}</div>
                        <div class="card-desc">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"VIEW DETAILS →", key=f"card_{t_idx}", use_container_width=True):
                    st.session_state["page"] = "detail"
                    st.session_state["sel_topic_idx"] = t_idx
                    # 주제 바뀌면 데이터 초기화
                    for k2 in ["news_ko","news_en","papers","arxiv","sel_news","sel_papers","sel_arxiv","report"]:
                        st.session_state[k2] = [] if k2 != "report" else ""
                    st.session_state["step"] = 0
                    st.session_state["active_tab"] = "news"
                    st.rerun()

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

# =====================================================================
# DETAIL — 개별 주제 뷰
# =====================================================================
else:
    t_idx = st.session_state["sel_topic_idx"]
    num, ko, en, bg, kw = TOPICS[t_idx]
    color = THUMB_COLORS[t_idx % len(THUMB_COLORS)]

    # 히어로
    st.markdown(f"""
    <div class="detail-hero" data-num="{num}">
        <div class="detail-label">BATTERY RESEARCH HUB · TOPIC {num}</div>
        <div class="detail-title">{ko}</div>
        <div class="detail-en">{en}</div>
        <div style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
            {"".join([f'<span style="background:rgba(255,255,255,0.08);color:#aaa;padding:3px 10px;border-radius:2px;font-size:0.72rem;">{k}</span>' for k in kw])}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 뒤로가기 버튼
    back_col, _ = st.columns([2, 8])
    with back_col:
        if st.button("← HOME으로 돌아가기", key="back_btn"):
            st.session_state["page"] = "home"
            st.rerun()

    st.markdown("<hr style='margin:0;'>", unsafe_allow_html=True)

    # 메인 + 사이드 레이아웃
    main_col, side_col = st.columns([7, 3], gap="medium")

    # ── 사이드바 ──────────────────────────
    with side_col:
        st.markdown(f"""
        <div class="side-widget">
            <div class="side-widget-title">KEYWORDS</div>
            {"".join([f'<span class="kw-tag">{k}</span>' for k in kw])}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="side-widget">
            <div class="side-widget-title">TOPIC INFO</div>
            <div style="font-size:0.82rem; color:#444; line-height:1.7;">{bg}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="side-widget">
            <div class="side-widget-title">SEARCH KEYWORD</div>
            <div style="font-size:0.8rem; color:#1a73e8; font-weight:500; background:#e8f0fe; padding:8px 12px; border-radius:2px;">{en}</div>
        </div>
        """, unsafe_allow_html=True)

        # 진행상태
        step = st.session_state["step"]
        steps = [("뉴스 수집",1),("논문 검색",2),("자료 선택",3),("보고서 생성",4)]
        st.markdown('<div class="side-widget"><div class="side-widget-title">PROGRESS</div>', unsafe_allow_html=True)
        for label, threshold in steps:
            done = step >= threshold
            color_s = "#e8001c" if done else "#ddd"
            icon_s  = "●" if done else "○"
            st.markdown(f"<div style='font-size:0.8rem;color:{color_s};padding:4px 0;border-bottom:1px solid #eee;font-weight:{'700' if done else '400'};'>{icon_s} {label}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 메인 콘텐츠 ──────────────────────
    with main_col:
        # 탭 버튼 (커스텀)
        tab_labels = [
            ("news",   "📡 뉴스 수집"),
            ("papers", "📚 논문 검색"),
            ("select", "✅ 자료 선택"),
            ("report", "📄 보고서"),
            ("save",   "💾 다운로드"),
        ]
        tab_html = '<div class="portal-tabs">'
        for tab_key, tab_label in tab_labels:
            active_cls = "active" if st.session_state["active_tab"] == tab_key else ""
            tab_html += f'<div class="portal-tab {active_cls}" onclick="">{tab_label}</div>'
        tab_html += "</div>"
        st.markdown(tab_html, unsafe_allow_html=True)

        # 탭 전환 버튼 (스트림릿 실제 동작)
        tab_cols = st.columns(len(tab_labels))
        for i, (tk, tl) in enumerate(tab_labels):
            with tab_cols[i]:
                if st.button(tl, key=f"tab_{tk}", use_container_width=True):
                    st.session_state["active_tab"] = tk
                    st.rerun()

        active = st.session_state["active_tab"]

        # ─── 뉴스 탭 ───
        if active == "news":
            st.markdown("**Google News에서 국내·해외 뉴스를 수집합니다.**")
            c1, c2 = st.columns([3, 1])
            with c1:
                run_news = st.button("🔄 뉴스 수집 시작", type="primary", use_container_width=True)
            with c2:
                if st.button("초기화", use_container_width=True):
                    st.session_state["news_ko"] = []; st.session_state["news_en"] = []
                    st.rerun()

            if run_news:
                prog = st.progress(0)
                prog.progress(20)
                raw_ko = fetch_news(ko + " 배터리", "ko", "KR", "KR:ko", 8)
                st.session_state["news_ko"] = [{"title":e.title,"link":e.link,"lang":"ko","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_ko]
                prog.progress(65)
                raw_en = fetch_news(en, "en", "US", "US:en", 8)
                st.session_state["news_en"] = [{"title":e.title,"link":e.link,"lang":"en","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_en]
                prog.progress(100); prog.empty()
                if st.session_state["step"] < 1: st.session_state["step"] = 1
                st.rerun()

            ko_list = st.session_state["news_ko"]
            en_list = st.session_state["news_en"]

            if ko_list or en_list:
                st.success(f"✅ 총 {len(ko_list)+len(en_list)}건 수집 완료")
                all_items = [("🇰🇷", item) for item in ko_list] + [("🌍", item) for item in en_list]
                for idx, (flag, item) in enumerate(all_items, 1):
                    st.markdown(f"""
                    <div class="news-row">
                        <div class="news-row-num">{idx:02d}</div>
                        <div class="news-row-content">
                            <div class="news-row-flag">{flag} {item['source']}</div>
                            <div class="news-row-title"><a href="{item['link']}" target="_blank">{item['title']}</a></div>
                            <div class="news-row-meta">📅 {item['published']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""<div style="text-align:center;padding:50px;color:#aaa;border:2px dashed #ddd;border-radius:4px;margin-top:16px;">
                    <div style="font-size:2rem;margin-bottom:8px;">📰</div>
                    <div>위 버튼을 클릭해 뉴스를 수집하세요</div>
                </div>""", unsafe_allow_html=True)

        # ─── 논문 탭 ───
        elif active == "papers":
            # arXiv
            st.markdown('<div style="background:#fff3e0;border-left:3px solid #f59e0b;padding:8px 14px;margin-bottom:12px;font-size:0.82rem;border-radius:0 4px 4px 0;">💡 arXiv — 무료·차단없음·최신 프리프린트</div>', unsafe_allow_html=True)
            ca1, ca2 = st.columns([3,1])
            with ca1: run_arxiv = st.button("🔍 arXiv 논문 검색", type="primary", use_container_width=True)
            with ca2:
                if st.button("초기화 ", use_container_width=True):
                    st.session_state["arxiv"] = []; st.rerun()

            if run_arxiv:
                with st.spinner("arXiv 검색 중... (최대 10초)"):
                    results = fetch_arxiv(en, 6)
                if results:
                    st.session_state["arxiv"] = results
                    if st.session_state["step"] < 2: st.session_state["step"] = 2
                    st.rerun()
                else:
                    st.error("arXiv 검색 결과 없음. 잠시 후 재시도하세요.")

            arxiv_list = st.session_state["arxiv"]
            if arxiv_list:
                st.success(f"✅ arXiv {len(arxiv_list)}편 수집")
                for p in arxiv_list:
                    abs_t = (p['abstract'][:220]+"...") if len(p['abstract'])>220 else p['abstract']
                    st.markdown(f"""
                    <div class="paper-row">
                        <span class="paper-badge arxiv">arXiv</span>
                        <div class="paper-row-title"><a href="{p['url']}" target="_blank">{p['title']}</a></div>
                        <div class="paper-row-author">👤 {p['authors']} &nbsp;|&nbsp; 📅 {p['published']}</div>
                        <div class="paper-row-abs">{abs_t}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # Scholar
            st.markdown('<div style="background:#fff8e1;border-left:3px solid #f59e0b;padding:8px 14px;margin-bottom:12px;font-size:0.82rem;border-radius:0 4px 4px 0;">⚠️ Google Scholar — 잦은 요청 시 일시 차단될 수 있음</div>', unsafe_allow_html=True)
            cs1, cs2 = st.columns([3,1])
            with cs1: run_scholar = st.button("🔍 Google Scholar 검색", type="primary", use_container_width=True)
            with cs2:
                if st.button("초기화  ", use_container_width=True):
                    st.session_state["papers"] = []; st.rerun()

            if run_scholar:
                with st.spinner("Google Scholar 조회 중... (최대 20초)"):
                    sch = fetch_scholar(en, 4)
                st.session_state["papers"] = sch
                if st.session_state["step"] < 2: st.session_state["step"] = 2
                st.rerun()

            scholar_list = st.session_state["papers"]
            if scholar_list:
                st.success(f"✅ Google Scholar {len(scholar_list)}편 수집")
                for p in scholar_list:
                    abs_t = (p['abstract'][:220]+"...") if len(p['abstract'])>220 else p['abstract']
                    link_h = f"<a href='{p['url']}' target='_blank' style='color:#e8001c;font-size:0.75rem;'>원문 →</a>" if p.get('url') else ""
                    st.markdown(f"""
                    <div class="paper-row">
                        <span class="paper-badge scholar">Scholar</span>
                        <div class="paper-row-title">{p['title']} ({p['year']}) {link_h}</div>
                        <div class="paper-row-author">👤 {p['authors']}{(' | 📔 ' + p['journal']) if p.get('journal') else ''}</div>
                        <div class="paper-row-abs">{abs_t}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # ─── 자료 선택 탭 ───
        elif active == "select":
            all_news   = st.session_state["news_ko"] + st.session_state["news_en"]
            all_arxiv  = st.session_state["arxiv"]
            all_scholar= st.session_state["papers"]

            if not all_news and not all_arxiv and not all_scholar:
                st.info("먼저 뉴스와 논문을 수집해주세요.")
            else:
                sel_n=[]; sel_a=[]; sel_s=[]
                if all_news:
                    st.markdown('<div class="select-box">📰 보고서에 포함할 뉴스를 선택하세요</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    for i, item in enumerate(all_news):
                        flag = "🇰🇷" if item.get("lang")=="ko" else "🌍"
                        with (c1 if i%2==0 else c2):
                            if st.checkbox(f"{flag} {item['title'][:50]}{'...' if len(item['title'])>50 else ''}", key=f"sn_{i}"):
                                sel_n.append(item)

                if all_arxiv or all_scholar:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div class="select-box">📚 보고서에 포함할 논문을 선택하세요</div>', unsafe_allow_html=True)
                    if all_arxiv:
                        st.markdown("<div style='font-size:0.8rem;font-weight:700;color:#e8710a;margin:8px 0 4px;'>arXiv</div>", unsafe_allow_html=True)
                        for i, p in enumerate(all_arxiv):
                            if st.checkbox(f"[arXiv] {p['title'][:55]}{'...' if len(p['title'])>55 else ''} ({p['published'][:7]})", key=f"sa_{i}"):
                                sel_a.append(p)
                    if all_scholar:
                        st.markdown("<div style='font-size:0.8rem;font-weight:700;color:#1a73e8;margin:8px 0 4px;'>Google Scholar</div>", unsafe_allow_html=True)
                        for i, p in enumerate(all_scholar):
                            if st.checkbox(f"[Scholar] {p['title'][:55]}{'...' if len(p['title'])>55 else ''} ({p['year']})", key=f"ss_{i}"):
                                sel_s.append(p)

                st.session_state["sel_news"] = sel_n
                st.session_state["sel_papers"] = sel_s
                st.session_state["sel_arxiv"] = sel_a
                total = len(sel_n)+len(sel_a)+len(sel_s)

                st.markdown("<br>", unsafe_allow_html=True)
                if total > 0:
                    st.success(f"✅ 선택 완료: 뉴스 {len(sel_n)}건 + arXiv {len(sel_a)}편 + Scholar {len(sel_s)}편")
                    if st.session_state["step"] < 3: st.session_state["step"] = 3

                gen = st.button("📄 전문 보고서 자동 생성", type="primary", use_container_width=True, disabled=(total==0))
                if gen and total > 0:
                    with st.spinner("보고서 생성 중..."):
                        time.sleep(0.3)
                        report = build_report(num, ko, en, bg, kw,
                                              st.session_state["sel_news"],
                                              [n for n in st.session_state["sel_news"] if n.get("lang")=="en"],
                                              st.session_state["sel_papers"],
                                              st.session_state["sel_arxiv"])
                        st.session_state["report"] = report
                        if st.session_state["step"] < 4: st.session_state["step"] = 4
                    st.success("✅ 보고서 생성 완료! '보고서' 탭에서 확인하세요.")

        # ─── 보고서 탭 ───
        elif active == "report":
            rpt = st.session_state["report"]
            if rpt:
                st.markdown(rpt)
            else:
                st.markdown("""<div style="text-align:center;padding:50px;color:#aaa;border:2px dashed #ddd;border-radius:4px;">
                    <div style="font-size:2rem;margin-bottom:8px;">📄</div>
                    <div>자료 선택 탭에서 보고서를 생성하세요</div>
                </div>""", unsafe_allow_html=True)

        # ─── 다운로드 탭 ───
        elif active == "save":
            rpt = st.session_state["report"]
            if rpt:
                st.success("✅ 보고서 준비 완료")
                edited = st.text_area("✏️ 최종 수정", value=rpt, height=400, key=f"edit_{num}")
                st.session_state["report"] = edited
                file_base = f"BMS_SOH_{num}_{datetime.now().strftime('%Y%m%d')}"
                c1, c2, c3 = st.columns(3)
                with c1: st.download_button("📄 TXT 다운로드", data=edited, file_name=f"{file_base}.txt", mime="text/plain", type="primary", use_container_width=True)
                with c2: st.download_button("📋 Markdown", data=edited, file_name=f"{file_base}.md", mime="text/markdown", type="primary", use_container_width=True)
                with c3:
                    if st.button("🖨️ 인쇄/PDF", use_container_width=True):
                        st.info("Ctrl+P → PDF로 저장")
            else:
                st.markdown("""<div style="text-align:center;padding:50px;color:#aaa;border:2px dashed #ddd;border-radius:4px;">
                    <div style="font-size:2rem;margin-bottom:8px;">💾</div>
                    <div>보고서를 먼저 생성해주세요</div>
                </div>""", unsafe_allow_html=True)
