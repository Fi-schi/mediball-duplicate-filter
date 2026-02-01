import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pathlib import Path
import traceback
import re
import csv

__version__ = "1.0.0"

class MediballDuplicateFinder:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Mediball CSV Duplikat-Filter v{__version__}")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        
        self.input_file = None
        self.output_file = None
        self.detected_separator = ","
        
        self.setup_ui()
    
    def setup_ui(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Titel
        title_label = ttk.Label(main_frame, text="🎭 Mediball Duplikat-Filter", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Eingabedatei-Bereich
        ttk.Label(main_frame, text="Eingabe CSV-Datei:").grid(row=1, column=0, 
                                                               sticky=tk.W, pady=5)
        self.input_label = ttk.Label(main_frame, text="Keine Datei ausgewählt", 
                                     relief="sunken", width=50)
        self.input_label.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Durchsuchen…", 
                   command=self.browse_input).grid(row=1, column=2, pady=5)
        
        # Ausgabeort-Bereich
        ttk.Label(main_frame, text="Bereinigte Ausgabe-Datei:").grid(row=2, column=0, 
                                                           sticky=tk.W, pady=5)
        self.output_label = ttk.Label(main_frame, text="Keine Datei ausgewählt", 
                                      relief="sunken", width=50)
        self.output_label.grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Durchsuchen…", 
                   command=self.browse_output).grid(row=2, column=2, pady=5)
        
        # Optional: Duplikate-Report Datei
        ttk.Label(main_frame, text="Report der entfernten Duplikate:").grid(row=3, column=0, 
                                                           sticky=tk.W, pady=5)
        self.report_label = ttk.Label(main_frame, text="Optional - wird automatisch erstellt", 
                                      relief="sunken", width=50)
        self.report_label.grid(row=3, column=1, padx=5, pady=5)
        self.save_report = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Report speichern", 
                       variable=self.save_report).grid(row=3, column=2, pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=4, column=0, 
                                                            columnspan=3, 
                                                            sticky=(tk.W, tk.E), 
                                                            pady=15)
        
        # Optionen
        options_frame = ttk.LabelFrame(main_frame, text="Filter-Optionen", padding="10")
        options_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                          pady=10)
        
        # Suchmodus
        ttk.Label(options_frame, text="Was soll gefiltert werden?", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.search_mode = tk.StringVar(value="alle")
        
        ttk.Radiobutton(options_frame, 
                       text="🎫 Begleitungs-Duplikate (Person hat sich selbst angemeldet + ist als Begleitung eingetragen)",
                       variable=self.search_mode, 
                       value="begleitung").grid(row=1, column=0, columnspan=2, 
                                                sticky=tk.W, padx=20, pady=3)
        
        ttk.Radiobutton(options_frame, 
                       text="👥 Doppelte Personen (gleicher Name = gleiche Person) ⭐ PRIMÄR",
                       variable=self.search_mode, 
                       value="person").grid(row=2, column=0, columnspan=2, 
                                           sticky=tk.W, padx=20, pady=3)
        
        ttk.Radiobutton(options_frame, 
                       text="🔍 Alle Duplikate (beide Modi kombiniert) ⭐ EMPFOHLEN",
                       variable=self.search_mode, 
                       value="alle").grid(row=3, column=0, columnspan=2, 
                                         sticky=tk.W, padx=20, pady=3)
        
        # Case-Sensitivity
        self.case_sensitive = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Groß-/Kleinschreibung beachten beim Vergleich", 
                       variable=self.case_sensitive).grid(row=4, column=0, 
                                                          columnspan=2, 
                                                          sticky=tk.W, 
                                                          padx=20, pady=5)
        
        # Email-basierte Duplikate (zusätzlich)
        self.check_email_duplicates = tk.BooleanVar(value=True)
        email_check = ttk.Checkbutton(options_frame, 
                       text="✓ Auch gleiche Email prüfen (zusätzlich, findet Tippfehler im Namen)", 
                       variable=self.check_email_duplicates)
        email_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=20, pady=5)
        
        # Output separator
        ttk.Label(options_frame, text="CSV-Trennzeichen für Ausgabe:").grid(
            row=6, column=0, sticky=tk.W, padx=20, pady=5)
        self.output_sep = tk.StringVar(value="auto")
        sep_frame = ttk.Frame(options_frame)
        sep_frame.grid(row=6, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(sep_frame, text="Auto (wie Input)", variable=self.output_sep, value="auto").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sep_frame, text="Komma", variable=self.output_sep, value=",").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(sep_frame, text="Semikolon", variable=self.output_sep, value=";").pack(side=tk.LEFT, padx=5)
        
        # Info-Box
        info_frame = ttk.Frame(options_frame, relief="solid", borderwidth=1)
        info_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10, padx=20)
        
        info_text = ("ℹ️  WICHTIG: Gleicher Name = gleiche Person (wird automatisch entfernt).\n"
                    "   ⚠️  Auch bei unterschiedlichen Emails! Prüfe den Report bei Zweifeln.\n"
                    "   Die ERSTE Anmeldung (nach Datum/Zeit) wird behalten.")
        ttk.Label(info_frame, text=info_text, foreground="blue", 
                 font=('Arial', 9)).pack(padx=10, pady=10)
        
        # Aktion Button
        self.process_button = ttk.Button(main_frame, text="🔎 Duplikate filtern und bereinigen", 
                                        command=self.find_duplicates,
                                        state="disabled")
        self.process_button.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Ergebnis-Textbereich
        result_frame = ttk.LabelFrame(main_frame, text="Ergebnisse & Log", padding="5")
        result_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.result_text = tk.Text(result_frame, height=14, width=95, wrap=tk.WORD,
                                   font=('Consolas', 9))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", 
                                 command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # Grid-Gewichte
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="CSV-Datei auswählen",
            filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )
        if filename:
            self.input_file = filename
            self.input_label.config(text=Path(filename).name)
            
            # Auto-suggest output filename
            if not self.output_file:
                suggested = str(Path(filename).parent / (Path(filename).stem + "_bereinigt.csv"))
                self.output_file = suggested
                self.output_label.config(text=Path(suggested).name)
            
            self.check_ready()
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Bereinigte Datei speichern als",
            defaultextension=".csv",
            filetypes=[("CSV Dateien", "*.csv"), ("Alle Dateien", "*.*")]
        )
        if filename:
            self.output_file = filename
            self.output_label.config(text=Path(filename).name)
            self.check_ready()
    
    def check_ready(self):
        if self.input_file and self.output_file:
            self.process_button.config(state="normal")
    
    def normalize_text(self, text):
        """Normalisiert Text für Vergleich"""
        if pd.isna(text) or text is None:
            return ""
        text = str(text).strip()
        # ✅ V7: Entferne mehrfache Leerzeichen
        text = re.sub(r'\s+', ' ', text)
        if not self.case_sensitive.get():
            text = text.lower()
        return text
    
    def extract_names_from_begleitung(self, text):
        """
        Extrahiert Namen aus Begleitungsfeld.
        Splittet bei Komma, Semikolon, "und", "&", Zeilenumbrüche.
        Returns: Liste normalisierter Namen
        """
        if pd.isna(text) or text is None:
            return []
        
        text = str(text).strip()
        
        # Splitte bei gängigen Trennern
        # Trenne bei: , ; & "und" "Und" Zeilenumbruch (auch mit Leerzeichen drum herum)
        parts = re.split(r'[,;&\n]|\sund\s|\sUnd\s', text, flags=re.IGNORECASE)
        
        # Normalisiere jeden Teil
        names = []
        for part in parts:
            part_clean = part.strip()
            # Entferne Klammer-Inhalte wie "(Begleitung)"
            part_clean = re.sub(r'\([^)]*\)', '', part_clean).strip()
            
            if part_clean:
                # Normalisiere wie andere Namen
                normalized = self.normalize_text(part_clean)
                if normalized:
                    names.append(normalized)
        
        return names
    
    def parse_datetime(self, date_str):
        """Parst Datum aus verschiedenen Formaten - robust"""
        if pd.isna(date_str) or str(date_str).strip() == "":
            return pd.NaT
        
        # Erst normales Format
        dt = pd.to_datetime(date_str, errors="coerce")
        
        # Falls fehlgeschlagen: dayfirst (europäisch)
        if pd.isna(dt):
            dt = pd.to_datetime(date_str, errors="coerce", dayfirst=True)
        
        return dt
    
    def detect_separator(self, filepath, sample_lines=5):
        """
        Erkennt das CSV-Trennzeichen mit csv.Sniffer (robust).
        Fallback auf manuelle Erkennung bei Fehlschlag.
        """
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                # Lese Sample für Sniffer
                sample = ''.join([f.readline() for _ in range(sample_lines)])
                
                # ✅ V7: Nutze csv.Sniffer (robuster als Zählen)
                try:
                    sniffer = csv.Sniffer()
                    dialect = sniffer.sniff(sample, delimiters=',;')
                    return dialect.delimiter
                except:
                    # Fallback: manuelle Erkennung
                    comma_count = sample.count(',')
                    semicolon_count = sample.count(';')
                    
                    if semicolon_count > comma_count:
                        return ';'
                    else:
                        return ','
        except:
            return ','  # Default fallback
    
    def read_csv_robust(self, filepath):
        """Liest CSV robust ein - handelt Encoding, Trennzeichen, BOM, etc."""
        try:
            # Erkenne Trennzeichen mit Sniffer
            detected_sep = self.detect_separator(filepath)
            
            # Robustes Einlesen mit erkanntem Separator
            df = pd.read_csv(
                filepath,
                sep=detected_sep,
                engine="python",
                encoding="utf-8-sig",
                dtype=str,
                keep_default_na=True
            )
            
            # Speichere für Output
            self.detected_separator = detected_sep
            
            # Spaltennamen normalisieren
            df.columns = (
                df.columns
                .astype(str)
                .str.replace("\ufeff", "", regex=False)
                .str.strip()
            )
            
            # Einheitliche Spaltennamen
            rename_map = {
                " ID": "ID",
                "ID": "ID",
                " Datum": "Datum",
                "Datum": "Datum",
                "Uni-Mail": "Uni-Mail",
                " Uni-Mail": "Uni-Mail",
                "Vollständiger Name": "Vollständiger Name",
                " Vollständiger Name": "Vollständiger Name",
                "Bitte Begleitung eintragen": "Bitte Begleitung eintragen",
                " Bitte Begleitung eintragen": "Bitte Begleitung eintragen",
            }
            
            existing_renames = {k: v for k, v in rename_map.items() if k in df.columns}
            if existing_renames:
                df = df.rename(columns=existing_renames)
            
            return df
            
        except Exception as e:
            raise Exception(f"Fehler beim Einlesen der CSV: {str(e)}")
    
    def compare_dates_or_ids(self, date1, date2, id1, id2):
        """
        Vergleicht zwei Einträge nach Datum, mit ID als Fallback.
        Returns: True wenn date1/id1 SPÄTER ist als date2/id2
        """
        if pd.notna(date1) and pd.notna(date2):
            return date1 > date2
        
        if pd.isna(date1) and pd.notna(date2):
            return True
        
        if pd.notna(date1) and pd.isna(date2):
            return False
        
        # Beide NaT: Fallback auf ID
        try:
            id1_num = int(str(id1).strip())
            id2_num = int(str(id2).strip())
            return id1_num > id2_num
        except:
            return str(id1) > str(id2)
    
    def find_begleitungs_duplikate(self, df):
        """
        Findet Personen, die sich selbst angemeldet haben UND als Begleitung eingetragen sind.
        Nimmt das FRÜHESTE Match als Referenz.
        Robust gegen mehrere Namen im Begleitungsfeld.
        """
        zu_entfernen = []
        details = []
        
        df_work = df.copy()
        
        df_work['_name_norm'] = df_work['Vollständiger Name'].apply(self.normalize_text)
        df_work['_datum_parsed'] = df_work['Datum'].apply(self.parse_datetime)
        df_work['_id_num'] = pd.to_numeric(df_work['ID'], errors='coerce').fillna(10**18)
        
        # Extrahiere Namen aus Begleitungsfeld (kann mehrere enthalten)
        df_work['_begleitung_names'] = df_work['Bitte Begleitung eintragen'].apply(
            self.extract_names_from_begleitung
        )
        
        for idx, row in df_work.iterrows():
            person_name = row['_name_norm']
            
            if not person_name:
                continue
            
            # Suche, ob dieser Name in irgendeinem Begleitungsfeld vorkommt
            matches = df_work[
                (df_work['_begleitung_names'].apply(lambda names: person_name in names)) & 
                (df_work.index != idx)
            ]
            
            if len(matches) > 0:
                # Nimm das FRÜHESTE Match
                matches_sorted = matches.sort_values(
                    ['_datum_parsed', '_id_num'], 
                    ascending=[True, True],
                    na_position='last'
                )
                match_row = matches_sorted.iloc[0]
                
                person_date = row['_datum_parsed']
                match_date = match_row['_datum_parsed']
                person_id = row['ID']
                match_id = match_row['ID']
                
                if self.compare_dates_or_ids(person_date, match_date, person_id, match_id):
                    if idx not in zu_entfernen:
                        zu_entfernen.append(idx)
                        
                        if pd.notna(person_date):
                            datum_info = f"angemeldet am {row['Datum']}"
                        else:
                            datum_info = f"angemeldet ohne Datum (ID: {person_id})"
                        
                        if pd.notna(match_date):
                            match_datum_info = f"am {match_row['Datum']}"
                        else:
                            match_datum_info = f"ohne Datum (ID: {match_id})"
                        
                        details.append({
                            'modus': 'begleitung',  # ✅ V7: modus-Spalte
                            'entfernt_id': person_id,
                            'entfernt_name': row['Vollständiger Name'],
                            'entfernt_email': row['Uni-Mail'],
                            'entfernt_datum': row['Datum'],
                            'grund': f"Hat sich selbst angemeldet ({datum_info}), ist aber bereits als Begleitung von {match_row['Vollständiger Name']} (ID: {match_id}, {match_datum_info}) eingetragen",
                            'behalten_id': match_id,
                            'behalten_name': match_row['Vollständiger Name']
                        })
        
        return zu_entfernen, details
    
    def find_personen_duplikate(self, df):
        """
        Findet doppelte Anmeldungen derselben Person.
        PRIMÄR: Gleicher Name = gleiche Person (wichtig für Mediball)
        SEKUNDÄR: Auch gleiche Email prüfen (zusätzlich, wenn aktiviert)
        """
        zu_entfernen = []
        details = []
        
        df_work = df.copy()
        
        df_work['_name_norm'] = df_work['Vollständiger Name'].apply(self.normalize_text)
        df_work['_email_norm'] = df_work['Uni-Mail'].apply(self.normalize_text)
        df_work['_datum_parsed'] = df_work['Datum'].apply(self.parse_datetime)
        df_work['_id_num'] = pd.to_numeric(df_work['ID'], errors='coerce').fillna(10**18)
        
        # === PRIMÄR: Name-basierte Duplikate (WICHTIG für Mediball) ===
        for name, group in df_work[df_work['_name_norm'] != ''].groupby('_name_norm'):
            if len(group) > 1:
                # Sortiere mit numerischer ID
                group_sorted = group.sort_values(
                    ['_datum_parsed', '_id_num'],
                    ascending=[True, True],
                    na_position='last'
                )
                
                erste_anmeldung = group_sorted.iloc[0]
                duplikate = group_sorted.iloc[1:]
                
                for idx, dup_row in duplikate.iterrows():
                    if idx not in zu_entfernen:
                        zu_entfernen.append(idx)
                        
                        # Datum-Info
                        if pd.notna(dup_row['_datum_parsed']):
                            dup_datum_info = dup_row['Datum']
                        else:
                            dup_datum_info = f"ohne Datum (ID: {dup_row['ID']})"
                        
                        if pd.notna(erste_anmeldung['_datum_parsed']):
                            erste_datum_info = erste_anmeldung['Datum']
                        else:
                            erste_datum_info = f"ohne Datum (ID: {erste_anmeldung['ID']})"
                        
                        # Prüfe ob Emails unterschiedlich sind
                        email_unterschiedlich = (
                            (dup_row['_email_norm'] != erste_anmeldung['_email_norm']) and 
                            (dup_row['_email_norm'] != '') and 
                            (erste_anmeldung['_email_norm'] != '')
                        )
                        
                        if email_unterschiedlich:
                            email_hinweis = f" ⚠️ ACHTUNG: Unterschiedliche Emails ({dup_row['Uni-Mail']} vs {erste_anmeldung['Uni-Mail']})"
                        else:
                            email_hinweis = ""
                        
                        details.append({
                            'modus': 'person_name',  # ✅ V7: modus-Spalte
                            'entfernt_id': dup_row['ID'],
                            'entfernt_name': dup_row['Vollständiger Name'],
                            'entfernt_email': dup_row['Uni-Mail'],
                            'entfernt_datum': dup_row['Datum'],
                            'grund': f"Doppelte Anmeldung (gleicher Name). Angemeldet am {dup_datum_info}. Erste Anmeldung war am {erste_datum_info} (ID: {erste_anmeldung['ID']}){email_hinweis}",
                            'behalten_id': erste_anmeldung['ID'],
                            'behalten_name': erste_anmeldung['Vollständiger Name'],
                            'behalten_email': erste_anmeldung['Uni-Mail']
                        })
        
        # === SEKUNDÄR: Email-basierte Duplikate (nur wenn noch nicht erfasst) ===
        if self.check_email_duplicates.get():
            for email, group in df_work[df_work['_email_norm'] != ''].groupby('_email_norm'):
                if len(group) > 1:
                    group_sorted = group.sort_values(
                        ['_datum_parsed', '_id_num'],
                        ascending=[True, True],
                        na_position='last'
                    )
                    
                    erste_anmeldung = group_sorted.iloc[0]
                    duplikate = group_sorted.iloc[1:]
                    
                    for idx, dup_row in duplikate.iterrows():
                        # Nur hinzufügen, wenn nicht schon via Name erwischt
                        if idx not in zu_entfernen:
                            zu_entfernen.append(idx)
                            
                            if pd.notna(dup_row['_datum_parsed']):
                                dup_datum_info = dup_row['Datum']
                            else:
                                dup_datum_info = f"ohne Datum (ID: {dup_row['ID']})"
                            
                            if pd.notna(erste_anmeldung['_datum_parsed']):
                                erste_datum_info = erste_anmeldung['Datum']
                            else:
                                erste_datum_info = f"ohne Datum (ID: {erste_anmeldung['ID']})"
                            
                            details.append({
                                'modus': 'person_email',  # ✅ V7: modus-Spalte
                                'entfernt_id': dup_row['ID'],
                                'entfernt_name': dup_row['Vollständiger Name'],
                                'entfernt_email': dup_row['Uni-Mail'],
                                'entfernt_datum': dup_row['Datum'],
                                'grund': f"⚠️ Doppelte Anmeldung (gleiche Email, unterschiedlicher Name: '{dup_row['Vollständiger Name']}' vs '{erste_anmeldung['Vollständiger Name']}'). Angemeldet am {dup_datum_info}. Erste Anmeldung war am {erste_datum_info} (ID: {erste_anmeldung['ID']}). Könnte Tippfehler im Namen sein!",
                                'behalten_id': erste_anmeldung['ID'],
                                'behalten_name': erste_anmeldung['Vollständiger Name'],
                                'behalten_email': erste_anmeldung['Uni-Mail']
                            })
        
        return zu_entfernen, details
    
    def find_duplicates(self):
        try:
            self.result_text.delete(1.0, tk.END)
            
            self.log_result("🔄 Lese CSV-Datei ein...\n")
            df = self.read_csv_robust(self.input_file)
            original_count = len(df)
            
            self.log_result(f"✓ CSV-Datei eingelesen: {original_count} Anmeldungen\n")
            self.log_result(f"✓ Eingelesen mit Trennzeichen: '{self.detected_separator}'\n")
            self.log_result(f"\n📋 Erkannte Spalten ({len(df.columns)}):\n")
            for i, col in enumerate(df.columns, 1):
                self.log_result(f"   {i:2d}. '{col}'\n")
            self.log_result(f"\n{'='*85}\n\n")
            
            required_cols = ['Vollständiger Name', 'Uni-Mail', 'Bitte Begleitung eintragen', 'ID', 'Datum']
            missing = [col for col in required_cols if col not in df.columns]
            
            if missing:
                error_msg = f"❌ Fehlende Spalten: {', '.join(missing)}\n\n"
                error_msg += f"Verfügbare Spalten:\n"
                for col in df.columns:
                    error_msg += f"  - '{col}'\n"
                messagebox.showerror("Fehler - Spalten nicht gefunden", error_msg)
                self.log_result(error_msg)
                return
            
            mode = self.search_mode.get()
            alle_zu_entfernen = []
            alle_details = []
            
            # Begleitungs-Duplikate
            if mode in ['begleitung', 'alle']:
                self.log_result("🔍 Prüfe Begleitungs-Duplikate...\n")
                begleitungs_entfernen, begleitungs_details = self.find_begleitungs_duplikate(df)
                alle_zu_entfernen.extend(begleitungs_entfernen)
                alle_details.extend(begleitungs_details)
                
                if begleitungs_details:
                    self.log_result(f"⚠️  {len(begleitungs_details)} Begleitungs-Duplikate gefunden:\n\n")
                    for detail in begleitungs_details:
                        self.log_result(f"   ❌ ENTFERNT: {detail['entfernt_name']} (ID: {detail['entfernt_id']})\n")
                        self.log_result(f"      └─ {detail['grund']}\n\n")
                else:
                    self.log_result("   ✓ Keine Begleitungs-Duplikate gefunden\n\n")
            
            # Personen-Duplikate
            if mode in ['person', 'alle']:
                self.log_result("🔍 Prüfe doppelte Personen (primär: Name)...\n")
                if self.check_email_duplicates.get():
                    self.log_result("   ✓ Email-basierte Duplikate werden zusätzlich geprüft\n")
                personen_entfernen, personen_details = self.find_personen_duplikate(df)
                alle_zu_entfernen.extend(personen_entfernen)
                alle_details.extend(personen_details)
                
                if personen_details:
                    self.log_result(f"⚠️  {len(personen_details)} Personen-Duplikate gefunden:\n\n")
                    for detail in personen_details:
                        self.log_result(f"   ❌ ENTFERNT: {detail['entfernt_name']} (ID: {detail['entfernt_id']})\n")
                        self.log_result(f"      Email: {detail['entfernt_email']}\n")
                        self.log_result(f"      └─ {detail['grund']}\n\n")
                else:
                    self.log_result("   ✓ Keine Personen-Duplikate gefunden\n\n")
            
            # Entferne Duplikate
            alle_zu_entfernen = sorted(list(set(alle_zu_entfernen)))
            df_bereinigt = df.drop(index=alle_zu_entfernen).reset_index(drop=True)
            
            # Statistik
            self.log_result(f"{'='*85}\n")
            self.log_result(f"📊 ZUSAMMENFASSUNG:\n\n")
            self.log_result(f"   Original Anmeldungen:      {original_count}\n")
            self.log_result(f"   Entfernte Duplikate:       {len(alle_zu_entfernen)}\n")
            self.log_result(f"   Bereinigte Anmeldungen:    {len(df_bereinigt)}\n")
            self.log_result(f"   {'─'*40}\n")
            self.log_result(f"   Verfügbare Ticketplätze:   {len(df_bereinigt)} 🎫\n")
            
            # Bestimme Output-Separator
            if self.output_sep.get() == "auto":
                output_sep = self.detected_separator
            else:
                output_sep = self.output_sep.get()
            
            # Speichern
            df_bereinigt.to_csv(self.output_file, index=False, encoding='utf-8-sig', sep=output_sep)
            self.log_result(f"\n✅ Bereinigte Datei gespeichert: {Path(self.output_file).name}\n")
            self.log_result(f"   Trennzeichen: '{output_sep}'\n")
            
            # Optional: Report mit modus-Spalte
            if self.save_report.get() and alle_details:
                report_file = str(Path(self.output_file).parent / (Path(self.output_file).stem + "_entfernte_duplikate.csv"))
                
                # ✅ V7: Sortiere Report nach modus für bessere Übersicht
                df_report = pd.DataFrame(alle_details)
                # Spalten-Reihenfolge: modus zuerst
                cols = ['modus'] + [col for col in df_report.columns if col != 'modus']
                df_report = df_report[cols]
                
                df_report.to_csv(report_file, index=False, encoding='utf-8-sig', sep=output_sep)
                self.log_result(f"📄 Duplikate-Report gespeichert: {Path(report_file).name}\n")
                self.log_result(f"   (Spalte 'modus' zeigt Duplikat-Typ: begleitung/person_name/person_email)\n")
            
            messagebox.showinfo("Erfolg! 🎉", 
                f"Duplikat-Filterung abgeschlossen!\n\n"
                f"Original: {original_count} Anmeldungen\n"
                f"Entfernt: {len(alle_zu_entfernen)} Duplikate\n"
                f"Bereinigt: {len(df_bereinigt)} gültige Anmeldungen\n\n"
                f"Gleicher Name = gleiche Person (primär).\n"
                f"(Bei fehlendem Datum wurde die niedrigere ID bevorzugt)")
            
        except Exception as e:
            error_detail = traceback.format_exc()
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n\n{str(e)}")
            self.log_result(f"\n❌ FEHLER: {str(e)}\n\n")
            self.log_result(f"Details:\n{error_detail}\n")
    
    def log_result(self, message):
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
        self.root.update()

def main():
    root = tk.Tk()
    app = MediballDuplicateFinder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
