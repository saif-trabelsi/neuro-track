# Configuration du projet Neuro-Track (Algorithmes Génétiques & Neuroévolution)

# Dimensions de l'application (Arène + Dashboard Télémétrie)
ARENA_WIDTH = 1040                  # Largeur de la zone de course
PANEL_WIDTH = 400                   # Largeur du panneau latéral d'analyse
SCREEN_WIDTH = ARENA_WIDTH + PANEL_WIDTH  # 1440 px
SCREEN_HEIGHT = 760                 # Hauteur générale

FPS = 60

# Palette de couleurs moderne (UI & Télémétrie)
COLOR_BG_DARK = (15, 18, 24)
COLOR_PANEL_BG = (22, 27, 36)
COLOR_PANEL_CARD = (30, 36, 48)
COLOR_PANEL_BORDER = (45, 55, 72)
COLOR_PRIMARY = (0, 190, 255)       # Cyan électrique
COLOR_ACCENT = (255, 180, 0)        # Or / Jaune Champion
COLOR_SUCCESS = (46, 204, 113)      # Vert validation
COLOR_DANGER = (231, 76, 60)        # Rouge collision
COLOR_TEXT_MAIN = (240, 245, 250)
COLOR_TEXT_MUTED = (140, 155, 175)

# Couleurs du circuit
COLOR_GRASS = (24, 48, 32)          # Obstacle hors-piste
COLOR_ROAD = (60, 64, 72)           # Asphalte
COLOR_BORDER = (225, 230, 240)      # Liseré de délimitation
COLOR_MIDLINE = (85, 92, 105)       # Ligne de trajectoire médiane
COLOR_START_LINE = (255, 255, 255)

# Hyperparamètres Voitures
CAR_WIDTH = 26
CAR_HEIGHT = 14
CAR_SPEED = 5.5
MAX_STEER_ANGLE = 5.0
SENSOR_ANGLES = [-65, -35, 0, 35, 65]
SENSOR_MAX_LENGTH = 175
SENSOR_STEP = 4
MAX_FRAMES_STALL = 180              # 3 secondes max sans checkpoint (anti-boucle)

# Hyperparamètres de l'Algorithme Génétique
POPULATION_SIZE = 40
ELITISM_COUNT = 4                   # Top 10% champions préservés
MUTATION_RATE = 0.12                # Probabilité de mutation par gène
MUTATION_SCALE = 0.35               # Écart-type du bruit gaussien
CROSSOVER_RATE = 0.85               # Probabilité de croisement uniforme

# Architecture du Réseau de Neurones (MLP)
NN_INPUT_SIZE = len(SENSOR_ANGLES)  # 5 neurones d'entrée (radars)
NN_HIDDEN_SIZE = 8                  # 8 neurones cachés
NN_OUTPUT_SIZE = 1                  # 1 neurone de sortie (braquage)
