# Réponses aux questions du TP

1. Un fournisseur d'identité centralise l'identité, la connexion et la fédération pour éviter de gérer des comptes séparés dans chaque application.
2. L'authentification vérifie qui est l'utilisateur ; l'autorisation détermine ce qu'il peut faire ou consulter.
3. Le serveur traite les requêtes web et l'interface IAM ; le worker exécute les tâches asynchrones. Ils partagent la clé Authentik et la base.
4. Les ports sont propres à chaque espace réseau de conteneur. Deux applications peuvent donc écouter sur 3000 à l'intérieur, mais les ports publiés sur l'hôte doivent être distincts. Ici Grafana utilise 3000 ; la question vient de la version originale avec Gitea.
5. PostgreSQL ne doit pas être exposé sur le poste : il n'est consommé que par Authentik sur le réseau Docker, ce qui réduit la surface d'attaque.
6. `.env` contient les valeurs locales et sensibles ; `.env.example` documente uniquement les noms ; un gestionnaire de secrets fournit stockage, contrôle d'accès, rotation et audit adaptés à un environnement réel.
7. La même clé Authentik doit rester stable pour relire les données chiffrées et conserver la cohérence après redémarrage.
8. Une configuration Compose valide prouve seulement que le YAML et les variables sont acceptables ; elle ne prouve ni le téléchargement des images, ni la santé des dépendances, ni le fonctionnement applicatif.
9. La persistance conserve des données après recréation ; une sauvegarde est une copie récupérable, idéalement testée et stockée séparément.
10. Tester Grafana avec une connexion locale confirme que Grafana, sa base et son compte fonctionnent avant d'ajouter la complexité du SSO.
11. Le socket Docker donne un pouvoir important sur l'hôte. Un outil IAM n'en a pas besoin ici ; le monter augmente inutilement l'impact d'une compromission.
12. Pour une restauration complète, préserver les volumes PostgreSQL et Grafana, les fichiers Authentik, les secrets/clé Authentik, la configuration Compose, les certificats éventuels et une procédure de restauration testée.

Question originale liée au test Gitea / Git : question non applicable dans notre réalisation, Gitea n'ayant pas été retenu. Aucun test Gitea n'est déclaré.

