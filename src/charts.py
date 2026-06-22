import plotly.express as px
import pandas as pd

_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a1a1aa", family="sans-serif"),
    margin=dict(l=10, r=10, t=30, b=10),
)

# Sectors considered public management
_PUBLIC_SECTORS = {
    "Provincial", "Municipal", "FFAA/Seguridad",
    "Servicio Penitenciario Provincial", "Servicio Penitenciario Federal",
    "Universitario público",
}


def build_centers_by_dept_chart(df_centers):
    counts = df_centers["departamento_nombre"].value_counts().reset_index()
    counts.columns = ["Departamento", "Cantidad"]
    counts = counts.sort_values(by="Cantidad", ascending=True)

    fig = px.bar(
        counts,
        y="Departamento",
        x="Cantidad",
        orientation="h",
        color_discrete_sequence=["#6366f1"],
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        height=520,
        xaxis=dict(showgrid=True, gridcolor="#27272a", color="#71717a"),
        yaxis=dict(showgrid=False, color="#a1a1aa"),
    )
    return fig


def build_sector_donut_chart(df_centers):
    """Donut: Público vs. Privado (grouped from all financing categories)."""
    df = df_centers.copy()
    df["Gestión"] = df["origen_financiamiento"].apply(
        lambda s: "Pública" if s in _PUBLIC_SECTORS else "Privada"
    )
    counts = df["Gestión"].value_counts().reset_index()
    counts.columns = ["Gestión", "Cantidad"]

    fig = px.pie(
        counts,
        names="Gestión",
        values="Cantidad",
        hole=0.58,
        color_discrete_sequence=["#6366f1", "#f59e0b"],
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        height=400,
        legend=dict(
            orientation="h",
            font=dict(size=13, color="#a1a1aa"),
            x=0.5,
            y=-0.08,
            xanchor="center",
        ),
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(size=14, color="#f4f4f5"),
    )
    return fig


def build_financing_breakdown_chart(df_centers):
    """Horizontal bar chart: full breakdown by financing origin, sorted by count."""
    counts = df_centers["origen_financiamiento"].value_counts().reset_index()
    counts.columns = ["Sector", "Cantidad"]
    counts = counts.sort_values("Cantidad", ascending=True)

    fig = px.bar(
        counts,
        y="Sector",
        x="Cantidad",
        orientation="h",
        color_discrete_sequence=["#818cf8"],
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        height=400,
        xaxis=dict(showgrid=True, gridcolor="#27272a", color="#71717a"),
        yaxis=dict(showgrid=False, color="#a1a1aa"),
    )
    return fig


def build_centers_per_capita_chart(df_centers, population_data):
    # Normalize to uppercase to match CSV values (e.g. "CAPITAL") against dict keys ("Capital")
    counts = df_centers["departamento_nombre"].str.upper().value_counts().to_dict()

    data = []
    for dept, pop in population_data.items():
        count = counts.get(dept.upper(), 0)
        rate = (count / pop) * 10000
        data.append({"Departamento": dept, "Centros por 10k Hab": round(rate, 2)})

    df_rate = pd.DataFrame(data).sort_values(by="Centros por 10k Hab", ascending=True)

    fig = px.bar(
        df_rate,
        y="Departamento",
        x="Centros por 10k Hab",
        orientation="h",
        color_discrete_sequence=["#6366f1"],
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        height=520,
        xaxis=dict(showgrid=True, gridcolor="#27272a", color="#71717a"),
        yaxis=dict(showgrid=False, color="#a1a1aa"),
    )
    return fig
