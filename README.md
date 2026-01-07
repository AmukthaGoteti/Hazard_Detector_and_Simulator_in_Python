# 🔍 Hazard Detector and Simulator in Python

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Domain](https://img.shields.io/badge/Domain-Digital%20Logic-orange.svg)
![Focus](https://img.shields.io/badge/Focus-Hazard%20Detection-purple.svg)
![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)

A Python-driven framework designed for **automatic detection, simulation, and visualization of logic hazards** in combinational digital circuits.
The analyzer incorporates realistic gate-delay modeling, identifies glitches during input transitions, and recommends Boolean corrections using consensus terms.

---

## 📌 Problem Statement

A Boolean expression may be logically sound, yet **unequal propagation delays** in real hardware can still introduce transient output glitches—commonly referred to as **logic hazards**.

Traditional manual analysis:

* Does not scale well
* Overlooks timing-induced failures
* Becomes error-prone as complexity increases

This project delivers a **fully automated, timing-aware approach** to hazard analysis.

---

## 🚀 Core Capabilities

* Custom Boolean expression input
* Complete truth table generation
* Randomized gate-delay assignment
* Gate-level transition simulation
* Automated identification of:

  * Static hazards
  * Dynamic hazards
  * Essential hazards
* Hazard severity evaluation via toggle counts
* Automatic consensus-term recommendations
* Optional waveform-based visualization
* Clean, modular, and extensible design

---

## 🧠 Hazard Classification

| Hazard Type   | Description                                                |
| ------------- | ---------------------------------------------------------- |
| **Static**    | Output momentarily changes despite a stable expected value |
| **Dynamic**   | Output oscillates multiple times before settling           |
| **Essential** | Hazard caused by unavoidable delay dependencies            |

---

## 🏗️ Architecture Overview

```
User Input
│
▼
Boolean Expression Engine
│
▼
Truth Table Generator
│
▼
Delay Modeling Module
│
▼
Transition Simulator
│
▼
Hazard Detection Engine
│
▼
Fix Recommendations + Waveform Output
```

---

## 📂 Repository Layout

```
advanced-logic-hazard-analyzer/
│
├── Hazard_Detector_and_Simulator_in_Python.py   # End-to-end hazard analysis engine
├── README.md                                   # Project documentation
```

---

## 🛠️ Technology Stack

* Python 3.x
* Boolean Algebra
* Digital Logic Design Principles
* Monte Carlo–based Delay Simulation
* Matplotlib for waveform visualization

---

## ▶️ Quick Start

### 1️⃣ Install Requirements

```bash
pip install matplotlib
```

### 2️⃣ Execute the Analyzer

```bash
python main.py
```

---

## 🧪 Sample Input

```text
Enter Boolean expression (& | ~): (~A & ~B) | (A & ~C)
Variables (comma-separated): A, B, C
Show truth table? (y/n): y
Show waveform? (y/n): y
```

---

## 📊 Example Output

```text
Hazard 1: Static-1 Hazard
Transition: (0, 0, 0) → (0, 0, 1)
Confidence: 35%
Severity (toggles): 2
Explanation: OR reconvergent path delay mismatch
Suggested Consensus Term: ~A & ~B
```

---

## 📈 Waveform Analysis

> Output glitches are visualized using step-based waveforms to enable precise timing inspection.

**Example:**
Waveform plots clearly expose transient behavior during critical input transitions.

---

## 🧩 Hazard Elimination Strategy

To remove static hazards without altering logic functionality, the analyzer proposes **consensus terms**.

**Illustration**

```text
Original: A·B + A'·C
Improved: A·B + A'·C + B·C
```

---

## 🎯 What Makes This Project Distinct

* Captures **real-world timing behavior**, not idealized logic
* Automates a traditionally manual verification process
* Connects digital logic theory with practical hardware concerns
* Well-suited for:

  * ECE academic projects
  * Hardware verification practice
  * Research groundwork
  * Strong technical portfolios and interviews

---

## 🔮 Planned Enhancements

* SOP and POS canonical form support
* Karnaugh map-based visualization
* Gate-level netlist parsing
* Configurable delay distributions
* Exportable analysis reports
* Integration with HDL-based workflows