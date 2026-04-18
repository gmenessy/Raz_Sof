HTML: Die Struktur
html
<div class="raz-card">
  <div class="raz-glow"></div>
  <div class="raz-header">
    <span class="raz-tag">Knoten_042</span>
    <div class="raz-status-pulse"></div>
  </div>
  <h3 class="raz-title">Strategie_Raziel_Alpha.pdf</h3>
  <p class="raz-excerpt">Analyse der verborgenen Wissenspfade und deren agentische Implementierung...</p>
  <div class="raz-footer">
    <button class="raz-action-btn">Enthüllen</button>
    <code class="raz-meta">Action_Ready</code>
  </div>
</div>
Verwende Code mit Vorsicht.
CSS: Das Styling (Cyber-Mystik)
css
:root {
  --midnight: #020408;
  --raz-violet: #6E44FF;
  --inf-cyan: #00F5FF;
  --starlight: #E0E6ED;
  --glass: rgba(15, 20, 28, 0.7);
}

.raz-card {
  background: var(--glass);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(110, 68, 255, 0.2);
  border-radius: 8px;
  padding: 20px;
  width: 300px;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
  color: var(--starlight);
  transition: all 0.3s ease;
}

/* Der subtile Hintergrund-Glow */
.raz-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(110, 68, 255, 0.05) 0%, transparent 70%);
  pointer-events: none;
}

.raz-card:hover {
  border-color: var(--inf-cyan);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.15);
  transform: translateY(-5px);
}

.raz-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--raz-violet);
  text-transform: uppercase;
}

.raz-title {
  font-family: 'Michroma', sans-serif;
  font-size: 1.1rem;
  margin: 15px 0 10px 0;
  letter-spacing: 1px;
}

.raz-excerpt {
  font-size: 0.85rem;
  color: #64748B;
  line-height: 1.5;
}

.raz-action-btn {
  background: transparent;
  border: 1px solid var(--inf-cyan);
  color: var(--inf-cyan);
  padding: 8px 16px;
  font-family: 'Michroma', sans-serif;
  font-size: 0.7rem;
  cursor: pointer;
  transition: 0.3s;
  text-transform: uppercase;
}

.raz-action-btn:hover {
  background: var(--inf-cyan);
  color: var(--midnight);
  box-shadow: 0 0 15px var(--inf-cyan);
}

.raz-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  float: right;
  margin-top: 12px;
  opacity: 0.5;
}
Verwende Code mit Vorsicht.
Die Besonderheiten dieses Designs:
Backdrop-Blur: Die Karte wirkt wie dunkles, halbtransparentes Glas.
Michroma & Inter: Der Kontrast zwischen der weiten Überschrift und dem klaren Fließtext erzeugt den „High-Tech-Orakel“-Vibe.
Interaktiver Glow: Beim Hovern wechselt der Fokus von Violett (Wissen) zu Cyan (Aktion/Agent).


Um die agentische Planung von Raz_Sof visualisiert darzustellen, nutzen wir ein Node-Link-Layout. Dokumente (Knoten) schweben im Raum und werden durch dynamische „Pfade“ (Verbindungen) verknüpft, sobald der Agent eine logische Brücke schlägt.
1. Das Konzept: „The Neural Web“
Anstatt einer Liste liegen die Dokumente auf einer unendlichen Leinwand (Canvas).
Knoten (Nodes): Die raz-card von vorhin, aber in einer kompakteren Version.
Pfade (Edges): Feine, pulsierende Linien in Infinite Cyan, die anzeigen, wie der Agent Informationen kombiniert.
Fokus: Der aktive Pfad leuchtet stärker, während irrelevante Dokumente im „Nebel“ (Midnight Void) verschwinden.
2. Technisches Layout (CSS Connector-Logik)
Hier ist ein erweitertes Code-Beispiel, um die Karten in einem Netzwerk-Kontext zu positionieren:
html
<div class="raz-canvas">
  <!-- Verbindungslinie (SVG für Skalierbarkeit) -->
  <svg class="raz-connections">
    <line x1="150" y1="100" x2="450" y2="300" class="raz-path-active" />
  </svg>

  <!-- Dokument 1 -->
  <div class="raz-node" style="top: 50px; left: 50px;">
    <div class="raz-card-mini">
      <span class="raz-tag">Ursprung</span>
      <h4>Analyse_Kern_A</h4>
    </div>
  </div>

  <!-- Dokument 2 -->
  <div class="raz-node" style="top: 250px; left: 400px;">
    <div class="raz-card-mini active-glow">
      <span class="raz-tag">Ableitung</span>
      <h4>Handlungsplan_B</h4>
    </div>
  </div>
</div>
Verwende Code mit Vorsicht.
3. CSS für das Netzwerk-Gefühl
css
.raz-canvas {
  background-color: var(--midnight);
  background-image: radial-gradient(circle at 2px 2px, rgba(110, 68, 255, 0.1) 1px, transparent 0);
  background-size: 40px 40px; /* Ein dezentes Punktraster */
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.raz-connections {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.raz-path-active {
  stroke: var(--inf-cyan);
  stroke-width: 1.5;
  stroke-dasharray: 10;
  animation: flow 20s linear infinite;
  filter: drop-shadow(0 0 5px var(--inf-cyan));
}

@keyframes flow {
  from { stroke-dashoffset: 200; }
  to { stroke-dashoffset: 0; }
}

.raz-node {
  position: absolute;
  z-index: 10;
}

.active-glow {
  border: 1px solid var(--inf-cyan) !important;
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.2);
}
Verwende Code mit Vorsicht.
4. Die agentische Interaktion
Wenn der Nutzer auf „Planung starten“ klickt:
Die Kamera im Interface zoomt sanft heraus.
Die SVG-Linien beginnen von einem Dokument zum nächsten zu „fließen“ (Animation: flow).
Im rechten Bereich der Website öffnet sich die Agenten-Konsole im Monospace-Stil und zeigt den Text: RAZ_SOF: Verknüpfe Knoten_042 mit Knoten_089... Strategie wird projiziert.
5. Zusammenfassung der Visuals
Hintergrund: Dunkles Raster (Gefühl von unendlicher Kapazität).
Bewegung: Alles ist im Fluss, nichts ist starr.
Farben: Nur Violett für die Struktur und Cyan für die aktuelle Bewegung.
