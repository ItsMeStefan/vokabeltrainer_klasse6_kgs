# Verb Room

Mobiler Vokabeltrainer für die unregelmäßigen Verben aus den drei abfotografierten Buchseiten.

Enthalten sind zunächst:

- Infinitive
- Simple past
- German
- Lernkarten-Läufe mit 10, 20 oder allen 69 Vokabeln
- automatisch gemischte Reihenfolge pro Lauf
- jede Vokabel höchstens einmal pro Lauf
- Karte antippen, umdrehen und anschließend mit „richtig“ oder „nochmal“ bewerten
- Trefferzähler, Trefferquote, Laufzähler und beste Runde
- Modi für Gegenwart/Infinitive, Vergangenheit/Simple past, Deutsch und gemischt

Die Anwendung ist komplett statisch und benötigt keinen Server und keine Datenbank. Der Lernfortschritt wird nur im jeweiligen Browser per `localStorage` gespeichert.

## Lokal öffnen

Einfach `index.html` im Browser öffnen. Für eine realistischere Vorschau mit lokalem Webserver:

```bash
python3 -m http.server 8000
```

Danach `http://localhost:8000` aufrufen.

## GitHub Pages

Das Repository auf GitHub pushen und unter **Settings → Pages** als Quelle den Branch mit dem Ordner `/ (root)` auswählen. Danach ist die App über die von GitHub angezeigte Pages-Adresse erreichbar.
