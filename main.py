import pygame
import sys
import webbrowser
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, POPULATION_SIZE
from track import Track
from ga import GeneticAlgorithm
from ui_panel import UIPanel
from ui_modal import ReportModal
from plot_results import generate_fitness_plot
from export_report import generate_html_report

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuro-Track : Conduite Autonome par Algorithmes Génétiques - Saifeddine TRABELSI")
    clock = pygame.time.Clock()

    # Initialisation des composants
    track = Track()
    ga = GeneticAlgorithm(POPULATION_SIZE)
    population = ga.create_population(track.start_x, track.start_y, track.start_angle)
    
    panel = UIPanel()
    modal = ReportModal()

    generation = 1
    all_time_best_fitness = 0.0
    all_time_best_car = None

    sim_speed = 1
    radar_mode = 1              # 0: Masqué, 1: Leader uniquement, 2: Tous
    is_paused = False
    status_message = "Prêt. Cliquez sur [Consulter le Rapport] ou [F1] pour les explications."
    status_timer = 240

    def trigger_action(action_id):
        nonlocal is_paused, sim_speed, radar_mode, status_message, status_timer, population, generation, all_time_best_fitness, all_time_best_car
        
        if action_id == "toggle_pause":
            is_paused = not is_paused
            status_message = "PAUSE ACTIVÉE" if is_paused else "SIMULATION EN COURS"
            status_timer = 90
            
        elif action_id == "speed_up":
            speeds = [1, 2, 4, 8, 16]
            curr_idx = speeds.index(sim_speed) if sim_speed in speeds else 0
            sim_speed = speeds[(curr_idx + 1) % len(speeds)]
            status_message = f"Vitesse de simulation : {sim_speed}x"
            status_timer = 90
            
        elif action_id == "toggle_radar":
            radar_mode = (radar_mode + 1) % 3
            modes = ["Radars Masqués", "Radars du Leader", "Tous les Radars"]
            status_message = f"Mode Radars : {modes[radar_mode]}"
            status_timer = 90
            
        elif action_id == "skip_gen":
            # Termine immédiatement la génération en cours
            for c in population:
                c.alive = False
            status_message = "Génération écourtée manuellement."
            status_timer = 90
            
        elif action_id == "save_dna":
            if all_time_best_car:
                ga.save_best_dna(all_time_best_car, "best_brain.json")
                status_message = "Champion sauvegardé dans 'best_brain.json' !"
            else:
                status_message = "Aucun champion enregistré pour l'instant."
            status_timer = 120
            
        elif action_id == "load_dna":
            try:
                loaded_dna = ga.load_best_dna("best_brain.json")
                for c in population:
                    c.brain.set_dna(loaded_dna.copy())
                    c.x = track.start_x
                    c.y = track.start_y
                    c.angle = track.start_angle
                    c.alive = True
                    c.checkpoint_index = 1
                    c.checkpoints_passed = 0
                    c.stall_timer = 0
                    c.fitness = 0.0
                status_message = "ADN Champion injecté dans toute la population !"
            except Exception as e:
                status_message = f"Fichier 'best_brain.json' introuvable : {e}"
            status_timer = 140
            
        elif action_id == "open_report":
            modal.toggle()
            status_message = "Rapport technique ouvert."
            status_timer = 60

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        panel.handle_mouse_move(mouse_pos)

        # 1. Gestion des Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if modal.is_open:
                    action = modal.handle_click(mouse_pos)
                    if action == "export_html":
                        ga.export_csv("metrics.csv")
                        generate_fitness_plot("metrics.csv", "fitness_evolution.png")
                        generate_html_report("metrics.csv", "fitness_evolution.png", "rapport_neurotrack.html")
                        try:
                            webbrowser.open("rapport_neurotrack.html")
                        except Exception:
                            pass
                        status_message = "Rapport HTML généré et ouvert dans le navigateur !"
                        status_timer = 150
                else:
                    action_id = panel.handle_mouse_click(mouse_pos)
                    if action_id:
                        trigger_action(action_id)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if modal.is_open:
                        modal.is_open = False
                    else:
                        running = False
                elif event.key == pygame.K_F1:
                    modal.toggle()
                elif event.key == pygame.K_SPACE:
                    trigger_action("toggle_pause")
                elif event.key in (pygame.K_UP, pygame.K_PLUS, pygame.K_KP_PLUS):
                    trigger_action("speed_up")
                elif event.key == pygame.K_r:
                    trigger_action("toggle_radar")
                elif event.key == pygame.K_s:
                    trigger_action("save_dna")
                elif event.key == pygame.K_l:
                    trigger_action("load_dna")
                elif event.key == pygame.K_p:
                    ga.export_csv("metrics.csv")
                    ok = generate_fitness_plot("metrics.csv", "fitness_evolution.png")
                    status_message = "Graphique mis à jour : 'fitness_evolution.png'" if ok else "Erreur graphique"
                    status_timer = 120

        # 2. Mise à jour de la physique et de l'IA
        if not is_paused and not modal.is_open:
            for _ in range(sim_speed):
                alive_count = 0
                current_leader = None
                max_current_fit = -1.0

                for car in population:
                    if car.alive:
                        car.update(track)
                        alive_count += 1
                        if car.fitness > max_current_fit:
                            max_current_fit = car.fitness
                            current_leader = car

                if current_leader and current_leader.fitness > all_time_best_fitness:
                    all_time_best_fitness = current_leader.fitness
                    all_time_best_car = current_leader

                # Évolution quand tous les véhicules se sont crashés
                if alive_count == 0:
                    population, stats = ga.evolve(population, track.start_x, track.start_y, track.start_angle)
                    ga.export_csv("metrics.csv")
                    generate_fitness_plot("metrics.csv", "fitness_evolution.png")
                    generation += 1
                    status_message = f"Génération {generation} - Record: {int(all_time_best_fitness)} pts"
                    status_timer = 100
                    break

        # 3. Rendu de la piste et des voitures
        track.draw(screen, show_checkpoints=False)

        alive_cars = [c for c in population if c.alive]
        leader = max(alive_cars, key=lambda c: c.fitness) if alive_cars else (all_time_best_car if all_time_best_car else population[0])

        for car in population:
            draw_radar = False
            if radar_mode == 2:
                draw_radar = True
            elif radar_mode == 1 and car is leader:
                draw_radar = True
            car.draw(screen, draw_radars=draw_radar)

        # 4. Rendu du panneau latéral de bord (Dashboard)
        panel.draw(
            screen=screen,
            ga=ga,
            leader_car=leader,
            generation=generation,
            alive_count=len(alive_cars),
            total_count=POPULATION_SIZE,
            all_time_best=all_time_best_fitness,
            is_paused=is_paused,
            sim_speed=sim_speed,
            radar_mode=radar_mode
        )

        # 5. Rendu de la modale académique de rapport si activée
        if modal.is_open:
            modal.draw(screen)

        # 6. Notification statut en haut à gauche
        if status_timer > 0:
            status_timer -= 1
            font_notif = pygame.font.SysFont("Consolas", 13, bold=True)
            notif_lbl = font_notif.render(f"> {status_message}", True, (0, 240, 150))
            notif_bg = pygame.Surface((notif_lbl.get_width() + 16, 26), pygame.SRCALPHA)
            notif_bg.fill((15, 20, 28, 220))
            pygame.draw.rect(notif_bg, (0, 190, 255), (0, 0, notif_bg.get_width(), 26), width=1, border_radius=4)
            notif_bg.blit(notif_lbl, (8, 5))
            screen.blit(notif_bg, (15, 12))

        pygame.display.flip()
        clock.tick(FPS)

    # Sauvegarde automatique à la sortie
    if len(ga.history) > 0:
        ga.export_csv("metrics.csv")
        generate_fitness_plot("metrics.csv", "fitness_evolution.png")
        generate_html_report("metrics.csv", "fitness_evolution.png", "rapport_neurotrack.html")
        if all_time_best_car:
            ga.save_best_dna(all_time_best_car, "best_brain.json")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
