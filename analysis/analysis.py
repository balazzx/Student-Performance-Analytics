
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Dataset location
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "dataset"
    / "students.csv"
)


# 1. Load dataset
def load_data():
    df = pd.read_csv(DATA_PATH)

    # Calculate total and average marks
    subjects = ["Python", "Java", "Mathematics"]

    df["Total"] = df[subjects].sum(axis=1)
    df["Average"] = df[subjects].mean(axis=1)

    return df


# 2. Subject-wise analysis
def subject_analysis(df):
    return df[
        ["Python", "Java", "Mathematics"]
    ].mean()


# 3. Department-wise analysis
def department_analysis(df):
    subjects = ["Python", "Java", "Mathematics"]

    result = df.groupby("Department")[subjects].mean()

    result["Overall_Average"] = result.mean(axis=1)

    return result


# 4. Student ranking
def student_ranking(df):
    return df.sort_values(
        by="Average",
        ascending=False
    )


# 5. Attendance analysis
def attendance_analysis(df, limit=75):
    return df[df["Attendance"] < limit]


# 6. Data quality analysis
def data_quality(df):
    return {
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Records": int(df.duplicated().sum()),
        "Invalid Marks": int(
            ((df[["Python", "Java", "Mathematics"]] < 0) |
             (df[["Python", "Java", "Mathematics"]] > 100))
            .any(axis=1).sum()
        ),
        "Invalid Attendance": int(
            ((df["Attendance"] < 0) |
             (df["Attendance"] > 100)).sum()
        )
    }


# 7. Subject-wise bar chart
def subject_chart(df):
    averages = subject_analysis(df)

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        x=averages.index,
        y=averages.values,
        ax=ax
    )

    ax.set_title("Subject-wise Average Performance")
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)

    fig.tight_layout()
    return fig


# 8. Department-wise bar chart
def department_chart(df):
    averages = department_analysis(df)

    fig, ax = plt.subplots(figsize=(7, 4))

    sns.barplot(
        x=averages.index,
        y=averages["Overall_Average"],
        ax=ax
    )

    ax.set_title("Department-wise Performance")
    ax.set_xlabel("Department")
    ax.set_ylabel("Average Marks")
    ax.set_ylim(0, 100)

    fig.tight_layout()
    return fig


# 9. Student ranking chart
def ranking_chart(df):
    ranking = student_ranking(df)

    fig, ax = plt.subplots(figsize=(9, 5))

    sns.barplot(
        data=ranking,
        x="Name",
        y="Average",
        ax=ax
    )

    ax.set_title("Student Performance Ranking")
    ax.set_xlabel("Students")
    ax.set_ylabel("Average Marks")
    ax.tick_params(axis="x", rotation=45)
    ax.set_ylim(0, 100)

    fig.tight_layout()
    return fig


# 10. Attendance chart
def attendance_chart(df):
    fig, ax = plt.subplots(figsize=(9, 5))

    sns.barplot(
        data=df,
        x="Name",
        y="Attendance",
        ax=ax
    )

    ax.axhline(
        y=75,
        linestyle="--",
        label="75% Attendance Limit"
    )

    ax.set_title("Student Attendance Analysis")
    ax.set_xlabel("Students")
    ax.set_ylabel("Attendance (%)")
    ax.tick_params(axis="x", rotation=45)
    ax.set_ylim(0, 110)
    ax.legend()

    fig.tight_layout()
    return fig


# 11. Student subject heatmap
def heatmap_chart(df):
    subjects = ["Python", "Java", "Mathematics"]

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        df.set_index("Name")[subjects],
        annot=True,
        cmap="YlGnBu",
        ax=ax
    )

    ax.set_title("Student Subject Performance Heatmap")

    fig.tight_layout()
    return fig


# 12. Correlation heatmap
def correlation_chart(df):
    columns = [
        "Python", "Java", "Mathematics",
        "Attendance", "Average"
    ]

    correlation = df[columns].corr()

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )

    ax.set_title("Student Performance Correlation")

    fig.tight_layout()
    return fig
