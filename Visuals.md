## 1. Die Farbmatrix (Web-Konform)
Wir nutzen ein kontrastreiches Schema, das auf Tiefe und Leuchtkraft optimiert ist.

| Element | Farbe | HEX | Einsatzbereich |
|---|---|---|---|
| Hintergrund | Midnight Void | #020408 | Gesamter Body, tiefste Ebene. |
| Ebenen/Cards | Obsidian Glass | rgba(15, 20, 28, 0.7) | Dokumenten-Karten, Sidebars (mit Backdrop-Blur). |
| Primär-Akzent | Raziel Violet | #6E44FF | Hover-Effekte, Agenten-Status, Markenelemente. |
| Aktions-Neon | Infinite Cyan | #00F5FF | Planungs-Pfade, Fortschritt, „Action“-Buttons. |
| Highlight | Sacred Ember | #FFD700 | Erfolg, wichtige Knotenpunkte, Icons. |
| Text (Primär) | Starlight White | #E0E6ED | Alle wichtigen Inhalte und Titel. |
| Text (Sekundär) | Ghost Grey | #64748B | Metadaten, inaktive Elemente. |

------------------------------
## 2. Typografie (Webfonts)
Die Schriftarten kombinieren archaische Breite mit technologischer Präzision.

* Überschriften (H1, H2, H3): Michroma
* Stil: Sans-Serif, weitläufig, futuristisch.
   * Wirkung: Wirkt wie eine Gravur auf einem digitalen Monument.
   * CSS: font-family: 'Michroma', sans-serif; letter-spacing: 0.1em; text-transform: uppercase;
* Fließtext & Daten: Inter
* Stil: Hochmodern, neutral, extrem gut lesbar.
   * Wirkung: Bringt Sachlichkeit in das mystische Design.
   * CSS: font-family: 'Inter', sans-serif; font-weight: 300; line-height: 1.6;
* System-Outputs & Agenten-Logs: JetBrains Mono
* Stil: Monospace.
   * Wirkung: Signalisiert: „Hier arbeitet der Agent“.
   * CSS: font-family: 'JetBrains Mono', monospace; color: #00F5FF; font-size: 0.85rem;

------------------------------
## 3. Visuelle Effekte (Web-Styles)
Um die Identität digital „fühlbar“ zu machen, werden diese CSS-Prinzipien angewendet:

* Der „Raziel-Glow“:
Buttons und aktive Icons haben keinen harten Schatten, sondern einen weichen, violetten Schein.
* CSS: box-shadow: 0 0 15px rgba(110, 68, 255, 0.4);
* Backdrop Blur:
Alle Overlays (Modale) wirken wie mattiertes Glas.
* CSS: backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1);
* Gitter-Hintergrund (Subtil):
Ein fast unsichtbares Punkt-Raster (Dots) über dem Hintergrund, das die „Struktur des Wissens“ darstellt.

------------------------------
## 4. Komponenten-Beispiel: Der „Action-Button“
Ein Button für den Start einer agentischen Planung sieht so aus:

* Grundzustand: Schwarzer Hintergrund, Cyan-farbene Umrandung (1px).
* Hover-Zustand: Die Umrandung beginnt zu pulsieren, der Text „Enthüllen“ leuchtet leicht violett auf.
* Klick-Zustand: Ein kurzer Cyan-farbener Blitz breitet sich vom Klickpunkt aus.

------------------------------
## 5. UI-Struktur (Layout)

* Navigation: Linksbündig, schmal, einklappbar (Minimalismus).
* Hauptbereich: Ein „Canvas“-Layout (keine starren Boxen), in dem Dokumente wie in einer Mindmap durch Linien verbunden sind.
* Agenten-Konsole: Ein schmales Panel am rechten Rand, das im Monospace-Stil die aktuellen Gedankenschritte des Agenten in Echtzeit mitloggt.

 

