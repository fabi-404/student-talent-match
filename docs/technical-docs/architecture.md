---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }


{: .no_toc }
# Architecture

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

**Student-Talent-Matcher**

Student-Talent-Matcher ist eine Recruiting-Plattform, die Studierende dabei unterstützt, passende berufliche Einstiegsmöglichkeiten zu finden und praktische Erfahrungen zu sammeln.  
Die Anwendung ermöglicht es Studierenden, anonymisierte oder öffentliche Profile mit ihren individuellen Skills zu erstellen, während Arbeitgeber diesen Talent-Pool mithilfe spezifischer Filterkriterien gezielt durchsuchen können.

**Technische Umsetzung**

Die Plattform basiert auf einem **Flask-Backend**, das serverseitig mit **Jinja2-Templates** und **Tailwind CSS** gerendert wird.  
Die Datenpersistenz erfolgt über eine lokale **SQLite-Datenbank**.  
Die eindeutige Zuordnung der Benutzerrollen (**Studierende** und **Arbeitgeber**) wird über ein **Session-Management** realisiert.

## Codemap

Die Anwendung folgt dem klassischen **Flask-Architekturpattern** mit einer klaren Trennung der Verantwortlichkeiten:

* **app.py**  
  Zentraler Einstiegspunkt der Anwendung.  
  Verantwortlich für Routing, Session-Management sowie die Steuerung der Interaktion zwischen **WTForms** und der Datenbank.

* **schema.sql**  
  Definition des Datenbankschemas.  
  Enthält unter anderem die Tabellen:
  - `Student` & `Employer` 
  - `Swipe` (Persistenz der Like-/Pass-Entscheidungen)  

* **database.py**
  Der Code dient der Initialisierung und Verwaltung der SQLite-Datenbank für die Anwendung **Student-Talent-Matcher** und stellt sicher, dass diese vor der    Nutzung korrekt erstellt und konfiguriert wird. --> `student_talent.db`

* **forms.py**  
  Beinhaltet die **WTForms-Definitionen** für Registrierung und Profilerstellung.  
  Enthält Validierungsregeln zur Sicherstellung konsistenter Eingaben.

* **templates/**  
  Enthält alle **Jinja2-Templates** für die serverseitige Darstellung.  
  Besonders relevant:
  * Rollenspezifische Dashboards für Studierende und Arbeitgeber     
  
Alle Templates nutzen konsequent **Tailwind-Utility-Classes**, um ein responsives und konsistentes Design zu gewährleisten. Interaktive Elemente wie Hover-Effekte werden ausschließlich über CSS umgesetzt, sodass vollständig auf clientseitiges JavaScript verzichtet werden kann und die vorgegebenen technischen Rahmenbedingungen eingehalten werden.



## Cross-cutting concerns

**Authentifizierung & Zugriffskontrolle**
- Trennung der Benutzerrollen **Student** und **Employer**
- Zugriffsschutz über einen `@login_required`-Decorator
- Session-Management zur Speicherung von Login-Status und Rolle

**Datenbank-Interaktion**
- Direkter Datenbankzugriff mit **Plain SQL** (ohne ORM)
- Zentrale Helper-Funktion für Verbindungen zur SQLite-Datenbank
- Nutzung von `sqlite3.Row` für besser lesbaren Code
- Explizite Transaktionskontrolle mittels `commit()`

**User Feedback**
- Nutzerfeedback über **Flask Flash Messages**
- Zentrale Darstellung im Base-Template
- Visuelles Feedback durch Tailwind-gestylte Alert-Boxen

**Sicherheit**
- Keine Klartext-Passwörter
- Passwort-Hashing mit `werkzeug.security`
- Sichere Validierung beim Login

