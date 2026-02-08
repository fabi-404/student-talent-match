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

Status  
: **entschieden**  
Updated  
: 08-02-2026

### Problem statement

Bei der Entwicklung des Frontends standen wir vor einer ganz praktischen Frage:
Wie bauen wir eine Oberfläche, die sich gut anfühlt (besonders die Swipe-Funktion auf dem Handy),
ohne dass wir uns technisch verrennen?

Da unser Projekt-Fokus klar auf dem Python-Backend liegt, wollten wir uns nicht
mit komplexen JavaScript-Build-Tools (wie Node.js, Webpack oder npm) belasten.
Wir brauchten eine Styling-Lösung, mit der wir schnell sichtbare Ergebnisse erzielen ("Rapid Prototyping"),
ohne stundenlang in separaten CSS-Dateien Fehler zu suchen.

Die Wahl stand zwischen:
1. Einem fertigen Baukasten (Bootstrap) nehmen und hoffen, dass es nicht zu langweilig aussieht.
2. Alles von Hand selbst schreiben (Custom CSS) und viel Zeit investieren.
3. Einen modernen Mittelweg finden (Utility-First).

### Decision

Wir haben uns für **Tailwind CSS** (via CDN) entschieden.

Der Grund ist simpel: Der "Utility-First"-Ansatz macht die Entwicklung extrem schnell.
Wir schreiben das Design direkt in unsere HTML-Templates (Jinja2). Das spart uns das
ständige Hin- und Herspringen zwischen HTML- und CSS-Dateien. Man sieht sofort, was passiert.

Ein riesiger Pluspunkt für unser Setup war die einfache Einbindung über einen CDN-Link.
Das hält unser Projekt sauber: Wir brauchen keine riesigen `node_modules`-Ordner oder
komplizierte Build-Pipelines. Wir bleiben bei Python, HTML und einem Link im Header.

Außerdem gab uns Tailwind die Freiheit, unsere speziellen "Swipe-Karten" für die Arbeitgeber
genau so zu gestalten, wie wir sie im Kopf hatten – ohne gegen die starren Vorgaben
eines Standard-Frameworks kämpfen zu müssen.

### Regarded options

Wir haben abgewogen, was uns am schnellsten ans Ziel bringt, ohne die Optik zu opfern.

**Legende**

| Status | Bedeutung |
| :--- | :--- |
| ✅ **Ideal** | Optimale Lösung |
| ⚠️ **Neutral** | Technisch okay, hat aber Nachteile für uns. |
| ❌ **Kritisch** | Killt den Zeitplan oder die Flexibilität. |

<br>

| Kriterium | Tailwind CSS (Gewählt) | Bootstrap (Alternative) | Custom / Vanilla CSS |
| :--- | :--- | :--- | :--- |
| Individualität | ✅ **Hoch**: Wir bauen genau das Design, das wir wollen. Kein Einheitsbrei. | ⚠️ **Mittel**: Sieht oft sehr generisch ("nach Baukasten") aus. | ✅ **Maximal**: Alles geht, aber man muss jedes Detail selbst erfinden. |
| Tempo | ✅ **Sehr schnell**: Klassen direkt ins HTML schreiben, fertig. | ✅ **Schnell**: Fertige Komponenten (wie Navbars) sparen anfangs Zeit. | ❌ **Langsam**: Jedes Layout und jede Handy-Ansicht muss manuell programmiert werden. |
| Komplexität | ✅ **Minimal (CDN)**: Ein Link im Header reicht. Perfekt für uns. | ✅ **Minimal**: Auch einfach via CDN möglich. | ⚠️ **Mittel**: Keine Tools nötig, aber der Code wird schnell unübersichtlich ("Spaghetti-CSS"). |
| Responsivität | ✅ **Mobile-First**: Super einfach, Dinge auf dem Handy anders aussehen zu lassen. | ✅ **Gut**: Solides Raster, aber manchmal unflexibel bei Details. | ❌ **Aufwendig**: Media-Queries müssen mühsam von Hand geschrieben werden. |

Bootstrap wäre zwar der bequemste Start gewesen, aber wir wollten nicht, dass unsere App
aussieht wie jede andere Standard-Seite. Alles selbst zu schreiben (Custom CSS) hätte
einfach zu lange gedauert.

*Tailwind CSS war für uns der "Sweetspot": Die Geschwindigkeit eines Frameworks,
aber mit der Freiheit, es genau so aussehen zu lassen, wie wir wollen.*
---

Ja, absolut. Wenn man sich den Code in der `app.py` (speziell die Route `/employer/swipe`) ansieht, fällt eine fundamentale Logik-Entscheidung auf, die massiven Einfluss auf die User Experience (UX) hat: **Wie streng filtert der Algorithmus?**

Hier ist ein Vorschlag für eine dritte Design-Decision, die sich auf die **Such-Logik** bezieht. Das ist oft ein kritischer Punkt bei MVPs (Minimum Viable Products), da man mit wenigen Daten startet.

---

## 04: Filter-Strategie (Soft-Matching vs. Hard-Matching)

**Status**
: **entschieden**

**Updated**
: 08-02-2026

### Problem statement

Ein Arbeitgeber wählt im Filter-Dashboard oft mehrere gewünschte Fähigkeiten gleichzeitig aus (z. B. "Python" und "SQL" und "Englisch").

Wir mussten definieren, wie die Datenbank diese Anfrage interpretiert:

1. **Strict/Hard Matching (AND):** Zeige nur Studenten, die **alle** gewählten Skills besitzen.
2. **Soft Matching (OR):** Zeige alle Studenten, die **mindestens einen** der gewählten Skills besitzen.

Das Problem: In der Startphase der App (wenig Nutzerdaten) führt eine strikte "AND"-Logik sehr schnell zu "0 Treffern", was für den Arbeitgeber frustrierend ist ("Die App funktioniert nicht").

### Decision

Wir haben uns für das **Soft-Matching (OR-Logik)** entschieden.

Im Backend setzen wir dies durch eine SQL `IN`-Abfrage um:

```python
query += f" AND s.id IN (SELECT student_id FROM Student_Skill WHERE skill_id IN ({placeholders}))"

```

Das bedeutet: Wählt ein Arbeitgeber 5 Skills aus, erweitern wir den Suchradius, statt ihn zu verengen. Wir priorisieren, dass der Arbeitgeber *überhaupt* Kandidaten sieht (Quantität), auch wenn diese vielleicht nur 50% der Anforderungen erfüllen. Das passt besser zu unserem "Swipe"-Ansatz, der auf schnelle visuelle Bewertung setzt, anstatt auf eine präzise Datenbank-Abfrage wie bei klassischen Jobportalen.

### Regarded options

| Kriterium | Soft-Matching / OR (Gewählt) | Hard-Matching / AND (Alternative) |
| --- | --- | --- |
| **Ergebnis-Menge** | ✅ **Hoch**: Der User bekommt fast immer Profile zum Swipen angezeigt. | ❌ **Niedrig**: Hohes Risiko für "Leere Ergebnisse" (Zero Results), besonders bei vielen ausgewählten Filtern. |
| **Relevanz** | ⚠️ **Mittel**: Es tauchen auch Kandidaten auf, die nur 1 von 5 Kriterien erfüllen. | ✅ **Hoch**: Die Kandidaten passen perfekt auf das Profil. |
| **SQL-Komplexität** | ✅ **Gering**: Einfaches `WHERE id IN (...)`. | ⚠️ **Mittel**: Erfordert komplexere Aggregation (`GROUP BY ... HAVING COUNT = X`). |
| **User Experience** | ✅ **Flüssig**: Der "Swipe-Flow" bricht nicht ab. | ❌ **Stockend**: User muss ständig Filter lockern, um Ergebnisse zu sehen. |

*Wir haben uns hier bewusst für die **Vermeidung von leeren Ergebnislisten** entschieden, um die Interaktion auf der Plattform in der frühen Phase am Laufen zu halten.*
