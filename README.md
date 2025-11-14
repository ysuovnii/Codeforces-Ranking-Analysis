# Codeforces-Ranking-Analysis

This Python tool analyzes **Codeforces contest standings** and finds:

- Users with **lower rating than you** but placed **above** you
- Users with **lower rating than you** placed **below** you  
- Users with **higher rating than you** but placed **below** you  
- Users with **higher rating than you** placed **above** you  

Useful for analyzing performance and identifying "rating anomalies" in contests.

---

## Features

- Fetches contest data using the **Codeforces API**
- Filters participants based on:
  - Rating < yours AND rank above you  
  - Rating > yours AND rank below you  
- Saves filtered data into JSON files

---

## Installation

```bash
git clone https://github.com/<your-username>/codeforces-rating-analysis.git
cd codeforces-rating-analysis

pip install -r requirements.txt
