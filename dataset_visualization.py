import pandas as pd
import matplotlib, matplotlib.pyplot as plt

def is_interface():
    backend = matplotlib.get_backend().lower()
    return any(x in backend for x in ["qt", "tk", "wx", "gtk", "macosx", "nbagg"])

file_name = "cities_average_temperature_annual_line_graph.png"

df = pd.read_csv("dataset.csv", low_memory=False)

df["Date"] = pd.to_datetime(df[["Year", "Month", "Day"]], errors="coerce")
df = df.dropna(subset=["Date"])

cities = ["Sao Paulo", "Rio de Janeiro", "Tokyo", "Amsterdam"]
df = df[df["City"].isin(cities)]

df["AvgTemperatureC"] = (df["AvgTemperature"] - 32) * 5/9

df_annual = df.groupby(["City", "Year"])["AvgTemperatureC"].mean().reset_index()

plt.figure(figsize=(10,6))

for city in cities:
    data = df_annual[df_annual["City"] == city]
    plt.plot(data["Year"], data["AvgTemperatureC"], marker="o", label=city)

plt.title("Temperatura Média Anual")
plt.xlabel("Ano")
plt.ylabel("Temperatura Média (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()

if is_interface():
    plt.show()
else:
    plt.savefig(file_name)
    print(f"No UI detected. Graph saved as {file_name}")