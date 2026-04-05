\---

title: Mistake Analyzer

emoji: 🤖

colorFrom: blue

colorTo: green

sdk: docker

app\_file: server/app.py

pinned: false

\---



\# AI Mistake Analyzer



This project analyzes student mistake patterns and provides learning insights.



\## Features



\- Detects mistake patterns (formula, calculation, logic)

\- Predicts future errors

\- Assigns reward scores (0–1)

\- OpenEnv-style API with /step, /reset, /state



\## How it works



Send input like:



```json

{

&#x20; "answers": \["formula", "formula", "calculation"]

}

