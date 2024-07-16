from django.shortcuts import render
import plotly.express as px
import plotly.offline as pyo    
from django.db.models import Count
from django.http import HttpResponse
from django.template.loader import render_to_string
from thyroid.models import Thyroid
from thyroid.models import Location
from thyroid.models import PatientData
import pandas as pd
import plotly.graph_objects as go


def index(request):

    context = {
        'message': 'Hello'
    }

    return render(request, 'index.html', context)

def bar_chart(request):
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
    
    # Create the animated bar chart with enhancements
    fig = px.bar(
        df[df['status_type'] == 'thyroid'],
        x='status',
        y='count',
        color='status',
        animation_frame='year',
        range_y=[0, df['count'].max()],
        labels={'status': 'Thyroid Status', 'count': 'Count'},
        title='Thyroid Status Counts by Year'
    )
    
    # Update layout for better aesthetics
    fig.update_layout(
        title={'text': 'Thyroid Status Counts by Year', 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
        xaxis_title='Thyroid Status',
        yaxis_title='Count',
        legend_title='Thyroid Status',
        font=dict(family="Arial, sans-serif", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    # Add custom hover information
    fig.update_traces(
        hovertemplate='<b>Status:</b> %{x}<br><b>Count:</b> %{y}<br><b>Year:</b> %{frame}'
    )

    # Convert the chart to HTML
    chart = fig.to_html(full_html=False)

    # Pass the chart to the template
    context = {'chart': chart}
    return render(request, 'bar_chart.html', context)

def line_chart(request):
    thyroid = Thyroid.objects.all()

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(list(thyroid.values('year', 'gender', 'treatment_status', 'thyroid_status')))

    # Filter data for 'yes' thyroid_status and 'yes' treatment_status
    df_filtered = df[(df['thyroid_status'] == 'yes') | (df['treatment_status'] == 'yes')]

    # Group by year and count occurrences for both statuses
    df_grouped = df_filtered.groupby('year').agg({
        'thyroid_status': lambda x: (x == 'yes').sum(),
        'treatment_status': lambda x: (x == 'yes').sum()
    }).reset_index()

    # Initialize figure
    fig = go.Figure()

    # Add trace for 'yes' thyroid status
    fig.add_trace(go.Scatter(x=df_grouped['year'], y=df_grouped['thyroid_status'], mode='lines+markers', 
                             name='Thyroid Disorder', line=dict(color="#33CFA5")))

    # Add trace for 'yes' treatment status
    fig.add_trace(go.Scatter(x=df_grouped['year'], y=df_grouped['treatment_status'], mode='lines+markers', 
                             name='Thyroid Disorder with Treatment', line=dict(color="#F06A6A")))

    # Annotations for Thyroid Disorder trace
    max_thyroid_year = df_grouped.loc[df_grouped['thyroid_status'].idxmax(), 'year']
    max_thyroid_annotation = [
        dict(
            x=max_thyroid_year,
            y=df_grouped.loc[df_grouped['year'] == max_thyroid_year, 'thyroid_status'].values[0],
            xref="x",
            yref="y",
            text=f'Max Thyroid Disorder: {df_grouped["thyroid_status"].max()}',
            showarrow=True, arrowhead=7, ax=50, ay=-40
        )
    ]

    # Annotations for Thyroid Disorder with Treatment trace
    max_treatment_year = df_grouped.loc[df_grouped['treatment_status'].idxmax(), 'year']
    max_treatment_annotation = [
        dict(
            x=max_treatment_year,
            y=df_grouped.loc[df_grouped['year'] == max_treatment_year, 'treatment_status'].values[0],
            xref="x",
            yref="y",
            text=f'Max Treatment: {df_grouped["treatment_status"].max()}',
            showarrow=True, arrowhead=7, ax=-50, ay=70
        )
    ]

    # Add annotations to the figure
    fig.update_layout(
        annotations=max_thyroid_annotation + max_treatment_annotation
    )

    # Update layout
    fig.update_layout(
        title="Thyroid Disorder Analysis",
        xaxis_title="Year",
        yaxis_title="Count",
        legend=dict(x=0.01, y=0.99),
        plot_bgcolor='rgba(0,0,0,0)',
        updatemenus=[
            dict(
                type="buttons",
                direction="down",
                buttons=list([
                    dict(label="Reset",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Thyroid Disorder Analysis",
                                "annotations": max_thyroid_annotation + max_treatment_annotation}]),
                    dict(label="Max Values",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Thyroid/Treatment with Max Values",
                                "annotations": max_thyroid_annotation + max_treatment_annotation}]),
                    dict(label="Thyroid Only",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Thyroid Disorder Analysis",
                                "annotations": max_thyroid_annotation}]),
                    dict(label="Treatment Only",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Thyroid Disorder with Treatment Analysis",
                                "annotations": max_treatment_annotation}]),
                ]),
                showactive=True,
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

def stacked_bar_chart(request):
    thyroid_data = Thyroid.objects.all()

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(list(thyroid_data.values('year', 'gender', 'treatment_status', 'thyroid_status')))

    # Filter data for 'yes' thyroid_status and 'yes' treatment_status
    df_filtered = df[(df['thyroid_status'] == 'yes') | (df['treatment_status'] == 'yes')]

    # Group by year and gender, count occurrences for each status
    df_grouped = df_filtered.groupby(['year', 'gender']).agg({
        'treatment_status': lambda x: (x == 'yes').sum(),
        'thyroid_status': lambda x: (x == 'yes').sum()
    }).reset_index()

    # Pivot the DataFrame for easier plotting
    df_pivot = df_grouped.pivot(index='year', columns='gender', values=['treatment_status', 'thyroid_status']).fillna(0)

    # Plotting the stacked bar chart
    fig = go.Figure()

    # Add traces for treatment_status
    fig.add_trace(go.Bar(x=df_pivot.index.astype(str), y=df_pivot['treatment_status']['male'], name='Male - Treated',
                         marker_color='#1f77b4'))
    fig.add_trace(go.Bar(x=df_pivot.index.astype(str), y=df_pivot['treatment_status']['female'], name='Female - Treated',
                         marker_color='#ff7f0e'))

    # Add traces for thyroid_status
    fig.add_trace(go.Bar(x=df_pivot.index.astype(str), y=df_pivot['thyroid_status']['male'], name='Male - Thyroid Disease',
                         marker_color='#2ca02c'))
    fig.add_trace(go.Bar(x=df_pivot.index.astype(str), y=df_pivot['thyroid_status']['female'], name='Female - Thyroid Disease',
                         marker_color='#d62728'))

    # Update layout
    fig.update_layout(
        barmode='stack',
        xaxis=dict(
            title='Year',
            tickmode='linear',
            tick0=df_pivot.index.min(),
            dtick=1,
            tickangle=-45,
            tickformat='%Y',  # Format as year
            showgrid=True,
            gridcolor='lightgray',
        ),
        yaxis_title='Count',
        legend=dict(x=0.01, y=0.99),
        plot_bgcolor='rgba(0,0,0,0)',
        title='Thyroid Disorder and Treatment Status by Gender',
        margin=dict(t=50, l=10, r=10, b=70),  # Increased bottom margin for x-axis labels
    )

    # Convert figure to HTML
    stacked_bar_chart = fig.to_html()

    context = {'stacked_bar_chart': stacked_bar_chart}
    return render(request, 'stacked_bar_chart.html', context)

def thyroid_map_view(request):
        
    # Fetch all locations from the database
    locations = Location.objects.all()

    # Filter out locations where latitude or longitude is 0
    filtered_locations = [loc for loc in locations if loc.latnum != 0 and loc.longnum != 0]
    
    # Create a DataFrame from the fetched data
    data = {
        'Latitude': [loc.latnum for loc in filtered_locations],
        'Longitude': [loc.longnum for loc in filtered_locations]
    }
    df = pd.DataFrame(data)
    
    # Generate the Plotly heatmap with a less intense color scale
    fig = px.density_mapbox(
        df, lat='Latitude', lon='Longitude', radius=10,
        mapbox_style='open-street-map',
        title='Thyroid Locations Heatmap',
        height=1000,  # Increase the height of the map
        color_continuous_scale="Viridis"  # Adjust color scale to be less intense
    )
    
    # Set the opacity of the heatmap
    fig.update_traces(opacity=0.6)  # Adjust the opacity to make the colors less intense
    
    # Set the map's center and zoom level
    fig.update_layout(mapbox=dict(center=dict(lat=df['Latitude'].mean(), lon=df['Longitude'].mean()), zoom=4.5))
    
    # Convert the Plotly figure to HTML
    plot_div = fig.to_html(full_html=False)
    
    # Render the template with the Plotly map
    return render(request, 'thyroid_map.html', {'plot_div': plot_div})

def plot_visualizations(request):
    # Fetch data from the database
    data = PatientData.objects.all().values()
    df = pd.DataFrame(data)
    
    # Visualization 1: Distribution of age by gender
    fig1 = px.histogram(df, x='age', color='sex', barmode='overlay', title='Age Distribution by Gender')
    plot1 = pyo.plot(fig1, output_type='div')

    # Visualization 2: Scatter plot of TSH vs T3 levels
    fig2 = px.scatter(df, x='TSH', y='T3', color='sex', title='TSH vs T3 Levels')
    plot2 = pyo.plot(fig2, output_type='div')

    # Visualization 3: Bar plot of the count of different thyroid conditions
    condition_cols = [
        'on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 'sick', 'pregnant', 
        'thyroid_surgery', 'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid', 
        'lithium', 'goitre', 'tumor', 'hypopituitary', 'psych'
    ]
    condition_counts = df[condition_cols].sum().reset_index()
    condition_counts.columns = ['condition', 'count']
    fig3 = px.bar(condition_counts, x='condition', y='count', title='Count of Different Thyroid Conditions')
    plot3 = pyo.plot(fig3, output_type='div')

    context = {
        'plot1': plot1,
        'plot2': plot2,
        'plot3': plot3
    }

    return render(request, 'patient_data.html', context)

def hyper_hypo(request):
    # Get all patient data
    data = PatientData.objects.all().values()
    
    # Convert QuerySet to DataFrame
    df = pd.DataFrame(data)
    
    # Visualization for query_hypothyroid
    query_hypothyroid_counts = df['query_hypothyroid'].value_counts().reset_index()
    query_hypothyroid_counts.columns = ['query_hypothyroid', 'count']
    fig_hypo = px.bar(query_hypothyroid_counts, x='query_hypothyroid', y='count', 
                      title='Count of Query Hypothyroid (0 = False, 1 = True)')
    
    # Visualization for query_hyperthyroid
    query_hyperthyroid_counts = df['query_hyperthyroid'].value_counts().reset_index()
    query_hyperthyroid_counts.columns = ['query_hyperthyroid', 'count']
    fig_hyper = px.bar(query_hyperthyroid_counts, x='query_hyperthyroid', y='count', 
                       title='Count of Query Hyperthyroid (0 = False, 1 = True)')
    
    # Convert the Plotly figures to HTML
    fig_hypo_html = fig_hypo.to_html(full_html=False)
    fig_hyper_html = fig_hyper.to_html(full_html=False)
    
    # Render the visualizations in the template
    return render(request, 'hyper_hypo.html', 
                  {'fig_hypo_html': fig_hypo_html, 'fig_hyper_html': fig_hyper_html})

def dashboard(request):
    # Render individual views and collect HTML outputs
    bar_chart_html = bar_chart(request).content.decode('utf-8')
    line_chart_html = line_chart(request).content.decode('utf-8')
    scatter_plot_html = scatter_plot(request).content.decode('utf-8')
    stacked_bar_chart_html = stacked_bar_chart(request).content.decode('utf-8')
    plot_visualizations_html = plot_visualizations(request).content.decode('utf-8')
    thyroid_map_view_html = thyroid_map_view(request).content.decode('utf-8')

    # Render a combined HTML template
    combined_html = render_to_string('dashboard.html', {
        'bar_chart_html': bar_chart_html,
        'line_chart_html': line_chart_html,
        'scatter_plot_html': scatter_plot_html,
        'stacked_bar_chart_html': stacked_bar_chart_html,
        'plot_visualizations_html': plot_visualizations_html,
        'thyroid_map_view_html': thyroid_map_view_html,
    })
    
    return HttpResponse(combined_html)