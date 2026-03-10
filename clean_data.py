import pandas as pd

file_name = "ebay_tech_deals.csv"

df = pd.read_csv(file_name, dtype=str)

df["price"] = df["price"].str.replace("US $", "", regex=False)
df["price"] = df["price"].str.replace(",", "", regex=False)
df["price"] = df["price"].str.strip()

df["original_price"] = df["original_price"].str.replace("US $", "", regex=False)
df["original_price"] = df["original_price"].str.replace(",", "", regex=False)
df["original_price"] = df["original_price"].str.strip()

df["original_price"] = df["original_price"].replace(["N/A", "", " "], pd.NA)
df["original_price"] = df["original_price"].fillna(df["price"])

df["shipping"] = df["shipping"].replace(["N/A", "", " "], "Shipping info unavailable")
df["shipping"] = df["shipping"].fillna("Shipping info unavailable")

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["original_price"] = pd.to_numeric(df["original_price"], errors="coerce")

df["discount_percentage"] = ((df["original_price"] - df["price"]) / df["original_price"]) * 100
df["discount_percentage"] = df["discount_percentage"].round(2)

df.to_csv("cleaned_ebay_deals.csv", index=False)

print("cleaned data saved to cleaned_ebay_deals.csv")