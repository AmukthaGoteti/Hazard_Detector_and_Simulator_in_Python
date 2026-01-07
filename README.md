# 💬 Emotional Support Chatbot (Python)

A **rule-based emotional support chatbot** built using Python that engages in natural conversation, recognizes emotional cues, and responds with empathetic, supportive, and encouraging messages.

This project demonstrates **string processing, regular expressions, control flow, and conversational logic**, making it ideal for beginners and for showcasing a meaningful Python mini-project.

---

## 🌟 Features

* Friendly greetings and farewells
* Emotion-aware responses (sad, happy, anxious, lonely, stressed, etc.)
* Motivation and encouragement support
* Study, career, and interview guidance
* Casual conversation (jokes, hobbies, travel, food, music, sports)
* Simple rule-based Natural Language Processing using **regex**
* Randomized responses for natural interaction

---

## 🛠️ Technologies Used

* **Python 3**
* **Regular Expressions (`re`)**
* **Random module**

---

## 📂 Project Structure

```bash
├── chatbot.py
└── README.md
```

---

## ▶️ How to Run

### Prerequisites

* Python **3.9+** recommended

### Run the Chatbot

```bash
python chatbot.py
```

---

## 🧠 How It Works

### Pattern Matching

* User input is matched against predefined **regex patterns**
* Each pattern maps to a list of suitable responses
* A random response is selected to keep conversations natural

### Flow

1. User enters a message
2. Input is converted to lowercase
3. Regex patterns are checked using `re.search()`
4. A relevant response is returned
5. Chat continues until the user types **bye** or **goodbye**

---

## 🗣️ Example Interaction

```text
You: I feel very stressed today
Bot: Burnout is a sign you’ve been pushing hard. Rest matters too.

You: tell me a joke
Bot: Why do programmers prefer dark mode? Because light attracts bugs!

You: goodbye
Bot: Goodbye! Take care.
```

---

## 🎯 Learning Outcomes

By building this project, you will learn:

* Regex-based intent recognition
* Rule-based chatbot design
* Handling emotional and conversational states
* Clean function-based Python structure
* Randomized response generation

---

## 🚀 Possible Enhancements

* GUI using **Tkinter**
* Conversation memory
* Logging chat history
* Voice input/output
* NLP libraries (NLTK / spaCy)
* Sentiment analysis
* Web or mobile integration

---

## ⚠️ Disclaimer

This chatbot is **not a replacement for professional mental health support**.
It is intended for **educational and conversational purposes only**.

---

**Happy coding and thoughtful conversations! 🌱**
