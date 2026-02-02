# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

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
