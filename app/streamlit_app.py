import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import os

# --- 1. PAGE CONFIGURATION & CSS ---
st.set_page_config(page_title="Manufacturing 360 Control Tower", page_icon="🏭", layout="wide")

st.markdown("""
<style>
    .kpi-card {
        background-color: #1E1E2E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        text-align: center;
        border-left: 5px solid #00E676;
    }
    .kpi-card-danger {
        border-left: 5px solid #FF3D00;
    }
    .kpi-title {
        color: #B0BEC5;
        font-size: 14px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-value {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: bold;
    }
    .analytics-text {
        background-color: #262730;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #457B9D;
        font-size: 14px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    sales_path = os.path.join(os.path.dirname(__file__), "../data/processed/datamart_sales.csv")
    inv_path = os.path.join(os.path.dirname(__file__), "../data/processed/datamart_inventory.csv")
    
    if not os.path.exists(sales_path) or not os.path.exists(inv_path):
        return None, None
        
    sales_df = pd.read_csv(sales_path)
    inv_df = pd.read_csv(inv_path)
    return sales_df, inv_df

sales_df, inv_df = load_data()

if sales_df is None:
    st.error("🚨 Không tìm thấy dữ liệu Data Marts. Vui lòng chạy file `01_eda_quality.ipynb` để xuất file CSV trước!")
    st.stop()

# --- 3. SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=100)
st.sidebar.title("⚙️ Điều khiển & Cấu hình")

api_key = st.sidebar.text_input("🔑 OpenRouter API Key", type="password", help="Nhập API Key do đề bài cấp để kích hoạt Trợ lý AI")

st.sidebar.markdown("### 🔍 Bộ lọc Dữ liệu")
priority_filter = st.sidebar.multiselect(
    "Mức độ ưu tiên đơn hàng (Priority)",
    options=sales_df['Priority'].dropna().unique(),
    default=sales_df['Priority'].dropna().unique()
)

filtered_sales = sales_df[sales_df['Priority'].isin(priority_filter)]

# --- 4. MAIN DASHBOARD ---
st.title("🏭 Manufacturing 360: Control Tower")
st.markdown("Giám sát Chuỗi cung ứng theo thời gian thực (Tích hợp Trợ lý AI)")

tab1, tab2, tab3 = st.tabs(["📊 Executive Summary", "📈 Analytics & 4-Tier Insights", "🤖 AI Root-Cause Analyst"])

# ================= TAB 1: EXECUTIVE (KPIs) =================
with tab1:
    st.markdown("### 🏆 Key Performance Indicators (KPIs)")
    
    total_revenue = filtered_sales['LineTotal_Calc'].sum()
    late_orders = filtered_sales['Is_Delayed'].sum()
    total_orders = len(filtered_sales)
    late_rate = (late_orders / total_orders) * 100 if total_orders > 0 else 0
    
    stockout_items = inv_df['Stockout_Risk'].sum()
    total_items = len(inv_df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Tổng Doanh Thu</div><div class="kpi-value">${total_revenue:,.0f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card kpi-card-danger"><div class="kpi-title">Đơn Hàng Trễ (Q1)</div><div class="kpi-value">{late_orders} ({late_rate:.1f}%)</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card kpi-card-danger"><div class="kpi-title">Vật Tư Cạn Kho (Q2)</div><div class="kpi-value">{stockout_items} / {total_items}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">Tổng Đơn Hàng</div><div class="kpi-value">{total_orders}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚠️ Danh sách Đơn hàng ưu tiên cao đang bị trễ hẹn")
    high_risk = filtered_sales[(filtered_sales['Is_Delayed'] == True) & (filtered_sales['Priority'].isin(['High', 'Critical']))]
    if not high_risk.empty:
        st.dataframe(high_risk[['OrderID', 'Priority', 'OrderDate', 'RequiredDate', 'ActualEndDate', 'LineTotal_Calc']], use_container_width=True)
    else:
        st.success("Tuyệt vời! Không có đơn hàng High/Critical nào bị trễ.")

# ================= TAB 2: CHARTS & 4-TIER ANALYTICS =================
with tab2:
    st.markdown("### Phân tích Chuyên sâu (4-Tier Analytics Framework)")
    
    # --- PHẦN 1: PHÂN PHỐI ---
    st.subheader("1. Khám phá Phân phối Dữ liệu (Distribution)")
    col_dist1, col_dist2 = st.columns(2)
    with col_dist1:
        fig_dist1 = px.histogram(filtered_sales, x='LineTotal_Calc', title='Phân phối Giá trị Đơn hàng', template="plotly_dark", color_discrete_sequence=['#2D6A4F'])
        st.plotly_chart(fig_dist1, use_container_width=True)
    with col_dist2:
        fig_dist2 = px.box(inv_df, y='CurrentStock', title='Phân bố Tồn kho (Outlier Detection)', template="plotly_dark", color_discrete_sequence=['#F4A261'])
        st.plotly_chart(fig_dist2, use_container_width=True)
        
    st.markdown("""
    <div class="analytics-text">
    <b>💡 Phân tích Đa chiều (4-Tier Analytics):</b><br>
    - 📊 <b>Descriptive:</b> Phân phối doanh thu lệch phải (Right-skewed) rõ rệt. Đa số đơn hàng lắt nhắt, doanh thu gánh bởi cá mập. Tồn kho phân tán rộng nhưng không có Outliers.<br>
    - 🔍 <b>Diagnostic:</b> Xưởng đang tốn quá nhiều nguồn lực điều phối (setup time) cho các đơn hàng nhỏ lẻ, làm giảm hiệu suất tổng thể.<br>
    - 🔮 <b>Predictive:</b> Nếu đưa biến `LineTotal_Calc` vào mô hình, các đơn hàng giá trị siêu nhỏ có thể là yếu tố dự báo mạnh cho việc bị trễ hẹn do bị bỏ bê.<br>
    - 🚀 <b>Prescriptive:</b> Cân nhắc áp dụng MOQ (Số lượng đặt hàng tối thiểu) hoặc gom các đơn nhỏ thành batch để sản xuất một lần.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- PHẦN 1.5: CƠ CẤU TRỄ HẸN (PIE & STACKED BAR) ---
    st.subheader("1.5. Cơ cấu Trễ hẹn (Delay Status Breakdown)")
    col_pie, col_stacked = st.columns(2)
    
    with col_pie:
        delay_counts = filtered_sales['Is_Delayed'].value_counts().reset_index()
        delay_counts.columns = ['Status', 'Count']
        delay_counts['Status'] = delay_counts['Status'].map({True: 'Trễ hẹn (Delayed)', False: 'Đúng hạn (On-time)'})
        
        # Donut Chart
        fig_pie = px.pie(
            delay_counts, 
            values='Count', 
            names='Status', 
            title='Tỷ lệ Trễ hẹn Tổng thể (Donut Chart)', 
            template="plotly_dark", 
            color='Status', 
            color_discrete_map={'Trễ hẹn (Delayed)': '#FF3D00', 'Đúng hạn (On-time)': '#52B788'},
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_stacked:
        stacked_data = filtered_sales.groupby(['Priority', 'Is_Delayed']).size().reset_index(name='Count')
        stacked_data['Is_Delayed'] = stacked_data['Is_Delayed'].map({True: 'Trễ hẹn', False: 'Đúng hạn'})
        
        # Stacked Bar Chart
        fig_stacked = px.bar(
            stacked_data, 
            x='Priority', 
            y='Count', 
            color='Is_Delayed', 
            title='Trạng thái Đơn hàng theo Độ ưu tiên (Stacked Chart)', 
            template="plotly_dark", 
            barmode='stack', 
            color_discrete_map={'Trễ hẹn': '#FF3D00', 'Đúng hạn': '#52B788'}
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
        
    st.markdown("---")
    
    # --- PHẦN 2: Q1 (TRỄ HẸN) ---
    st.subheader("2. Phân tích Trễ hẹn Đơn hàng (Sales vs Production)")
    priority_late = filtered_sales[filtered_sales['Is_Delayed'] == True].groupby('Priority').size().reset_index(name='Count')
    priority_late = priority_late.sort_values(by='Count', ascending=False)
    # Tô màu 2 cột cao nhất
    priority_late['Color'] = ['#FF3D00' if i < 2 else '#52B788' for i in range(len(priority_late))]
    
    fig_q1 = px.bar(priority_late, x='Priority', y='Count', title='Số lượng Đơn Trễ theo Mức độ Ưu tiên', template="plotly_dark")
    fig_q1.update_traces(marker_color=priority_late['Color'])
    st.plotly_chart(fig_q1, use_container_width=True)
    
    st.markdown("""
    <div class="analytics-text">
    <b>💡 Phân tích Đa chiều (4-Tier Analytics):</b><br>
    - 📊 <b>Descriptive (Mô tả):</b> Biểu đồ cho thấy nhóm đơn hàng <code>Medium</code> và <code>Critical</code> đang dẫn đầu về số lượng trễ hẹn. Nhóm <code>Critical</code> đáng lẽ phải ưu tiên nhất nhưng lại đứng Top 2 độ trễ.<br>
    - 🔍 <b>Diagnostic (Chẩn đoán):</b> Xưởng sản xuất đang điều độ lệnh theo cơ chế "Cào bằng" hoặc "Vào trước làm trước" (FIFO), ngắt kết nối hoàn toàn với mức độ ưu tiên từ phòng Sales.<br>
    - 🔮 <b>Predictive (Dự đoán):</b> Sự mâu thuẫn này biến biến <code>Priority</code> thành một Đặc trưng lõi (Core Feature) có sức mạnh dự báo cao khi đưa vào mô hình Machine Learning.<br>
    - 🚀 <b>Prescriptive (Hành động):</b> Cài đặt quy tắc "Luồng xanh" (Fast-track). Ép hệ thống ERP đẩy lệnh sản xuất Critical lên đầu hàng đợi máy móc.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # --- PHẦN 3: Q2 (TỒN KHO) ---
    st.subheader("3. Rủi ro Đứt gãy Vật tư (Materials vs Production)")
    inv_df['Shortage'] = inv_df['ReorderPoint'] - inv_df['CurrentStock']
    stockout_df = inv_df[inv_df['Stockout_Risk'] == True].sort_values('Shortage', ascending=False).head(10)
    # Tô màu Top 2
    stockout_df['Color'] = ['#FF3D00' if i < 2 else '#F4A261' for i in range(len(stockout_df))]
    
    fig_q2 = px.bar(stockout_df, x='MaterialName', y='Shortage', title='Top Vật tư Thiếu Hụt Nặng Nhất (Mức độ hụt so với Reorder Point)', template="plotly_dark")
    fig_q2.update_traces(marker_color=stockout_df['Color'])
    st.plotly_chart(fig_q2, use_container_width=True)
    
    st.markdown("""
    <div class="analytics-text">
    <b>💡 Phân tích Đa chiều (4-Tier Analytics):</b><br>
    - 📊 <b>Descriptive (Mô tả):</b> Thiếu hụt vật tư không dàn trải mà tập trung cực đoan vào 2 mã lõi: <code>Carbon Steel</code> và <code>Bearing Ball</code> (hụt ~300 units). Có sự sụt giảm (drop-off) rõ rệt từ vật tư thứ 3.<br>
    - 🔍 <b>Diagnostic (Chẩn đoán):</b> Việc cạn kiệt 2 vật tư nền tảng này chính là nút thắt cổ chai (Bottleneck) đứt gãy chuỗi cung ứng. Không có thép Carbon, không thể lắp ráp thành phẩm.<br>
    - 🔮 <b>Predictive (Dự đoán):</b> Tỷ lệ hụt (`ReorderPoint - CurrentStock`) của 2 vật tư này là chỉ báo dẫn dắt (Leading Indicator) cực tốt để Model dự đoán xác suất đình trệ xưởng trong tuần tới.<br>
    - 🚀 <b>Prescriptive (Hành động):</b> Mua hàng áp dụng quy tắc "Vital Few", dồn ngân sách tạo lệnh mua khẩn cấp (Expedited PO) cho 2 mã màu đỏ này.
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 3: AI ASSISTANT =================
with tab3:
    st.markdown("### 🤖 Trợ lý Phân tích AI (OpenRouter)")
    st.info("AI sẽ tự động đọc bảng dữ liệu Đơn hàng trễ và Tồn kho để đưa ra Insight (Hiện trạng), Root-Cause Analysis (Nguyên nhân) và Recommendation (Đề xuất hành động).")
    
    if st.button("🚀 Kích hoạt AI Phân tích Dữ liệu", type="primary"):
        if not api_key:
            st.error("Vui lòng nhập OpenRouter API Key ở thanh bên trái (Sidebar) trước khi phân tích!")
        else:
            with st.spinner("AI đang quét toàn bộ chuỗi cung ứng..."):
                sales_summary = high_risk[['OrderID', 'Priority', 'RequiredDate']].to_dict(orient='records')
                inv_summary = inv_df[inv_df['Stockout_Risk'] == True][['MaterialName', 'CurrentStock', 'ReorderPoint']].to_dict(orient='records')
                
                prompt = f"""
                Bạn là Giám đốc Vận hành (COO) của nhà máy. Dựa vào dữ liệu dưới đây, hãy viết một báo cáo ngắn gọn (tiếng Việt):
                1. Đơn hàng ưu tiên cao đang bị trễ: {sales_summary}
                2. Vật tư đang cạn kho (Dưới mức an toàn): {inv_summary}
                
                Yêu cầu báo cáo có cấu trúc rõ ràng:
                - 🛑 Hiện trạng (Insights)
                - 🔍 Phân tích nguyên nhân gốc rễ (Root-cause)
                - 💡 Hành động đề xuất khẩn cấp (Recommendation)
                """
                
                try:
                    headers = {
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": "qwen/qwen3.7-plus",
                        "messages": [{"role": "user", "content": prompt}],
                        "reasoning": {"enabled": True}  # Kích hoạt tính năng Reasoning của OpenRouter
                    }
                    
                    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                    
                    if res.status_code == 200:
                        result = res.json()
                        message = result['choices'][0]['message']
                        ai_content = message.get('content', '')
                        reasoning_text = message.get('reasoning', '')
                        
                        st.success("✅ Phân tích hoàn tất!")
                        
                        # Hiển thị quá trình tư duy nếu có
                        if reasoning_text:
                            with st.expander("🤔 Xem quá trình Tư duy của AI (Reasoning Chain)"):
                                st.markdown(f"*{reasoning_text}*")
                                
                        st.markdown(ai_content)
                    else:
                        st.error(f"Lỗi API: {res.status_code} - {res.text}")
                        
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi khi gọi API: {str(e)}")
