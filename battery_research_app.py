import streamlit as st
import feedparser
from scholarly import scholarly
from datetime import datetime
import time

# =====================================================================
# 1. 페이지 설정
# =====================================================================
st.set_page_config(
    page_title="배터리 건강 추정 연구 대시보드",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

/* ── 전체 기본 ── */
html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}
.stApp {
    background-color: #f5f7fa;
    color: #1a1a2e;
}

/* ── 사이드바 ── */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e0e4ea;
}
section[data-testid="stSidebar"] * {
    color: #333 !important;
}

/* ── 탑 네비 스타일 헤더 ── */
.top-nav {
    background: #ffffff;
    border-bottom: 2px solid #e8eaf0;
    padding: 16px 32px;
    margin-bottom: 24px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.top-nav-logo {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1a73e8;
    letter-spacing: -0.5px;
}
.top-nav-sub {
    color: #5f6368;
    font-size: 0.85rem;
    border-left: 1px solid #dadce0;
    padding-left: 16px;
    margin-left: 4px;
}

/* ── 주제 헤더 카드 ── */
.topic-header {
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 20px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.topic-num {
    font-size: 0.78rem;
    color: #1a73e8;
    font-weight: 600;
    background: #e8f0fe;
    border-radius: 20px;
    padding: 2px 12px;
    display: inline-block;
    margin-bottom: 8px;
}
.topic-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #202124;
    margin: 0;
}
.topic-en {
    font-size: 0.85rem;
    color: #5f6368;
    margin-top: 4px;
}

/* ── 흐름 바 ── */
.flow-bar {
    display: flex;
    align-items: center;
    gap: 0;
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.flow-step {
    font-size: 0.82rem;
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 20px;
    color: #9aa0a6;
    background: #f1f3f4;
}
.flow-step.active {
    background: #1a73e8;
    color: #ffffff;
}
.flow-step.done {
    background: #e6f4ea;
    color: #137333;
}
.flow-arrow {
    color: #dadce0;
    font-size: 1rem;
    margin: 0 6px;
}

/* ── 메트릭 카드 ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.metric-card-label {
    font-size: 0.75rem;
    color: #5f6368;
    margin-bottom: 6px;
    font-weight: 500;
}
.metric-card-value {
    font-size: 1.35rem;
    font-weight: 700;
    color: #1a73e8;
}
.metric-card-value.green { color: #137333; }
.metric-card-value.gray  { color: #9aa0a6; }

/* ── 뉴스 카드 ── */
.news-item {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    transition: box-shadow 0.15s, border-color 0.15s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.news-item:hover {
    box-shadow: 0 3px 12px rgba(26,115,232,0.12);
    border-color: #1a73e8;
}
.news-item-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: #1a0dab;
    margin-bottom: 5px;
    line-height: 1.4;
}
.news-item-title a {
    color: #1a0dab;
    text-decoration: none;
}
.news-item-title a:hover { text-decoration: underline; }
.news-item-meta {
    font-size: 0.76rem;
    color: #5f6368;
}

/* ── 논문 카드 ── */
.paper-item {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-left: 4px solid #1a73e8;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin: 8px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.paper-item-title  { font-size: 0.92rem; font-weight: 600; color: #1a0dab; margin-bottom: 4px; }
.paper-item-author { font-size: 0.8rem; color: #5f6368; margin-bottom: 4px; }
.paper-item-venue  { font-size: 0.78rem; color: #137333; margin-bottom: 6px; }
.paper-item-abs    { font-size: 0.82rem; color: #3c4043; line-height: 1.65; }

/* ── 섹션 타이틀 ── */
.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #202124;
    margin: 0 0 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e8eaf0;
}

/* ── 버튼 ── */
.stButton > button {
    background-color: #1a73e8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 8px 20px !important;
    transition: background 0.2s, box-shadow 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #1557b0 !important;
    box-shadow: 0 2px 10px rgba(26,115,232,0.3) !important;
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 10px 10px 0 0;
    border-bottom: 2px solid #e8eaf0;
    padding: 0 10px;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.88rem;
    font-weight: 500;
    color: #5f6368;
    padding: 12px 20px;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: #1a73e8 !important;
    border-bottom-color: #1a73e8 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 24px !important;
}

/* ── textarea ── */
textarea {
    background: #fafafa !important;
    color: #202124 !important;
    border: 1px solid #dadce0 !important;
    border-radius: 8px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── 보고서 미리보기 ── */
.report-preview {
    background: #fafafa;
    border: 1px solid #e0e4ea;
    border-radius: 10px;
    padding: 24px 28px;
    font-size: 0.88rem;
    color: #3c4043;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* ── 상태 박스 ── */
.status-box {
    background: #e8f0fe;
    border: 1px solid #c5d8fc;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 0.85rem;
    color: #1557b0;
    margin-bottom: 8px;
}
.status-box.green {
    background: #e6f4ea;
    border-color: #a8d5b5;
    color: #137333;
}
.status-box.warn {
    background: #fef7e0;
    border-color: #fde68a;
    color: #b45309;
}

/* ── selectbox ── */
div[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 8px !important;
    color: #202124 !important;
}

/* ── 사이드바 진행상태 ── */
.sidebar-step {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0;
    font-size: 0.84rem;
    color: #5f6368;
    border-bottom: 1px solid #f1f3f4;
}
.sidebar-step.done { color: #137333; font-weight: 600; }

/* ── 정보 알림 ── */
.stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 8px !important;
}

/* ── 섹션 컨테이너 ── */
.content-card {
    background: #ffffff;
    border: 1px solid #e0e4ea;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

hr { border-color: #e8eaf0 !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. 데이터
# =====================================================================
TOPICS = [
    ("01", "배터리 건강 추정의 필요성",                 "Battery State of Health Estimation"),
    ("02", "음극 노화",                                  "Lithium-ion Battery Anode Aging"),
    ("03", "양극 노화",                                  "Lithium-ion Battery Cathode Aging"),
    ("04", "R₀에 대한 전압 감도",                        "Battery Internal Resistance Voltage Sensitivity"),
    ("05", "R₀를 추정하기 위한 코드",                    "Battery Internal Resistance Estimation Algorithm"),
    ("06", "전체 용량에 대한 전압의 민감도 Q",           "Battery Voltage Sensitivity Total Capacity"),
    ("07", "칼만 필터를 통한 파라미터 추정",             "Kalman Filter Battery Parameter Estimation"),
    ("08", "EKF 파라미터 추정",                          "Extended Kalman Filter Battery SOH"),
    ("09", "SPKF 파라미터 추정",                         "Sigma-Point Kalman Filter Battery"),
    ("10", "조인트 추정과 듀얼 추정",                    "Joint Dual Estimation Battery State"),
    ("11", "견고성과 속도",                              "Robustness Speed Battery Estimation"),
    ("12", "선형 회귀를 통한 전체 용량의 비편향 추정값", "Unbiased Battery Capacity Linear Regression"),
    ("13", "가중 일반 최소제곱법",                       "Weighted Generalized Least Squares Battery"),
    ("14", "총 가중 최소제곱법",                         "Weighted Total Least Squares Battery"),
    ("15", "모델 적합도의 우수성",                       "Goodness of Fit Battery Equivalent Circuit"),
    ("16", "신뢰 구간",                                  "Confidence Interval Battery Estimation"),
    ("17", "단순화된 총 최소제곱",                       "Simplified Total Least Squares Battery"),
    ("18", "근사 전체 솔루션",                           "Approximate Total Solution Battery"),
    ("19", "방법별 시뮬레이션 코드",                     "Battery SOH Estimation Simulation Code"),
    ("20", "HEV 시뮬레이션 예시",                        "Hybrid Electric Vehicle Battery Simulation"),
    ("21", "EV 시뮬레이션 예시",                         "Electric Vehicle EV Battery Simulation"),
    ("22", "시뮬레이션에 대한 논의",                     "Battery Simulation Discussion Results"),
    ("23", "결론 및 향후 방향",                          "Battery Health Estimation Future Research"),
    ("24", "비선형 칼만 필터 알고리즘",                  "Nonlinear Kalman Filter Algorithm Battery"),
]
TOPIC_DISPLAY = [f"{n}. {k}" for n, k, e in TOPICS]

# =====================================================================
# 3. 함수
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news_en(keyword, max_results=5):
    url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    return feedparser.parse(url).entries[:max_results]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news_ko(keyword, max_results=5):
    url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:max_results]

def fetch_scholar(keyword, max_results=4):
    results = []
    try:
        gen = scholarly.search_pubs(keyword)
        for _ in range(max_results):
            try:
                results.append(next(gen))
            except StopIteration:
                break
    except Exception:
        pass
    return results

def build_report(num, ko, en, news_ko, news_en, papers):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# 연구 분석 보고서: {num}. {ko}",
        f"> 작성일: {today}",
        f"> 영문 키워드: {en}",
        f"> 기준 문헌: Gregory Plett - Battery Management Systems\n",
        "---\n",
        "## 1. 핵심 개념 요약",
        "(검색 결과를 참고하여 이 주제의 핵심 개념과 원리를 서술하세요.)\n",
        "## 2. 국내 최신 뉴스/정보",
    ]
    if news_ko:
        for e in news_ko:
            lines.append(f"- [{e['title']}]({e['link']})  _{e['published']}_")
    else:
        lines.append("- 관련 국내 뉴스 없음")

    lines += ["", "## 3. 해외 최신 뉴스/정보"]
    if news_en:
        for e in news_en:
            lines.append(f"- [{e['title']}]({e['link']})  _{e['published']}_")
    else:
        lines.append("- 관련 해외 뉴스 없음")

    lines += ["", "## 4. 참고문헌 (Google Scholar)"]
    if papers:
        for i, p in enumerate(papers, 1):
            ref = f"[{i}] {p['authors']} ({p['year']}). {p['title']}."
            if p['journal']: ref += f" {p['journal']}."
            if p['url']:     ref += f" {p['url']}"
            lines.append(ref)
    else:
        lines.append("- 검색된 논문 없음")

    lines += ["", "## 5. 분석 및 향후 적용 방안",
              "(검색 결과를 바탕으로 본인의 분석과 적용 계획을 작성하세요.)"]
    return "\n".join(lines)

# =====================================================================
# 4. 세션 초기화
# =====================================================================
for k, v in [("news_ko", []), ("news_en", []), ("papers", []),
              ("report_text", ""), ("step", 0), ("prev_idx", -1)]:
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================================
# 5. 사이드바
# =====================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 12px; border-bottom:1px solid #e8eaf0; margin-bottom:14px;">
        <div style="font-size:1rem; font-weight:700; color:#1a73e8;">🔋 배터리 건강 추정</div>
        <div style="font-size:0.75rem; color:#9aa0a6; margin-top:2px;">2-04 연구 대시보드</div>
    </div>
    """, unsafe_allow_html=True)

    selected_display = st.selectbox("소제목 선택", TOPIC_DISPLAY, label_visibility="collapsed")
    idx = TOPIC_DISPLAY.index(selected_display)
    num, ko, en = TOPICS[idx]

    if st.session_state["prev_idx"] != idx:
        for k in ["news_ko", "news_en", "papers", "report_text"]:
            st.session_state[k] = [] if k != "report_text" else ""
        st.session_state["step"] = 0
        st.session_state["prev_idx"] = idx

    st.markdown(f"""
    <div style="background:#e8f0fe; border-radius:8px; padding:10px 14px; margin:12px 0;">
        <div style="font-size:0.72rem; color:#1557b0; font-weight:600; margin-bottom:3px;">🔑 검색 키워드</div>
        <div style="font-size:0.8rem; color:#1a73e8; font-weight:500; line-height:1.5;">{en}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#5f6368; margin:14px 0 8px;'>진행 상태</div>", unsafe_allow_html=True)
    step = st.session_state["step"]
    for label, threshold in [("① 자료수집", 1), ("② 뉴스/정보", 2), ("③ 참고문헌", 3), ("④ 보고서", 4)]:
        done = step >= threshold
        icon  = "✅" if done else "○"
        color = "#137333" if done else "#9aa0a6"
        weight= "600" if done else "400"
        st.markdown(f"<div style='color:{color}; font-size:0.82rem; font-weight:{weight}; padding:5px 0; border-bottom:1px solid #f1f3f4;'>{icon} {label}</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:#bdc1c6; font-size:0.72rem; margin-top:14px;'>{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)

# =====================================================================
# 6. 상단 네비바
# =====================================================================
st.markdown(f"""
<div class="top-nav">
    <div class="top-nav-logo">🔋 BMS·SOH 연구 대시보드</div>
    <div class="top-nav-sub">배터리 건강 추정 &nbsp;|&nbsp; 2-04 &nbsp;|&nbsp; 자료수집 → 뉴스 → 참고문헌 → 보고서</div>
</div>
""", unsafe_allow_html=True)

# 주제 헤더
st.markdown(f"""
<div class="topic-header">
    <div class="topic-num">Chapter 2-04 &nbsp;·&nbsp; {num}번 주제</div>
    <div class="topic-title">{num}. {ko}</div>
    <div class="topic-en">{en}</div>
</div>
""", unsafe_allow_html=True)

# 흐름 바
step = st.session_state["step"]
def fc(n): return "done" if step > n else ("active" if step == n else "")
st.markdown(f"""
<div class="flow-bar">
    <div class="flow-step {fc(0)}">① 자료수집 시작</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step {fc(1)}">② 최신 뉴스/정보</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step {fc(2)}">③ 참고문헌</div>
    <div class="flow-arrow">→</div>
    <div class="flow-step {fc(3)}">④ 보고서 자동생성</div>
</div>
""", unsafe_allow_html=True)

# 메트릭
news_cnt  = len(st.session_state["news_ko"]) + len(st.session_state["news_en"])
paper_cnt = len(st.session_state["papers"])
has_report= bool(st.session_state["report_text"])

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-card-label">선택 주제</div>
        <div class="metric-card-value">{num}번</div>
    </div>
    <div class="metric-card">
        <div class="metric-card-label">수집 뉴스</div>
        <div class="metric-card-value {'green' if news_cnt else 'gray'}">{news_cnt}건</div>
    </div>
    <div class="metric-card">
        <div class="metric-card-label">수집 논문</div>
        <div class="metric-card-value {'green' if paper_cnt else 'gray'}">{paper_cnt}편</div>
    </div>
    <div class="metric-card">
        <div class="metric-card-label">보고서</div>
        <div class="metric-card-value {'green' if has_report else 'gray'}">{'완성 ✓' if has_report else '대기중'}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# 7. 탭
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📡 ① 자료수집 (뉴스)",
    "📚 ② 참고문헌 (논문)",
    "📝 ③ 보고서 자동생성",
    "💾 ④ 저장 & 다운로드",
])

# ──────────────────────────
# Tab 1 : 뉴스
# ──────────────────────────
with tab1:
    st.markdown('<div class="section-title">📡 최신 뉴스 및 정보 수집</div>', unsafe_allow_html=True)
    st.markdown("Google News에서 **국내(한국어)** 와 **해외(영어)** 뉴스를 동시에 수집합니다.", unsafe_allow_html=False)

    c1, c2, c3 = st.columns([2, 2, 6])
    with c1:
        run_news = st.button("🔄 뉴스 수집 시작", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑️ 초기화", use_container_width=True):
            st.session_state["news_ko"] = []
            st.session_state["news_en"] = []
            st.session_state["step"] = max(0, st.session_state["step"] - 1) if st.session_state["step"] <= 2 else st.session_state["step"]
            st.rerun()

    if run_news:
        prog   = st.progress(0)
        status = st.empty()

        status.info("🇰🇷 국내 뉴스 검색 중...")
        prog.progress(25)
        raw_ko = fetch_news_ko(ko + " 배터리", 5)
        st.session_state["news_ko"] = [
            {"title": e.title, "link": e.link,
             "published": getattr(e, 'published', ''),
             "source": (e.get('source', {}) or {}).get('title', 'Google News')}
            for e in raw_ko
        ]

        status.info("🌍 해외 뉴스 검색 중...")
        prog.progress(75)
        raw_en = fetch_news_en(en, 5)
        st.session_state["news_en"] = [
            {"title": e.title, "link": e.link,
             "published": getattr(e, 'published', ''),
             "source": (e.get('source', {}) or {}).get('title', 'Google News')}
            for e in raw_en
        ]

        prog.progress(100)
        status.empty(); prog.empty()
        if st.session_state["step"] < 2:
            st.session_state["step"] = 2
        st.rerun()

    ko_list = st.session_state["news_ko"]
    en_list = st.session_state["news_en"]

    if ko_list or en_list:
        col_ko, col_en = st.columns(2)
        with col_ko:
            st.markdown(f"<div style='font-size:0.9rem; font-weight:700; color:#202124; margin-bottom:10px;'>🇰🇷 국내 뉴스 ({len(ko_list)}건)</div>", unsafe_allow_html=True)
            if ko_list:
                for item in ko_list:
                    st.markdown(f"""
                    <div class="news-item">
                        <div class="news-item-title"><a href="{item['link']}" target="_blank">{item['title']}</a></div>
                        <div class="news-item-meta">📅 {item['published']} &nbsp;·&nbsp; {item['source']}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("국내 뉴스 없음")

        with col_en:
            st.markdown(f"<div style='font-size:0.9rem; font-weight:700; color:#202124; margin-bottom:10px;'>🌍 해외 뉴스 ({len(en_list)}건)</div>", unsafe_allow_html=True)
            if en_list:
                for item in en_list:
                    st.markdown(f"""
                    <div class="news-item">
                        <div class="news-item-title"><a href="{item['link']}" target="_blank">{item['title']}</a></div>
                        <div class="news-item-meta">📅 {item['published']} &nbsp;·&nbsp; {item['source']}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("해외 뉴스 없음")
    else:
        st.markdown("""
        <div style="text-align:center; padding:40px; color:#9aa0a6;">
            <div style="font-size:2.5rem; margin-bottom:12px;">📰</div>
            <div style="font-size:0.95rem;">위 버튼을 클릭하면 국내·해외 뉴스를 동시에 수집합니다</div>
        </div>""", unsafe_allow_html=True)

# ──────────────────────────
# Tab 2 : 논문
# ──────────────────────────
with tab2:
    st.markdown('<div class="section-title">📚 학술 논문 / 참고문헌 수집</div>', unsafe_allow_html=True)
    st.warning("⚠️ Google Scholar는 잦은 요청 시 일시 차단될 수 있습니다. 결과가 없으면 1~2분 후 재시도하세요.")

    c1, c2, c3 = st.columns([2, 2, 6])
    with c1:
        run_scholar = st.button("🔍 논문 검색 시작", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑️ 초기화 ", use_container_width=True):
            st.session_state["papers"] = []
            st.rerun()

    if run_scholar:
        with st.spinner("Google Scholar 조회 중... (최대 20초 소요)"):
            raw = fetch_scholar(en, 4)
        papers = []
        for pub in raw:
            bib = pub.get('bib', {})
            papers.append({
                "title":    bib.get('title', '제목 없음'),
                "authors":  bib.get('author', '저자 미상'),
                "year":     bib.get('pub_year', ''),
                "journal":  bib.get('venue', ''),
                "abstract": bib.get('abstract', ''),
                "url":      pub.get('pub_url', ''),
            })
        st.session_state["papers"] = papers
        if st.session_state["step"] < 3:
            st.session_state["step"] = 3
        st.rerun()

    papers = st.session_state["papers"]
    if papers:
        st.success(f"✅ 논문 {len(papers)}편 수집 완료")
        for i, p in enumerate(papers, 1):
            abs_text  = (p['abstract'][:280] + "...") if len(p['abstract']) > 280 else p['abstract']
            abs_html  = f"<div class='paper-item-abs'><b>Abstract:</b> {abs_text}</div>" if abs_text else ""
            link_html = f"<a href='{p['url']}' target='_blank' style='color:#1a73e8; font-size:0.8rem; font-weight:600;'>➡️ 원문 보기</a>" if p['url'] else ""
            st.markdown(f"""
            <div class="paper-item">
                <div class="paper-item-title">[{i}] {p['title']} ({p['year']})</div>
                <div class="paper-item-author">👤 {p['authors']}</div>
                {"<div class='paper-item-venue'>📔 " + p['journal'] + "</div>" if p['journal'] else ""}
                {abs_html}
                <div style="margin-top:8px;">{link_html}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:40px; color:#9aa0a6;">
            <div style="font-size:2.5rem; margin-bottom:12px;">📖</div>
            <div style="font-size:0.95rem;">위 버튼을 클릭하면 Google Scholar에서 관련 논문을 검색합니다</div>
        </div>""", unsafe_allow_html=True)

# ──────────────────────────
# Tab 3 : 보고서 자동생성
# ──────────────────────────
with tab3:
    st.markdown('<div class="section-title">📝 보고서 자동 생성 및 편집</div>', unsafe_allow_html=True)

    news_ok   = bool(st.session_state["news_ko"] or st.session_state["news_en"])
    papers_ok = bool(st.session_state["papers"])

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        cls = "green" if news_ok else "warn"
        msg = f"✅ 뉴스 {len(st.session_state['news_ko'])}건(국내) + {len(st.session_state['news_en'])}건(해외) 수집 완료" if news_ok else "⚠️ 뉴스 미수집 → ①탭에서 먼저 수집하세요"
        st.markdown(f'<div class="status-box {cls}">{msg}</div>', unsafe_allow_html=True)
    with col_s2:
        cls = "green" if papers_ok else "warn"
        msg = f"✅ 논문 {len(st.session_state['papers'])}편 수집 완료" if papers_ok else "⚠️ 논문 미수집 → ②탭에서 먼저 수집하세요"
        st.markdown(f'<div class="status-box {cls}">{msg}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_gen, _ = st.columns([3, 7])
    with col_gen:
        if st.button("⚡ 보고서 자동 생성", type="primary",
                     use_container_width=True, disabled=not (news_ok or papers_ok)):
            with st.spinner("수집된 데이터로 보고서를 생성하는 중..."):
                time.sleep(0.4)
                report = build_report(
                    num, ko, en,
                    st.session_state["news_ko"],
                    st.session_state["news_en"],
                    st.session_state["papers"]
                )
                st.session_state["report_text"] = report
                if st.session_state["step"] < 4:
                    st.session_state["step"] = 4
            st.rerun()

    if not (news_ok or papers_ok):
        st.info("뉴스 또는 논문을 먼저 수집해야 보고서를 생성할 수 있습니다.")

    if st.session_state["report_text"]:
        st.markdown("---")
        st.markdown("<div style='font-size:0.9rem; font-weight:700; color:#202124; margin-bottom:8px;'>✏️ 보고서 편집</div>", unsafe_allow_html=True)
        edited = st.text_area(
            "내용을 자유롭게 수정하세요 (마크다운 지원)",
            value=st.session_state["report_text"],
            height=500,
            key=f"editor_{num}"
        )
        st.session_state["report_text"] = edited
        st.markdown("---")
        st.markdown("<div style='font-size:0.9rem; font-weight:700; color:#202124; margin-bottom:10px;'>👁️ 미리보기</div>", unsafe_allow_html=True)
        st.markdown(edited)

# ──────────────────────────
# Tab 4 : 저장 & 다운로드
# ──────────────────────────
with tab4:
    st.markdown('<div class="section-title">💾 저장 및 다운로드</div>', unsafe_allow_html=True)

    report_text = st.session_state["report_text"]
    if report_text:
        st.success("✅ 보고서가 준비되었습니다. 원하는 형식으로 다운로드하세요.")
        st.markdown("<br>", unsafe_allow_html=True)

        file_base = f"BMS_SOH_{num}_{datetime.now().strftime('%Y%m%d')}"
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 TXT 다운로드", data=report_text,
                               file_name=f"{file_base}.txt", mime="text/plain",
                               type="primary", use_container_width=True)
        with c2:
            st.download_button("📋 Markdown 다운로드", data=report_text,
                               file_name=f"{file_base}.md", mime="text/markdown",
                               type="primary", use_container_width=True)
        with c3:
            if st.button("🖨️ 인쇄 / PDF 저장", use_container_width=True):
                st.info("브라우저에서 Ctrl+P → PDF로 저장하세요.")

        st.markdown("---")
        st.markdown("<div style='font-size:0.9rem; font-weight:700; color:#202124; margin-bottom:10px;'>📋 보고서 전문</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="report-preview">{report_text}</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center; padding:50px; color:#9aa0a6;">
            <div style="font-size:2.5rem; margin-bottom:14px;">📋</div>
            <div style="font-size:1rem; font-weight:600; color:#5f6368; margin-bottom:8px;">아직 보고서가 없습니다</div>
            <div style="font-size:0.88rem;">① 뉴스 수집 → ② 논문 검색 → ③ 보고서 생성 순서로 진행해주세요</div>
        </div>""", unsafe_allow_html=True)
