# 🔍 Checkliste: Verdachtsfälle manuell prüfen

## 📋 Was sind Verdachtsfälle?

Verdachtsfälle sind **ähnliche Namen mit unterschiedlichen Emails**, die das Tool NICHT automatisch löscht.

Beispiele:
- Schmidt vs Schmitt
- Meyer vs Meier
- Alexander vs Alex

---

## ✅ Prüf-Checkliste (in dieser Reihenfolge!)

### 1. Email-Domains vergleichen

**Frage:** Sind beide Emails vom gleichen Provider?

- ✅ Beide @uni-rostock.de → wahrscheinlich **2 Personen**
- ✅ Beide @gmail.com → wahrscheinlich **2 Personen**
- ⚠️ @uni-rostock.de vs @gmail.com → **könnte 1 Person sein**

**Beispiel:**
```
ID 100: Max Schmidt, max.schmidt@uni-rostock.de
ID 101: Max Schmitt, max.schmitt@uni-rostock.de
→ Wahrscheinlich 2 Personen (beide Uni-Mail mit unterschiedlicher Schreibweise)
```

---

### 2. Email-Local-Part vergleichen

**Frage:** Ist der Teil vor @ ähnlich?

- ✅ max.schmidt@ vs max.schmitt@ → **könnte Typo sein**
- ✅ m.schmidt@ vs max.schmidt@ → wahrscheinlich **1 Person**
- ❌ max.schmidt@ vs julia.meier@ → sicher **2 Personen**

---

### 3. Anmeldedatum prüfen

**Frage:** Wie weit liegen die Anmeldungen auseinander?

- ⚠️ < 5 Minuten → **könnte Korrektur-Anmeldung sein**
- ✅ > 1 Stunde → wahrscheinlich **2 Personen**

**Beispiel:**
```
ID 100: 2026-01-10 14:00:00
ID 101: 2026-01-10 14:02:00
→ Nur 2 Min Abstand → Person könnte Fehler bemerkt und neu angemeldet haben
```

---

### 4. Begleitungsfeld prüfen

**Frage:** Sind die Begleitungen unterschiedlich?

- ✅ Person A mit Begleitung X
- ✅ Person B mit Begleitung Y
→ Wahrscheinlich **2 Personen**

---

## 🎯 Entscheidungshilfe

| Indikator | 1 Person | 2 Personen |
|-----------|----------|------------|
| **Email-Local-Part** | Sehr ähnlich | Komplett unterschiedlich |
| **Email-Domain** | Uni vs Privat | Beide gleich |
| **Zeitabstand** | < 5 Min | > 1h |
| **Begleitung** | Gleich/leer | Unterschiedlich |
| **Name-Distanz** | 1-2 Buchstaben | Phonetisch ähnlich |

---

## 💡 Faustregel

**Im Zweifel: Beide behalten!**

Lieber 1 Duplikat zu viel als 1 echte Person gelöscht.
