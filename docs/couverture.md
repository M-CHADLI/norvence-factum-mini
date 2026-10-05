# Couverture de code

La CI était verte car les tests passaient, mais aucun ne fournissait un montant avec une virgule décimale.
La branche `elif "," in text` de `normalize.py` était évaluée sans jamais être prise : ligne couverte, branche manquante.
Et rien ne mesurait la couverture, ni n'imposait de seuil : un trou dans les tests ne pouvait pas faire échouer le build.

## Seuil retenu : 85 %

- Mesure actuelle : **90 %** (lignes + branches), dont `normalize.py` à 100 % de branches.
- Mesure avant les tests paramétrés : **75 %**.
- 85 % se situe entre les deux : supprimer les tests de `normalize.py` fait passer la CI au rouge, tandis que les 5 points de marge absorbent le client HTTP réel (`HttpLLMClient`), qui appelle le réseau et n'est pas testé en unitaire.
- Le seuil est défini dans `pyproject.toml` (`[tool.coverage.report] fail_under`), pas dans le workflow : la même règle s'applique en local et en CI.

## Relancer la mesure en local

```bash
uv sync
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```
