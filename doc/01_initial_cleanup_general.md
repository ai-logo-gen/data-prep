# Allgemeine Datenbereinigung und Strukturierung

Die initiale Bereinigung der Rohdaten ist ein fundamentaler Schritt, um aus einem unstrukturierten Textfeld einen sauberen, tabellarischen Datensatz zu generieren. Dieser Prozess wird zentral durch die Funktion `parse_text` im Skript `utils/text.py` gesteuert und im Notebook `notebooks/amazing_logos_v4_cleanup/step2.ipynb` angewendet.

### Ziel: Verfeinerung der Datenstruktur

Das primäre Ziel dieses Schrittes ist die Transformation der semi-strukturierten `text`-Spalte in vier separate, semantisch eindeutige Spalten: `company`, `description`, `category` und `tags`. Obwohl die Informationen in den Rohdaten durch Kommas getrennt vorliegen, ist diese Struktur für eine direkte maschinelle Verarbeitung und Analyse unzureichend und fehleranfällig.

### Vorgehen: Regelbasiertes Parsen und heuristische Korrektur

Der Bereinigungsprozess zerlegt den kommagetrennten Text-String und wendet eine mehrstufige, regelbasierte Logik an, um die Datenqualität zu maximieren:

1.  **Heuristische Korrektur von Beschreibung und Kategorie:** Eine Analyse der Rohdaten zeigte, dass die Felder für Beschreibung und Kategorie häufig vertauscht waren. Um dies zu korrigieren, wurde eine Heuristik implementiert: Wenn der extrahierte `category`-String mehr als zwei Wörter umfasst und gleichzeitig länger ist als der `description`-String, werden die Inhalte der beiden Felder getauscht. Diese Regel basiert auf der Annahme, dass Kategorien in der Regel kurz und prägnant sind, während Beschreibungen tendenziell länger ausfallen.

2.  **Bereinigung und Umverteilung der Tags:** Die `tags`-Spalte wird ebenfalls einer Bereinigung unterzogen. Tags, die aus mehr als drei Wörtern bestehen, werden als Teil der Beschreibung interpretiert und aus der Tag-Liste entfernt und stattdessen an die `description`-Spalte angehängt. Dies schärft die Definition eines "Tags" als kurzes, prägnantes Schlüsselwort.

3.  **Finale Normalisierung:** In einem letzten Schritt werden alle extrahierten Felder von unerwünschten Sonderzeichen und überflüssigen Leerzeichen befreit, um eine konsistente Datenbasis zu gewährleisten.

### Ergebnis: Strukturierter Datensatz

Das Ergebnis dieses Prozesses ist ein strukturierter DataFrame, in dem die ursprünglichen Textinformationen sauber in die Zielspalten `company`, `description`, `category` und `tags` aufgeteilt sind. Dieser bereinigte Datensatz bildet die Grundlage für alle nachfolgenden, spezifischeren Bereinigungs- und Analyseschnitte, wie etwa die detaillierte Bearbeitung der `category`-Spalte.