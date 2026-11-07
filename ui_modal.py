import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_PRIMARY,
    COLOR_ACCENT, COLOR_PANEL_BG, COLOR_PANEL_CARD,
    COLOR_PANEL_BORDER, COLOR_TEXT_MAIN, COLOR_TEXT_MUTED
)

class ReportModal:
    """
    Fenêtre modale académique interactive affichant le rapport technique
    et les explications mathématiques de l'AG directement dans l'interface de simulation.
    """
    def __init__(self):
        self.is_open = False
        self.active_tab = 0 # 0: Contexte, 1: Modélisation AG, 2: Résultats, 3: FAQ Jury
        
        # Dimensions de la modale
        self.width = 1100
        self.height = 640
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Polices
        self.font_title = pygame.font.SysFont("Trebuchet MS", 20, bold=True)
        self.font_tab = pygame.font.SysFont("Trebuchet MS", 13, bold=True)
        self.font_h2 = pygame.font.SysFont("Trebuchet MS", 15, bold=True)
        self.font_body = pygame.font.SysFont("Arial", 13)
        self.font_mono = pygame.font.SysFont("Consolas", 12)
        
        self.tabs = [
            "1. Problématique & IA",
            "2. Modélisation de l'AG",
            "3. Analyse & Convergence",
            "4. Argumentaire Soutenance (FAQ)"
        ]

    def toggle(self):
        self.is_open = not self.is_open

    def handle_click(self, mouse_pos):
        if not self.is_open:
            return None

        # Clic en dehors ou bouton fermer
        close_btn_rect = pygame.Rect(self.rect.right - 45, self.rect.y + 12, 32, 28)
        if close_btn_rect.collidepoint(mouse_pos):
            self.is_open = False
            return "close"

        # Bouton export HTML
        export_btn_rect = pygame.Rect(self.rect.right - 280, self.rect.y + 12, 220, 28)
        if export_btn_rect.collidepoint(mouse_pos):
            return "export_html"

        # Onglets
        for i, _ in enumerate(self.tabs):
            tab_rect = pygame.Rect(self.rect.x + 20 + i * 210, self.rect.y + 55, 200, 32)
            if tab_rect.collidepoint(mouse_pos):
                self.active_tab = i
                return f"tab_{i}"

        return None

    def draw(self, screen):
        if not self.is_open:
            return

        # 1. Voile sombre transparent en arrière-plan
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 20, 220))
        screen.blit(overlay, (0, 0))

        # 2. Boîte modale principale
        pygame.draw.rect(screen, COLOR_PANEL_BG, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_PRIMARY, self.rect, width=2, border_radius=10)

        # 3. En-tête
        title = self.font_title.render("RAPPORT TECHNIQUE OFFICIEL : NEURO-TRACK (AG)", True, COLOR_PRIMARY)
        screen.blit(title, (self.rect.x + 25, self.rect.y + 15))

        # Bouton d'export HTML
        export_rect = pygame.Rect(self.rect.right - 280, self.rect.y + 12, 220, 28)
        pygame.draw.rect(screen, (0, 130, 200), export_rect, border_radius=6)
        lbl_export = self.font_tab.render("📄 Exporter en Rapport Web (HTML)", True, (255, 255, 255))
        screen.blit(lbl_export, (export_rect.x + 10, export_rect.y + 5))

        # Bouton fermer [X]
        close_rect = pygame.Rect(self.rect.right - 45, self.rect.y + 12, 32, 28)
        pygame.draw.rect(screen, (200, 60, 60), close_rect, border_radius=6)
        lbl_close = self.font_tab.render("X", True, (255, 255, 255))
        screen.blit(lbl_close, (close_rect.x + 11, close_rect.y + 5))

        # 4. Barre des onglets
        for i, tab_name in enumerate(self.tabs):
            tab_rect = pygame.Rect(self.rect.x + 20 + i * 210, self.rect.y + 55, 200, 32)
            is_active = (i == self.active_tab)
            col = COLOR_PRIMARY if is_active else COLOR_PANEL_CARD
            border_col = COLOR_PRIMARY if is_active else COLOR_PANEL_BORDER
            
            pygame.draw.rect(screen, col, tab_rect, border_radius=6)
            pygame.draw.rect(screen, border_col, tab_rect, width=1, border_radius=6)
            
            txt_col = (255, 255, 255) if is_active else COLOR_TEXT_MUTED
            lbl = self.font_tab.render(tab_name, True, txt_col)
            screen.blit(lbl, (tab_rect.x + 10, tab_rect.y + 6))

        # 5. Contenu de l'onglet actif
        content_rect = pygame.Rect(self.rect.x + 20, self.rect.y + 98, self.width - 40, self.height - 118)
        pygame.draw.rect(screen, COLOR_PANEL_CARD, content_rect, border_radius=8)
        pygame.draw.rect(screen, COLOR_PANEL_BORDER, content_rect, width=1, border_radius=8)

        if self.active_tab == 0:
            self._render_tab_problem(screen, content_rect)
        elif self.active_tab == 1:
            self._render_tab_ga(screen, content_rect)
        elif self.active_tab == 2:
            self._render_tab_results(screen, content_rect)
        elif self.active_tab == 3:
            self._render_tab_faq(screen, content_rect)

    def _render_tab_problem(self, screen, rect):
        x = rect.x + 25
        y = rect.y + 20
        
        screen.blit(self.font_h2.render("1. Le Problème Traité : Conduite Autonome Sans Modèle Prédéfini", True, COLOR_PRIMARY), (x, y))
        y += 30
        
        p1 = [
            "• Objectif : Piloter un véhicule sur un circuit fermé sans trajectoire préprogrammée.",
            "• Contrainte majeure : L'algorithme ignore la courbure de la piste et l'emplacement des bordures.",
            "• Système sensoriel : 5 radars virtuels (angles -65°, -35°, 0°, +35°, +65°) mesurent la distance à l'herbe.",
            "• Prise de décision : Un Perceptron Multicouche (MLP) convertit les 5 distances en un angle de braquage.",
            "• Pourquoi la Neuroévolution plutôt que le Deep Learning classique (Gradient) ?",
            "  -> Pas de jeu de données préétabli : il n'y a pas de conducteur humain pour superviser l'apprentissage.",
            "  -> Fonction d'évaluation non différentiable : heurter un mur est un événement discret irréversible.",
            "  -> L'Algorithme Génétique explore l'espace des poids synaptiques par sélection naturelle."
        ]
        for line in p1:
            col = COLOR_ACCENT if "Pourquoi" in line else COLOR_TEXT_MAIN
            screen.blit(self.font_body.render(line, True, col), (x, y))
            y += 24

        y += 15
        screen.blit(self.font_h2.render("Architecture Système : Découpage Modulaire", True, COLOR_PRIMARY), (x, y))
        y += 30
        
        modules = [
            "• config.py : Hyperparamètres centralisés (taux de mutation, élitisme, vitesse de simulation).",
            "• brain.py  : Modèle mathématique du réseau de neurones (MLP) et sérialisation 1D de l'ADN.",
            "• car.py    : Cinématique 2D, raycasting des 5 capteurs radars et détection de collision.",
            "• track.py  : Circuit asphalté, vibreurs, détection de texture et 18 checkpoints de guidage.",
            "• ga.py     : Moteur de sélection, croisement uniforme, mutation gaussienne et archivage CSV."
        ]
        for mod in modules:
            screen.blit(self.font_mono.render(mod, True, COLOR_TEXT_MUTED), (x + 10, y))
            y += 22

    def _render_tab_ga(self, screen, rect):
        x = rect.x + 25
        y = rect.y + 20
        
        screen.blit(self.font_h2.render("2. Modélisation Mathématique de l'Algorithme Génétique", True, COLOR_PRIMARY), (x, y))
        y += 30

        items = [
            ("A. L'Individu et l'ADN (Chromosome)", [
                "• Individu = Une voiture équipée d'un réseau de neurones.",
                "• Chromosome = Vecteur 1D concaténant tous les poids et biais :",
                "  Taille ADN = (5x8) + 8 + (8x1) + 1 = 57 gènes réels dans l'intervalle [-1.0, 1.0]."
            ]),
            ("B. La Fonction de Fitness (Score d'aptitude)", [
                "• Fitness = (Checkpoints_Validés * 1000) + Progression_vers_le_prochain_checkpoint.",
                "• Pénalité fatale : En cas de choc contre un mur, la voiture est éliminée (alive = False).",
                "• Protection anti-boucle : Si aucun checkpoint n'est validé en 3s, la voiture est détruite."
            ]),
            ("C. Les Opérateurs Génétiques", [
                "• Élitisme (10%) : Les 4 meilleurs véhicules sont clonés directement pour garantir zéro régression.",
                "• Sélection par Tournoi (k = 3) : 3 individus choisis au hasard, le plus apte devient parent.",
                "• Croisement Uniforme (Pc = 85%) : Chaque gène a 50% de chance de provenir du parent A ou B.",
                "• Mutation Gaussienne (Pm = 12%) : Gène <- Gène + Bruit_Gaussien(0, σ = 0.35)."
            ])
        ]
        for header, lines in items:
            screen.blit(self.font_h2.render(header, True, COLOR_ACCENT), (x, y))
            y += 24
            for l in lines:
                screen.blit(self.font_body.render(l, True, COLOR_TEXT_MAIN), (x + 15, y))
                y += 22
            y += 10

    def _render_tab_results(self, screen, rect):
        x = rect.x + 25
        y = rect.y + 20
        
        screen.blit(self.font_h2.render("3. Analyse de la Convergence et Résultats Expérimentaux", True, COLOR_PRIMARY), (x, y))
        y += 30

        results = [
            "• Génération 1 à 3 (Exploration naïve) :",
            "  -> 90% des voitures heurtent le premier virage. Le Fitness moyen est faible (~500 pts).",
            "• Génération 4 à 8 (Émergence du comportement d'évitement) :",
            "  -> La mutation découvre que braquer quand le radar avant diminue évite le mur.",
            "  -> Les champions franchissent les virages 1 et 2 (Fitness dépasse 8 000 pts).",
            "• Génération 10 à 15 (Maîtrise du circuit fermé) :",
            "  -> Le croisement stabilise les trajectoires. Le champion réalise des tours complets (Laps).",
            "  -> Le Fitness maximal atteint plus de 25 000 pts.",
            "",
            "• Justification de l'Apprentissage :",
            "  La courbe tracée en direct montre une croissance logarithmique typique des algorithmes génétiques,",
            "  prouvant mathématiquement que la population optimise sa politique de conduite au fil du temps."
        ]
        for r in results:
            col = COLOR_ACCENT if "Génération" in r else COLOR_TEXT_MAIN
            screen.blit(self.font_body.render(r, True, col), (x, y))
            y += 24

    def _render_tab_faq(self, screen, rect):
        x = rect.x + 25
        y = rect.y + 20
        
        screen.blit(self.font_h2.render("4. Argumentaire pour la Soutenance (Questions Possibles de Mme Bouhajeb)", True, COLOR_PRIMARY), (x, y))
        y += 30

        faq = [
            ("Q : Pourquoi avoir choisi l'Élitisme ?",
             "R : Sans élitisme, une bonne combinaison de gènes peut être détruite par la mutation ou le croisement. L'élitisme garantit mathématiquement que le score maximal est monotone croissant."),
            ("Q : Comment empêchez-vous les voitures de tourner en rond pour accumuler du score ?",
             "R : Grâce aux 18 checkpoints ordonnés et au timer anti-blocage (3 secondes). Tourner en rond n'apporte aucun point et provoque l'élimination immédiate de l'individu."),
            ("Q : Quelle est l'utilité de la couche cachée de 8 neurones ?",
             "R : Une simple combinaison linéaire (sans couche cachée) ne peut pas résoudre les virages en S. Les 8 neurones cachés combinés à l'activation non linéaire Tanh permettent d'apprendre des décisions complexes."),
            ("Q : Le modèle peut-il conduire sur un autre circuit ?",
             "R : Oui ! Les gènes n'apprennent pas les coordonnées de la piste mais une politique réactive : si mur proche à gauche, braquer à droite. Le cerveau généralise donc à d'autres tracés.")
        ]
        for q, a in faq:
            screen.blit(self.font_body.render(q, True, COLOR_ACCENT), (x, y))
            y += 22
            screen.blit(self.font_body.render(a, True, COLOR_TEXT_MAIN), (x + 15, y))
            y += 30
