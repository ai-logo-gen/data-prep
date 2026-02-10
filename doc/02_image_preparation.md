# Phase 2: Bild-Vorbereitung (`image_prep`)

## Ziel

Die Pipeline `image_prep` ist verantwortlich für die Auswahl, Filterung und Organisation der eigentlichen Bilddateien. Aufbauend auf den in Phase 1 bereinigten Metadaten wird hier der finale Bild-Pool für das Training zusammengestellt. Das Hauptziel ist es, eine qualitativ hochwertige und repräsentative Auswahl an Logos zu treffen, die den Anforderungen des Modelltrainings entspricht.

## Prozessschritte

Die Pipeline wird durch das Skript `pipelines/image_prep.py` gesteuert und führt die folgenden Notebooks aus:

### 1. Extrahieren der Bilder (`extract_images.ipynb`)

-   **Eingabe**: Die bereinigten Metadaten aus der `meta_cleanup`-Pipeline.
-   **Prozess**: Dieses Notebook liest die Metadaten und kopiert die entsprechenden Logo-Bilder aus dem ursprünglichen, umfangreichen Datensatz in ein dediziertes Verzeichnis. Nur Bilder, die in den bereinigten Metadaten referenziert sind, werden für die weiteren Schritte berücksichtigt.
-   **Ausgabe**: Ein Verzeichnis, das alle relevanten Logo-Bilder enthält.

### 2. Filtern nach minimalistischen Logos (`filter_minimalistic_logos.ipynb`)

-   **Eingabe**: Der extrahierte Bild-Pool.
-   **Prozess**: Für die spezifische Zielsetzung, ein Modell zur Generierung von minimalistischen Logos zu trainieren, wird in diesem Schritt eine Filterung durchgeführt. Es wird angenommen, dass ein Mechanismus (z.B. basierend auf Bildanalyse oder vordefinierten Kriterien) existiert, um nicht-minimalistische Logos zu identifizieren und auszuschließen.
-   **Ausgabe**: Ein gefilterter Satz von Bildern, der nur noch minimalistische Logos enthält, sowie eine aktualisierte Metadaten-Datei, die diese Auswahl widerspiegelt.

### 3. Erstellen der finalen Metadaten (`create_metadata10_from_total_filtered.ipynb`)

-   **Eingabe**: Die gefilterte Bildauswahl und die zugehörigen Metadaten.
-   **Prozess**: Dieses Notebook konsolidiert die Informationen der gefilterten Logos und erstellt eine finale Metadaten-Datei (`metadata10.csv`). Diese Datei dient als "Single Source of Truth" für die nachfolgenden Schritte und enthält alle für das Training relevanten Informationen zu den ausgewählten Bildern.
-   **Ausgabe**: `metadata10.csv`.

### 4. Erstellen einer klassen-ausgewogenen Teilmenge (`extract_balanced_images.ipynb`)

-   **Eingabe**: `metadata10.csv` und der Pool an minimalistischen Logo-Bildern.
-   **Prozess**: Um zu verhindern, dass das Modell eine Tendenz (Bias) zu überrepräsentierten Kategorien entwickelt, wird eine klassen-ausgewogene Teilmenge der Bilder erstellt. Dies bedeutet, dass aus jeder Kategorie eine ähnliche Anzahl von Beispielen ausgewählt wird. Dies ist besonders wichtig für die Stabilität des Trainings und die Generalisierungsfähigkeit des Modells.
-   **Ausgabe**: Ein neues Verzeichnis (`balanced_sample_2k_512x512`), das die ausgewogene Auswahl an Bildern enthält. Die Größe (z.B. 2k) und Auflösung (z.B. 512x512) sind hierbei konfigurierbar.

## Ergebnis

Am Ende dieser Pipeline steht ein sorgfältig kuratierter und ausgewogener Datensatz von Logo-Bildern zur Verfügung. Dieser Datensatz ist nicht nur thematisch (minimalistisch) fokussiert, sondern auch strukturell (klassen-ausgewogen) für ein effektives Training optimiert. Die Bilder sind in einem standardisierten Format und einer einheitlichen Größe für die nächsten Verarbeitungsschritte vorbereitet.
