# hr-deep-learning 
This code is a comprehensive analysis and machine learning model building process using Python. 
The dataset is loaded using Pandas, and basic information about its structure and missing values is displayed.
No missing values or duplicate rows are found.
Several columns (Over18, EmployeeNumber, EmployeeCount, StandardHours) with constant values or no impact on analysis are removed.

Descriptive Statistics:
Descriptive statistics are provided for numeric columns, giving insights into the distribution and central tendencies of various attributes.
The unique values of categorical columns are explored, including business travel frequency, department, education field, gender, job role, marital status, and overtime. Count plots and pie charts are generated to visualize the distribution of these categorical variables.
Numeric Data Analysis includes descriptive statistics, including mean, standard deviation, and quartiles, are calculated for numeric columns.
Box plots are created to visualize the distribution of numeric features.

Attrition Analysis:
Bar plots are generated to analyze the attrition rates based on various categorical variables such as department, age, marital status, business travel, job role, and overtime. Insights are provided for each analysis, helping to understand factors contributing to attrition.

Salary Analysis:
Bar plots are created to compare median salaries across different departments and attrition statuses.
Insights are provided regarding the median salaries of current and former employees.

Correlation Matrix:
A heatmap is generated to visualize the correlation matrix of numeric variables, highlighting potential collinearity issues.
Machine Learning - Logistic Regression:

The data is prepared for machine learning, with the target variable (Attrition_Binary) encoded as binary.
Logistic regression is applied to predict employee attrition.
Model performance is evaluated using accuracy, confusion matrix, and classification report.
The model shows an accuracy of 87.2%, but a warning about convergence issues is noted.
Resampling for Imbalanced Data:
Imbalanced data is addressed using the RandomOverSampler from imbalanced-learn.
The logistic regression model is then applied to the resampled data, and performance is evaluated.
Conclusion:

The notebook concludes with insights from the analyses and machine learning models, summarizing key findings related to employee attrition.
Overall, the code demonstrates a thorough exploratory data analysis (EDA) and machine learning workflow using popular Python libraries like Pandas, NumPy, Matplotlib, Seaborn, Plotly, Scikit-Learn, and imbalanced-learn.
