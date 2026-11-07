import numpy as np
import json
import csv
from car import Car
from config import (
    POPULATION_SIZE, ELITISM_COUNT, MUTATION_RATE,
    MUTATION_SCALE, CROSSOVER_RATE
)

class GeneticAlgorithm:
    """
    Moteur d'optimisation par Algorithmes Génétiques (Neuroévolution).
    Gère la sélection par tournoi, le croisement génétique (crossover),
    la mutation gaussienne, l'élitisme et l'export des métriques.
    """
    def __init__(self, population_size=POPULATION_SIZE):
        self.population_size = population_size
        self.history = [] # Enregistre les métriques pour chaque génération

    def create_population(self, start_x, start_y, start_angle=90.0):
        """Initialise une population de départ avec des réseaux aux poids aléatoires."""
        return [Car(start_x, start_y, start_angle) for _ in range(self.population_size)]

    def evolve(self, population, start_x, start_y, start_angle=90.0):
        """
        Transition vers la génération suivante (N+1) à partir des résultats de la génération N.
        """
        # 1. Tri décroissant par Fitness
        population.sort(key=lambda car: car.fitness, reverse=True)
        
        # 2. Collecte des métriques d'apprentissage
        fitnesses = [c.fitness for c in population]
        best_fitness = fitnesses[0]
        avg_fitness = float(np.mean(fitnesses))
        max_checkpoints = population[0].checkpoints_passed
        
        gen_number = len(self.history) + 1
        stats = {
            "generation": gen_number,
            "best_fitness": round(best_fitness, 2),
            "avg_fitness": round(avg_fitness, 2),
            "max_checkpoints": max_checkpoints
        }
        self.history.append(stats)
        
        # 3. Élitisme : conservation directe des meilleurs individus (Champions)
        new_population = []
        elite_count = min(ELITISM_COUNT, len(population))
        
        for i in range(elite_count):
            champ = population[i]
            elite_car = Car(start_x, start_y, start_angle)
            elite_car.brain.set_dna(champ.brain.get_dna().copy())
            elite_car.is_champion = True
            new_population.append(elite_car)

        # 4. Reproduction (Sélection + Croisement + Mutation) pour le reste
        pool = population[:max(5, len(population) // 2)] # Sélection parmi la moitié supérieure
        
        while len(new_population) < self.population_size:
            # Sélection par tournoi (k = 3)
            p1 = self._tournament_selection(pool, k=3)
            p2 = self._tournament_selection(pool, k=3)
            
            # Croisement (Crossover)
            if np.random.rand() < CROSSOVER_RATE:
                child_dna = self._crossover(p1.brain.get_dna(), p2.brain.get_dna())
            else:
                child_dna = p1.brain.get_dna().copy()
                
            # Mutation génétique
            child_dna = self._mutate(child_dna)
            
            # Instanciation du descendant
            child_car = Car(start_x, start_y, start_angle)
            child_car.brain.set_dna(child_dna)
            new_population.append(child_car)
            
        return new_population, stats

    def _tournament_selection(self, candidates, k=3):
        """Sélectionne le meilleur individu parmi k candidats choisis au hasard."""
        chosen = np.random.choice(candidates, size=min(k, len(candidates)), replace=False)
        return max(chosen, key=lambda c: c.fitness)

    def _crossover(self, dna1, dna2):
        """Croisement uniforme : chaque gène a 50% de probabilité de provenir de chaque parent."""
        mask = np.random.rand(len(dna1)) < 0.5
        child_dna = np.where(mask, dna1, dna2)
        return child_dna

    def _mutate(self, dna):
        """Mutation gaussienne : perturbe certains gènes avec un bruit normalisé."""
        mutation_mask = np.random.rand(len(dna)) < MUTATION_RATE
        noise = np.random.randn(len(dna)) * MUTATION_SCALE
        dna[mutation_mask] += noise[mutation_mask]
        return dna

    def export_csv(self, filepath="metrics.csv"):
        """Exporte l'historique complet des générations au format CSV."""
        if not self.history:
            return
        keys = self.history[0].keys()
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.history)

    def save_best_dna(self, best_car, filepath="best_brain.json"):
        """Sauvegarde les poids du meilleur véhicule pour réutilisation ou démo."""
        data = {
            "fitness": best_car.fitness,
            "checkpoints": best_car.checkpoints_passed,
            "dna": best_car.brain.get_dna().tolist()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_best_dna(self, filepath="best_brain.json"):
        """Charge un génome sauvegardé."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return np.array(data["dna"], dtype=float)
