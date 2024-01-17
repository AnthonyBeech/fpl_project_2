"""THis script will form the blueprint for a flask app where each week a
new model will be trained on the laest data by running src/pipeline/train.py.
This script outputs a pickle file that will be used to make predictions along with plots
and metrics that will be displayed on the flask app. Also the time of the last training
will be displayed on the flask app. """

import os
import json
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

bp = Blueprint("train", __name__, url_prefix="/train")


@bp.route("/")
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
