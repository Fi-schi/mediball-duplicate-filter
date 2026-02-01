# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

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
