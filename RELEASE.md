# Release-Prozess

Diese Anleitung beschreibt, wie eine neue Release-Version erstellt wird.

## Voraussetzungen

- Alle Änderungen sind committed und in den main Branch gemerged
- Alle Tests laufen erfolgreich
- CHANGELOG.md ist aktualisiert

## Release erstellen

### 1. Version aktualisieren

Aktualisiere die Versionsnummer in folgenden Dateien:
- `VERSION` - Die Versionsnummer (z.B. `1.0.0`)
- `mediball_duplicate_finder_production_V7.py` - Die `__version__` Variable
- `CHANGELOG.md` - Füge einen neuen Abschnitt für die Version hinzu

### 2. Commit und Push

```bash
git add VERSION mediball_duplicate_finder_production_V7.py CHANGELOG.md
git commit -m "Release v1.0.0"
git push origin main
```

### 3. Tag erstellen und pushen

```bash
# Tag erstellen (mit führendem 'v')
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag pushen
git push origin v1.0.0
```

### 4. GitHub Actions wird automatisch ausgeführt

Nach dem Pushen des Tags:
1. GitHub Actions startet automatisch den Build-Workflow
2. Executables werden für Windows, Mac und Linux gebaut
3. Ein GitHub Release wird automatisch erstellt
4. Die Executables werden zum Release hinzugefügt

### 5. Release überprüfen

- Gehe zu: https://github.com/Fi-schi/mediball-duplicate-filter/releases
- Überprüfe, dass das Release korrekt erstellt wurde
- Teste die Downloads für jede Plattform

## Versionsnummern-Schema

Wir folgen [Semantic Versioning](https://semver.org/lang/de/):

- **MAJOR** (1.x.x): Inkompatible API-Änderungen
- **MINOR** (x.1.x): Neue Features, abwärtskompatibel
- **PATCH** (x.x.1): Bugfixes, abwärtskompatibel

Beispiele:
- `1.0.0` - Erste stabile Version
- `1.1.0` - Neue Features hinzugefügt
- `1.1.1` - Bugfix
- `2.0.0` - Breaking Changes

## Troubleshooting

### Build schlägt fehl

1. Überprüfe GitHub Actions Logs: https://github.com/Fi-schi/mediball-duplicate-filter/actions
2. Stelle sicher, dass alle Dependencies korrekt sind
3. Teste den Build lokal mit PyInstaller

### Release wurde nicht automatisch erstellt

1. Überprüfe, dass der Tag mit `v` beginnt (z.B. `v1.0.0`)
2. Überprüfe die GitHub Actions Logs
3. Stelle sicher, dass die Permissions korrekt sind (contents: write)

### Tag löschen und neu erstellen

Wenn ein Tag fehlerhaft ist:

```bash
# Lokal löschen
git tag -d v1.0.0

# Remote löschen
git push origin :refs/tags/v1.0.0

# Neu erstellen
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Manual Release (falls GitHub Actions nicht verfügbar)

Falls GitHub Actions nicht verwendet werden kann:

```bash
# Dependencies installieren
pip install -r requirements.txt pyinstaller

# Build für aktuelles OS
pyinstaller --name=Mediball_Duplikat_Filter --onefile --windowed mediball_duplicate_finder_production_V7.py

# Executable findest du in: dist/
```

Dann manuell auf GitHub Release hochladen.
