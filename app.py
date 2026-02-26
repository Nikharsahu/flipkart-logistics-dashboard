import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Flipkart Logistics Enterprise Dashboard", layout="wide")

# ---------------- THEME STYLING ----------------
st.markdown("""
    <style>
    .main-title {
        font-size:32px;
        font-weight:700;
        color:#2874F0;
    }
    .kpi-box {
        background-color:#1C1F26;
        padding:20px;
        border-radius:12px;
        text-align:center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD FUNCTION ----------------
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🚚 Flipkart Logistics Enterprise Dashboard</div>', unsafe_allow_html=True)
st.markdown("Advanced Logistics Performance Monitoring System")
st.markdown("---")

menu = st.sidebar.selectbox(
    "📊 Select Module",
    ["Orders", "Routes", "Warehouses", "Delivery Agents", "Shipment Tracking"]
)

# ================== ORDERS ==================
if menu == "Orders":
    df = load_data("Flipkart_Orders - Sheet1.csv")

    st.subheader("📦 Orders Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", len(df))

    if "Delivery_Status" in df.columns:
        delayed = df[df["Delivery_Status"] == "Delayed"]
        col2.metric("Delayed Orders", len(delayed))

    if "Order_Value" in df.columns:
        col3.metric("Total Revenue", int(df["Order_Value"].sum()))

    st.markdown("### 📊 Order Status Distribution")

    if "Delivery_Status" in df.columns:
        fig_status = px.pie(
            df,
            names="Delivery_Status",
            title="Order Status Breakdown",
            hole=0.4
        )
        st.plotly_chart(fig_status, use_container_width=True)

    # Revenue Trend (if date column exists)
    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(df["Order_Date"])
        revenue_trend = df.groupby("Order_Date")["Order_Value"].sum().reset_index()

        fig_trend = px.line(
            revenue_trend,
            x="Order_Date",
            y="Order_Value",
            title="Revenue Trend Over Time",
            markers=True
        )

        st.plotly_chart(fig_trend, use_container_width=True)

    st.dataframe(df, use_container_width=True)
# ================== ROUTES ==================
elif menu == "Routes":
    df = load_data("Flipkart_Routes - Sheet1.csv")

    st.subheader("🛣 Route Performance Analytics")

    if "Route_ID" in df.columns:
        route_filter = st.selectbox("Filter by Route", df["Route_ID"].unique())
        df_filtered = df[df["Route_ID"] == route_filter]
    else:
        df_filtered = df

    if "Traffic_Delay_Min" in df.columns:
        fig = px.bar(df, x="Route_ID", y="Traffic_Delay_Min",
                     title="Traffic Delay per Route",
                     color="Traffic_Delay_Min",
                     color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_filtered, use_container_width=True)

# ================== WAREHOUSES ==================
elif menu == "Warehouses":
    df = load_data("Flipkart_Warehouses - Sheet1.csv")

    st.subheader("🏭 Warehouse Efficiency")

    # Optional filter
    city_filter = st.multiselect(
        "Filter by City (Optional)",
        df["City"].unique()
    )

    if city_filter:
        df_filtered = df[df["City"].isin(city_filter)]
    else:
        df_filtered = df

    fig = px.bar(
        df_filtered,
        x="Warehouse_Name",
        y="Average_Processing_Time_Min",
        color="Average_Processing_Time_Min",
        color_continuous_scale="Oranges",
        title="Average Processing Time by Warehouse"
    )

    fig.update_layout(
        xaxis_title="Warehouse",
        yaxis_title="Processing Time (Minutes)",
        xaxis_tickangle=-45,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_filtered, use_container_width=True)
# ================== DELIVERY AGENTS ==================
elif menu == "Delivery Agents":
    df = load_data("Flipkart_DeliveryAgents - Sheet1.csv")

    st.subheader("🚴 Delivery Agent Performance")

    if "On_Time_Delivery_Percentage" in df.columns:
        fig = px.bar(df,
                     x="Agent_Name",
                     y="On_Time_Delivery_Percentage",
                     title="On-Time Delivery %",
                     color="On_Time_Delivery_Percentage",
                     color_continuous_scale="Greens")
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True)

# ================== SHIPMENT TRACKING ==================
elif menu == "Shipment Tracking":
    df = load_data("Flipkart_ShipmentTracking - Sheet1.csv")

    st.subheader("📍 Shipment Tracking Overview")

    st.dataframe(df, use_container_width=True)

# ---------------- INSIGHTS BOX ----------------
st.markdown("---")
st.info("💡 Insight: This dashboard enables real-time monitoring of logistics performance across orders, routes, warehouses, and agents.")

st.sidebar.success("Enterprise Logistics Admin Panel")


