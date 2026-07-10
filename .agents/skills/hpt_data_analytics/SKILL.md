---
name: HPT Data Analytics & Visualization
description: >
  Skill for building professional data analytics visualizations and dashboards.
  Covers notebook EDA charts (matplotlib/seaborn), KPI cards (HTML in notebook),
  web dashboards (HTML/CSS/JS + Chart.js), and end-to-end report workflow.
  Applies to any dataset — e-commerce, churn, inventory, financial analysis, etc.
---

# HPT Data Analytics & Visualization Skill

## Khi nào kích hoạt skill này

- Khi user yêu cầu phân tích dữ liệu, EDA, trực quan hóa
- Khi user yêu cầu tạo dashboard, biểu đồ, KPI cards
- Khi user yêu cầu báo cáo phân tích với chart đẹp
- Khi user làm bài test Data Analytics & AI

---

## 1. Design System — Bắt buộc tuân theo

### 1.1 Color Palette

```python
PALETTE = {
    'primary':   '#2D6A4F',   # Xanh lá đậm — doanh thu, metric chính
    'secondary': '#52B788',   # Xanh lá nhạt — metric phụ tích cực
    'accent':    '#F4A261',   # Cam — cảnh báo nhẹ, highlight
    'danger':    '#E76F51',   # Đỏ cam — metric xấu, cancel, loss
    'neutral':   '#6C757D',   # Xám — baseline, reference
    'light':     '#F8F9FA',   # Nền sáng
    'dark':      '#212529',   # Text đậm
    'blue':      '#457B9D',   # Xanh dương — metric phụ, so sánh
    'purple':    '#9B5DE5',   # Tím — AOV, metric đặc biệt
    'stockout':  '#E63946',   # Đỏ tươi — hết hàng
    'overstock': '#F4A261',   # Cam — tồn kho dư
    'stable':    '#2A9D8F',   # Xanh ngọc — ổn định
    'warning':   '#E9C46A',   # Vàng — cảnh báo
}
```

**Quy tắc chọn màu:**
- Metric tích cực → `primary` hoặc `secondary`
- Metric tiêu cực → `danger` hoặc `stockout`
- So sánh 2 loại → `primary` vs `blue`
- Cảnh báo → `accent` hoặc `warning`
- Bar chart nhiều category → dùng list: `[primary, secondary, stable, blue, accent, purple]`
- Bar chart highlight worst → worst dùng `danger`, còn lại dùng `secondary`

### 1.2 Typography & Layout

```python
plt.rcParams.update({
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
    'axes.edgecolor':    '#DDDDDD',
    'axes.titleweight':  'bold',
    'axes.titlecolor':   '#2B3A42',
    'axes.labelcolor':   '#2B3A42',
    'xtick.color':       '#5B6D74',
    'ytick.color':       '#5B6D74',
    'font.size':         11,
    'axes.titlesize':    14,
    'axes.labelsize':    12,
    'xtick.labelsize':   10,
    'ytick.labelsize':   10,
    'legend.fontsize':   10,
    'figure.titlesize':  16,
    'grid.color':        '#E5E5E5',
    'grid.linestyle':    '--',
    'grid.linewidth':    0.6,
    'legend.frameon':    False,
    'figure.dpi':        120,
})
sns.set_style('whitegrid')
```

### 1.3 Spine Formatting — Áp dụng cho MỌI chart

```python
def format_spines(ax, right_border=False):
    ax.spines['top'].set_visible(False)
    if not right_border:
        ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.tick_params(colors='#5B6D74', which='both')
    ax.yaxis.label.set_color('#2B3A42')
    ax.xaxis.label.set_color('#2B3A42')
    ax.title.set_color('#2B3A42')
```

**Bắt buộc**: gọi `format_spines(ax)` sau mỗi chart. Dùng `right_border=True` khi có twinx (trục phải).

---

## 2. Chart Patterns — Template cho từng loại

### 2.1 Bar Chart (So sánh)

```python
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(x_labels, values, color=PALETTE['primary'], alpha=0.9, edgecolor='white')
# Gắn label lên đầu mỗi bar:
for bar in ax.patches:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval * 1.02,
            f'{yval:.1f}', ha='center', va='bottom',
            fontsize=10, fontweight='bold', color='#2B3A42')
ax.set_title('Tiêu đề tiếng Việt', fontsize=14)
ax.set_ylabel('Đơn vị')
format_spines(ax)
plt.tight_layout()
```

### 2.2 Horizontal Bar (Ranking / Pareto)

```python
fig, ax = plt.subplots(figsize=(12, 6))
# Sort ascending để item lớn nhất ở trên
data_sorted = data.sort_values(ascending=True)
ax.barh(data_sorted.index, data_sorted.values, color=PALETTE['blue'], alpha=0.9)
# Label ở cuối bar:
max_x = ax.get_xlim()[1]
for bar in ax.patches:
    xval = bar.get_width()
    ax.text(xval + max_x * 0.01, bar.get_y() + bar.get_height()/2,
            f'{xval:,.0f}', ha='left', va='center',
            fontsize=10, fontweight='bold', color='#2B3A42')
format_spines(ax)
```

### 2.3 Line Chart (Xu hướng thời gian)

```python
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(x, y1, label='Revenue', color=PALETTE['primary'], lw=2)
ax.plot(x, y2, label='Profit', color=PALETTE['blue'], lw=2)
ax.fill_between(x, y1, alpha=0.12, color=PALETTE['primary'])  # Area fill nhẹ
ax.set_title('Xu hướng theo Tháng')
ax.legend()
format_spines(ax)
```

### 2.4 Multi-panel (2x2 hoặc 1x3)

```python
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Tiêu đề tổng', fontsize=14, fontweight='bold', y=1.02)
# Mỗi panel:
axes[0].bar(...)
axes[0].set_title('Panel 1', fontweight='bold', fontsize=12)
format_spines(axes[0])
# ... tương tự cho axes[1], axes[2]
plt.tight_layout()
```

### 2.5 Heatmap

```python
sns.heatmap(pivot_table, ax=ax, annot=True, fmt='.1f',
            cmap='Reds', linewidths=0.5,
            cbar_kws={'label': 'Label (%)'})
ax.set_title('Tiêu đề')
```

### 2.6 Scatter + Regression Line

```python
ax.scatter(x, y, alpha=0.15, s=15, color=PALETTE['neutral'])
z = np.polyfit(x, y, 1)
x_reg = np.linspace(x.min(), x.max(), 100)
ax.plot(x_reg, np.poly1d(z)(x_reg), color=PALETTE['danger'], lw=2.5)
# Annotation box cho correlation:
r, p = pearsonr(x, y)
ax.text(0.05, 0.95, f'r = {r:.3f}\np = {p:.4f}',
        transform=ax.transAxes, va='top', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='white',
                  edgecolor=PALETTE['danger'], alpha=0.8))
```

### 2.7 Pareto Chart (Bar + Cumulative Line)

```python
fig, ax = plt.subplots()
ax2 = ax.twinx()
# Bars (sorted desc)
ax.bar(range(len(values)), values, color=[PALETTE['danger'] if i < 2 else PALETTE['accent'] for i in range(len(values))], alpha=0.85)
# Cumulative line
cum_pct = values.cumsum() / values.sum() * 100
ax2.plot(range(len(values)), cum_pct, color=PALETTE['blue'], lw=2.5, marker='o', markersize=6)
ax2.axhline(80, color='gray', ls='--', lw=1.2, alpha=0.7)
format_spines(ax, right_border=True)
```

---

## 3. KPI Cards — Render HTML trong Notebook

### Pattern chuẩn:

```python
def display_kpi_cards(cards):
    """cards = [{'label': 'Tổng DT', 'value': '15.68 Tỷ', 'color': '#2D6A4F'}, ...]"""
    html = '<div style="display:flex; gap:15px; flex-wrap:wrap; margin:15px 0;">'
    for card in cards:
        color = card.get('color', '#2D6A4F')
        html += f"""
        <div style="flex:1; min-width:180px; background:white;
                    border-left:5px solid {color}; padding:15px;
                    border-radius:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.08);">
            <p style="margin:0; font-size:12px; color:#7f8c8d;
                      text-transform:uppercase; letter-spacing:0.04em;">
                {card['label']}</p>
            <p style="margin:8px 0 0 0; font-size:24px; font-weight:700;
                      color:#2B3A42;">{card['value']}</p>
        </div>"""
    html += '</div>'
    display(HTML(html))
```

### Quy tắc KPI card:
- Label: UPPERCASE, font 12px, màu `#7f8c8d`
- Value: font 24px, bold 700, màu `#2B3A42`
- Border-left 5px solid → dùng màu semantic (xanh = tốt, đỏ = xấu, cam = warning)
- Shadow nhẹ: `0 2px 4px rgba(0,0,0,0.08)`
- Min-width: 180px, flex:1 cho responsive

### KPI card kiểu matplotlib (trong figure):

```python
def _kpi_card(ax, title, value, subtitle, color):
    ax.axis('off')
    ax.plot([0.05, 0.05], [0.1, 0.9], color=color, lw=4, transform=ax.transAxes)
    ax.text(0.1, 0.70, title.upper(), fontsize=10, color='#7f8c8d',
            fontweight='bold', transform=ax.transAxes)
    ax.text(0.1, 0.35, value, fontsize=24, color='#2B3A42',
            fontweight='bold', transform=ax.transAxes)
    ax.text(0.1, 0.10, subtitle, fontsize=10, color='#7f8c8d',
            transform=ax.transAxes)
```

---

## 4. Section Headers — Cho notebook dashboard-style

```python
def display_section_header(title, subtitle=''):
    html = f"""
    <div style="background: linear-gradient(135deg, #1B4332, #2D6A4F);
                padding: 18px 25px; border-radius: 8px; margin: 25px 0 15px 0;">
        <h3 style="color:white; margin:0; font-size:16px; font-weight:700;">
            {title}</h3>
        <p style="color:rgba(255,255,255,0.7); margin:5px 0 0 0; font-size:13px;">
            {subtitle}</p>
    </div>
    """
    display(HTML(html))
```

---

## 5. Formatting Helpers

```python
def _fmt_percent(val):
    return f"{val*100:.1f}%" if val < 1 else f"{val:.1f}%"

def _fmt_currency(val, decimals=0):
    if val >= 1e9:   return f"{val/1e9:.{decimals}f} Tỷ"
    if val >= 1e6:   return f"{val/1e6:.1f} Tr"
    return f"{val:,.0f}"

def _fmt_number(val, decimals=0):
    return f"{val:,.{decimals}f}"
```

**Quy tắc format:**
- Tiền VNĐ ≥ 1 tỷ → "X.XX Tỷ"
- Tiền VNĐ ≥ 1 triệu → "X.X Tr"
- Tiền nhỏ → "X,XXX" (dùng comma separator)
- Phần trăm < 1 → nhân 100, thêm %
- Phần trăm ≥ 1 → giữ nguyên, thêm %

---

## 6. Figure Saving Convention

```python
FIG_DIR = BASE_DIR / 'figures'
FIG_DIR.mkdir(exist_ok=True, parents=True)

# Naming: XX_descriptive_name.png
# 00_average_revenue_trends.png
# 01_sales_revenue_trend.png
# 08_returns_cancellations_deepdive.png

fig.savefig(FIG_DIR / 'XX_chart_name.png', dpi=150, bbox_inches='tight')
```

---

## 7. Workflow: Notebook → Web Dashboard

### Bước 1: Tính KPIs trong notebook
```python
kpis = {
    'total_revenue': master_df['net_revenue'].sum(),
    'gross_margin': ...,
    'cancel_rate': ...,
    # ... tất cả metric cần hiển thị
}
```

### Bước 2: Export JSON
```python
import json

dashboard_data = {
    'kpis': [
        {'label': 'Tổng Doanh Thu', 'value': f"{kpis['total_revenue']/1e9:.2f} Tỷ", 'color': PALETTE['primary']},
        {'label': 'Gross Margin', 'value': f"{kpis['gross_margin']:.1f}%", 'color': PALETTE['secondary']},
        # ...
    ],
    'charts': {
        'revenue_by_month': {
            'labels': monthly['YearMonth'].tolist(),
            'datasets': [
                {'label': 'Revenue', 'data': (monthly['Revenue']/1e6).tolist(), 'color': PALETTE['primary']},
                {'label': 'Profit', 'data': (monthly['Profit']/1e6).tolist(), 'color': PALETTE['blue']},
            ]
        },
        # ... thêm chart data khác
    }
}

with open('dashboard/js/data.js', 'w', encoding='utf-8') as f:
    f.write(f'const DASHBOARD_DATA = {json.dumps(dashboard_data, ensure_ascii=False, indent=2)};')
```

### Bước 3: Dashboard HTML đọc `data.js` → render Chart.js
(Xem template trong `resources/components/`)

---

## 8. Anti-patterns — KHÔNG làm

| ❌ Sai | ✅ Đúng |
|--------|---------|
| Dùng màu mặc định matplotlib | Dùng PALETTE semantic |
| Chart không có title tiếng Việt | Mỗi chart có title + ylabel tiếng Việt |
| Để spine top + right | Luôn `format_spines(ax)` |
| Bar chart không có label số | Luôn gắn label lên bar |
| figsize quá nhỏ `(6,4)` | Tối thiểu `(10,5)` cho single, `(18,5)` cho multi |
| Lưu figure không `bbox_inches='tight'` | Luôn `bbox_inches='tight'` |
| KPI hiển thị bằng `print()` | Dùng HTML cards với `display(HTML(...))` |
| Grid quá đậm | Grid nhẹ: `#E5E5E5`, dashed, linewidth 0.6 |
| Legend có frame | `legend.frameon = False` |

---

## 9. Data Pipeline & Modular Workflow (CỰC KỲ QUAN TRỌNG)

Khi được yêu cầu xây dựng một dự án phân tích (như Mock Assessment), **KHÔNG BAO GIỜ** dồn mọi thứ vào 1 notebook duy nhất. 
BẮT BUỘC áp dụng cấu trúc 5-Phase Data Pipeline:

### Kiến trúc 5 Notebook chuyên biệt:
1. `notebooks/00_business_understanding.ipynb`: Tạo Data Dictionary, xác định mục tiêu kinh doanh, và đặt ra các giả thuyết cần kiểm định.
2. `notebooks/01_data_quality.ipynb`: Đọc raw data, xử lý lỗi dtypes, missing values. Cuối file xuất ra `data/processed/01_cleaned.csv`.
3. `notebooks/02_exploratory_data_analysis.ipynb`: Load data cleaned. Trực quan hóa. **BẮT BUỘC** lưu mọi đồ thị quan trọng bằng lệnh `save_fig(fig, 'ten_hinh.png')` vào thư mục `figures/`. 
   - **Framework Bắt Buộc cho EDA**: Phải chia thành 4 cấp độ phân tích:
     + **Descriptive (Mô tả):** Chuyện gì đang xảy ra? (Vd: Phân bố Churn rate).
     + **Diagnostic (Chẩn đoán):** Tại sao nó xảy ra? (Vd: Phân tích các yếu tố lõi ảnh hưởng tới Churn).
     + **Predictive (Dự đoán - Tiền đề):** Yếu tố nào tiềm năng nhất để đưa vào mô hình dự đoán? (Vd: Feature importance sơ bộ dựa trên tương quan).
     + **Prescriptive (Đề xuất hành động):** Từ insight đó, doanh nghiệp cần làm gì ngay lập tức? (So-What).
4. `notebooks/03_feature_engineering.ipynb`: Load data cleaned. Tạo feature mới (CLV, Risk Level, Count...), xử lý phân phối (Log Transform, Binning), và kiểm tra tương quan đa cộng tuyến. Cuối file xuất ra `data/processed/02_engineered.csv`.
5. `notebooks/04_modeling.ipynb`: Load data engineered. Xây dựng ML Pipeline (Train/Test Split, Scaler, Model). Cuối file xuất mô hình `.pkl` vào `outputs/model/` (vd: `rf_model.pkl`).

### Quy tắc Sinh Code (Gen Code) cho Notebook:
- Khi Agent tự động tạo file `.ipynb` (thông qua Python script sinh JSON hoặc tạo trực tiếp), **BẮT BUỘC phải tạo ra các cell Markdown đan xen với các cell Code**.
- **Cell Markdown:** Luôn có giải thích ngữ cảnh kinh doanh (Insight & "So what") hoặc hướng dẫn các bước. Không bao giờ viết notebook mà chỉ có code.
- **TOC:** Notebook phải luôn bắt đầu bằng một cell Markdown liệt kê Table of Contents.

### Tích hợp Streamlit & Report:
- **Streamlit Demo:** File `app/streamlit_app.py` CHỈ load file `.pkl` từ `outputs/model/` để chạy predict. Không code lại quá trình train trong app.
- **Business Report:** File Markdown/PDF trong `report/` CHỈ nhúng các hình ảnh `.png` từ thư mục `figures/`. Tránh copy lại code vẽ hình.

---

## 10. Senior Data Science Mindset (Tư duy Cấp cao)

Để đạt điểm tuyệt đối trong mắt Giám khảo cấp Quản lý (Manager/Director), Agent phải luôn tự động áp dụng các tiêu chuẩn sau mà không cần User phải nhắc:

1. **Data Dictionary:** Luôn có bảng Từ điển Dữ liệu (Markdown) ngay đầu file `01_data_quality.ipynb` trước khi code.
2. **Executive KPIs:** Tại `02_exploratory_data_analysis.ipynb`, ngay sau khi load data, phải hiển thị một dãy `kpi_cards` (ví dụ: Tổng Doanh thu, Doanh thu tổn thất) để Giám đốc nắm tình hình.
3. **Statistical Validation (Kiểm định thống kê):** Trong phần Diagnostic EDA, luôn chèn một bài test nhỏ (VD: Chi-Square Test cho biến phân loại) để chứng minh tính khoa học.
4. **Rule-based Customer Segmentation:** Ưu tiên phân khúc khách hàng bằng Luật kinh doanh (Rule-based: VD "High-Risk Newbie") ở `03_feature_engineering.ipynb` thay vì dùng thuật toán K-Means tốn thời gian.
5. **Feature Validation (Correlation Heatmap):** BẮT BUỘC đặt Ma trận tương quan ở CUỐI file `03_feature_engineering.ipynb` để chứng minh các biến mới tạo ra có sức mạnh dự đoán (Predictive power) tốt hơn biến thô.
6. **Pipeline vs get_dummies (TỐI KỴ):** KHÔNG BAO GIỜ dùng `pd.get_dummies()` trong lúc làm EDA/Feature Engineering. Bắt buộc dùng `OneHotEncoder` nhúng bên trong `ColumnTransformer` (Scikit-Learn Pipeline) ở `04_modeling.ipynb` để tránh Data Leakage và dễ dàng Deploy lên Web App.
7. **Xử lý Outlier:** Trong viễn thông (Telco), cước phí cao không phải là lỗi nhập liệu mà là khách VIP/High-Risk. Tuyệt đối không tự ý xóa (drop) các outlier này nếu nó mang ý nghĩa kinh doanh. Mọi hàm xử lý biến đổi toán học (Log transform, Binning) phải nằm ở file số 03.
