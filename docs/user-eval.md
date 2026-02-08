
## 01: Usability-Test der Kernfunktionen (MVP)

### Meta

Status
: **Done**

Updated
: 08-02-2026

### Goal

Das Ziel dieser Evaluation war es zu überprüfen, ob die **Trennung der Benutzerrollen** (Student vs. Arbeitgeber) intuitiv verstanden wird und ob der **Matching-Prozess** (Filtern & Swipen) für neue Nutzer ohne Erklärung bedienbar ist.
Konkrete Forschungsfragen:

1. Verstehen Nutzer auf der Startseite sofort, welchen "Pfad" sie wählen müssen?
2. Ist der Ablauf "Filter setzen -> Kandidaten swipen" für Arbeitgeber logisch?
3. Treten bei der Profilerstellung Hürden auf, die die Sichtbarkeit im Pool verhindern?

### Method

Wir haben einen qualitativen **"Think Aloud"-Test** mit **5 Testpersonen** (Kommilitonen aus anderen Fachbereichen) durchgeführt.
Jeder Teilnehmer musste zwei Szenarien durchlaufen:

* **Szenario A (Student):** "Registriere dich, lege ein Profil an und stelle sicher, dass du gefunden werden kannst."
* **Szenario B (Arbeitgeber):** "Registriere dich als Firma, suche nach Studenten mit 'Python'-Kenntnissen und lade einen Kandidaten zum Interview ein."

Wir beobachteten dabei Klickpfade, Zögern und baten die Teilnehmer, ihre Gedanken laut auszusprechen.

### Results

Die Ergebnisse waren überwiegend positiv, deckten aber zwei spezifische UX-Probleme auf:

1. **Rollen-Trennung (Login/Register):**
* **Ergebnis:** 5 von 5 Nutzern navigierten auf der Startseite fehlerfrei zum richtigen Registrierungs-Button. Die visuelle Trennung (Blau/Grün vs. Dunkelgrau) funktioniert sehr gut.


2. **Swipe-Mechanik:**
* **Ergebnis:** Das Karten-Design mit den großen "X" und "Herz"-Symbolen wurde sofort als "Tinder-Prinzip" erkannt. Die Bedienung war intuitiv.


3. **Hürde "Sichtbarkeit":**
* **Problem:** 2 von 5 Testern im Studenten-Szenario übersahen im Profil die Checkbox *"Profil für Arbeitgeber sichtbar machen"*. Sie speicherten das Profil, wären aber im Pool nicht aufgetaucht.


4. **Filter-Feedback:**
* **Ergebnis:** Das Filtern nach Skills wurde verstanden, aber wenn ein Filter zu *keinen* Ergebnissen führte, fehlte einigen Testern ein klarer "Filter zurücksetzen"-Button direkt in der Leermeldung.



### Implications

Basierend auf diesem Feedback haben wir folgende Verbesserungen für den nächsten Sprint definiert:

1. **Default-Werte anpassen:** Die Checkbox `is_active` im Studentenprofil wird standardmäßig auf `True` (aktiviert) gesetzt, damit neue Nutzer sofort sichtbar sind, ohne einen extra Klick machen zu müssen.
2. **Empty-State verbessern:** Wenn der Swipe-Stapel leer ist, fügen wir einen direkten Link "Filter bearbeiten/löschen" hinzu, statt nur "Zurück zum Start" anzuzeigen.
3. **Feedback-Schleife:** Nach einem erfolgreichen Match (Interview-Einladung) soll ein noch deutlicheres visuelles Feedback (z.B. Konfetti-Animation oder Modal) erscheinen, um die Aktion zu bestätigen.
