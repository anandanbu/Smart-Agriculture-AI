def get_crop_recommendation(crop):
    crop_profit = {
        "rice": 20000,
        "wheat": 15000,
        "maize": 18000,
        "cotton": 25000,
        "sugarcane": 30000
    }

    profit = crop_profit.get(crop, 10000)

    return f"🌾 Recommended Crop: {crop} | 💰 Expected Profit: ₹{profit}"
