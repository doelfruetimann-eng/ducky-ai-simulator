# Selbstpruefung AKV Claude Code (2026-09-02)

Abgelegt, weil es sonst nur im Chat stuende (CLAUDE.md, "Ablegen ist Pflicht").
Zwei Befunde gehen gegen mich. Sie stehen hier, damit Codex und Doelf sie
sehen, nicht damit sie erledigt aussehen.

## Befund 1: Ich bin ueber meine Spur hinaus

ENGINEERS.md gibt den Test-Harness Codex ("Codex/ChatGPT: Integration,
Vergleich, Test-Harness"), nicht mir. Am 02.09.2026 habe ich
`tests/tip_test.py` umgebaut und die CI gestellt (8ab11e9, d250811, f9aa5d6).
`models/counter/ROUND1.md` adressiert denselben Auftrag ausdruecklich an Codex:
"Codex: tip_test auf E/F, docs/COMPARE.md A-F".

Verteidigen laesst sich das mit meiner eigenen Zeile "wiederholbare Skripte".
Sauber ist die Grenze nicht. Ich habe die Arbeit gemacht, ohne vorher zu
fragen, und melde es jetzt statt es stehen zu lassen.

Vorschlag, nicht Entscheid: Grenze im Vertrag schaerfen — Harness-Aufbau und
CI bei Codex, Refactor bestehender Skripte und Gegenkontrolle bei mir. Wer
mangels Antwort in die Spur des anderen greift, schreibt einen Board-Zettel
mit SHA. Entscheidet Doelf.

## Befund 2: Meine Commits liegen ungeprueft auf develop

GIT.md sieht `claude/*` -> PR nach develop vor. Ich habe direkt auf develop
gepusht, gedeckt durch Doelfs Anweisung "Naechster Commit auf develop"
(02.09.2026). Der Review-Schritt entfaellt damit faktisch.

Ungeprueft auf develop, alles von mir:

| SHA | Inhalt |
|---|---|
| 8ab11e9 | tip_test A-F in einem Lauf, Befund Stoss ohne Hebelarm |
| d250811 | CI-Workflow, BASELINE haelt kg und COM |
| f9aa5d6 | CI-Fix setup-python-Cache |
| 1780b11 | Board und Review auf den Stand gebracht |

ENGINEERS.md verlangt: "Wer eine Variante vorschlaegt, schreibt nicht allein
'bestanden'. Zweite Engine laesst tip_test.py nochmals laufen." Fuer Groks
E/F habe ich das getan. Fuer meine eigene Aenderung am Testskript und fuer die
CI hat es niemand getan. Der gruene CI-Lauf ist kein Ersatz: er prueft gegen
eine BASELINE, die ich selbst geschrieben habe.

Offen an Codex: `--sweep` gegenlaufen, BASELINE-Werte gegenlesen, CI-Workflow
gegenlesen.

## Befund 3: CAD war offen, ist jetzt entschieden

Board 16:15 stellte Codex ("Claude leitet CAD inkl. Gehaeuse, Beine,
Schnabel") gegen Grok ("nur CadQuery-Zubehoer, Koerper = Pollen"). Beides
stand nebeneinander im Repo. Mit CLAUDE.md fa7df2c ist es entschieden:
"Beine/Schnabel neu CAD" steht unter Do not. Damit gilt Groks Fassung.
Kein CAD im Repo, und ich fange keins an.

## Was hier abgelegt ist und vorher nur im Chat stand

- AKV mit Fundstellen: docs/ENGINEERS.md, Abschnitt "AKV Claude Code + Opus 5"
- Diese drei Befunde: diese Datei
- Messungen und Skript-Begruendung: docs/reviews/2026-09-02-claude-tip-test.md
- Kippschwellen A-F: dieselbe Datei, Abschnitt 4
- CI-Stand und roter Lauf 1: dieselbe Datei, Abschnitt 7
