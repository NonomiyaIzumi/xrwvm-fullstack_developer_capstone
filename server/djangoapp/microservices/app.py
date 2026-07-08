"""Flask microservice that scores the sentiment of a dealer review.

Runs independently of the Django app (deployable as its own container/service)
and is called over HTTP by djangoapp.restapis.analyze_review_sentiments.
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()


def classify(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, scores


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "sentiment-analyzer"})


@app.route("/analyze/<path:text>", methods=["GET"])
def analyze(text):
    label, scores = classify(text)
    return jsonify({"sentiment": label, "scores": scores})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)
