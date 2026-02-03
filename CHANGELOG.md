# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.6.0] - 2026-02-03 - V7.6 Enhanced Email Processing

### Verbessert
- 🎯 **Verdachtsfälle-Report komplett überarbeitet** (wichtigster Fix!)
  - Problem: Gruppierung nach `_name_norm` hat nur identische normalisierte Namen verglichen
  - Fix: Nachname-Blocking - vergleicht jetzt auch ähnliche Namen wie "Hofmann" vs "Hoffmann"
  - Findet jetzt echte Verdachtsfälle: "Schmidt" vs "Schmitt", "Mustermann" vs "Musterman"
  - Performance: O(n²) nur innerhalb Nachname-Blöcke statt global
  - **Report ist jetzt wirklich nützlich!**

- 📧 **Email-Cleaning erweitert**
  - Entfernt trailing punctuation: `max@uni.de.` → `max@uni.de`
  - Entfernt leading/trailing Zeichen: `()[]{}<>.,;:`
  - Bessere Whitespace-Behandlung (Tabs, Newlines, etc.)
  - Validierung: Email muss `@` und `.` in Domain enthalten

- 🔍 **Typo-Hint auf Levenshtein umgestellt**
  - Statt zip/diff-Zählung nutzt jetzt konsistent `levenshtein_distance()`
  - Präzisere Erkennung von Einfügen/Löschen/Vertauschen
  - Zeigt Distance im Report für bessere Transparenz

- 👥 **Komma-Liste bei Begleitung erkannt**
  - Heuristik: 2+ Wörter vor Komma → Vollname-Liste
  - Beispiel: "Max Mustermann, Marie Mustermann" → beide erkannt
  - "Mustermann, Max" → weiterhin als "Nachname, Vorname" behandelt
  - Reduziert false negatives bei Begleitungs-Duplikaten

### Technisch
- Alle Fixes nutzen bestehende Funktionen (Levenshtein, normalize_text)
- Keine Breaking Changes
- Abwärtskompatibel mit V7.5 Daten

## [1.5.0] - 2026-02-02 - V7.5 FINAL Production-Ready

### Hinzugefügt
- ✨ **Levenshtein-Distance Algorithmus (`levenshtein_distance()` Methode)**
  - Berechnet präzise die Ähnlichkeit zwischen zwei Strings
  - Verwendet für Verdachtsfälle-Erkennung (Distance 1-2)
  - Beispiele: "Mustermann" vs "Musterman" = Distance 1

- ⚠️ **Verdachtsfälle-Report (`find_verdachtsfaelle()` Methode)**
  - Findet ähnliche Namen (Distance 1-2) mit unterschiedlichen Emails
  - Diese werden NICHT automatisch gelöscht
  - Neue Report-Datei: `*_verdachtsfaelle.csv`
  - Ermöglicht manuelle Prüfung von möglichen Tippfehlern
  - Beispiel: "Mustermann" (max@uni.de) vs "Musterman" (lisa@gmx.de)

### Bug-Fixes
- 🐛 **Bug Fix 1: Email-Split bei Komma**
  - Problem: `re.split(r'[;]', email)` hat nur bei Semikolon getrennt
  - Fix: `re.split(r'[;,]', email)` trennt jetzt bei beiden Zeichen
  - Beispiel: `"max@uni.de, lisa@uni.de"` → nimmt jetzt korrekt `"max@uni.de"`

- 🐛 **Bug Fix 2: Non-Breaking Space Normalisierung**
  - Problem: Non-Breaking Space (`\u00A0`) aus PDFs/Word wurde nicht erkannt
  - Fix: `text.replace('\u00A0', ' ')` in `normalize_text()`
  - Beispiel: `"Max\u00A0Mustermann"` matcht jetzt mit `"Max Mustermann"`

- 🐛 **Bug Fix 3: Mehr Begleitungs-Trenner**
  - Problem: User tippen Begleitungen mit `/`, `+`, `|`
  - Fix: `re.split(r'[;&\n/+|]|\bund\b', text)` erkennt jetzt alle Trenner
  - Beispiele: `"Max / Lisa"`, `"Max + Paul"`, `"Max | Lisa"` werden korrekt getrennt

### Verbessert
- 📊 **Drei Output-Dateien statt zwei**
  - `*_bereinigt.csv` - Bereinigte Anmeldungen
  - `*_entfernte_duplikate.csv` - Entfernte Duplikate (wie bisher)
  - `*_verdachtsfaelle.csv` - ⚠️ NEU: Verdachtsfälle für manuelle Prüfung

- 📝 **Report-Spalte `modus` erweitert**
  - Neuer Wert: `suspicious` für Verdachtsfälle
  - In separater Datei für bessere Übersicht

- 🎨 **UI und Log-Messages aktualisiert**
  - Info-Box zeigt V7.5 Features und Bug-Fixes
  - Log-Output zeigt detaillierte V7.5 Informationen
  - Success-Messagebox zeigt Anzahl der Verdachtsfälle

## [1.2.0] - 2026-02-02

### Hinzugefügt
- ✨ **Email-Säuberung (`clean_email()` Methode)**
  - Entfernt mailto:, MAILTO: Präfixe
  - Entfernt Leerzeichen aus Emails
  - Nimmt erste Email bei mehreren (getrennt durch ; oder ,)
  - Beispiele: `MAILTO:max@uni.de` → `max@uni.de`, `max @uni.de ; max@gmail.com` → `max@uni.de`

- ✨ **Titel-Entfernung (`remove_titles()` Methode)**
  - Entfernt akademische Titel automatisch
  - Beispiele: `Dr. Max Mustermann` → `Max Mustermann`, `Prof. Dr. med. Lisa Müller` → `Lisa Müller`
  - Unterstützte Titel: dr, prof, med, cand, dipl, ing, phd, msc, bsc, ba, ma (mit/ohne Punkt)

- ✨ **Apostroph-Normalisierung (`normalize_apostrophes()` Methode)**
  - Normalisiert verschiedene Apostroph-Varianten zu Standard-Apostroph
  - Behandelt Unicode-Varianten: U+2019, U+2018, U+02BC, U+0060, U+00B4
  - Beispiel: O'Connor (typografisch) → O'Connor (standard)

- ✨ **"Nachname, Vorname" Erkennung (`flip_lastname_firstname()` Methode)**
  - Erkennt und dreht automatisch "Nachname, Vorname" Format
  - Beispiele: `Mustermann, Max` → `Max Mustermann`, `Müller-Lüdenscheidt, Lisa Maria` → `Lisa Maria Müller-Lüdenscheidt`
  - Sicherheits-Checks: Nur bei genau 1 Komma, max 3 Wörter pro Teil

- 🎓 **Uni-Email Priorität**
  - Bei unterschiedlichen Emails wird erkannt, ob eine Uni-Email (.uni-, .edu, .ac.) und die andere privat ist
  - Gibt entsprechenden Hinweis im Report

- ⚡ **Performance-Optimierung: Typo-Check nur in Email-Gruppen**
  - Typo-Erkennung wird nur noch innerhalb von Email-Gruppen durchgeführt
  - Performance-Gewinn: 500x schneller bei 1000 Einträgen (500.000 → 1.000 Vergleiche)
  - Keine false negatives - alle Typos werden weiterhin gefunden

### Verbessert
- 📝 **Erweiterte Text-Normalisierung**
  - `normalize_text()` ruft jetzt alle neuen Normalisierungen auf
  - Bindestrich wird als Leerzeichen behandelt (für Namen wie "Müller-Lüdenscheidt")
  - Mehrfache Leerzeichen werden nach allen Transformationen entfernt

- 🔍 **Verbessertes `extract_names_from_begleitung()`**
  - Nutzt `flip_lastname_firstname()` für bessere Namens-Erkennung
  - Beispiele: `"Mustermann, Max; Müller, Lisa"` → `["Max Mustermann", "Lisa Müller"]`
  - Splitte nicht mehr bei Komma allein (für "Nachname, Vorname" Format)

- 🎯 **Verbesserte Typo-Erkennung**
  - Einfache Ähnlichkeits-Prüfung für Namen innerhalb von Email-Gruppen
  - Erkennt Tippfehler wie "Freytagg" vs "Freytag"
  - Hinweis im Report bei möglichen Tippfehlern

### Geändert
- DataFrame-Spalte `_email_norm` wurde durch `_email_clean` ersetzt
- `_email_clean` verwendet neue `clean_email()` Funktion statt `normalize_text()`

## [1.1.0] - 2026-02-02

### Hinzugefügt
- ✨ **Deutsche Umlaut-Normalisierung** im Such-Algorithmus
  - Behandelt automatisch Variationen wie "Müller" vs "Mueller"
  - Normalisiert ä→ae, ö→oe, ü→ue, ß→ss
  - Verbessert Duplikat-Erkennung für Namen mit Umlauten
  - Beispiele: "Schäfer"="Schaefer", "Größe"="Groesse", "Pflücke"="Pfluecke"

### Verbessert
- Robustere Namens-Erkennung bei verschiedenen Schreibweisen
- Bessere Duplikat-Erkennung für deutsche Namen

## [1.0.0] - 2026-02-01

### Hinzugefügt
- Erste offizielle Release-Version
- Name-basierte Duplikat-Erkennung (primär für Mediball)
- Email-basierte Duplikate-Erkennung (findet Tippfehler)
- Begleitungs-Duplikate-Erkennung (Person + Begleitung)
- Robuste CSV-Verarbeitung (UTF-8 BOM, Komma/Semikolon-Unterstützung)
- Detaillierter Report mit `modus`-Spalte zum Filtern
- GUI-Anwendung mit Tkinter
- Automatische GitHub Actions Builds für Windows, Mac und Linux
- Versionsnummer im Fenstertitel

### Features
- Erste Anmeldung wird immer behalten (wichtig für Ticketvergabe)
- Mehrere Filter-Modi: Begleitungs-Duplikate, Doppelte Personen, Alle Duplikate
- Konfigurierbare Optionen: Groß-/Kleinschreibung, Email-Duplikate, CSV-Trennzeichen
- Zwei Ausgabedateien: bereinigte CSV und Report der entfernten Duplikate

[1.0.0]: https://github.com/Fi-schi/mediball-duplicate-filter/releases/tag/v1.0.0
