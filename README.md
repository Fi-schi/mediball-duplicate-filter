# Mediball Duplikat-Filter V2.0

[![Version](https://img.shields.io/badge/version-2.0.2-brightgreen.svg)](https://github.com/Fi-schi/mediball-duplicate-filter)

## Aktuelle Version

**Aktuelle Version: 2.0.2** 🎉

## Features

### Duplikat-Erkennung
- ✅ **V1.7.8 NEU: Hybrid Domain-Korrektur** (3-Stufen: Pattern + Known + Learning)
- ✅ **V1.7.7: Domain-Typo-Korrektur** (uni-rostok.de → uni-rostock.de)

### Technisch
- ✅ **Detaillierter Report** mit `modus`-Spalte (begleitung/person_name/person_email/suspicious/suspicious_phonetic/domain_learned)

### V7.8: Hybrid Domain-Korrektur 🚀
- 📧 **Stufe 1: Pattern-Check** (Subdomain-Typos, TLD-Typos)
  - studnet.uni-rostock.de → student.uni-rostock.de
  - web.dee → web.de
- 📋 **Stufe 2: Known-Domains** (15+ vordefinierte Domains)
- 📊 **Stufe 3: Domain-Learning** (häufige Domains aus CSV, min. 3x)
- ⚡ **+45% mehr Domain-Korrekturen** vs V7.7

### Intelligente Text-Normalisierung
V7.8

### V2.0 NEU: Production Features
- ✅ **Email-Quality-Scoring** (Typo-Emails werden erkannt, auch bei gleichem Namen!)
- ✅ **Intelligente Email-Varianten-Erkennung** (max@ vs m@ = Variante, nicht Typo)
- ✅ **Sonderzeichen-Filter** (Emojis, Excel-Artefakte werden ignoriert)
- ✅ **"Warum behalten?"-Spalte** (Transparenz im bereinigten CSV)
- 📋 **Verdachtsfälle-Checkliste** (Guidelines für Orga-Team)

## Changelog

### V1.7.8 (2026-02-03) - Hybrid Domain Intelligence
- ✅ **V7.8 NEU: 3-Stufen Hybrid Domain-Korrektur** (+45% mehr Korrekturen)
- 📧 **Pattern-Check:** Subdomain-Typos (studnet → student), TLD-Typos (.dee → .de)
- 📋 **Known-Domains:** 15+ vordefinierte Domains (uni-rostock.de, gmail.com, etc.)
- 📊 **Domain-Learning:** Häufige Domains aus CSV werden automatisch erkannt (min. 3x)
- ⚡ **Performance:** Optimiert für 1000+ Einträge, keine Verzögerung
- 🎯 **Intelligenz:** Erkennt auch seltene Custom-Domains automatisch

## 📋 "Warum behalten?"-Spalte (V2.0 NEU!)

Das **bereinigte CSV** (`*_bereinigt.csv`) enthält jetzt eine Spalte `behalten_grund`:

| behalten_grund | Bedeutung |
|----------------|-----------|
| `Einzige Anmeldung` | Keine Duplikate gefunden |
| `Uni-Email bevorzugt` | Uni-Email hat Vorrang vor privater Email |
| `Beste Email-Qualität` | Diese Email ist korrekt, andere hatte Tippfehler |
| `Früheste Anmeldung` | Früheste Anmeldung wurde behalten |
| `Niedrigste ID (Fallback)` | Bei absoluter Gleichheit: niedrigste ID |

**Beispiel:**
```csv
ID,Name,Email,behalten_grund
6699,Max Mustermann,max.mustermann@uni-rostock.de,Beste Email-Qualität
```
(Alle Namen sind anonymisiert)

## 📥 Installation

### Option 1: Vorkompilierte Executables (empfohlen)

1. Gehe zu [Releases](https://github.com/Fi-schi/mediball-duplicate-filter/releases)
2. Lade die Datei für dein Betriebssystem herunter:
   - **Windows:** `Mediball_Duplikat_Filter_Windows.exe`
   - **Mac:** `Mediball_Duplikat_Filter_Mac`
   - **Linux:** `Mediball_Duplikat_Filter_Linux`
3. Doppelklick zum Starten (keine Installation erforderlich)
4. Bei Mac/Linux: Falls nötig, Ausführungsrechte erteilen: `chmod +x Mediball_Duplikat_Filter_Mac`

### Option 2: Python-Skript ausführen

**Voraussetzungen:**
- Python 3.11 oder höher
- pip (Python Package Manager)

**Installation:**
```bash
# Repository klonen
git clone https://github.com/Fi-schi/mediball-duplicate-filter.git
cd mediball-duplicate-filter

# Dependencies installieren
pip install -r requirements.txt

# Programm starten
python3 mediball_duplicate_finder.py
```

## 🚀 Verwendung

### GUI-Anwendung

1. **Starte das Programm** (Executable oder Python-Skript)
2. **CSV-Datei auswählen:**
   - Klicke auf "Durchsuchen…"
   - Wähle deine Mediball-Anmeldungs-CSV aus
3. **Optionen konfigurieren:**
   - ✅ **Email-Typos korrigieren** (empfohlen, Standard: AN)
   - Wähle Filter-Modus (z.B. "Alle Duplikate entfernen")
   - Aktiviere "Email-Duplikate prüfen" für bessere Erkennung
4. **"Starte Filter" klicken**
5. **Ergebnisse prüfen:**
   - `*_bereinigt.csv` - Bereinigte Anmeldungen (für Import)
   - `*_entfernte_duplikate.csv` - Übersicht der entfernten Duplikate
   - `*_verdachtsfaelle.csv` - Verdachtsfälle zur manuellen Prüfung
   - `*_email_korrekturen.csv` - Liste korrigierter Emails (wenn Option aktiviert)

### CSV-Format

**Erforderliche Spalten:**
- `Nachname` oder `Name` - Name der Person
- `Email` oder `E-Mail` - Email-Adresse
- `Begleitung` (optional) - Namen von Begleitpersonen

**Beispiel:**
```csv
ID,Name,Email,Begleitung
1,Max Mustermann,max@uni-rostock.de,
2,Lisa Müller,lisa@gmail.com,Maria Schmidt
```

### Ausgabe-Dateien

| Datei | Beschreibung |
|-------|--------------|
| `*_bereinigt.csv` | Bereinigte Liste ohne Duplikate (für Import verwenden) |
| `*_entfernte_duplikate.csv` | Alle entfernten Duplikate mit Begründung |
| `*_verdachtsfaelle.csv` | Ähnliche Namen für manuelle Prüfung |
| `*_email_korrekturen.csv` | Korrigierte Email-Adressen (V2.0.2+) |

## 📚 Weitere Dokumentation

- [CHANGELOG.md](CHANGELOG.md) - Vollständige Versionshistorie
- [VERDACHTSFAELLE_CHECKLISTE.md](VERDACHTSFAELLE_CHECKLISTE.md) - Anleitung zur manuellen Prüfung
- [RELEASE.md](RELEASE.md) - Release-Prozess für Entwickler
- [WORKFLOW_RESTART.md](WORKFLOW_RESTART.md) - GitHub Actions Workflow-Anleitung

## 🆘 Support

Bei Fragen oder Problemen:
1. Prüfe die [Issues](https://github.com/Fi-schi/mediball-duplicate-filter/issues)
2. Erstelle ein neues Issue mit detaillierter Beschreibung

## 📄 Lizenz

Dieses Projekt ist für den internen Gebrauch bei Mediball-Events bestimmt.
