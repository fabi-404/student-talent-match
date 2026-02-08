## 🚀 Installation & Ausführung (How to execute)

Folge diesen Schritten, um die Anwendung lokal auf deinem Computer zum Laufen zu bringen.

### 1. Voraussetzungen

Stelle sicher, dass du **Python 3.x** installiert hast.

```bash
python --version
# oder
python3 --version

```

### 2. Repository klonen & Verzeichnis öffnen

```bash
git clone <DEIN_REPO_URL>
cd student-talent-match

```

### 3. Virtuelle Umgebung erstellen (Empfohlen)

Es ist Best Practice, eine virtuelle Umgebung zu nutzen, um Abhängigkeiten isoliert zu halten.

* **Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate

```


* **Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 4. Abhängigkeiten installieren

Installiere die benötigten Python-Pakete (Flask und Flask-WTF).

```bash
pip install Flask Flask-WTF email-validator

```

*(Hinweis: Falls eine `requirements.txt` existiert, nutze alternativ: `pip install -r requirements.txt`)*

### 5. Datenbank initialisieren

Bevor die App startet, muss die SQLite-Datenbank und die Tabellenstruktur erstellt werden. Führe dazu das `database.py` Skript aus:

```bash
python database.py

```

*Erwartete Ausgabe:* `Neue Datenbank wurde erstellt.` (oder `Datenbank existiert bereits...`)
*Dadurch wird die Datei `student_talent.db` im Hauptverzeichnis erzeugt.*

### 6. Anwendung starten

Starte den Flask Development Server:

```bash
flask run

```

*(Alternativ: `python -m flask run`)*

### 7. App im Browser öffnen

Öffne deinen Browser und gehe auf:
👉 **[http://127.0.0.1:5000](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5000)**

---

### 🛠 Troubleshooting / Debugging

* **Fehler: "no such table"**:
Das bedeutet, die Datenbank wurde nicht initialisiert. Führe Schritt 5 (`python database.py`) erneut aus.
* **Datenbank zurücksetzen**:
Wenn du die Datenbank komplett leeren willst, lösche einfach die Datei `student_talent.db` und führe `python database.py` erneut aus.
* **Test-Skript**:
Um zu prüfen, ob alle Tabellen korrekt angelegt wurden, kannst du das Test-Skript ausführen:
```bash
python test_tables.py

```

---

### 🔑 Test-Accounts (Optional)

Da es noch keine Seed-Daten gibt, musst du dich zunächst registrieren:

1. Klicke auf **"Start als Unternehmen"** -> Registrieren.
2. Klicke auf **"Start als Student"** -> Registrieren.
3. Logge dich als Student ein, lege Skills an und setze das Profil auf "Sichtbar".
4. Logge dich als Unternehmen ein, filtere nach den Skills und beginne zu swipen.
