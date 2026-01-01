import itertools
from typing import List, Tuple
import matplotlib.pyplot as plt


# ---------------- Boolean Logic ---------------- #

class BooleanFunction:
    def __init__(self, expression: str, variables: List[str]):
        self.expression = expression
        self.variables = variables
        self.compiled = compile(expression, "<expr>", "eval")

    def evaluate(self, values: Tuple[int, ...]) -> int:
        env = {v: bool(values[i]) for i, v in enumerate(self.variables)}
        return int(eval(self.compiled, {}, env))


# ---------------- Truth Table ---------------- #

class TruthTable:
    def __init__(self, logic: BooleanFunction):
        self.logic = logic
        self.table = self._generate()

    def _generate(self):
        return {
            inputs: self.logic.evaluate(inputs)
            for inputs in itertools.product([0, 1], repeat=len(self.logic.variables))
        }

    def display(self):
        print("\nTruth Table")
        print(" ".join(self.logic.variables), "| F")
        print("-" * (4 * len(self.logic.variables)))
        for k, v in self.table.items():
            print(" ".join(map(str, k)), "|", v)


# ---------------- Transition Simulator ---------------- #

class TransitionSimulator:
    def __init__(self, logic: BooleanFunction):
        self.logic = logic

    def simulate_all_paths(self, start, end):
        diff = [i for i in range(len(start)) if start[i] != end[i]]
        waves = []

        for order in itertools.permutations(diff):
            state = list(start)
            wave = [self.logic.evaluate(tuple(state))]

            for idx in order:
                state[idx] = end[idx]
                wave.append(self.logic.evaluate(tuple(state)))

            waves.append(wave)

        return waves


# ---------------- Hazard Detection ---------------- #

class HazardDetector:
    def __init__(self, truth_table: TruthTable, simulator: TransitionSimulator):
        self.table = truth_table.table
        self.simulator = simulator

    @staticmethod
    def hamming_distance(a, b):
        return sum(x != y for x, y in zip(a, b))

    @staticmethod
    def toggle_count(wave):
        return sum(wave[i] != wave[i - 1] for i in range(1, len(wave)))

    def detect(self):
        hazards = []
        states = list(self.table.keys())

        for s1, s2 in itertools.combinations(states, 2):
            hd = self.hamming_distance(s1, s2)
            v1, v2 = self.table[s1], self.table[s2]

            waves = self.simulator.simulate_all_paths(s1, s2)

            # ---------- STATIC HAZARDS ----------
            if hd == 1 and v1 == v2:
                for wave in waves:
                    if self.toggle_count(wave) >= 1:
                        htype = "Static-1 Hazard" if v1 == 1 else "Static-0 Hazard"
                        hazards.append((s1, s2, htype, wave))
                        break

            # ---------- DYNAMIC HAZARDS ----------
            if hd >= 2 and v1 != v2:
                for wave in waves:
                    if self.toggle_count(wave) > 1:
                        hazards.append((s1, s2, "Dynamic Hazard", wave))
                        break

        return hazards


# ---------------- Consensus Term ---------------- #

class ConsensusGenerator:
    @staticmethod
    def suggest(start, end, variables):
        terms = []
        for i, var in enumerate(variables):
            if start[i] == end[i]:
                terms.append(var if start[i] else f"~{var}")
        return " & ".join(terms) if terms else None


# ---------------- Waveform Plot ---------------- #

def plot_waveform(wave, title):
    plt.figure()
    plt.step(range(len(wave)), wave, where="post")
    plt.ylim(-0.2, 1.2)
    plt.xlabel("Time")
    plt.ylabel("Output")
    plt.title(title)
    plt.grid(True)
    plt.show()


# ---------------- User Input ---------------- #

def get_user_input():
    print("\n--- Hazard Detector Input ---\n")
    expr = input("Enter Boolean expression (& | ~): ").strip()
    variables = [v.strip() for v in input("Variables (comma-separated): ").split(",")]

    show_tt = input("Show truth table? (y/n): ").lower() == "y"
    show_wave = input("Show waveform? (y/n): ").lower() == "y"

    return expr, variables, show_tt, show_wave


# ---------------- Main ---------------- #

def main():
    expr, variables, show_tt, show_wave = get_user_input()

    logic = BooleanFunction(expr, variables)
    tt = TruthTable(logic)
    sim = TransitionSimulator(logic)
    detector = HazardDetector(tt, sim)

    if show_tt:
        tt.display()

    hazards = detector.detect()

    print("\n--- Hazard Analysis ---\n")

    if not hazards:
        print("✔ Logic is HAZARD-FREE")
        return

    for i, (s1, s2, htype, wave) in enumerate(hazards, 1):
        print(f"Hazard {i}: {htype}")
        print(f"Transition: {s1} → {s2}")
        print(f"Waveform: {wave}")

        fix = ConsensusGenerator.suggest(s1, s2, variables)
        if fix:
            print(f"Suggested consensus term: {fix}")

        if show_wave:
            plot_waveform(wave, f"{htype}: {s1} → {s2}")

        print("-" * 60)


if __name__ == "__main__":
    main()