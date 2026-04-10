import streamlit as st
import feedparser
from scholarly import scholarly
from datetime import datetime
import time
import re

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

html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.stApp { background-color: #f5f7fa; color: #1a1a2e; }

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e0e4ea;
}

.top-nav {
    background: #ffffff; border-bottom: 2px solid #e8eaf0;
    padding: 16px 32px; margin-bottom: 20px; border-radius: 12px;
    display: flex; align-items: center; gap: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.top-nav-logo { font-size: 1.5rem; font-weight: 800; color: #1a73e8; letter-spacing: -0.5px; }
.top-nav-sub  { color: #5f6368; font-size: 0.85rem; border-left: 1px solid #dadce0; padding-left: 16px; }

.topic-header {
    background: #ffffff; border: 1px solid #e0e4ea; border-radius: 12px;
    padding: 20px 28px; margin-bottom: 16px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.topic-num   { font-size: 0.78rem; color: #1a73e8; font-weight: 600; background: #e8f0fe; border-radius: 20px; padding: 2px 12px; display: inline-block; margin-bottom: 8px; }
.topic-title { font-size: 1.5rem; font-weight: 700; color: #202124; margin: 0; }
.topic-en    { font-size: 0.85rem; color: #5f6368; margin-top: 4px; }

.flow-bar { display: flex; align-items: center; background: #ffffff; border: 1px solid #e0e4ea; border-radius: 10px; padding: 12px 20px; margin-bottom: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.flow-step { font-size: 0.82rem; font-weight: 600; padding: 6px 16px; border-radius: 20px; color: #9aa0a6; background: #f1f3f4; }
.flow-step.active { background: #1a73e8; color: #ffffff; }
.flow-step.done   { background: #e6f4ea; color: #137333; }
.flow-arrow { color: #dadce0; font-size: 1rem; margin: 0 6px; }

.metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 16px; }
.metric-card { background: #ffffff; border: 1px solid #e0e4ea; border-radius: 12px; padding: 16px 18px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
.metric-card-label { font-size: 0.74rem; color: #5f6368; margin-bottom: 5px; font-weight: 500; }
.metric-card-value { font-size: 1.2rem; font-weight: 700; color: #1a73e8; }
.metric-card-value.green { color: #137333; }
.metric-card-value.gray  { color: #9aa0a6; }

.news-item { background: #ffffff; border: 1px solid #e8eaf0; border-radius: 10px; padding: 12px 16px; margin: 6px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.04); transition: box-shadow 0.15s, border-color 0.15s; }
.news-item:hover { box-shadow: 0 3px 12px rgba(26,115,232,0.12); border-color: #1a73e8; }
.news-item-title { font-size: 0.9rem; font-weight: 600; color: #1a0dab; margin-bottom: 4px; line-height: 1.4; }
.news-item-title a { color: #1a0dab; text-decoration: none; }
.news-item-title a:hover { text-decoration: underline; }
.news-item-meta  { font-size: 0.75rem; color: #5f6368; }

.paper-item { background: #ffffff; border: 1px solid #e8eaf0; border-left: 4px solid #1a73e8; border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 8px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.paper-item-title  { font-size: 0.9rem; font-weight: 600; color: #1a0dab; margin-bottom: 4px; }
.paper-item-author { font-size: 0.78rem; color: #5f6368; margin-bottom: 3px; }
.paper-item-venue  { font-size: 0.76rem; color: #137333; margin-bottom: 6px; }
.paper-item-abs    { font-size: 0.81rem; color: #3c4043; line-height: 1.65; }

.select-header { background: #e8f0fe; border: 1px solid #c5d8fc; border-radius: 8px; padding: 10px 16px; margin-bottom: 12px; font-size: 0.85rem; color: #1557b0; font-weight: 600; }
.section-title { font-size: 1.05rem; font-weight: 700; color: #202124; margin: 0 0 14px; padding-bottom: 10px; border-bottom: 2px solid #e8eaf0; }

/* 보고서 전문 스타일 */
.report-wrap {
    background: #ffffff; border: 1px solid #e0e4ea; border-radius: 14px;
    padding: 48px 56px; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    max-width: 860px; margin: 0 auto;
}
.report-doctitle {
    font-size: 1.45rem; font-weight: 800; color: #1a73e8;
    text-align: center; margin-bottom: 6px; line-height: 1.4;
}
.report-subtitle {
    font-size: 0.88rem; color: #5f6368; text-align: center; margin-bottom: 4px;
}
.report-meta {
    font-size: 0.8rem; color: #9aa0a6; text-align: center;
    border-bottom: 2px solid #e8eaf0; padding-bottom: 20px; margin-bottom: 28px;
}
.report-abstract {
    background: #f8f9fa; border-left: 4px solid #1a73e8;
    border-radius: 0 8px 8px 0; padding: 16px 20px; margin-bottom: 28px;
    font-size: 0.88rem; color: #3c4043; line-height: 1.8;
}
.report-abstract-title { font-size: 0.78rem; font-weight: 700; color: #1a73e8; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.report-h2 { font-size: 1.05rem; font-weight: 700; color: #202124; margin: 28px 0 12px; padding-left: 12px; border-left: 4px solid #1a73e8; }
.report-h3 { font-size: 0.92rem; font-weight: 700; color: #3c4043; margin: 16px 0 8px; }
.report-p  { font-size: 0.88rem; color: #3c4043; line-height: 1.9; margin-bottom: 10px; }
.report-news-item { background: #f8f9fa; border: 1px solid #e8eaf0; border-radius: 8px; padding: 12px 16px; margin: 8px 0; }
.report-news-title { font-size: 0.88rem; font-weight: 600; color: #1a0dab; margin-bottom: 4px; }
.report-news-meta  { font-size: 0.76rem; color: #5f6368; }
.report-paper-item { background: #f8f9fa; border: 1px solid #e8eaf0; border-left: 3px solid #1a73e8; border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 8px 0; }
.report-paper-title  { font-size: 0.88rem; font-weight: 600; color: #202124; margin-bottom: 4px; }
.report-paper-author { font-size: 0.78rem; color: #5f6368; margin-bottom: 4px; }
.report-paper-abs    { font-size: 0.82rem; color: #3c4043; line-height: 1.7; }
.report-ref { font-size: 0.82rem; color: #3c4043; line-height: 1.7; padding: 6px 0; border-bottom: 1px solid #f1f3f4; }
.report-keyword { display: inline-block; background: #e8f0fe; color: #1557b0; border-radius: 4px; padding: 2px 8px; font-size: 0.76rem; font-weight: 500; margin: 2px; }
.report-divider { border: none; border-top: 1px solid #e8eaf0; margin: 24px 0; }

.status-box       { background: #e8f0fe; border: 1px solid #c5d8fc; border-radius: 8px; padding: 10px 16px; font-size: 0.84rem; color: #1557b0; margin-bottom: 8px; }
.status-box.green { background: #e6f4ea; border-color: #a8d5b5; color: #137333; }
.status-box.warn  { background: #fef7e0; border-color: #fde68a; color: #b45309; }

.stButton > button { background-color: #1a73e8 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; font-family: 'Noto Sans KR', sans-serif !important; font-weight: 600 !important; font-size: 0.88rem !important; transition: background 0.2s !important; width: 100% !important; }
.stButton > button:hover { background-color: #1557b0 !important; box-shadow: 0 2px 10px rgba(26,115,232,0.3) !important; }

.stTabs [data-baseweb="tab-list"] { background: #ffffff; border-radius: 10px 10px 0 0; border-bottom: 2px solid #e8eaf0; padding: 0 10px; }
.stTabs [data-baseweb="tab"] { font-family: 'Noto Sans KR', sans-serif; font-size: 0.88rem; font-weight: 500; color: #5f6368; padding: 12px 20px; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.stTabs [aria-selected="true"] { color: #1a73e8 !important; border-bottom-color: #1a73e8 !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-panel"] { background: #ffffff; border: 1px solid #e8eaf0; border-top: none; border-radius: 0 0 10px 10px; padding: 24px !important; }

textarea { background: #fafafa !important; color: #202124 !important; border: 1px solid #dadce0 !important; border-radius: 8px !important; }
hr { border-color: #e8eaf0 !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. 주제 데이터 (배경 지식 포함)
# =====================================================================
TOPICS = [
    ("01", "배터리 건강 추정의 필요성", "Battery State of Health Estimation",
     "배터리 건강 상태(SOH, State of Health)는 배터리의 현재 용량을 초기 용량 대비 비율로 나타내며, 전기차·에너지 저장 시스템의 안전성과 성능 관리에 핵심적인 역할을 한다. SOH 추정은 과충전·과방전 방지, 잔여 수명 예측, 배터리 교체 시점 결정에 활용된다.",
     ["SOH (State of Health)", "배터리 열화", "잔여 유용 수명 (RUL)", "전기차 (EV)", "BMS (Battery Management System)"]),

    ("02", "음극 노화", "Lithium-ion Battery Anode Aging",
     "음극(주로 흑연)의 노화는 리튬 도금(Li plating), SEI(고체 전해질 계면) 성장, 구조적 균열 등으로 발생한다. 이는 가역 용량 손실과 내부 저항 증가를 초래하며, 배터리 수명 단축의 주요 원인이다.",
     ["SEI (Solid Electrolyte Interphase)", "리튬 도금 (Li Plating)", "흑연 음극", "용량 손실", "사이클 열화"]),

    ("03", "양극 노화", "Lithium-ion Battery Cathode Aging",
     "양극 노화는 구조적 상변이, 전이금속 용해, 입자 균열 등으로 발생한다. NMC, LFP 등 양극 소재별로 열화 메커니즘이 다르며, 고온 환경에서 가속화된다.",
     ["양극 소재 (NMC/LFP/NCA)", "구조적 열화", "전이금속 용해", "상변이", "캘린더 노화"]),

    ("04", "R₀에 대한 전압 감도", "Battery Internal Resistance Voltage Sensitivity",
     "내부 저항 R₀는 배터리 전압 강하의 주요 원인으로, SOH와 밀접한 상관관계를 가진다. 전압 감도 분석을 통해 R₀ 변화를 추적하면 배터리 열화 진단이 가능하다.",
     ["내부 저항 (R₀)", "전압 강하", "등가 회로 모델", "임피던스", "열화 진단"]),

    ("05", "R₀를 추정하기 위한 코드", "Battery Internal Resistance Estimation Algorithm",
     "전류 펄스 응답, 전기화학 임피던스 분광법(EIS), 최소제곱법 등을 활용하여 R₀를 실시간으로 추정한다. Python·MATLAB 기반 알고리즘이 주로 사용된다.",
     ["최소제곱법", "EIS", "전류 펄스", "실시간 추정", "Python 알고리즘"]),

    ("06", "전체 용량에 대한 전압의 민감도 Q", "Battery Voltage Sensitivity Total Capacity",
     "전체 용량 Q는 배터리 SOH 추정의 핵심 파라미터로, OCV-SOC 곡선의 기울기 변화를 통해 추정할 수 있다. 용량 감소는 활물질 손실과 직접적으로 연결된다.",
     ["전체 용량 (Q)", "OCV-SOC 곡선", "활물질 손실", "쿨롱 카운팅", "용량 추정"]),

    ("07", "칼만 필터를 통한 파라미터 추정", "Kalman Filter Battery Parameter Estimation",
     "칼만 필터(KF)는 노이즈가 있는 측정값에서 배터리 상태변수를 최적으로 추정하는 재귀적 알고리즘이다. 선형 시스템에 적합하며 SOC·SOH 동시 추정에 널리 활용된다.",
     ["칼만 필터 (KF)", "상태 추정", "공분산", "예측-수정", "재귀 알고리즘"]),

    ("08", "EKF 파라미터 추정", "Extended Kalman Filter Battery SOH",
     "확장 칼만 필터(EKF)는 비선형 배터리 모델에 칼만 필터를 적용하기 위해 야코비안(Jacobian) 행렬로 선형화하는 방법이다. SOC와 R₀의 동시 추정에 효과적이다.",
     ["EKF (확장 칼만 필터)", "야코비안 행렬", "비선형 시스템", "SOC 추정", "선형화"]),

    ("09", "SPKF 파라미터 추정", "Sigma-Point Kalman Filter Battery",
     "시그마 포인트 칼만 필터(SPKF)는 UKF(무향 칼만 필터)라고도 하며, 비선형 변환을 시그마 포인트의 통계적 전파로 근사한다. EKF보다 정확도가 높고 야코비안 계산이 불필요하다.",
     ["SPKF/UKF", "시그마 포인트", "무향 변환", "비선형 추정", "통계적 근사"]),

    ("10", "조인트 추정과 듀얼 추정", "Joint Dual Estimation Battery State",
     "조인트 추정은 상태변수와 파라미터를 단일 확장 상태벡터로 동시 추정하고, 듀얼 추정은 두 개의 분리된 필터로 각각 추정하는 방법이다. 두 방법 모두 SOC와 SOH의 동시 추정에 활용된다.",
     ["조인트 추정", "듀얼 추정", "상태-파라미터 동시 추정", "이중 필터", "적응형 추정"]),

    ("11", "견고성과 속도", "Robustness Speed Battery Estimation",
     "추정 알고리즘의 견고성은 센서 노이즈, 모델 불확실성, 초기값 오차에 대한 민감도를 의미한다. 계산 속도는 실시간 BMS 적용을 위한 핵심 요소이며, 두 특성 간 트레이드오프가 존재한다.",
     ["견고성 (Robustness)", "계산 복잡도", "실시간 처리", "노이즈 민감도", "수렴 속도"]),

    ("12", "선형 회귀를 통한 전체 용량의 비편향 추정값", "Unbiased Battery Capacity Linear Regression",
     "선형 회귀를 통해 측정 데이터에서 배터리 전체 용량을 편향 없이 추정한다. 누적 전류(쿨롱 카운팅) 데이터와 SOC 변화량의 관계를 활용하며, 최소제곱법이 기본 도구로 사용된다.",
     ["비편향 추정", "선형 회귀", "쿨롱 카운팅", "최소제곱법 (OLS)", "용량 추정"]),

    ("13", "가중 일반 최소제곱법", "Weighted Generalized Least Squares Battery",
     "가중 일반 최소제곱법(WGLS)은 측정 노이즈의 분산이 불균일할 때 각 데이터 포인트에 가중치를 부여하여 추정 정확도를 향상시키는 방법이다.",
     ["WGLS", "이분산성", "가중 행렬", "최적 추정", "노이즈 모델링"]),

    ("14", "총 가중 최소제곱법", "Weighted Total Least Squares Battery",
     "총 가중 최소제곱법(TWLS)은 입력과 출력 모두에 노이즈가 존재하는 오차변수모델(EIV)에 적합한 추정 방법으로, 배터리 용량 추정의 정확도를 개선한다.",
     ["TWLS", "오차변수모델 (EIV)", "양방향 노이즈", "총 최소제곱", "용량 추정"]),

    ("15", "모델 적합도의 우수성", "Goodness of Fit Battery Equivalent Circuit",
     "등가 회로 모델의 적합도는 RMSE, R², AIC 등의 지표로 평가한다. 좋은 적합도는 정확한 SOH 추정의 전제 조건이며, 과적합을 방지하기 위한 모델 복잡도 선택이 중요하다.",
     ["RMSE", "R² (결정계수)", "AIC/BIC", "등가 회로 모델", "모델 검증"]),

    ("16", "신뢰 구간", "Confidence Interval Battery Estimation",
     "추정값의 신뢰 구간은 추정 불확실성을 정량화하며, 배터리 안전 마진 설정에 활용된다. 칼만 필터의 공분산 행렬에서 직접 신뢰 구간을 도출할 수 있다.",
     ["신뢰 구간", "불확실성 정량화", "공분산", "오차 한계", "통계적 추론"]),

    ("17", "단순화된 총 최소제곱", "Simplified Total Least Squares Battery",
     "단순화된 TLS는 계산 복잡도를 줄이면서도 EIV 모델의 장점을 유지하는 방법이다. 실시간 BMS 적용을 위해 연산량을 최소화한 근사 알고리즘이 개발되었다.",
     ["단순화된 TLS", "근사 알고리즘", "계산 효율", "실시간 BMS", "EIV 모델"]),

    ("18", "근사 전체 솔루션", "Approximate Total Solution Battery",
     "근사 전체 솔루션은 복잡한 최적화 문제를 닫힌 형태(closed-form)의 해로 근사하여 계산 효율을 높이는 방법이다. 배터리 파라미터 추정에서 정확도와 속도의 균형을 맞춘다.",
     ["근사 해 (Closed-form)", "계산 최적화", "파라미터 추정", "수치 안정성", "실시간 구현"]),

    ("19", "방법별 시뮬레이션 코드", "Battery SOH Estimation Simulation Code",
     "EKF, SPKF, 최소제곱법 등 다양한 SOH 추정 방법의 성능을 Python·MATLAB 시뮬레이션으로 비교한다. 동일한 배터리 데이터셋에서 각 방법의 정확도, 수렴 속도, 계산량을 평가한다.",
     ["시뮬레이션", "Python/MATLAB", "알고리즘 비교", "성능 평가", "배터리 데이터셋"]),

    ("20", "HEV 시뮬레이션 예시", "Hybrid Electric Vehicle Battery Simulation",
     "하이브리드 전기차(HEV)의 배터리는 빈번한 충방전과 높은 전류 변동이 특징이다. HEV 주행 사이클(UDDS, HWFET 등)을 적용한 SOH 추정 시뮬레이션으로 실제 환경 성능을 검증한다.",
     ["HEV (하이브리드 전기차)", "주행 사이클", "UDDS/HWFET", "동적 부하", "SOH 추정"]),

    ("21", "EV 시뮬레이션 예시", "Electric Vehicle EV Battery Simulation",
     "순수 전기차(EV)는 1회 충전 주행거리와 배터리 수명이 상품성의 핵심이다. WLTP, EPA 등 표준 주행 사이클에서의 SOH 추정 정확도와 에너지 관리 전략을 시뮬레이션으로 분석한다.",
     ["EV (순수 전기차)", "주행거리 (Range)", "WLTP/EPA", "에너지 관리", "충전 전략"]),

    ("22", "시뮬레이션에 대한 논의", "Battery Simulation Discussion Results",
     "다양한 추정 방법의 시뮬레이션 결과를 비교·분석하고, 실차 적용 시 고려할 사항(센서 정밀도, 온도 영향, 계산 자원)을 논의한다. 시뮬레이션과 실험 결과의 차이도 검토한다.",
     ["결과 비교", "실차 적용", "온도 영향", "센서 오차", "검증 및 시험"]),

    ("23", "결론 및 향후 방향", "Battery Health Estimation Future Research",
     "배터리 SOH 추정 기술의 현재 한계를 정리하고, 머신러닝 기반 추정, 디지털 트윈, 클라우드 BMS 등 미래 연구 방향을 제시한다. 고체 배터리 등 차세대 배터리에 대한 적용 가능성도 논의한다.",
     ["머신러닝 SOH 추정", "디지털 트윈", "차세대 배터리", "클라우드 BMS", "연구 과제"]),

    ("24", "비선형 칼만 필터 알고리즘", "Nonlinear Kalman Filter Algorithm Battery",
     "EKF, UKF, CKF(Cubature KF), PF(파티클 필터) 등 비선형 칼만 필터 계열 알고리즘의 이론적 배경과 배터리 SOH 추정에의 적용을 체계적으로 정리한다.",
     ["비선형 칼만 필터", "UKF/CKF", "파티클 필터", "비선형 추정", "알고리즘 비교"]),
]

TOPIC_MAP = {f"{n}. {k}": (n, k, e, bg, kw) for n, k, e, bg, kw in TOPICS}
TOPIC_DISPLAY = [f"{n}. {k}" for n, k, e, bg, kw in TOPICS]

# =====================================================================
# 3. 함수
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news_en(keyword, max_results=6):
    url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    return feedparser.parse(url).entries[:max_results]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_news_ko(keyword, max_results=6):
    url = f"https://news.google.com/rss/search?q={keyword.replace(' ', '+')}&hl=ko&gl=KR&ceid=KR:ko"
    return feedparser.parse(url).entries[:max_results]

def fetch_scholar(keyword, max_results=5):
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

def generate_structured_report(num, ko, en, bg, keywords, sel_news, sel_papers):
    """선택한 뉴스·논문을 전문 학술 보고서 형식으로 자동 구조화"""
    today = datetime.now().strftime("%Y년 %m월 %d일")
    kw_list = " / ".join(keywords)

    # ── 초록 자동 생성
    abstract = f"{ko}은(는) 배터리 건강 상태(SOH) 추정 분야의 핵심 주제 중 하나이다. {bg} 본 보고서는 최신 뉴스·동향 자료 {len(sel_news)}건과 학술 논문 {len(sel_papers)}편을 수집·분석하여 해당 주제의 현황과 연구 동향을 체계적으로 정리한다."

    # ── 국내/해외 뉴스 분리
    news_ko_sel = [n for n in sel_news if n.get("lang") == "ko"]
    news_en_sel = [n for n in sel_news if n.get("lang") == "en"]

    # ── 논문 인용 번호
    ref_list = []
    for i, p in enumerate(sel_papers, 1):
        ref = f"[{i}] {p['authors']} ({p['year']}). {p['title']}."
        if p['journal']: ref += f" {p['journal']}."
        if p['url']:     ref += f" Retrieved from {p['url']}"
        ref_list.append(ref)

    # ── 뉴스 인용 번호 (논문 이어서)
    news_ref_start = len(sel_papers) + 1
    news_refs = []
    for i, n in enumerate(sel_news, news_ref_start):
        news_refs.append(f"[{i}] {n['title']}. {n['source']} ({n['published']}). {n['link']}")

    all_refs = ref_list + news_refs

    # ── 기술 분석 텍스트
    paper_analysis = ""
    if sel_papers:
        for i, p in enumerate(sel_papers, 1):
            abs_text = p['abstract'][:200] + "..." if len(p['abstract']) > 200 else p['abstract']
            paper_analysis += f"\n**{p['title']}** ({p['year']}) [{i}]"
            if p['authors']:
                paper_analysis += f" — {p['authors'][:60]}"
            if abs_text:
                paper_analysis += f"\n\n> {abs_text}\n"
    else:
        paper_analysis = "\n(수집된 논문 없음 — ②탭에서 논문을 검색하세요)\n"

    # ── 최종 마크다운 보고서
    report = f"""# {num}. {ko}
## 연구 분석 보고서

---
**작성일:** {today} &nbsp;|&nbsp; **키워드:** {kw_list}  
**기준 문헌:** Gregory Plett - *Battery Management Systems: Equivalent-Circuit Methods*  
**수집 자료:** 뉴스 {len(sel_news)}건 · 논문 {len(sel_papers)}편

---

## 초록 (Abstract)

{abstract}

**주요 키워드:** {kw_list}

---

## 1. 서론 (Introduction)

### 1.1 연구 배경 및 필요성

{bg}

배터리 에너지 저장 시스템(BESS)의 급속한 보급과 전기차 시장의 성장에 따라, 배터리의 건강 상태를 정확히 파악하는 것은 안전성 확보, 수명 예측, 운용 최적화 측면에서 필수적인 과제가 되고 있다. 특히 {ko} 분야는 배터리 관리 시스템(BMS)의 핵심 기능 중 하나로, 최근 연구가 활발히 진행되고 있다.

### 1.2 연구 목적

본 보고서는 {ko}({en})에 관한 최신 연구 동향과 기술 현황을 체계적으로 분석하고, 관련 핵심 개념 및 방법론을 정리하는 것을 목적으로 한다.

### 1.3 보고서 구성

본 보고서는 이론적 배경(2장), 최신 기술 동향(3장), 핵심 선행 연구 검토(4장), 기술적 분석 및 고찰(5장), 결론(6장) 순으로 구성된다.

---

## 2. 이론적 배경 (Theoretical Background)

### 2.1 핵심 개념 정의

{bg}

배터리의 건강 상태 추정은 다음의 핵심 파라미터를 중심으로 이루어진다:

- **SOH (State of Health):** 현재 최대 용량 / 초기 정격 용량 × 100%
- **SOC (State of Charge):** 현재 잔여 용량 / 현재 최대 용량 × 100%
- **내부 저항 (R₀):** 배터리 열화의 직접적 지표

### 2.2 관련 핵심 개념

| 개념 | 설명 |
|------|------|
{"".join([f"| **{kw}** | {ko} 분야의 핵심 요소 |\n" for kw in keywords])}

### 2.3 기존 연구 동향 요약

{ko} 분야에서는 전통적인 물리 기반 모델부터 데이터 기반 머신러닝 방법까지 다양한 접근법이 연구되고 있다. 등가 회로 모델(ECM)은 구현 용이성과 실시간 처리 능력으로 BMS에 널리 채택되며, 칼만 필터 계열 알고리즘이 파라미터 추정에 주로 활용된다.

---

## 3. 최신 기술 동향 분석 (Recent Trends)

### 3.1 국내 동향

{"아래는 수집된 국내 최신 뉴스 및 기술 동향이다." if news_ko_sel else "이번 수집에서 국내 관련 뉴스는 확인되지 않았다."}

{"".join([f'''
**[뉴스 {i+1}]** [{n["title"]}]({n["link"]})  
> 출처: {n["source"]} | 날짜: {n["published"]}

''' for i, n in enumerate(news_ko_sel)])}

### 3.2 해외 동향

{"아래는 수집된 해외 최신 연구 동향 및 산업 뉴스이다." if news_en_sel else "이번 수집에서 해외 관련 뉴스는 확인되지 않았다."}

{"".join([f'''
**[뉴스 {i+1}]** [{n["title"]}]({n["link"]})  
> 출처: {n["source"]} | 날짜: {n["published"]}

''' for i, n in enumerate(news_en_sel)])}

---

## 4. 핵심 선행 연구 검토 (Literature Review)

본 장에서는 수집된 학술 논문 {len(sel_papers)}편을 분석하여 {ko} 분야의 주요 연구 성과를 정리한다.

{paper_analysis if sel_papers else "(②탭에서 논문을 검색하고 선택하면 이 섹션이 자동으로 채워집니다)"}

---

## 5. 기술적 분석 및 고찰 (Technical Analysis)

### 5.1 주요 연구 특징 비교

수집된 자료를 바탕으로 {ko} 관련 주요 기술적 접근법을 비교하면 다음과 같다:

| 구분 | 주요 방법 | 특징 | 적용 분야 |
|------|----------|------|----------|
| 모델 기반 | 등가 회로 모델 | 구현 용이, 실시간 처리 | BMS 내장 |
| 필터 기반 | EKF / UKF | 높은 정확도, 노이즈 강인성 | 전기차 |
| 데이터 기반 | 머신러닝 / 딥러닝 | 대용량 데이터 필요 | 클라우드 BMS |

### 5.2 성능 지표 및 평가 기준

- **정확도:** RMSE (Root Mean Square Error), MAE (Mean Absolute Error)
- **견고성:** 센서 노이즈, 온도 변화, 초기값 오차에 대한 민감도
- **계산 효율:** 실시간 BMS 적용을 위한 연산 복잡도

### 5.3 한계점 및 개선 방향

현재 {ko} 연구의 주요 한계점은 다음과 같다:
1. 실제 차량 환경의 복잡한 동적 부하 조건 재현의 어려움
2. 온도, 충방전 패턴 등 다양한 외부 조건에 대한 일반화 부족
3. 센서 오차 및 초기 파라미터 불확실성에 따른 추정 오차

---

## 6. 결론 및 향후 연구 방향 (Conclusion)

### 6.1 주요 발견사항 요약

본 보고서에서는 {ko}({en})에 관한 최신 동향과 핵심 선행 연구를 체계적으로 분석하였다. 수집된 {len(sel_news)}건의 뉴스와 {len(sel_papers)}편의 논문 분석을 통해 다음과 같은 주요 결론을 도출하였다:

- {ko}은(는) 배터리 BMS의 핵심 기능으로, 전기차 시장 성장과 함께 연구 수요가 지속 증가하고 있다
- 칼만 필터 계열과 데이터 기반 방법의 융합 연구가 최신 트렌드로 부상하고 있다
- 실시간 처리와 정확도를 동시에 만족하는 경량화 알고리즘 개발이 핵심 과제이다

### 6.2 향후 연구 방향 제언

1. **AI/ML 융합:** 딥러닝 기반 SOH 추정 모델과 물리 기반 모델의 융합 연구
2. **디지털 트윈:** 실시간 배터리 디지털 트윈을 활용한 예측적 SOH 추정
3. **차세대 배터리 적용:** 고체 배터리, 리튬-황 배터리 등 차세대 소재에 대한 SOH 추정 방법론 개발
4. **클라우드 BMS:** 대규모 차량 군집의 배터리 데이터 기반 집단 지성형 SOH 추정

---

## 참고문헌 (References)

{"".join([f"{r}  \n" for r in all_refs]) if all_refs else "(수집된 참고문헌 없음)"}

---
*본 보고서는 배터리 건강 추정 연구 대시보드에서 자동 생성되었습니다.*  
*기준 교재: Gregory Plett, Battery Management Systems Vol.2 (2015)*
"""
    return report

# =====================================================================
# 4. 세션 초기화
# =====================================================================
defaults = {
    "news_ko": [], "news_en": [], "papers": [],
    "report_text": "", "step": 0, "prev_idx": -1,
    "sel_news": [], "sel_papers": []
}
for k, v in defaults.items():
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
    num, ko, en, bg, keywords = TOPIC_MAP[selected_display]

    if st.session_state["prev_idx"] != idx:
        for k in ["news_ko", "news_en", "papers", "report_text", "sel_news", "sel_papers"]:
            st.session_state[k] = [] if k != "report_text" else ""
        st.session_state["step"] = 0
        st.session_state["prev_idx"] = idx

    st.markdown(f"""
    <div style="background:#e8f0fe; border-radius:8px; padding:10px 14px; margin:12px 0;">
        <div style="font-size:0.72rem; color:#1557b0; font-weight:600; margin-bottom:4px;">🔑 검색 키워드</div>
        <div style="font-size:0.8rem; color:#1a73e8; font-weight:500; line-height:1.5;">{en}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#5f6368; margin:14px 0 8px;'>진행 상태</div>", unsafe_allow_html=True)
    step = st.session_state["step"]
    for label, threshold in [("① 뉴스 수집", 1), ("② 논문 검색", 2), ("③ 자료 선택", 3), ("④ 보고서 생성", 4), ("⑤ 다운로드", 5)]:
        done = step >= threshold
        icon = "✅" if done else "○"
        color = "#137333" if done else "#9aa0a6"
        weight = "600" if done else "400"
        st.markdown(f"<div style='color:{color}; font-size:0.82rem; font-weight:{weight}; padding:5px 0; border-bottom:1px solid #f1f3f4;'>{icon} {label}</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:#bdc1c6; font-size:0.72rem; margin-top:14px;'>{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)

# =====================================================================
# 6. 메인
# =====================================================================
st.markdown(f"""
<div class="top-nav">
    <div class="top-nav-logo">🔋 BMS·SOH 연구 대시보드</div>
    <div class="top-nav-sub">배터리 건강 추정 2-04 | 자료수집 → 선택 → 전문 보고서 자동 생성 | API 키 불필요</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="topic-header">
    <div class="topic-num">Chapter 2-04 &nbsp;·&nbsp; {num}번 주제</div>
    <div class="topic-title">{num}. {ko}</div>
    <div class="topic-en">{en}</div>
</div>
""", unsafe_allow_html=True)

step = st.session_state["step"]
def fc(n): return "done" if step > n else ("active" if step == n else "")
st.markdown(f"""
<div class="flow-bar">
    <div class="flow-step {fc(0)}">① 뉴스 수집</div><div class="flow-arrow">→</div>
    <div class="flow-step {fc(1)}">② 논문 검색</div><div class="flow-arrow">→</div>
    <div class="flow-step {fc(2)}">③ 자료 선택</div><div class="flow-arrow">→</div>
    <div class="flow-step {fc(3)}">④ 보고서 생성</div><div class="flow-arrow">→</div>
    <div class="flow-step {fc(4)}">⑤ 다운로드</div>
</div>
""", unsafe_allow_html=True)

news_cnt   = len(st.session_state["news_ko"]) + len(st.session_state["news_en"])
paper_cnt  = len(st.session_state["papers"])
sel_total  = len(st.session_state["sel_news"]) + len(st.session_state["sel_papers"])
has_report = bool(st.session_state["report_text"])

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card"><div class="metric-card-label">선택 주제</div><div class="metric-card-value">{num}번</div></div>
    <div class="metric-card"><div class="metric-card-label">수집 뉴스</div><div class="metric-card-value {'green' if news_cnt else 'gray'}">{news_cnt}건</div></div>
    <div class="metric-card"><div class="metric-card-label">수집 논문</div><div class="metric-card-value {'green' if paper_cnt else 'gray'}">{paper_cnt}편</div></div>
    <div class="metric-card"><div class="metric-card-label">선택 자료</div><div class="metric-card-value {'green' if sel_total else 'gray'}">{sel_total}건</div></div>
    <div class="metric-card"><div class="metric-card-label">보고서</div><div class="metric-card-value {'green' if has_report else 'gray'}">{'완성 ✓' if has_report else '대기중'}</div></div>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# 7. 탭
# =====================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📡 ① 뉴스 수집",
    "📚 ② 논문 검색",
    "✅ ③ 자료 선택 & 보고서 생성",
    "💾 ④ 저장 & 다운로드",
])

# ── Tab 1: 뉴스 ──────────────────────────
with tab1:
    st.markdown('<div class="section-title">📡 최신 뉴스 및 정보 수집</div>', unsafe_allow_html=True)
    c1, c2, _ = st.columns([2, 2, 6])
    with c1:
        run_news = st.button("🔄 뉴스 수집 시작", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑️ 초기화", use_container_width=True):
            st.session_state["news_ko"] = []
            st.session_state["news_en"] = []
            st.rerun()

    if run_news:
        prog = st.progress(0); status = st.empty()
        status.info("🇰🇷 국내 뉴스 검색 중...")
        prog.progress(25)
        raw_ko = fetch_news_ko(ko + " 배터리", 6)
        st.session_state["news_ko"] = [
            {"title": e.title, "link": e.link, "lang": "ko",
             "published": getattr(e, 'published', ''),
             "source": (e.get('source') or {}).get('title', 'Google News')}
            for e in raw_ko
        ]
        status.info("🌍 해외 뉴스 검색 중...")
        prog.progress(75)
        raw_en = fetch_news_en(en, 6)
        st.session_state["news_en"] = [
            {"title": e.title, "link": e.link, "lang": "en",
             "published": getattr(e, 'published', ''),
             "source": (e.get('source') or {}).get('title', 'Google News')}
            for e in raw_en
        ]
        prog.progress(100); status.empty(); prog.empty()
        if st.session_state["step"] < 1:
            st.session_state["step"] = 1
        st.rerun()

    ko_list = st.session_state["news_ko"]
    en_list = st.session_state["news_en"]
    if ko_list or en_list:
        st.success(f"✅ 총 {len(ko_list)+len(en_list)}건 수집 완료 — ③탭에서 원하는 항목을 선택하세요")
        col_ko, col_en = st.columns(2)
        with col_ko:
            st.markdown(f"<div style='font-weight:700; margin-bottom:8px;'>🇰🇷 국내 ({len(ko_list)}건)</div>", unsafe_allow_html=True)
            for item in ko_list:
                st.markdown(f"""<div class="news-item">
                    <div class="news-item-title"><a href="{item['link']}" target="_blank">{item['title']}</a></div>
                    <div class="news-item-meta">📅 {item['published']} · {item['source']}</div>
                </div>""", unsafe_allow_html=True)
        with col_en:
            st.markdown(f"<div style='font-weight:700; margin-bottom:8px;'>🌍 해외 ({len(en_list)}건)</div>", unsafe_allow_html=True)
            for item in en_list:
                st.markdown(f"""<div class="news-item">
                    <div class="news-item-title"><a href="{item['link']}" target="_blank">{item['title']}</a></div>
                    <div class="news-item-meta">📅 {item['published']} · {item['source']}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="text-align:center; padding:40px; color:#9aa0a6;">
            <div style="font-size:2.5rem; margin-bottom:12px;">📰</div>
            <div>위 버튼을 클릭하면 국내·해외 뉴스를 수집합니다</div>
        </div>""", unsafe_allow_html=True)

# ── Tab 2: 논문 ──────────────────────────
with tab2:
    st.markdown('<div class="section-title">📚 학술 논문 검색</div>', unsafe_allow_html=True)
    st.warning("⚠️ Google Scholar는 잦은 요청 시 일시 차단될 수 있습니다.")
    c1, c2, _ = st.columns([2, 2, 6])
    with c1:
        run_scholar = st.button("🔍 논문 검색 시작", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑️ 초기화 ", use_container_width=True):
            st.session_state["papers"] = []; st.rerun()

    if run_scholar:
        with st.spinner("Google Scholar 조회 중... (최대 20초 소요)"):
            raw = fetch_scholar(en, 5)
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
        if st.session_state["step"] < 2:
            st.session_state["step"] = 2
        st.rerun()

    papers = st.session_state["papers"]
    if papers:
        st.success(f"✅ 논문 {len(papers)}편 수집 완료 — ③탭에서 원하는 논문을 선택하세요")
        for i, p in enumerate(papers, 1):
            abs_text  = (p['abstract'][:300] + "...") if len(p['abstract']) > 300 else p['abstract']
            abs_html  = f"<div class='paper-item-abs'><b>Abstract:</b> {abs_text}</div>" if abs_text else ""
            link_html = f"<a href='{p['url']}' target='_blank' style='color:#1a73e8; font-size:0.8rem; font-weight:600;'>➡️ 원문 보기</a>" if p['url'] else ""
            st.markdown(f"""<div class="paper-item">
                <div class="paper-item-title">[{i}] {p['title']} ({p['year']})</div>
                <div class="paper-item-author">👤 {p['authors']}</div>
                {"<div class='paper-item-venue'>📔 " + p['journal'] + "</div>" if p['journal'] else ""}
                {abs_html}
                <div style="margin-top:8px;">{link_html}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="text-align:center; padding:40px; color:#9aa0a6;">
            <div style="font-size:2.5rem; margin-bottom:12px;">📖</div>
            <div>위 버튼을 클릭하면 Google Scholar에서 관련 논문을 검색합니다</div>
        </div>""", unsafe_allow_html=True)

# ── Tab 3: 자료 선택 & 보고서 생성 ─────
with tab3:
    st.markdown('<div class="section-title">✅ 자료 선택 및 전문 보고서 자동 생성</div>', unsafe_allow_html=True)

    all_news   = st.session_state["news_ko"] + st.session_state["news_en"]
    all_papers = st.session_state["papers"]

    if not all_news and not all_papers:
        st.info("먼저 ①탭에서 뉴스를, ②탭에서 논문을 수집해주세요.")
    else:
        # 뉴스 선택
        sel_news_list = []
        if all_news:
            st.markdown('<div class="select-header">📰 보고서에 포함할 뉴스를 선택하세요 (복수 선택 가능)</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            for i, item in enumerate(all_news):
                flag = "🇰🇷" if item.get("lang") == "ko" else "🌍"
                with (col1 if i % 2 == 0 else col2):
                    if st.checkbox(f"{flag} {item['title'][:55]}{'...' if len(item['title'])>55 else ''}", key=f"nc_{i}"):
                        sel_news_list.append(item)

        # 논문 선택
        sel_paper_list = []
        if all_papers:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="select-header">📚 보고서에 포함할 논문을 선택하세요 (복수 선택 가능)</div>', unsafe_allow_html=True)
            for i, p in enumerate(all_papers):
                if st.checkbox(f"[{i+1}] {p['title'][:65]}{'...' if len(p['title'])>65 else ''} ({p['year']})", key=f"pc_{i}"):
                    sel_paper_list.append(p)

        st.session_state["sel_news"]   = sel_news_list
        st.session_state["sel_papers"] = sel_paper_list
        total_sel = len(sel_news_list) + len(sel_paper_list)

        st.markdown("<br>", unsafe_allow_html=True)
        if total_sel > 0:
            st.success(f"✅ 뉴스 {len(sel_news_list)}건 + 논문 {len(sel_paper_list)}편 선택됨")
        else:
            st.warning("⚠️ 최소 1개 이상 선택해야 보고서를 생성할 수 있습니다.")

        st.markdown("---")
        col_gen, _ = st.columns([3, 7])
        with col_gen:
            gen_btn = st.button("📄 전문 보고서 자동 생성", type="primary",
                                use_container_width=True, disabled=(total_sel == 0))

        if gen_btn and total_sel > 0:
            with st.spinner("전문 보고서를 생성하는 중입니다..."):
                time.sleep(0.5)
                report = generate_structured_report(
                    num, ko, en, bg, keywords,
                    sel_news_list, sel_paper_list
                )
                st.session_state["report_text"] = report
                if st.session_state["step"] < 4:
                    st.session_state["step"] = 4
            st.success("✅ 보고서 생성 완료! ④탭에서 확인 및 다운로드하세요.")
            st.markdown("---")
            st.markdown(report)

        elif st.session_state["report_text"] and not gen_btn:
            st.markdown("---")
            st.markdown("### 📄 이전에 생성된 보고서")
            st.markdown(st.session_state["report_text"])

# ── Tab 4: 저장 & 다운로드 ───────────────
with tab4:
    st.markdown('<div class="section-title">💾 저장 및 다운로드</div>', unsafe_allow_html=True)
    report_text = st.session_state["report_text"]

    if report_text:
        st.success("✅ 보고서가 준비되었습니다.")
        st.markdown("<div style='font-size:0.88rem; font-weight:600; color:#5f6368; margin-bottom:6px;'>✏️ 최종 수정 (수정 후 다운로드)</div>", unsafe_allow_html=True)
        edited = st.text_area("내용을 수정하세요", value=report_text, height=400, key=f"final_{num}")
        st.session_state["report_text"] = edited

        st.markdown("<br>", unsafe_allow_html=True)
        file_base = f"BMS_SOH_{num}_{datetime.now().strftime('%Y%m%d')}"
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 TXT 다운로드", data=edited, file_name=f"{file_base}.txt", mime="text/plain", type="primary", use_container_width=True)
        with c2:
            st.download_button("📋 Markdown(.md)", data=edited, file_name=f"{file_base}.md", mime="text/markdown", type="primary", use_container_width=True)
        with c3:
            if st.button("🖨️ 인쇄/PDF", use_container_width=True):
                st.info("브라우저에서 Ctrl+P → PDF로 저장하세요.")

        st.markdown("---")
        st.markdown("### 👁️ 최종 미리보기")
        st.markdown(edited)
    else:
        st.markdown("""<div style="text-align:center; padding:50px; color:#9aa0a6;">
            <div style="font-size:2.5rem; margin-bottom:14px;">📋</div>
            <div style="font-size:1rem; font-weight:600; color:#5f6368; margin-bottom:8px;">아직 보고서가 없습니다</div>
            <div>① 뉴스 수집 → ② 논문 검색 → ③ 자료 선택 후 보고서 생성</div>
        </div>""", unsafe_allow_html=True)
