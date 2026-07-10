# BÁO CÁO TỔNG KẾT PHASE 0 & 1 (Business Understanding & Data Integration)

Tài liệu này tổng hợp các kết quả cốt lõi đã thực thi trong Notebook `00` và `01`, đồng thời cung cấp các "Talking Points" (Điểm nhấn thuyết trình) để bảo vệ giải pháp trước Giám khảo hoặc Ban lãnh đạo.

---

## 1. Những Gì Đã Đạt Được (Key Achievements)

### Phase 0: Business Understanding (`00_business_understanding.ipynb`)
- Khảo sát cấu trúc (Data Profiling) toàn diện 6 file Excel gốc (CRM, Sales, Production, Materials, Quality, HRM).
- Phát hiện các rủi ro Null tiềm ẩn và đề xuất Giả định (Assumptions Log) chặt chẽ.
- Chuyển hóa yêu cầu kinh doanh thành **4 Câu hỏi Liên miền (Cross-Domain KPIs)** định lượng được.
- Chốt chiến lược **MVP (Minimum Viable Product)**: Tập trung vào 3 phân hệ lõi (Sales, Production, Materials) để đảm bảo tiến độ hoàn thành Dashboard trong 2 giờ thi.

### Phase 1: Data Integration & Quality (`01_eda_quality.ipynb`)
- Thiết kế **Data Quality Framework** chuẩn mực: Bọc các bước kiểm tra Missing, Duplicates, PK/FK, Business Rules vào các hàm Python (Functions) dễ dàng tái sử dụng và kiểm toán.
- Khám phá tính năng tự động nhận diện `datetime` cực mạnh của `pd.read_excel`.
- Thay vì dùng `pd.merge` mù quáng gây lỗi nhân bản (Cartesian explosion), dự án đã áp dụng kiến trúc **Data Marts**:
  - Xuất thành công `datamart_sales.csv`: Gom nhóm chính xác Doanh thu từ `OrderLines` và ngày hoàn thành từ `ProductionOrders` để tính cờ `Is_Delayed` (Giải quyết Q1).
  - Xuất thành công `datamart_inventory.csv`: Tính toán cờ rủi ro `Stockout_Risk` dựa trên Tồn kho và Reorder Point (Giải quyết Q2).

---

## 2. Cẩm Nang Giải Thích Hiệu Quả (Talking Points & Defense Strategy)

*Dưới đây là 3 câu hỏi hóc búa nhất mà người chấm thi thường hỏi, và cách bạn trả lời để thể hiện tư duy của một Senior Data Analyst:*

### 🎯 Điểm nhấn 1: Chiến lược "Chia để trị" (Data Marts vs Flat Table)
**Giám khảo hỏi:** *"Tại sao em không dùng một lệnh `pd.merge` để gộp cả 6 bảng lại thành 1 cái Flat Table duy nhất cho dễ vẽ biểu đồ?"*
**Bạn trả lời:** 
> "Dữ liệu ERP có tính chất quan hệ nhiều-nhiều (Ví dụ 1 Đơn hàng có nhiều Dòng sản phẩm, 1 Sản phẩm lại cần nhiều Vật tư trong BOM). Nếu gộp tất cả thành 1 bảng duy nhất, dữ liệu như Doanh thu (Revenue) hay Số lượng (Quantity) sẽ bị **nhân bản (Duplicated)** lên n lần. Thay vào đó, em dùng kiến trúc Data Marts: Tổng hợp (Aggregate) từng luồng dữ liệu trước, xuất ra các file CSV nhỏ (`datamart_sales.csv`, `datamart_inventory.csv`) rồi mới đưa vào Dashboard. Điều này đảm bảo tính vẹn toàn dữ liệu (Granularity)."

### 🎯 Điểm nhấn 2: Xử lý Null bằng Business Logic
**Giám khảo hỏi:** *"Anh thấy bảng ProductionOrders có rất nhiều Null ở SalesOrderID và ActualEndDate. Xử lý Missing Values là bước cơ bản, sao em không dùng `.dropna()` để xóa hoặc `.fillna()` điền trung bình vào?"*
**Bạn trả lời:** 
> "Dữ liệu Null ở đây không phải là lỗi hệ thống (System Error) mà là **Nghiệp vụ (Business Logic)**. 
> - `SalesOrderID` bị Null là do đó là lệnh Sản xuất lưu kho (Make-to-stock), không gắn với đơn hàng nào. Em đã chủ động tách chúng ra khỏi luồng Join với bảng Sales.
> - `ActualEndDate` bị Null nghĩa là lệnh sản xuất chưa hoàn thành. Nếu xóa đi, ta sẽ mất cái nhìn về năng lực xưởng. Em đã kết hợp cột Null này với `RequiredDate` để đẻ ra cờ Cảnh báo Trễ hẹn (`Is_Delayed`). Em tin rằng Data Analyst giỏi là người biết dùng Null để ra Insight."

### 🎯 Điểm nhấn 3: Chiến lược MVP (Tối ưu thời gian)
**Giám khảo hỏi:** *"Đề bài cung cấp cả dữ liệu Nhân sự (HR) và Chất lượng (Quality), sao em không phân tích luôn?"*
**Bạn trả lời:** 
> "Trong bối cảnh áp lực thời gian (Time-boxed 2 giờ), nếu ôm đồm cả 6 Domain, rủi ro lớn nhất là hệ thống bị đổ vỡ và không kịp lên Dashboard. Em áp dụng **nguyên tắc Pareto (80/20)**: Nỗi đau lớn nhất của Ban điều hành lúc này là Trễ đơn hàng (Q1) và Đứt gãy vật tư (Q2). Do đó em tạo ra một sản phẩm MVP xử lý triệt để 2 vấn đề này trước. Kiến trúc Data Marts của em có khả năng mở rộng (Scalable), nếu có thêm thời gian, em chỉ cần viết thêm 1 file `datamart_quality.csv` và cắm (plug-in) vào Streamlit là xong."
