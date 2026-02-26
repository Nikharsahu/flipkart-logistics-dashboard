import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Flipkart Logistics Analytics Dashboard", layout="wide")

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

# ---------------- FUNCTION TO LOAD CSV SAFELY ----------------
def load_data(file_name):
    df = pd.read_csv(file_name)
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace("%", "")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df

# ---------------- ORDERS ----------------
if menu == "Orders":
    df = load_data("Flipkart_Orders - Sheet1.csv")

    st.subheader("📦 Orders Overview")
    st.metric("Total Orders", len(df))

    if "Delivery_Status" in df.columns:
        delayed = df[df["Delivery_Status"] == "Delayed"]
        st.metric("Delayed Orders", len(delayed))

    st.dataframe(df)

# ---------------- ROUTES ----------------
elif menu == "Routes":
    df = load_data("Flipkart_Routes - Sheet1.csv")

    st.subheader("🛣 Route Performance")
    st.dataframe(df)

    if "Traffic_Delay_Min" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["Route_ID"], df["Traffic_Delay_Min"])
        ax.set_title("Traffic Delay per Route")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ---------------- WAREHOUSES ----------------
elif menu == "Warehouses":
    df = load_data("Flipkart_Warehouses - Sheet1.csv")

    st.subheader("🏭 Warehouse Performance")
    st.dataframe(df)

    if "Average_Processing_Time_Min" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["Warehouse_Name"], df["Average_Processing_Time_Min"])
        ax.set_title("Average Processing Time")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ---------------- DELIVERY AGENTS ----------------
elif menu == "Delivery Agents":
    df = load_data("Flipkart_DeliveryAgents - Sheet1.csv")

    st.subheader("🚴 Delivery Agent Performance")
    st.dataframe(df)

    if "On_Time_Delivery_Percentage" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["Agent_Name"], df["On_Time_Delivery_Percentage"])
        ax.set_title("On-Time Delivery %")
        plt.xticks(rotation=45)
        st.pyplot(fig)

# ---------------- SHIPMENT TRACKING ----------------
elif menu == "Shipment Tracking":
    df = load_data("Flipkart_ShipmentTracking - Sheet1.csv")

    st.subheader("📍 Shipment Tracking")
    st.dataframe(df)

st.sidebar.markdown("---")
st.sidebar.success("Admin Panel - Logistics Analytics")
