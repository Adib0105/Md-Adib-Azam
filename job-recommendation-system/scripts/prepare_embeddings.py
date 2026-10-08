"""Operator-only model download; never called from a Flask request."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--revision", required=True, help="Exact 40-character upstream model commit SHA"
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.revision):
        parser.error("Pin the exact upstream model commit, not a moving branch.")
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("Use an empty model directory to preserve its version metadata.")
    from sentence_transformers import SentenceTransformer

    name = "sentence-transformers/all-MiniLM-L6-v2"
    model = SentenceTransformer(
        name,
        revision=args.revision,
        trust_remote_code=False,
        device="cpu",
        model_kwargs={"use_safetensors": True},
    )
    if model.get_sentence_embedding_dimension() != 384:
        raise ValueError("Unexpected model dimension.")
    model.save(str(args.output), safe_serialization=True)
    (args.output / "jobmatch-model.json").write_text(
        json.dumps(
            {
                "model_name": name,
                "revision": args.revision,
                "dimension": 384,
                "purpose": "pretrained semantic inference; not fine-tuned on JobMatch labels",
            },
            indent=2,
        )
        + "\n"
    )
    print(
        f"Prepared local model at {args.output.resolve()}. Set EMBEDDINGS_ENABLED=true, EMBEDDING_MODEL_PATH to that directory, and EMBEDDING_MODEL_REVISION={args.revision}; restart the application."
    )


if __name__ == "__main__":
    main()
