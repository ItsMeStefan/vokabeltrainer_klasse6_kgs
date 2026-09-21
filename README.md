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
- kostenlose, vorab erzeugte englische Sprachausgabe über das Lautsprechersymbol
- Trefferzähler, Trefferquote, Laufzähler und beste Runde
- Modi für Gegenwart/Infinitive, Vergangenheit/Simple past, Deutsch und gemischt

Die 69 Vokabeln bilden aktuell ein gemeinsames Set aus **Red Line 2** (Klett), Kapitel G, Seiten 215–217. Weitere auswählbare Sets können ergänzt werden, sobald die dazugehörigen Vokabeldaten vorliegen.

Die Anwendung ist komplett statisch und benötigt keinen Server und keine Datenbank. Der Lernfortschritt wird nur im jeweiligen Browser per `localStorage` gespeichert.

## Sprachausgabe

Die englischen Audiodateien werden mit dem lokal ausgeführten Modell **Piper**, der britischen Stimme `en_GB-aru-medium` und Sprecher 3 erzeugt. Die einzelnen Vokabeln werden mit einem Satzabschluss synthetisiert, damit auch Endkonsonanten wie das `t` in „went“ deutlich hörbar bleiben. Beim Export wird langer, sehr leiser Vorlauf am Anfang gekürzt; ein kurzer natürlicher Übergang bleibt erhalten, damit die Stimme nicht abgehackt startet. Kommagetrennte Formen wie „smelt, smelled“ werden als einzelne MP3-Dateien gespeichert und beim Abspielen mit einer kurzen Pause nacheinander abgespielt. Die fertigen MP3-Dateien liegen unter `audio/tts/`; Besucher benötigen keine API und verursachen keine TTS-Kosten. Falls eine Audiodatei fehlt, fällt die Seite auf die Browser-Sprachausgabe zurück.

Zum erneuten Erzeugen oder Aktualisieren der Dateien werden `piper-tts` und `ffmpeg` benötigt. Stimme und Modell können so geladen und verwendet werden:

```bash
python3 -m pip install piper-tts
python3 -m piper.download_voices en_GB-aru-medium --data-dir .cache/piper
python3 tools/generate_piper_audio.py \
  --model .cache/piper/en_GB-aru-medium.onnx \
  --speaker 3 \
  --force
```

Die Piper-Engine steht unter GPL-3.0. Die verwendete Aru-Stimme ist im Voice-Repository als MIT markiert; die Trainingsdaten sind laut Modellkarte unter CC BY 4.0 dokumentiert: <https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_GB/aru/medium>.

## Lokal öffnen

Einfach `index.html` im Browser öffnen. Für eine realistischere Vorschau mit lokalem Webserver:

```bash
python3 -m http.server 16001 --bind 0.0.0.0
```

Danach lokal `http://localhost:16001` oder im LAN `http://<IP-des-Rechners>:16001` aufrufen.

Für einen dauerhaften lokalen Dienst steht `verb-room.service.example` als Vorlage bereit. Vor dem Aktivieren muss `WorkingDirectory` auf den lokalen Klon-Pfad angepasst werden:

```bash
mkdir -p ~/.config/systemd/user
cp verb-room.service.example ~/.config/systemd/user/verb-room.service
systemctl --user daemon-reload
systemctl --user enable --now verb-room.service
```

Status prüfen oder Dienst stoppen:

```bash
systemctl --user status verb-room.service
systemctl --user disable --now verb-room.service
```
