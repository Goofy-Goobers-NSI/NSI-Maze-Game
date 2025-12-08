# Structure du projet final

nsi-maze-game/

- src/
Contient tout le code source.

    - __init__.py – permet à Python de reconnaître le dossier comme un package

    - cell.py – définit une cellule du labyrinthe (murs, position, etc...)

    - maze.py – gère la génération du labyrinthe (algorithme de Wilson)

    - player.py – gère les déplacements et les contrôles du joueur

    - game.py – fichier principal qui exécute le jeu et relie tous les éléments

    - textures/ Dossier pour les images, et autres éléments visuels.

- README.md - Description générale du projet et instructions d’installation

- BEST_PRACTICES.md - Bonnes pratiques d’organisation de l’équipe

- requirements.txt - Liste des dépendances (pygame-ce, etc...)

## Programmation
- Ajouter des commentaires pour expliquer votre code (en Anglais ou en Français)

- La branche "main" est la version stable qui devrait lancer sans bug 

    - Pour effectuer des changements dans "main" eviter de coder directement, créez votre propre branche pour des changements complexes

- Avant de coder, verifier que vos fichiers sont a jours, dans le terminale utiliser cette commande: 
    - git pull origin main

- Pour creer une branche faite:
    - git checkout -b feature/<nom-de-votre-fonctionnalité>
- Tester votre code dans vos branche
- Garder une tache par branche pour eviter de vous confondre
- Pour ajoutez et validez vos modifications:
    - git add .
    - git commit -m "Décrivez clairement ce que vous avez fait"

- Si vous ne comprenez pas quelque chose, n'hésitez pas à poser des questions ; j'aimerais éviter de détruire le projet (par accident).