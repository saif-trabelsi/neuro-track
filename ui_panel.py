import pygame
import math
import numpy as np
from config import (
    ARENA_WIDTH, PANEL_WIDTH, SCREEN_HEIGHT,
    COLOR_PANEL_BG, COLOR_PANEL_CARD, COLOR_PANEL_BORDER,
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_SUCCESS, COLOR_DANGER,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED
)

class Button:
    """Bouton interactif avec détection de survol (hover) et clic."""
    def __init__(self, rect, text, callback_id, bg_color=COLOR_PANEL_CARD, text_color=COLOR_TEXT_MAIN):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback_id = callback_id
        self.bg_color = bg_color
        self.text_color = text_color
        self.hovered = False

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

    def draw(self, screen, font):
        color = (min(self.bg_color[0] + 25, 255), min(self.bg_color[1] + 25, 255), min(self.bg_color[2] + 35, 255)) if self.hovered else self.bg_color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        pygame.draw.rect(screen, COLOR_PRIMARY if self.hovered else COLOR_PANEL_BORDER, self.rect, width=1, border_radius=6)
        
        lbl = font.render(self.text, True, COLOR_PRIMARY if self.hovered else self.text_color)
        lbl_rect = lbl.get_rect(center=self.rect.center)
        screen.blit(lbl, lbl_rect)

class UIPanel:
    """
    Panneau latéral d'analyse télémétrique, visualisation neuronale en direct,
    graphique de convergence dynamique et boutons interactifs.
    """
    def __init__(self, x=ARENA_WIDTH, y=0, width=PANEL_WIDTH, height=SCREEN_HEIGHT):
        self.rect = pygame.Rect(x, y, width, height)
        
        # Polices
        self.font_title = pygame.font.SysFont("Trebuchet MS", 18, bold=True)
        self.font_sub = pygame.font.SysFont("Arial", 11)
        self.font_bold = pygame.font.SysFont("Trebuchet MS", 13, bold=True)
        self.font_data = pygame.font.SysFont("Consolas", 12, bold=True)
        self.font_btn = pygame.font.SysFont("Trebuchet MS", 11, bold=True)
        
        # Initialisation des boutons
        self._init_buttons()

    def _init_buttons(self):
        bx = self.rect.x + 15
        bw = (self.rect.width - 40) // 2
        bh = 28
        y = 590
        
        self.buttons = [
            Button((bx, y, bw, bh), "▶ / ⏸ Pause", "toggle_pause", bg_color=(35, 45, 65)),
            Button((bx + bw + 10, y, bw, bh), "⚡ Vitesse : +", "speed_up", bg_color=(35, 45, 65)),
            Button((bx, y + 34, bw, bh), "👁 Radars (R)", "toggle_radar", bg_color=(35, 45, 65)),
            Button((bx + bw + 10, y + 34, bw, bh), "⏭ Sauter Gén.", "skip_gen", bg_color=(45, 40, 60)),
            Button((bx, y + 68, bw, bh), "💾 Sauver ADN", "save_dna", bg_color=(30, 50, 45)),
            Button((bx + bw + 10, y + 68, bw, bh), "📂 Charger Best", "load_dna", bg_color=(50, 45, 30)),
            Button((bx, y + 102, self.rect.width - 30, 32), "📄 Consulter le Rapport de Projet (F1)", "open_report", bg_color=(0, 110, 180), text_color=(255, 255, 255))
        ]

    def handle_mouse_move(self, mouse_pos):
        for btn in self.buttons:
            btn.check_hover(mouse_pos)

    def handle_mouse_click(self, mouse_pos):
        for btn in self.buttons:
            if btn.rect.collidepoint(mouse_pos):
                return btn.callback_id
        return None

    def draw(self, screen, ga, leader_car, generation, alive_count, total_count, all_time_best, is_paused, sim_speed, radar_mode):
        # 1. Fond du panneau
        pygame.draw.rect(screen, COLOR_PANEL_BG, self.rect)
        pygame.draw.line(screen, COLOR_PANEL_BORDER, (self.rect.x, 0), (self.rect.x, self.rect.height), 2)
        
        # 2. Header
        t_title = self.font_title.render("NEURO-TRACK : AG", True, COLOR_PRIMARY)
        t_sub = self.font_sub.render("Projet d'IA - Encadré par Mme Bouhajeb", True, COLOR_TEXT_MUTED)
        screen.blit(t_title, (self.rect.x + 15, 12))
        screen.blit(t_sub, (self.rect.x + 15, 34))

        # 3. Carte de Télémétrie Génétique
        self._draw_stats_card(screen, generation, alive_count, total_count, leader_car, all_time_best, is_paused, sim_speed)

        # 4. Moniteur du Réseau de Neurones en Direct (Visualiseur de cerveau)
        self._draw_neural_net_card(screen, leader_car)

        # 5. Graphique de Convergence en Direct (Fitness vs Générations)
        self._draw_live_fitness_chart(screen, ga.history)

        # 6. Boutons interactifs
        for btn in self.buttons:
            btn.draw(screen, self.font_btn)

    def _draw_stats_card(self, screen, generation, alive, total, leader, record_fitness, is_paused, speed):
        card = pygame.Rect(self.rect.x + 15, 54, self.rect.width - 30, 108)
        pygame.draw.rect(screen, COLOR_PANEL_CARD, card, border_radius=6)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, card, width=1, border_radius=6)
        
        # Phase d'apprentissage pédagogique
        if generation <= 3:
            stage_str = "Phase 1 : Exploration naïve (Chaos initial)"
            stage_col = COLOR_DANGER
        elif generation <= 8:
            stage_str = "Phase 2 : Négociation des virages"
            stage_col = COLOR_ACCENT
        else:
            stage_str = "Phase 3 : Trajectoires optimisées & laps"
            stage_col = COLOR_SUCCESS

        cur_fit = leader.fitness if leader else 0.0
        cur_cps = leader.checkpoints_passed if leader else 0

        lines = [
            (f"Génération    : {generation}", COLOR_TEXT_MAIN),
            (f"Survivants    : {alive} / {total} voitures", COLOR_PRIMARY if alive > 0 else COLOR_DANGER),
            (f"Fitness Actuel: {int(cur_fit)} pts  (Laps: {cur_cps})", COLOR_TEXT_MAIN),
            (f"Fitness Record: {int(record_fitness)} pts", COLOR_ACCENT),
            (f"Vitesse : {speed}x {'[EN PAUSE]' if is_paused else ''}", (180, 220, 255)),
        ]
        
        for idx, (txt, col) in enumerate(lines):
            screen.blit(self.font_data.render(txt, True, col), (card.x + 12, card.y + 8 + idx * 17))
            
        # Badge du stade
        badge = self.font_sub.render(stage_str, True, stage_col)
        screen.blit(badge, (card.x + 12, card.y + 92))

    def _draw_neural_net_card(self, screen, leader):
        """Affiche le cerveau du leader en temps réel (neurones actifs et synapses)."""
        card = pygame.Rect(self.rect.x + 15, 170, self.rect.width - 30, 220)
        pygame.draw.rect(screen, COLOR_PANEL_CARD, card, border_radius=6)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, card, width=1, border_radius=6)
        
        title = self.font_bold.render("Cerveau Artificiel en Direct (MLP)", True, COLOR_PRIMARY)
        screen.blit(title, (card.x + 12, card.y + 8))
        
        sub = self.font_sub.render("5 Capteurs  ->  8 Cachés  ->  1 Braquage", True, COLOR_TEXT_MUTED)
        screen.blit(sub, (card.x + 12, card.y + 24))

        if not leader:
            msg = self.font_sub.render("En attente de la nouvelle génération...", True, COLOR_TEXT_MUTED)
            screen.blit(msg, (card.x + 30, card.y + 110))
            return

        brain = leader.brain
        inputs = brain.last_inputs
        hidden = brain.last_hidden
        output = brain.last_output

        # Positions des neurones
        in_x = card.x + 40
        hid_x = card.x + card.width // 2
        out_x = card.x + card.width - 40

        in_ys = [card.y + 55 + i * 32 for i in range(5)]
        hid_ys = [card.y + 45 + i * 20 for i in range(8)]
        out_ys = [card.y + 125]

        # Dessin des synapses W1 (Input -> Hidden)
        for i in range(5):
            for h in range(8):
                weight = brain.w1[i][h]
                if abs(weight) > 0.4:
                    col = (0, 200, 255) if weight > 0 else (255, 80, 80)
                    alpha = min(200, int(abs(weight) * 90))
                    pygame.draw.line(screen, col, (in_x, in_ys[i]), (hid_x, hid_ys[h]), 1)

        # Dessin des synapses W2 (Hidden -> Output)
        for h in range(8):
            weight = brain.w2[h][0]
            if abs(weight) > 0.3:
                col = (0, 200, 255) if weight > 0 else (255, 80, 80)
                pygame.draw.line(screen, col, (hid_x, hid_ys[h]), (out_x, out_ys[0]), 1)

        # Neurones d'entrée (5)
        for i in range(5):
            val = float(inputs[i]) if i < len(inputs) else 0.5
            intensity = int(val * 255)
            node_col = (intensity, intensity, 100) # Vert/jaune selon proximité
            pygame.draw.circle(screen, node_col, (in_x, in_ys[i]), 7)
            pygame.draw.circle(screen, (255, 255, 255), (in_x, in_ys[i]), 7, 1)

        # Neurones cachés (8)
        for h in range(8):
            val = float(hidden[h]) if h < len(hidden) else 0.0
            act_col = (0, 180, 255) if val >= 0 else (255, 90, 90)
            pygame.draw.circle(screen, act_col, (hid_x, hid_ys[h]), 6)
            pygame.draw.circle(screen, (220, 220, 220), (hid_x, hid_ys[h]), 6, 1)

        # Neurone de sortie (1) : Braquage
        steer_col = COLOR_SUCCESS if abs(output) < 0.2 else (COLOR_PRIMARY if output < 0 else COLOR_ACCENT)
        pygame.draw.circle(screen, steer_col, (out_x, out_ys[0]), 10)
        pygame.draw.circle(screen, (255, 255, 255), (out_x, out_ys[0]), 10, 2)
        
        # Jauge de braquage en dessous
        action_text = "Tout droit" if abs(output) < 0.15 else ("Braque GAUCHE" if output > 0 else "Braque DROITE")
        lbl_action = self.font_sub.render(f"Sortie : {action_text} ({output:+.2f})", True, COLOR_TEXT_MAIN)
        screen.blit(lbl_action, (card.x + 15, card.y + 198))

    def _draw_live_fitness_chart(self, screen, history):
        """Tracé vectoriel direct du graphique Fitness vs Génération dans Pygame."""
        card = pygame.Rect(self.rect.x + 15, 398, self.rect.width - 30, 182)
        pygame.draw.rect(screen, COLOR_PANEL_CARD, card, border_radius=6)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, card, width=1, border_radius=6)
        
        title = self.font_bold.render("Courbe d'Apprentissage en Direct", True, COLOR_ACCENT)
        screen.blit(title, (card.x + 12, card.y + 6))
        
        # Zone du graphique
        gx = card.x + 36
        gy = card.y + 30
        gw = card.width - 48
        gh = card.height - 48

        # Cadre et grille
        pygame.draw.rect(screen, (20, 24, 32), (gx, gy, gw, gh))
        pygame.draw.line(screen, (60, 70, 85), (gx, gy + gh // 2), (gx + gw, gy + gh // 2), 1)

        if len(history) < 2:
            hint = self.font_sub.render("La courbe se dessinera dès la Génération 2...", True, COLOR_TEXT_MUTED)
            screen.blit(hint, (gx + 10, gy + gh // 2 - 8))
            return

        max_val = max(h["best_fitness"] for h in history)
        max_val = max(max_val, 1000.0)
        n = len(history)

        best_pts = []
        avg_pts = []
        for i, h in enumerate(history):
            px = int(gx + (i / (n - 1)) * gw)
            py_best = int(gy + gh - (h["best_fitness"] / max_val) * (gh - 10))
            py_avg = int(gy + gh - (h["avg_fitness"] / max_val) * (gh - 10))
            best_pts.append((px, py_best))
            avg_pts.append((px, py_avg))

        # Tracé des lignes
        if len(avg_pts) >= 2:
            pygame.draw.lines(screen, (230, 130, 40), False, avg_pts, 1)
        if len(best_pts) >= 2:
            pygame.draw.lines(screen, COLOR_PRIMARY, False, best_pts, 2)
            for pt in best_pts:
                pygame.draw.circle(screen, COLOR_PRIMARY, pt, 2)

        # Légende
        screen.blit(self.font_sub.render(f"Max: {int(max_val)}", True, COLOR_PRIMARY), (gx + 4, gy + 3))
        screen.blit(self.font_sub.render("Bleu: Max  Orange: Moyenne", True, COLOR_TEXT_MUTED), (gx + gw - 140, gy + gh + 4))
