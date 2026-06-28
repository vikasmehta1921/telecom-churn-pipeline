import pandas as pd
import numpy as np
import os

# ── Reproducible randomness ────────────────────────────────
np.random.seed(42)
N = 2_000_000 # 2 million customers

print(f"Generating {N:,} rows of synthetic telecom data...")

# ── Customer IDs ───────────────────────────────────────────
customer_ids = [f"CUST{str(i).zfill(7)}" for i in range(1, N + 1)]

# ── 1. customer_profile ────────────────────────────────────
print("Generating customer_profile...")

contract_types = np.random.choice(
    ["Month-to-month", "One year", "Two year"],
    size=N,
    p=[0.55, 0.25, 0.20]  # month-to-month most common (your observation)
)

tenure_months = np.where(
    contract_types == "Month-to-month",
    np.random.randint(1, 24, size=N),   # shorter tenure for m-t-m
    np.random.randint(6, 72, size=N)    # longer for annual contracts
)

genders = np.random.choice(["Male", "Female"], size=N)
senior = np.random.choice([0, 1], size=N, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], size=N)
dependents = np.random.choice(["Yes", "No"], size=N, p=[0.30, 0.70])

# Churn logic based on your observations
churn_prob = (
    (contract_types == "Month-to-month") * 0.35 +
    (tenure_months < 18) * 0.25 +
    senior * 0.10
)
churn_prob = np.clip(churn_prob, 0.05, 0.75)
churned = np.random.binomial(1, churn_prob)

customer_profile = pd.DataFrame({
    "customer_id"   : customer_ids,
    "gender"        : genders,
    "senior_citizen": senior,
    "partner"       : partner,
    "dependents"    : dependents,
    "tenure_months" : tenure_months,
    "contract_type" : contract_types,
    "churned"       : churned
})

out = "data/split_5m"
os.makedirs(out, exist_ok=True)

customer_profile.to_csv(f"{out}/customer_profile.csv", index=False)
print(f"customer_profile.csv done — {len(customer_profile):,} rows")

# ── 2. billing_data ────────────────────────────────────────
print("Generating billing_data...")

# Higher charges for fiber/premium customers
base_charge = np.random.normal(65, 30, size=N)
base_charge = np.clip(base_charge, 20, 120)

# Spike: some customers have unusually high bills
spike_flag = np.random.choice([0, 1], size=N, p=[0.92, 0.08])
monthly_charges = np.where(
    spike_flag == 1,
    base_charge * np.random.uniform(2.1, 3.0, size=N),
    base_charge
)
monthly_charges = np.round(np.clip(monthly_charges, 20, 200), 2)

total_charges = np.round(
    monthly_charges * tenure_months * np.random.uniform(0.85, 1.0, size=N), 2
)

payment_methods = np.random.choice(
    ["Electronic check", "Mailed check",
     "Bank transfer (automatic)", "Credit card (automatic)"],
    size=N,
    p=[0.34, 0.23, 0.22, 0.21]
)

paperless = np.random.choice(["Yes", "No"], size=N, p=[0.59, 0.41])

billing_data = pd.DataFrame({
    "customer_id"      : customer_ids,
    "monthly_charges"  : monthly_charges,
    "total_charges"    : total_charges,
    "payment_method"   : payment_methods,
    "paperless_billing": paperless,
    "billing_spike_flag": spike_flag
})

billing_data.to_csv(f"{out}/billing_data.csv", index=False)
print(f"billing_data.csv done — {len(billing_data):,} rows")

# ── 3. cdr_simulation ─────────────────────────────────────
print("Generating cdr_simulation...")

internet_service = np.random.choice(
    ["Fiber optic", "DSL", "No"],
    size=N,
    p=[0.44, 0.34, 0.22]
)

# Drop rate based on internet service (your observation)
drop_rate = np.where(
    internet_service == "Fiber optic",
    np.round(np.random.uniform(0.10, 0.30, size=N), 4),
    np.where(
        internet_service == "DSL",
        np.round(np.random.uniform(0.03, 0.12, size=N), 4),
        np.round(np.random.uniform(0.01, 0.05, size=N), 4)
    )
)

phone_service  = np.random.choice(["Yes", "No"], size=N, p=[0.90, 0.10])
multiple_lines = np.where(
    phone_service == "No", "No",
    np.random.choice(["Yes", "No"], size=N)
)
online_security = np.random.choice(["Yes", "No"], size=N, p=[0.29, 0.71])
tech_support    = np.random.choice(["Yes", "No"], size=N, p=[0.29, 0.71])
streaming_tv    = np.random.choice(["Yes", "No"], size=N, p=[0.38, 0.62])
streaming_movies= np.random.choice(["Yes", "No"], size=N, p=[0.39, 0.61])

cdr_simulation = pd.DataFrame({
    "customer_id"    : customer_ids,
    "phone_service"  : phone_service,
    "multiple_lines" : multiple_lines,
    "internet_service": internet_service,
    "online_security": online_security,
    "tech_support"   : tech_support,
    "streaming_tv"   : streaming_tv,
    "streaming_movies": streaming_movies,
    "drop_rate"      : drop_rate
})

cdr_simulation.to_csv(f"{out}/cdr_simulation.csv", index=False)
print(f"cdr_simulation.csv done — {len(cdr_simulation):,} rows")

# ── Summary ────────────────────────────────────────────────
print("\n✅ All 3 files generated in data/split_5m/")
print(f"Churn rate in dataset: {churned.mean()*100:.1f}%")
print(f"High monthly charges (>74): {(monthly_charges > 74).sum():,} customers")
print(f"Month-to-month contracts: {(contract_types == 'Month-to-month').sum():,} customers")
print(f"Short tenure (<18 months): {(tenure_months < 18).sum():,} customers")