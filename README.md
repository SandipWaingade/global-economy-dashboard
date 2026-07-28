# 🌍 Global Economy Analysis — Data Visualization Final Project

**Course:** Data Visualization · Summer 2026  
**Dataset:** World Development Indicators — 50 Countries · 2000–2023  
**Tools:** Python · Pandas · Plotly · Streamlit  

---

## 📁 Project Structure

```
food_project/
├── global_economy.csv              # Dataset — 50 countries × 24 years × 15 indicators
├── global_economy_analysis.ipynb   # Jupyter notebook — EDA + 10 analytical questions
├── app.py                          # Streamlit dashboard
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔍 10 Analytical Questions

| # | Question |
|---|---|
| Q1 | How has GDP per capita grown across income groups from 2000 to 2023? |
| Q2 | Which regions show the biggest gap between GDP and life expectancy? |
| Q3 | Is there a relationship between inflation and GDP growth by continent? |
| Q4 | Which countries are most export-dependent and how did this change post-2008? |
| Q5 | Do countries investing more in education show stronger GDP growth 10 years later? |
| Q6 | How does unemployment vary by region and who recovered fastest? |
| Q7 | Which countries decoupled economic growth from CO2 emissions? |
| Q8 | How does health expenditure correlate with life expectancy? |
| Q9 | Is internet penetration linked to GDP growth in developing nations? |
| Q10 | Which economies were hit hardest by COVID-19 and who recovered fastest? |

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Jupyter Notebook
```bash
jupyter notebook global_economy_analysis.ipynb
```

### 3. Run Streamlit Dashboard
```bash
streamlit run app.py
```

---

## 📊 Dashboard Features
- Filter by Region, Income Group, Year Range, Country
- 4 tabs: Growth & Inequality · Trade & Environment · Health & Education · World Map
- Animated charts · Choropleth map · Interactive filters
- CVD-safe colour palette throughout

---

## 🌐 Deploy to Streamlit Community Cloud
1. Push this folder to a **public GitHub repository**
2. Go to **share.streamlit.io**
3. Connect your GitHub repo
4. Set main file as `app.py`
5. Click **Deploy** — live URL generated automatically

---

**Deadline: Friday 31 July 2026**
