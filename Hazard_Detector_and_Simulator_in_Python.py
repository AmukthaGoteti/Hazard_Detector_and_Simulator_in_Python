import itertools
import random
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt

# ============================================================
# Boolean Function Engine
# ============================================================

class BooleanFunction:
    def __init__(self, expression: str, variables: List[str]):
        self.expression = expression
        self.variables = variables
        self.compiled = compile(expression, "<expr>", "eval")

    def evaluate(self, values: Tuple[int, ...]) -> int:
        env = dict(zip(self.variables, map(bool, values)))
        return int(eval(self.compiled, {}, env))


# ============================================================
# Truth Table
# ============================================================

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


# ============================================================
# Delay Model
# ============================================================

class DelayModel:
    def __init__(self, variables: List[str], delay_range=(1, 5)):
        self.delays = {
            v: random.randint(*delay_range) for v in variables
        }

    def delay_of(self, variable):
        return self.delays[variable]


# ============================================================
# Transition Simulator (Gate-Level)
# ============================================================

class TransitionSimulator:
    def __init__(self, logic: BooleanFunction, delay_model: DelayModel):
        self.logic = logic
        self.delay_model = delay_model

    def simulate(self, start, end):
        diff = [i for i in range(len(start)) if start[i] != end[i]]
        timelines = []

        for order in itertools.permutations(diff):
            t = 0
            state = list(start)
            timeline = [(t, self.logic.evaluate(tuple(state)))]

            for idx in order:
                var = self.logic.variables[idx]
                t += self.delay_model.delay_of(var)
                state[idx] = end[idx]
                timeline.append((t, self.logic.evaluate(tuple(state))))

            timelines.append(timeline)

        return timelines


# ============================================================
# Hazard Detector (Professional Grade)
# ============================================================

class HazardDetector:
    def __init__(self, tt: TruthTable, simulator: TransitionSimulator):
        self.tt = tt.table
        self.sim = simulator

    @staticmethod
    def hamming(a, b):
        return sum(x != y for x, y in zip(a, b))

    @staticmethod
    def toggle_count(wave):
        return sum(wave[i][1] != wave[i - 1][1] for i in range(1, len(wave)))

    def detect(self, monte_carlo_runs=20):
        hazards = []

        for s1, s2 in itertools.combinations(self.tt.keys(), 2):
            hd = self.hamming(s1, s2)
            v1, v2 = self.tt[s1], self.tt[s2]

            glitch_count = 0
            worst_wave = None
            max_toggles = 0

            for _ in range(monte_carlo_runs):
                waves = self.sim.simulate(s1, s2)
                for w in waves:
                    toggles = self.toggle_count(w)
                    if toggles > 0:
                        glitch_count += 1
                        if toggles > max_toggles:
                            max_toggles = toggles
                            worst_wave = w

            if glitch_count == 0:
                continue

            confidence = glitch_count / monte_carlo_runs

            if hd == 1 and v1 == v2:
                htype = "Static-1 Hazard" if v1 == 1 else "Static-0 Hazard"
            elif hd >= 2 and v1 != v2:
                htype = "Dynamic Hazard"
            elif hd >= 2 and v1 == v2:
                htype = "Essential Hazard"
            else:
                continue

            hazards.append({
                "type": htype,
                "from": s1,
                "to": s2,
                "confidence": round(confidence, 2),
                "severity": max_toggles,
                "timeline": worst_wave,
                "explanation": self._explain(htype)
            })

        return hazards

    @staticmethod
    def _explain(htype):
        explanations = {
            "Static-1 Hazard": "Unequal delays in OR reconvergent paths.",
            "Static-0 Hazard": "Unequal delays in AND reconvergent paths.",
            "Dynamic Hazard": "Multiple transitions before stabilization.",
            "Essential Hazard": "Unavoidable delay dependency."
        }
        return explanations.get(htype, "Unknown behavior")


# ============================================================
# Consensus Term Generator
# ============================================================

class ConsensusGenerator:
    @staticmethod
    def suggest(a, b, vars):
        term = []
        for i, v in enumerate(vars):
            if a[i] == b[i]:
                term.append(v if a[i] else f"~{v}")
        return " & ".join(term) if term else None


# ============================================================
# Waveform Visualization
# ============================================================

def plot_waveform(wave, title):
    t = [x[0] for x in wave]
    y = [x[1] for x in wave]

    plt.figure(figsize=(8, 3))
    plt.step(t, y, where="post")
    plt.ylim(-0.2, 1.2)
    plt.xlabel("Time")
    plt.ylabel("Output")
    plt.title(title)
    plt.grid(True)
    plt.show()


# ============================================================
# User Interface
# ============================================================

def main():
    print("\nAdvanced Logic Hazard Analyzer\n")

    expr = input("Enter Boolean expression (& | ~): ")
    variables = [v.strip() for v in input("Variables (comma-separated): ").split(",")]

    show_tt = input("Show truth table? (y/n): ").lower() == "y"
    show_wave = input("Show waveform? (y/n): ").lower() == "y"

    logic = BooleanFunction(expr, variables)
    tt = TruthTable(logic)
    delay_model = DelayModel(variables)
    sim = TransitionSimulator(logic, delay_model)
    detector = HazardDetector(tt, sim)

    if show_tt:
        tt.display()

    hazards = detector.detect()

    print("\n--- Hazard Analysis Report ---\n")

    if not hazards:
        print("✔ Function is logically and delay-robust under simulated conditions.")
        return

    for i, h in enumerate(hazards, 1):
        print(f"Hazard {i}: {h['type']}")
        print(f"Transition: {h['from']} → {h['to']}")
        print(f"Confidence: {h['confidence'] * 100:.0f}%")
        print(f"Severity (toggles): {h['severity']}")
        print(f"Explanation: {h['explanation']}")

        fix = ConsensusGenerator.suggest(h["from"], h["to"], variables)
        if fix:
            print(f"Suggested Consensus Term: {fix}")

        if show_wave and h["timeline"]:
            plot_waveform(h["timeline"], h["type"])

        print("-" * 60)


if __name__ == "__main__":
    main()