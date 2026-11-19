# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Project 2: Student Academic Performance Analytics

---

### **Document Control**
- **Project Title:** Student Academic Performance Analytics
- **Document Version:** 1.0.0
- **Industry Sector:** Education / EdTech
- **Target Audience:** Academic Administrators, Faculty Advisors, Institutional Quality Cells
- **Academic Context:** Five-Day Engineering Student Training | First Year – First Semester
- **Author:** First-Year Engineering Student (Data Analytics Track)
- **Status:** Approved / Completed
- **Tools & Tech Stack:** Python 3.13, NumPy 2.3, Pandas 2.3, Jupyter Notebook

---

## 1. Introduction & Problem Statement

### 1.1 Problem Statement
Higher education institutions face significant challenges in tracking undergraduate academic progress in real-time. Often, students facing foundational difficulties in core technical subjects (such as programming, mathematics, and database systems) remain undetected until end-semester summative exams, when corrective remediation is too late. Furthermore, student learning outcomes are heavily influenced by multidimensional factors, including class attendance consistency, weekly independent study habits, and home internet accessibility.

Without a systematic, automated analytical framework, academic institutions struggle with:
1. Uncleaned administrative records with missing attendance, duplicate identification keys, and clerical score recording errors.
2. An inability to flag vulnerable, at-risk students who fall below institutional passing thresholds early in the semester.
3. Lack of empirical evidence to assess how attendance shortage and digital divide barriers correlate with student test marks.
4. Absence of data-backed intervention policies to allocate faculty tutoring and campus infrastructure effectively.

This project addresses these challenges by developing an end-to-end exploratory and descriptive data analytics solution using Python, NumPy, and Pandas.

### 1.2 Objectives
The primary objectives of this project are:
- **Data Ingestion & Hygiene Auditing:** Load raw tabular academic records, inspect data types and dimensions, and detect anomalies.
- **Data Cleaning & Imputation:** Systematically resolve duplicate records, impute missing attendance values using a statistically justified department-wise median strategy, and enforce boundary constraints ($[0, 100]$) on assessment marks.
- **Feature Engineering & Academic Categorization:** Compute total marks, average marks, standard letter grades using `pd.cut()`, and attendance policy compliance tiers.
- **Departmental & Demographic Benchmarking:** Aggregate academic performance across engineering departments and quantify the performance gap associated with home internet accessibility.
- **Statistical Dispersion & Outlier Modeling:** Leverage NumPy numerical functions to compute central tendencies, standard deviation, quartiles, and Tukey's Interquartile Range (IQR) to detect statistical score outliers.
- **Evidence-Based Academic Recommendations:** Synthesize five concrete, data-backed operational recommendations for academic mentors and leadership.

### 1.3 Scope of the Project
- **In-Scope:**
  - Processing tabular academic records from `02_student_performance.csv` containing student IDs, names, academic departments, attendance percentages, weekly self-study hours, internet access indicators, and assessment marks across three courses (`Python_Marks`, `Math_Marks`, `DBMS_Marks`).
  - Implementation of descriptive statistics, data transformation, conditional filtering, and group-wise aggregations in Python, NumPy, and Pandas.
  - Output generation in the form of clean summary tables, an executed Jupyter Notebook (`src/analysis.ipynb`), a standalone Python script (`src/analysis.py`), and a cleaned CSV artifact.
- **Out-of-Scope:**
  - Predictive Machine Learning modeling (e.g., classification trees or linear regression) or neural networks.
  - Clinical, psychological, or non-academic behavioral diagnostics.
  - Direct causal determinations (correlation will not be claimed as causation).
  - Real-time cloud database streaming or live LMS web application hosting.

---

## 2. Dataset Description

The dataset `02_student_performance.csv` simulates a realistic first-year engineering student cohort. The schema consists of 9 core attributes:

| Column Name | Data Type | Description | Expected Range / Domain |
| :--- | :--- | :--- | :--- |
| `Student_ID` | String (`object`) | Unique student identifier | Format: `STU1001`, `STU1002`, ... |
| `Name` | String (`object`) | Full name of the student | Alphabetic text |
| `Department` | Categorical (`object`) | Engineering academic branch | CS, IT, Data Science, Electronics, Mechanical |
| `Attendance` | Float (`float64`) | Classroom attendance percentage | $0.0\% - 100.0\%$ (contains missing values) |
| `Study_Hours` | Float (`float64`) | Weekly independent study hours | $0.0 - 40.0$ hours |
| `Internet_Access` | Categorical (`object`) | Home broadband / internet availability | `'Yes'` or `'No'` |
| `Python_Marks` | Float (`float64`) | Score in Python Programming assessment | $0.0 - 100.0$ |
| `Math_Marks` | Float (`float64`) | Score in Applied Mathematics assessment | $0.0 - 100.0$ |
| `DBMS_Marks` | Float (`float64`) | Score in Database Management Systems | $0.0 - 100.0$ |

---

## 3. Functional Requirements (FR)

The system fulfills 15 primary functional requirements corresponding directly to the project tasks:

### FR-01: Dataset Ingestion & Structural Inspection
- The system shall load the raw CSV dataset into a Pandas DataFrame.
- The system shall output dataset dimensions (row count, column count), column headers, and data type mapping (`dtypes`).
- The system shall display the first 5 records (`head()`) and statistical overview (`describe()`).

### FR-02: Missing Value and Duplicate Auditing
- The system shall compute and report the count of missing (`NaN`) values per attribute.
- The system shall inspect the primary key `Student_ID` for duplicate entries, display duplicate rows, and remove duplicate entries while retaining the first occurrence.

### FR-03: Attendance Imputation with Statistical Justification
- The system shall impute missing values in the `Attendance` column using Department-wise Median Imputation.
- *Justification:* Median is robust to skewness and extreme outliers (e.g. prolonged medical absence), while department grouping accounts for differing departmental attendance norms.

### FR-04: Assessment Score Range Validation
- The system shall scan all score columns (`Python_Marks`, `Math_Marks`, `DBMS_Marks`) for values outside the legitimate educational range of $0.0$ to $100.0$.
- The system shall report detected erroneous records and rectify them via numeric clipping (`clip(lower=0.0, upper=100.0)`).

### FR-05: Total and Average Marks Computation
- The system shall calculate `Total_Marks` by summing `Python_Marks`, `Math_Marks`, and `DBMS_Marks`.
- The system shall compute `Average_Marks` as $\text{Total\_Marks} / 3$ rounded to two decimal places.

### FR-06: Categorical Grade Allocation
- The system shall assign an academic letter grade using `pd.cut()` based on the following rubric:
  - **A (Outstanding):** $[85, 100]$
  - **B (Good):** $[70, 85)$
  - **C (Satisfactory):** $[55, 70)$
  - **D (Pass):** $[40, 55)$
  - **F (Fail):** $[0, 40)$

### FR-07: Department-Wise Performance Aggregation
- The system shall group data by `Department` using `groupby().agg()` to compute:
  - Total student enrollment count.
  - Mean overall average marks.
  - Mean subject scores (Python, Mathematics, DBMS).
  - Mean attendance percentage.
- The output shall be sorted in descending order of average marks.

### FR-08: Academic Merit Identification (Top 10 Students)
- The system shall rank and display the top 10 students sorted by `Average_Marks` descending, along with department, attendance, study hours, and assigned grade.

### FR-09: At-Risk Cohort Identification (< 40% Marks)
- The system shall filter and isolate all students scoring an `Average_Marks` below the $40.0\%$ passing mark.
- The system shall report the total count, percentage of total student cohort, and detailed individual student records.

### FR-10: Attendance Band Comparative Analysis
- The system shall segment students into four institutional attendance tiers via `pd.cut()`:
  - Critical Shortage: $<60\%$
  - Attendance Shortage: $60\% - 75\%$
  - Satisfactory Attendance: $75\% - 85\%$
  - High Attendance: $85\% - 100\%$
- The system shall compute student counts, mean, median, min, and max marks for each tier.

### FR-11: Study Habit Correlation & Banded Analytics
- The system shall compute the Pearson correlation coefficient between weekly `Study_Hours` and `Average_Marks`.
- The system shall group study hours into tiers (`<10 hrs`, `10-20 hrs`, `>20 hrs`) to evaluate performance progressions.
- The system shall explicitly document that correlation indicates association, not causation.

### FR-12: Digital Equity & Internet Accessibility Comparison
- The system shall group students by `Internet_Access` (`Yes` vs. `No`) to calculate comparative mean and median scores across all subjects and overall average marks.
- The system shall quantify the net performance gap between connected and non-connected students.

### FR-13: NumPy Numerical Dispersion Metrics for Python_Marks
- The system shall extract `Python_Marks` into a 1D NumPy array.
- The system shall compute statistical metrics using NumPy functions: Mean (`np.mean`), Median (`np.median`), Standard Deviation (`np.std`), Variance (`np.var`), and Quartiles Q1 (25th), Q2 (50th), and Q3 (75th) (`np.percentile`).

### FR-14: Tukey's IQR Anomaly & Outlier Identification
- The system shall calculate the Interquartile Range: $\text{IQR} = Q_3 - Q_1$.
- The system shall establish outlier boundaries:
  - $\text{Lower Fence} = Q_1 - 1.5 \times \text{IQR}$
  - $\text{Upper Fence} = Q_3 + 1.5 \times \text{IQR}$
- The system shall filter and display all student records whose `Python_Marks` fall outside these bounds.

### FR-15: Evidence-Based Institutional Recommendations
- The system shall formulate five actionable, data-backed recommendations for academic support derived strictly from the empirical analysis results.

---

## 4. Non-Functional Requirements (NFR)

1. **Accuracy & Numerical Integrity:** All statistical calculations, quartiles, and correlations must be computed dynamically using NumPy and Pandas functions without hard-coded estimates.
2. **Code Simplicity & Readability:** Code must be structured according to first-year engineering standards, utilizing clear variable naming conventions, modular blocks, and comprehensive explanatory comments.
3. **Reproducibility:** Analysis must yield identical results across multiple executions when evaluated on the benchmark dataset.
4. **Execution Performance:** The full end-to-end analytical pipeline must execute within under 5 seconds on standard commodity hardware.
5. **Cross-Platform Portability:** Code must execute seamlessly on Windows, macOS, and Linux without platform-dependent path errors.

---

## 5. Tools, Technologies & Dependencies

| Tool / Technology | Version | Purpose in Project |
| :--- | :--- | :--- |
| **Python** | 3.13+ | Core programming environment |
| **NumPy** | 2.3+ | Numerical arrays, percentiles, quartiles, variance, IQR fences |
| **Pandas** | 2.3+ | Tabular data manipulation, cleaning, imputation, grouping, binning |
| **Jupyter Notebook** | Latest | Interactive development, formatted table rendering, documentation |
| **Visual Studio Code** | Latest | Code editing, script execution, Git version control |
| **Git / GitHub** | Latest | Version control, codebase hosting, reproducibility |

---

## 6. Analytical Methodology & Workflow

The project follows a standard 7-stage Data Analytics Lifecycle:

```
+-------------------------------------------------------------+
| 1. DATA INGESTION                                           |
|    Load 02_student_performance.csv via Pandas read_csv()    |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 2. AUDITING & ANOMALY DETECTION                             |
|    Check shape, types, missing values, duplicates, [0,100]  |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 3. DATA CLEANING & IMPUTATION                               |
|    - Drop duplicate Student_IDs                             |
|    - Impute Attendance using Department-Wise Median         |
|    - Clip out-of-bounds scores to [0.0, 100.0]              |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 4. FEATURE ENGINEERING                                      |
|    - Total_Marks = Sum(Python, Math, DBMS)                  |
|    - Average_Marks = Total_Marks / 3                        |
|    - Grade = pd.cut(Average_Marks, bins=[0,40,55,70,85,100])|
|    - Attendance_Band = pd.cut(Attendance, policy tiers)     |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 5. COMPARATIVE & GROUPED ANALYTICS                          |
|    - Department-wise averages via groupby().agg()           |
|    - Top 10 rankers and At-risk cohort (<40%)               |
|    - Attendance and study hours correlation (r = 0.62)      |
|    - Digital equity evaluation (Internet Yes vs. No)        |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 6. NUMPY STATISTICAL DISPERSION & IQR OUTLIERS              |
|    - Median, Standard Deviation, Quartiles (Q1, Q2, Q3)     |
|    - IQR = Q3 - Q1; Lower/Upper Outlier Fences              |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| 7. RECOMMENDATION SYNTHESIS                                 |
|    Formulate 5 actionable, empirical academic interventions |
+-------------------------------------------------------------+
```

---

## 7. Expected Deliverables & Outcomes

1. **Cleaned Dataset:** `data/02_student_performance_cleaned.csv` containing fully audited, deduplicated, and feature-engineered records.
2. **Interactive Jupyter Notebook:** `src/analysis.ipynb` with Markdown narrative, code cells, and executed output tables.
3. **Executable Python Script:** `src/analysis.py` for terminal execution and verification.
4. **SRS Specification:** `SRS/project_SRS.pdf` and `SRS/project_SRS.md` fulfilling academic submission criteria.
5. **Documentation & Repository:** `README.md` containing reproduction instructions, rubric mapping, and project summary.
6. **Academic Intervention Plan:** 5 data-supported recommendations ready for institutional review.

---
*End of Software Requirements Specification Document.*
