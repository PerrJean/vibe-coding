# Contrat : <projet>

Cent lignes au plus. Au-delà, découper en plusieurs outils qui se passent des fichiers.

## Entrées
| Entrée | Source | Format | Exemple |
| --- | --- | --- | --- |
| <nom> | <base, API, fichier> | <format> | <valeur réelle anonymisée> |

## Sorties
| Sortie | Destination | Format |
| --- | --- | --- |
| <nom> | <dossier exclu de git, base, API> | <format> |

## Hors périmètre
- <Ce que l'outil refuse de faire>

## Dépendances déclarées
Le code ne lit et n'écrit rien d'autre. Un test le vérifie.
- Lit : <tables, fichiers, API>
- Écrit : <tables, fichiers, API, ou « rien »>

## Écriture
À remplir si l'outil écrit ailleurs que dans son dossier de sorties.
- Registre de ce qui sera écrit : <fichier ou table>
- Retour arrière : <commande>, testé le <date>

## Vérification
`./verifier` : tests, tailles de fichiers, fichiers interdits. Même commande pour l'humain, l'agent et les hooks.
