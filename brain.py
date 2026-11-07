import numpy as np

class Brain:
    """
    Réseau de neurones artificiels (Perceptron multicouche - MLP)
    servant de système de décision embarqué dans chaque véhicule.
    
    Architecture :
    - 5 neurones d'entrée (capteurs de distance normalisés)
    - 8 neurones cachés (activation Tanh)
    - 1 neurone de sortie (activation Tanh : -1.0 braquage gauche, +1.0 braquage droite)
    """
    def __init__(self, input_size=5, hidden_size=8, output_size=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Poids et biais initialisés selon une distribution gaussienne normalisée
        self.w1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((hidden_size,))
        self.w2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((output_size,))

        # Mémoire des dernières activations pour la visualisation en temps réel dans l'UI
        self.last_inputs = np.zeros(input_size)
        self.last_hidden = np.zeros(hidden_size)
        self.last_output = 0.0

    def forward(self, inputs):
        """Propagation avant avec enregistrement des activations pour le moniteur visuel."""
        self.last_inputs = np.array(inputs, dtype=float)
        
        # Couche cachée
        z1 = np.dot(self.last_inputs, self.w1) + self.b1
        self.last_hidden = np.tanh(z1)
        
        # Couche de sortie
        z2 = np.dot(self.last_hidden, self.w2) + self.b2
        output = np.tanh(z2)
        self.last_output = float(output[0])
        
        return self.last_output

    def get_dna(self):
        """Sérialise tous les poids et biais en un vecteur 1D de 57 gènes réels."""
        return np.concatenate([
            self.w1.flatten(),
            self.b1.flatten(),
            self.w2.flatten(),
            self.b2.flatten()
        ])

    def set_dna(self, dna):
        """Désérialise un chromosome 1D pour restaurer l'état synaptique du cerveau."""
        idx = 0
        w1_size = self.input_size * self.hidden_size
        self.w1 = dna[idx:idx + w1_size].reshape((self.input_size, self.hidden_size))
        idx += w1_size

        b1_size = self.hidden_size
        self.b1 = dna[idx:idx + b1_size].reshape((self.hidden_size,))
        idx += b1_size

        w2_size = self.hidden_size * self.output_size
        self.w2 = dna[idx:idx + w2_size].reshape((self.hidden_size, self.output_size))
        idx += w2_size

        b2_size = self.output_size
        self.b2 = dna[idx:idx + b2_size].reshape((self.output_size,))

    def copy(self):
        clone = Brain(self.input_size, self.hidden_size, self.output_size)
        clone.set_dna(self.get_dna().copy())
        return clone
