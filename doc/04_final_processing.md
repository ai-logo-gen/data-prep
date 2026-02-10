# Phase 4: Finale Metadaten-Nachbearbeitung (`meta_postprep`)

## Ziel

Die `meta_postprep`-Pipeline ist der letzte Schritt der Metadaten-Verarbeitung vor der endgültigen Aufteilung des Datensatzes. Ihr Ziel ist es, die textuellen Prompts zu erstellen, die das Diffusionsmodell während des Trainings als Anleitung verwenden wird. Diese Prompts werden aus den bereinigten und angereicherten Metadaten synthetisiert.

## Prozessschritte

Die Pipeline wird durch das Skript `pipelines/meta_postprep.py` gesteuert und besteht aus zwei Hauptschritten:

### 1. Filtern der Metadaten (`filter_metadata.ipynb`)

-   **Eingabe**: Die Metadaten der klassen-ausgewogenen Bildauswahl (`metadata10.csv`) aus der `image_prep`-Pipeline.
-   **Prozess**: Obwohl bereits eine Auswahl getroffen wurde, kann in diesem Schritt eine letzte Filterung stattfinden. Dies könnte beispielsweise das Entfernen von Einträgen mit unvollständigen oder problematischen Metadaten umfassen, die in den vorherigen Schritten nicht erfasst wurden. Es wird sichergestellt, dass nur die qualitativ hochwertigsten Datenpunkte in die Prompt-Erstellung einfließen.
-   **Ausgabe**: Eine final gefilterte Metadaten-Datei.

### 2. Erstellung der Trainings-Prompts (`prompt_creation.ipynb`)

-   **Eingabe**: Die final gefilterte Metadaten-Datei.
-   **Prozess**: Dies ist ein entscheidender Schritt, in dem die strukturierten Metadaten (wie Kategorien, Tags, Beschreibungen) in einen fließenden, natürlichsprachigen Text umgewandelt werden – den **Prompt**. Die Qualität dieser Prompts hat einen direkten Einfluss auf die Fähigkeit des Modells, die gewünschten Logos zu generieren. Ein typischer Prompt könnte nach einer Vorlage wie dieser aufgebaut sein:
    > "Ein minimalistisches Logo für ein [Unternehmenstyp] Unternehmen, Stil: [Tags], Beschreibung: [Beschreibung]."
    
    Die genaue Struktur und der Inhalt der Prompts werden in diesem Notebook definiert und für jeden Datensatz generiert.
-   **Ausgabe**: Eine finale CSV-Datei (`final_prompts.csv`), die für jedes Bild-Tripel (Logo, Skizze, Map) den zugehörigen, generierten Prompt enthält.

## Ergebnis

Das Ergebnis dieser Pipeline ist die Datei `final_prompts.csv`. Sie ist das Kernstück der textuellen Daten für das Modelltraining. Jede Zeile in dieser Datei repräsentiert einen vollständigen Trainings-Datenpunkt auf der Meta-Ebene und verknüpft eine eindeutige Bild-ID mit einem sorgfältig konstruierten textuellen Prompt. Diese Datei ist die direkte Eingabe für den letzten Schritt des gesamten Prozesses: die Aufteilung des Datensatzes.
