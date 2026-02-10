# Phase 4: Initiales Prompt Engineering

## Zielsetzung
Das Ziel dieser Phase ist die systematische Erstellung von Text-Prompts für das Training des Logo-Generierungsmodells. Der Prozess, der im Jupyter-Notebook `notebooks/meta_postprep/prompt_creation.ipynb` implementiert ist, wandelt die aufbereiteten Metadaten in ein strukturiertes Format um, das als direkte Eingabe für das Modell dient.

## Methodik

Das Prompt Engineering basiert auf der Hypothese, dass eine präzise und konsistente Struktur der Eingabeaufforderungen die Qualität und stilistische Kohärenz der generierten Bilder maßgeblich verbessert.

### 1. Definition eines Standard-Prompts
Basierend auf ersten Tests wurde ein statischer Präfix für jeden Prompt definiert: `minimalistic logo, solid background`. Dieser dient dazu, eine grundlegende stilistische Ausrichtung sicherzustellen und die Komplexität für das Modell zu reduzieren, indem ein einheitlicher visueller Kontext (minimalistisches Design vor einem einfarbigen Hintergrund) vorgegeben wird.

### 2. Bereinigung der Tags
Die Analyse der vorhandenen Tags ergab, dass einige Begriffe entweder zu abstrakt, subjektiv oder für die visuelle Generierung als nicht zielführend eingestuft wurden. Folgende Tags werden daher systematisch aus den Metadaten entfernt:
```
'relatable', 'thoughtprovoking', 'minimalist', 'recognizable', 'successful_vibe'
```
Die Entfernung des Tags `minimalist` erfolgt auch, um Redundanz zu vermeiden, da dieser bereits Teil des Standard-Prompts ist.

### 3. Dynamische Prompt-Komposition
Die finalen Prompts werden durch die Konkatenation des Standard-Prompts mit den dynamischen, datensatzspezifischen Merkmalen `description` und den bereinigten `tags` erstellt. Die einzelnen Komponenten werden durch ein Semikolon (`;`) getrennt, um eine klare Strukturierung für das Modell zu gewährleisten.

Das resultierende Format ist:
`minimalistic logo, solid background; description: {description}; tags: {tags}`

### 4. Bewusster Verzicht auf weitere Metadaten
In diesem ersten Entwurf wird bewusst auf die Integration von Merkmalen wie dem Firmennamen (`company_name`) oder der Hauptkategorie (`category_main`) verzichtet. Die zugrundeliegende Annahme ist, dass diese Informationen in einer ersten Iteration die Qualität der generierten Logos nicht signifikant verbessern und potenziell als "Rauschen" (Noise) wirken könnten. Dieser reduzierte Ansatz ermöglicht eine fokussierte Bewertung der grundlegenden Fähigkeit des Modells, visuelle Konzepte aus Beschreibungen und Tags zu synthetisieren.

## Ergebnis
Das Ergebnis dieses Prozesses ist die Datei `final_prompts.csv`, die für jeden Datensatz einen eindeutigen Identifier (`id`) und den zugehörigen, strukturierten Prompt enthält. Diese Datei bildet die finale Eingabegrundlage für das Training des Generierungsmodells.
