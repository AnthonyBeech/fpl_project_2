import pandas as pd
import joblib

# Load the trained RandomForestRegressor model
model_filename = "random_forest_regressor_model.pkl"
model = joblib.load(model_filename)

# Load new data
new_data = pd.read_csv("data/transformed/predict_data.csv")

# Extract player IDs
player_ids = new_data["player"]
new_data = new_data.drop("player", axis=1)

# Generate predictions using the model
predictions = model.predict(new_data)

# Load configuration and base URL
from src.utils import load_config
cfg = load_config()
base_url = cfg["base_url"]

# Retrieve player names
from src.components.request_utils import _get_global_data
from src.components.utils import _get_info_from_elements

player_names = []
json_data = _get_global_data(base_url)
for id in player_ids:
    for i, elem in  enumerate(json_data["elements"]):
        idj = elem["id"]
        
        if idj == id:
            name, _, _ = _get_info_from_elements(json_data, i)
            player_names.append(name.replace('.csv', ''))  # Removing '.csv' from names

# Create a DataFrame with player names and predicted points
predictions_df = pd.DataFrame({
    "id": player_ids,
    "name": player_names,
    "points": predictions
})

# Sort the DataFrame by points in descending order
predictions_df = predictions_df.sort_values(by="points", ascending=False)

# Save the DataFrame to a CSV file
predictions_df.to_csv("data/predicted/predict_data.csv", index=False)

print("Predictions saved and sorted in data/predicted/predict_data.csv")
