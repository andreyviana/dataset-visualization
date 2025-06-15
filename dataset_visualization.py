import pandas as pd
import matplotlib, matplotlib.pyplot as plt
import plotly.graph_objects as go

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

df_year = df[df["Year"] == year]
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

if is_interface():
    plt.show()
    fig.show()
else:
    print(f"No UI detected to show any graph.")