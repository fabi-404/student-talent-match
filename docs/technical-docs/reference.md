---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Jane Dane]

{: .no_toc }
# Reference documentation

{: .attention }
> This page collects internal functions, routes with their functions, and APIs (if any).
> 
> See [Uber](https://developer.uber.com/docs/drivers/references/api) or [PayPal](https://developer.paypal.com/api/rest/) for exemplary high-quality API reference documentation.
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Section / module]

### `function_definition()`

**Route:** `/route/`

**Methods:** `POST` `GET` `PATCH` `PUT` `DELETE`

**Purpose:** [Short explanation of what the function does and why]

**Sample output:**

[Show an image, string output, or similar illustration -- or write NONE if function generates no output]

---

---

## Authentication & Base

### `index()`

**Route:** `/`

**Methods:** `GET`

**Purpose:** Zeigt die Landingpage mit der Auswahlmöglichkeit für Studenten oder Arbeitgeber an.

**Sample output:**
Renders template `frontpage.html` (Landing Page mit zwei Call-to-Action Buttons).
<img width="1057" height="850" alt="image" src="https://github.com/user-attachments/assets/426baf7c-e52c-4d93-bbb2-b654c219b9dd" />


---

### `login_student()`

**Route:** `/login/student`

**Methods:** `GET` `POST`

**Purpose:** Validiert die Anmeldedaten des Studenten gegen die Tabelle `Student`. Bei Erfolg wird eine Session erstellt.

**Sample output:**
Renders template `login_student.html` und leitet weiter zum Profil.

<img width="1062" height="850" alt="image" src="https://github.com/user-attachments/assets/be210413-d7a9-46a3-947a-652f25c3d4f9" />


---

### `register_employer()`

**Route:** `/register/employer`

**Methods:** `GET` `POST`

**Purpose:** Registriert eine neue Firma. Hashes das Passwort via `werkzeug.security` und speichert den Eintrag in der Tabelle `Employer`.

**Sample output:**
Renders template `register_employer.html`.
<img width="1058" height="850" alt="image" src="https://github.com/user-attachments/assets/9b165815-3851-48e9-9d01-1cb589b16c07" />


---

## Student Module

### `student_profile()`

**Route:** `/student/profile`

**Methods:** `GET` `POST`

**Purpose:** Dashboard für Studenten.

* **GET:** Lädt Stammdaten und Skills aus der DB und füllt das Formular.
* **POST:** Aktualisiert Profil, Bio und verknüpft Skills (Many-to-Many in `Student_Skill`).

**Sample output:**

<img width="1059" height="853" alt="image" src="https://github.com/user-attachments/assets/70dba477-1f2c-4c90-ab03-339483a0a10b" />


---

### `student_matches()`

**Route:** `/student/matches`

**Methods:** `GET`

**Purpose:** Zeigt eine Liste aller Unternehmen an, die den Studenten "geliked" (zum Interview eingeladen) haben. Führt einen SQL-Join zwischen `interviews` und `Employer` durch.

**Sample output:**
Renders template `student_matches.html` (Liste mit Karten).

<img width="1059" height="843" alt="image" src="https://github.com/user-attachments/assets/0ebfbac4-32c2-4fbc-ba94-2e70bceb13e1" />


---

## Employer Module (Matching Core)

### `employer_filter()`

**Route:** `/employer/filter`

**Methods:** `GET` `POST`

**Purpose:** Setzt Filterkriterien für den Swipe-Algorithmus.

* **POST:** Speichert eine Liste von Skill-IDs in der `session['filter_skills']`.

**Sample output:**
Renders template `employer_filter.html` (Checkbox-Liste aller verfügbaren Skills).

<img width="1049" height="853" alt="image" src="https://github.com/user-attachments/assets/8f3d4865-9e50-4b7c-85a0-939f2a003113" />


---

### `employer_swipe()`

**Route:** `/employer/swipe`

**Methods:** `GET`

**Purpose:** **Kern-Logik der App.** Wählt einen zufälligen Studenten aus, der:

1. Aktiv ist (`is_active = 1`).
2. Die Filterkriterien erfüllt (SQL `IN` Clause).
3. Noch nicht von diesem Arbeitgeber geswiped wurde (`NOT IN Swipe`).

**Sample output:**

<img width="1053" height="845" alt="image" src="https://github.com/user-attachments/assets/41ba581c-5e81-4d15-96e5-86049e54fec2" />


---

### `action_candidate(student_id, action)`

**Route:** `/employer/action/<int:student_id>/<action>`

**Methods:** `POST`

**Purpose:** Verarbeitet die Entscheidung des Arbeitgebers.

* `action='invite'`: Erstellt Eintrag in `Swipe` (Richtung 1) und `interviews` (Status 'pending').
* `action='ignore'`: Erstellt Eintrag in `Swipe` (Richtung 0), damit Kandidat nicht erneut erscheint.

**Sample output:**
Redirects to `/employer/swipe` (lädt den nächsten Kandidaten).

---

## Debugging Tools

### `reset_swipes()`

**Route:** `/debug/reset_swipes`

**Methods:** `GET`

**Purpose:** Löscht alle Einträge in der `Swipe`-Tabelle für den aktuellen Arbeitgeber. Hilfreich beim Testen, um Kandidaten erneut anzuzeigen.

**Sample output:**
Flash Message: "Swipe-Historie zurückgesetzt."
