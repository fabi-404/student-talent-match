-- Datenbank-Schema für die Studenten-Job-Matching-App

-- 1. Tabelle: Studenten
Create Table Student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,       
    full_name TEXT NOT NULL,         
    university TEXT NOT NULL,        
    password_hash TEXT NOT NULL,     
    bio TEXT,                         
    is_active INTEGER DEFAULT 1,       --1: sichtbar  0: unsichtbar
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabelle: Arbeitgeber
Create Table Employer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 3. Tabelle: Skills
Create Table Skill (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
-- 4. Tabelle: Studenten-Skills 
Create Table Student_Skill (
    student_id INT,
    skill_id INT,
    PRIMARY KEY (student_id, skill_id),
    FOREIGN KEY (student_id) REFERENCES Student(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES Skill(id) ON DELETE CASCADE
);

-- 5. Tabelle: Swipe Logik 
Create Table Swipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    employer_id INT,
    direction INTEGER NOT NULL, -- 1: rechts (interessiert), 0: links (nicht interessiert)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    swiped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Zeitstempel der Aktion, wichtig für Matching-Logik
    UNIQUE(student_id, employer_id),
    FOREIGN KEY (student_id) REFERENCES Student(id) ON DELETE CASCADE,
    FOREIGN KEY (employer_id) REFERENCES Employer(id) ON DELETE CASCADE
);

-- 6. Matches/Einladung 
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    employer_id INTEGER NOT NULL,
    message TEXT,
    status TEXT DEFAULT 'pending',
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES Employer(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Student(id) ON DELETE CASCADE
);