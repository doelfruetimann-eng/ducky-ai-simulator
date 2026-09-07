# Macroduck — Beobachtungspunkt, 2026-09-03

Status: **beobachten**. Nichts entschieden, nichts bestellt, nichts geaendert.
Duty: Claude (Recherche + Ablage). Kein Auftrag an Mini oder Windows-PC.

## Was es ist

Andrea Esposito (Robotic Hand Lead bei Foundation, X `@aesposito0`) kuendigt am
30.08.2026 "Macroduck" an: einen Nachbau des Pollen MicroDuck. Er verlost einige
Exemplare, Anmeldung ueber `macroduck.bot` (X-Handle, E-Mail, Firmenname — keine
Zahlungsdaten, kein Verkauf). Versandangabe "~4 Wochen" statt der 4-6 Monate
Vorbestellzeit bei Pollen.

## Warum das plausibel und zugleich unfertig ist

Zeitachse: MicroDuck angekuendigt am 27.08.2026, erste Auslieferungen vor
Weihnachten 2026. Am 30.08. besass niemand ausserhalb von Pollen ein Geraet.
"Reverse engineered" kann daher kein Zerlegen physischer Hardware sein, sondern
nur die Ableitung aus den oeffentlichen Simulations-Meshes in
`pollen-robotics/microduck_rl` (76 STL, CC BY-SA-NC).

Folge: **Sim-Meshes sind keine Fertigungsteile.** Keine Toleranzen, keine
Gewinde, keine Sitze fuer Gewindeeinsaetze, keine Elektronik, keine Verkabelung.
Der veroeffentlichte CAD-Screenshot zeigt eine korrekte Form, keinen baubaren
Roboter. Der Weg von dort zu funktionierender Hardware ist der eigentliche
Aufwand.

## Lizenzfrage — ungeklaert

Vermutung, nicht belegt: die CAD ist aus den Sim-Meshes abgeleitet, also
CC BY-SA-NC.

- **NC** schliesst Verkauf aus. Eine Gratisverlosung passt vermutlich noch.
- **SA** verlangt, dass ein verteiltes Derivat unter derselben Lizenz
  weitergegeben wird. Das passt schlecht zur Ankuendigung "ich open-source BOM,
  CAD und Anleitung *vielleicht*, wenn genug Interesse da ist" — Share-Alike ist
  keine Kuer.
- Pollen-Press-Kit sagt ausdruecklich, den Roboter nicht als Open-Source-Hardware
  zu bezeichnen; The Register zitiert "no plans to open source the hardware".

Ob Pollen reagiert, ist offen.

## Was wir beobachten

Nicht die Gratis-Ente. Interessant ist eine moegliche **Freigabe von BOM, CAD und
Montageanleitung**. Das waere der erste offene 25-cm-Bauplan — Open Duck Mini ist
42 cm gross und seit Mitte 2025 im Wartungsmodus.

## Entscheid

Plan unveraendert: MicroDuck-Bestellung laeuft weiter, Simulator-Arbeit laeuft
parallel. Ein Verteiler-Eintrag kostet eine E-Mail-Adresse und verpflichtet zu
nichts. Eine Verlosung ist keine Beschaffung.

Nicht tun: Sim-Meshes oder abgeleitete CAD in dieses Repo kopieren.

## Quellen

- Post: <https://x.com/aesposito0/status/2094198418453495840> (30.08.2026)
- Anmeldung: <https://macroduck.bot/>
- Person: <https://www.linkedin.com/in/aesposito0>
- Erwaehnung: The Neuron, Digest 31.08.2026
- Pollen Press-Kit: <https://pollen-robotics.com/microduck/press-kit/>
