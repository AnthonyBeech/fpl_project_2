import os
import json
import pandas as pd
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from .auth import login_required

bp = Blueprint("train", __name__, url_prefix="/models")


@bp.route("/train")
@login_required
def train():
    # Define the path to the static directory
    static_dir = "flask_main/flaskr/static"

    # Load statistics from JSON file
    stats_file = os.path.join(static_dir, "model_statistics.json")
    with open(stats_file, "r") as file:
        stats = json.load(file)

    # Define the URLs for the plot images
    plot_url = "model_performance_plots.png"

    # Render the HTML template, passing the statistics and plot URL
    return render_template("train/index.html", stats=stats, plot_url=plot_url)


@bp.route("/predict")
@login_required
def predict():
    predictions_df = pd.read_csv("data/predicted/predict_data.csv")

    # Convert the DataFrame to a list of dictionaries for easy rendering in HTML
    predictions = predictions_df.to_dict(orient="records")

    # Render the HTML template, passing the statistics, plot URL, and predictions
    return render_template("predict/index.html", predictions=predictions)
