"""
Mini Project: AI-Powered Python Training Assistant
====================================================
Demonstrates: OpenAI API integration, conversation memory,
              system prompt engineering, graceful fallback.

This simulates a chatbot a trainer could embed in their
course portal to answer students' Python questions 24/7.

Run: python chatbot_ai_assistant.py
     (Set OPENAI_API_KEY env var to enable live responses)
"""

import os
import sys
from datetime import datetime

try:
    import openai
    OPENAI_OK = True
except ImportError:
    OPENAI_OK = False

SYSTEM_PROMPT = """
You are PythonBot, a friendly and expert Python programming assistant
for students at NTUC LearningHub. Your role is to:

1. Explain Python concepts clearly with practical, real-world examples.
2. Debug student code patiently and explain the fix, not just provide it.
3. Suggest exercises and projects to reinforce learning.
4. Always use Singaporean context in examples when relevant (HDB, MRT, CPF etc.).
5. Encourage learners and celebrate their progress.
6. Keep responses concise — ideally under 200 words unless the topic demands more.

You support these NTUC LearningHub Python courses:
- Fundamentals of Python Programming
- Analyse Business Data Using Python
- Advanced Analytics and Machine Learning Using Python
- Deep Learning Models and AI Using Python
"""

FALLBACK_RESPONSES = {
    "list": (
        "A Python list is an ordered, mutable collection. Example:\n\n"
        "  mrt_stations = ['Jurong East', 'Buona Vista', 'Orchard']\n"
        "  print(mrt_stations[0])  # Output: Jurong East\n\n"
        "Lists support indexing, slicing, append(), remove(), and len()."
    ),
    "loop": (
        "Python has two main loops:\n\n"
        "  for i in range(5):       # iterates 0 to 4\n"
        "      print(i)\n\n"
        "  count = 0\n"
        "  while count < 5:         # continues while condition is True\n"
        "      count += 1\n\n"
        "Use 'for' when you know the number of iterations; 'while' when you don't."
    ),
    "function": (
        "Functions are reusable blocks of code:\n\n"
        "  def calculate_cpf(salary, rate=0.20):\n"
        "      return salary * rate\n\n"
        "  contribution = calculate_cpf(5000)\n"
        "  print(contribution)  # 1000.0\n\n"
        "Always include a docstring to document what your function does!"
    ),
    "pandas": (
        "pandas is the go-to library for data analysis in Python:\n\n"
        "  import pandas as pd\n"
        "  df = pd.read_csv('data.csv')\n"
        "  df.head()          # first 5 rows\n"
        "  df.describe()      # summary statistics\n"
        "  df['Salary'].mean()  # average salary\n\n"
        "It's used in every data analytics and ML project!"
    ),
}


class PythonTrainingBot:
    def __init__(self):
        self.conversation_history = []
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.use_live_api = bool(self.api_key) and OPENAI_OK
        if self.use_live_api:
            self.client = openai.OpenAI(api_key=self.api_key)

    def get_response(self, user_message: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_message})

        if self.use_live_api:
            response = self._call_openai()
        else:
            response = self._fallback_response(user_message)

        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def _call_openai(self) -> str:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}]
                         + self.conversation_history[-10:],   # keep last 10 turns
                max_tokens=400,
                temperature=0.6,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"[API Error: {e}]\n\n{self._fallback_response(self.conversation_history[-1]['content'])}"

    def _fallback_response(self, message: str) -> str:
        msg_lower = message.lower()
        for keyword, response in FALLBACK_RESPONSES.items():
            if keyword in msg_lower:
                return response
        return (
            "Great question! In a live session I'd connect to GPT-4o for a "
            "tailored answer. Set OPENAI_API_KEY to enable live responses.\n\n"
            "Try asking about: 'list', 'loop', 'function', or 'pandas'."
        )

    def run_demo(self):
        """Run a predefined demo conversation for portfolio showcase."""
        demo_questions = [
            "What is a Python list and how do I use it?",
            "How do I read a CSV file using pandas?",
        ]
        print("\n" + "="*65)
        print("  AI MINI PROJECT — PYTHON TRAINING CHATBOT DEMO")
        print(f"  Mode: {'🟢 Live GPT-4o' if self.use_live_api else '🟡 Fallback (set OPENAI_API_KEY for live)'}")
        print("="*65)

        for q in demo_questions:
            print(f"\n  🎓 Student: {q}")
            print(f"\n  🤖 PythonBot: {self.get_response(q)}")
            print("\n  " + "-"*60)

        print("\n  ✅  Chatbot Demo Complete\n")


if __name__ == "__main__":
    bot = PythonTrainingBot()
    bot.run_demo()
