# Bereinigung der Spalte `category`

Die Bereinigung und Konsolidierung der `category`-Spalte erfolgt in mehreren aufeinander aufbauenden Notebooks im Ordner `notebooks/amazing_logos_v4_cleanup/`. Jeder Schritt verfeinert die Daten weiter. Die Benennung der Notebooks ist dabei nicht streng chronologisch, was zu Verwirrung führen kann. Die tatsächliche Abfolge ist wie folgt:

### 1. Normalisierung (`step3_categories.ipynb`)
- **Was passiert?** Die Kategorienamen werden in ein einheitliches Format gebracht.
- **Details:**
    - Alle Kategorien werden in Kleinbuchstaben umgewandelt.
    - Sonderzeichen werden entfernt und Leerzeichen durch Unterstriche (`_`) ersetzt.
    - Fehlende Kategoriewerte (`NaN`) werden durch den String `'na'` ersetzt.
- **Ergebnis:** `metadata3.csv`. In dieser Datei ist `minimalist` noch die häufigste Kategorie.

### 2. Herstellung semantischer Eindeutigkeit

- **Ziel:** In diesem Verarbeitungsschritt wird die semantische Trennung zwischen den Spalten `category` und `tags` geschärft. Die `category`-Spalte soll eine eindeutige thematische Klassifizierung des Logos ermöglichen (z.B. "Technologie", "Gastronomie"), während die `tags`-Spalte stilistische oder untergeordnete Merkmale beschreibt (z.B. "minimalistisch", "modern"). In den Rohdaten kam es hier zu signifikanten Überlappungen, bei denen stilistische Begriffe als Hauptkategorie eingetragen waren.

- **Vorgehen:** Um diese Überlappung aufzulösen, wurden zunächst die häufigsten Tags identifiziert, die primär stilistische Attribute repräsentieren (z.B. `minimalist`, `modern`, `letter`). Anschließend wurde der Datensatz iterativ geprüft: Stimmte der Wert in der `category`-Spalte eines Logos mit einem dieser stilistischen Top-Tags überein, wurde dieser Wert aus der `category`-Spalte entfernt. Um einen Informationsverlust zu vermeiden, wurde der entfernte Begriff stattdessen der `tags`-Spalte des betreffenden Logos hinzugefügt.

- **Ergebnis:** Durch diesen Prozess wurde die `category`-Spalte von stilistischen Attributen bereinigt. Begriffe wie `minimalist` fungieren nun konsistent als Tags, wodurch die `category`-Spalte eine klarere thematische Zuordnung der Logos gewährleistet. Dies erhöht die Datenqualität und semantische Konsistenz für das nachfolgende Modelltraining.

### 3. Konsolidierung (`step4_categories2.ipynb`)
- **Was passiert?** Ähnliche oder verwandte Kategorien werden zu übergeordneten Gruppen zusammengefasst.
- **Details:**
    - Rein numerische Kategorien (z.B. `'1990'`) werden entfernt.
    - Eine vordefinierte Zuordnungslogik (`consolidation_map`) fasst Hunderte von spezifischen Kategorien zu übergeordneten Gruppen zusammen (z.B. `'tech_startup'` wird zu `technology`).
    - Nicht zuordenbare Kategorien werden als `'unclassified'` markiert.
- **Ergebnis:** `metadata6.csv` mit konsolidierten Kategorien.

### 4. Reklassifizierung aus Tags (`step4_categories3.ipynb`)
- **Was passiert?** Es wird versucht, die als `'unclassified'` markierten Logos doch noch einer Kategorie zuzuordnen.
- **Details:**
    - Für jedes `'unclassified'`-Logo werden die `tags` analysiert.
    - Wenn ein Tag mit einer existierenden, häufigen Kategorie übereinstimmt, wird diese zugewiesen und der Tag entfernt.
- **Ergebnis:** `metadata7.csv` mit weniger `'unclassified'`-Logos.

### 5. Finale Filterung (`step4_categories4_filtering.ipynb`)
- **Was passiert?** Kategorien, die nur noch sehr selten vorkommen, werden entfernt, um die Datenqualität für das Training zu sichern.
- **Details:**
    - Alle Kategorien, die **weniger als 4 Logos** enthalten, werden aus dem Datensatz entfernt.
- **Ergebnis:** `metadata8.csv` mit dem finalen, bereinigten Set an Kategorien.
