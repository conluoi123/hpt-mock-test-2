# SKILLS.md — Checklist kỹ năng & công cụ (Generic)

> Dùng file này như **menu tra cứu nhanh** khi làm bài — không cần dùng hết, chỉ dùng đúng chỗ cần.

## 1. Core Stack

- **Python**: pandas, numpy, matplotlib/seaborn, plotly (interactive), scikit-learn
- **Notebook**: Jupyter — chia section bằng markdown headers + `viz_utils.section()`
- **Dashboard**: HTML/CSS/JS + Chart.js — mở trực tiếp trình duyệt
- **Module**: `src/viz_utils.py` — design system, chart helpers, KPI cards

## 2. Skill map theo từng Phase

### Phase 0 — Business Understanding
- Lập Data Dictionary giải thích các trường dữ liệu bằng ngôn ngữ dễ hiểu.
- Xác định Business Objective (Mục tiêu kinh doanh).
- Lên danh sách các giả thuyết (Hypotheses) cần kiểm định.

### Phase 1 — Data Understanding & Quality
- `quick_profile(df)` — overview 1 lệnh
- `df.info()`, `df.describe()`, `df.isnull().sum()`, `df.duplicated().sum()`
- Phát hiện lỗi "ẩn": cột số đọc thành string, date chưa parse, missing "giả" (string rỗng)
- Output: Data Quality Issues Log (bảng: issue → xử lý → lý do)

### Phase 2 — EDA & Insight Discovery
- **Framework Bắt Buộc (Business Questions-Driven EDA)**: 
  - KHÔNG vẽ biểu đồ vô định. Luôn BẮT ĐẦU bằng việc tự đặt ra các Câu hỏi Kinh doanh (Business Questions - BQs) mang tính thực tiễn cao.
  - Mỗi section trong EDA phải đi theo luồng: Đặt câu hỏi $\rightarrow$ Vẽ biểu đồ kiểm chứng $\rightarrow$ Rút ra Insight $\rightarrow$ "So What?" (Hành động tiếp theo).
- **Groupby analysis**: `groupby().agg()`, crosstab, pivot_table
- **Chart notebook** (dùng `viz_utils`):
  - `bar_chart()` — so sánh categories
  - `line_chart()` — xu hướng thời gian
  - `pareto_chart()` — 80/20 analysis
  - `sns.heatmap()` — correlation matrix
  - `sns.boxplot()` — phân bố & outlier
  - `plotly.express` — interactive khi cần khám phá sâu
- **KPI display**: `kpi_cards([...])` — metric tổng quan
- **Section header**: `section('Title', 'Subtitle')` — chia phần rõ

### Phase 3 — Feature Engineering
- Xử lý các biến phân loại (Categorical): dùng OneHotEncoder trong pipeline hoặc Ordinal Encoding.
- Tạo features có ý nghĩa business (ví dụ: tỷ lệ, rank, bins, flags, Customer Lifetime Value, RFM).
- Giải thích "vì sao tạo" cho từng feature.
- Chuẩn hóa phân phối: Log Transform cho biến lệch, Binning cho nhóm tuổi / thu nhập.
- Verify tương quan với target: groupby hoặc correlation heatmap (loại bỏ biến bị đa cộng tuyến - Multicollinearity).
- Đảm bảo dữ liệu đầu ra không có missing values, sẵn sàng 100% cho thuật toán Machine Learning.

### Phase 4 — Modeling
- Train/test split (stratify nếu imbalanced)
- Baseline: Logistic Regression / Decision Tree → dễ giải thích
- Nâng cao: Random Forest / XGBoost / LightGBM → so sánh
- Xử lý imbalanced: `class_weight='balanced'` hoặc SMOTE
- **Classification metrics**: ưu tiên Recall/F1/ROC-AUC > Accuracy
- **Regression metrics**: RMSE, MAE, R²

### Phase 5 — Interpretation
- `feature_importances_` (tree-based), coefficients (logistic)
- SHAP values (nếu đủ thời gian)
- Dịch sang business language: "Yếu tố X làm tăng nguy cơ Y gấp Z lần"

### Phase 6 — Dashboard (Streamlit App) 🆕
- **Dashboard Checklist (Bắt buộc phải có đủ 5 yếu tố)**:
  1. **[x] KPI**: Các chỉ số Executive Summary to rõ ràng ở trên cùng (VD: Tổng Doanh thu, Tỷ lệ Tồn kho rủi ro).
  2. **[x] Filters**: Bộ lọc tương tác (Theo Cửa hàng, Nhóm sản phẩm, Khoảng thời gian) trên Sidebar để user tự phân tích.
  3. **[x] Charts**: Biểu đồ trực quan (Dùng Plotly hoặc Altair) tích hợp ngay trên form.
  4. **[x] Insights**: Phần giải nghĩa tự động (VD: Text box hiển thị cảnh báo khi tồn kho < Reorder Point).
  5. **[x] Recommendation**: Gợi ý hành động do Model xuất ra (VD: "Đề xuất giảm giá 15% để xả kho").
- **Best Practice Streamlit**:
  - Dùng `st.columns()` để chia layout cho KPI và Chart.
  - Dùng `st.sidebar` cho toàn bộ Filters.
  - Render Markdown để báo cáo Insights.

### Phase 7 — Report & Recommendation
- **Report structure**:
  1. Executive Summary (cho người không chuyên)
  2. Bối cảnh & Yêu cầu bài toán
  3. Data Quality & EDA Insight
  4. Feature Engineering & Modeling (nếu có)
  5. Dashboard Demo URL
  6. Khuyến nghị: Short-term (0-30 ngày) + Long-term (hệ thống)
- **Nguyên tắc**: recommendation phải actionable, giao việc được ngay

## 3. `viz_utils.py` — Quick Reference

| Function | Mô tả | Ví dụ |
|----------|--------|-------|
| `setup()` | Áp dụng design system | Gọi 1 lần đầu notebook |
| `section(title, sub)` | Header gradient | `section('EDA', 'Phân tích khám phá')` |
| `kpi_cards([...])` | KPI cards HTML | `kpi_cards([{'label':..., 'value':..., 'color':...}])` |
| `kpi_card_mpl(ax,...)` | KPI card trên matplotlib | Dùng trong figure multi-panel |
| `bar_chart(x,y,title)` | Bar chart + labels | `bar_chart(cats, vals, 'Title')` |
| `line_chart(x,ds,title)` | Line chart + fill | `line_chart(months, [{'y':..., 'label':...}], 'Title')` |
| `pareto_chart(l,v,title)` | Pareto bar + cumulative | `pareto_chart(reasons, amounts, 'Title')` |
| `clean_spines(ax)` | Clean axis borders | Gọi sau mỗi custom chart |
| `clean_ax(ax, title, ...)` | Full axis cleanup | Title + labels + subtitle + spines |
| `label_bars_v(ax)` | Labels trên vertical bars | Sau `ax.bar(...)` |
| `label_bars_h(ax)` | Labels trên horizontal bars | Sau `ax.barh(...)` |
| `fmt_pct(val)` | Format phần trăm | `fmt_pct(0.097)` → `'9.7%'` |
| `fmt_currency(val)` | Format tiền VNĐ | `fmt_currency(15.68e9)` → `'15 Tỷ'` |
| `fmt_num(val)` | Format số | `fmt_num(24238)` → `'24,238'` |
| `quick_profile(df)` | Data profile nhanh | `quick_profile(df)` |
| `export_dashboard_json(d)` | Export JSON cho dashboard | `export_dashboard_json(data_dict)` |
| `save_fig(fig, name)` | Lưu figure | `save_fig(fig, '01_chart.png')` |

## 4. PALETTE Reference

| Key | Hex | Dùng cho |
|-----|-----|----------|
| `primary` | `#2D6A4F` | Metric chính, doanh thu |
| `secondary` | `#52B788` | Metric phụ tích cực |
| `accent` | `#F4A261` | Highlight, cảnh báo nhẹ |
| `danger` | `#E76F51` | Metric xấu, cancel, loss |
| `blue` | `#457B9D` | So sánh, metric phụ |
| `purple` | `#9B5DE5` | AOV, metric đặc biệt |
| `stockout` | `#E63946` | Hết hàng |
| `overstock` | `#F4A261` | Tồn kho dư |
| `stable` | `#2A9D8F` | Ổn định, đủ hàng |
| `warning` | `#E9C46A` | Cảnh báo |
| `neutral` | `#6C757D` | Baseline, reference |

## 5. Soft Skills (Rubric nhấn mạnh)

- **Business Understanding**: luôn quay lại câu hỏi business đầu đề
- **Report Quality**: viết cho người không chuyên kỹ thuật
- **Practical Recommendation**: actionable, giao việc được ngay
- **Dashboard Quality**: premium, responsive, dễ đọc
