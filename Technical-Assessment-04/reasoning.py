"""TA4: simple weather advice using rules and past cases."""
from copy import deepcopy

# Five facts in three categories: measurements, weather, and context.
FACTS = {
    "temperature": 32, "humidity": 85,              # Measurements
    "is_raining": True,                          # Weather
    "is_outdoors": True, "is_occupied": True,     # Context
}
CASES = [
    {"id": "C001", "problem": {
        "temperature": 33, "humidity": 80, "is_raining": True,
        "is_outdoors": True, "is_occupied": True,
    }, "solution": "Cool the room, reduce humidity, and bring a raincoat."},
    {"id": "C002", "problem": {
        "temperature": 25, "humidity": 60, "is_raining": False,
        "is_outdoors": True, "is_occupied": True,
    }, "solution": "Continue outdoor activities and carry water."},
    {"id": "C003", "problem": {
        "temperature": 28, "humidity": 70, "is_raining": True,
        "is_outdoors": True, "is_occupied": False,
    }, "solution": "Bring a raincoat and switch off unused cooling equipment."},
]


def rule_hot(facts):
    if facts["temperature"] > 30 and facts["is_occupied"]:
        return "Turn on a fan or air conditioner."


def rule_rain(facts):
    if facts["is_raining"] and facts["is_outdoors"]:
        return "Bring an umbrella or raincoat."


def rule_humid(facts):
    if facts["humidity"] > 80 and facts["is_occupied"]:
        return "Use a dehumidifier."


def infer(facts):
    actions = []
    for rule in [rule_hot, rule_rain, rule_humid]:
        action = rule(facts)
        if action:
            actions.append(action)
    return actions


def similarity(new, old):
    # Numeric features use fixed ranges; Boolean features use exact matches.
    scores = [
        1 - abs(new["temperature"] - old["temperature"]) / 50,
        1 - abs(new["humidity"] - old["humidity"]) / 100,
        new["is_raining"] == old["is_raining"],
        new["is_outdoors"] == old["is_outdoors"],
        new["is_occupied"] == old["is_occupied"],
    ]
    return sum(scores) / len(scores)


def retrieve(facts, cases):
    # Highest score first; case ID breaks ties.
    return sorted(cases, key=lambda case:
                  (-similarity(facts, case["problem"]), case["id"]))


def retain(cases, facts, solution):
    new_case = {"id": f"C{len(cases) + 1:03d}",
                "problem": facts.copy(), "solution": solution}
    cases.append(new_case)
    return new_case


if __name__ == "__main__":
    cases = deepcopy(CASES)
    print("INPUT:", FACTS)
    print("\nRBR: Check all three rules")
    for action in infer(FACTS):
        print("-", action)
    print("\nCBR: Compare the current facts with each past case")
    ranked = retrieve(FACTS, cases)
    for case in ranked:
        print(case["id"], f"similarity={similarity(FACTS, case['problem']):.3f}")
    best = ranked[0]                                      # Retrieve
    print("Retrieve:", best["id"])
    solution = best["solution"]                          # Reuse
    print("Reuse:", solution)
    revision = input("Revise (Enter to keep): ").strip()  # Revise
    solution = revision or solution
    saved = retain(cases, FACTS, solution)                # Retain
    print("Final solution:", solution)
    print("Retained:", saved["id"], "| Case count:", len(cases))
