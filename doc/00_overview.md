# Datenbasis und Aufbereitung: Ein Überblick

Dieses Dokument beschreibt den Prozess der Aufbereitung des "Amazing Logos v4" Datensatzes für das Training eines Diffusionsmodells. Der Prozess ist in mehrere Phasen unterteilt, die jeweils durch eine dedizierte Pipeline repräsentiert werden. Jede Pipeline besteht aus einer Reihe von Jupyter-Notebooks, die schrittweise ausgeführt werden, um die Daten zu bereinigen, zu transformieren und für das Modelltraining vorzubereiten.

## Workflow-Übersicht

Die Datenaufbereitung folgt einem sequenziellen Prozess, der in der `pipelines/README.md` definiert ist:

1.  **Metadaten-Bereinigung (`meta_cleanup`)**: Diese Phase konzentriert sich auf die Bereinigung und Normalisierung der mit den Logos verbundenen Metadaten. Dies umfasst die Kategorisierung, das Tagging und die Konsolidierung von Informationen.

2.  **Bild-Vorbereitung (`image_prep`)**: In dieser Phase werden die Bilddaten selbst verarbeitet. Dies beinhaltet das Extrahieren der relevanten Bilder basierend auf den bereinigten Metadaten, das Filtern nach bestimmten Kriterien (z.B. minimalistische Logos) und das Erstellen einer ausgewogenen Teilmenge.

3.  **Sketch-Erstellung (`sketch_prep`)**: Um das Modelltraining mit zusätzlichen Kontrollsignalen zu unterstützen (z.B. für ControlNet), werden in dieser Phase Skizzen und Kantenerkennungs-Maps (Edge Maps) aus den Logo-Bildern generiert.

4.  **Finale Metadaten-Nachbearbeitung (`meta_postprep`)**: In dieser Phase werden die Metadaten finalisiert. Dies umfasst das Filtern und die Erstellung der finalen Trainings-Prompts.

5.  **Datensatz-Aufteilung (`data_split`)**: Der letzte Schritt teilt den aufbereiteten Datensatz in Trainings-, Validierungs- und Testsets auf, um ein robustes Modelltraining und eine valide Evaluierung zu gewährleisten.

## Dokumentationsstruktur

Die folgenden Dokumente beschreiben jede Phase im Detail:

-   [**01_initial_cleanup.md**](./01_initial_cleanup.md): Detaillierte Beschreibung der Metadaten-Bereinigung.
-   [**02_image_preparation.md**](./02_image_preparation.md): Detaillierte Beschreibung der Bild-Vorbereitungsschritte.
-   [**03_sketch_generation.md**](./03_sketch_generation.md): Detaillierte Beschreibung der Sketch- und Map-Erstellung.
-   [**04_final_processing.md**](./04_final_processing.md): Detaillierte Beschreibung der finalen Metadaten-Nachbearbeitung und Prompt-Erstellung.
-   [**05_dataset_splitting.md**](./05_dataset_splitting.md): Detaillierte Beschreibung der Aufteilung des Datensatzes.
