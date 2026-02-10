# Phase 1: Metadaten-Bereinigung (`meta_cleanup`)

## Ziel

Die erste Phase der Datenaufbereitung, `meta_cleanup`, zielt darauf ab, die rohen Metadaten des "Amazing Logos v4" Datensatzes zu strukturieren, zu normalisieren und anzureichern. Eine hohe Qualität der Metadaten ist entscheidend, da sie die Grundlage für die Erstellung von Trainings-Prompts und die semantische Steuerung des Diffusionsmodells bilden. Der Prozess fokussiert sich auf die Konsolidierung von Kategorien und die strategische Zuweisung von Tags, um eine aussagekräftige und konsistente Datenbasis zu schaffen.

## Prozessschritte

Die Pipeline `meta_cleanup` wird durch das Skript `pipelines/meta_cleanup.py` gesteuert, welches eine Sequenz von Jupyter-Notebooks ausführt. Jeder Schritt baut auf dem vorherigen auf und verfeinert die Metadaten iterativ.

### 1. Kategorien-Konsolidierung (`step4_categories2.ipynb`)

-   **Eingabe**: Vorläufige Metadaten mit einer Vielzahl von Kategorien.
-   **Prozess**: In diesem Schritt werden semantisch ähnliche oder redundante Kategorien zu einer einzigen, standardisierten Kategorie zusammengefasst. Beispielsweise könnten "Technology Company" und "Tech" zu "Technology" konsolidiert werden. Dieser Prozess basiert auf vordefinierten Mappings und Analysen der Kategorienverteilung.
-   **Ausgabe**: Eine aktualisierte Metadaten-Datei (`metadata6.csv`) mit einem bereinigten und reduzierten Satz an Kategorien.

### 2. Tag-Zuweisung für unklassifizierte Kategorien (`step4_categories3.ipynb`)

-   **Eingabe**: `metadata6.csv`.
-   **Prozess**: Einige Logos gehören zu Kategorien, die so selten sind, dass sie keiner Hauptkategorie zugeordnet werden können ("unclassified"). Um den Informationsverlust zu minimieren, wird die ursprüngliche, seltene Kategorie als semantisches Tag zu den Metadaten des Logos hinzugefügt.
-   **Ausgabe**: Eine angereicherte Metadaten-Datei (`metadata7.csv`), in der die Information seltener Kategorien als Tags erhalten bleibt.

### 3. Filtern von niedrig-frequenten Kategorien (`step4_categories4_filtering.ipynb`)

-   **Eingabe**: `metadata7.csv`.
-   **Prozess**: Um das Modelltraining nicht durch unterrepräsentierte Klassen zu verzerren, werden Kategorien, die eine sehr geringe Anzahl von Beispielen aufweisen (hier: weniger als 4), herausgefiltert. Diese Logos werden ebenfalls als "unclassified" markiert, um sie für eine spätere, gezielte Behandlung vorzumerken.
-   **Ausgabe**: Eine gefilterte Metadaten-Datei (`metadata8.csv`).

### 4. Finale Kategorien-Bereinigung (`step5_categories.ipynb`)

-   **Eingabe**: `metadata8.csv`.
-   **Prozess**: Dieser Schritt führt eine finale Bereinigung durch.
    -   Kategorien, die nicht in der finalen Konsolidierungskarte (`consolidation_map`) enthalten sind, werden endgültig als "unclassified" markiert.
    -   Für häufig auftretende "unclassified"-Logos wird die ursprüngliche Kategorie als zusätzliches Tag hinzugefügt, um den Kontext zu bewahren.
-   **Ausgabe**: `metadata9.csv` mit einem finalen, bereinigten Kategoriensatz.

### 5. Erstellung von Top-Level-Kategorien (`step6_categories.ipynb`)

-   **Eingabe**: `metadata9.csv`.
-   **Prozess**: Aus den feingranularen, bereinigten Kategorien wird eine neue Spalte mit groben Top-Level-Kategorien abgeleitet. Dies ermöglicht eine hierarchische Strukturierung und kann für eine breitere kategoriale Steuerung im Modelltraining genutzt werden.
-   **Ausgabe**: Die finale Metadaten-Datei dieser Pipeline, die sowohl feingranulare als auch grobe Kategorien enthält.

## Ergebnis

Am Ende dieser Pipeline liegt ein bereinigter und angereicherter Metadaten-Datensatz vor. Die Kategorien sind konsolidiert, seltene Informationen als Tags bewahrt und eine hierarchische Kategorisierung wurde eingeführt. Diese solide Datenbasis ist die Voraussetzung für die nachfolgenden Schritte der Bild-Vorbereitung und Prompt-Erstellung.
