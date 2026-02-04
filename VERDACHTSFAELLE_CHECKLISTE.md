# 🔍 Checkliste: Verdachtsfälle manuell prüfen

## 📋 Was sind Verdachtsfälle?

Verdachtsfälle sind **ähnliche Namen mit unterschiedlichen Emails**, die das Tool NICHT automatisch löscht.

Das Tool findet diese Fälle in der Datei: `*_verdachtsfaelle.csv`

### Beispiele (anonymisiert):
- Schmidt vs Schmitt
- Meyer vs Meier  
- Alexander vs Alex

---

## ✅ Prüf-Checkliste (in dieser Reihenfolge!)

### 1️⃣ Email-Domains vergleichen

**Frage:** Sind beide Emails vom gleichen Provider?

- ✅ **Beide @uni-rostock.de** → wahrscheinlich **2 unterschiedliche Personen**
- ✅ **Beide @gmail.com** → wahrscheinlich **2 unterschiedliche Personen**
- ⚠️ **@uni-rostock.de vs @gmail.com** → **könnte 1 Person sein** (hat 2 Emails)

**Beispiel:**
```csv
Person A: Max Schmidt, max.schmidt@uni-rostock.de
Person B: Max Schmitt, max.schmitt@uni-rostock.de
```
→ Beide haben Uni-Email mit leicht unterschiedlicher Schreibweise
→ Wahrscheinlich **2 Personen**

---

### 2️⃣ Email-Local-Part vergleichen

**Frage:** Ist der Teil vor @ ähnlich zum Namen?

- ✅ `max.schmidt@` vs `max.schmitt@` → **Name-Typo möglich**
- ✅ `m.schmidt@` vs `max.schmidt@` → wahrscheinlich **1 Person** (Kurz- vs Langform)
- ❌ `max.schmidt@` vs `julia.meier@` → sicher **2 unterschiedliche Personen**

**Beispiel:**
```csv
Person A: Max Schmidt, m.schmidt@uni-rostock.de
Person B: Max Schmidt, max.schmidt@uni-rostock.de
```
→ Gleicher Name, ähnliche Emails
→ Wahrscheinlich **1 Person** (hat sich 2x angemeldet)

---

### 3️⃣ Anmeldedatum prüfen

**Frage:** Wie weit liegen die Anmeldungen zeitlich auseinander?

- ⚠️ **< 5 Minuten** → **könnte Korrektur-Anmeldung sein** (Person hat Fehler bemerkt)
- ✅ **> 1 Stunde** → wahrscheinlich **2 unterschiedliche Personen**
- ✅ **Unterschiedliche Tage** → wahrscheinlich **2 unterschiedliche Personen**

**Beispiel:**
```csv
Person A: 2026-01-10 14:00:00
Person B: 2026-01-10 14:02:00
```
→ Nur 2 Minuten Abstand!
→ Person könnte Tippfehler bemerkt und sich neu angemeldet haben

---

### 4️⃣ Begleitungsfeld prüfen

**Frage:** Haben beide Personen unterschiedliche Begleitungen?

- ✅ **Person A** mit Begleitung **X**
- ✅ **Person B** mit Begleitung **Y**
→ Wahrscheinlich **2 unterschiedliche Personen**

- ⚠️ **Person A** mit Begleitung **X**
- ⚠️ **Person B** ohne Begleitung
→ **Könnte 1 Person sein** (hat vergessen Begleitung einzutragen)

---

### 5️⃣ Telefonnummer prüfen (falls vorhanden)

**Frage:** Sind die Telefonnummern identisch?

- ✅ **Identische Nummer** → wahrscheinlich **1 Person**
- ✅ **Unterschiedliche Nummern** → wahrscheinlich **2 Personen**
- ⚠️ **Eine Nummer fehlt** → unklar

---

## 🎯 Entscheidungshilfe: Scoring-Tabelle

| Indikator | Punkte für "1 Person" | Punkte für "2 Personen" |
|-----------|----------------------|------------------------|
| **Email-Local-Part sehr ähnlich** | +2 | 0 |
| **Email-Domain unterschiedlich** | +1 | -1 |
| **Zeitabstand < 5 Min** | +2 | 0 |
| **Zeitabstand > 1h** | 0 | +2 |
| **Begleitung unterschiedlich** | 0 | +2 |
| **Begleitung fehlt** | +1 | 0 |
| **Telefon identisch** | +3 | 0 |
| **Name-Distanz = 1** | +1 | +1 |
| **Name phonetisch gleich** | +1 | +1 |

**Auswertung:**
- **Score ≥ 5 für "1 Person"** → Wahrscheinlich Duplikat, ältere Anmeldung löschen
- **Score ≥ 5 für "2 Personen"** → Wahrscheinlich unterschiedliche Personen, beide behalten
- **Score unklar** → Im Zweifel **beide behalten**!

---

## 💡 Faustregel

### **Im Zweifel: Beide behalten!**

Lieber 1 Duplikat zu viel als 1 echte Person gelöscht.

Bei Unsicherheit:
1. ✅ Beide Personen kontaktieren (per Email)
2. ✅ Nachfragen: "Haben Sie sich 2x angemeldet?"
3. ✅ Erst dann löschen

---

## 📊 Häufige Szenarien

### Szenario 1: Phonetisch ähnliche Nachnamen
```csv
Person A: Julia Meyer, julia.meyer@uni-rostock.de
Person B: Julia Meier, julia.meier@uni-rostock.de
```
**Analyse:**
- Email-Local-Part: sehr ähnlich (+2)
- Beide Uni-Email (+1 für 2 Personen)
- Unterschiedliche Namen in Email (+1 für 2 Personen)

**Entscheidung:** Wahrscheinlich **2 Personen** (reale Namensvariante)

---

### Szenario 2: Kurzform vs Langform
```csv
Person A: Alexander Müller, a.mueller@uni-rostock.de, 14:00
Person B: Alex Müller, alex.mueller@uni-rostock.de, 14:03
```
**Analyse:**
- Zeitabstand: 3 Minuten (+2 für 1 Person)
- Email-Local-Part: a. vs alex. (+1 für 1 Person)
- Beide Uni-Email (+1 für 2 Personen)

**Entscheidung:** Wahrscheinlich **1 Person** (hat sich korrigiert)

---

### Szenario 3: Tippfehler im Nachnamen
```csv
Person A: Max Schmidt, max.schmidt@uni-rostock.de, 10.01.
Person B: Max Schmitt, max.schmitt@uni-rostock.de, 15.01.
```
**Analyse:**
- Zeitabstand: 5 Tage (+2 für 2 Personen)
- Email-Local-Part: identisch zu Namen
- Beide Uni-Email (+1 für 2 Personen)

**Entscheidung:** Wahrscheinlich **2 Personen** (reale Namensvariante)

---

## ✉️ Email-Vorlage für Rückfragen

```
Betreff: Mediball 2026 - Rückfrage zu Ihrer Anmeldung

Hallo [Vorname],

wir haben in unserem System zwei Anmeldungen gefunden, die möglicherweise zu Ihnen gehören:

- Anmeldung 1: [Datum/Uhrzeit], [Email]
- Anmeldung 2: [Datum/Uhrzeit], [Email]

Haben Sie sich versehentlich zweimal angemeldet?

Falls ja: Welche Anmeldung sollen wir behalten?
Falls nein: Bitte ignorieren Sie diese Email.

Viele Grüße,
Das Mediball-Team
```

---

## 🔒 Datenschutz

- ✅ Alle Beispiele in dieser Checkliste sind anonymisiert
- ✅ Verdachtsfälle-CSV enthält echte Daten (lokal gespeichert)
- ✅ Niemals Verdachtsfälle öffentlich teilen
- ✅ Nach Prüfung: Verdachtsfälle-CSV sicher löschen

---

## 📞 Support

Bei Fragen zur Checkliste:
- GitHub Issues: https://github.com/Fi-schi/mediball-duplicate-filter/issues
- README: https://github.com/Fi-schi/mediball-duplicate-filter

**Version:** V2.0 (2026-02-04)
