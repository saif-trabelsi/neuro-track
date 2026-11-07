import pygame
import math
from config import (
    ARENA_WIDTH, SCREEN_HEIGHT, COLOR_GRASS, COLOR_ROAD,
    COLOR_BORDER, COLOR_MIDLINE, COLOR_START_LINE
)

class Track:
    """
    Gestionnaire du circuit : rendu visuel, masques de collision et checkpoints.
    Conçu pour s'intégrer harmonieusement à gauche du panneau de bord.
    """
    def __init__(self, width=ARENA_WIDTH, height=SCREEN_HEIGHT):
        self.width = width
        self.height = height
        
        # Dimensions géométriques de la piste
        self.outer_rect = pygame.Rect(70, 70, self.width - 140, self.height - 140)
        self.inner_rect = pygame.Rect(240, 230, self.width - 480, self.height - 460)
        self.outer_radius = 160
        self.inner_radius = 90
        
        # Position et direction de départ (ligne droite gauche, orienté vers le haut)
        self.start_x = 155
        self.start_y = 500
        self.start_angle = 90.0 # Vers le haut (Nord)
        
        # 18 Checkpoints ordonnés pour guider l'Algorithme Génétique
        self.checkpoints = [
            (155, 500), # 0: Ligne de départ
            (155, 380), # 1: Montée gauche
            (155, 250), # 2: Approche virage 1
            (205, 155), # 3: Virage 1
            (300, 115), # 4: Sortie virage 1
            (470, 115), # 5: Ligne droite haute
            (640, 115), # 6: Milieu ligne haute
            (810, 115), # 7: Fin ligne haute
            (915, 170), # 8: Entrée virage 2
            (945, 275), # 9: Descente droite
            (945, 410), # 10: Milieu descente droite
            (945, 520), # 11: Fin descente droite
            (895, 615), # 12: Entrée virage 3
            (780, 650), # 13: Sortie virage 3
            (600, 650), # 14: Ligne droite basse
            (420, 650), # 15: Milieu ligne basse
            (280, 640), # 16: Entrée virage 4
            (200, 580)  # 17: Sortie virage 4 vers l'arrivée
        ]
        
        self.surface = self._build_track_surface()
        
    def _build_track_surface(self):
        surface = pygame.Surface((self.width, self.height))
        # 1. Fond herbe (obstacle hors-piste)
        surface.fill(COLOR_GRASS)
        
        # 2. Vibreur extérieur blanc
        pygame.draw.rect(surface, COLOR_BORDER, self.outer_rect.inflate(8, 8), border_radius=self.outer_radius + 4)
        
        # 3. Piste asphaltée
        pygame.draw.rect(surface, COLOR_ROAD, self.outer_rect, border_radius=self.outer_radius)
        
        # 4. Vibreur intérieur blanc
        pygame.draw.rect(surface, COLOR_BORDER, self.inner_rect.inflate(8, 8), border_radius=self.inner_radius + 4)
        
        # 5. Herbe centrale (îlot intérieur)
        pygame.draw.rect(surface, COLOR_GRASS, self.inner_rect, border_radius=self.inner_radius)
        
        # 6. Ligne médiane stylisée
        mid_rect = pygame.Rect(155, 150, self.width - 310, self.height - 300)
        pygame.draw.rect(surface, COLOR_MIDLINE, mid_rect, width=2, border_radius=125)
        
        # 7. Damier sur la ligne de départ
        self._draw_finish_line(surface)
        
        return surface

    def _draw_finish_line(self, surface):
        """Damier racing officiel sur la ligne de départ."""
        start_x = 70
        end_x = 240
        y = self.start_y
        tile_size = 10
        for x in range(start_x, end_x, tile_size):
            for dy in range(-10, 10, tile_size):
                col = COLOR_START_LINE if ((x // tile_size) + (dy // tile_size)) % 2 == 0 else (25, 28, 35)
                pygame.draw.rect(surface, col, (x, y + dy, tile_size, tile_size))

    def is_on_road(self, x, y):
        """Vérifie si un point (x, y) est sur la piste asphaltée."""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.surface.get_at((int(x), int(y)))[:3] != COLOR_GRASS

    def draw(self, screen, show_checkpoints=False):
        screen.blit(self.surface, (0, 0))
        if show_checkpoints:
            for idx, (cx, cy) in enumerate(self.checkpoints):
                pygame.draw.circle(screen, (255, 215, 0), (cx, cy), 6, 2)
                ncx, ncy = self.checkpoints[(idx + 1) % len(self.checkpoints)]
                pygame.draw.line(screen, (90, 180, 90), (cx, cy), (ncx, ncy), 1)
