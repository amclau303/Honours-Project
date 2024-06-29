from django.shortcuts import render
import plotly.express as px
from django.db.models import Count
from thyroid.models import Thyroid
import pandas as pd
import plotly.graph_objects as go

def chart(request):
    # Define the years for the slide
    years = [2005, 2006, 2015, 2016, 2019, 2020, 2021]
    
    # Prepare data for both treatment_status and thyroid_status
    data = []
    for year in years:
        thyroid_year = Thyroid.objects.filter(year=year)
        treatment_counts = thyroid_year.filter(treatment_status__isnull=False).values('treatment_status').annotate(count=Count('treatment_status'))
        thyroid_counts = thyroid_year.values('thyroid_status').annotate(count=Count('thyroid_status'))
        
        for entry in treatment_counts:
            data.append({'year': year, 'status_type': 'treatment', 'status': entry['treatment_status'], 'count': entry['count']})
        for entry in thyroid_counts:
            data.append({'year': year, 'status_type': 'thyroid', 'status': entry['thyroid_status'], 'count': entry['count']})
    
    # Convert data to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Create the animated bar chart
    fig = px.bar(df[df['status_type'] == 'thyroid'], x='status', y='count', animation_frame='year', range_y=[0, df['count'].max()],
                 labels={'status': 'Thyroid Status', 'count': 'Count'},
                 title='Thyroid Status Counts by Year')   

    # Convert the chart to HTML
    chart = fig.to_html(full_html=False)

    # Pass the chart to the template
    context = {'chart': chart}
    return render(request, 'chart.html', context)

def line_chart(request):
    thyroid = Thyroid.objects.all()

    # Convert QuerySet to list of dictionaries
    thyroid_list = list(thyroid.values('year', 'gender', 'treatment_status', 'thyroid_status'))

    # Create DataFrame
    df = pd.DataFrame(thyroid_list)

    # Filter data for males with 'yes' as thyroid_status
    df_filtered_thyroid_status = df[(df['year'] != 2005) & (df['year'] != 2006) & (df['thyroid_status'] == 'yes')]

    # Group by year and count occurrences for thyroid_status
    df_grouped_thyroid_status = df_filtered_thyroid_status.groupby('year').size().reset_index(name='count')

    # Filter data for people with 'yes' as treatment_status
    df_filtered_treatment_status = df[df['treatment_status'] == 'yes']

    # Group by year and count occurrences for treatment_status
    df_grouped_treatment_status = df_filtered_treatment_status.groupby('year').size().reset_index(name='count')

    # Initialize figure
    fig = go.Figure()

    # Add trace for males with 'yes' thyroid status
    fig.add_trace(go.Scatter(x=df_grouped_thyroid_status['year'], y=df_grouped_thyroid_status['count'], mode='lines+markers', name='Amount of people with Thyroid Disorder', line=dict(color="#33CFA5")))

    # Add trace for people with 'yes' treatment status
    fig.add_trace(go.Scatter(x=df_grouped_treatment_status['year'], y=df_grouped_treatment_status['count'], mode='lines+markers', name='Amount of people with Thyroid Disorder who sought treatment', line=dict(color="#F06A6A")))

    # Annotations for the highest values
    max_thyroid_status = df_grouped_thyroid_status[df_grouped_thyroid_status['count'] == df_grouped_thyroid_status['count'].max()]
    max_treatment_status = df_grouped_treatment_status[df_grouped_treatment_status['count'] == df_grouped_treatment_status['count'].max()]

    max_thyroid_annotation = [
        dict(
            x=max_thyroid_status['year'].values[0],
            y=max_thyroid_status['count'].values[0],
            xref="x",
            yref="y",
            text=f"Max Thyroid Status: {max_thyroid_status['count'].values[0]}",
            showarrow=True,
            arrowhead=7,
            ax=50,
            ay=-40
        )
    ]

    max_treatment_annotation = [
        dict(
            x=max_treatment_status['year'].values[0],
            y=max_treatment_status['count'].values[0],
            xref="x",
            yref="y",
            text=f"Max Treatment Status: {max_treatment_status['count'].values[0]}",
            showarrow=True,
            arrowhead=7,
            ax=-50,
            ay=70
        )
    ]

    # Update layout with annotations
    fig.update_layout(
        title="",
        xaxis_title="Year",
        yaxis_title="Count",
        updatemenus =[
            dict(
                active=0,
                buttons=list([
                    dict(
                        label="None",
                        method="update",
                        args=[{"visible": [True, True]},
                              {"title": "Thyroid Status",
                               "annotations": []}]
                    ),
                    dict(
                        label="Both",
                        method="update",
                        args=[{"visible": [True, True]},
                              {"title": "Thyroid/Treatment with Max Values",
                               "annotations": max_treatment_annotation + max_thyroid_annotation}]
                    ),
                    dict(
                        label="Thyroid",
                        method="update",
                        args=[{"visible": [True, False]},
                              {"title": "Thyroid Disorder Amounts",
                               "annotations": max_thyroid_annotation}]
                    ),
                    dict(
                        label="Treatment",
                        method="update",
                        args=[{"visible": [False, True]},
                              {"title": "Treatment Amounts",
                               "annotations": max_treatment_annotation}]
                    ),
                ])
            )
        ]
    )

    # Convert figure to HTML
    line_chart = fig.to_html()

    context = {'line_chart': line_chart}
    return render(request, 'line_chart.html', context)

def scatter_plot(request):
    thyroid = Thyroid.objects.all()

    # Convert to DataFrame
    df = pd.DataFrame(thyroid.values())

    # Filter for 'yes' thyroid_status
    df_filtered = df[df['thyroid_status'] == 'yes']

    # Group by year and gender and count occurrences
    df_grouped = df_filtered.groupby(['year', 'gender']).size().reset_index(name='count')

    # Separate the data for male and female
    df_male = df_grouped[df_grouped['gender'] == 'male']
    df_female = df_grouped[df_grouped['gender'] == 'female']

    # Create scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_male['year'], 
        y=df_male['count'],
        mode='markers',
        name='Male',
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=df_female['year'], 
        y=df_female['count'],
        mode='markers',
        name='Female',
        marker=dict(color='pink')
    ))

    fig.update_layout(
        title="Scatter Plot of Thyroid Status 'Yes' by Gender",
        xaxis_title="Year",
        yaxis_title="Count",
        template='plotly_white'
    )

    scatter_plot_html = fig.to_html(full_html=False)

    context = {'scatter_plot': scatter_plot_html}
    return render(request, 'scatter_plot.html', context)