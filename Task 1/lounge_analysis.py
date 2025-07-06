import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load your dataset
df = pd.read_csv("flight_schedule.csv")  # Replace with your actual filename

# Lounge eligibility assumptions by TIME_OF_DAY
assumptions = {
    'Morning': {'Tier1': 0.02, 'Tier2': 0.05, 'Tier3': 0.20},
    'Mid-day': {'Tier1': 0.03, 'Tier2': 0.08, 'Tier3': 0.25},
    'Evening': {'Tier1': 0.05, 'Tier2': 0.10, 'Tier3': 0.30}
}

# Function to estimate lounge-eligible passengers
def estimate_lounge_eligibility(row):
    group = assumptions.get(row['TIME_OF_DAY'], {'Tier1': 0, 'Tier2': 0, 'Tier3': 0})
    tier1 = int(group['Tier1'] * row['FIRST_CLASS_SEATS'])
    tier2 = int(group['Tier2'] * row['BUSINESS_CLASS_SEATS'])
    tier3 = int(group['Tier3'] * row['ECONOMY_SEATS'])
    return pd.Series([tier1, tier2, tier3], index=['TIER1_ELIGIBLE_PAX', 'TIER2_ELIGIBLE_PAX', 'TIER3_ELIGIBLE_PAX'])

# Apply estimation function
df[['TIER1_ELIGIBLE_PAX', 'TIER2_ELIGIBLE_PAX', 'TIER3_ELIGIBLE_PAX']] = df.apply(estimate_lounge_eligibility, axis=1)

# Export updated CSV
df.to_csv("lounge_estimates_output.csv", index=False)

print("✅ Lounge estimates saved to 'lounge_estimates_output.csv'")
