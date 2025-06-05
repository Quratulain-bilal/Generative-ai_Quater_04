# 🧠 Why is the User Prompt Passed in `Runner.run()`? And Why is `run()` a Classmethod?

---

## 📍 Question:
**"Why is the user prompt passed in `Runner.run()`? Aur yeh method `classmethod` kyun hota hai?"**

---

## 🧩 1. Why is the **User Prompt** passed in `Runner.run()`?

### 🔍 What is a user prompt?

User prompt woh hota hai jo user input deta hai — yani instruction ya sawaal.  
Agent ka system prompt already fix hota hai (jaise uska role), lekin user prompt har dafa alag hota hai.

### 🧠 Purpose:

Agent ka role to pehle se hota hai (jaise: Travel Agent),  
lekin har baar user us se naya kaam karwana chahta hai:


System Prompt ➝ "Tum aik travel agent ho"
User Prompt ➝ "Mujhe Italy ka 5 din ka tour plan do"



Isliye, user prompt ko har baar **`Runner.run()`** mein pass karte hain, taake agent ko bataya ja sake:

- Kis city ke baare mein kaam karna hai?
- Konsa action lena hai?
- Kis format mein jawab dena hai?

---

### 📌 Benefits of Passing User Prompt:

| Benefit                         | Explanation |
|----------------------------------|-------------|
| 🎯 **Specific Query**             | Agent ko clear task milta hai |
| 🔁 **Dynamic Inputs**             | Har run mein naya input diya ja sakta hai |
| 🧪 **Testing Friendly**           | Alag alag inputs se test asaan hota hai |
| ⚙️ **Controlled Execution**       | Input pe control developer ke paas rehta hai |

---

### 💡 Real-world Analogy:

Jaise ek customer service agent hamesha ready rehta hai lekin  
har baar customer ka alag sawal hota hai.

```text
🧍 Customer      ➝ "Mujhe mobile recharge chahiye"
🤖 Agent System  ➝ Role: Telecom Support Agent
📝 User Prompt   ➝ Task: Recharge request
🧩 2. Why is Runner.run() a classmethod?
🔧 What is a classmethod?
A classmethod Python mein aisi method hoti hai jo object banaye baghair bhi chal sakti hai.

python
Copy code
class MyClass:
    @classmethod
    def greet(cls):
        print("Hello!")
python
Copy code
MyClass.greet()  # ✅ Object banane ki zarurat nahi
⚡ Why use it for Runner.run()?
Agar har baar object banayein to code lambaa aur repetitive ho jata hai.

Lekin classmethod banane se:

👌 Aap directly class se call kar sakte ho

🧼 Code clean aur short ban jata hai

🧰 Method har jagah se utility ki tarah reuse ho sakti hai

📦 Benefits of using classmethod in Runner.run():
Benefit	Explanation
🚀 No Object Needed	Class se direct call ho jata hai
🧹 Clean Syntax	Code readable aur short hota hai
🔁 Reusable Method	Alag alag jagahon pe use kar sakte ho
⚒️ Utility Style Access	Runner ko tool ki tarah use karte hain

🤝 Together: System Prompt + User Prompt + Classmethod


         ┌──────────────┐
         │ Agent (class)│
         └────┬─────────┘
              │
        ┌─────▼────────┐
        │System Prompt │  (Fixed role, e.g., travel planner)
        └─────┬────────┘
              │
        ┌─────▼─────────┐
        │User Prompt     │ (Input at runtime)
        └─────┬──────────┘
              │
        ┌─────▼────────────┐
        │Runner.run(...)    │  ← Classmethod executes prompt
        └──────────────────┘


🧾 Conclusion
Concept	Purpose/Benefit
✅ User Prompt	Agent ko task deta hai
✅ Classmethod	Code ko simple aur object-less banata hai
✅ Combined	Efficient, reusable, scalable AI agent design
