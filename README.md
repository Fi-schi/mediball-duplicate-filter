# Mediball Duplikat-Filter V2.0

[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)](https://github.com/Fi-schi/mediball-duplicate-filter)

## Aktuelle Version

**Aktuelle Version: 2.0.0** 🎉

## Features

### Duplikat-Erkennung
- ✅ **V7.8 NEU: Hybrid Domain-Korrektur** (3-Stufen: Pattern + Known + Learning)
- ✅ **V7.7: Domain-Typo-Korrektur** (uni-rostok.de → uni-rostock.de)

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

### V7.8 (2026-02-03) - Hybrid Domain Intelligence
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
