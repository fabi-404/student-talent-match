---
title: Improvements
parent: Team Evaluation
nav_order: 2
---

{: .label }
[Jane Dane]

{: .no_toc }
# How we would improve next time

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

---

## 1. Technische Architektur & Code-Struktur

### Modularisierung mit Flask Blueprints

**Beobachtung:** Aktuell befindet sich fast die gesamte Routing- und Business-Logik in einer einzigen Datei (`app.py`). Das war für die Geschwindigkeit der Entwicklung im MVP-Status hilfreich, führt aber bei wachsendem Code zu Unübersichtlichkeit.
**Verbesserung:** Beim nächsten Mal würden wir von Anfang an **Flask Blueprints** nutzen, um die Anwendung in logische Module zu unterteilen (z.B. `auth`, `student`, `employer`). Das würde die Wartbarkeit erhöhen und Merge-Konflikte im Team reduzieren.

### Repository Pattern für Datenbank-Zugriffe

**Beobachtung:** Wir nutzen "Plain SQL" direkt in den Routen-Funktionen. Das gibt uns zwar volle Kontrolle, vermischt aber Datenbank-Logik mit HTTP-Request-Logik.
**Verbesserung:** Wir würden ein **Repository Pattern** einführen. Das bedeutet, wir schreiben Python-Funktionen (z.B. `get_student_by_id(id)`), die das SQL kapseln. Die Routen rufen dann nur noch diese Funktionen auf. Das macht den Code sauberer und erleichtert das Testen.

---

## 2. Testing & Qualitätssicherung

### Automatisierte Unit-Tests (Pytest)

**Beobachtung:** Wir haben uns stark auf manuelles Testen ("Klicken durch die UI") und ein einfaches Hilfsskript (`test_tables.py`) verlassen.
**Verbesserung:** Die Einführung eines Test-Frameworks wie **pytest** wäre essenziell. Wir würden automatisierte Tests schreiben, die kritische Pfade (Login, Swipe-Logik, DB-Eintrag) bei jedem Commit prüfen. Das verhindert Regressionen (Fehler, die durch neue Änderungen entstehen).

### Frontend-Build-Pipeline

**Beobachtung:** Wir binden Tailwind CSS aktuell über ein CDN ein. Das ist perfekt für Prototyping, aber nicht optimal für die Performance und erlaubt keine Offline-Nutzung.
**Verbesserung:** Wir würden eine **Build-Pipeline (npm/Node.js)** aufsetzen, die das CSS kompiliert und minifiziert ("Tree Shaking"), um die Ladezeiten zu optimieren.

---

## 3. Algorithmus & Features

### Intelligentes Matching statt Zufallsprinzip

**Beobachtung:** Aktuell sortieren wir die Kandidaten im Swipe-Modus zufällig (`ORDER BY RANDOM()`), solange sie die Filterkriterien erfüllen.
**Verbesserung:** Wir würden einen **Scoring-Algorithmus** implementieren (z.B. basierend auf dem Jaccard-Koeffizienten), der berechnet, wie hoch die prozentuale Übereinstimmung der Skills ist. Kandidaten mit höherem Match-Score würden dann priorisiert angezeigt werden, statt rein zufällig.

### Asynchrone Kommunikation

**Beobachtung:** Wenn ein Match entsteht, passiert dies synchron.
**Verbesserung:** Wir würden echte E-Mail-Benachrichtigungen oder Push-Notifications integrieren, damit Studenten erfahren, wenn sie geliked wurden, auch wenn sie gerade nicht in der App eingeloggt sind.

---

## Zusammenarbeit & Team-Spirit

### Das lief gut (Positive Aspects)

* **"Kurzer Dienstweg":** Wir haben uns nicht mit langen Meetings aufgehalten. Entscheidungen fielen schnell per WhatsApp oder Discord, und wenn einer eine Idee hatte, wurde sie direkt umgesetzt.
* **Motivation trotz Crunch-Time:** Auch als es kurz vor Abgabe stressig wurde, war die Stimmung gut. Wir haben uns gegenseitig geholfen, statt Schuldzuweisungen zu machen, wenn mal Code nicht lief.
* **Learning by Doing:** Keiner von uns war Experte für alles. Wir haben uns einfach in die Themen (Flask, Python, Jinja, Datenbank) reingeworfen und zusammen gelernt.

### Was wir nächstes Mal besser machen wollen

Statt komplizierter Regeln nehmen wir uns drei einfache Dinge vor:

#### 1. "Wer bearbeitet was?"

**Problem:** Wir hatten öfter Merge-Konflikte, weil zwei Leute gleichzeitig in der `app.py` gearbeitet haben.
**Verbesserung:** Wir sprechen uns im Chat kurz ab ("Ich bin gerade an der Login-Route"), bevor jemand loslegt. Einfache Absprache statt technischer Hürden.

#### 2. "Realismus beim Scope"

**Problem:** Wir hatten am Anfang zu viele Ideen (Features), die wir am Ende streichen mussten.
**Verbesserung:** Wir definieren früher ein "Minimal-Ziel" (MVP), das sicher funktioniert, und bauen erst danach Zusatz-Features ein, wenn noch Zeit ist.

#### 3. "Früherer Integrationstest"

**Problem:** Wir haben oft lokal entwickelt und erst spät alles zusammengeführt.
**Verbesserung:** Wir versuchen, die Teile (Frontend und Backend) früher einmal zusammenzustecken, um böse Überraschungen kurz vor der Abgabe zu vermeiden.
