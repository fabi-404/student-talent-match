---
title: Goals
parent: Team Evaluation
nav_order: 1
---

{: .label }


{: .no_toc }
# Goals achieved and missed

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>



###  Achieved Goals  

Im Rahmen des Projekts "Student-Talent-Matcher" konnten wir die folgenden Kernziele erfolgreich umsetzen:  

* **Implementierung dualer Benutzerrollen:** Es wurden zwei Registrierungs- und Login-Flows für Studierende und Arbeitgeber entwickelt. Die Rollentrennung erfolgt zuverlässig über das Flask-Session-Management.  

* **Dynamisches Talent-Pool:** Arbeitgeber können den Pool an Kandidaten durch spezifische Skill-Filter gezielt eingrenzen. Die Filterlogik greift dabei direkt auf die in SQLite hinterlegten Profile zu.  

* **Kartenbasiertes Interface mit Tailwind CSS:** Das User Interface wurde mittels Jinja2-Templates und Tailwind CSS gestaltet, um eine moderne, übersichtliche Card-Ansicht der Studentenprofile zu ermöglichen. Dies erlaubt eine effiziente Sichtung von Skills und Kurz-Bios direkt im Browser.  

* **Persistente Entscheidungshistorie:** Jede Interaktion (Like/Pass) wird in einer Swipe-Tabelle gespeichert, wodurch Dopplungen vermieden werden und ein konsistenter Datenbestand gewährleistet ist.  

* **Matching-Funktionalität:** Sobald ein Arbeitgeber ein Profil positiv bewertet, wird dies als Match im System hinterlegt und ist für den Studenten in seiner persönlichen Übersicht einsehbar.  

###  Missed Goals  

Trotz der erfolgreichen Umsetzung mussten wir bei folgenden Punkten Abstriche machen:  

* **Haptisches Card-Swiping (JavaScript):** Das haptische Verschieben der Profilkarten per Maus oder Touch (Drag-and-Drop) konnte nicht wie geplant umgesetzt werden. Da dies eine intensive clientseitige Logik mittels JavaScript erfordert hätte, was nicht erlaubt war.  

* **Echtzeit-Kommunikation:** Die Funktion zur Interview-Einladung ist aktuell nur simuliert. Die Anbindung eines realen Mail-Servers oder eines internen Chats konnte im zeitlichen Rahmen nicht mehr realisiert werden.  

