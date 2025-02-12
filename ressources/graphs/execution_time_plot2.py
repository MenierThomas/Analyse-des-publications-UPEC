import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    "Nombre de Cœurs": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4],
    "Requête": [
        "publications_per_year", "top_domains_by_year", "domains_no_publications_since", 
        "average_publications_per_domain", "most_active_authors", "domains_in_year_range",
        "publications_per_year", "top_domains_by_year", "domains_no_publications_since", 
        "average_publications_per_domain", "most_active_authors", "domains_in_year_range",
        "publications_per_year", "top_domains_by_year", "domains_no_publications_since", 
        "average_publications_per_domain", "most_active_authors", "domains_in_year_range"
        ],
    "Temps d'Exécution (s)": [
        0.5057, 0.42449, 0.39752, 0.41207, 0.38328, 0.41810,
        0.4951, 0.41581, 0.38970, 0.41171, 0.38370, 0.41710,
        0.4969, 0.42171, 0.39150, 0.41033, 0.38226, 0.42001
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Pivot the data for easier plotting
pivoted = df.pivot(index="Requête", columns="Nombre de Cœurs", values="Temps d'Exécution (s)")

# Plot
plt.figure(figsize=(10, 6))
for request in pivoted.index:
    plt.plot(pivoted.columns, pivoted.loc[request], marker='o', label=request)

# Add titles and labels
plt.title("Execution Time by Request and Number of Cores", fontsize=14)
plt.xlabel("Number of Cores", fontsize=12)
plt.ylabel("Execution Time (s)", fontsize=12)
plt.legend(title="Request", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()

# Save the plot as an image
plt.savefig("execution_time_plot2.png", dpi=300)
plt.close()  # Close the plot to avoid showing it if running in a script