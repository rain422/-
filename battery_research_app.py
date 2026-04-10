import streamlit as st
import feedparser
from scholarly import scholarly
from datetime import datetime
import requests
import time
import urllib.parse

# =====================================================================
# 다국어 UI 텍스트
# =====================================================================
LANG_OPTIONS = {"🇰🇷 한국어": "ko", "🇺🇸 English": "en", "🇯🇵 日本語": "ja", "🇨🇳 中文": "zh"}

UI = {
    "ko": {
        "app_title":"🔋 BMS·SOH 연구 대시보드","app_sub":"배터리 건강 추정 2-04 | 자료수집 → 선택 → 전문 보고서 자동 생성",
        "sidebar_title":"🔋 배터리 건강 추정","sidebar_sub":"2-04 연구 대시보드","sidebar_keyword":"🔑 검색 키워드","sidebar_progress":"진행 상태","topic_chapter":"Chapter 2-04",
        "tab1":"📡 ① 뉴스 수집","tab2":"📚 ② 논문 검색","tab3":"✅ ③ 자료 선택 & 보고서","tab4":"💾 ④ 저장 & 다운로드",
        "news_collect":"🔄 뉴스 수집 시작","scholar_search":"🔍 Google Scholar 검색","arxiv_search":"🔍 arXiv 논문 검색","reset":"🗑️ 초기화","gen_report":"📄 전문 보고서 자동 생성",
        "download_txt":"📄 TXT 다운로드","download_md":"📋 Markdown 다운로드","print_pdf":"🖨️ 인쇄/PDF",
        "metric_topic":"선택 주제","metric_news":"수집 뉴스","metric_paper":"수집 논문","metric_selected":"선택 자료","metric_report":"보고서",
        "report_done":"완성 ✓","report_wait":"대기중",
        "select_news_header":"📰 보고서에 포함할 뉴스를 선택하세요 (복수 선택 가능)","select_paper_header":"📚 보고서에 포함할 논문을 선택하세요 (복수 선택 가능)",
        "domestic_news":"🇰🇷 국내 뉴스","foreign_news":"🌍 해외 뉴스",
        "no_data":"먼저 ①탭에서 뉴스를, ②탭에서 논문을 수집해주세요.",
        "scholar_warning":"⚠️ Google Scholar는 잦은 요청 시 일시 차단될 수 있습니다.",
        "arxiv_info":"💡 arXiv는 무료 학술 논문 저장소입니다. 차단 없이 안정적으로 검색됩니다.",
        "arxiv_no_result":"arXiv 검색 결과가 없습니다. 키워드를 확인하거나 잠시 후 다시 시도하세요.",
        "collected":"건 수집","papers_collected":"편 수집","select_tip":"③탭에서 원하는 항목을 선택하세요",
        "edit_label":"✏️ 최종 수정 (수정 후 다운로드)","preview":"👁️ 최종 미리보기",
        "no_report":"아직 보고서가 없습니다","no_report_guide":"① 뉴스 수집 → ② 논문 검색 → ③ 자료 선택 후 보고서 생성",
        "steps":["① 뉴스 수집","② 논문 검색","③ 자료 선택","④ 보고서 생성","⑤ 다운로드"],
        "flow":["① 뉴스 수집","② 논문 검색","③ 자료 선택","④ 보고서 생성","⑤ 다운로드"],
        "report_title":"연구 분석 보고서","abstract":"초록 (Abstract)","intro":"1. 서론","intro_bg":"1.1 연구 배경 및 필요성","intro_obj":"1.2 연구 목적","intro_struct":"1.3 보고서 구성",
        "theory":"2. 이론적 배경","theory_def":"2.1 핵심 개념 정의","theory_concept":"2.2 관련 핵심 개념","theory_trend":"2.3 기존 연구 동향",
        "trends":"3. 최신 기술 동향 분석","domestic_trend":"3.1 국내 동향","foreign_trend":"3.2 해외 동향",
        "literature":"4. 핵심 선행 연구 검토","arxiv_review":"4.2 arXiv 최신 연구",
        "analysis":"5. 기술적 분석 및 고찰","comparison":"5.1 주요 연구 특징 비교","metrics":"5.2 성능 지표 및 평가","limits":"5.3 한계점 및 개선 방향",
        "conclusion":"6. 결론 및 향후 연구 방향","findings":"6.1 주요 발견사항","future":"6.2 향후 연구 방향 제언",
        "references":"참고문헌 (References)","auto_generated":"본 보고서는 배터리 건강 추정 연구 대시보드에서 자동 생성되었습니다.",
        "written_date":"작성일","keyword_label":"키워드","ref_book":"기준 문헌","collected_data":"수집 자료","news_unit":"건","paper_unit":"편","lang_label":"언어 선택",
        "searching_arxiv":"arXiv 검색 중... (최대 10초 소요)","searching_scholar":"Google Scholar 조회 중... (최대 20초 소요)",
    },
    "en": {
        "app_title":"🔋 BMS·SOH Research Dashboard","app_sub":"Battery Health Estimation 2-04 | Collect → Select → Auto Report",
        "sidebar_title":"🔋 Battery Health","sidebar_sub":"2-04 Research Dashboard","sidebar_keyword":"🔑 Search Keyword","sidebar_progress":"Progress","topic_chapter":"Chapter 2-04",
        "tab1":"📡 ① News","tab2":"📚 ② Papers","tab3":"✅ ③ Select & Report","tab4":"💾 ④ Save & Download",
        "news_collect":"🔄 Collect News","scholar_search":"🔍 Google Scholar Search","arxiv_search":"🔍 arXiv Search","reset":"🗑️ Reset","gen_report":"📄 Generate Professional Report",
        "download_txt":"📄 Download TXT","download_md":"📋 Download Markdown","print_pdf":"🖨️ Print/PDF",
        "metric_topic":"Topic","metric_news":"News","metric_paper":"Papers","metric_selected":"Selected","metric_report":"Report",
        "report_done":"Done ✓","report_wait":"Pending",
        "select_news_header":"📰 Select news to include in the report","select_paper_header":"📚 Select papers to include in the report",
        "domestic_news":"🇰🇷 Korean News","foreign_news":"🌍 Global News",
        "no_data":"Please collect news (Tab ①) and papers (Tab ②) first.",
        "scholar_warning":"⚠️ Google Scholar may temporarily block frequent requests.",
        "arxiv_info":"💡 arXiv is a free open-access repository with stable access.",
        "arxiv_no_result":"No arXiv results found. Please check the keyword or try again later.",
        "collected":" collected","papers_collected":" papers found","select_tip":"Go to Tab ③ to select items",
        "edit_label":"✏️ Final Edit","preview":"👁️ Final Preview",
        "no_report":"No report yet","no_report_guide":"① Collect News → ② Search Papers → ③ Select & Generate",
        "steps":["① News","② Papers","③ Select","④ Report","⑤ Download"],
        "flow":["① News","② Papers","③ Select","④ Generate","⑤ Download"],
        "report_title":"Research Analysis Report","abstract":"Abstract","intro":"1. Introduction","intro_bg":"1.1 Background & Motivation","intro_obj":"1.2 Research Objectives","intro_struct":"1.3 Report Structure",
        "theory":"2. Theoretical Background","theory_def":"2.1 Key Concept Definitions","theory_concept":"2.2 Core Concepts","theory_trend":"2.3 Existing Research Overview",
        "trends":"3. Recent Technology Trends","domestic_trend":"3.1 Korean Trends","foreign_trend":"3.2 Global Trends",
        "literature":"4. Literature Review","arxiv_review":"4.2 Recent arXiv Preprints",
        "analysis":"5. Technical Analysis","comparison":"5.1 Methodology Comparison","metrics":"5.2 Performance Metrics","limits":"5.3 Limitations & Improvements",
        "conclusion":"6. Conclusion & Future Work","findings":"6.1 Key Findings","future":"6.2 Future Research Directions",
        "references":"References","auto_generated":"This report was auto-generated by the Battery Health Estimation Research Dashboard.",
        "written_date":"Date","keyword_label":"Keywords","ref_book":"Reference Book","collected_data":"Collected Data","news_unit":"","paper_unit":"","lang_label":"Language",
        "searching_arxiv":"Searching arXiv... (up to 10 sec)","searching_scholar":"Searching Google Scholar... (up to 20 sec)",
    },
    "ja": {
        "app_title":"🔋 BMS·SOH 研究ダッシュボード","app_sub":"バッテリー健全性推定 2-04 | 収集 → 選択 → 専門レポート自動生成",
        "sidebar_title":"🔋 バッテリー健全性推定","sidebar_sub":"2-04 研究ダッシュボード","sidebar_keyword":"🔑 検索キーワード","sidebar_progress":"進捗状況","topic_chapter":"Chapter 2-04",
        "tab1":"📡 ① ニュース収集","tab2":"📚 ② 論文検索","tab3":"✅ ③ 資料選択 & レポート","tab4":"💾 ④ 保存 & ダウンロード",
        "news_collect":"🔄 ニュース収集開始","scholar_search":"🔍 Google Scholar 検索","arxiv_search":"🔍 arXiv 論文検索","reset":"🗑️ リセット","gen_report":"📄 専門レポート自動生成",
        "download_txt":"📄 TXT ダウンロード","download_md":"📋 Markdown ダウンロード","print_pdf":"🖨️ 印刷/PDF",
        "metric_topic":"選択テーマ","metric_news":"収集ニュース","metric_paper":"収集論文","metric_selected":"選択資料","metric_report":"レポート",
        "report_done":"完成 ✓","report_wait":"待機中",
        "select_news_header":"📰 レポートに含めるニュースを選択してください","select_paper_header":"📚 レポートに含める論文を選択してください",
        "domestic_news":"🇰🇷 韓国ニュース","foreign_news":"🌍 海外ニュース",
        "no_data":"①タブでニュースを、②タブで論文を収集してください。",
        "scholar_warning":"⚠️ Google Scholarは頻繁なリクエストで一時ブロックされる場合があります。",
        "arxiv_info":"💡 arXivは無料の学術論文リポジトリです。安定してアクセス可能です。",
        "arxiv_no_result":"arXiv検索結果がありません。キーワードを確認するか、後でもう一度お試しください。",
        "collected":"件収集","papers_collected":"件収集","select_tip":"③タブで選択してください",
        "edit_label":"✏️ 最終編集","preview":"👁️ プレビュー",
        "no_report":"レポートがありません","no_report_guide":"① ニュース収集 → ② 論文検索 → ③ 資料選択後にレポート生成",
        "steps":["① ニュース","② 論文","③ 選択","④ 生成","⑤ DL"],
        "flow":["① ニュース収集","② 論文検索","③ 資料選択","④ レポート生成","⑤ DL"],
        "report_title":"研究分析レポート","abstract":"要旨 (Abstract)","intro":"1. 序論","intro_bg":"1.1 研究背景と必要性","intro_obj":"1.2 研究目的","intro_struct":"1.3 レポート構成",
        "theory":"2. 理論的背景","theory_def":"2.1 主要概念の定義","theory_concept":"2.2 関連コアコンセプト","theory_trend":"2.3 既存研究動向",
        "trends":"3. 最新技術動向分析","domestic_trend":"3.1 韓国動向","foreign_trend":"3.2 海外動向",
        "literature":"4. 先行研究レビュー","arxiv_review":"4.2 arXiv 最新研究",
        "analysis":"5. 技術的分析と考察","comparison":"5.1 主要手法の比較","metrics":"5.2 性能指標と評価","limits":"5.3 限界点と改善方向",
        "conclusion":"6. 結論と今後の研究方向","findings":"6.1 主な発見事項","future":"6.2 今後の研究提言",
        "references":"参考文献","auto_generated":"このレポートはバッテリー健全性推定研究ダッシュボードで自動生成されました。",
        "written_date":"作成日","keyword_label":"キーワード","ref_book":"参考教材","collected_data":"収集データ","news_unit":"件","paper_unit":"件","lang_label":"言語選択",
        "searching_arxiv":"arXiv 検索中... (最大10秒)","searching_scholar":"Google Scholar 照会中... (最大20秒)",
    },
    "zh": {
        "app_title":"🔋 BMS·SOH 研究仪表板","app_sub":"电池健康状态估计 2-04 | 收集 → 选择 → 自动生成专业报告",
        "sidebar_title":"🔋 电池健康估计","sidebar_sub":"2-04 研究仪表板","sidebar_keyword":"🔑 搜索关键词","sidebar_progress":"进度状态","topic_chapter":"Chapter 2-04",
        "tab1":"📡 ① 新闻收集","tab2":"📚 ② 论文检索","tab3":"✅ ③ 选择资料 & 报告","tab4":"💾 ④ 保存 & 下载",
        "news_collect":"🔄 开始收集新闻","scholar_search":"🔍 Google Scholar 搜索","arxiv_search":"🔍 arXiv 论文搜索","reset":"🗑️ 重置","gen_report":"📄 自动生成专业报告",
        "download_txt":"📄 下载 TXT","download_md":"📋 下载 Markdown","print_pdf":"🖨️ 打印/PDF",
        "metric_topic":"选择主题","metric_news":"收集新闻","metric_paper":"收集论文","metric_selected":"选择资料","metric_report":"报告",
        "report_done":"完成 ✓","report_wait":"等待中",
        "select_news_header":"📰 请选择要包含在报告中的新闻（可多选）","select_paper_header":"📚 请选择要包含在报告中的论文（可多选）",
        "domestic_news":"🇰🇷 韩国新闻","foreign_news":"🌍 国际新闻",
        "no_data":"请先在①标签收集新闻，在②标签检索论文。",
        "scholar_warning":"⚠️ Google Scholar 频繁请求可能被临时封锁。",
        "arxiv_info":"💡 arXiv 是免费学术论文存储库，访问稳定无封锁。",
        "arxiv_no_result":"未找到arXiv结果。请检查关键词或稍后重试。",
        "collected":"条已收集","papers_collected":"篇已收集","select_tip":"请在③标签选择所需内容",
        "edit_label":"✏️ 最终编辑（下载前可修改）","preview":"👁️ 最终预览",
        "no_report":"尚无报告","no_report_guide":"① 收集新闻 → ② 检索论文 → ③ 选择资料后生成报告",
        "steps":["① 新闻","② 论文","③ 选择","④ 生成","⑤ 下载"],
        "flow":["① 新闻收集","② 论文检索","③ 资料选择","④ 报告生成","⑤ 下载"],
        "report_title":"研究分析报告","abstract":"摘要 (Abstract)","intro":"1. 绪论","intro_bg":"1.1 研究背景与必要性","intro_obj":"1.2 研究目的","intro_struct":"1.3 报告结构",
        "theory":"2. 理论背景","theory_def":"2.1 核心概念定义","theory_concept":"2.2 相关核心概念","theory_trend":"2.3 既有研究动向",
        "trends":"3. 最新技术动向分析","domestic_trend":"3.1 韩国动向","foreign_trend":"3.2 国际动向",
        "literature":"4. 核心先行研究综述","arxiv_review":"4.2 arXiv 最新研究",
        "analysis":"5. 技术分析与考察","comparison":"5.1 主要方法比较","metrics":"5.2 性能指标与评估","limits":"5.3 局限性与改进方向",
        "conclusion":"6. 结论与未来研究方向","findings":"6.1 主要发现","future":"6.2 未来研究建议",
        "references":"参考文献","auto_generated":"本报告由电池健康估计研究仪表板自动生成。",
        "written_date":"日期","keyword_label":"关键词","ref_book":"参考教材","collected_data":"收集数据","news_unit":"条","paper_unit":"篇","lang_label":"语言选择",
        "searching_arxiv":"正在搜索arXiv... (最多10秒)","searching_scholar":"正在查询Google Scholar... (最多20秒)",
    },
}

# =====================================================================
# 주제 데이터 (언어별 이름 포함)
# =====================================================================
TOPICS = [
    ("01",
     {"ko":"배터리 건강 추정의 필요성","en":"Need for Battery Health Estimation","ja":"バッテリー健全性推定の必要性","zh":"电池健康估计的必要性"},
     "Battery State of Health Estimation",
     "배터리 건강 상태(SOH)는 현재 용량을 초기 용량 대비 비율로 나타내며 전기차·에너지 저장 시스템의 안전성과 성능 관리에 핵심적이다.",
     ["SOH","배터리 열화","RUL","EV","BMS"]),
    ("02",
     {"ko":"음극 노화","en":"Anode Aging","ja":"負極の劣化","zh":"负极老化"},
     "Lithium-ion Battery Anode Aging",
     "음극의 노화는 리튬 도금, SEI 성장, 구조적 균열 등으로 발생하며 가역 용량 손실과 내부 저항 증가를 초래한다.",
     ["SEI","리튬 도금","흑연 음극","용량 손실","사이클 열화"]),
    ("03",
     {"ko":"양극 노화","en":"Cathode Aging","ja":"正極の劣化","zh":"正极老化"},
     "Lithium-ion Battery Cathode Aging",
     "양극 노화는 구조적 상변이, 전이금속 용해, 입자 균열 등으로 발생하며 NMC·LFP 등 소재별로 열화 메커니즘이 다르다.",
     ["NMC/LFP/NCA","구조적 열화","전이금속 용해","상변이","캘린더 노화"]),
    ("04",
     {"ko":"R₀에 대한 전압 감도","en":"Voltage Sensitivity to R₀","ja":"R₀に対する電圧感度","zh":"对R₀的电压灵敏度"},
     "Battery Internal Resistance Voltage Sensitivity",
     "내부 저항 R₀는 배터리 전압 강하의 주요 원인으로 SOH와 밀접한 상관관계를 가진다.",
     ["내부 저항","전압 강하","등가 회로 모델","임피던스","열화 진단"]),
    ("05",
     {"ko":"R₀를 추정하기 위한 코드","en":"Code for Estimating R₀","ja":"R₀推定コード","zh":"估计R₀的代码"},
     "Battery Internal Resistance Estimation Algorithm",
     "전류 펄스 응답, EIS, 최소제곱법 등을 활용하여 R₀를 실시간으로 추정한다.",
     ["최소제곱법","EIS","전류 펄스","실시간 추정","Python 알고리즘"]),
    ("06",
     {"ko":"전체 용량에 대한 전압의 민감도 Q","en":"Voltage Sensitivity Q to Total Capacity","ja":"全容量に対する電圧感度Q","zh":"总容量的电压灵敏度Q"},
     "Battery Voltage Sensitivity Total Capacity",
     "전체 용량 Q는 SOH 추정의 핵심 파라미터로, OCV-SOC 곡선의 기울기 변화를 통해 추정할 수 있다.",
     ["전체 용량 Q","OCV-SOC","활물질 손실","쿨롱 카운팅","용량 추정"]),
    ("07",
     {"ko":"칼만 필터를 통한 파라미터 추정","en":"Parameter Estimation via Kalman Filter","ja":"カルマンフィルタによるパラメータ推定","zh":"通过卡尔曼滤波器进行参数估计"},
     "Kalman Filter Battery Parameter Estimation",
     "칼만 필터는 노이즈가 있는 측정값에서 배터리 상태변수를 최적으로 추정하는 재귀적 알고리즘이다.",
     ["칼만 필터","상태 추정","공분산","예측-수정","재귀 알고리즘"]),
    ("08",
     {"ko":"EKF 파라미터 추정","en":"EKF Parameter Estimation","ja":"EKFパラメータ推定","zh":"EKF参数估计"},
     "Extended Kalman Filter Battery SOH",
     "EKF는 비선형 배터리 모델에 야코비안 행렬로 선형화하여 칼만 필터를 적용하는 방법이다.",
     ["EKF","야코비안","비선형 시스템","SOC 추정","선형화"]),
    ("09",
     {"ko":"SPKF 파라미터 추정","en":"SPKF Parameter Estimation","ja":"SPKFパラメータ推定","zh":"SPKF参数估计"},
     "Sigma-Point Kalman Filter Battery",
     "SPKF/UKF는 비선형 변환을 시그마 포인트의 통계적 전파로 근사하며 EKF보다 정확도가 높다.",
     ["SPKF/UKF","시그마 포인트","무향 변환","비선형 추정","통계적 근사"]),
    ("10",
     {"ko":"조인트 추정과 듀얼 추정","en":"Joint and Dual Estimation","ja":"ジョイント推定とデュアル推定","zh":"联合估计与双重估计"},
     "Joint Dual Estimation Battery State",
     "조인트 추정은 상태변수와 파라미터를 단일 벡터로, 듀얼 추정은 두 필터로 각각 추정한다.",
     ["조인트 추정","듀얼 추정","이중 필터","적응형 추정","동시 추정"]),
    ("11",
     {"ko":"견고성과 속도","en":"Robustness and Speed","ja":"ロバスト性と速度","zh":"鲁棒性与速度"},
     "Robustness Speed Battery Estimation",
     "추정 알고리즘의 견고성은 센서 노이즈·모델 불확실성에 대한 민감도를 의미하며, 실시간 BMS 적용의 핵심이다.",
     ["견고성","계산 복잡도","실시간 처리","노이즈 민감도","수렴 속도"]),
    ("12",
     {"ko":"선형 회귀를 통한 전체 용량의 비편향 추정값","en":"Unbiased Capacity Estimation via Linear Regression","ja":"線形回帰による全容量の不偏推定","zh":"线性回归对总容量的无偏估计"},
     "Unbiased Battery Capacity Linear Regression",
     "선형 회귀를 통해 측정 데이터에서 배터리 전체 용량을 편향 없이 추정한다.",
     ["비편향 추정","선형 회귀","쿨롱 카운팅","OLS","용량 추정"]),
    ("13",
     {"ko":"가중 일반 최소제곱법","en":"Weighted Generalized Least Squares","ja":"重み付き一般最小二乗法","zh":"加权广义最小二乘法"},
     "Weighted Generalized Least Squares Battery",
     "WGLS는 측정 노이즈의 분산이 불균일할 때 각 데이터 포인트에 가중치를 부여하여 정확도를 향상시킨다.",
     ["WGLS","이분산성","가중 행렬","최적 추정","노이즈 모델링"]),
    ("14",
     {"ko":"총 가중 최소제곱법","en":"Total Weighted Least Squares","ja":"総重み付き最小二乗法","zh":"总加权最小二乗法"},
     "Weighted Total Least Squares Battery",
     "TWLS는 입출력 모두에 노이즈가 존재하는 EIV 모델에 적합한 추정 방법이다.",
     ["TWLS","EIV","양방향 노이즈","총 최소제곱","용량 추정"]),
    ("15",
     {"ko":"모델 적합도의 우수성","en":"Goodness of Model Fit","ja":"モデル適合度の優秀性","zh":"模型拟合优度"},
     "Goodness of Fit Battery Equivalent Circuit",
     "등가 회로 모델의 적합도는 RMSE, R², AIC 등으로 평가하며 과적합 방지를 위한 모델 복잡도 선택이 중요하다.",
     ["RMSE","R²","AIC/BIC","등가 회로 모델","모델 검증"]),
    ("16",
     {"ko":"신뢰 구간","en":"Confidence Intervals","ja":"信頼区間","zh":"置信区间"},
     "Confidence Interval Battery Estimation",
     "추정값의 신뢰 구간은 불확실성을 정량화하며, 배터리 안전 마진 설정에 활용된다.",
     ["신뢰 구간","불확실성 정량화","공분산","오차 한계","통계적 추론"]),
    ("17",
     {"ko":"단순화된 총 최소제곱","en":"Simplified Total Least Squares","ja":"簡略化された総最小二乗","zh":"简化总最小二乘"},
     "Simplified Total Least Squares Battery",
     "단순화된 TLS는 계산 복잡도를 줄이면서 EIV 모델의 장점을 유지하는 방법이다.",
     ["단순화 TLS","근사 알고리즘","계산 효율","실시간 BMS","EIV"]),
    ("18",
     {"ko":"근사 전체 솔루션","en":"Approximate Total Solution","ja":"近似全体ソリューション","zh":"近似总体解"},
     "Approximate Total Solution Battery",
     "근사 전체 솔루션은 복잡한 최적화를 닫힌 형태로 근사하여 계산 효율을 높이는 방법이다.",
     ["근사 해","계산 최적화","파라미터 추정","수치 안정성","실시간 구현"]),
    ("19",
     {"ko":"방법별 시뮬레이션 코드","en":"Simulation Code by Method","ja":"方法別シミュレーションコード","zh":"各方法仿真代码"},
     "Battery SOH Estimation Simulation Code",
     "EKF, SPKF, 최소제곱법 등의 성능을 Python·MATLAB 시뮬레이션으로 비교한다.",
     ["시뮬레이션","Python/MATLAB","알고리즘 비교","성능 평가","배터리 데이터셋"]),
    ("20",
     {"ko":"HEV 시뮬레이션 예시","en":"HEV Simulation Example","ja":"HEVシミュレーション例","zh":"HEV仿真示例"},
     "Hybrid Electric Vehicle Battery Simulation",
     "HEV의 배터리는 빈번한 충방전과 높은 전류 변동이 특징이며, UDDS·HWFET 사이클로 성능을 검증한다.",
     ["HEV","주행 사이클","UDDS/HWFET","동적 부하","SOH 추정"]),
    ("21",
     {"ko":"EV 시뮬레이션 예시","en":"EV Simulation Example","ja":"EVシミュレーション例","zh":"EV仿真示例"},
     "Electric Vehicle EV Battery Simulation",
     "EV는 1회 충전 주행거리와 배터리 수명이 핵심이며, WLTP·EPA 사이클에서 SOH 추정 정확도를 분석한다.",
     ["EV","주행거리","WLTP/EPA","에너지 관리","충전 전략"]),
    ("22",
     {"ko":"시뮬레이션에 대한 논의","en":"Discussion on Simulation","ja":"シミュレーションについての議論","zh":"仿真讨论"},
     "Battery Simulation Discussion Results",
     "다양한 추정 방법의 시뮬레이션 결과를 비교하고, 실차 적용 시 고려사항을 논의한다.",
     ["결과 비교","실차 적용","온도 영향","센서 오차","검증"]),
    ("23",
     {"ko":"결론 및 향후 방향","en":"Conclusion and Future Directions","ja":"結論と今後の方向性","zh":"结论与未来方向"},
     "Battery Health Estimation Future Research",
     "머신러닝 기반 추정, 디지털 트윈, 클라우드 BMS 등 미래 연구 방향을 제시한다.",
     ["머신러닝 SOH","디지털 트윈","차세대 배터리","클라우드 BMS","연구 과제"]),
    ("24",
     {"ko":"비선형 칼만 필터 알고리즘","en":"Nonlinear Kalman Filter Algorithm","ja":"非線形カルマンフィルタアルゴリズム","zh":"非线性卡尔曼滤波算法"},
     "Nonlinear Kalman Filter Algorithm Battery",
     "EKF, UKF, CKF, PF 등 비선형 칼만 필터 계열 알고리즘의 이론과 배터리 SOH 추정 적용을 정리한다.",
     ["비선형 칼만 필터","UKF/CKF","파티클 필터","비선형 추정","알고리즘 비교"]),
]

def get_topic_display(lang):
    return [f"{n}. {names[lang]}" for n, names, en, bg, kw in TOPICS]

def get_topic_map(lang):
    return {f"{n}. {names[lang]}": (n, names["ko"], en, bg, kw) for n, names, en, bg, kw in TOPICS}

# =====================================================================
# 페이지 설정
# =====================================================================
st.set_page_config(page_title="BMS·SOH Research Dashboard", page_icon="🔋", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');
html,body,[class*="css"]{font-family:'Noto Sans KR','Noto Sans JP','Noto Sans SC',sans-serif;}
.stApp{background-color:#f5f7fa;color:#1a1a2e;}
section[data-testid="stSidebar"]{background-color:#ffffff;border-right:1px solid #e0e4ea;}
.top-nav{background:#ffffff;border-bottom:2px solid #e8eaf0;padding:16px 32px;margin-bottom:20px;border-radius:12px;display:flex;align-items:center;gap:16px;box-shadow:0 2px 8px rgba(0,0,0,0.06);}
.top-nav-logo{font-size:1.5rem;font-weight:800;color:#1a73e8;letter-spacing:-0.5px;}
.top-nav-sub{color:#5f6368;font-size:0.85rem;border-left:1px solid #dadce0;padding-left:16px;}
.topic-header{background:#ffffff;border:1px solid #e0e4ea;border-radius:12px;padding:20px 28px;margin-bottom:16px;box-shadow:0 1px 6px rgba(0,0,0,0.05);}
.topic-num{font-size:0.78rem;color:#1a73e8;font-weight:600;background:#e8f0fe;border-radius:20px;padding:2px 12px;display:inline-block;margin-bottom:8px;}
.topic-title{font-size:1.5rem;font-weight:700;color:#202124;margin:0;}
.topic-en{font-size:0.85rem;color:#5f6368;margin-top:4px;}
.flow-bar{display:flex;align-items:center;background:#ffffff;border:1px solid #e0e4ea;border-radius:10px;padding:12px 20px;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,0.04);flex-wrap:wrap;gap:4px;}
.flow-step{font-size:0.8rem;font-weight:600;padding:5px 14px;border-radius:20px;color:#9aa0a6;background:#f1f3f4;}
.flow-step.active{background:#1a73e8;color:#ffffff;}
.flow-step.done{background:#e6f4ea;color:#137333;}
.flow-arrow{color:#dadce0;font-size:0.9rem;margin:0 4px;}
.metric-row{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:16px;}
.metric-card{background:#ffffff;border:1px solid #e0e4ea;border-radius:12px;padding:16px 18px;box-shadow:0 1px 4px rgba(0,0,0,0.04);}
.metric-card-label{font-size:0.74rem;color:#5f6368;margin-bottom:5px;font-weight:500;}
.metric-card-value{font-size:1.15rem;font-weight:700;color:#1a73e8;}
.metric-card-value.green{color:#137333;}
.metric-card-value.gray{color:#9aa0a6;}
.news-item{background:#ffffff;border:1px solid #e8eaf0;border-radius:10px;padding:12px 16px;margin:6px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04);}
.news-item-title a{color:#1a0dab;text-decoration:none;font-size:0.9rem;font-weight:600;}
.news-item-title a:hover{text-decoration:underline;}
.news-item-meta{font-size:0.75rem;color:#5f6368;margin-top:4px;}
.paper-item{background:#ffffff;border:1px solid #e8eaf0;border-left:4px solid #1a73e8;border-radius:0 10px 10px 0;padding:14px 18px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04);}
.arxiv-item{background:#ffffff;border:1px solid #e8eaf0;border-left:4px solid #e8710a;border-radius:0 10px 10px 0;padding:14px 18px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,0.04);}
.paper-item-title{font-size:0.9rem;font-weight:600;color:#1a0dab;margin-bottom:4px;}
.paper-item-author{font-size:0.78rem;color:#5f6368;margin-bottom:3px;}
.paper-item-venue{font-size:0.76rem;color:#137333;margin-bottom:6px;}
.paper-item-abs{font-size:0.81rem;color:#3c4043;line-height:1.65;}
.arxiv-badge{display:inline-block;background:#fff3e0;color:#e8710a;border:1px solid #ffcc80;border-radius:4px;padding:1px 8px;font-size:0.72rem;font-weight:700;margin-bottom:4px;}
.scholar-badge{display:inline-block;background:#e8f0fe;color:#1a73e8;border:1px solid #aecbfa;border-radius:4px;padding:1px 8px;font-size:0.72rem;font-weight:700;margin-bottom:4px;}
.select-header{background:#e8f0fe;border:1px solid #c5d8fc;border-radius:8px;padding:10px 16px;margin-bottom:12px;font-size:0.85rem;color:#1557b0;font-weight:600;}
.section-title{font-size:1.05rem;font-weight:700;color:#202124;margin:0 0 14px;padding-bottom:10px;border-bottom:2px solid #e8eaf0;}
.stButton>button{background-color:#1a73e8!important;color:#ffffff!important;border:none!important;border-radius:8px!important;font-family:inherit!important;font-weight:600!important;font-size:0.88rem!important;width:100%!important;}
.stButton>button:hover{background-color:#1557b0!important;box-shadow:0 2px 10px rgba(26,115,232,0.3)!important;}
.stTabs [data-baseweb="tab-list"]{background:#ffffff;border-radius:10px 10px 0 0;border-bottom:2px solid #e8eaf0;padding:0 10px;}
.stTabs [data-baseweb="tab"]{font-family:inherit;font-size:0.88rem;font-weight:500;color:#5f6368;padding:12px 18px;border-bottom:2px solid transparent;margin-bottom:-2px;}
.stTabs [aria-selected="true"]{color:#1a73e8!important;border-bottom-color:#1a73e8!important;font-weight:700!important;}
.stTabs [data-baseweb="tab-panel"]{background:#ffffff;border:1px solid #e8eaf0;border-top:none;border-radius:0 0 10px 10px;padding:24px!important;}
textarea{background:#fafafa!important;color:#202124!important;border:1px solid #dadce0!important;border-radius:8px!important;}
hr{border-color:#e8eaf0!important;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 수집 함수
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
    """arXiv API — HTTPS, 단순 쿼리"""
    try:
        query = urllib.parse.quote(keyword)
        url = f"https://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        headers = {"User-Agent": "Mozilla/5.0 BatteryResearchApp/1.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        # namespace 처리
        text = resp.text
        # atom namespace 제거 후 파싱
        text = text.replace('xmlns="http://www.w3.org/2005/Atom"', '')
        import xml.etree.ElementTree as ET
        root = ET.fromstring(text)

        results = []
        for entry in root.findall("entry"):
            def gt(tag):
                el = entry.find(tag)
                return el.text.strip() if el is not None and el.text else ""

            title   = gt("title").replace("\n", " ").replace("  ", " ")
            summary = gt("summary")[:400]
            pub     = gt("published")[:10]
            link_el = entry.find("id")
            link    = link_el.text.strip() if link_el is not None else ""
            authors = ", ".join(
                a.find("name").text for a in entry.findall("author")
                if a.find("name") is not None
            )[:3*30]

            if title:
                results.append({
                    "title": title, "authors": authors,
                    "abstract": summary, "url": link,
                    "published": pub, "source": "arXiv"
                })
        return results
    except Exception as e:
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
                    "title":    bib.get("title", "No title"),
                    "authors":  bib.get("author", "Unknown"),
                    "year":     bib.get("pub_year", ""),
                    "journal":  bib.get("venue", ""),
                    "abstract": bib.get("abstract", ""),
                    "url":      pub.get("pub_url", ""),
                })
            except StopIteration:
                break
    except:
        pass
    return results

# =====================================================================
# 보고서 생성
# =====================================================================
def generate_report(num, ko, en, bg, keywords, sel_news, sel_papers, sel_arxiv, t):
    today = datetime.now().strftime("%Y-%m-%d")
    kw_str = " / ".join(keywords)
    n_news = len(sel_news); n_papers = len(sel_papers) + len(sel_arxiv)
    abstract = f"{ko}은(는) 배터리 건강 상태(SOH) 추정의 핵심 주제이다. {bg} 본 보고서는 뉴스 {n_news}건, 논문 {n_papers}편을 분석하여 현황과 연구 동향을 체계적으로 정리한다."

    news_ko_sel = [n for n in sel_news if n.get("lang")=="ko"]
    news_en_sel = [n for n in sel_news if n.get("lang")=="en"]

    ref_num = 1; all_refs = []
    for p in sel_papers:
        ref = f"[{ref_num}] {p['authors']} ({p['year']}). {p['title']}."
        if p.get('journal'): ref += f" {p['journal']}."
        if p.get('url'):     ref += f" {p['url']}"
        all_refs.append(ref); ref_num += 1
    for p in sel_arxiv:
        all_refs.append(f"[{ref_num}] {p['authors']} ({p['published'][:4]}). {p['title']}. arXiv. {p['url']}")
        ref_num += 1
    for n in sel_news:
        all_refs.append(f"[{ref_num}] {n['title']}. {n['source']} ({n['published']}). {n['link']}")
        ref_num += 1

    scholar_body = "".join([
        f"\n**[{i}] {p['title']}** ({p['year']}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n"
        for i,p in enumerate(sel_papers,1)
    ]) or "(선택된 Scholar 논문 없음)"

    arxiv_body = "".join([
        f"\n**[{i}] [{p['title']}]({p['url']})** ({p['published'][:7]}) — {p['authors'][:50]}\n\n> {(p['abstract'][:250]+'...') if len(p['abstract'])>250 else p['abstract']}\n"
        for i,p in enumerate(sel_arxiv, len(sel_papers)+1)
    ]) or "(선택된 arXiv 논문 없음)"

    return f"""# {num}. {ko}
## {t['report_title']}

---
**{t['written_date']}:** {today} | **{t['keyword_label']}:** {kw_str}
**{t['ref_book']}:** Gregory Plett - *Battery Management Systems*
**{t['collected_data']}:** {t['metric_news']} {n_news}{t['news_unit']} · {t['metric_paper']} {n_papers}{t['paper_unit']}

---

## {t['abstract']}

{abstract}

**{t['keyword_label']}:** {kw_str}

---

## {t['intro']}

### {t['intro_bg']}
{bg}

배터리 에너지 저장 시스템의 급속한 보급에 따라 {ko} 분야는 BMS의 핵심 기능으로 주목받고 있다.

### {t['intro_obj']}
본 보고서는 {ko}({en})에 관한 최신 연구 동향과 기술 현황을 체계적으로 분석하는 것을 목적으로 한다.

### {t['intro_struct']}
이론적 배경(2장) → 최신 기술 동향(3장) → 선행 연구 검토(4장) → 기술적 분석(5장) → 결론(6장)

---

## {t['theory']}

### {t['theory_def']}
{bg}

- **SOH:** 현재 최대 용량 / 초기 정격 용량 × 100%
- **SOC:** 현재 잔여 용량 / 현재 최대 용량 × 100%
- **내부 저항 R₀:** 배터리 열화의 직접적 지표

### {t['theory_concept']}

| 개념 | 설명 |
|------|------|
{"".join([f"| **{kw}** | {ko} 분야 핵심 요소 |\n" for kw in keywords])}

---

## {t['trends']}

### {t['domestic_trend']}
{"다음은 수집된 국내 최신 뉴스이다." if news_ko_sel else "이번 수집에서 국내 뉴스는 없었다."}
{"".join([f'\n**[뉴스]** [{n["title"]}]({n["link"]})\n> {n["source"]} | {n["published"]}\n' for n in news_ko_sel])}

### {t['foreign_trend']}
{"다음은 수집된 해외 최신 뉴스이다." if news_en_sel else "이번 수집에서 해외 뉴스는 없었다."}
{"".join([f'\n**[News]** [{n["title"]}]({n["link"]})\n> {n["source"]} | {n["published"]}\n' for n in news_en_sel])}

---

## {t['literature']}

### 4.1 Google Scholar 논문
{scholar_body}

### {t['arxiv_review']}
{arxiv_body}

---

## {t['analysis']}

### {t['comparison']}

| 구분 | 주요 방법 | 특징 | 적용 분야 |
|------|----------|------|----------|
| 모델 기반 | 등가 회로 모델 | 구현 용이, 실시간 처리 | BMS 내장 |
| 필터 기반 | EKF / UKF | 높은 정확도, 노이즈 강인성 | 전기차 |
| 데이터 기반 | 머신러닝 / 딥러닝 | 대용량 데이터 필요 | 클라우드 BMS |

### {t['metrics']}
- **정확도:** RMSE, MAE
- **견고성:** 노이즈·온도·초기값 오차에 대한 민감도
- **계산 효율:** 실시간 BMS 적용을 위한 연산 복잡도

### {t['limits']}
1. 실제 차량 환경의 복잡한 동적 부하 조건 재현의 어려움
2. 온도·충방전 패턴 등 다양한 외부 조건에 대한 일반화 부족
3. 센서 오차 및 초기 파라미터 불확실성

---

## {t['conclusion']}

### {t['findings']}
- {ko}은(는) 배터리 BMS의 핵심 기능으로 연구 수요가 지속 증가
- 칼만 필터 계열과 데이터 기반 방법의 융합 연구가 최신 트렌드
- 실시간 처리와 정확도를 동시에 만족하는 경량화 알고리즘 개발이 핵심 과제

### {t['future']}
1. **AI/ML 융합:** 딥러닝 기반 SOH 추정과 물리 기반 모델의 융합
2. **디지털 트윈:** 실시간 배터리 디지털 트윈 활용
3. **차세대 배터리:** 고체 배터리·리튬-황 배터리 적용 방법론 개발
4. **클라우드 BMS:** 집단 지성형 SOH 추정 시스템 구축

---

## {t['references']}

{"".join([f"{r}  \n" for r in all_refs]) if all_refs else "(참고문헌 없음)"}

---
*{t['auto_generated']}*
"""

# =====================================================================
# 세션 초기화
# =====================================================================
for k, v in [("news_ko",[]),("news_en",[]),("papers",[]),("arxiv_papers",[]),
              ("report_text",""),("step",0),("prev_idx",-1),
              ("sel_news",[]),("sel_papers",[]),("sel_arxiv",[]),("ui_lang","ko")]:
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================================================
# 사이드바
# =====================================================================
with st.sidebar:
    lang_choice = st.selectbox("🌐 Language / 언어", list(LANG_OPTIONS.keys()),
                                index=list(LANG_OPTIONS.values()).index(st.session_state["ui_lang"]))
    st.session_state["ui_lang"] = LANG_OPTIONS[lang_choice]
    lang = st.session_state["ui_lang"]
    t = UI[lang]

    # 언어에 맞는 주제 목록 생성
    TOPIC_DISPLAY = get_topic_display(lang)
    TOPIC_MAP     = get_topic_map(lang)

    st.markdown(f"""
    <div style="padding:14px 0 10px;border-bottom:1px solid #e8eaf0;margin-bottom:12px;">
        <div style="font-size:1rem;font-weight:700;color:#1a73e8;">{t['sidebar_title']}</div>
        <div style="font-size:0.75rem;color:#9aa0a6;margin-top:2px;">{t['sidebar_sub']}</div>
    </div>
    """, unsafe_allow_html=True)

    selected_display = st.selectbox("", TOPIC_DISPLAY, label_visibility="collapsed")
    idx = TOPIC_DISPLAY.index(selected_display)
    num, ko, en, bg, keywords = TOPIC_MAP[selected_display]

    if st.session_state["prev_idx"] != idx:
        for k2 in ["news_ko","news_en","papers","arxiv_papers","report_text","sel_news","sel_papers","sel_arxiv"]:
            st.session_state[k2] = [] if k2 != "report_text" else ""
        st.session_state["step"] = 0
        st.session_state["prev_idx"] = idx

    st.markdown(f"""
    <div style="background:#e8f0fe;border-radius:8px;padding:10px 14px;margin:10px 0;">
        <div style="font-size:0.72rem;color:#1557b0;font-weight:600;margin-bottom:3px;">{t['sidebar_keyword']}</div>
        <div style="font-size:0.8rem;color:#1a73e8;font-weight:500;line-height:1.5;">{en}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='font-size:0.8rem;font-weight:600;color:#5f6368;margin:12px 0 8px;'>{t['sidebar_progress']}</div>", unsafe_allow_html=True)
    step = st.session_state["step"]
    for i, label in enumerate(t["steps"], 1):
        done = step >= i
        color = "#137333" if done else "#9aa0a6"
        st.markdown(f"<div style='color:{color};font-size:0.82rem;font-weight:{'600' if done else '400'};padding:5px 0;border-bottom:1px solid #f1f3f4;'>{'✅' if done else '○'} {label}</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:#bdc1c6;font-size:0.72rem;margin-top:12px;'>{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)

# =====================================================================
# 메인
# =====================================================================
# 사이드바에서 이미 설정된 lang, t, TOPIC_MAP 사용
st.markdown(f'<div class="top-nav"><div class="top-nav-logo">{t["app_title"]}</div><div class="top-nav-sub">{t["app_sub"]}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="topic-header"><div class="topic-num">{t["topic_chapter"]} · {num}</div><div class="topic-title">{num}. {selected_display.split(". ",1)[1]}</div><div class="topic-en">{en}</div></div>', unsafe_allow_html=True)

step = st.session_state["step"]
def fc(n): return "done" if step > n else ("active" if step == n else "")
flow_html = "".join([f'<div class="flow-step {fc(i)}">{t["flow"][i]}</div>' + (f'<div class="flow-arrow">→</div>' if i<len(t["flow"])-1 else "") for i in range(len(t["flow"]))])
st.markdown(f'<div class="flow-bar">{flow_html}</div>', unsafe_allow_html=True)

news_cnt  = len(st.session_state["news_ko"]) + len(st.session_state["news_en"])
paper_cnt = len(st.session_state["papers"]) + len(st.session_state["arxiv_papers"])
sel_total = len(st.session_state["sel_news"]) + len(st.session_state["sel_papers"]) + len(st.session_state["sel_arxiv"])
has_rpt   = bool(st.session_state["report_text"])

st.markdown(f"""<div class="metric-row">
    <div class="metric-card"><div class="metric-card-label">{t['metric_topic']}</div><div class="metric-card-value">{num}</div></div>
    <div class="metric-card"><div class="metric-card-label">{t['metric_news']}</div><div class="metric-card-value {'green' if news_cnt else 'gray'}">{news_cnt}{t['news_unit']}</div></div>
    <div class="metric-card"><div class="metric-card-label">{t['metric_paper']}</div><div class="metric-card-value {'green' if paper_cnt else 'gray'}">{paper_cnt}{t['paper_unit']}</div></div>
    <div class="metric-card"><div class="metric-card-label">{t['metric_selected']}</div><div class="metric-card-value {'green' if sel_total else 'gray'}">{sel_total}</div></div>
    <div class="metric-card"><div class="metric-card-label">{t['metric_report']}</div><div class="metric-card-value {'green' if has_rpt else 'gray'}">{t['report_done'] if has_rpt else t['report_wait']}</div></div>
</div>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

# ── Tab 1: 뉴스 ──
with tab1:
    st.markdown(f'<div class="section-title">{t["tab1"]}</div>', unsafe_allow_html=True)
    c1, c2, _ = st.columns([2,2,6])
    with c1: run_news = st.button(t["news_collect"], type="primary", use_container_width=True)
    with c2:
        if st.button(t["reset"], key="r_news", use_container_width=True):
            st.session_state["news_ko"] = []; st.session_state["news_en"] = []; st.rerun()

    if run_news:
        prog = st.progress(0); status = st.empty()
        status.info("🇰🇷 ...")
        prog.progress(25)
        raw_ko = fetch_news(ko + " 배터리", "ko", "KR", "KR:ko", 6)
        st.session_state["news_ko"] = [{"title":e.title,"link":e.link,"lang":"ko","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_ko]
        status.info("🌍 ...")
        prog.progress(75)
        raw_en = fetch_news(en, "en", "US", "US:en", 6)
        st.session_state["news_en"] = [{"title":e.title,"link":e.link,"lang":"en","published":getattr(e,'published',''),"source":(e.get('source') or {}).get('title','Google News')} for e in raw_en]
        prog.progress(100); status.empty(); prog.empty()
        if st.session_state["step"] < 1: st.session_state["step"] = 1
        st.rerun()

    ko_list = st.session_state["news_ko"]; en_list = st.session_state["news_en"]
    if ko_list or en_list:
        st.success(f"✅ {len(ko_list)+len(en_list)}{t['news_unit']} {t['collected']} — {t['select_tip']}")
        col_ko, col_en = st.columns(2)
        with col_ko:
            st.markdown(f"<div style='font-weight:700;margin-bottom:8px;'>{t['domestic_news']} ({len(ko_list)}{t['news_unit']})</div>", unsafe_allow_html=True)
            for item in ko_list:
                st.markdown(f'<div class="news-item"><div class="news-item-title"><a href="{item["link"]}" target="_blank">{item["title"]}</a></div><div class="news-item-meta">📅 {item["published"]} · {item["source"]}</div></div>', unsafe_allow_html=True)
        with col_en:
            st.markdown(f"<div style='font-weight:700;margin-bottom:8px;'>{t['foreign_news']} ({len(en_list)}{t['news_unit']})</div>", unsafe_allow_html=True)
            for item in en_list:
                st.markdown(f'<div class="news-item"><div class="news-item-title"><a href="{item["link"]}" target="_blank">{item["title"]}</a></div><div class="news-item-meta">📅 {item["published"]} · {item["source"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:40px;color:#9aa0a6;"><div style="font-size:2.5rem;margin-bottom:12px;">📰</div><div>{t["news_collect"]}</div></div>', unsafe_allow_html=True)

# ── Tab 2: 논문 ──
with tab2:
    st.markdown(f'<div class="section-title">{t["tab2"]}</div>', unsafe_allow_html=True)

    # arXiv
    st.markdown(f'<div style="background:#fff3e0;border:1px solid #ffcc80;border-radius:8px;padding:10px 16px;margin-bottom:12px;font-size:0.84rem;color:#7f4f00;">💡 {t["arxiv_info"]}</div>', unsafe_allow_html=True)
    ca1, ca2, _ = st.columns([2,2,6])
    with ca1: run_arxiv = st.button(t["arxiv_search"], type="primary", use_container_width=True)
    with ca2:
        if st.button(t["reset"], key="r_arxiv", use_container_width=True):
            st.session_state["arxiv_papers"] = []; st.rerun()

    if run_arxiv:
        with st.spinner(t["searching_arxiv"]):
            results = fetch_arxiv(en, 5)
        if results:
            st.session_state["arxiv_papers"] = results
            if st.session_state["step"] < 2: st.session_state["step"] = 2
            st.rerun()
        else:
            st.error(t["arxiv_no_result"])

    arxiv_list = st.session_state["arxiv_papers"]
    if arxiv_list:
        st.success(f"✅ arXiv {len(arxiv_list)}{t['paper_unit']} {t['papers_collected']}")
        for i, p in enumerate(arxiv_list, 1):
            abs_t = (p['abstract'][:280]+"...") if len(p['abstract'])>280 else p['abstract']
            st.markdown(f"""<div class="arxiv-item">
                <div class="arxiv-badge">arXiv</div>
                <div class="paper-item-title">[{i}] <a href="{p['url']}" target="_blank" style="color:#1a0dab;">{p['title']}</a></div>
                <div class="paper-item-author">👤 {p['authors']} | 📅 {p['published']}</div>
                <div class="paper-item-abs">{abs_t}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Scholar
    st.warning(t["scholar_warning"])
    cs1, cs2, _ = st.columns([2,2,6])
    with cs1: run_scholar = st.button(t["scholar_search"], type="primary", use_container_width=True)
    with cs2:
        if st.button(t["reset"], key="r_scholar", use_container_width=True):
            st.session_state["papers"] = []; st.rerun()

    if run_scholar:
        with st.spinner(t["searching_scholar"]):
            scholar_results = fetch_scholar(en, 4)
        st.session_state["papers"] = scholar_results
        if st.session_state["step"] < 2: st.session_state["step"] = 2
        st.rerun()

    scholar_list = st.session_state["papers"]
    if scholar_list:
        st.success(f"✅ Google Scholar {len(scholar_list)}{t['paper_unit']} {t['papers_collected']}")
        for i, p in enumerate(scholar_list, 1):
            abs_t = (p['abstract'][:280]+"...") if len(p['abstract'])>280 else p['abstract']
            link_html = f"<a href='{p['url']}' target='_blank' style='color:#1a73e8;font-size:0.8rem;'>➡️</a>" if p.get('url') else ""
            st.markdown(f"""<div class="paper-item">
                <div class="scholar-badge">Scholar</div>
                <div class="paper-item-title">[{i}] {p['title']} ({p['year']}) {link_html}</div>
                <div class="paper-item-author">👤 {p['authors']}</div>
                {"<div class='paper-item-venue'>📔 " + p['journal'] + "</div>" if p.get('journal') else ""}
                <div class="paper-item-abs">{abs_t}</div>
            </div>""", unsafe_allow_html=True)

# ── Tab 3: 선택 & 보고서 ──
with tab3:
    st.markdown(f'<div class="section-title">{t["tab3"]}</div>', unsafe_allow_html=True)
    all_news    = st.session_state["news_ko"] + st.session_state["news_en"]
    all_scholar = st.session_state["papers"]
    all_arxiv   = st.session_state["arxiv_papers"]

    if not all_news and not all_scholar and not all_arxiv:
        st.info(t["no_data"])
    else:
        sel_news_list=[]; sel_scholar_list=[]; sel_arxiv_list=[]

        if all_news:
            st.markdown(f'<div class="select-header">{t["select_news_header"]}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            for i, item in enumerate(all_news):
                flag = "🇰🇷" if item.get("lang")=="ko" else "🌍"
                with (col1 if i%2==0 else col2):
                    if st.checkbox(f"{flag} {item['title'][:55]}{'...' if len(item['title'])>55 else ''}", key=f"nc_{i}"):
                        sel_news_list.append(item)

        if all_arxiv or all_scholar:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="select-header">{t["select_paper_header"]}</div>', unsafe_allow_html=True)
            if all_arxiv:
                st.markdown("<div style='font-size:0.84rem;font-weight:700;color:#e8710a;margin:8px 0 4px;'>📄 arXiv</div>", unsafe_allow_html=True)
                for i, p in enumerate(all_arxiv):
                    if st.checkbox(f"[arXiv] {p['title'][:60]}{'...' if len(p['title'])>60 else ''} ({p['published'][:7]})", key=f"ax_{i}"):
                        sel_arxiv_list.append(p)
            if all_scholar:
                st.markdown("<div style='font-size:0.84rem;font-weight:700;color:#1a73e8;margin:8px 0 4px;'>📚 Google Scholar</div>", unsafe_allow_html=True)
                for i, p in enumerate(all_scholar):
                    if st.checkbox(f"[Scholar] {p['title'][:60]}{'...' if len(p['title'])>60 else ''} ({p['year']})", key=f"sc_{i}"):
                        sel_scholar_list.append(p)

        st.session_state["sel_news"]=sel_news_list; st.session_state["sel_papers"]=sel_scholar_list; st.session_state["sel_arxiv"]=sel_arxiv_list
        total_sel = len(sel_news_list)+len(sel_scholar_list)+len(sel_arxiv_list)

        st.markdown("<br>", unsafe_allow_html=True)
        if total_sel > 0:
            st.success(f"✅ {t['metric_news']} {len(sel_news_list)}{t['news_unit']} + arXiv {len(sel_arxiv_list)}{t['paper_unit']} + Scholar {len(sel_scholar_list)}{t['paper_unit']}")
        else:
            st.warning("⚠️ 최소 1개 이상 선택하세요.")

        st.markdown("---")
        col_gen, _ = st.columns([3,7])
        with col_gen:
            gen_btn = st.button(t["gen_report"], type="primary", use_container_width=True, disabled=(total_sel==0))

        if gen_btn and total_sel > 0:
            with st.spinner("..."):
                time.sleep(0.3)
                report = generate_report(num, ko, en, bg, keywords, sel_news_list, sel_scholar_list, sel_arxiv_list, t)
                st.session_state["report_text"] = report
                if st.session_state["step"] < 4: st.session_state["step"] = 4
            st.success(f"✅ {t['report_done']} → {t['tab4']}")
            st.markdown("---")
            st.markdown(report)
        elif st.session_state["report_text"] and not gen_btn:
            st.markdown("---")
            st.markdown(st.session_state["report_text"])

# ── Tab 4: 다운로드 ──
with tab4:
    st.markdown(f'<div class="section-title">{t["tab4"]}</div>', unsafe_allow_html=True)
    rpt = st.session_state["report_text"]
    if rpt:
        st.success(f"✅ {t['report_done']}")
        edited = st.text_area(t["edit_label"], value=rpt, height=400, key=f"final_{num}_{lang}")
        st.session_state["report_text"] = edited
        st.markdown("<br>", unsafe_allow_html=True)
        file_base = f"BMS_SOH_{num}_{datetime.now().strftime('%Y%m%d')}"
        c1, c2, c3 = st.columns(3)
        with c1: st.download_button(t["download_txt"], data=edited, file_name=f"{file_base}.txt", mime="text/plain", type="primary", use_container_width=True)
        with c2: st.download_button(t["download_md"], data=edited, file_name=f"{file_base}.md", mime="text/markdown", type="primary", use_container_width=True)
        with c3:
            if st.button(t["print_pdf"], use_container_width=True): st.info("Ctrl+P → PDF")
        st.markdown("---")
        st.markdown(f"### {t['preview']}")
        st.markdown(edited)
    else:
        st.markdown(f'<div style="text-align:center;padding:50px;color:#9aa0a6;"><div style="font-size:2.5rem;margin-bottom:14px;">📋</div><div style="font-size:1rem;font-weight:600;color:#5f6368;margin-bottom:8px;">{t["no_report"]}</div><div>{t["no_report_guide"]}</div></div>', unsafe_allow_html=True)
