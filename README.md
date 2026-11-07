# Neuro-Track : Conduite Autonome par Algorithmes Génétiques (Neuroévolution)

Projet d'Ingénierie Logiciel (3ème année) présenté à **Madame Bouhajeb**.  
Auteur : **Saifeddine TRABELSI**

---

## 🌟 Points Forts du Projet & Valeur Ajoutée Académique

Ce projet a été conçu selon les standards les plus exigeants pour garantir la note maximale :
1. **Démonstration Visuelle Spectaculaire (Effet "Waouh") :**
   - **Visualiseur du Cerveau en Direct :** Les 5 neurones d'entrée, 8 neurones cachés et le neurone de braquage s'allument en temps réel dans l'interface, avec les synapses colorées (vert/cyan pour les poids positifs, rouge pour les poids négatifs).
   - **Courbe d'Apprentissage Directe dans l'UI :** Un graphique vectoriel dynamique s'actualise génération par génération directement dans la barre latérale.
   - **Faisceaux Radars :** Visualisation des 5 rayons de raycasting qui sondent les bordures de la piste.
2. **Interface Utilisateur Moderne & Ergonomique :**
   - Panneau de contrôle interactif avec boutons cliquables à la souris (Pause, Accélération jusqu'à 16x, Radars, Saut de génération, Sauvegarde).
3. **Rapport Académique Intégré dans l'UI (Touche `F1`) :**
   - Une fenêtre modale en 4 onglets résume le problème, la modélisation mathématique du chromosome, la fonction de fitness et les réponses aux questions pièges du jury.
   - Un bouton permet d'exporter d'un clic le rapport web haute définition (`rapport_neurotrack.html`) prêt à être imprimé en PDF.
4. **Sécurité Anti-Bug le Jour J ("Safety Demo") :**
   - Un modèle pré-entraîné (`best_brain.json`) est inclus. Un simple clic sur `[Charger Best]` ou la touche `L` injecte un champion capable d'enchaîner plusieurs tours sans aucune sortie de piste.

---

## 📁 Architecture du Code Source

```text
emna/
│
├── config.py              # Hyperparamètres centralisés (écran 1440x760, mutation, vitesses, radars)
├── brain.py               # Réseau de neurones artificiels (MLP, activations en direct, ADN 1D)
├── car.py                 # Moteur cinématique 2D, raycasting des capteurs, calcul de Fitness continu
├── track.py               # Circuit fermé de Grand Prix (asphalte, vibreurs) et 18 checkpoints ordonnés
├── ga.py                  # Moteur génétique : sélection par tournoi (k=3), crossover uniforme, mutation, élitisme
├── ui_panel.py            # Dashboard latéral de télémétrie, moniteur neuronal et boutons cliquables
├── ui_modal.py            # Modale académique interactive en 4 onglets (Rapport intégré dans la simulation)
├── plot_results.py        # Traceur de la courbe d'apprentissage haute résolution (PNG)
├── export_report.py       # Générateur du rapport officiel en HTML/PDF prêt à l'impression
├── main.py                # Boucle principale interactive Pygame
├── best_brain.json        # Poids synaptiques du champion pré-entraîné (> 56 000 pts de Fitness)
├── metrics.csv            # Historique de convergence des générations
├── fitness_evolution.png  # Graphique de convergence officiel
└── rapport_neurotrack.html# Rapport web officiel prêt à être présenté
```

---

## 🚀 Lancement Rapide

```bash
# Lancer la simulation interactive
python main.py
```

---

## 🎮 Commandes Interactives (Souris & Clavier)

Vous pouvez tout contrôler **directement à la souris** via les boutons du panneau droit, ou avec ces raccourcis :

| Commande | Action | Utilisation recommandée lors de la soutenance |
| :--- | :--- | :--- |
| **`F1` / Clic [Rapport]** | **Ouvrir le Rapport dans l'UI** | Présentez le formalisme mathématique directement depuis la simulation devant Mme Bouhajeb |
| **`ESPACE` / Clic [Pause]** | **Mettre en Pause / Reprendre** | Figez l'action dans un virage serré pour montrer comment les radars et le réseau réagissent |
| **`FLECHE HAUT` / `+`** | **Accélérer ($2\times, 4\times, 8\times, 16\times$)** | Faites défiler 10 générations en 15 secondes pour prouver la vitesse d'apprentissage |
| **`FLECHE BAS` / `-`** | **Ralentir la simulation** | Repassez à $1\times$ pour observer la finesse de pilotage |
| **`R` / Clic [Radars]** | **Basculer le mode Radars** | Masqué / Leader uniquement / Toute la flotte |
| **`L` / Clic [Charger Best]** | **Démonstration Parfaite** | Charge instantanément le génome champion capable de boucler des tours parfaits |
| **`S` / Clic [Sauver ADN]** | **Sauvegarder l'élite** | Enregistre le meilleur individu dans `best_brain.json` |
| **`P`** | **Générer Graphique PNG** | Génère immédiatement `fitness_evolution.png` |
