# 🔍 2-SAT Satisfiability Solver

> **Computer Science Project** | Python | Formal Logic | Compiler Design

---

## 📌 Overview

A Python program that parses two Boolean formulas in **Conjunctive Normal Form (CNF)** and determines whether they are satisfiable. If satisfiable, the program also outputs a valid **satisfying assignment** of truth values.

This project demonstrates applied knowledge of formal logic, parsing theory, and constraint satisfaction — core areas of theoretical computer science.

---

## ⚙️ How It Works

1. **Parsing** — Input CNF formulas are lexed and parsed using **PLY (lex & yacc)**, a Python implementation of classic compiler-construction tools
2. **Satisfiability Check** — The **Resolution Method** is applied to determine if the formula can be satisfied
3. **Assignment Output** — If satisfiable, a concrete variable assignment that satisfies the formula is returned

---

## 🗂️ Project Structure

```
2SAT/
├── boolean.py          # Core logic: CNF parsing, resolution algorithm, assignment generation
├── boolean-test.py     # Test cases validating satisfiability outcomes
├── parsetab.py         # Auto-generated PLY parser table
└── parser.out          # PLY parser diagnostic output
```

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| Language | Python 3.x |
| Lexer | PLY (lex) |
| Parser | PLY (yacc) |
| Logic Method | Resolution Method |

---

## 🚀 Getting Started

```bash
pip install ply
python boolean.py
```

Run the test suite:
```bash
python boolean-test.py
```

---

## 💡 Key Concepts Demonstrated

- **Lexical analysis & parsing** using lex/yacc — the same principles underlying real compilers
- **Propositional logic** and CNF representation
- **Resolution-based theorem proving** — a foundational AI and logic technique
- **Constraint satisfaction** problem solving

---

## 👤 Author

**Steve George Parakal** | [GitHub](https://github.com/steveparakal)
