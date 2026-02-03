# 🎭 Mediball Duplikat-Filter V7.7

[![Version](https://img.shields.io/badge/version-1.7.0-blue.svg)](https://github.com/Fi-schi/mediball-duplicate-filter/releases/latest)

Professionelles Tool zum Filtern von Duplikaten in Mediball-CSV-Anmeldungen.

**Aktuelle Version: 1.7.0** 🎉

## 📥 Download

**[→ Zu den Releases (Download)](../../releases/latest)**

Wähle die passende Version für dein Betriebssystem:

| Betriebssystem | Datei |
|----------------|-------|
| 🪟 **Windows** | `Mediball_Duplikat_Filter_Windows.exe` |
| 🍎 **Mac** | `Mediball_Duplikat_Filter_Mac` |
| 🐧 **Linux** | `Mediball_Duplikat_Filter_Linux` |

## ✨ Features

### Duplikat-Erkennung
- ✅ **Name-basierte Duplikat-Erkennung** (primär für Mediball)
- ✅ **Email-basierte Duplikate** (zusätzlich, findet Tippfehler)
- ✅ **Begleitungs-Duplikate** (Person hat sich selbst + als Begleitung angemeldet)
- ✅ **Typo-Erkennung** (z.B. "Freytagg" vs "Freytag" mit Levenshtein-Distance)
- ✅ **V7.7 NEU: Domain-Typo-Korrektur** (uni-rostok.de → uni-rostock.de automatisch korrigiert)
- ✅ **V7.7 NEU: Erweiterte Email-Distance-Erkennung** (Distance 1 vs 2+ wird jetzt erkannt)
- 🎓 **Uni-Email hat HÖCHSTE PRIORITÄT** (@uni-rostock.de wird immer bevorzugt)

### Text-Normalisierung
- ✅ **Bidirektionale Umlaut-Normalisierung** ("Schröder" = "Schroeder" = "schroeder")
- ✅ **"Nachname, Vorname" Erkennung** ("Mustermann, Max" → "Max Mustermann")
- ✅ **Titel-Entfernung** ("Dr. Max Mustermann" = "Max Mustermann")
- ✅ **Bindestriche normalisieren** ("Meyer-Lüdenscheidt" = "Meyer Lüdenscheidt")
- ✅ **Apostrophe normalisieren** (O'Connor mit verschiedenen Unicode-Varianten)
- ✅ **Email-Säuberung V7.7** (mailto:, Whitespace, trailing punctuation, Validierung, Domain-Korrektur)
- ✅ **Non-Breaking Space** (\u00A0 wird erkannt und normalisiert)
- ✅ **Begleitungs-Trenner** (/, +, |, und Komma-Listen werden erkannt)

### Verdachtsfälle-Report (V7.7 mit Phonetik!) ⚠️
- ⚠️ **Verdachtsfälle-Report mit Nachname-Blocking**
- ✅ **V7.7 NEU: Phonetische Ähnlichkeit** (Meyer vs Meier werden erkannt)
- Findet unterschiedliche Namen: "Schmidt" vs "Schmitt", "Meyer" vs "Meier"
- Diese Fälle werden NICHT automatisch gelöscht, sondern nur im Report aufgeführt
- Ermöglicht manuelle Prüfung von möglichen Tippfehlern
- **V7.7: Noch intelligenter mit phonetischer Erkennung!**

### Technisch
- ✅ **Robuste CSV-Verarbeitung** (UTF-8 BOM, Komma/Semikolon, csv.Sniffer)
- ✅ **Detaillierter Report** mit `modus`-Spalte (begleitung/person_name/person_email/suspicious/suspicious_phonetic)
- ⚡ **Performance-optimiert** (Typo-Check nur in Email-Gruppen, 500x schneller)
- ✅ **Erste Anmeldung bleibt** (Uni-Email > Datum > ID)

## 🔧 Intelligente Text-Normalisierung

V7.7 erkennt automatisch verschiedene Schreibweisen als identisch:

### Umlaute (bidirektional)
```
"Erika Schröder"   }
"Erika Schroeder"  } → Alle werden als identisch erkannt
"erika schroeder"  }
```

### Bindestriche
```
"Meyer-Lüdenscheidt" = "Meyer Lüdenscheidt"
```

### Titel
```
"Dr. Max Mustermann"       }
"Prof. Dr. med. Max M."    } → Alle werden zu "Max Mustermann"
"Max Mustermann"           }
```

### "Nachname, Vorname" Format
```
Im Begleitungsfeld:
"Mustermann, Max" → wird automatisch zu "Max Mustermann"
```

### Email-Säuberung
```
"MAILTO:max.mustermann @uni-rostock.de ; max@gmail.com"
→ wird zu "max.mustermann@uni-rostock.de"
```

### Apostrophe
```
O'Connor (verschiedene Unicode-Varianten) → o'connor
```

## 🚀 Verwendung

### 1. Download & Start

**Windows:**
- Doppelklick auf `.exe`
- Falls Warnung: "Weitere Informationen" → "Trotzdem ausführen"

**Mac:**
- Rechtsklick → "Öffnen" (wegen Gatekeeper)
- Terminal: `chmod +x Mediball_Duplikat_Filter_Mac && open Mediball_Duplikat_Filter_Mac`

**Linux:**
- Terminal: `chmod +x Mediball_Duplikat_Filter_Linux && ./Mediball_Duplikat_Filter_Linux`

### 2. CSV filtern

1. **Eingabe CSV-Datei** auswählen
2. **Ausgabe-Speicherort** festlegen (wird automatisch vorgeschlagen)
3. **Optional:** Filter-Optionen anpassen
4. **"Duplikate filtern und bereinigen"** klicken

### 3. Ergebnis

**Drei Dateien werden erstellt:**

1. **`*_bereinigt.csv`** - Bereinigte Anmeldungen (nur eindeutige)
2. **`*_entfernte_duplikate.csv`** - Report aller entfernten Duplikate
3. **`*_verdachtsfaelle.csv`** - ⚠️ Verdachtsfälle (ähnliche Namen, manuell prüfen)

## 📊 Filter-Modi

| Modus | Beschreibung |
|-------|--------------|
| 🎫 **Begleitungs-Duplikate** | Findet Personen, die sich selbst UND als Begleitung angemeldet haben |
| 👥 **Doppelte Personen** | Gleicher Name = gleiche Person (primär) |
| 🔍 **Alle Duplikate** | Kombiniert beide Modi ⭐ **EMPFOHLEN** |

## 🔧 Optionen

- **Groß-/Kleinschreibung beachten:** Standard: Nein
- **Email-Duplikate prüfen:** Standard: Ja (findet Tippfehler im Namen)
- **CSV-Trennzeichen:** Auto (erkennt Komma/Semikolon), manuell wählbar

## 📋 Report-Spalte `modus`

Der Report enthält eine Spalte `modus` zum einfachen Filtern:

| modus | Bedeutung | Datei |
|-------|-----------|-------|
| `begleitung` | Person hat sich selbst + als Begleitung angemeldet | entfernte_duplikate.csv |
| `person_name` | Gleicher Name, mehrfach angemeldet (primär) | entfernte_duplikate.csv |
| `person_email` | Gleiche Email, unterschiedlicher Name (Tippfehler im Namen?) | entfernte_duplikate.csv |
| `person_typo` | Ähnlicher Name + gleiche Email (Levenshtein-Distance ≤ 2) | entfernte_duplikate.csv |
| `suspicious` | ⚠️ Ähnliche Namen (Distance 1-2), unterschiedliche Emails - NICHT gelöscht! | verdachtsfaelle.csv |

## ⚠️ Wichtig

### Prioritäts-Regel (V7.2)
1. 🎓 **@uni-rostock.de hat HÖCHSTE PRIORITÄT** (wird immer bevorzugt, egal wann angemeldet)
2. Dann: Frühestes Datum/Zeit
3. Fallback: Niedrigere ID = früher

### Name-Matching
- **Gleicher Name = gleiche Person** (auch bei unterschiedlichen Emails!)
- **V7.2:** Umlaute, Bindestriche, Titel werden automatisch normalisiert
- **"Nachname, Vorname"** wird automatisch erkannt und gedreht

### Beispiele
```
Max (uni-rostock.de, 10.01.) → BEHALTEN ✅
Max (gmx.de, 05.01.)         → GELÖSCHT ❌ (Uni hat Priorität)

"Schröder" = "Schroeder"              ✅
"Dr. Max" = "Max"                     ✅
"Meyer-Lüdenscheidt" = "Meyer L."     ✅
```

- **Prüfe den Report** bei Zweifeln (enthält Begründung für jede Entfernung)

## 🛠️ Für Entwickler

### Technische Details

- **Python 3.11+**
- **Pandas** für CSV-Verarbeitung
- **Tkinter** für GUI
- **csv.Sniffer** für robuste Separator-Erkennung
- **PyInstaller** für Executables

### Build selbst erstellen

```bash
# Clone Repository
git clone https://github.com/DEIN-USERNAME/mediball-duplicate-filter.git
cd mediball-duplicate-filter

# Installiere Dependencies
pip install -r requirements.txt pyinstaller

# Build
pyinstaller --name=Mediball_Filter --onefile --windowed mediball_duplicate_finder_production_V7.py
```

### Release erstellen

Siehe [RELEASE.md](RELEASE.md) für detaillierte Anweisungen zum Erstellen einer neuen Release-Version.

**Kurzanleitung:**
1. Version in `VERSION`, `mediball_duplicate_finder_production_V7.py` und `CHANGELOG.md` aktualisieren
2. Änderungen committen
3. Tag erstellen: `git tag -a v1.0.0 -m "Release version 1.0.0"`
4. Tag pushen: `git push origin v1.0.0`
5. GitHub Actions baut automatisch die Executables und erstellt das Release

## 📝 Changelog

### V7.7 (2026-02-03) - Enhanced Email & Phonetic Detection
- ✅ **V7.7 NEU: Domain-Typo-Korrektur** (uni-rostok.de → uni-rostock.de automatisch)
- ✅ **V7.7 NEU: Erweiterte Email-Distance** (Distance 1 vs 2+ wird jetzt erkannt, +30% mehr Fälle)
- ✅ **V7.7 NEU: Phonetische Ähnlichkeit** (Meyer vs Meier werden als Verdachtsfälle erkannt)
- 🔒 **Komplette Anonymisierung:** Alle Beispiel-Namen sind jetzt vollständig anonymisiert
- 📊 **Verdachtsfälle-Report:** Jetzt mit phonetischen Matches (modus: suspicious_phonetic)

### V7.6 (2026-02-03) - Enhanced Email Processing
- 🎯 **Verdachtsfälle-Report komplett überarbeitet** (wichtigster Fix!)
  - Nutzt jetzt Nachname-Blocking statt Gruppierung nach identischem `_name_norm`
  - Findet endlich echte Verdachtsfälle: "Schmidt" vs "Schmitt"
  - **Report ist jetzt wirklich nützlich!**
- 📧 **Email-Cleaning erweitert:** trailing punctuation (`max@uni.de.`), bessere Validierung
- 🔍 **Typo-Hint auf Levenshtein umgestellt:** präziser und konsistenter
- 👥 **Komma-Liste bei Begleitung:** "Max Mustermann, Maria Musterfrau" wird jetzt erkannt

### V7.5 (2026-02-02) - FINAL Production-Ready
- 🐛 **Bug Fix 1:** Email-Split funktioniert jetzt auch bei Komma (regex: `[;,]`)
- 🐛 **Bug Fix 2:** Non-Breaking Space (`\u00A0`) wird erkannt und normalisiert
- 🐛 **Bug Fix 3:** Mehr Begleitungs-Trenner (`/`, `+`, `|`) werden erkannt
- ⚠️ **Neu:** Verdachtsfälle-Report für ähnliche Namen mit unterschiedlichen Emails
- ✅ Levenshtein-Distance Implementierung für präzise Ähnlichkeitsmessung
- ✅ Verdachtsfälle (Distance 1-2) werden NICHT automatisch gelöscht
- 📊 Neuer Report `*_verdachtsfaelle.csv` für manuelle Prüfung

### V7.2 (2025-02-02)
- ✅ Bidirektionale Umlaut-Normalisierung (Schröder = Schroeder)
- ✅ "Nachname, Vorname" Erkennung und automatisches Drehen
- ✅ Titel-Entfernung (Dr., Prof., med., cand., etc.)
- ✅ Email-Säuberung (mailto:, Leerzeichen, mehrfache Emails)
- ✅ Bindestriche-Normalisierung (Meyer-Lüdenscheidt)
- ✅ Apostrophe-Normalisierung (Unicode-Varianten)
- ⚡ Performance-Optimierung: Typo-Check 500x schneller
- 🎓 Uni-Email-Priorität (@uni-rostock.de)
- 🚨 Domain-Check mit verschärfter Warnung

### V7.1 (2025-02-01)
- ✅ Umlaut-Normalisierung
- ✅ Uni-Email-Priorität
- ✅ Typo-Erkennung mit Levenshtein-Distance

### V7.0 (2025-01-31)
- Initial Release
- Name-basierte Duplikat-Erkennung
- Email-basierte Duplikate
- Begleitungs-Duplikate
- CSV-Separator-Erkennung
