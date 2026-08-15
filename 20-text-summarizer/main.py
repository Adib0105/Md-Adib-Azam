import argparse
import re
from collections import Counter
from pathlib import Path


STOPWORDS = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "in", "is", "it", "of", "on", "that", "the", "to", "was", "were", "will", "with"}


def split_sentences(text: str) -> list[str]:
    return [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text.strip()) if sentence.strip()]


def summarize(text: str, sentence_count: int = 3) -> str:
    sentences = split_sentences(text)
    if len(sentences) <= sentence_count:
        return " ".join(sentences)
    words = [word for word in re.findall(r"[a-z]+", text.lower()) if word not in STOPWORDS]
    frequencies = Counter(words)
    scores = []
    for index, sentence in enumerate(sentences):
        tokens = re.findall(r"[a-z]+", sentence.lower())
        score = sum(frequencies[token] for token in tokens if token in frequencies) / max(len(tokens), 1)
        scores.append((score, index))
    selected = sorted(index for _, index in sorted(scores, reverse=True)[:sentence_count])
    return " ".join(sentences[index] for index in selected)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a text file locally")
    parser.add_argument("file", type=Path)
    parser.add_argument("--sentences", type=int, default=3)
    args = parser.parse_args()
    print(summarize(args.file.read_text(encoding="utf-8"), args.sentences))


if __name__ == "__main__":
    main()
