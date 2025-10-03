import os
import numpy as np
import bibtexparser
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Ensure 'figures' directory exists
os.makedirs('figures', exist_ok=True)

# Load and parse the BibTeX file
with open('file.bib', 'r') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# Extract years from entries
years = [entry.get('year') for entry in bib_database.entries if 'year' in entry]

# Count the number of articles per year
year_counts = Counter(years)

# Create a DataFrame from the counts and sort by year
df = pd.DataFrame(sorted(year_counts.items()), columns=['Year', 'Count'])

# Convert Year to numeric for proper plotting
df['Year'] = pd.to_numeric(df['Year'])

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(df['Year'], df['Count'], color='skyblue')
plt.xlabel('Year')
plt.ylabel('Number of Articles')
plt.title('Number of Articles per Year')
plt.xticks(rotation=45)

# Calculate moving average (window size = e.g., 3 years)
window_size = 3
df['MovingAvg'] = df['Count'].rolling(window=window_size, min_periods=1).mean()

# Plot the moving average line
plt.plot(df['Year'], df['MovingAvg'], color='orange', linewidth=2, label=f'{window_size}-Year Moving Average')

coeffs_poly = np.polyfit(df['Year'], df['Count'], 2)
poly_trend = np.poly1d(coeffs_poly)(df['Year'])

plt.plot(df['Year'], poly_trend, color='green', linestyle='-.', linewidth=2, label='Quadratic Trend')

# Add labels to each bar with smaller font size and integer formatting
for index, row in df.iterrows():
    if row['Count'] > 0:
        plt.text(
            row['Year'],
            row['Count'] + 0.1,  # slight offset above the bar
            f"{int(row['Count'])}",  # format as integer
            ha='center',
            va='bottom',
            fontsize=8  # reduce font size as desired
        )
        
# Add a legend
plt.legend()

# Add a text below the plot showing total entries
total_entries = len(years)
plt.figtext(0.5, 0.01, f'Total bibtex entries parsed: {total_entries}', ha='center', fontsize=12)

# Adjust layout
plt.tight_layout()

# Save and show the plot
plt.savefig('figures/articles_per_year.png')
plt.show()

# Future additions, add:
# Living review apparatus to extract study features from PDF files - https://andjar.github.io/metawoRld/articles/conceptual_overview.html#introduction-towards-living-reviews
# Social network analysis based on author and citation map in the style of R bibliometrix or Network workbench