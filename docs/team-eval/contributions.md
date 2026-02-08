---
title: Contributions
parent: Team Evaluation
nav_order: 4
---

{: .label }


{: .no_toc }
# Summary of individual contributions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Fabian Patzer

Contributions  
**Backend Architecture & Integration (app.py):** Übernahme der Hauptverantwortung für die zentrale Applikationslogik. Um eine konsistente Code-Struktur zu gewährleisten, wurde die Implementierung der Routen, Sessions und der Matching-Logik hier zentral zusammengeführt und finalisiert. Session-Management; "Swipe"- und Matching-Logik;
Full-Stack Integration & Sicherheit: Zusammenführung der Frontend-Templates mit dem Backend sowie Implementierung der Sicherheitsfeatures (Login-System, login_required-Decorator, Passwort-Hashing).

## Erik Wlochal 

Contributions  
**Backend & Datenmanagement** (app.py, database.py): Hauptverantwortung für das Datenbank-Fundament und die Datenverarbeitung. Erstellung des Entwurfs  (schema.sql) sowie das testen der Tabellenstrukturen mittels (test_table.py). Mit Implementierung der Registrierungs- und Login-Logik in der app.py unter Verwendung von Flask-Sessions zur Rollentrennung.  Absicherung der Nutzerdaten durch Passwort-Hashing innerhalb des Registrierungsprozesses. Datenbank-Anbindung & Query-Logik: Entwicklung der SQL-Abfragen zur Bereitstellung gefilterter Profile sowie die mit Implementierung der Skill-Verarbeitung in app.py.

## Yusuf Can Uyar

Contributions
: **Frontend-Architektur & Design-System:** Gesamtverantwortung für das visuelle Konzept und die technische Umsetzung des Frontends mittels Tailwind CSS (Utility-First). Entwicklung der modularen Template-Struktur (`base.html`), um ein konsistentes und responsives Layout für Desktop und Mobile sicherzustellen.
: **UX-Design & Interaktionslogik:** Implementierung der zentralen "Active Sourcing"-Logik im Frontend, insbesondere des interaktiven Swipe-Dashboards für Arbeitgeber (`card_view_swipe.html`) und der Match-Übersicht für Studenten.
: **Template-Integration & Usability:** Verknüpfung der Backend-Daten mit Jinja2-Templates sowie Gestaltung benutzerfreundlicher Formulare (Flask-WTF) inklusive visuellem Feedback-System (Flash-Messages) und Error-Handling.
