#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/abdyraman/hr-deep-learning/blob/main/deep_hr.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[24]:


import streamlit as st
import pandas as pd
import numpy as np
import hvplot.pandas  # Import hvplot for DataFrame plotting
import holoviews as hv
import panel as pn
pn.extension("tabulator","echarts", "plotly", "vega", "vizzu")


# In[25]:


df_full = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')


# **Data cleaning**

# In[26]:


# remove 4 columns
df = df_full.drop(['Over18', 'EmployeeNumber','EmployeeCount','StandardHours'],axis=1)


# In[27]:


idf=df.interactive()


# **Descriptive statistics**

# In[28]:


# Widget for gender selection as a CheckBoxGroup
gender_source = pn.widgets.CheckBoxGroup(
    name='Gender', 
    options=['Female', 'Male'],
    value=['Female', 'Male']  # Sets both options as selected by default
)


# Monthly Income

# In[29]:


# Define the pipeline
def create_pipeline(selected_gender):
    return (
        df[df['Gender'] == selected_gender]
        .groupby(['YearsAtCompany','Age'])['MonthlyIncome']
        .mean()
        .round(0) 
        .reset_index()
    )


# In[30]:


# Function to create the plot based on selected genders (adapted for multiple selections)
def averagelinearplot_gender_age(selected_genders):
    plots = []
    color_map = {'Female': 'blue', 'Male': 'orange'}
    
    for gender in selected_genders:
        average_data = create_pipeline(gender)
        # Plot 1: Average MonthlyIncome by YearsAtCompany (aggregating across Age)
        avg_income_by_years = average_data.groupby('YearsAtCompany')['MonthlyIncome'].mean().reset_index()
        avg_income_by_years['MonthlyIncome'] = avg_income_by_years['MonthlyIncome'].round(0)
        plot1 = avg_income_by_years.hvplot.line(
            x="YearsAtCompany",
            y='MonthlyIncome',
            line_color=color_map[gender],
            line_width=5,
            title="Average Monthly Income by Years at Company",
            ylabel="Average Monthly Income",
            xlabel="Years at Company",
            ylim=(0, avg_income_by_years['MonthlyIncome'].max() + 10)
        )
        plots.append(plot1)  # Add plot to the list
    
    return hv.Overlay(plots) if plots else hv.Overlay()

# Bind the plotting function to the CheckBoxGroup widget
averages_yearsatcompany_gender_linear_plot = pn.bind(averagelinearplot_gender_age, selected_genders=gender_source)


# In[31]:


# Function to create the plot based on selected genders (adapted for multiple selections)
def averagelinearplot_gender_employeeage(selected_genders):
    plots = []
    color_map = {'Female': 'blue', 'Male': 'orange'}
    
    for gender in selected_genders:
        average_data = create_pipeline(gender)
        # Plot 1: Average MonthlyIncome by YearsAtCompany (aggregating across Age)
        avg_income_by_age = average_data.groupby('Age')['MonthlyIncome'].mean().reset_index()
        avg_income_by_age['MonthlyIncome'] = avg_income_by_age['MonthlyIncome'].round(0)
        plot2 = avg_income_by_age.hvplot.line(
            x="Age",
            y='MonthlyIncome',
            line_color=color_map[gender],
            line_width=5,
            title="Average Monthly Income by Employee Age at Company",
            ylabel="Average Monthly Income",
            xlabel="Age",
            ylim=(0, avg_income_by_age['MonthlyIncome'].max() + 10)
        )
        plots.append(plot2)  # Add plot to the list
    
    return hv.Overlay(plots) if plots else hv.Overlay()

# Bind the plotting function to the CheckBoxGroup widget
averages_employeeage_gender_linear_plot = pn.bind(averagelinearplot_gender_employeeage, selected_genders=gender_source)


# In[32]:


# Define the pipeline
def create_pipeline_2(selected_gender):
    return (
        df[df['Gender'] == selected_gender]
        .groupby(['YearsAtCompany','Age'])['HourlyRate']
        .mean()
        .round(0) 
        .reset_index()
    )


# In[33]:


# Function to create the plot based on selected genders (adapted for multiple selections)
def averagelinearplot_gender_age(selected_genders):
    plots = []
    color_map = {'Female': 'blue', 'Male': 'orange'}
    
    for gender in selected_genders:
        average_data = create_pipeline_2(gender)
        # Plot 1: Average HourlyIncome by YearsAtCompany (aggregating across Age)
        avg_income_by_years = average_data.groupby('YearsAtCompany')['HourlyRate'].mean().reset_index()
        avg_income_by_years['HourlyRate'] = avg_income_by_years['HourlyRate'].round(0)
        plot1 = avg_income_by_years.hvplot.line(
            x="YearsAtCompany",
            y='HourlyRate',
            line_color=color_map[gender],
            line_width=5,
            title="Average Hourly Rate by Years at Company",
            ylabel="Average HourlyRate",
            xlabel="Years at Company",
            ylim=(0, avg_income_by_years['HourlyRate'].max() + 10)
        )
        plots.append(plot1)  # Add plot to the list
    
    return hv.Overlay(plots) if plots else hv.Overlay()

# Bind the plotting function to the CheckBoxGroup widget
hourly_yearsatcompany_gender_linear_plot = pn.bind(averagelinearplot_gender_age, selected_genders=gender_source)


# In[35]:


# Function to create the plot based on selected genders (adapted for multiple selections)
def averagelinearplot_gender_employeeage(selected_genders):
    plots = []
    color_map = {'Female': 'blue', 'Male': 'orange'}
    
    for gender in selected_genders:
        average_data = create_pipeline_2(gender)
        # Plot 1: Average HourlyIncome by Age
        avg_income_by_age = average_data.groupby('Age')['HourlyRate'].mean().reset_index()
        avg_income_by_age['HourlyRate'] = avg_income_by_age['HourlyRate'].round(0)
        plot2 = avg_income_by_age.hvplot.line(
            x="Age",
            y='HourlyRate',
            line_color=color_map[gender],
            line_width=5,
            title="Average HourlyRate by Employee Age at Company",
            ylabel="Average Hourly Rate",
            xlabel="Age",
            ylim=(0, avg_income_by_age['HourlyRate'].max() + 10)
        )
        plots.append(plot2)  # Add plot to the list
    
    return hv.Overlay(plots) if plots else hv.Overlay()

# Bind the plotting function to the CheckBoxGroup widget
hourly_employeeage_gender_linear_plot = pn.bind(averagelinearplot_gender_employeeage, selected_genders=gender_source)


# Panel 1

# In[37]:


# Text label above the gender selection widget
gender_selection_text = pn.pane.Markdown("### Check on the box below to display the data for either Females or Males")

# Define the layout for the top row and bottom row
top_row_layout = pn.Row(averages_yearsatcompany_gender_linear_plot,hourly_yearsatcompany_gender_linear_plot)
down_row_layout = pn.Row(averages_employeeage_gender_linear_plot,hourly_employeeage_gender_linear_plot)

# Additional sidebar information
logo = 'accelerateinclusion.png'
sidebar_text = """
Inclusion Accelerator has conducted an analysis of a publicly available IBM HR Analytics dataset from Kaggle, which includes data from nearly 1,500 current and former employees. 
This interactive dashboard offers insights into the relationships between Monthly Income and Hourly Rate, taking into account employees' tenure with the company and age, as well as disaggregating these metrics by gender."""

# Create a Panel layout for the sidebar with the text and the widget
sidebar_layout = pn.Column(sidebar_text, gender_selection_text, gender_source)

# Create the dashboard template
dashboard_template = pn.template.FastListTemplate(
    title="Interactive Dashboard",
    logo=logo,
    sidebar=sidebar_layout,
    sidebar_width=250,
    main=[top_row_layout, down_row_layout]
)

# Display the dashboard
dashboard_template.show()

