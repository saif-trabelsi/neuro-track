import pygame
import math
import numpy as np
from brain import Brain
from config import (
    CAR_WIDTH, CAR_HEIGHT, CAR_SPEED, MAX_STEER_ANGLE,
    SENSOR_ANGLES, SENSOR_MAX_LENGTH, SENSOR_STEP,
    MAX_FRAMES_STALL, NN_INPUT_SIZE, NN_HIDDEN_SIZE, NN_OUTPUT_SIZE,
    COLOR_PRIMARY, COLOR_ACCENT
)

class Car:
    """
    Véhicule autonome guidé par réseau de neurones et évalué par Fitness.
    """
    def __init__(self, x, y, angle=90.0):
        self.x = float(x)
        self.y = float(y)
        self.angle = float(angle)
        self.speed = CAR_SPEED
        self.alive = True
        
        # Réseau de neurones embarqué
        self.brain = Brain(NN_INPUT_SIZE, NN_HIDDEN_SIZE, NN_OUTPUT_SIZE)
        
        # Radars
        self.sensor_endpoints = []
        self.sensor_distances = np.ones(len(SENSOR_ANGLES), dtype=float)
        
        # Télémétrie et Fitness
        self.checkpoint_index = 1
        self.checkpoints_passed = 0
        self.fitness = 0.0
        self.stall_timer = 0
        self.total_frames = 0
        
        self.color = COLOR_PRIMARY
        self.is_champion = False

    def get_corner_points(self):
        """Retourne les 4 sommets du véhicule pour la détection précise de collision."""
        rad = math.radians(self.angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        hl = CAR_WIDTH / 2.0
        hw = CAR_HEIGHT / 2.0
        
        # Vecteur avant et vecteur transversal
        fx, fy = hl * cos_a, -hl * sin_a
        lx, ly = -hw * sin_a, -hw * cos_a
        
        return [
            (self.x + fx + lx, self.y + fy + ly), # Avant gauche
            (self.x + fx - lx, self.y + fy - ly), # Avant droit
            (self.x - fx + lx, self.y - fy + ly), # Arrière gauche
            (self.x - fx - lx, self.y - fy - ly)  # Arrière droit
        ]

    def update(self, track):
        """Met à jour les capteurs, l'inférence neuronale et la position."""
        if not self.alive:
            return

        self.total_frames += 1
        self.stall_timer += 1
        
        # 1. Perception radar
        self._cast_sensors(track)
        
        # 2. Prise de décision (Forward pass)
        steer_decision = self.brain.forward(self.sensor_distances)
        
        # 3. Braquage et cinématique
        self.angle += steer_decision * MAX_STEER_ANGLE
        self.angle %= 360.0
        
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += -math.sin(rad) * self.speed
        
        # 4. Checkpoints & Fitness
        self._check_checkpoints(track)
        self._compute_fitness(track)
        
        # 5. Collision avec l'herbe
        self._check_collision(track)
        
        # 6. Anti-blocage (si la voiture tourne en rond ou ne progresse plus)
        if self.stall_timer > MAX_FRAMES_STALL:
            self.alive = False

    def _cast_sensors(self, track):
        """Projections des rayons de détection d'obstacles (Raycasting)."""
        self.sensor_endpoints.clear()
        
        for i, delta_deg in enumerate(SENSOR_ANGLES):
            ray_angle = math.radians(self.angle + delta_deg)
            cos_r = math.cos(ray_angle)
            sin_r = -math.sin(ray_angle)
            
            dist = float(SENSOR_MAX_LENGTH)
            hit_x = self.x + cos_r * SENSOR_MAX_LENGTH
            hit_y = self.y + sin_r * SENSOR_MAX_LENGTH
            
            for d in range(8, SENSOR_MAX_LENGTH + 1, SENSOR_STEP):
                test_x = self.x + cos_r * d
                test_y = self.y + sin_r * d
                
                if not track.is_on_road(test_x, test_y):
                    dist = float(d)
                    hit_x = test_x
                    hit_y = test_y
                    break
                    
            self.sensor_endpoints.append((int(hit_x), int(hit_y)))
            self.sensor_distances[i] = dist / SENSOR_MAX_LENGTH

    def _check_checkpoints(self, track):
        """Valide le passage du checkpoint ciblé."""
        target_cp = track.checkpoints[self.checkpoint_index]
        dist_sq = (self.x - target_cp[0]) ** 2 + (self.y - target_cp[1]) ** 2
        
        if dist_sq < (75 ** 2):
            self.checkpoints_passed += 1
            self.checkpoint_index = (self.checkpoint_index + 1) % len(track.checkpoints)
            self.stall_timer = 0

    def _compute_fitness(self, track):
        """Calcul continu du score de Fitness."""
        target_cp = track.checkpoints[self.checkpoint_index]
        prev_idx = (self.checkpoint_index - 1) % len(track.checkpoints)
        prev_cp = track.checkpoints[prev_idx]
        
        seg_dist = math.hypot(target_cp[0] - prev_cp[0], target_cp[1] - prev_cp[1])
        cur_dist = math.hypot(target_cp[0] - self.x, target_cp[1] - self.y)
        progress = max(0.0, seg_dist - cur_dist)
        
        self.fitness = (self.checkpoints_passed * 1000.0) + progress

    def _check_collision(self, track):
        """Détection de sortie de piste."""
        for cx, cy in self.get_corner_points():
            if not track.is_on_road(cx, cy):
                self.alive = False
                return

    def draw(self, screen, draw_radars=False):
        """Rendu graphique du véhicule."""
        if not self.alive:
            return

        # Faisceaux radars
        if draw_radars:
            for end_x, end_y in self.sensor_endpoints:
                pygame.draw.line(screen, (0, 240, 150), (int(self.x), int(self.y)), (end_x, end_y), 1)
                pygame.draw.circle(screen, (255, 65, 65), (end_x, end_y), 3)

        # Châssis
        body = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        car_color = COLOR_ACCENT if self.is_champion else self.color
        pygame.draw.rect(body, car_color, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=3)
        
        # Pare-brise et détails visuels
        pygame.draw.rect(body, (20, 24, 30), (CAR_WIDTH - 9, 2, 4, CAR_HEIGHT - 4), border_radius=1)
        pygame.draw.circle(body, (255, 255, 220), (CAR_WIDTH - 2, 3), 2)
        pygame.draw.circle(body, (255, 255, 220), (CAR_WIDTH - 2, CAR_HEIGHT - 3), 2)

        # Rotation
        rotated_surf = pygame.transform.rotate(body, self.angle)
        rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surf, rect.topleft)
