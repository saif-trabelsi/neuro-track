import os
import csv
import matplotlib.pyplot as plt

def generate_fitness_plot(csv_path="metrics.csv", output_png="fitness_evolution.png"):
    """
    Génère la courbe d'apprentissage officielle pour le rapport de Madame Bouhajeb :
    Évolution du Fitness Maximal et Moyen en fonction de la Génération.
    """
    if not os.path.exists(csv_path):
        print(f"[Plot] Fichier {csv_path} introuvable. Lancez d'abord la simulation.")
        return False

    generations = []
    best_fitnesses = []
    avg_fitnesses = []

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            generations.append(int(row["generation"]))
            best_fitnesses.append(float(row["best_fitness"]))
            avg_fitnesses.append(float(row["avg_fitness"]))

    if not generations:
        print("[Plot] Aucune donnée à tracer.")
        return False

    plt.figure(figsize=(10, 6), dpi=150)
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')

    # Courbe du meilleur fitness (Fitness Max)
    plt.plot(generations, best_fitnesses, color="#007acc", linewidth=2.5, marker="o", markersize=4, label="Fitness Maximal (Élite)")
    # Courbe de la moyenne de la population
    plt.plot(generations, avg_fitnesses, color="#e67e22", linewidth=1.8, linestyle="--", label="Fitness Moyen de la Population")

    plt.title("Neuro-Track : Courbe d'Apprentissage par Algorithme Génétique", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Numéro de la Génération", fontsize=12)
    plt.ylabel("Score de Fitness (Distance & Checkpoints)", fontsize=12)
    plt.legend(loc="upper left", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.6)

    # Annoter le score maximal atteint
    max_idx = best_fitnesses.index(max(best_fitnesses))
    plt.annotate(
        f"Pic: {best_fitnesses[max_idx]:.0f} pts (Gén {generations[max_idx]})",
        xy=(generations[max_idx], best_fitnesses[max_idx]),
        xytext=(generations[max_idx] - max(1, len(generations)//8), best_fitnesses[max_idx] * 0.9),
        arrowprops=dict(facecolor="#27ae60", shrink=0.08, width=1.5, headwidth=8),
        fontsize=10,
        fontweight="bold",
        color="#27ae60"
    )

    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()
    print(f"[Plot] Graphique d'apprentissage sauvegardé avec succès sous '{output_png}'.")
    return True

if __name__ == "__main__":
    generate_fitness_plot()
