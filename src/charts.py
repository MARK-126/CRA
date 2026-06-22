import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

_LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a1a1aa", family="sans-serif"),
    margin=dict(l=10, r=10, t=30, b=10),
)

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
        color="Cantidad",
        color_continuous_scale=["#4f46e5", "#818cf8", "#f97316"],
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        height=520,
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor="#27272a", color="#71717a"),
        yaxis=dict(showgrid=False, color="#a1a1aa"),
    )
    return fig


def build_sector_donut_chart(df_centers):
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
    counts = df_centers["origen_financiamiento"].value_counts().reset_index()
    counts.columns = ["Sector", "Cantidad"]

    fig = px.treemap(
        counts,
        path=[px.Constant("Financiamiento"), "Sector"],
        values="Cantidad",
        color="Cantidad",
        color_continuous_scale=["#1e1b2e", "#4f46e5", "#818cf8"],
    )
    fig.update_layout(
        **_LAYOUT_BASE,
        height=400,
        coloraxis_showscale=False,
    )
    fig.update_traces(
        textfont=dict(color="#f4f4f5", size=13),
        marker_line_color="#0c0c0e",
        marker_line_width=2,
        hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<extra></extra>",
    )
    return fig


def build_centers_per_capita_chart(df_centers, population_data):
    counts = df_centers["departamento_nombre"].str.upper().value_counts().to_dict()

    data = []
    for dept, pop in population_data.items():
        count = counts.get(dept.upper(), 0)
        rate = (count / pop) * 10000
        data.append({"Departamento": dept, "Centros por 10k Hab": round(rate, 2)})

    df_rate = pd.DataFrame(data).sort_values(by="Centros por 10k Hab", ascending=True)

    fig = go.Figure()

    for _, row in df_rate.iterrows():
        fig.add_shape(
            type="line",
            x0=0,
            x1=row["Centros por 10k Hab"],
            y0=row["Departamento"],
            y1=row["Departamento"],
            line=dict(color="#4f46e5", width=2),
        )

    min_val = df_rate["Centros por 10k Hab"].min()
    max_val = df_rate["Centros por 10k Hab"].max()
    norm = (df_rate["Centros por 10k Hab"] - min_val) / (max_val - min_val + 1e-9)
    dot_colors = [
        f"rgb({int(99 + (249 - 99) * n)}, {int(102 + (115 - 102) * n)}, {int(241 + (22 - 241) * n)})"
        for n in norm
    ]

    fig.add_trace(go.Scatter(
        x=df_rate["Centros por 10k Hab"],
        y=df_rate["Departamento"],
        mode="markers",
        marker=dict(
            color=dot_colors,
            size=12,
            line=dict(color="rgba(255,255,255,0.15)", width=1),
        ),
        hovertemplate="%{y}: <b>%{x:.2f}</b> centros por 10k hab<extra></extra>",
    ))

    fig.update_layout(
        **_LAYOUT_BASE,
        height=520,
        xaxis=dict(
            showgrid=True,
            gridcolor="#27272a",
            color="#71717a",
            title="Centros por 10k Hab",
            zeroline=True,
            zerolinecolor="#27272a",
        ),
        yaxis=dict(showgrid=False, color="#a1a1aa"),
        showlegend=False,
    )
    return fig
