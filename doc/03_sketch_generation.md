# Phase 3: Sketch- und Map-Erstellung (`sketch_prep`)

## Ziel

Die `sketch_prep`-Pipeline dient der Erzeugung von zusätzlichen Kontrollsignalen für das Training des Diffusionsmodells. Moderne Architekturen wie ControlNet können neben textuellen Prompts auch bildbasierte Inputs nutzen, um die Generierung präziser zu steuern. In diesem Projekt werden zwei Arten von Kontrollbildern erzeugt:

1.  **Sketches (Skizzen)**: Eine vereinfachte, strichbasierte Darstellung des Logos, generiert durch ein Stable Diffusion ControlNet-Modell.
2.  **Maps (Karten)**: Detaillierte Kantenerkennungs-Maps (Line Art), die die strukturellen Umrisse des Logos präzise hervorheben.

Diese zusätzlichen Daten ermöglichen es dem Modell, die Form und Struktur des zu generierenden Logos besser zu verstehen und zu replizieren.

## Prozessschritte

Die Pipeline wird durch das Skript `pipelines/sketch_prep.py` ausgeführt und umfasst die folgenden Schritte:

### 1. Sketch-Generierung (`sketch_gen.ipynb`)

-   **Eingabe**: Der klassen-ausgewogene Satz von Logo-Bildern aus der `image_prep`-Pipeline.
-   **Modell und Methode**:
    -   **ControlNet-Modell**: `lllyasviel/control_v11p_sd15_scribble`
    -   **Basis-Diffusionsmodell**: `runwayml/stable-diffusion-v1-5`
    -   **Kontrollbild-Erzeugung**: Für jedes Logo wird zunächst mit einem HED-Detektor (`lllyasviel/Annotators`) eine "Scribble-Map" (eine grobe Kantenerkennung) erstellt.
    -   **Generierung**: Diese Scribble-Map dient als Input für das ControlNet-Modell. Mit einem spezifischen Prompt (`"minimalistic sketch, simple and abstract drawing, white background, amateur drawing"`) wird das Stable Diffusion-Modell angewiesen, eine neue, saubere und abstrahierte Skizze des Logos zu generieren. Dieser Ansatz nutzt die generative Fähigkeit des Modells, um eine künstlerisch interpretierte Strichzeichnung anstelle einer reinen Kantenerkennung zu erzeugen.
-   **Ausgabe**: Ein neues Verzeichnis, das für jedes Logo-Bild eine entsprechende, KI-generierte Skizze im PNG-Format enthält.

### 2. Skizzen-Nachbearbeitung (`sketch_postproc.ipynb`)

-   **Eingabe**: Die im vorherigen Schritt generierten Skizzen.
-   **Prozess**: Dieses Notebook führt eine einfache Nachbearbeitung der generierten Skizzen durch. Nachdem sichergestellt wird, dass das Bild in Graustufen vorliegt, wird der Kontrast mittels einer linearen Transformation (`cv2.convertScaleAbs`) erhöht. Dadurch werden die Linien dunkler und der Hintergrund heller, was zu einer saubereren Skizze führt.
-   **Ausgabe**: Ein Verzeichnis mit den nachbearbeiteten, kontrastreicheren Skizzen.

## Ergebnis

Nach Abschluss dieser Pipeline liegen für jedes Logo im ausgewählten Trainingsdatensatz drei verschiedene, aber korrespondierende Bilder vor:

-   Das **Original-Logo**.
-   Die generierte **KI-Skizze**.
-   Die extrahierte **Line-Art-Map**.

Dieses "Tripel" aus Bildern (Logo, Skizze, Map) bildet zusammen mit dem textuellen Prompt aus den Metadaten eine reichhaltige und multimodale Dateneinheit für das Training des Diffusionsmodells mit ControlNet.