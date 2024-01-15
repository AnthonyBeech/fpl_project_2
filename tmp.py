import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt


df = pd.read_csv("data/transformed/transformed.csv")
sampled_df = df.sample(frac=0.001, random_state=42)

# 2. Split the data into training and testing sets
X = sampled_df.drop("8day_points", axis=1)
y = sampled_df["8day_points"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

param_grid = {
    "bootstrap": [True],
    "max_depth": [10],
    "min_samples_leaf": [4],
    "min_samples_split": [10],
    "n_estimators": [200],
}

grid_search = RandomizedSearchCV(
    estimator=RandomForestRegressor(random_state=42),
    param_distributions=param_grid,
    n_iter=30,
    cv=3,
    verbose=2,
    random_state=42,
    n_jobs=-1,
)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Print the best parameters
print("Best Parameters:", grid_search.best_params_)




sampled_df = df.sample(frac=0.01, random_state=42)

# 2. Split the data into training and testing sets
X = sampled_df.drop("8day_points", axis=1)
y = sampled_df["8day_points"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(X_train.shape, y_train.shape)
# Use the best estimator for further predictions and analysis
best_model = grid_search.best_estimator_


# 3. Train a regression model
model = best_model
model.fit(X_train, y_train)

# 4. Output sorted feature importances
feature_importances = pd.DataFrame(
    model.feature_importances_, index=X_train.columns, columns=["importance"]
).sort_values("importance", ascending=False)
print("Feature Importances:\n", feature_importances)

# Calculate R-squared values for train and test sets
r2_train = r2_score(y_train, model.predict(X_train))
r2_test = r2_score(y_test, model.predict(X_test))

print(f"train: {r2_train}, test {r2_test}")

# 5. Plotting Predictions vs True Values for Training Set
y_train_pred = model.predict(X_train)
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.scatter(y_train, y_train_pred, alpha=0.5)
plt.xlabel("True Values (Train)")
plt.ylabel("Predictions (Train)")
plt.title(f"Training Set: True vs Predicted Values\nR-squared = {r2_train:.2f}")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--", lw=4)

# Plotting Predictions vs True Values for Testing Set
y_test_pred = model.predict(X_test)
plt.subplot(1, 2, 2)
plt.scatter(y_test, y_test_pred, alpha=0.5)
plt.xlabel("True Values (Test)")
plt.ylabel("Predictions (Test)")
plt.title(f"Testing Set: True vs Predicted Values\nR-squared = {r2_test:.2f}")
plt.plot([y.min(), y.max()], [y.min(), y.max()], "k--", lw=4)

plt.tight_layout()
plt.show()
