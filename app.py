
import streamlit as st
import pandas as pd
from io import BytesIO

from analysis.analysis import (
    load_data,
    subject_analysis,
    department_analysis,
    student_ranking,
    attendance_analysis,
    data_quality,
    subject_chart,
    department_chart,
    ranking_chart,
    attendance_chart,
    heatmap_chart,
    correlation_chart
)

# ==================================================
# EXCEL REPORT GENERATOR
# ==================================================

def convert_to_excel(dataframe):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Student Report"
        )

    return output.getvalue()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Student Analytics Portal",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# CUSTOM STYLING
# ==================================================

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

h1 {
    color: #183153;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD DATASET
# ==================================================

df = load_data()


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.title("📊 Analytics Portal")
st.sidebar.caption("Student Performance Monitoring")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Student Performance",
        "Department Analytics",
        "Attendance Monitoring",
        "Data Quality"
    ]
)

st.sidebar.divider()


# ==================================================
# DEPARTMENT FILTER
# ==================================================

departments = ["All Departments"] + sorted(
    df["Department"].unique().tolist()
)

selected_department = st.sidebar.selectbox(
    "Select Department",
    departments
)

filtered_df = df.copy()

if selected_department != "All Departments":

    filtered_df = filtered_df[
        filtered_df["Department"] == selected_department
    ]


# ==================================================
# DASHBOARD HEADING
# ==================================================

st.title("Student Performance Analytics")

st.caption(
    "Academic Data Analysis and Visualization Portal"
)


if filtered_df.empty:

    st.warning("No records available.")

else:

    # ==============================================
    # 1. OVERVIEW PAGE
    # ==============================================

    if page == "Overview":

        st.subheader("Dashboard Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Students",
            len(filtered_df)
        )

        col2.metric(
            "Average Marks",
            f"{filtered_df['Average'].mean():.2f}"
        )

        col3.metric(
            "Average Attendance",
            f"{filtered_df['Attendance'].mean():.2f}%"
        )

        top_student = filtered_df.loc[
            filtered_df["Average"].idxmax(),
            "Name"
        ]

        col4.metric(
            "Top Performer",
            top_student
        )

        st.divider()

        # Subject Performance

        st.subheader("Subject Performance")

        st.pyplot(
            subject_chart(filtered_df)
        )

        # Student Ranking

        st.subheader("Student Performance Ranking")

        st.pyplot(
            ranking_chart(filtered_df)
        )

        # Student Records

        st.subheader("Student Records")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        # Download Reports

        st.divider()

        st.subheader("Download Student Reports")

        col1, col2 = st.columns(2)

        # CSV Download

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        col1.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="student_performance_report.csv",
            mime="text/csv"
        )

        # Excel Download

        excel_data = convert_to_excel(filtered_df)

        col2.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name="student_performance_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


    # ==============================================
    # 2. STUDENT PERFORMANCE PAGE
    # ==============================================

    elif page == "Student Performance":

        st.subheader("Student Performance Analysis")

        search = st.text_input(
            "Search Student by Name"
        )

        student_data = filtered_df.copy()

        if search:

            student_data = student_data[
                student_data["Name"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        st.subheader("Student Records")

        st.dataframe(
            student_data,
            use_container_width=True,
            hide_index=True
        )

        if not student_data.empty:

            # Individual Student Profile

            st.divider()

            st.subheader("Individual Student Profile")

            selected_student = st.selectbox(
                "Select Student",
                student_data["Name"].tolist()
            )

            student = student_data[
                student_data["Name"] == selected_student
            ].iloc[0]

            st.markdown(
                f"### 👨‍🎓 {student['Name']}"
            )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Student ID",
                int(student["Student_ID"])
            )

            col2.metric(
                "Department",
                student["Department"]
            )

            col3.metric(
                "Total Marks",
                int(student["Total"])
            )

            col4.metric(
                "Average Marks",
                f"{student['Average']:.2f}"
            )

            # Subject-wise Marks

            st.subheader("Subject-wise Marks")

            marks = pd.DataFrame({
                "Subject": [
                    "Python",
                    "Java",
                    "Mathematics"
                ],
                "Marks": [
                    student["Python"],
                    student["Java"],
                    student["Mathematics"]
                ]
            })

            st.bar_chart(
                marks.set_index("Subject")
            )

            # Attendance Details

            st.subheader("Attendance Details")

            st.progress(
                float(student["Attendance"]) / 100
            )

            st.write(
                f"Attendance: {student['Attendance']}%"
            )

            # Complete Academic Details

            st.subheader("Complete Academic Details")

            st.dataframe(
                student.to_frame("Details"),
                use_container_width=True
            )

            # Student Ranking

            st.divider()

            st.subheader("Student Ranking")

            st.dataframe(
                student_ranking(student_data)[
                    [
                        "Name",
                        "Department",
                        "Total",
                        "Average"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            st.pyplot(
                ranking_chart(student_data)
            )

            # Subject Performance Heatmap

            st.subheader("Subject Performance Heatmap")

            st.pyplot(
                heatmap_chart(student_data)
            )

            # Download Student Report

            st.divider()

            st.subheader("Download Student Report")

            col1, col2 = st.columns(2)

            csv_data = student_data.to_csv(
                index=False
            ).encode("utf-8")

            col1.download_button(
                "📥 Download CSV",
                data=csv_data,
                file_name="student_performance_report.csv",
                mime="text/csv"
            )

            excel_data = convert_to_excel(student_data)

            col2.download_button(
                "📊 Download Excel",
                data=excel_data,
                file_name="student_performance_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:

            st.info("No matching student found.")


    # ==============================================
    # 3. DEPARTMENT ANALYTICS PAGE
    # ==============================================

    elif page == "Department Analytics":

        st.subheader("Department-wise Analysis")

        st.dataframe(
            department_analysis(filtered_df),
            use_container_width=True
        )

        st.pyplot(
            department_chart(filtered_df)
        )

        st.subheader("Subject-wise Average")

        st.dataframe(
            subject_analysis(filtered_df).rename(
                "Average Marks"
            ),
            use_container_width=True
        )

        st.pyplot(
            subject_chart(filtered_df)
        )

        st.subheader("Correlation Analysis")

        st.pyplot(
            correlation_chart(filtered_df)
        )


    # ==============================================
    # 4. ATTENDANCE MONITORING PAGE
    # ==============================================

    elif page == "Attendance Monitoring":

        st.subheader("Attendance Monitoring")

        st.metric(
            "Average Attendance",
            f"{filtered_df['Attendance'].mean():.2f}%"
        )

        st.pyplot(
            attendance_chart(filtered_df)
        )

        st.subheader("Low Attendance Students")

        limit = st.slider(
            "Attendance Threshold (%)",
            min_value=50,
            max_value=100,
            value=75
        )

        low_students = attendance_analysis(
            filtered_df,
            limit
        )

        st.dataframe(
            low_students[
                [
                    "Name",
                    "Department",
                    "Attendance"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


    # ==============================================
    # 5. DATA QUALITY PAGE
    # ==============================================

    elif page == "Data Quality":

        st.subheader("Dataset Quality Report")

        quality = data_quality(filtered_df)

        quality_df = pd.DataFrame(
            list(quality.items()),
            columns=[
                "Quality Check",
                "Count"
            ]
        )

        st.dataframe(
            quality_df,
            use_container_width=True,
            hide_index=True
        )

        if all(value == 0 for value in quality.values()):

            st.success(
                "All basic data quality checks passed."
            )

        else:

            st.warning(
                "Some data quality issues were detected."
            )

        st.subheader("Dataset Preview")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# FOOTER
# ==================================================

st.sidebar.divider()

st.sidebar.caption(
    "Student Analytics Project | Python"
)
