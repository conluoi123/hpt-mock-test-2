# PHASE.md — Kế hoạch triển khai 3 giờ (Modular Pipeline)

Tổng thời gian: **195 phút**.

---

## Phase 0: Business Understanding (00_business_understanding.ipynb) — 15 phút
- Khai báo Data Dictionary: Định nghĩa rõ các cột dữ liệu.
- Làm rõ Business Objective: Bài toán giải quyết vấn đề gì (vd: Churn, Cross-sell)?
- Xác định Output cuối cùng: Model, Dashboard, hay Report?
- Đặt ra các giả thuyết kinh doanh ban đầu để kiểm chứng ở bước EDA.

## Phase 1: Data Quality (01_data_quality.ipynb) — 15 phút
- Load raw data.
- Profile nhanh (`quick_profile`).
- Xử lý missing values, sửa data types (vd: TotalCharges).
- **Export:** `data/processed/01_cleaned.csv`.

## Phase 2: EDA (02_exploratory_data_analysis.ipynb) — 45 phút
- Phân tích sâu 3 góc độ: Hành vi khách hàng, Dịch vụ, Tài chính.
- Sử dụng `viz_utils.py` để biểu đồ đẹp và chuẩn HPT.
- 1 biểu đồ = 1 insight = 1 markdown giải thích.
- **Export:** `save_fig(fig, '...')` ra thư mục `figures/`.

## Phase 3: Feature Engineering (03_feature_engineering.ipynb) — 20 phút
- Tạo biến mới: Customer Lifetime Value (CLV), Số lượng dịch vụ (ServiceCount), Rủi ro hợp đồng.
- Kiểm tra tương quan.
- **Export:** `data/processed/02_engineered.csv`.

## Phase 4: Modeling (04_modeling.ipynb) — 30 phút
- Scale dữ liệu, Encode Categorical.
- Train Baseline (Logistic Regression) & Advanced Model (Random Forest).
- Tính Feature Importances và xuất biểu đồ ra `figures/`.
- **Export:** `outputs/model/rf_model.pkl`.

## Phase 5: Streamlit App (app/streamlit_app.py) — 25 phút
- Viết file giao diện web cho Customer Success Team.
- Load mô hình `.pkl`.
- Input thông tin → Tính điểm rủi ro rời mạng (Risk Score) → Gợi ý hành động.

## Phase 6: Report (report/TeleConnect_Churn_Report.md) — 35 phút
- Viết tóm tắt cho Ban lãnh đạo.
- Nhúng các file `.png` từ `figures/` vào Markdown.
- Ghi rõ khuyến nghị ngắn hạn & dài hạn.

## Phase 7: Kiểm tra & Đóng gói — 10 phút
- Chạy thử Streamlit.
- Đảm bảo Report render đúng ảnh.
- Nén file nộp bài.
