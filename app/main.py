from fastapi import FastAPI
from app.data_loader import load_bottle_data, load_user_bar
from app.recommender import create_user_profile, recommend

import logging


app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/recommend")
def get_recommendations(min_price: float = 0, max_price: float = 200):
    try:
        bottle_data = load_bottle_data()
        print("Loaded bottle data")

        user_data = load_user_bar()
        print("Loaded user data")

        profile = create_user_profile(user_data)
        print("Created user profile:", profile)

        filtered_data = bottle_data[
        (bottle_data["fair_price"] >= min_price) &
        (bottle_data["fair_price"] <= max_price)
    ]

        results = recommend(filtered_data, profile)
        return {"recommendations": results}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
