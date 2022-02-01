import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Assignment: Global CO2 emissions for Winc Academy
Hugo Maat, 31-1-2022
Version 1.0
"""

tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions")
table_1 = tables[1]
table_1 = table_1.loc[3:] # removing non-countries (except the E.U.)
table_1.columns = ["countries", "1990", "2005", "2017", 
"2017_percent_world", "2017vs1990", "2017_perlandarea",
"2017_percapita", "2018", "2018no"]
table_1 = table_1[["countries","1990","2005","2017","2018"]]

# Cleaning and selecting top 5
table_1 = table_1.set_index("countries")
table_1.at["Serbia & Montenegro","2018"] = 45.45
# Values for Serbia & Montenegro in 2018 were "45.45/2.55", 
# which is str not float. Sorting functions would not work.
table_1 = table_1.drop("European Union")
table_1 = table_1.reset_index()

table_1["2018"] = table_1["2018"].astype(float)
top5 = table_1.nlargest(5, "2018")

# For graph 1

fig, ax = plt.subplots()

timeframe = [1990,2005,2017,2018]
for index, row in top5.iterrows():
    ax.plot(timeframe, row[1:], label=row[0])
ax.set_xticks(timeframe,timeframe)
# I set the x axis to space the dates of measurement numerically,
# otherwise the change in interval would distort the data.
ax.set_xlabel("Estimates by year")
ax.set_ylabel("Emissions in Mt CO2")
ax.set_title("Top 5 biggest CO2 producers")
ax.legend()

# For graph 2

for index, row in table_1.iterrows():
    for year in ["1990", "2005", "2017", "2018"]:
        table_1.at[index,f"change_{year}"] = table_1.at[index,year] \
        / table_1.at[index,"1990"] * 100

top3 = table_1.nlargest(3, "change_2018")
bottom3 = table_1.nsmallest(3, "change_2018")
# This returns some very small countries, like the Solomon Islands.
# Countries with CO2 emissions below 5 Mt in 1990 will filtered out.

table_1 = table_1.rename(columns={"1990":"y1990"})
table_2 = table_1.loc[table_1.y1990 > 5]
# This I find very unpleasant, but table_1.loc[table_1.1990 > 5]
# caused an error. Apparently .loc does not want me to name columns
# using numbers. 

top3 = table_2.nlargest(3, "change_2018")
bottom3 = table_2.nsmallest(3, "change_2018")

fig, (ax2, ax3) = plt.subplots(2,1,sharex=True)

for index, row in top3.iterrows():
    ax2.plot(timeframe, row[5:], label=row[0])
ax2.set_xticks(timeframe,timeframe)
ax2.set_xlabel("Estimates by year")
ax2.set_ylabel("Emission relative to 1990 in %")
ax2.set_title("Top 3 increase CO2 emissions")
ax2.legend()

for index, row in bottom3.iterrows():
    ax3.plot(timeframe, row[5:], label=row[0])
ax3.set_xticks(timeframe,timeframe)
ax3.set_xlabel("Estimates by year")
ax3.set_ylabel("Emission relative to 1990 in %")
ax3.set_title("Top 3 decrease CO2 emissions")
ax3.legend()

plt.show()