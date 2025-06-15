import pandas as pd
import matplotlib, matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

def is_interface():
    backend = matplotlib.get_backend().lower()
    return any(x in backend for x in ["qt", "tk", "wx", "gtk", "macosx", "nbagg"])

year = 2020

df = pd.read_csv("https://raw.githubusercontent.com/andreyviana/dataset-visualization/refs/heads/main/dataset.csv", low_memory=False)

df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]], errors="coerce")
df = df.dropna(subset=["Date"])

df["AvgTemperatureC"] = (df["AvgTemperature"] - 32) * 5/9

cities = ["Sao Paulo", "Rio de Janeiro", "Tokyo", "Amsterdam", "La Paz", "Buenos Aires", "Bogota"]
df = df[df["City"].isin(cities)]
df_year = df[df["Year"] == year]


def line_graph():
    df_annual = df.groupby(["City", "Year"])["AvgTemperatureC"].mean().reset_index()

    plt.figure(figsize=(10, 6))

    for city in cities:
        data = df_annual[df_annual["City"] == city]
        plt.plot(data["Year"], data["AvgTemperatureC"], marker="o", label=city)

    plt.title("Temperatura Média Anual")
    plt.xlabel("Ano")
    plt.ylabel("Temperatura Média (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.show()

def choropleth_map():
    df_country_avg = df_year.groupby("Country")["AvgTemperatureC"].mean().reset_index()

    fig = go.Figure(data=go.Choropleth(
        locations=df_country_avg["Country"],
        z=df_country_avg["AvgTemperatureC"],
        locationmode="country names",
        colorscale="Reds",
        colorbar_title="Temperatura (°C)",
    ))

    fig.update_layout(
        title_text=f"Temperatura Média em {year} - América do Sul",
        geo_scope="south america",
    )

    fig.show()

def chord_diagram():
    countries = ["Brazil", "Bolivia", "Colombia", "Argentina"]

    df_south_america = df_year[df_year["Country"].isin(countries)]

    df_country_diff = df_south_america.groupby("Country")["AvgTemperatureC"].mean().reset_index()

    labels = df_country_diff["Country"].tolist()
    values = df_country_diff["AvgTemperatureC"].tolist()

    matrix = np.zeros((len(labels), len(labels)))

    for i in range(len(labels)):
        for j in range(len(labels)):
            if i != j:
                matrix[i][j] = abs(values[i] - values[j])

    df_diff = pd.DataFrame(matrix, index=labels, columns=labels).round(2)

    fig = go.Figure(data=[go.Table(
        header=dict(values=[""] + labels,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[labels] + [df_diff[col].tolist() for col in df_diff.columns],
                   fill_color='lavender',
                   align='left'))
    ])

    fig.update_layout(
        title=f"Diferença de Temperatura Média entre Países - {year}"
    )

    fig.show()

if is_interface():
    line_graph()
    choropleth_map()
    chord_diagram()

else:
    print(f"No UI detected to show any graph.")