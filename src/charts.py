import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def build_centers_by_dept_chart(df_centers):
    counts = df_centers["departamento_nombre"].value_counts().reset_index()
    counts.columns = ["Departamento", "Cantidad"]
    counts = counts.sort_values(by="Cantidad", ascending=True)
    
    fig = px.bar(
        counts,
        y="Departamento",
        x="Cantidad",
        orientation="h",
        color_discrete_sequence=["#0f766e"]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ccfbf1"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor="#115e59"),
        yaxis=dict(showgrid=False)
    )
    return fig

def build_sector_distribution_chart(df_centers):
    counts = df_centers["origen_financiamiento"].value_counts().reset_index()
    counts.columns = ["Sector", "Cantidad"]
    
    fig = px.pie(
        counts,
        names="Sector",
        values="Cantidad",
        hole=0.4,
        color_discrete_sequence=["#0f766e", "#0d9488"]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ccfbf1"),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    fig.update_traces(textinfo="percent+label")
    return fig

def build_centers_per_capita_chart(df_centers, population_data):
    counts = df_centers["departamento_nombre"].value_counts().to_dict()
    
    data = []
    for dept, pop in population_data.items():
        count = counts.get(dept, 0)
        rate = (count / pop) * 10000
        data.append({"Departamento": dept, "Centros por 10k Hab": round(rate, 2)})
        
    df_rate = pd.DataFrame(data).sort_values(by="Centros por 10k Hab", ascending=True)
    
    fig = px.bar(
        df_rate,
        y="Departamento",
        x="Centros por 10k Hab",
        orientation="h",
        color_discrete_sequence=["#0f766e"]
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ccfbf1"),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor="#115e59"),
        yaxis=dict(showgrid=False)
    )
    return fig
