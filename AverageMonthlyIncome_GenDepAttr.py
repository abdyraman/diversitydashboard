import streamlit as st
import pandas as pd
import numpy as np
import hvplot.pandas  # Import hvplot for DataFrame plotting
import holoviews as hv
import panel as pn
import matplotlib.pyplot as plt
pn.extension("tabulator","echarts", "plotly", "vega", "vizzu")


# In[2]:


df_full = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')


# **Data cleaning**

# In[3]:


# remove 4 columns
df = df_full.drop(['Over18', 'EmployeeNumber','EmployeeCount','StandardHours'],axis=1)

idf=df.interactive()

# ## Attrition

# In[11]:


# Widget for attrition selection
attrition_source = pn.widgets.CheckBoxGroup(
    name='Attrition',
    options=['Yes', 'No'],  # Options for attrition
    value=['Yes', 'No']     # Sets both options selected by default
)


# In[12]:


# Widget for attrition selection
department_source = pn.widgets.CheckBoxGroup(
    name='Departments',
    options=['Sales', 'Research & Development', 'Human Resources'],  # Options for attrition
    value=['Sales', 'Research & Development', 'Human Resources']    # Sets both options selected by default
)


# In[13]:


# Pipeline function to filter and group data
def create_attrition_pipeline(selected_attrition, selected_department):
    if isinstance(selected_attrition, str):
        selected_attrition = [selected_attrition]
    if isinstance(selected_department, str):
        selected_department = [selected_department]
    
    # Filter and group by Gender, Attrition, and Department
    return (
        df[
            df['Attrition'].isin(selected_attrition) & 
            df['Department'].isin(selected_department)
        ]
        .groupby(['Gender', 'Attrition', 'Department'])['MonthlyIncome']
        .mean()
        .reset_index()
        .round(0)
    )


# In[14]:


# Update function for displaying values for females
def update_female_plot(selected_attrition, selected_department):
    if not selected_attrition:
        selected_attrition = ['Yes', 'No']
    if not selected_department:
        selected_department = ['Sales', 'Research & Development', 'Human Resources']
    
    average_data = create_attrition_pipeline(selected_attrition, selected_department)

    # Prepare text output for females
    female_data = average_data[average_data['Gender'] == 'Female']
    
    if female_data.empty:
        # If there's no data for females, handle that case
        female_data = pd.DataFrame({
            'Gender': ['Female'] * 2,
            'Attrition': ['Yes', 'No'],
            'MonthlyIncome': [0, 0],
            'Department': ['N/A', 'N/A']  # Adding a placeholder for the Department
        })
    
    # Calculate the mean of the monthly income for females and round it
    female_mean_income = female_data['MonthlyIncome'].mean().round(0)

    # Constructing the output string
    female_output = f"### Average Monthly Income for Females: ${int(female_mean_income)}\n"

    # Filter data for females who left the company (Attrition = 1)
    left_females = female_data[female_data['Attrition'] == 'Yes']
    # Filter data for females who stayed with the company (Attrition = 0)
    stayed_females = female_data[female_data['Attrition'] == 'No']

    # Writing for females who left the company
    if not left_females.empty:
        female_output += "\n**Females Who Left the Company:**\n"
        for _, row in left_females.iterrows():
            female_output += f"- **{row['Department']}**: ${int(row['MonthlyIncome'])}\n"

    # Writing for females who continued working
    if not stayed_females.empty:
        female_output += "\n**Females Who Stayed with the Company:**\n"
        for _, row in stayed_females.iterrows():
            female_output += f"- **{row['Department']}**: ${int(row['MonthlyIncome'])}\n"

    return pn.pane.Markdown(female_output)

# Binding the update functions with the widget values
female_plot_panel = pn.bind(update_female_plot, selected_attrition=attrition_source, selected_department=department_source)


# In[15]:


# Update function for displaying values for females
def update_male_plot(selected_attrition, selected_department):
    if not selected_attrition:
        selected_attrition = ['Yes', 'No']
    if not selected_department:
        selected_department = ['Sales', 'Research & Development', 'Human Resources']
    
    average_data = create_attrition_pipeline(selected_attrition, selected_department)

    # Prepare text output for females
    male_data = average_data[average_data['Gender'] == 'Male']
    
    if male_data.empty:
        # If there's no data for females, handle that case
        male_data = pd.DataFrame({
            'Gender': ['Male'] * 2,
            'Attrition': ['Yes', 'No'],
            'MonthlyIncome': [0, 0],
            'Department': ['N/A', 'N/A']  # Adding a placeholder for the Department
        })
    
    # Calculate the mean of the monthly income for females and round it
    male_mean_income = male_data['MonthlyIncome'].mean().round(0)

    # Constructing the output string
    male_output = f"### Average Monthly Income for Males: ${int(male_mean_income)}\n"

    # Filter data for females who left the company (Attrition = 1)
    left_males = male_data[male_data['Attrition'] == 'Yes']
    # Filter data for females who stayed with the company (Attrition = 0)
    stayed_males = male_data[male_data['Attrition'] == 'No']

    # Writing for females who left the company
    if not left_males.empty:
        male_output += "\n**Males Who Left the Company:**\n"
        for _, row in left_males.iterrows():
            male_output += f"- **{row['Department']}**: ${int(row['MonthlyIncome'])}\n"

    # Writing for females who continued working
    if not stayed_males.empty:
        male_output += "\n**Males Who Stayed with the Company:**\n"
        for _, row in stayed_males.iterrows():
            male_output += f"- **{row['Department']}**: ${int(row['MonthlyIncome'])}\n"

    return pn.pane.Markdown(male_output)

# Binding the update functions with the widget values
male_plot_panel = pn.bind(update_male_plot, selected_attrition=attrition_source, selected_department=department_source)


# In[16]:


# Function to create bar plot for females
def create_female_bar_plot(selected_attrition, selected_department):
    average_data = create_attrition_pipeline(selected_attrition, selected_department)

    # Filter female data
    female_data = average_data[average_data['Gender'] == 'Female']
    
    # Handle empty female data case
    if female_data.empty:
        female_data = pd.DataFrame({
            'Department': ['Sales', 'Research & Development', 'Human Resources'],
            'MonthlyIncome': [0, 0, 0],
            'Attrition': ['Yes', 'No', 'Yes']  # Example attrition for the empty DataFrame
        })

    # Prepare the plot data
    female_grouped = female_data.groupby(['Department', 'Attrition'])['MonthlyIncome'].mean().unstack()

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    female_grouped.plot(kind='bar', ax=ax, color=['blue', 'lightblue'], edgecolor='black')
    
    # Set title and labels
    ax.set_title('Average Monthly Income for Females by Attrition Status')
    ax.set_xlabel('Department')
    ax.set_ylabel('Average Monthly Income ($)')
    ax.set_ylim(0, female_grouped.max().max() * 1.1)
    plt.xticks(rotation=0)
    ax.legend(title='Attrition', loc='upper left')

    return pn.pane.Matplotlib(fig)

# Function to create bar plot for males
def create_male_bar_plot(selected_attrition, selected_department):
    average_data = create_attrition_pipeline(selected_attrition, selected_department)

    # Filter male data
    male_data = average_data[average_data['Gender'] == 'Male']
    
    # Handle empty male data case
    if male_data.empty:
        male_data = pd.DataFrame({
            'Department': ['Sales', 'Research & Development', 'Human Resources'],
            'MonthlyIncome': [0, 0, 0],
            'Attrition': ['Yes', 'No', 'Yes']  # Example attrition for the empty DataFrame
        })

    # Prepare the plot data
    male_grouped = male_data.groupby(['Department', 'Attrition'])['MonthlyIncome'].mean().unstack()

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 4))
    male_grouped.plot(kind='bar', ax=ax, color=['orange', 'lightcoral'], edgecolor='black')

    # Set title and labels
    ax.set_title('Average Monthly Income for Males by Attrition Status')
    ax.set_xlabel('Department')
    ax.set_ylabel('Average Monthly Income ($)')
    ax.set_ylim(0, male_grouped.max().max() * 1.1)
    plt.xticks(rotation=0)
    ax.legend(title='Attrition', loc='upper left')

    return pn.pane.Matplotlib(fig)

# Binding the update functions with the widget values
female_barplot_panel = pn.bind(create_female_bar_plot, selected_attrition=attrition_source, selected_department=department_source)
male_barplot_panel = pn.bind(create_male_bar_plot, selected_attrition=attrition_source, selected_department=department_source)


# Panel 2

# In[20]:


# Text label above the gender selection widget
selection_text_one = pn.pane.Markdown("### Uncheck the box below to display the average monthly income for employees who have left the company.")
selection_text_two = pn.pane.Markdown("### Uncheck the boxes below to filter the departments for which you want to see average income data.")

# Define the layout for the top row and bottom row
top_row_layout = pn.Row(female_plot_panel,female_barplot_panel)
down_row_layout = pn.Row(male_plot_panel,male_barplot_panel)

# Additional sidebar information
logo = 'accelerateinclusion.png'
sidebar_text = """
Employee attrition measures how many workers have left an organization and is a common metric companies use to assess their performance."""

# Create a Panel layout for the sidebar with the text and the widget
sidebar_layout = pn.Column(sidebar_text, selection_text_one, attrition_source,selection_text_two, department_source)

# Create the dashboard template
dashboard_template = pn.template.FastListTemplate(
    title="Dynamic Insights: Average Monthly Income Based on Gender, Department and Attrition",
    logo=logo,
    sidebar=sidebar_layout,
    sidebar_width=250,
    main=[top_row_layout, down_row_layout]
)

# Display the dashboard
dashboard_template.show()