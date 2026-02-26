import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Flipkart Logistics Enterprise Dashboard", layout="wide")

# ---------------- USER DATABASE ----------------
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "viewer": {"password": "viewer123", "role": "Viewer"}
}

# ---------------- LOGIN FUNCTION ----------------
def login():
    st.markdown("<h1 style='text-align:center;color:#2874F0;'>🚚 Flipkart Logistics Portal</h1>", unsafe_allow_html=True)
    st.markdown("### 🔐 Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
        else:
            st.error("Invalid username or password")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.success(f"👤 {st.session_state.username} ({st.session_state.role})")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.clear()
    st.rerun()

menu = st.sidebar.selectbox(
    "📊 Select Module",
    ["Executive Summary", "Orders", "Routes", "Warehouses", "Delivery Agents", "Shipment Tracking"]
)

# ---------------- LOAD FUNCTION ----------------
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

# ================= EXECUTIVE SUMMARY =================
if menu == "Executive Summary":
    st.title("📈 Executive Overview")

    orders = load_data("Flipkart_Orders - Sheet1.csv")
    routes = load_data("Flipkart_Routes - Sheet1.csv")
    warehouses = load_data("Flipkart_Warehouses - Sheet1.csv")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Orders", len(orders))
    col2.metric("Total Routes", len(routes))
    col3.metric("Total Warehouses", len(warehouses))

    st.info("💡 This executive dashboard provides real-time monitoring of logistics operations across the enterprise.")

# ================= ORDERS =================
elif menu == "Orders":
    df = load_data("Flipkart_Orders - Sheet1.csv")

    st.title("📦 Orders Analytics")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", len(df))

    if "Delivery_Status" in df.columns:
        delayed = df[df["Delivery_Status"] == "Delayed"]
        col2.metric("Delayed Orders", len(delayed))

    if "Order_Value" in df.columns:
        col3.metric("Total Revenue", int(df["Order_Value"].sum()))

    if "Delivery_Status" in df.columns:
        fig = px.pie(df, names="Delivery_Status", hole=0.4,
                     title="Order Status Distribution")
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.role == "Admin":
        st.dataframe(df, use_container_width=True)

# ================= ROUTES =================
elif menu == "Routes":
    df = load_data("Flipkart_Routes - Sheet1.csv")

    st.title("🛣 Route Performance")

    if "Traffic_Delay_Min" in df.columns:
        fig = px.bar(df, x="Route_ID", y="Traffic_Delay_Min",
                     color="Traffic_Delay_Min",
                     color_continuous_scale="Blues",
                     title="Traffic Delay by Route")
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.role == "Admin":
        st.dataframe(df, use_container_width=True)

# ================= WAREHOUSES =================
elif menu == "Warehouses":
    df = load_data("Flipkart_Warehouses - Sheet1.csv")

    st.title("🏭 Warehouse Efficiency")

    if "Average_Processing_Time_Min" in df.columns:
        fig = px.bar(df, x="Warehouse_Name",
                     y="Average_Processing_Time_Min",
                     color="Average_Processing_Time_Min",
                     color_continuous_scale="Oranges",
                     title="Processing Time by Warehouse")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.role == "Admin":
        st.dataframe(df, use_container_width=True)

# ================= DELIVERY AGENTS =================
elif menu == "Delivery Agents":
    df = load_data("Flipkart_DeliveryAgents - Sheet1.csv")

    st.title("🚴 Agent Performance")

    if "On_Time_Delivery_Percentage" in df.columns:
        fig = px.bar(df, x="Agent_Name",
                     y="On_Time_Delivery_Percentage",
                     color="On_Time_Delivery_Percentage",
                     color_continuous_scale="Greens",
                     title="On-Time Delivery %")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.role == "Admin":
        st.dataframe(df, use_container_width=True)

# ================= SHIPMENT TRACKING =================
elif menu == "Shipment Tracking":
    df = load_data("Flipkart_ShipmentTracking - Sheet1.csv")

    st.title("📍 Shipment Monitoring")

    col1, col2 = st.columns(2)

    col1.metric("Total Shipments", len(df))

    if "Delivery_Speed" in df.columns:
        col2.metric("Avg Speed", round(df["Delivery_Speed"].mean(), 2))

    if "Delay_Reason" in df.columns:
        fig = px.bar(df["Delay_Reason"].value_counts().reset_index(),
                     x="index", y="Delay_Reason",
                     title="Delay Reasons",
                     color="Delay_Reason",
                     color_continuous_scale="Reds")
        st.plotly_chart(fig, use_container_width=True)

    if st.session_state.role == "Admin":
        st.dataframe(df, use_container_width=True)
