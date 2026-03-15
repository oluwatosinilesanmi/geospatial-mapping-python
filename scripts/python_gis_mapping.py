import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx

# Read shapefile
states = gpd.read_file("data/State.shp")

# Read population data
pop = pd.read_csv("data/Population_state.csv")

# Clean state names
states['statename'] = states['statename'].str.lower().str.strip()
pop['State'] = pop['State'].str.lower().str.strip()

# Join tables
states_joined = states.merge(
    pop[['State','Total']],
    left_on='statename',
    right_on='State',
    how='left'
)

# Convert population to numeric
states_joined['Total'] = pd.to_numeric(states_joined['Total'], errors='coerce')

# Reproject for basemap
states_map = states_joined.to_crs(epsg=3857)

# Plot map
fig, ax = plt.subplots(figsize=(10,8))

states_map.plot(
    column='Total',
    cmap='YlOrRd',
    scheme='Quantiles',
    k=5,
    legend=True,
    edgecolor='black',
    ax=ax
)

ctx.add_basemap(ax)

ax.set_title("Population Distribution by State")

plt.show()
