# Student Performance Data Analytics & Visualization

An interactive web-based dashboard built using Python, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit to analyze and visualize student academic performance.

## Project Overview

The Student Performance Analytics Portal helps analyze student marks, attendance, department performance, and academic records through interactive visualizations and reports.

## Features

- Interactive student analytics dashboard
- Student search and individual profiles
- Subject-wise performance analysis
- Department-wise performance comparison
- Student ranking and performance heatmap
- Attendance monitoring with adjustable thresholds
- Dataset quality checks
- Correlation analysis
- CSV and Excel report downloads
- Department-based filtering

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Project Structure

```text
Student_Performance_Analytics/
├── analysis/
│   ├── __init__.py
│   └── analysis.py
├── dataset/
│   └── students.csv
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Student_Performance_Analytics
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The dashboard will open in your web browser.

## Dashboard Modules

1. Overview
2. Student Performance
3. Department Analytics
4. Attendance Monitoring
5. Data Quality

## Dataset

The project uses a sample student dataset containing student details, department information, subject marks, and attendance percentages.

## Future Enhancements

- Machine learning-based student performance prediction
- Larger real-world academic datasets
- Advanced academic performance reports
- Database integration

## License

This project is available for educational and learning purposes.