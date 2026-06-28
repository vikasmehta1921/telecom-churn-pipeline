import pandas as pd
import os

# ── Load raw file ──────────────────────────────────────────
raw_path = os.path.join("data", "raw", "Telco-Customer-Churn.csv")
df = pd.read_csv(raw_path)

# ── Clean TotalCharges (blank strings → 0) ─────────────────
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

# ── Standardise "No internet service" → "No" ──────────────
internet_cols = [
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies"
]
for col in internet_cols:
    df[col] = df[col].replace("No internet service", "No")

# ── Standardise "No phone service" → "No" ─────────────────
df["MultipleLines"] = df["MultipleLines"].replace("No phone service", "No")

# ── Output folder ──────────────────────────────────────────
out = os.path.join("data", "split")
os.makedirs(out, exist_ok=True)

# ── 1. customer_profile.csv ────────────────────────────────
customer_profile = df[[
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "Contract",
    "Churn"
]].rename(columns={
    "customerID"   : "customer_id",
    "SeniorCitizen": "senior_citizen",
    "Partner"      : "partner",
    "Dependents"   : "dependents",
    "tenure"       : "tenure_months",
    "Contract"     : "contract_type",
    "Churn"        : "churned"
})

customer_profile["churned"] = customer_profile["churned"].map({"Yes": 1, "No": 0})
customer_profile.to_csv(os.path.join(out, "customer_profile.csv"), index=False)
print(f"customer_profile.csv  →  {len(customer_profile)} rows")

# ── 2. billing_data.csv ────────────────────────────────────
billing_data = df[[
    "customerID",
    "MonthlyCharges",
    "TotalCharges",
    "PaymentMethod",
    "PaperlessBilling"
]].rename(columns={
    "customerID"      : "customer_id",
    "MonthlyCharges"  : "monthly_charges",
    "TotalCharges"    : "total_charges",
    "PaymentMethod"   : "payment_method",
    "PaperlessBilling": "paperless_billing"
})

# Billing spike flag: monthly charge > 2x average
avg_charge = billing_data["monthly_charges"].mean()
billing_data["billing_spike_flag"] = (
    billing_data["monthly_charges"] > 2 * avg_charge
).astype(int)

billing_data.to_csv(os.path.join(out, "billing_data.csv"), index=False)
print(f"billing_data.csv      →  {len(billing_data)} rows")

# ── 3. cdr_simulation.csv ─────────────────────────────────
cdr_simulation = df[[
    "customerID",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies"
]].rename(columns={
    "customerID"     : "customer_id",
    "PhoneService"   : "phone_service",
    "MultipleLines"  : "multiple_lines",
    "InternetService": "internet_service",
    "OnlineSecurity" : "online_security",
    "TechSupport"    : "tech_support",
    "StreamingTV"    : "streaming_tv",
    "StreamingMovies": "streaming_movies"
})

# Simulate drop rate based on internet service type
# Fiber optic customers have higher simulated drop rate (real-world pattern)
cdr_simulation["drop_rate"] = cdr_simulation["internet_service"].map({
    "Fiber optic": 0.18,
    "DSL"        : 0.07,
    "No"         : 0.02
})

cdr_simulation.to_csv(os.path.join(out, "cdr_simulation.csv"), index=False)
print(f"cdr_simulation.csv    →  {len(cdr_simulation)} rows")

print("\nAll 3 files created successfully in data/split/")