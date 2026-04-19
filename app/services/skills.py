from typing import List, Dict

SKILL_REGISTRY: List[Dict[str, str]] = [
    {
        "id": "advocatus_diaboli",
        "name": "Advocatus Diaboli",
        "category": "Metaphorisch",
        "ziel": "Schwachstellen und rechtliche Risiken gnadenlos aufdecken.",
        "prompt": "Agiere als Advocatus Diaboli für Verwaltungshandeln. Deine Aufgabe ist es, den vorliegenden Entwurf/Vorgang radikal infrage zu stellen. Suche gezielt nach:\n- Verfahrensfehlern: Wo wurden Fristen oder Beteiligungsschritte ignoriert?\n- Rechtlichen Lücken: Welche Norm wurde zu schwach ausgelegt?\n- Logischen Brüchen: Wo widerspricht sich die Begründung?\nGib keine konstruktive Kritik, sondern zerstöre die Argumentation fachlich fundiert, damit wir sie im nächsten Schritt wasserfest machen können."
    },
    {
        "id": "eighth_man_analysis",
        "name": "Eighth Man Analysis",
        "category": "Metaphorisch",
        "ziel": "Ganzheitliche Bewertung mit Fokus auf das eine 'Killer-Argument'.",
        "prompt": "Führe eine Eighth Man Analysis für den vorliegenden Sachverhalt durch.\nErstelle zuerst 7 Pro-Perspektiven, die jeweils einen anderen Fachbereich abdecken (z.B. IT-Sicherheit, Haushaltsrecht, Bürgerfreundlichkeit, Personalrat, Datenschutz, Effizienz, politisches Image).\nFormuliere abschließend 1 fundamentales Contra-Argument, das so schwer wiegt, dass es das gesamte Vorhaben zu Fall bringen könnte (Der 'Achte Mann', der widersprechen MUSS, wenn alle anderen zustimmen)."
    },
    {
        "id": "olfactory_extractor",
        "name": "Olfactory Extractor",
        "category": "Metaphorisch",
        "ziel": "Informationsextraktion nach dem Schichten-Modell (Parfüm-Prinzip).",
        "prompt": "Wende den Olfactory Extractor auf das Dokument an. Strukturiere die Analyse streng in vier Schichten:\n- Kopfnote (Flüchtig): Ein Abstract in maximal 3 Sätzen. Worum geht es sofort?\n- Herznote (Charakter): Was sind die zentralen Entscheidungskriterien und Abwägungen?\n- Basisnote (Langhaftend): Welche Gesetze, Verordnungen oder Aktenplan-Nummern bilden das rechtliche Fundament?\n- Der Flakon (Rahmen): Liste die Metadaten: Aktenzeichen, Ersteller, Datum und Aufbewahrungsfrist (sofern ersichtlich)."
    },
    {
        "id": "anforderungs_analyse",
        "name": "Anforderungs-Analyse",
        "category": "Metaphorisch",
        "ziel": "Transformation von Prosa in präzise technische/fachliche Vorgaben.",
        "prompt": "Agiere als Business Analyst für die öffentliche Verwaltung. Extrahiere aus dem vorliegenden Text eine strukturierte Anforderungsliste. Unterteile diese in:\n- Funktionale Anforderungen: Was muss das System/die Akte leisten?\n- Nicht-funktionale Anforderungen: (Sicherheit, Performance, Archivierung).\n- Stakeholder: Wer ist betroffen?\nNutze eine klare Priorisierung (Must-have, Should-have, Nice-to-have)."
    },
    {
        "id": "revisionist",
        "name": "Der Revisionist",
        "category": "Metaphorisch",
        "ziel": "Prüfung der Aktenmäßigkeit und Revisionssicherheit.",
        "prompt": "Agiere als Revisor des Landesrechnungshofs. Prüfe den Vorgang auf die Grundsätze ordnungsgemäßer Aktenführung. Achte besonders auf:\n- Nachvollziehbarkeit: Könnte ein unbeteiligter Dritter die Entscheidung in zwei Jahren noch verstehen?\n- Vollständigkeit: Fehlen Zwischenschritte oder logische Verknüpfungen?\n- Integrität: Werden rechtliche Rahmenbedingungen sauber zitiert?\nMarkiere jede Stelle, die bei einer Prüfung zu einer Rüge führen würde."
    },
    {
        "id": "buerger_prisma",
        "name": "Das Bürger-Prisma",
        "category": "Metaphorisch",
        "ziel": "Übersetzung von Behördenlogik in Bürger-Nutzen (UX).",
        "prompt": "Agiere als Ombudsperson für Bürgerbelange. Betrachte den vorliegenden Prozess/Text durch das Bürger-Prisma.\n- Wo führt das 'Behörden-Sprech' zu Missverständnissen?\n- Ist der Prozess für Menschen ohne juristisches Vorwissen handhabbar?\n- Mache drei konkrete Vorschläge, wie die Aktenführung oder Kommunikation transparenter und serviceorientierter gestaltet werden kann, ohne die Rechtssicherheit zu verlieren."
    },
    {
        "id": "echo_filter",
        "name": "Das Echo-Filter",
        "category": "Metaphorisch",
        "ziel": "Fernwirkungen von Aktenentscheidungen antizipieren.",
        "prompt": "Untersuche die Maßnahme/den Text auf ihr Echo in vier Wellen:\n1. Direkte Rechtswirkung\n2. Finanzielle Folgekosten\n3. Politische Außenwirkung\n4. Präzedenzfall-Charakter für künftige Aktenführungen."
    },
    {
        "id": "zeitkapsel_check",
        "name": "Der Zeitkapsel-Check",
        "category": "Metaphorisch",
        "ziel": "Bewertung des historischen Wertes und der digitalen Langzeitverfügbarkeit.",
        "prompt": "Agiere als Historiker des 22. Jahrhunderts. Bewerte dieses Artefakt nach dem Zeitkapsel-Prinzip: Sind die Informationen ohne heutiges Kontextwissen in 50 Jahren noch interpretierbar? Sind Abhängigkeiten zu kurzlebigen Technologien erkennbar? Entscheide argumentativ: Archivwürdig oder digitaler Datenmüll?"
    },
    {
        "id": "matroschka_strategie",
        "name": "Die Matroschka-Strategie",
        "category": "Metaphorisch",
        "ziel": "Prüfung der Konsistenz von der Strategie bis zur Einzelakte.",
        "prompt": "Wende die Matroschka-Analyse an: Zerlege das Vorhaben von der obersten politischen/strategischen Zielsetzung (Große Puppe) über die Fachstrategie und den Aktenplan bis hin zur kleinsten Einheit – der Einzelakte oder dem Datenfeld (Kleinste Puppe). Zeige auf, an welcher Stelle die strategische Absicht im operativen Klein-Klein verloren geht oder inkonsistent wird."
    },
    {
        "id": "aktenplan_strukturierer",
        "name": "Aktenplan-Strukturierer",
        "category": "Verwaltung",
        "ziel": "Erstellung einer logischen Hierarchie.",
        "prompt": "Agiere als Experte für Verwaltungsorganisation. Erstelle für das im Text behandelte Fachgebiet einen Entwurf für einen Aktenplan nach dem Prinzip der Aufgabenorientierung. Gliedere die Struktur in Hauptgruppen, Gruppen und Untergruppen. Achte darauf, dass die Systematik überschneidungsfrei ist und Raum für Querschnittsaufgaben sowie Fallakten lässt."
    },
    {
        "id": "schriftgut_designer",
        "name": "Schriftgutordnungs-Designer",
        "category": "Verwaltung",
        "ziel": "Definition von Verhaltensregeln und Standards für die Aktenführung.",
        "prompt": "Agiere als Organisationsberater in der öffentlichen Verwaltung. Entwirf basierend auf dem Dokument ein Kapitel für eine Schriftgutordnung. Berücksichtige dabei die Grundsätze der Aktenmäßigkeit, Nachvollziehbarkeit und Integrität. Formuliere verbindliche Regeln für die Bediensteten, wie Dokumente zu kennzeichnen und in das DMS zu übertragen sind."
    },
    {
        "id": "aktenzeichen_generator",
        "name": "Aktenzeichen-Generator",
        "category": "Verwaltung",
        "ziel": "Ableitung korrekter Metadaten aus dem Sachverhalt.",
        "prompt": "Du bist ein digitaler Registrator. Generiere basierend auf den Informationen aus dem Dokument ein systematisches Aktenzeichen. Erkläre kurz die Zusammensetzung des Zeichens (z. B. Betreffseinheit, Laufende Nummer, Jahreszahl)."
    },
    {
        "id": "fristen_analyst",
        "name": "Fristen-Analyst",
        "category": "Verwaltung",
        "ziel": "Ermittlung und Anwendung von Aufbewahrungsfristen.",
        "prompt": "Agiere als Archivar und Rechtsexperte. Analysiere das Dokument hinsichtlich enthaltener Dokumentenarten und Vorgänge. Ordne diesen rechtssichere Aufbewahrungsfristen nach geltendem Recht zu. Unterscheide zwischen 'Vernichten nach Fristablauf' und 'Anbieten an das Archiv'."
    },
    {
        "id": "e_akte_konzeptionaer",
        "name": "E-Akte Fachkonzeptionär",
        "category": "Verwaltung",
        "ziel": "Erarbeitung technischer und prozessualer Anforderungen für die Digitalisierung.",
        "prompt": "Agiere als IT-Business-Analyst für den öffentlichen Sektor. Erstelle basierend auf dem Kontext ein Fachkonzept für die Einführung/Handhabung der E-Akte. Definiere darin: 1. Das Berechtigungskonzept (Rollen), 2. Den Scan-/Digitalisierungsprozess und 3. Die Anforderungen an die Volltextsuche und Metadatenerfassung."
    },
    {
        "id": "kosten_detektiv",
        "name": "Der Kosten-Detektiv",
        "category": "Analyse & Strategie",
        "ziel": "Versteckte Kosten analysieren.",
        "prompt": "Analysiere versteckte Kosten im Kontext des Dokuments: Personalkosten, Opportunitätskosten, Wartung, Schulung, Migration. Erstelle eine Schätzung der Total Cost of Ownership (TCO) über 5 Jahre."
    },
    {
        "id": "praezedenz_jaeger",
        "name": "Der Präzedenz-Jäger",
        "category": "Analyse & Strategie",
        "ziel": "Ähnliche Fälle und Muster identifizieren.",
        "prompt": "Suche im Sachverhalt nach Präzedenzfällen oder Mustern. Welche ähnlichen Entscheidungen wurden in der Verwaltungspraxis typischerweise getroffen? Welche Fehler oder Grundsatzentscheidungen wiederholen sich?"
    },
    {
        "id": "stakeholder_kartograph",
        "name": "Der Stakeholder-Kartograph",
        "category": "Analyse & Strategie",
        "ziel": "Erstellung einer Stakeholder-Matrix.",
        "prompt": "Erstelle eine Stakeholder-Matrix aus dem vorliegenden Text: Wer ist betroffen? Stelle Einfluss vs. Interesse gegenüber. Definiere konkret: Wer muss informiert werden, wer muss beteiligt werden?"
    },
    {
        "id": "prozess_chirurg",
        "name": "Der Prozess-Chirurg",
        "category": "Analyse & Strategie",
        "ziel": "Zerlegung und Analyse von Prozessen.",
        "prompt": "Zerlege den im Dokument beschriebenen Prozess in Einzelschritte. Identifiziere gnadenlos: Bottlenecks, Redundanzen, Automatisierungspotenzial und Medienbrüche."
    },
    {
        "id": "compliance_scanner",
        "name": "Der Compliance-Scanner",
        "category": "Analyse & Strategie",
        "ziel": "Prüfung gegen rechtliche Rahmenbedingungen.",
        "prompt": "Prüfe den Sachverhalt gegen gängige Compliance-Richtlinien (z.B. DSGVO, IFG, VwVfG, GoBD, BITV). Markiere potenzielle Verstöße und Risiken. Erstelle einen fiktiven Compliance-Score."
    },
    {
        "id": "behoerden_uebersetzer",
        "name": "Der Übersetzer",
        "category": "Kommunikation",
        "ziel": "Zielgruppengerechte Übersetzung von Behördentexten.",
        "prompt": "Übersetze die Kernaussagen des Dokuments in: 1. Leichte Sprache, 2. Einen kurzen englischen Abstract, 3. Eine Version für die politische Leitungsebene (Management Summary)."
    },
    {
        "id": "krisen_simulator",
        "name": "Der Krisen-Simulator",
        "category": "Kommunikation",
        "ziel": "Simulation von Worst-Case-Szenarien.",
        "prompt": "Simuliere basierend auf dem Vorhaben 3 Worst-Case-Szenarien: Was passiert bei einem Datenleck, einem gravierenden Fristversäumnis oder plötzlichem politischen Gegenwind? Erstelle pro Szenario einen groben Notfallplan."
    },
    {
        "id": "automatisierungs_scout",
        "name": "Der Automatisierungs-Scout",
        "category": "Optimierung",
        "ziel": "Identifikation von Automatisierungspotenzial.",
        "prompt": "Identifiziere das Automatisierungspotenzial im beschriebenen Sachverhalt: Wo können RPA, KI oder Workflows helfen? Schätze das Aufwand/Nutzen-Verhältnis und priorisiere 2-3 Quick Wins."
    },
    {
        "id": "wissens_destillierer",
        "name": "Der Wissens-Destillierer",
        "category": "Optimierung",
        "ziel": "Extraktion von implizitem Wissen.",
        "prompt": "Extrahiere das implizite Wissen aus dem Text: Wer weiß in diesem Konstrukt was? Wo sitzen die wahren Experten oder Engpässe? Erstelle eine kurze Wissenslandkarte."
    },
    {
        "id": "zukunfts_prophet",
        "name": "Der Zukunfts-Prophet",
        "category": "Optimierung",
        "ziel": "Prognose von Entwicklungen.",
        "prompt": "Prognostiziere die Entwicklung des Sachverhalts über die nächsten 3 Jahre: Welche rechtlichen oder gesellschaftlichen Änderungen könnten relevant werden? Welche Technologien könnten den Prozess überholen? Erstelle eine proaktive Roadmap."
    },
    {
        "id": "konsistenz_waechter",
        "name": "Der Konsistenz-Wächter",
        "category": "Qualität",
        "ziel": "Prüfung auf logische und datenbezogene Konsistenz.",
        "prompt": "Prüfe die Konsistenz des Textes: Suche aktiv nach Widersprüchen in Zahlen, Daten, Zuständigkeiten oder Zeitachsen. Erstelle einen Abweichungsbericht der gefundenen logischen Fehler."
    },
    {
        "id": "barrierefreiheits_checker",
        "name": "Der Barrierefreiheits-Checker",
        "category": "Qualität",
        "ziel": "Prüfung auf Barrierefreiheit.",
        "prompt": "Prüfe den Sachverhalt (soweit textlich möglich) nach Kriterien der Barrierefreiheit (z.B. BITV 2.0). Ist die Sprache verständlich? Werden Alternativen mitgedacht? Erstelle eine konzeptionelle Mängelliste."
    }
]

def get_all_skills() -> List[Dict]:
    return SKILL_REGISTRY

def get_skill_by_id(skill_id: str) -> Dict | None:
    for skill in SKILL_REGISTRY:
        if skill["id"] == skill_id:
            return skill
    return None
