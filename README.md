# Verb Room

Mobiler Vokabeltrainer

Enthalten sind zunächst:

- Infinitive
- Simple past
- German
- Lernkarten-Läufe mit 10, 20 oder allen 69 Vokabeln
- automatisch gemischte Reihenfolge pro Lauf
- jede Vokabel höchstens einmal pro Lauf
- Karte antippen, umdrehen und anschließend mit „richtig“ oder „nochmal“ bewerten
- nach dem Lauf eine Liste der Problemvokabeln mit direkter Fehler-Wiederholungsrunde
- Sprachausgabe über das Lautsprechersymbol im Browser
- Trefferzähler, Trefferquote, Laufzähler und beste Runde
- Modi für Gegenwart/Infinitive, Vergangenheit/Simple past, Deutsch und gemischt

Die 69 Vokabeln bilden aktuell ein gemeinsames Set aus **Red Line 2** (Klett), Kapitel G, Seiten 215–217. Weitere auswählbare Sets können ergänzt werden, sobald die dazugehörigen Vokabeldaten vorliegen.

Die Anwendung ist komplett statisch und benötigt keinen Server und keine Datenbank. Der Lernfortschritt wird nur im jeweiligen Browser per `localStorage` gespeichert.

## Lokal öffnen

Einfach `index.html` im Browser öffnen. Für eine realistischere Vorschau mit lokalem Webserver:

```bash
python3 -m http.server 8000
```

Danach `http://localhost:8000` aufrufen.
