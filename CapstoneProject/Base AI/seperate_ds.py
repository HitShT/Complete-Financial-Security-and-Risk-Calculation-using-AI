import pandas as pd

df = pd.read_csv("Complete_AI_Prediction_DS.csv")

# total_amount_end // Done
# total_spent_job_loss
# health_insurance_amount

predicting_savings = {
    "salary":list(df["monthly_expense"]),
    "monthly_expense":list(df["monthly_expense"]),
    "dependents":list(df["dependents"]),
    "investment":list(df["investment"]),
    "year_start_investing":list(df["year_start_investing"]),
    "investment_amount_monthly":list(df["investment_amount_monthly"]),
    "investment_return":list(df["investment_return"]),
    "health_insurance":list(df["health_insurance"]),
    "health_insurance_amount":list(df["health_insurance_amount"]),
    "health_emergency":list(health["emergency"]),
    "health_emergency_amount":list(health["amount"]),
    "investment_stopped":list(df["investment_stopped"]),
    "investment_stopped_year":list(df["investment_stopped_year"]),
    "job_loss":list(df["job_loss"]),
    "months_out_job":list(df["months_out_job"]),
    "total_spent_job_loss":list(df["total_spent_job_loss"]),
    "total_returns_before_withdrawl":list(df["total_returns_before_withdrawl"]),
    "amount_taken":list(df["amount_taken"]),
    "remaining_investment_return":list(df["remaining_investment_return"]),
    "total_amount_end":list(df["total_amount_end"])
}
predicting_job_loss = {
    "salary":list(df["monthly_expense"]),
    "monthly_expense":list(df["monthly_expense"]),
    "dependents":list(df["dependents"]),
    "investment":list(df["investment"]),
    "year_start_investing":list(df["year_start_investing"]),
    "investment_amount_monthly":list(df["investment_amount_monthly"]),
    "investment_return":list(df["investment_return"]),
    "health_insurance":list(df["health_insurance"]),
    "health_insurance_amount":list(df["health_insurance_amount"]),
    "health_emergency":list(health["emergency"]),
    "health_emergency_amount":list(health["amount"]),
    "investment_stopped":list(df["investment_stopped"]),
    "investment_stopped_year":list(df["investment_stopped_year"]),
    "job_loss":list(df["job_loss"]),
    "months_out_job":list(df["months_out_job"]),
    "total_spent_job_loss":list(df["total_spent_job_loss"]),
    "total_returns_before_withdrawl":list(df["total_returns_before_withdrawl"]),
    "amount_taken":list(df["amount_taken"]),
    "remaining_investment_return":list(df["remaining_investment_return"]),
    "total_amount_end":list(df["total_amount_end"])
}
predicting_insurance = {
    "salary":list(df["monthly_expense"]),
    "monthly_expense":list(df["monthly_expense"]),
    "dependents":list(df["dependents"]),
    "investment":list(df["investment"]),
    "year_start_investing":list(df["year_start_investing"]),
    "investment_amount_monthly":list(df["investment_amount_monthly"]),
    "investment_return":list(df["investment_return"]),
    "health_insurance":list(df["health_insurance"]),
    "health_insurance_amount":list(df["health_insurance_amount"]),
    "health_emergency":list(health["emergency"]),
    "health_emergency_amount":list(health["amount"]),
    "investment_stopped":list(df["investment_stopped"]),
    "investment_stopped_year":list(df["investment_stopped_year"]),
    "job_loss":list(df["job_loss"]),
    "months_out_job":list(df["months_out_job"]),
    "total_spent_job_loss":list(df["total_spent_job_loss"]),
    "total_returns_before_withdrawl":list(df["total_returns_before_withdrawl"]),
    "amount_taken":list(df["amount_taken"]),
    "remaining_investment_return":list(df["remaining_investment_return"]),
    "total_amount_end":list(df["total_amount_end"])
}
