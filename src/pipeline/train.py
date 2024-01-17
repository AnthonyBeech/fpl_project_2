import pandas as pd
import os
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import joblib  # Import joblib for saving the model

# Load the dataset
df = pd.read_csv("data/transformed/transformed.csv")
sampled_df = df.sample(frac=1, random_state=42)

# Split the data into training and testing sets
X = sampled_df.drop("8day_points", axis=1)
y = sampled_df["8day_points"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize RandomForestRegressor with predefined parameters
model = RandomForestRegressor(
    bootstrap=True,
    max_depth=10,
    min_samples_leaf=4,
    min_samples_split=10,
    n_estimators=200,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, "random_forest_regressor_model.pkl")

# Calculate and store feature importances
feature_importances = pd.DataFrame(
    model.feature_importances_,
    index=X_train.columns,
    columns=["importance"]
).sort_values("importance", ascending=False)

# Calculate R-squared values for train and test sets
r2_train = r2_score(y_train, model.predict(X_train))
r2_test = r2_score(y_test, model.predict(X_test))

# Prepare statistics to be saved
stats = {
    "feature_importances": feature_importances["importance"].to_dict(),
    "r2_train": r2_train,
    "r2_test": r2_test,
    "run_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Ensure the directory exists
plot_directory = "flask_main/flaskr/static"
os.makedirs(plot_directory, exist_ok=True)

# Save statistics as JSON
stats_filename = os.path.join(plot_directory, "model_statistics.json")
with open(stats_filename, 'w') as file:
    json.dump(stats, file, indent=4)

print(f"Statistics saved to {stats_filename}")

# Plotting Predictions vs True Values
plt.figure(figsize=(12, 6))
# Training Set Plot
y_train_pred = model.predict(X_train)
plt.subplot(1, 2, 1)
plt.scatter(y_train, y_train_pred, alpha=0.5)
plt.xlabel("True Values (Train)")
plt.ylabel("Predictions (Train)")
plt.title(f"Training Set: True vs Predicted Values\nR-squared = {r2_train:.2f}")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--", lw=4)

# Testing Set Plot
y_test_pred = model.predict(X_test)
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_test_pred, alpha=0.5)
plt.xlabel("True Values (Test)")
plt.ylabel("Predictions (Test)")
plt.title(f"Testing Set: True vs Predicted Values\nR-squared = {r2_test:.2f}")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--", lw=4)

plt.tight_layout()

# Save the figure to the specified directory
plot_filename = os.path.join(plot_directory, "model_performance_plots.png")
plt.savefig(plot_filename)

print(f"Plots saved to {plot_filename}")

# Optionally, show the plot as well
# plt.show()
