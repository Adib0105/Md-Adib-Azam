# Decision brief: nlp-sentiment-intelligence

## Metrics

- **Macro F1**: 1.0
- **Reviews Scored**: 800
- **Negative Share Pct**: 35.0
- **Topic Distribution Drift**: 0.17
- **Drift Alert**: True

## Recommended actions

- Route high-confidence negative reviews to service recovery.
- Retrain vocabulary when the drift alert persists across two windows.
