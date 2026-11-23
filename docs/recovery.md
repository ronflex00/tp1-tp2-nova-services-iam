# Récupération MFA

## Facteurs

- TOTP : facteur principal généré par une application d'authentification.
- Static Tokens : facteurs de secours à usage contrôlé et unique.
- Aucun vrai code, QR code ou secret TOTP n'est écrit dans Git.

## Procédure contrôlée

1. Vérifier l'identité par un canal hors bande.
2. Vérifier les sessions actives et révoquer les sessions suspectes.
3. Utiliser un facteur de secours validé et à usage unique.
4. Révoquer le périphérique perdu dans Authentik.
5. Enrôler un nouveau périphérique TOTP.
6. Révoquer les anciens facteurs et renouveler les recovery codes.
7. Vérifier une nouvelle connexion et consigner uniquement l'action, jamais le code.

## Mesures à ne pas automatiser

Le seed TOTP, le QR code, les recovery codes et les cookies de session ne doivent être ni lus, ni générés, ni stockés par les tests Playwright. Le MFA reste une intervention humaine.
