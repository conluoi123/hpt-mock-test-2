# ARCHITECTURE.md — Cấu trúc dự án Modular Data Pipeline

> **Cấu trúc 4-Phase Pipeline** — Dùng cho mọi đề tài, giúp code gọn gàng, tách biệt Data/Model và dễ đưa lên Web.

## 1. Cấu trúc thư mục

```
project-root/
├── data/
│   ├── raw/                    # Dữ liệu gốc (CSV/Excel) — KHÔNG sửa trực tiếp
│   └── processed/              # Dữ liệu xuất ra từ pipeline (01_cleaned, 02_engineered)
│
├── notebooks/
│   ├── 00_business_understanding.ipynb # Giải thích business, từ điển dữ liệu
│   ├── 01_data_quality.ipynb           # Làm sạch dữ liệu, xuất 01_cleaned.csv
│   ├── 02_exploratory_data_analysis.ipynb # EDA, lưu hình vào figures/
│   ├── 03_feature_engineering.ipynb    # Tạo biến, xuất 02_engineered.csv
│   └── 04_modeling.ipynb               # Train Model, xuất rf_model.pkl
│
├── src/
│   ├── __init__.py
│   └── viz_utils.py            # ★ Module trực quan hóa (design system, chart helpers)
│
├── figures/                    # ★ Chart PNG export từ notebook (Dùng cho Report)
│
├── outputs/
│   └── model/                  # ★ Model artifacts (.pkl) (Dùng cho Streamlit)
│
├── app/                        
│   └── streamlit_app.py        # ★ Web dashboard đọc trực tiếp từ outputs/model/
│
├── report/
│   └── Report.md               # Báo cáo phân tích (PDF/HTML) nhúng ảnh từ figures/
│
├── docs/
│   ├── ARCHITECTURE.md         # (file này)
│   ├── PHASE.md                # Kế hoạch 3 giờ
│   └── SKILLS.md               # Checklist kỹ năng
│
└── README.md
```

## 2. Luồng dữ liệu (Data Pipeline)

```
[data/raw/dataset.csv]
          │
          ▼
 (00_business_understanding.ipynb)
          │
          ▼
 (01_data_quality.ipynb) ───▶ [data/processed/01_cleaned.csv]
          │
          ├──▶ (02_exploratory_data_analysis.ipynb) ───▶ [figures/*.png]
          │
          ▼
(03_feature_engineering.ipynb) ───▶ [data/processed/02_engineered.csv]
          │
          ▼
  (04_modeling.ipynb) ───▶ [outputs/model/rf_model.pkl]
```

## 3. Lợi ích của kiến trúc này
- **Tách biệt mối quan tâm (SoC):** Lỗi ở Model không làm hỏng Code EDA.
- **Tái sử dụng:** Report chỉ việc link tới `figures/`. Web App chỉ việc load `.pkl`.
- **Chuyên nghiệp:** Giống hệ thống MLOps thực tế.
