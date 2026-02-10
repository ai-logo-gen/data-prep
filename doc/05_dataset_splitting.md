# Phase 5: Datensatz-Aufteilung (`data_split.ipynb`)

## Ziel

Der letzte Schritt des Vorverarbeitungsprozesses ist die Aufteilung des gesamten aufbereiteten Datensatzes in drei separate Teilmengen:

1.  **Trainings-Set (Training Set)**: Der größte Teil der Daten, der verwendet wird, um das Modell zu trainieren.
2.  **Validierungs-Set (Validation Set)**: Eine kleinere Teilmenge, die während des Trainings verwendet wird, um die Hyperparameter zu optimieren und Overfitting zu vermeiden.
3.  **Test-Set (Test Set)**: Eine ebenfalls kleinere, aber "unsichtbare" Teilmenge, die erst nach Abschluss des Trainings verwendet wird, um die finale Leistung und Generalisierungsfähigkeit des Modells objektiv zu bewerten.

Dieser Schritt wird durch das Jupyter-Notebook `data_split.ipynb` durchgeführt und stellt sicher, dass das Modell robust trainiert und evaluiert werden kann.

## Prozessschritte

### 1. Laden der finalen Daten

-   **Eingabe**: Die finale Prompt-Datei `final_prompts.csv` aus der `meta_postprep`-Pipeline.
-   **Prozess**: Das Notebook lädt die CSV-Datei, die alle Metadaten und die generierten Prompts enthält.

### 2. Mischen und Aufteilen

-   **Prozess**:
    -   **Mischen (Shuffle)**: Zuerst wird der gesamte Datensatz zufällig gemischt. Dies ist ein entscheidender Schritt, um sicherzustellen, dass die Aufteilung unvoreingenommen (unbiased) ist und keine systematischen Muster aus der ursprünglichen Reihenfolge der Daten in die Teilmengen gelangen.
    -   **Aufteilen (Split)**: Der gemischte Datensatz wird anschließend in die drei Ziel-Sets aufgeteilt. Eine typische und hier verwendete Aufteilung ist:
        -   **80% Training**
        -   **10% Validierung**
        -   **10% Test**
-   **Ausgabe**: Drei separate DataFrames (für Training, Validierung und Test), die jeweils eine `split`-Spalte enthalten, die ihre Zugehörigkeit markiert.

### 3. Kopieren der Dateien

-   **Prozess**: Basierend auf der Zugehörigkeit jedes Datenpunktes zu einem der drei Sets, werden die entsprechenden Dateien (Original-Logo, Skizze, Map) in eine neue, finale Verzeichnisstruktur kopiert. Diese Struktur ist typischerweise wie folgt aufgebaut:
    ```
    final/
    ├── train/
    │   ├── logo/
    │   ├── sketches/
    │   └── maps/
    ├── val/
    │   ├── logo/
    │   ├── sketches/
    │   └── maps/
    └── test/
        ├── logo/
        ├── sketches/
        └── maps/
    ```
-   **Ausgabe**: Eine sauber organisierte Ordnerstruktur, die die aufgeteilten Bilddaten enthält.

### 4. Speichern der geteilten Metadaten

-   **Prozess**: Für jedes Set (Training, Validierung, Test) wird eine eigene `prompts.csv`-Datei im jeweiligen Unterverzeichnis gespeichert. Diese CSV-Dateien enthalten nur die Metadaten und Prompts für die Bilder in diesem spezifischen Set.
-   **Ausgabe**: `train/prompts.csv`, `val/prompts.csv`, `test/prompts.csv`.

### 5. Verifizierung

-   **Prozess**: Als finaler Qualitätssicherungsschritt überprüft das Notebook, ob die Anzahl der Dateien in den Zielverzeichnissen mit der Anzahl der Einträge in den `prompts.csv`-Dateien übereinstimmt. Dies stellt sicher, dass der Kopiervorgang vollständig und fehlerfrei war.
-   **Ausgabe**: Eine Bestätigungsmeldung, ob die Verifizierung erfolgreich war.

## Ergebnis

Am Ende dieses Prozesses liegt ein vollständig aufbereiteter, aufgeteilter und verifizierter Datensatz vor, der direkt für das Training und die Evaluierung eines Diffusionsmodells mit ControlNet verwendet werden kann. Die klare Trennung von Trainings-, Validierungs- und Testdaten ist fundamental für die wissenschaftliche Validität der Modellergebnisse.
