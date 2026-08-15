# 10 — Customer Review Insights

**Question:** What sentiment and product themes appear in customer feedback?

The default analysis is fully local: it scores a transparent sentiment lexicon, summarizes product ratings, and charts sentiment distribution. An optional `--ai` flag uses the OpenAI Responses API to turn the computed statistics into a short management summary.

```bash
python analysis.py
# Optional, after setting OPENAI_API_KEY locally:
python analysis.py --ai
```

Never commit API keys. The repository's `.gitignore` excludes `.env` files.

**Output:** `outputs/review_insights.png`

**Skills:** text cleaning, sentiment analysis, review analytics, optional AI-assisted reporting.
