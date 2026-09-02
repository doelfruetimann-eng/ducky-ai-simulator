# Git-Fluss

Privat bleiben. ChatGPT-App muss das Repo einmalig sehen (Settings → Applications → Configure → ducky-ai-simulator).
Ohne das: 404, kein Codex-Push.

## Branches

- main: Meilenstein, nur Dölf oder grüner, bewusster Merge
- develop: Arbeitsstand (jetzt angelegt, gleich mit main)
- grok/*, codex/*, claude/*: Arbeit, PR nach develop

## Auto-Merge

Geht erst wenn:
1. App oder PAT schreiben darf
2. tests/tip_test.py in CI läuft — steht: .github/workflows/tip-test.yml,
   `--check` gegen die BASELINE im Skript (Push und PR auf develop/main)
3. PRs nicht alle BOARD.md in der Mitte umschreiben

Bis CI steht: PR nach develop, Dölf muss nicht jede XML-Zeile mergen — aber den ersten App-Klick schon.

ONNX Tutor/Maker/Inspector360 bleibt vorläufig bis Commit auf develop.
