import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Flipkart Logistics Admin Panel", layout="wide")

# ---------------- LOGIN SYSTEM ----------------
def login():
    st.title("🔐 Flipkart Logistics Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
        else:
            st.error("Invalid Credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- MAIN DASHBOARD ----------------
st.title("🚚 Flipkart Logistics Analytics Dashboard")

menu = st.sidebar.selectbox(
    "Select Module",
    ["Orders", "Routes", "Warehouses", "Delivery Agents", "Shipment Tracking"]
)

# ---------------- ORDERS ----------------
if menu == "Orders":
    df = pd.read_csv("Flipkart_Orders - Sheet1.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("%","").str.replace("(","").str.replace(")","")

    st.subheader("📦 Orders Overview")

    col1, col2 = st.columns(2)
    col1.metric("Total Orders", len(df))

    delayed = df[df["Delivery_Status"] == "Delayed"]
    col2.metric("Delayed Orders", len(delayed))

    st.dataframe(df)

# ---------------- ROUTES ----------------
elif menu == "Routes":
    df = pd.read_csv("Flipkart_Routes - Sheet1.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("%","").str.replace("(","").str.replace(")","")

    st.subheader("🛣 Route Performance")

    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df["Route_ID"], df["Traffic_Delay"])
    ax.set_title("Traffic Delay per Route")
    st.pyplot(fig)

# ---------------- WAREHOUSES ----------------
elif menu == "Warehouses":
    df = pd.read_csv("Flipkart_Warehouses - Sheet1.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("%","").str.replace("(","").str.replace(")","")

    st.subheader("🏭 Warehouse Performance")

    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df["Warehouse_Name"], df["Avg_Processing_Time"])
    ax.set_title("Avg Processing Time")
    st.pyplot(fig)

# ---------------- DELIVERY AGENTS ----------------
elif menu == "Delivery Agents":
    df = pd.read_csv("Flipkart_DeliveryAgents - Sheet1.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("%","").str.replace("(","").str.replace(")","")

    st.subheader("🚴 Delivery Agent Performance")

    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.bar(df["Agent_Name"], df["Delivery_Efficiency"])
    ax.set_title("Agent Efficiency %")
    st.pyplot(fig)

# ---------------- SHIPMENT TRACKING ----------------
elif menu == "Shipment Tracking":
    df = pd.read_csv("Flipkart_ShipmentTracking - Sheet1.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("%","").str.replace("(","").str.replace(")","")

    st.subheader("📍 Shipment Tracking")

    st.dataframe(df)

st.sidebar.markdown("---")

st.sidebar.success("Admin Panel - Logistics Analytics")


