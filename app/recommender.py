from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def create_user_profile(user_data):
    user_products = [item["product"] for item in user_data if "product" in item and "spirit" in item["product"]]
    
    if not user_products:
        raise ValueError("No valid bottles with 'spirit' found in user data.")

    # Convert spirit → spirit_type
    for p in user_products:
        p["spirit_type"] = p["spirit"]

    user_df = pd.DataFrame(user_products)

    return {
        "avg_proof": user_df["proof"].mean(),
        "top_spirit": user_df["spirit_type"].mode()[0],
        "avg_price": user_df["fair_price"].mean()
    }



def recommend(df, user_profile, top_n=5):
    df = df[df["spirit_type"] == user_profile["top_spirit"]].copy()
    df["score"] = (
        (df["proof"] - user_profile["avg_proof"]).abs() +
        (df["fair_price"] - user_profile["avg_price"]).abs()
    )

    top_picks = df.sort_values("score").head(top_n)
    results = []

    for _, row in top_picks.iterrows():
        reason = f"Similar spirit type ({row['spirit_type']}), close in proof and price."
        results.append({
            "name": row["name"],
            "proof": row["proof"],
            "spirit_type": row["spirit_type"],
            "fair_price": round(row["fair_price"], 2),
            "reason": reason,
            "image_url": row.get("image_url", "")
        })

    return results
