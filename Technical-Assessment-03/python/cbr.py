"""A small case-based math tutor using a JSON case base."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASE_FILE = ROOT / "cases.json"
TOPICS = {
    "Fractions": ["Unlike denominators", "Numerator and denominator confusion"],
    "Linear equations": ["Sign error", "Unbalanced operations"],
    "Geometry": ["Wrong formula", "Unit confusion"],
}
FORMATS = ["Visual", "Worked example", "Practice"]
DEMO = {"topic": "Fractions", "error": "Unlike denominators", "mastery": 40,
        "format": "Worked example", "minutes": 15}


def load_cases(path=CASE_FILE):
    if not path.exists():
        path = ROOT / "seed_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))


def validate(problem):
    topic = problem.get("topic")
    if topic not in TOPICS or problem.get("error") not in TOPICS[topic]:
        raise ValueError("Select a topic and a matching error.")
    if problem.get("format") not in FORMATS:
        raise ValueError("Select a supported lesson format.")
    for key, low, high in [("mastery", 0, 100), ("minutes", 5, 60)]:
        value = problem.get(key)
        if type(value) is not int or not low <= value <= high:
            raise ValueError(f"{key} must be a whole number from {low} to {high}.")


def retrieve(problem, cases):
    """Compare each past case and return the highest scores first."""
    validate(problem)
    results = []
    for case in cases:
        past = case["problem"]
        score = (0.30 * (problem["topic"] == past["topic"])
                 + 0.35 * (problem["error"] == past["error"])
                 + 0.20 * (1 - abs(problem["mastery"] - past["mastery"]) / 100)
                 + 0.15 * (problem["format"] == past["format"]))
        results.append({"case": case, "score": score})
    return sorted(results, key=lambda item: (-item["score"], item["case"]["id"]))


def adapt(problem, case):
    """Reuse feedback and adjust the lesson to the learner's needs."""
    validate(problem)
    if any(problem[key] != case["problem"][key] for key in ["topic", "error"]):
        raise ValueError("No matching lesson. Ask a teacher to add a case.")
    solution = case["solution"].copy()
    exercises = solution["exercises"]
    if problem["mastery"] < 50:
        exercises += 2
        solution["support"] = "Guided steps with a check after each step"
    else:
        solution["support"] = "Independent practice with a final check"
    time_limit = max(1, (problem["minutes"] - 3) // 2)
    solution["exercises"] = min(exercises, time_limit)
    solution["format"] = problem["format"]
    solution["minutes"] = problem["minutes"]
    return solution


def retain(problem, solution, source_id, outcome, post_mastery, review_id, path=CASE_FILE):
    """Save a reviewed successful lesson. A review ID prevents duplicate saves."""
    validate(problem)
    if not solution["feedback"].strip() or not outcome.strip() or not review_id.strip():
        raise ValueError("Enter reviewed feedback, an outcome and a review ID.")
    if type(post_mastery) is not int or not problem["mastery"] < post_mastery <= 100:
        raise ValueError("Post-lesson mastery must improve and be at most 100.")
    cases = load_cases(path)
    for case in cases:
        if case.get("review_id") == review_id:
            return case
    if source_id not in [case["id"] for case in cases]:
        raise ValueError("The source case is missing.")
    new_case = {"id": f"C{len(cases) + 1:02}", "problem": problem.copy(),
                "solution": solution.copy(), "source_case_id": source_id,
                "outcome": {"notes": outcome.strip(), "post_mastery": post_mastery},
                "review_id": review_id}
    cases.append(new_case)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(cases, indent=2), encoding="utf-8")
    temporary.replace(path)
    return new_case


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save-demo", action="store_true")
    args = parser.parse_args()
    print("New problem:", DEMO)
    ranking = retrieve(DEMO, load_cases())
    print("Similarity ranking:")
    for item in ranking:
        print(item["case"]["id"], round(item["score"], 3))
    best = ranking[0]["case"]
    solution = adapt(DEMO, best)
    print("Retrieved case:", best["id"])
    print("Adapted lesson:", json.dumps(solution, indent=2))
    if args.save_demo:
        saved = retain(DEMO, solution, best["id"],
                       "Fictional demo: learner corrected 4 of 5 items.", 60, "cli-demo")
        print("New case saved:", saved["id"])
    print("Case base:", [case["id"] for case in load_cases()])
