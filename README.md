# Konditionierte KI-Generierung minimalistischer Logos

Dieses Repository dient als Anhang zur Masterarbeit mit dem Titel "Konditionierte KI-Generierung minimalistischer Logos: Konzeption, Auswahl und Evaluation eines Modellprototyps".

## Projektstruktur

- **`/pipelines`**: Enthält die Hauptskripte zur Datenvorverarbeitung.
- **`/utils`**: Beinhaltet Hilfsfunktionen, die von den Pipelines verwendet werden, z.B. für Bildverarbeitung und Textnormalisierung.
- **`/input`**: Verzeichnis für die Eingabedaten.
- **`/output`**: Hier werden die verarbeiteten Daten und generierten Bilder gespeichert.
- **`/doc`**: Dokumentation der einzelnen Schritte des Prozesses.

## Abhängigkeiten

Das Projekt wurde mit Python 3.11 entwickelt. Die wichtigsten Pakete sind:

- `pandas`
- `papermill`
- `opencv-python`
- `scikit-learn`
- `Pillow`
- `torch`
- `diffusers`
- `controlnet_aux`
- `google-generativeai`
