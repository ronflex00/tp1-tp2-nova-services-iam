# Test de persistance

À réaliser après l'initialisation manuelle d'Authentik :

1. Créer `tp1-persistence` dans Directory → Groups, sans membre ni superuser.
2. Prendre la capture avant redémarrage.
3. Exécuter `docker compose down` (sans `-v`).
4. Exécuter `docker compose up -d --wait --wait-timeout 600`.
5. Vérifier `akadmin`, le groupe et l'API Grafana.
6. Prendre la capture après redémarrage, puis supprimer uniquement le groupe.

Un conteneur est une instance exécutable remplaçable ; un volume conserve les données hors du conteneur. La persistance permet de retrouver des données après recréation des conteneurs, mais ne remplace pas une sauvegarde : il faut encore copier et restaurer les volumes et les éléments de configuration/secrets de façon contrôlée.

Résultat de recette du 25 novembre 2026 : volumes et montages contrôlés présents. Le cycle avant/après n'a pas été relancé pour le rendu et aucune paire de captures n'est disponible. Statut : PARTIAL. Cette procédure reste indicative ; ne pas la relancer pour reconstituer une preuve historique.

