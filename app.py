# =========================================
# CUSTOMER ENGAGEMENT STREAMLIT DASHBOARD
# =========================================

# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Customer Engagement Analytics",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

def load_data():

    return pd.read_csv("European_Bank.csv")

df = load_data()

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load("model.pkl")

# =========================================
# SIDEBAR NAVIGATION
# =========================================

st.sidebar.markdown("""
# 🏦 Smart Navigation
""")

page = st.sidebar.radio(
    "Go To",
    [
        "Home",
        "Engagement Analytics",
        "Product Utilization",
        "High-Value Disengaged Customers",
        "Retention Strength",
        "Churn Prediction"
    ]
)

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.image(
    "bank_ai_dashboard.png",
    use_container_width=True
)
st.sidebar.markdown("""
## 🎯 Customer Filters
""")

# Active Member Filter
active_filter = st.sidebar.selectbox(
    "Active Member",
    ["All", "Active", "Inactive"]
)

# Product Count Slider
product_filter = st.sidebar.slider(
    "Number of Products",
    1,
    4,
    (1,4)
)

# Balance Threshold
balance_threshold = st.sidebar.slider(
    "Minimum Balance",
    0,
    250000,
    0
)

# Salary Threshold
salary_threshold = st.sidebar.slider(
    "Minimum Salary",
    0,
    250000,
    0
)

# =========================================
# APPLY FILTERS
# =========================================

filtered_df = df.copy()

# Active Filter
if active_filter == "Active":

    filtered_df = filtered_df[
        filtered_df['IsActiveMember'] == 1
    ]

elif active_filter == "Inactive":

    filtered_df = filtered_df[
        filtered_df['IsActiveMember'] == 0
    ]

# Product Filter
filtered_df = filtered_df[
    (filtered_df['NumOfProducts'] >= product_filter[0]) &
    (filtered_df['NumOfProducts'] <= product_filter[1])
]

# Balance Filter
filtered_df = filtered_df[
    filtered_df['Balance'] >= balance_threshold
]

# Salary Filter
filtered_df = filtered_df[
    filtered_df['EstimatedSalary'] >= salary_threshold
]

st.sidebar.markdown("---")

st.sidebar.markdown("## Selected Filters")

st.sidebar.write(f"Active Status: {active_filter}")
st.sidebar.write(f"Products: {product_filter}")
st.sidebar.write(f"Min Balance: {balance_threshold}")
st.sidebar.write(f"Min Salary: {salary_threshold}")

# =========================================
# HOME PAGE
# =========================================

if page == "Home":

    st.image(
        "bank_ai_dashboard.png",
        use_container_width=True
    )

    st.markdown("""
    <h1 style='color:#1F4E79;'>
    Customer Engagement and Product Utilization Analytics
    </h1>
    """, unsafe_allow_html=True)

    st.info(
        "AI-powered analytics helping banks identify churn risks and improve customer engagement."
    )

    st.markdown("## KPI")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Customers",
            len(filtered_df)
        )

    with col2:

        churn_rate = filtered_df['Exited'].mean() * 100

        st.metric(
            "Churn Rate",
            f"{round(churn_rate,2)}%"
        )

    with col3:

        active_rate = filtered_df['IsActiveMember'].mean() * 100

        st.metric(
            "Active Customers",
            f"{round(active_rate,2)}%"
        )

    with col4:

        avg_products = filtered_df['NumOfProducts'].mean()

        st.metric(
            "Avg Products",
            round(avg_products,2)
        )

    st.markdown("---")

    st.subheader("Customer Segment Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        inactive_customers = len(
            filtered_df[
                filtered_df['IsActiveMember'] == 0
            ]
        )

        st.info(
            f"Inactive Customers: {inactive_customers}"
        )

    with col2:

        high_balance = len(
            filtered_df[
                filtered_df['Balance'] > 100000
            ]
        )

        st.warning(
            f"High Balance Customers: {high_balance}"
        )

    with col3:

        churn_customers = len(
            filtered_df[
                filtered_df['Exited'] == 1
            ]
        )

        st.error(
            f"Churned Customers: {churn_customers}"
        )

    st.markdown("---")

    st.caption(
        "Developed for Customer Engagement and Product Utilization Analytics"
    )
  
  
# =========================================
# ENGAGEMENT ANALYTICS
# =========================================

elif page == "Engagement Analytics":

    st.header("📊 Engagement vs Churn Overview")

    # KPIs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Active Customers",
            (
                filtered_df['IsActiveMember'] == 1
            ).sum()
        )

    with col2:
        st.metric(
            "Inactive Customers",
            (
                filtered_df['IsActiveMember'] == 0
            ).sum()
        )

    with col3:
        inactive_churn = filtered_df[
            (filtered_df['IsActiveMember'] == 0) &
            (filtered_df['Exited'] == 1)
        ]

        st.metric(
            "Inactive Churned Customers",
            len(inactive_churn)
        )

    st.markdown("---")

    st.subheader("Filtered Customers")

    st.dataframe(

        filtered_df[
            [
                'CustomerId',
                'CreditScore',
                'Balance',
                'NumOfProducts',
                'IsActiveMember',
                'Exited'
            ]
        ]

    )
# =========================================
# PRODUCT UTILIZATION
# =========================================
elif page == "Product Utilization":

    st.header("📦 Product Utilization Impact")

    product_customers = filtered_df[
        filtered_df['NumOfProducts'] >= 3
    ]

    st.metric(
        "High Product Customers",
        len(product_customers)
    )

    st.markdown("---")

    st.dataframe(

        product_customers[
            [
                'CustomerId',
                'NumOfProducts',
                'Balance',
                'EstimatedSalary',
                'Exited'
            ]
        ]

    )
# =========================================
# HIGH VALUE CUSTOMERS
# =========================================

elif page == "High-Value Disengaged Customers":

    st.header(
        "💰 High-Value Disengaged Customer Detector"
    )

    # Better filtering logic
    high_value = filtered_df[
        (filtered_df['Balance'] >= 50000) &
        (filtered_df['IsActiveMember'] == 0)
    ]

    # KPI
    st.metric(
        "Detected Customers",
        len(high_value)
    )

    st.markdown("---")

    # If no customers found
    if len(high_value) == 0:

        st.warning(
            "No high-value disengaged customers found for selected filters."
        )

    else:

        st.success(
            "Customers identified for retention targeting."
        )

        st.dataframe(

            high_value[
                [
                    'CustomerId',
                    'CreditScore',
                    'Balance',
                    'EstimatedSalary',
                    'NumOfProducts',
                    'Exited'
                ]
            ]

        )
# =========================================
# RETENTION STRATEGY PANEL
# =========================================

elif page == "Retention Strength":

    st.header("🛡️ Retention Strategy Recommendations")

    # =========================================
    # RETENTION SCORE
    # =========================================

    filtered_df['RetentionScore'] = (
        filtered_df['IsActiveMember'] * 40
        + filtered_df['NumOfProducts'] * 20
        + (filtered_df['Balance'] > 100000) * 20
        + filtered_df['HasCrCard'] * 20
    )

    # =========================================
    # RETENTION LEVEL
    # =========================================

    filtered_df['RetentionLevel'] = np.where(
        filtered_df['RetentionScore'] >= 70,
        "Strong Retention",
        "Weak Retention"
    )

    # =========================================
    # RETENTION STRATEGY FUNCTION
    # =========================================

    def retention_strategy(row):

        # High-value inactive customers
        if (
            row['Balance'] > 100000
            and row['IsActiveMember'] == 0
        ):

            return "Priority Relationship Manager Outreach"

        # Single-product customers
        elif row['NumOfProducts'] == 1:

            return "Cross-Selling & Product Bundle Offers"

        # Inactive customers
        elif row['IsActiveMember'] == 0:

            return "Customer Engagement Reactivation"

        # Older customers
        elif row['Age'] >= 45:

            return "Loyalty Benefits & Personalized Support"

        # High churn-risk customers
        elif row['Exited'] == 1:

            return "Immediate Retention Campaign"

        # Default strategy
        else:

            return "Standard Customer Retention Program"

    # =========================================
    # APPLY STRATEGY
    # =========================================

    filtered_df['RetentionStrategy'] = filtered_df.apply(
        retention_strategy,
        axis=1
    )

    # =========================================
    # KPIs
    # =========================================

    col1, col2, col3 = st.columns(3)

    with col1:

        strong_retention = len(
            filtered_df[
                filtered_df['RetentionLevel'] == "Strong Retention"
            ]
        )

        st.success(
            f"Strong Retention Customers: {strong_retention}"
        )

    with col2:

        weak_retention = len(
            filtered_df[
                filtered_df['RetentionLevel'] == "Weak Retention"
            ]
        )

        st.warning(
            f"Weak Retention Customers: {weak_retention}"
        )

    with col3:

        high_risk = len(
            filtered_df[
                filtered_df['Exited'] == 1
            ]
        )

        st.error(
            f"High Churn Risk Customers: {high_risk}"
        )

    st.markdown("---")

    # =========================================
    # RETENTION TABLE
    # =========================================

    st.subheader("📋 Customer Retention Recommendations")

    st.dataframe(

        filtered_df[
            [
                'CustomerId',
                'Balance',
                'EstimatedSalary',
                'NumOfProducts',
                'RetentionScore',
                'RetentionLevel',
                'RetentionStrategy'
            ]
        ]

    )

# =========================================
# CHURN PREDICTION
# =========================================


elif page == "Churn Prediction":

    st.header("🤖 Customer Churn Prediction")

    # Inputs
    credit_score = st.number_input(
        "Credit Score",
        300,
        900,
        650
    )

    age = st.number_input(
        "Age",
        18,
        100,
        35
    )

    tenure = st.number_input(
        "Tenure",
        0,
        10,
        5
    )

    balance = st.number_input(
        "Balance",
        0.0,
        250000.0,
        50000.0
    )

    products = st.number_input(
        "Number of Products",
        1,
        4,
        2
    )

    active_member = st.selectbox(
        "Active Member",
        [0,1]
    )

    salary = st.number_input(
        "Estimated Salary",
        0.0,
        250000.0,
        70000.0
    )

    geography = st.selectbox(
        "Geography",
        ["France", "Germany", "Spain"]
    )

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    # Prediction
    if st.button("Predict Churn"):

        # Feature Engineering
        ProductCategory_Num = (
            1 if products > 1 else 0
        )

        CreditTier2_Num = (
            1 if credit_score >= 650 else 0
        )

        AgeGroup2_Num = (
            1 if age >= 45 else 0
        )

        SalaryGroup_Num = (
            1 if salary >= 100000 else 0
        )

        ProductDepth_Num = (
            1 if products >= 3 else 0
        )

        Geography_Germany = (
            1 if geography == "Germany" else 0
        )

        Geography_Spain = (
            1 if geography == "Spain" else 0
        )

        Gender_Male = (
            1 if gender == "Male" else 0
        )

        # Final Input
        input_data = np.array([[

            credit_score,
            age,
            tenure,
            balance,
            products,
            1,
            active_member,
            salary,
            ProductCategory_Num,
            CreditTier2_Num,
            AgeGroup2_Num,
            SalaryGroup_Num,
            ProductDepth_Num,
            Geography_Germany,
            Geography_Spain,
            Gender_Male

        ]])

        # Prediction Probability
        probability = (
            model.predict_proba(input_data)[0][1]
        )

        # Threshold Decision
        if probability >= 0.4:

            st.error(
                f"⚠️ High Churn Risk: {probability:.2%}"
            )

        else:

            st.success(
                f"✅ Low Churn Risk: {probability:.2%}"
            )