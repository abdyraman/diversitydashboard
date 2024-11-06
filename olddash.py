#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/abdyraman/hr-deep-learning/blob/main/deep_hr.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[61]:


import streamlit as st
import pandas as pd
import numpy as np
import hvplot.pandas  # Import hvplot for DataFrame plotting
import holoviews as hv
import panel as pn
pn.extension("tabulator","echarts", "plotly", "vega", "vizzu")



# In[48]:


df_full = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')


# **Data cleaning**

# In[49]:


# remove 4 columns
df = df_full.drop(['Over18', 'EmployeeNumber','EmployeeCount','StandardHours'],axis=1)


# In[50]:


idf=df.interactive()


# **Descriptive statistics**

# In[51]:


# Widget for gender selection as a ToggleGroup
gender_source = pn.widgets.ToggleGroup(
    name='Gender', 
    options=['Female', 'Male'], 
    button_type='success',
    behavior='radio'  # This makes it behave like a radio button group
)
gender_source


# Years at company

# In[52]:


# Define the pipeline
def create_pipeline(selected_gender):
    return (
        df[df['Gender'] == selected_gender]
        .groupby(['YearsAtCompany'])['MonthlyIncome']
        .mean()
        .round(0) 
        .reset_index()
    )

# Function to create the plot based on the selected gender
def averagelinearplot_gender_age(selected_gender):
    # Create the pipeline based on selected gender
    average_data = create_pipeline(selected_gender)
    
    # Define colors for each gender
    color_map = {
        'Female': 'blue',  # Color for Female
        'Male': 'orange'   # Color for Male
    }

    # Plot the average values by YearsAtCompany, only for the selected Gender
    fig = average_data.hvplot.line(
        x="YearsAtCompany",                # Use YearsAtCompany as the x-axis
        y='MonthlyIncome',                 # Always plot MonthlyIncome
        line_color=color_map[selected_gender],  # Set color based on selected gender
        line_width=5,                       # Line width
        title=f"Average Monthly Income by Years at Company ({selected_gender})",
        ylabel="Average Monthly Income",
        xlabel="Years at Company",
        ylim=(0, average_data['MonthlyIncome'].max() + 10)  # Set y-axis limit based on max of selected variable
    )

    return fig

# Create a Panel layout to include the plot
averages_yearsatcompany_gender_linear_plot = pn.bind(averagelinearplot_gender_age, selected_gender=gender_source)


# Employee Age

# In[53]:


# Define the pipeline for Age
def create_age_pipeline(selected_gender):
    return (
        df[df['Gender'] == selected_gender]
        .groupby(['Age'])['MonthlyIncome']
        .mean()
        .round(0) 
        .reset_index()
    )

# Function to create the plot based on Age
def plot_average_income_by_age(selected_gender):
    average_data = create_age_pipeline(selected_gender)
    
    color_map = {
        'Female': 'blue',
        'Male': 'orange'
    }

    fig = average_data.hvplot.line(
        x="Age",
        y='MonthlyIncome',
        line_color=color_map[selected_gender],
        line_width=5,
        title=f"Average Monthly Income by Employee Age ({selected_gender})",
        ylabel="Average Monthly Income",
        xlabel="Employee Age",
        ylim=(0, average_data['MonthlyIncome'].max() + 10)
    )

    return fig

# Create a Panel layout to include both plots
averages_age_gender_linear_plot = pn.Row(
    pn.bind(plot_average_income_by_age, selected_gender=gender_source)
)


# Attrition

# In[54]:


# Define the pipeline for calculating averages based on selected gender
def create_attrition_pipeline(selected_gender):
    return (
        df[df['Gender'] == selected_gender]
        .groupby(['Attrition'])['MonthlyIncome']  # Only use MonthlyIncome for calculation
        .mean()
        .reset_index()
        .round(0)  # Round the mean to the nearest whole number
    )

# Function to create the plot based on the selected gender
def update_averages_plot(selected_gender):
    average_data = create_attrition_pipeline(selected_gender)  # Create the pipeline

    # Define the color based on the selected gender
    color_map = {
        'Female': 'blue',
        'Male': 'orange'
    }
    color = color_map[selected_gender]  # Get the color for the selected gender

    # Create a bar plot for MonthlyIncome grouped by Attrition
    fig = average_data.hvplot.bar(
        x='Attrition',          # Use Attrition status as the x-axis
        y='MonthlyIncome',      # Fixed to MonthlyIncome
        title=f'Average Monthly Income by Gender and Attrition ({selected_gender})',
        ylabel='Average Monthly Income',
        xlabel='Attrition',
        ylim=(0, average_data['MonthlyIncome'].max() + 10),  # Set y-axis limit based on max of selected variable
        color=color,           # Set color based on selected gender
        legend='top_left'      # Position of the legend
    )

    # Add data labels on top of the bars, positioned closer to the edge
    for i, row in average_data.iterrows():
        fig = fig * hv.Text(x=row['Attrition'], y=row['MonthlyIncome'] + 2, text=str(int(row['MonthlyIncome'])), halign='center', valign='bottom')

    return fig

# Create a Panel layout to include the plot and the gender widget
averages_plot_panel = pn.bind(update_averages_plot, selected_gender=gender_source)


# Department

# In[55]:


# Define the pipeline for calculating averages based on selected gender
def create_department_pipeline(selected_gender):
    return (
        df[df['Gender'] == selected_gender]
        .groupby(['Department'])['MonthlyIncome']  # Change to Department for calculation
        .mean()
        .reset_index()
        .round(0)  # Round the mean to the nearest whole number
    )

# Function to create the plot based on the selected gender
def update_averages_plot(selected_gender):
    average_data = create_department_pipeline(selected_gender)  # Create the pipeline

    # Define the color based on the selected gender
    color_map = {
        'Female': 'blue',
        'Male': 'orange'
    }
    color = color_map[selected_gender]  # Get the color for the selected gender

    # Create a bar plot for MonthlyIncome grouped by Department
    fig = average_data.hvplot.bar(
        x='Department',         # Use Department as the x-axis
        y='MonthlyIncome',      # Fixed to MonthlyIncome
        title=f'Average Monthly Income by Gender and Department ({selected_gender})',
        ylabel='Average Monthly Income',
        xlabel='Department',
        ylim=(0, average_data['MonthlyIncome'].max() + 10),  # Set y-axis limit based on max of selected variable
        color=color,            # Set color based on selected gender
        legend='top_left'       # Position of the legend
    )

    # Add data labels on top of the bars, positioned closer to the edge
    for i, row in average_data.iterrows():
        fig = fig * hv.Text(x=row['Department'], y=row['MonthlyIncome'] + 2, text=str(int(row['MonthlyIncome'])), halign='center', valign='bottom')

    return fig

# Create a Panel layout to include the plot and the gender widget
averages_department_plot_panel = pn.bind(update_averages_plot, selected_gender=gender_source)


# Dashboard

# In[56]:


# Text label above the gender selection widget
gender_selection_text = pn.pane.Markdown("### Click on the button below to display the data for either Females or Males")

# Define the top row layout with two plots
top_row_layout = pn.Row(
    averages_yearsatcompany_gender_linear_plot,  # First plot
    averages_plot_panel                          # Second plot
)

# Define the bottom row layout with two additional plots
down_row_layout = pn.Row(
    averages_age_gender_linear_plot,             # Third plot
    averages_department_plot_panel               # Fourth plot
)

# Additional sidebar information
logo = 'accelerateinclusion.png'
sidebar_text = """
Inclusion Accelerator analyzed a publicly available IBM HR Analytics dataset, published on Kaggle, which includes data from nearly 1,500 current and former employees. This dataset offers insights into job satisfaction, work-life balance, tenure, experience, salary, and demographic details.
"""

# Create a Panel layout for the sidebar with the text and the widget
sidebar_layout = pn.Column(sidebar_text, gender_selection_text, gender_source)

# Creating the dashboard template with a specified sidebar width
dashboard_template = pn.template.FastListTemplate(
    title="Interactive Dashboard",
    logo=logo,
    sidebar=sidebar_layout,  # Add the widget to the sidebar
    sidebar_width=250,       # Set the sidebar width to 250 pixels
    main=[top_row_layout, down_row_layout],  # Combine the rows in the main area
)

# Display the dashboard
dashboard_template.show()


# In[ ]:




