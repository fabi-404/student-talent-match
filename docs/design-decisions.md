---
title: Design Decisions
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Design decisions

## Table of contents
{: .text-delta }

- TOC
{:toc}

## 01: Wahl des Datenbank-Zugriffs 

Status  
: **entschieden**  
Updated  
: 08-02-2026

### Problem statement

Im Rahmen der Entwicklung von "Student-Talent-Match" stehen wir vor der Herausforderung,
ein Datenmodell zu implementieren, das die Dynamik einer Recruiting-Plattform
(Nutzerprofile, Skill-Sets, Swipe-Logik und Interview-Einladungen) stabil abbildet.

Da unsere Web-App auf Python/Flask und SQLite basiert, ist die zentrale Frage,
wie wir die Interaktion zwischen der Anwendungslogik und der Datenhaltung gestalten.

Konkret müssen wir entscheiden, ob wir ein **Object-Relational Mapping (ORM)**
wie SQLAlchemy einsetzen oder die Datenbank-Operationen (CRUD) über **Plain SQL**
abwickeln.

Wir brauchten eine Lösung, die maximale Kontrolle bei minimalem technischem Overhead bietet.

### Decision

Wir entschieden uns bewusst für **Plain SQL**.

Diese Strategie gibt uns die maximale Transparenz, die wir für unser Matching-System brauchen.

Da das Filtern von Talenten nach spezifischen Skills das Herzstück unserer App ist,
wollen wir die volle Kontrolle über jede einzelne Query behalten, anstatt uns auf die
automatische Generierung eines ORMs zu verlassen.

Durch den Verzicht auf SQLAlchemy halten wir den Technologie-Stack schlank und vermeiden
eine "Blackbox", die uns beim Debugging nur Zeit kosten würde.

Wir sind überzeugt, dass wir durch diesen direkten Zugriff auf die Datenbankebene
eine deutlich robustere Matching-Logik implementieren konnten, bei der wir genau wissen,
was im Hintergrund passiert.

### Regarded options

Für die Datenhaltung haben wir zwei grundlegende Strategien gegenübergestellt,
um die beste Basis für unser Projekt zu finden.

Legende ||  
| :--- | :--- |
| ✅ Ideal | Optimale Lösung |
| ⚠️ Neutral | Technisch stark, aber für unser spezifisches Setup mit Nachteilen verbunden. |
| ❌ Kritisch | Hohes Risiko für Zeitplan oder Flexibilität. |

| Kriterium | Plain SQL (Gewählt) | SQLAlchemy (Alternative) |
| :--- | :--- | :--- |
| Kontrolle | ✅ Wir haben die volle Kontrolle über jede Abfrage. | ⚠️ SQL-Generierung oft intransparent. |
| Lernkurve | ✅ Bestehendes SQL-Wissen sofort nutzbar/kein Zeitverlust | ❌ Erfordert Einarbeitung in eine komplexe neue Syntax, die uns Zeit kostet. |
| Effizienz | ✅ Schnelle, direkte Umsetzung ohne unnötigen Framework-Ballast. | ✅ Hohe Automatisierung bei Standard-Tasks. |
| Fehlersuche | ✅ Queries können wir 1:1 direkt in der SQL-Konsole prüfen. | ⚠️ Fehler verstecken sich oft hinter den Abstraktionsschichten des Mappers. |
| Skalierung | ❌ DB-Wechsel braucht Syntax-Anpassung. | ✅ Vollkommen datenbankunabhängig. |

Obwohl SQLAlchemy starke Vorteile bei der Automatisierung und Skalierbarkeit bietet,
priorisierten wir für unser Projekt die direkte Kontrolle und Umsetzungsgeschwindigkeit.

*Plain SQL ist für uns der sicherste Weg, um die spezifischen Anforderungen von
Student-Talent-Match ohne Umwege und mit voller Transparenz umzusetzen.*

---

## 02: Frontend-Design

### Meta

Status  
: Work in progress - **Decided** - Obsolete

Updated  
: 08-02-2026

### Problem statement

### Decision

### Regarded options

---
