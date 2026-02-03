# Workflow Neustart-Anleitung

## Produktionsserver/Agent neu starten

Da der Workflow bereits mit `workflow_dispatch` konfiguriert ist, kann er jederzeit manuell über die GitHub Actions UI neu gestartet werden.

### Schritte zum manuellen Neustart:

1. **GitHub Actions öffnen:**
   - Gehe zu: https://github.com/Fi-schi/mediball-duplicate-filter/actions

2. **Workflow auswählen:**
   - Klicke auf "Build Executables for All Platforms" in der linken Sidebar

3. **Workflow starten:**
   - Klicke auf den Button "Run workflow" (rechts oben)
   - Wähle Branch: `main`
   - Klicke auf "Run workflow" (grüner Button)

4. **Status überprüfen:**
   - Der Workflow startet innerhalb weniger Sekunden
   - Du siehst den Fortschritt in Echtzeit
   - Nach Abschluss werden die Artifacts (Executables) verfügbar sein

### Was passiert beim Workflow-Run?

Der Workflow baut automatisch:
- **Windows Executable** (`Mediball_Duplikat_Filter.exe`)
- **Mac Executable** (`Mediball_Duplikat_Filter`)
- **Linux Executable** (`Mediball_Duplikat_Filter`)

Die Executables werden als Artifacts gespeichert und sind 90 Tage verfügbar.

### Automatischer Trigger

Alternativ wird der Workflow automatisch ausgelöst bei:
- **Tag-Push:** Wenn ein Tag mit dem Muster `v*` gepusht wird (z.B. `v1.5.0`)
  - In diesem Fall wird zusätzlich ein GitHub Release mit den Executables erstellt

### Status-Überprüfung

Aktueller Status der letzten Runs:
```
✓ v1.2      - completed/success (2026-02-02)
✓ v1.0      - completed/success (2026-02-01)  
✓ main      - completed/success (2026-02-01)
```

Alle Workflows sind erfolgreich abgeschlossen. Es gibt keine fehlgeschlagenen Runs, die neu gestartet werden müssten.

### Workflow-Konfiguration

Der Workflow ist in `.github/workflows/build.yml` definiert und läuft auf:
- **Windows:** `windows-latest`
- **Mac:** `macos-latest`
- **Linux:** `ubuntu-latest`

Python Version: 3.11

### Hinweis

Falls der Workflow bei einem Run fehlschlägt, kann er direkt über die GitHub UI neu gestartet werden:
1. Gehe zu dem fehlgeschlagenen Run
2. Klicke auf "Re-run jobs"
3. Wähle "Re-run all jobs"
