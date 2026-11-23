# Récupération MFA

Préparer des Static tokens / Recovery codes pour l'administrateur Authentik et Charlie. Aucun code réel, QR code ou secret TOTP ne doit apparaître dans Git, les captures ou ce document.

Procédure en cas de perte du téléphone :

1. Vérifier l'identité de la personne par un canal hors bande.
2. Contrôler les sessions actives et révoquer celles qui sont suspectes.
3. Utiliser un facteur de secours à usage unique, selon la procédure validée.
4. Révoquer l'ancien périphérique MFA.
5. Enrôler un nouveau périphérique TOTP.
6. Renouveler les codes de récupération et détruire l'ancienne liste.
7. Vérifier une nouvelle connexion et consigner l'opération sans secret.

