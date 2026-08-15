QUESTIONS = [
    {"question": "Which keyword defines a function?", "options": ["A. func", "B. def", "C. make"], "answer": "b"},
    {"question": "Which type stores key-value pairs?", "options": ["A. dict", "B. tuple", "C. set"], "answer": "a"},
    {"question": "What does len([1, 2, 3]) return?", "options": ["A. 2", "B. 3", "C. 4"], "answer": "b"},
]


def normalize_answer(answer: str) -> str:
    return answer.strip().lower()[:1]


def calculate_score(questions: list[dict], answers: list[str]) -> int:
    return sum(normalize_answer(given) == item["answer"] for item, given in zip(questions, answers))


def main() -> None:
    answers = []
    for item in QUESTIONS:
        print("\n" + item["question"])
        print("\n".join(item["options"]))
        answers.append(input("Answer: "))
    score = calculate_score(QUESTIONS, answers)
    print(f"\nScore: {score}/{len(QUESTIONS)}")


if __name__ == "__main__":
    main()
