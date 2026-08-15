from pathlib import Path
import argparse
import json
import os
import re

import matplotlib.pyplot as plt
import pandas as pd


POSITIVE = {"great", "comfortable", "good", "smooth", "fast", "excellent", "compact", "useful", "bright", "amazing", "easy", "clear", "simple", "value", "quick", "quality", "well"}
NEGATIVE = {"poor", "drops", "slow", "stopped", "weak", "inaccurate", "cheap", "blurry", "slowly", "failed"}
BASE = Path(__file__).parent


def sentiment(text: str) -> str:
    words = set(re.findall(r"[a-z]+", text.lower()))
    score = len(words & POSITIVE) - len(words & NEGATIVE)
    return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"


def ai_summary(stats: dict) -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("AI summary skipped: set OPENAI_API_KEY locally, then run with --ai.")
        return
    from openai import OpenAI

    response = OpenAI().responses.create(
        model="gpt-5-mini",
        input=(
            "Write a concise, factual management summary of these aggregated review "
            "statistics. Give three findings and two actions. Do not invent data.\n"
            + json.dumps(stats)
        ),
    )
    print("\nAI management summary:\n" + response.output_text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ai", action="store_true", help="Generate an optional OpenAI summary")
    args = parser.parse_args()

    df = pd.read_csv(BASE / "data/reviews.csv")
    df["sentiment"] = df["review"].map(sentiment)
    counts = df["sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)
    product_ratings = df.groupby("product")["rating"].mean().sort_values(ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    counts.plot.bar(ax=axes[0], color=["#22c55e", "#94a3b8", "#ef4444"], title="Review sentiment")
    product_ratings.sort_values().plot.barh(ax=axes[1], color="#6366f1", title="Average rating by product")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Reviews")
    axes[1].set_xlabel("Rating (1–5)")
    axes[1].set_ylabel("")
    fig.suptitle("Customer Review Insights", fontsize=16, fontweight="bold")
    fig.tight_layout()
    (BASE / "outputs").mkdir(exist_ok=True)
    fig.savefig(BASE / "outputs/review_insights.png", dpi=160, bbox_inches="tight")
    plt.close(fig)

    stats = {
        "review_count": int(len(df)),
        "average_rating": round(float(df["rating"].mean()), 2),
        "sentiment_counts": {k: int(v) for k, v in counts.items()},
        "average_rating_by_product": {k: round(float(v), 2) for k, v in product_ratings.items()},
    }
    print(json.dumps(stats, indent=2))
    if args.ai:
        ai_summary(stats)


if __name__ == "__main__":
    main()
