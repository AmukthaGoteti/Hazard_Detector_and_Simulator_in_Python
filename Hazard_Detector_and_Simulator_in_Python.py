"""
Smart Hazard Detector and Simulator
-----------------------------------

Features:
- User-input Boolean expression & variables
- Truth table generation (optional display)
- Static-0, Static-1, Dynamic hazard detection
- Transition-level simulation with unequal delays
- Consensus-term suggestions
- Optional waveform visualization
"""

import itertools
from typing import List, Tuple
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

class BooleanFunction:
    def __init__(self, expression: str, variables: List[str]):
        self.expression = expression
        self.variables = variables
        self.compiled = compile(expression, "<expr>", "eval")

    def evaluate(self, values: Tuple[int, ...]) -> int:
        env = dict(zip(self.variables, map(bool, values)))
        return int(eval(self.compiled, {}, env))

class TruthTable:
    def __init__(self, logic: BooleanFunction):
        self.logic = logic
        self.table = self._generate()

    def _generate(self):
        return {
            values: self.logic.evaluate(values)
            for values in itertools.product([0, 1], repeat=len(self.logic.variables))
        }

    def display(self):
        print("\nTruth Table:")
        header = " ".join(self.logic.variables) + " | F"
        print(header)
        print("-" * len(header))
        for inputs, output in self.table.items():
            print(" ".join(map(str, inputs)), "|", output)

class TransitionSimulator:
    def __init__(self, logic: BooleanFunction):
        self.logic = logic

    @staticmethod
    def is_adjacent(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1

    def simulate(self, start, end):
        idx = next(i for i in range(len(start)) if start[i] != end[i])
        intermediate = list(start)
        intermediate[idx] = end[idx]

        return [
            self.logic.evaluate(state)
            for state in (start, tuple(intermediate), end)
        ]

class HazardDetector:
    def __init__(self, truth_table: TruthTable, simulator: TransitionSimulator):
        self.table = truth_table.table
        self.simulator = simulator

    @staticmethod
    def toggle_count(wave):
        return sum(wave[i] != wave[i - 1] for i in range(1, len(wave)))

    def detect(self):
        hazards = []
        states = list(self.table.keys())

        for s1, s2 in itertools.combinations(states, 2):
            if not self.simulator.is_adjacent(s1, s2):
                continue

            wave = self.simulator.simulate(s1, s2)
            v1, v2 = self.table[s1], self.table[s2]

            if v1 == v2 and any(x != v1 for x in wave):
                hazard = "Static-1 Hazard" if v1 else "Static-0 Hazard"
                hazards.append((s1, s2, hazard, wave))

            elif v1 != v2 and self.toggle_count(wave) > 1:
                hazards.append((s1, s2, "Dynamic Hazard", wave))

        return hazards

class ConsensusGenerator:
    @staticmethod
    def suggest(start, end, variables):
        terms = []
        for i, var in enumerate(variables):
            if start[i] == end[i]:
                terms.append(var if start[i] else f"~{var}")
        return " & ".join(terms) if terms else None

def plot_waveform(wave, title):
    plt.figure()
    plt.step(range(len(wave)), wave, where="post")
    plt.ylim(-0.2, 1.2)
    plt.xlabel("Time")
    plt.ylabel("Output")
    plt.title(title)
    plt.grid(True)
    plt.show(block=True)

def get_user_input():
    print("\n--- Hazard Detector Input ---\n")
    expr = input("Enter Boolean expression (use &, |, ~): ").strip()
    variables = input("Enter variables (comma-separated): ").split(",")
    variables = [v.strip() for v in variables]

    show_tt = input("Show truth table? (y/n): ").lower() == "y"
    show_wave = input("Show waveform for hazards? (y/n): ").strip().lower() in ("y", "yes")

    return expr, variables, show_tt, show_wave

def main():
    expr, variables, show_tt, show_wave = get_user_input()

    logic = BooleanFunction(expr, variables)
    truth_table = TruthTable(logic)
    simulator = TransitionSimulator(logic)
    detector = HazardDetector(truth_table, simulator)

    if show_tt:
        truth_table.display()

    hazards = detector.detect()

    print("\n--- Hazard Analysis Result ---\n")

    if not hazards:
        print("✔ The given logic is HAZARD-FREE.")
        return

    print(f"⚠ Hazardous Logic Detected ({len(hazards)} case(s)):\n")

    for i, (start, end, htype, wave) in enumerate(hazards, 1):
        print(f"Hazard {i}: {htype}")
        print(f"Transition: {start} → {end}")
        print(f"Waveform values: {wave}")

        fix = ConsensusGenerator.suggest(start, end, variables)
        if fix:
            print(f"Suggested consensus term: {fix}")

        if show_wave:
            plot_waveform(wave, f"{htype}: {start} → {end}")

        print("-" * 60)


if __name__ == "__main__":
    main()