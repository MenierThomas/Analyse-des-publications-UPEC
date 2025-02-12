import matplotlib.pyplot as plt
import pandas as pd

# Data
data = {
    "Nombre de Cœurs": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4],
    "Requête": [
        "publications_per_year", "top_domains_by_year", "domains_no_publications_since", 
        "average_publications_per_domain", "most_active_authors", "domains_in_year_range", 
        "top_authors_by_domain", "publication_trends",
        "publications_per_year", "top_domains_by_year", "domains_no_publications_since", 
        "average_publications_per_domain", "most_active_authors", "domains_in_year_range", 
        "top_authors_by_domain", "publication_trends",
        "publications_per_year", "top_domains_by_year", "domains_no_publications_since", 
        "average_publications_per_domain", "most_active_authors", "domains_in_year_range", 
        "top_authors_by_domain", "publication_trends"
    ],
    "Temps d'Exécution (s)": [
        0.03664350509643555, 0.026810169219970703, 0.01346588134765625, 0.030362367630004883, 0.019965648651123047, 0.01910567283630371, 0.016681432723999023, 0.013717889785766602, 0.022779226303100586, 0.02055048942565918, 0.009142160415649414, 0.010412216186523438, 0.01852273941040039, 0.01616668701171875, 0.012877225875854492, 0.016306161880493164, 0.01985454559326172, 0.018095970153808594, 0.011481523513793945, 0.010516881942749023, 0.011121511459350586, 0.013059377670288086, 0.011122465133666992, 0.013131380081176758
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
plt.savefig("execution_time_plot.png", dpi=300)
plt.close()  # Close the plot to avoid showing it if running in a script
