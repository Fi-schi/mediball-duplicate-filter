# 🎭 Mediball Duplikat-Filter V7

Professionelles Tool zum Filtern von Duplikaten in Mediball-CSV-Anmeldungen.

## 📥 Download

**[→ Zu den Releases (Download)](../../releases/latest)**

Wähle die passende Version für dein Betriebssystem:

| Betriebssystem | Datei |
|----------------|-------|
| 🪟 **Windows** | `Mediball_Duplikat_Filter_Windows.exe` |
| 🍎 **Mac** | `Mediball_Duplikat_Filter_Mac` |
| 🐧 **Linux** | `Mediball_Duplikat_Filter_Linux` |

## ✨ Features

- ✅ **Name-basierte Duplikat-Erkennung** (primär für Mediball)
- ✅ **Email-basierte Duplikate** (zusätzlich, findet Tippfehler)
- ✅ **Begleitungs-Duplikate** (Person hat sich selbst + als Begleitung angemeldet)
- ✅ **Robuste CSV-Verarbeitung** (UTF-8 BOM, Komma/Semikolon, mehrere Namen)
- ✅ **Detaillierter Report** mit `modus`-Spalte zum Filtern
- ✅ **Erste Anmeldung bleibt** (wichtig für Ticketvergabe)

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

**Zwei Dateien werden erstellt:**

1. **`*_bereinigt.csv`** - Bereinigte Anmeldungen (nur eindeutige)
2. **`*_entfernte_duplikate.csv`** - Report aller entfernten Duplikate

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

| modus | Bedeutung |
|-------|-----------|
| `begleitung` | Person hat sich selbst + als Begleitung angemeldet |
| `person_name` | Gleicher Name, mehrfach angemeldet |
| `person_email` | Gleiche Email, unterschiedlicher Name (Tippfehler?) |

## ⚠️ Wichtig

- **Gleicher Name = gleiche Person** (auch bei unterschiedlichen Emails!)
- **Erste Anmeldung** (nach Datum/Zeit) wird IMMER behalten
- Bei fehlendem Datum: Niedrigere ID = früher
- **Prüfe den Report** bei Zweifeln!

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
