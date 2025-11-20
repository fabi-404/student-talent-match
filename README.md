
# 🚀 Product Requirements Document (PRD): Talent-Swipe (Tinder für studentische Talente)

| Attribut | Wert |
| :--- | :--- |
| **Produktname** | Talent-Swipe |
| **Plattform** | Web-Anwendung (Full-Stack) |
| **Kerntechnologie** | Python/Flask, SQLite, Jinja2, HTML/CSS |
| **Zielgruppe** | Studierende/Absolventen & Arbeitgeber von Einstiegspositionen |
| **Entwicklungsfokus** | Duale Benutzererfahrung (Student vs. Arbeitgeber) |
| **Teamgröße** | 3 Personen |

---

## 1. 🎯 Produktziel und Value Proposition

### 1.1 Vision
Die Vision ist es, den Einstellungsprozess für Praktika und Junior-Rollen zu **gamifizieren** und zu **beschleunigen**. Der **Talent-Swipe** ermöglicht Arbeitgebern eine intuitive, filterbasierte **Talent-Identifikation** und bietet Studierenden eine Plattform für hohe Sichtbarkeit.

### 1.2 Value Proposition
* **Für Studierende:** Erhöhte Sichtbarkeit bei relevanten Arbeitgebern; direkter Weg zur Interview-Einladung ohne formelles Anschreiben.
* **Für Arbeitgeber:** Effizientes Filtern nach spezifischen Skills; schneller Zugang zu potenziellen Kandidaten durch den "Swipe"-Mechanismus.

---

## 2. 👩‍💻 Benutzerrollen und deren Anforderungen

| Rolle | Beschreibung | Primäre Aktionen (Funktionalitäten) |
| :--- | :--- | :--- |
| **Student** | Legt ein anonymisiertes Profil mit Skills an, wartet auf Likes und Interview-Einladungen. | Login, **Profil erstellen/aktualisieren**, Status (aktiv/inaktiv) setzen, Matches einsehen. |
| **Arbeitgeber** | Identifiziert und liked passende Profile von Studierenden. | Login, **Filter setzen**, **Talent-Pool swipen**, Interviews einladen. |
| **Anonymer Nutzer** | Vor der Anmeldung. | Registrieren, Login. |

---

## 3. ⚙️ Funktionale Anforderungen (Was die App tun muss)

### FR-1: Authentifizierung & Duale Profile
| ID | Anforderung | Rolle |
| :--- | :--- | :--- |
| FR-1.1 | Die App muss **zwei getrennte Login-/Registrierungs-Flows** bereitstellen: **Student** und **Arbeitgeber**. | Beide |
| FR-1.2 | Die App muss das Anlegen von **Studentenprofilen (Skills, Bio)** und **Arbeitgeberprofilen (Firma, Suchfilter)** in **SQLite** speichern. | Beide |
| FR-1.3 | Die App muss **Session-Management** (Flask Sessions) zur Identifizierung beider Rollen nutzen. | Beide |

### FR-2: Studentisches Talent-Pool-Management
| ID | Anforderung | Rolle |
| :--- | :--- | :--- |
| FR-2.1 | Der Student muss seine **Skills/Tags** über ein einfaches Formular eingeben können (kommaseparierter String). | Student |
| FR-2.2 | Die App muss sicherstellen, dass nur **aktive** Studentenprofile im Swipe-Pool erscheinen. | Student |
| FR-2.3 | Der Student muss eine Ansicht der **Matches** und **Interview-Einladungen** erhalten. | Student |

### FR-3: Talent-Swipe Logik & Filterung (Kernfunktionalität)
| ID | Anforderung | Rolle |
| :--- | :--- | :--- |
| FR-3.1 | Der Arbeitgeber muss **Filter-Kriterien** (z.B. **Pflicht-Skills**) setzen, um den Pool einzugrenzen. | Arbeitgeber |
| FR-3.2 | Die App muss auf Basis der Filter die **Studentenprofile** nacheinander im Swipe-View präsentieren. | Arbeitgeber |
| FR-3.3 | Die App muss bei jedem "Swipe" (Like/Pass) einen Eintrag in der **`SwipeLog`**-Tabelle in **SQLite** speichern. | Arbeitgeber |
| FR-3.4 | Die App muss vermeiden, dass ein Arbeitgeber dasselbe Profil mehrmals swipen kann. | Arbeitgeber |

### FR-4: Matching und Kommunikation
| ID | Anforderung | Rolle |
| :--- | :--- | :--- |
| FR-4.1 | Die App muss das **Matching** speichern: Wer hat wen "geliked". (Ein Match entsteht, wenn der Arbeitgeber den Studenten liked). | Beide |
| FR-4.2 | Der Arbeitgeber muss über einen Button im Match-Übersicht eine **simulierte Interview-Einladung** an den Studenten senden können. | Arbeitgeber |

---

## 4. 🖼️ Benutzeroberfläche & Visuelle Anforderungen (Jinja2/CSS)

Die UI wird als **kartenbasiertes** Design über **Jinja2** und **CSS** gerendert.

| Screen-ID | Name | Key Visuals/Interaktion |
| :--- | :--- | :--- |
| UI-1 | **Login/Register** | Zwei klare Anmeldeoptionen (Student/Arbeitgeber). |
| UI-2 | **Studentenprofil-Eingabe** | Formular zur Erfassung von Bio und Skills (Tags). |
| UI-3 | **Arbeitgeber-Filter-Dashboard** | Formular zur **Filtersetzung** (z.B. Textfeld für Skills). |
| UI-4 | **Talent-Swipe-View** | **Zentrale Card-Ansicht** des Studentenprofils (Bio, Skills). Große Buttons: **"Interessiert" (Grün)** und **"Nicht geeignet" (Rot)**. |
| UI-5 | **Match- & Einladungs-Übersicht** | Liste der Profile, die der Arbeitgeber "geliked" hat. Button **"Interview einladen"**. |

---

## 5. 💻 Technische Anforderungen & Architektur

### 5.1 Technologie-Stack (Mandatory)
* **Backend/Logik:** Python 3 + **Flask**
* **Template Engine:** **Jinja2**
* **Datenbank:** **SQLite**
* **Datenübertragung:** **JSON** (für interne Datenverarbeitung)
* **Frontend-Struktur:** HTML, CSS (Fokus auf Responsive Design für die Swipe-Karten).

### 5.2 Datenbank-Schema (SQLite/SQLAlchemy)

Die Datenbank muss mindestens folgende Tabellen umfassen:

1.  **`User`**: Speichert beide Benutzertypen.
    * `id` (PRIMARY KEY), `username`, `password_hash`
    * `is_student` (Boolean), `is_employer` (Boolean)
    * `skills_json` (Studenten-Skills als JSON-String)
2.  **`SwipeLog`**: Speichert alle Swipe-Aktionen.
    * `id` (PRIMARY KEY), `employer_id` (FK), `student_id` (FK)
    * `status` (String: 'Liked' oder 'Passed')
3.  **`FilterPreset` (Optional):** Speichert die Suchkriterien des Arbeitgebers.
    * `id` (PRIMARY KEY), `employer_id` (FK)
    * `required_skills_json` (JSON-String der Such-Tags)

### 5.3 Rollenverteilung (Zusammenfassung)

| Rolle | Fokus-Bereich | Code-Anteile (Schwerpunkte) |
| :--- | :--- | :--- |
| **Mitglied 1: Lead Backend & DB** | SQLite-Design, Login/Sessions, JSON-API | DB-Models, **SQLite-CRUD**, **Authentifizierung**, Daten-Seeding. |
| **Mitglied 2: Flask-Routing & Logik** | Anwendungs-Controller, **Swiping-Logik**, Filterung | **Flask-Routen** (POST/GET), **Swipe-Logik** (Datenbankabfrage), **Match-Berechnung**. |
| **Mitglied 3: UI/UX & Visuelles Design** | Jinja2-Templates, CSS, UX-Flow | Alle **Jinja2-Templates**, **CSS-Styling** (kartenbasiertes Design), **Formular-Rendern**. |
