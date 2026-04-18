# Gesamtanforderungsspezifikation: Agentische Akten-, Dokumenten- und Wissensplattform

## Zweck und Zielbild

Ziel ist die Konzeption und schrittweise Umsetzung einer mandantenfähigen, agentischen Plattform zur Verwaltung, Analyse, Planung, Verdichtung und Nutzung von Akten, Dokumenten und aktenübergreifendem Wissen. Die Plattform soll Rohquellen in Form von Akten und Dokumenten verwalten, deren Essenz extrahieren, aktive Planungs- und Analyseunterstützung liefern, widersprüchliches Wissen aushandeln und daraus eine mandantenbezogene, persistent gepflegte Live-Wiki aufbauen. Agentic-AI-Architekturen eignen sich insbesondere für solche wissensintensiven Enterprise-Workflows, wenn sie mit klaren Governance-Regeln, Multi-Agent-Orchestrierung und menschlichen Freigabepunkten kombiniert werden. [web:181][web:182][web:183]

Die Plattform folgt den Leitprinzipien **Leichtgewichtigkeit**, **Agentic AI First**, **Automation second**, **Human in the Loop am Ende**, **maximale UI/UX-Erfahrung**, **Priorisierung von Aha- und Wow-Effekten** sowie **frühe Nutzbarkeit mit realem Zeitgewinn und proaktiven Aktionen**. MVP- und Agentic-AI-Leitfäden empfehlen ausdrücklich, frühe Ausbaustufen auf sofort nutzbare Kernjobs, sichtbare Produktivitätseffekte und progressive Wertlieferung auszurichten. [web:172][web:175][web:178]

## Produktprinzipien

Die Lösung soll von Anfang an nicht nur Daten verwalten, sondern fachliche Arbeit aktiv beschleunigen. Das System soll zuerst denken, dann vorschlagen und erst vor persistierenden oder risikobehafteten Aktionen einen Menschen einbeziehen. Human-in-the-loop-Pattern gelten insbesondere bei kritischen Entscheidungen, sensiblen Dokumenten und extern wirksamen Änderungen als geeigneter Governance-Mechanismus. [web:166][web:168][web:186]

Die Plattform soll keine generische „Chat mit Dateien“-Oberfläche sein, sondern eine produktive Arbeitsumgebung, die Sachverhalte sichtbar macht, Konflikte aufdeckt, Folgeaktionen empfiehlt und Ergebnisse in verwertbare Artefakte überführt. Agentic-AI-Plattformen entfalten laut Enterprise-Analysen ihren Mehrwert besonders dort, wo sie Analyse, Entscheidungsvorbereitung und kontrollierte Ausführung verbinden. [web:180][web:183][web:192]

## Geltungsbereich

Die Spezifikation umfasst fachliche, technische und gestalterische Anforderungen an eine browserbasierte Webanwendung mit Python-Backend, Vanilla-Web-Frontend, OpenAI-kompatibler LLM-Anbindung, Mandantenfähigkeit, Rollenkonzept, Akten- und Dokumentverwaltung, Wissensdatenbank, Live-Wiki, Skill-System, Planung, Exporten, Auditierbarkeit, Policy-Kontrollen und schrittweiser DMS-Integration. OpenAI-kompatible Server und Router ermöglichen dabei die Anbindung unterschiedlicher Modelle und Provider über ein einheitliches API-Schema. [web:184][web:187][web:193]

## Fachliche Leitideen

- Rohdokumente und Akten bleiben die **Source of Truth**.
- Wissen wird aus Quellen extrahiert, verdichtet, versioniert und in einer persistenten Wissensschicht gepflegt.
- Neues Wissen darf altes Wissen überschreiben, jedoch nie still löschen; historische Versionen bleiben nachvollziehbar erhalten.
- Persistente, externe oder risikobehaftete Aktionen erfordern menschliche Freigabe.
- Früheste Produktstufen müssen bereits einen klaren Zeitgewinn erzeugen und proaktive Unterstützung leisten. [web:172][web:181][web:182]

## Mandantenmodell

Das System ist mandantenfähig. Jeder Mandant stellt einen logisch getrennten Arbeits-, Daten-, Rechte- und Wissensraum dar. Mandantenfähige Systeme benötigen eine klare Isolation von Daten, Konfiguration und Sichtbarkeit, insbesondere in Multi-Tenant-Umgebungen mit unterschiedlichen organisatorischen Zuständigkeiten. [web:189][web:184]

Ein systemweiter **Admin** kann Mandanten erstellen und besitzt administrative Vollrechte über alle Mandanten hinweg. Inhalte, Wiki-Räume, Akten, Dokumente, Skills, Konfigurationen und Exporte sind grundsätzlich mandantenspezifisch zu behandeln, soweit nicht ausdrücklich systemweit freigegebene Verwaltungsfunktionen betroffen sind. [web:182][web:189]

## Rollenmodell

Innerhalb des Systems gelten mindestens folgende Rollen:

| Rolle | Rechte |
|---|---|
| **Admin** | Kann Mandanten erstellen, besitzt alle Rechte in allen Mandanten, verwaltet Nutzer, Rollen, Richtlinien, Skills, Integrationen, Exporte, Logs und Systemeinstellungen. |
| **Planer (Mandanten-Admin)** | Darf innerhalb seines Mandanten Akten und Wissensdatenbanken erstellen und bearbeiten, Dokumente hinzufügen oder löschen, Analysen, Reports und Planungen durchführen sowie das Wiki lesen und freigaberelevante Inhalte bearbeiten. |
| **Analyst** | Darf innerhalb einer Akte Anfragen, Analysen und Planungen durchführen, jedoch nur im Rahmen der ihm zugewiesenen Akten und ohne mandantenweite Administration. |
| **User** | Darf Akten lesen, chatten und Dashboards ansehen, aber keine Schreib- oder Persistenzoperationen ausführen. |

Der Wiki-Bereich ist mandantenbezogen und nur für **Planer** und **Admin** sichtbar. Analysten und User erhalten keinen direkten Sichtzugriff auf das Wiki. Policy-basierte Rechtevergabe und klare Accountability-Zuordnung sind bei agentischen Multi-User-Systemen zentrale Governance-Bausteine. [web:182][web:189]

## Statusmodell

### Akte

Eine Akte besitzt genau zwei Status:
- **aktiv**
- **archiviert**

Ist eine Akte **aktiv**, sind Lesen, Chat, Analyse und Planung gemäß Rollenmodell zulässig. Ist eine Akte **archiviert**, ist sie ausschließlich lesend zugänglich; weitere Planungen, operative Fortschreibungen und inhaltliche Schreiboperationen sind unzulässig. Menschliche Freigabepunkte für sensible und finale Aktionen entsprechen dem Human-in-the-loop-Designpattern für kritische Entscheidungen. [web:186][web:183]

### Wissensdatenbank

Eine Wissensdatenbank ist stets **aktiv**. Sie dient als dauerhaft gepflegte, lebende Wissensbasis und kennt keinen Archivstatus. Wissen kann dort auf Basis neuer Informationen aktualisiert werden, wobei ältere Wissensstände versioniert und nachvollziehbar erhalten bleiben. [web:181][web:180]

### Wiki

Das Wiki ist **mandantenbezogen**. Jeder Mandant besitzt einen eigenen Wiki-Raum. Wissen aus archivierten Akten bleibt erhalten und darf durch neuere Informationen überschrieben werden, jedoch ausschließlich unter Beibehaltung historischer Versionen und Entscheidungsprotokolle. [web:182][web:191]

## Wissens- und Konfliktregeln

Neues Wissen darf bestehendes Wissen nicht still ersetzen, wenn widersprechende Evidenz vorliegt. Stattdessen eröffnet das System einen **Wissenskonfliktfall**. Multi-Agent-Systeme lösen Konflikte typischerweise über strukturierte Kommunikation, Moderation, Abstimmung oder Verhandlung; diese Mechanismen eignen sich auch für widersprüchliches Fachwissen in Wikis und Wissensdatenbanken. [web:185][web:188][web:191]

Der Standardmechanismus zur Konfliktauflösung ist ein **LLM-basierter Aushandlungs-Skill**. Dabei vertreten mindestens mehrere Agenten gegensätzliche Positionen zur bestehenden und neuen Wissenslage, während ein Moderator- oder Judge-Agent eine belastbare Synthese erzeugt. Agentic-AI-Umgebungen mit klaren menschlichen Freigabepunkten und Multi-Agent-Orchestrierung gelten als geeigneter Ansatz für komplexe, widersprüchliche Wissenslagen. [web:183][web:185][web:191]

Im Wiki wird ein Wissenskonflikt sichtbar gemacht durch:
- Statuskennzeichnung wie „stabil“, „in Prüfung“, „umstritten“, „abgelöst“, „historisch“.
- Versionsvergleich zwischen alter und neuer Wissensfassung.
- Verlinkung auf Quellen, Debattenprotokoll und Entscheidungsverlauf.
- Kennzeichnung der aktuell gültigen Leitfassung.

Die finale Übernahme einer neuen Wissensfassung erfolgt durch eine berechtigte Rolle im Human-in-the-loop-Schritt, mindestens durch einen Planer, bei sensiblen Fällen zusätzlich durch einen Admin. Human Approval Gates für high-impact decisions sind ein zentrales Governance-Prinzip agentischer Systeme. [web:182][web:186]

## Fachliche Hauptfunktionen

### Aktenverwaltung

Das System muss Akten anlegen, lesen, klassifizieren, versionieren, archivieren und rollenbasiert zugänglich machen. Zu einer Akte müssen Dokumente, Notizen, Aufgaben, Fristen, Statusinformationen, Konflikthinweise und Verweise auf verwandte Inhalte zugeordnet werden können. Agentische Enterprise-Plattformen erzeugen besonderen Mehrwert, wenn sie strukturierte Vorgänge mit kontextbezogener Intelligenz anreichern. [web:180][web:192]

### Dokumentstore

Das System muss Dokumente verschiedener Typen speichern, versionieren und einer oder mehreren Akten zuordnen können. In frühen Entwicklungsstufen erfolgt der Import per Datei-Upload und URL; in der Produktionsphase ist eine Integration mit dem DMS per API vorzusehen. Multi-Model- und Agentic-Plattformen profitieren von klar getrennten Ingest-Schichten und Tool-Interfaces. [web:183][web:189]

### Essenzextraktion

Das System muss aus Dokumenten und Akten automatisiert Essenzen erzeugen. Diese Essenzen enthalten Kernaussagen, Sachverhalt, Risiken, offene Punkte, Handlungsimplikationen und relevante Metadaten. Frühe AI-Produkte liefern besonders hohen Nutzen, wenn sie den manuellen Lese- und Strukturierungsaufwand drastisch reduzieren. [web:172][web:180]

### Indexbildung

Für jede Akte muss ein kompakter Index erzeugt werden, der „auf einen Blick“ sichtbar macht, worum es geht. Der Index soll mindestens Gegenstand, Sachverhalt, Beteiligte, relevante Zeitpunkte, Fristen, Risiken, Konflikte, offene Aufgaben und Dokumentenlage enthalten. UI-seitig soll dieser Index nicht als rohe Tabelle, sondern als verständlicher, visuell priorisierter Einstieg in die Akte erscheinen. Eine AI-first UX sollte kontextbezogene Orientierung und nächste Schritte sichtbar machen. [web:174][web:176]

### Chat mit Dokumentstore und Akten

Das System muss dialogischen Zugriff auf Dokumente, Dokumentmengen, einzelne Akten und Aktenbestände ermöglichen. Nutzer sollen in natürlicher Sprache fragen, recherchieren und Folgefragen stellen können. Der Chat soll quellenbezogene Antworten liefern und nach Möglichkeit direkt sinnvolle nächste Aktionen vorschlagen. HITL-Systeme und agentische Plattformen entfalten ihren Mehrwert dort, wo sie Handlungsvorschläge mit kontrollierter Eskalation kombinieren. [web:183][web:186]

### Planung

Das System muss Planungen gegenüber Akten und Dokumentlagen durchführen können. Dazu zählen Maßnahmenpläne, Vorgehensvorschläge, Risikoabschätzungen, Entscheidungsvorlagen, Alternativen, Priorisierungen und Folgeaktivitäten. Eine archivierte Akte darf nicht weiter geplant werden. [web:183][web:186]

### Reports und Analysen

Das System muss Analysen, Reports und weitere fachliche Auswertungen auf Basis von Akten, Dokumenten, Wissensobjekten und Planungen erzeugen können. Dabei sind sowohl ad-hoc-Anfragen als auch proaktive Anstöße durch Agenten zu unterstützen. Frühe Produktstufen sollen insbesondere Zeit sparen, indem sie aus Rohmaterial rasch belastbare Entwürfe erzeugen. [web:172][web:175]

### Live-Wiki nach LLM-Wiki-Prinzip

Die Plattform muss eine mandantenbezogene Live-Wiki pflegen, in der aktenübergreifendes Wissen persistent verdichtet und laufend aktualisiert wird. Wissen wird dort nicht nur bei Anfrage ad hoc rekonstruiert, sondern als wartbare, versionierte Wissensschicht geführt. Agentic-AI-Architekturen mit kontinuierlicher Wissenspflege und Decision Traces stärken Nachvollziehbarkeit und Wiederverwendbarkeit. [web:181][web:182]

## Skill-System

Die Plattform muss ein versioniertes Skill-System bereitstellen. Skills sind standardisierte agentische Arbeitsmodule mit definierter Zielsetzung, Eingabestruktur, Ausgabestruktur, Qualitätskriterien, Modellprofil und Fallback-Verhalten. Da unterschiedliche Modelle verschiedene Fähigkeiten und Grenzen haben, ist ein robustes, modellagnostisches Skill-Design zentral. OpenAI-kompatible Multi-Model-Architekturen unterstützen genau diese lose Kopplung zwischen Fachlogik und Modellwahl. [web:184][web:187][web:193]

### Anforderungen an Skills

- Jeder Skill muss klaren Zweck, Eingaben, Ausgaben und Qualitätskriterien definieren.
- Jeder Skill muss mit größeren und kleineren Modellen funktionsfähig sein.
- Jeder Skill muss versioniert, testbar und auditierbar sein.
- Jeder Skill muss Quellenbezug und Entscheidungsnachweise unterstützen.
- Jeder Skill muss in Planungs-, Analyse-, Qualitäts- oder Exportprozesse integrierbar sein.

### Metaphorische Analyse-Skills

Folgende Skills sind verbindlich vorzusehen:
- **Advocatus Diaboli**: destruktive Gegenprüfung von Verwaltungshandeln.
- **Eighth Man Analysis**: 7 Pro-Perspektiven und 1 fundamentales Contra.
- **Olfactory Extractor**: Analyse in Kopfnote, Herznote, Basisnote, Flakon.
- **Anforderungs-Analyse**: Transformation von Prosa in strukturierte Anforderungen.
- **Der Revisionist**: Prüfung auf Aktenmäßigkeit und Revisionssicherheit.
- **Das Bürger-Prisma**: Übersetzung von Behördenlogik in Bürgerperspektive.
- **Das Echo-Filter**: Bewertung von Fernwirkungen über vier Wellen.
- **Der Zeitkapsel-Check**: Bewertung von Langzeitlesbarkeit und Archivwürdigkeit.
- **Die Matroschka-Strategie**: hierarchischer Drill-down von Strategie bis Einzelmetadatum.

### Verwaltungs-Skills

Folgende verwaltungsfachlichen Skills sind verbindlich vorzusehen:
- **Aktenplan-Strukturierer**
- **Schriftgutordnungs-Designer**
- **Aktenzeichen-Generator**
- **Fristen-Analyst**
- **E-Akte Fachkonzeptionär**

### Datenqualitäts-Skill

Es ist ein dedizierter **LLM-Datenqualitäts-Skill** vorzusehen, der Dubletten, fehlende Metadaten, inkonsistente Klassifikationen, Widersprüche, Veraltungsrisiken, Konfidenzprobleme und terminologische Abweichungen identifiziert. Agentische Systeme benötigen laut Governance-Analysen laufendes Monitoring, Decision Traces und Qualitätskontrollen, um Drift und inkonsistentes Verhalten zu beherrschen. [web:179][web:182]

## Export- und Publikationsfunktionen

Das System muss auf Anfrage oder aus Planungssituationen heraus Exporte erzeugen können. Unterstützt werden mindestens:
- Präsentation
- Bericht
- Blogbeitrag
- Social-Media-Beiträge
- PDF
- Word-Dokument
- PowerPoint
- weitere formatierbare Zielformate über Skills oder Templates

Exporte dürfen frontendseitig oder backendseitig erstellt werden. Entscheidend ist, dass Vorlagen, Bausteine, Layoutregeln und allgemeine CI-Informationen berücksichtigt werden können. Persistente oder externe Exporte sind vor finaler Freigabe in den Human-in-the-loop-Prozess einzubinden. [web:186][web:183]

## Technische Architektur

### Backend

Das Backend muss in **Python** implementiert werden. Es umfasst API-Schicht, Orchestrierung, Ingest, Skill-Ausführung, Planungsdienste, Wiki-Pflege, Exportdienste, Policy-Prüfung, Auditierung und Integrationen. Python ist im LLM- und Agentic-Umfeld besonders geeignet, da Modellorchestrierung, API-Integration und Datenverarbeitung dort breit unterstützt werden. [web:184][web:181]

### LLM-Schicht

Alle Modellaufrufe müssen ausschließlich über eine **OpenAI-kompatible API** erfolgen. Dabei ist die Nutzung mehrerer Modelle und Anbieter über ein einheitliches Routing-/Gateway-Prinzip vorzusehen. OpenAI-kompatible Router und Server erlauben Modellwechsel, Fallbacks, Kostenoptimierung und Providerabstraktion mit geringem Einfluss auf die Fachlogik. [web:184][web:187][web:193]

Es sind unterschiedliche Modellprofile für Chat, Extraktion, Planung, Qualitätsprüfung, Konfliktaushandlung und Export zu unterstützen. Multi-Agent- und Agentic-Plattformen profitieren von task-spezifischer Modellzuordnung statt eines einzigen Universalmodells. [web:183][web:184]

### Frontend

Das Frontend muss mit **Vanilla HTML5**, **CSS3** und **Vanilla JavaScript** umgesetzt werden. Ziel ist eine leichtgewichtige, performante, modulare und designstarke Webanwendung. Die UX muss „Aha“- und „Wow“-Momente priorisieren, ohne in unnötige Komplexität oder Framework-Overhead abzugleiten. Eine AI-first UX soll Verstehen, Handeln und Kontrollieren sichtbar und unmittelbar erfahrbar machen. [web:174][web:176]

## UI/UX-Leitbild

Die Benutzeroberfläche ist als produktive Agentic-Workbench zu konzipieren, nicht als bloßer Formular- oder Dateibrowser. Folgende Erlebnismomente sind prioritär:

- **Aha: Sofort-Verstehen** – Ein Dokument oder eine Akte wird binnen Sekunden in einen verständlichen Sachverhaltsraum überführt.
- **Aha: Der Agent denkt mit** – Antworten enthalten nicht nur Inhalte, sondern auch Risiken, nächste Schritte und offene Fragen.
- **Aha: Wissen vernetzt sich** – Relevante Querverbindungen erscheinen kontextbezogen und automatisch.
- **Wow: Ein Klick zu Artefakt** – Aus Analyse oder Planung wird sofort ein nutzbarer Bericht oder eine Präsentation.
- **Wow: Konflikte werden sichtbar** – Widersprüche erscheinen als nachvollziehbare Debatte oder Konfliktansicht statt als versteckte Inkonsistenz.

AI-first UX-Ansätze empfehlen, Nutzer nicht in Menüs, sondern in kontextbezogene Denk- und Handlungsflüsse zu führen. [web:170][web:174][web:176]

## Agentic-AI-First-Interaktionsmodell

Die Plattform folgt einem **Agentic AI First**-Ansatz:
- Agenten bilden die primäre Denk- und Assistenzschicht.
- Automation folgt aus Agentenempfehlungen und Richtlinien, nicht umgekehrt.
- Der Mensch sitzt am Ende des kritischen Entscheidungswegs.
- Nicht-kritische, nicht-persistente Aktionen dürfen voll agentisch erfolgen.

Dieses Modell entspricht aktuellen Governance-Empfehlungen, nach denen Menschen an den relevanten Eskalations- und Commit-Punkten eingebunden werden sollten, nicht bei jedem Zwischenschritt. [web:166][web:182][web:186]

## Proaktive Aktionen

Die Plattform muss schon in frühen Entwicklungsstufen proaktive Aktionen vorschlagen oder vorbereiten können. Dazu zählen insbesondere:
- Hinweis auf unvollständige Akten.
- Erkennung fehlender Risiko- oder Qualitätsprüfungen.
- Hinweis auf widersprüchliche Wissenslagen.
- Vorschlag passender Analyse- oder Planungsskills.
- Vorschlag zur Wissensextraktion aus archivierungsreifen Akten.
- Vorschlag, aus Analyse oder Planung direkt ein Artefakt zu erzeugen.

Der proaktive Layer ist für frühen Nutzwert zentral, weil er Zeit spart und relevante Folgeaktionen initiiert, ohne dass Nutzer jede nächste Handlung selbst antizipieren müssen. [web:172][web:175][web:183]

## Human-in-the-Loop-Modell

Das System unterscheidet drei Zonen:

- **Grüne Zone**: rein lesende, temporäre, nicht-persistente Aktionen; voll agentisch zulässig.
- **Gelbe Zone**: fachlich wirksame Entwürfe und Empfehlungen; Nutzer bestätigt nach kompaktem Decision Sheet.
- **Rote Zone**: persistente, externe oder risikoreiche Aktionen; nur mit expliziter Freigabe.

Ein Decision Sheet muss mindestens Ziel, Quellenlage, Modell-/Skill-Herkunft, Konflikte, erwartete Auswirkungen und Rollback-Hinweise zeigen. Human checkpoints für high-impact actions sind ein zentrales Agentic-AI-Governance-Muster. [web:182][web:186]

## Policy Engine und Objektrechte

Vor jeder persistenten Operation muss eine **Policy Engine** prüfen, ob Rolle, Mandantenkontext, Objektstatus, Konfliktlage und Richtlinie die Aktion erlauben. Mandantenbezogene Konfiguration, Auditierbarkeit und Policy-basierte Guardrails sind zentrale SOTA-Prinzipien für agentische Multi-Tenant-Plattformen. [web:189][web:182]

Mindestens folgende Objektklassen sind rechtegesteuert abzubilden:
- Akte
- Dokument
- Wissensdatenbank-Eintrag
- Wiki-Seite
- Skill
- Planung
- Export
- Integrationsziel

## AI Runtime Controls

Neben Prozessgovernance sind Laufzeitkontrollen erforderlich. Dazu gehören:
- Prompt-Logging
- Response-Logging
- Policy-Prüfungen vor Persistenz
- Fallback auf alternative Modelle
- Kill-Switch pro Modell oder Skill
- Incident Logging
- Monitoring von Drift, Konfliktrate und Agentenverhalten

Governance-Rahmen für agentische Systeme betonen ausdrücklich kontinuierliches Monitoring, Decision Traces und adaptive Policy Updates. [web:179][web:182][web:183]

## Audit und Lineage

Jede fachlich relevante Aktion muss nachvollziehbar sein. Ein Lineage-Standard ist vorzusehen:

**Quelle → Skill → Modell → Ergebnis → Freigabe → Zielobjekt**

Für Upload, Analyse, Skill-Ausführung, Planung, Wiki-Änderung, Konfliktlösung, Export und Archivierung sind Audit-Logs mit Zeit, Rolle, Mandant, Input, Output und Entscheidungsgrund zu führen. AI-Dokumentation und Decision Traces gelten als zentrale Grundlage für Accountability und Governance. [web:179][web:182]

## Integrationsmodell

### Frühphase

Die erste Entwicklungsstufe muss bereits nützlich sein. Import erfolgt zunächst über:
- Datei-Upload
- URL-Einspielung

### Produktionsphase

Für die Produktionsphase ist eine DMS-Integration per API vorzusehen. Diese Integration muss lesend beginnen und perspektivisch kontrollierte Schreib- oder Synchronisationspfade unterstützen, sofern Governance und Freigaben dies zulassen. Sichere APIs und kontrollierte Enterprise-Integration sind typische Bausteine agentischer Plattformen. [web:183][web:184]

## Entwicklungsstufen

### Stufe 1 – Understand

Upload/URL → Essenz → Index → Chat. Ziel ist, dass eine Akte oder ein Dokument binnen kurzer Zeit verständlich wird und sofort Zeit spart. Frühe MVP-Stufen sollten auf einen klaren Kernjob mit sofort sichtbarem Nutzen fokussieren. [web:172][web:175]

### Stufe 2 – Assist

Analyse-Skills, proaktive Hinweise, Planungsentwürfe und Risiko-Checks. Ziel ist weniger Such- und Denkaufwand sowie frühzeitige Handlungsvorschläge. [web:175][web:183]

### Stufe 3 – Decide

Wissenskonflikte, Review-Flows, Wiki-Vorschläge und Freigabeschritte. Ziel ist höhere Qualität und bessere Steuerbarkeit. [web:182][web:185]

### Stufe 4 – Execute

DMS-Integration, kontrollierte Exporte, teilautonome Workflows und produktive Policy-Kontrollen. Ziel ist echte operative Wirkung unter Governance. [web:183][web:189]

## Nutzen- und Erfolgsmessung

Die Plattform ist an ihrem realen Zeitgewinn und ihrer Proaktivität zu messen. Daher sind mindestens folgende Metriken vorzusehen:
- Zeit bis zum ersten Aktenverständnis
- Zeitersparnis gegenüber manueller Analyse
- Anteil angenommener proaktiver Vorschläge
- Anteil akzeptierter Planungsentwürfe
- Anzahl früh erkannter Konflikte
- Anteil der Exporte, die ohne wesentliche Nachbearbeitung nutzbar sind
- Nutzerbewertung zu „Aha“- und „Wow“-Momenten

Frühe AI-Produkte sollten nicht nur Features liefern, sondern messbare Produktivitäts- und Nutzererlebniseffekte erzeugen. [web:172][web:173][web:176]

## Nichtfunktionale Anforderungen

### Performance

| Anforderung | Zielwert |
|---|---|
| Chat-Antwortzeit | unter 3 Sekunden für 95 Prozent der Requests |
| Suchantwortzeit | unter 1 Sekunde für Volltextsuche, unter 5 Sekunden für semantische Suche |
| Indexierung neuer Dokumente | unter 30 Sekunden pro Dokument |
| Exportdauer bis 20 Seiten | unter 60 Sekunden |
| Dashboard-Ladezeit | unter 2 Sekunden |

### Verfügbarkeit

| Anforderung | Zielwert |
|---|---|
| Plattform-Verfügbarkeit | 99,5 Prozent pro Monat |
| Chat-Verfügbarkeit | 99,9 Prozent |
| Wiki-Lesezugriff | 99,9 Prozent |

### Skalierbarkeit

| Anforderung | Zielwert |
|---|---|
| Dokumente pro Mandant | mindestens 100.000 |
| Akten pro Mandant | mindestens 50.000 |
| Gleichzeitige Nutzer pro Mandant | mindestens 100 |

### Sicherheit

| Anforderung | Zielwert/Regel |
|---|---|
| Authentifizierung | OIDC / SSO |
| Autorisierung | rollen- und richtlinienbasiert |
| Verschlüsselung | at-rest und in-transit |
| Audit-Log-Retention | mindestens 5 Jahre |

## Datenmodell

Mindestens folgende Objektklassen sind vorzusehen:
- Mandant
- Nutzer
- Rolle
- Akte
- Dokument
- Dokumentversion
- Dokumentessenz
- Aktenessenz
- Indexeintrag
- Wissensdatenbankeintrag
- Wiki-Seite
- Wissenskonflikt
- Skill
- Skill-Version
- Skill-Ausführung
- Planung
- Exportauftrag
- Template
- CI-Profil
- Policy-Regel
- Audit-Log
- Freigabeobjekt

## Akzeptanzkriterien

Die Plattform gilt als fachlich geeignet, wenn ein Nutzer eine Akte oder ein Dokument innerhalb kurzer Zeit verstehen, dazu chatten, Analysen und Planungen erzeugen und diese unter Governance in nutzbare Artefakte überführen kann. AI-first Produktstufen liefern Wert, wenn sie frühe Kernjobs bereits messbar beschleunigen. [web:172][web:175]

Die Plattform gilt als governance-seitig geeignet, wenn persistente oder risikobehaftete Aktionen nachvollziehbar, rollenbasiert, mandantenbezogen und human-in-the-loop abgesichert sind. Meaningful human accountability, Auditierbarkeit und klare Kontrollpunkte gelten als Kernanforderungen agentischer Systeme. [web:182][web:183]

Die Plattform gilt als UX-seitig geeignet, wenn sie nicht nur Informationen anzeigt, sondern Verstehen, Vernetzen, Vorschlagen und Exportieren in einer hochwertigen, leichtgewichtigen und spürbar intelligenten Benutzererfahrung zusammenführt. AI-first UX sollte handlungsfähig, kontextuell und produktiv sein. [web:174][web:176]

## Offene Punkte für die nächste Spezifikationsstufe

- Feingranulare Objektrechte pro Aktenklasse und Dokumenttyp
- Konkrete Modellfreigabeliste und Modellzuordnung je Skill-Typ
- Definition der DMS-Zielsysteme und API-Verträge
- Template-Engine und CI-Datenmodell
- Teststrategie für Skills, Modelle und Agentenketten
- Monitoring-Dashboard für Proaktivität, Konflikte und Qualitätsmetriken

