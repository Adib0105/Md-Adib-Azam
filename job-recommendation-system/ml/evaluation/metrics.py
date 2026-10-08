"""Query-level ordinal metrics; relevance means label >= 2, not weak label 1."""

import math


def ranking_metrics(ranked_ids, judgments, ks=(5, 10, 20)):
    if any(k <= 0 for k in ks):
        raise ValueError("K must be positive.")
    if len(ranked_ids) != len(set(ranked_ids)) or any(
        j not in judgments for j in ranked_ids
    ):
        raise ValueError("Ranking contains duplicate or unjudged jobs.")
    if any(
        isinstance(label, bool) or not isinstance(label, int) or label not in range(4)
        for label in judgments.values()
    ):
        raise ValueError("Judgments must be ordinal labels 0–3.")
    relevant = sum(label >= 2 for label in judgments.values())

    def dcg(values):
        return sum((2**value - 1) / math.log2(i + 2) for i, value in enumerate(values))

    labels = [judgments[job] for job in ranked_ids]
    hits = 0
    average_precision = 0.0
    reciprocal = 0.0
    for i, label in enumerate(labels, 1):
        if label >= 2:
            hits += 1
            average_precision += hits / i
            if not reciprocal:
                reciprocal = 1 / i
    result = {
        "mrr": reciprocal,
        "map": average_precision / relevant if relevant else 0.0,
    }
    for k in ks:
        top = labels[:k]
        ideal = dcg(sorted(judgments.values(), reverse=True)[:k])
        result.update(
            {
                f"precision@{k}": sum(v >= 2 for v in top) / k,
                f"recall@{k}": sum(v >= 2 for v in top) / relevant if relevant else 0.0,
                f"ndcg@{k}": dcg(top) / ideal if ideal else 0.0,
            }
        )
    return result
