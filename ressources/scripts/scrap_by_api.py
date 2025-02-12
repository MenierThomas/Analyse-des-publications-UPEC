import tkinter as tk
from tkinter import messagebox
import requests


def search_hal():
    """Effectue une recherche sur l'API HAL avec le nom complet fourni."""
    name = search_entry.get().strip()
    if not name:
        messagebox.showerror("Erreur", "Veuillez entrer un nom complet.")
        return

    # URL de l'API HAL
    hal_api_url = "https://api.archives-ouvertes.fr/search/"
    params = {
        "q": f"authFullName_t:\"{name}\"",
        "wt": "json",
        "rows": 10  # Nombre de résultats à afficher
    }

    try:
        # Effectuer la requête API
        response = requests.get(hal_api_url, params=params)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP
        data = response.json()

        # Extraire et afficher les résultats
        docs = data.get("response", {}).get("docs", [])
        if not docs:
            results_text.set("Aucun résultat trouvé.")
        else:
            results = "\n\n".join(
                f"Titre: {doc.get('title_s', ['Sans titre'])[0]}\n"
                f"Auteurs: {', '.join(doc.get('authFullName_s', []))}\n"
                f"URL: {doc.get('uri_s')}"
                for doc in docs
            )
            results_text.set(results)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")


# Création de la fenêtre principale
root = tk.Tk()
root.title("Recherche HAL")
root.geometry("600x400")

# Interface utilisateur
tk.Label(root, text="Rechercher un auteur dans HAL", font=("Helvetica", 16)).pack(pady=10)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_entry = tk.Entry(search_frame, width=50, font=("Helvetica", 14))
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Rechercher", command=search_hal, font=("Helvetica", 12))
search_button.pack(side=tk.LEFT)

results_label = tk.Label(root, text="Résultats:", font=("Helvetica", 14), anchor="w")
results_label.pack(fill="x", padx=10, pady=5)

results_text = tk.StringVar()
results_display = tk.Label(root, textvariable=results_text, font=("Helvetica", 12), justify="left", wraplength=580)
results_display.pack(fill="both", expand=True, padx=10, pady=5)

# Lancement de l'application
root.mainloop()