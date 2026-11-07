import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import pygame
from config import POPULATION_SIZE
from track import Track
from ga import GeneticAlgorithm
from plot_results import generate_fitness_plot
from export_report import generate_html_report

def train():
    pygame.init()
    track = Track()
    ga = GeneticAlgorithm(population_size=POPULATION_SIZE)
    pop = ga.create_population(track.start_x, track.start_y, track.start_angle)

    print("=== Entraînement d'un Champion Neuro-Track (15 générations) ===")
    all_time_best = None
    all_time_fit = 0.0

    for gen in range(1, 16):
        steps = 0
        while any(c.alive for c in pop) and steps < 1200:
            for c in pop:
                if c.alive:
                    c.update(track)
            steps += 1
            
        cur_leader = max(pop, key=lambda c: c.fitness)
        if cur_leader.fitness > all_time_fit:
            all_time_fit = cur_leader.fitness
            all_time_best = cur_leader

        pop, stats = ga.evolve(pop, track.start_x, track.start_y, track.start_angle)
        print(f"Génération {stats['generation']:2d} : Fitness Max = {stats['best_fitness']:8.1f} pts | Checkpoints = {stats['max_checkpoints']:2d} | Moyenne = {stats['avg_fitness']:7.1f} pts")

    if all_time_best:
        ga.save_best_dna(all_time_best, "best_brain.json")
        print(f"\n[OK] Champion sauvegardé avec succès dans 'best_brain.json' (Record : {all_time_fit:.1f} pts)")

    ga.export_csv("metrics.csv")
    generate_fitness_plot("metrics.csv", "fitness_evolution.png")
    generate_html_report("metrics.csv", "fitness_evolution.png", "rapport_neurotrack.html")
    print("[OK] Métriques, graphique et rapport HTML générés !")

if __name__ == "__main__":
    train()
