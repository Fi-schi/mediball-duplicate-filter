import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pathlib import Path
import traceback
import re
import csv

__version__ = "2.0.2"  # V2.0.2 - Feature: Email-Korrektur statt Löschung (Warteplatz-Erhaltung)

class MediballDuplicateFinder:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Mediball CSV Duplikat-Filter v{__version__}")
        self.root.geometry("850x700")
        self.root.resizable(True, True)
        
        self.input_file = None
        self.output_file = None
        self.detected_separator = ","
        
        # V7.2: Akademische Titel für Entfernung
        self.titles_to_remove = [
            'dr', 'dr.', 'prof', 'prof.', 'professor',
            'med', 'med.', 'cand', 'cand.', 'dipl', 'dipl.',
            'ing', 'ing.', 'phd', 'ph.d.',
            'msc', 'm.sc.', 'bsc', 'b.sc.',
            'ba', 'b.a.', 'ma', 'm.a.'
        ]
        
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
        
        # ✅ V2.0.2 NEU: Email-Typo-Korrektur
        self.correct_email_typos_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, 
                       text="📧 Email-Typos automatisch korrigieren (empfohlen)", 
                       variable=self.correct_email_typos_var).grid(row=5, column=1, sticky=tk.W, padx=20, pady=5)
        
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
        
        info_text = ("ℹ️  V2.0.2 - Email-Korrektur + Hybrid Domain:\n"
                    "   📧 Email-Typo-Korrektur (NEU)\n"
                    "   ✓ Pattern-Check (Subdomains, TLD-Typos)\n"
                    "   ✓ Known-Domains (uni-rostock.de, gmail.com, etc.)\n"
                    "   📊 Domain-Learning (häufige Domains aus CSV)\n"
                    "   🎓 Uni-Mail-Priorität\n"
                    "   ⚡ Production-Ready")
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
    
    
    
    def is_uni_email(self, email):
        """
        V7.2: Prüft ob eine Email eine Universitäts-Email ist
        
        Uni-Domains:
        - uni- am Anfang (z.B. uni-rostock.de)
        - .uni. im Domain
        - .edu Domain
        - .ac.uk, .ac.at, .ac.de Domains
        """
        if not email or '@' not in email:
            return False
        
        parts = email.split('@')
        if len(parts) != 2 or not parts[1]:
            return False
        
        domain = parts[1]
        return (
            domain.startswith('uni-') or 
            '.uni.' in domain or
            domain.endswith('.edu') or 
            domain.endswith('.ac.uk') or
            domain.endswith('.ac.at') or
            domain.endswith('.ac.de')
        )
    
    def clean_email(self, email, learned_domains=[]):
        """
        V7.8: Erweiterte Email-Säuberung mit Hybrid Domain-Korrektur
        - Entfernt mailto:, MAILTO: Präfixe
        - Entfernt alle Whitespace (Leerzeichen, Tabs, Newlines, etc.)
        - Nimmt erste Email bei mehreren (getrennt durch ; oder ,)
        - Entfernt umschließende Zeichen wie < > " ' ( )
        - Validiert Email-Format (muss @ enthalten)
        - ✅ V7.8 NEU: Hybrid Domain-Korrektur (3-Stufen: Pattern + Known + Learning)
        - Lowercase
        
        Beispiele:
        - MAILTO:max@uni.de → max@uni.de
        - max@uni.de;max@gmail.com → max@uni.de
        - <max@uni.de> → max@uni.de
        - "max@uni.de" → max@uni.de
        - max @uni. de → max@uni.de
        - max\t@uni.de\n → max@uni.de
        - max@studnet.uni-rostock.de → max@student.uni-rostock.de ✅ V7.8
        - max@web.dee → max@web.de ✅ V7.8
        """
        if pd.isna(email) or email is None:
            return ""
        
        email = str(email).strip()
        
        # Entferne mailto: oder MAILTO:
        email = re.sub(r'^mailto:', '', email, flags=re.IGNORECASE)
        
        # V7.6: Entferne umschließende Zeichen wie < > " ' ( )
        email = email.strip('<>"\'()')
        
        # V7.6: Entferne alle Whitespace-Zeichen (Leerzeichen, Tabs, Newlines, etc.)
        email = re.sub(r'\s+', '', email)
        
        # Bei mehreren Emails (getrennt durch ; oder ,), nimm die erste
        if ';' in email or ',' in email:
            email = re.split(r'[;,]', email, maxsplit=1)[0]  # ✅ V7.5 FIX: Split bei ; UND ,
        
        # V7.6: Entferne trailing/leading punctuation nach Split (z.B. "max@uni.de." oder "max@uni.de)")
        email = email.strip('()[]{}<>.,;:')
        
        # Lowercase
        email = email.lower()
        
        # V7.6: Validiere Email-Format - muss @ enthalten und mindestens ein Zeichen davor und danach
        if not email or '@' not in email:
            return ""
        
        # V7.6: Einfache Validierung - min. 1 Zeichen vor @, min. 2 nach @ (für x@a.b)
        parts = email.split('@')
        if len(parts) != 2 or not parts[0] or len(parts[1]) < 3 or '.' not in parts[1]:
            return ""
        
        # ✅ V7.8: Hybrid Domain-Korrektur (3-Stufen)
        email = self.suggest_domain_correction(email, learned_domains)
        
        return email
    
    def _check_uni_rostock_subdomains(self, domain):
        """
        ✅ V7.8: Erkennt Typos in Uni-Rostock-Subdomains.
        
        Beispiele:
        - studnet.uni-rostock.de → student.uni-rostock.de
        - studennt.uni-rostock.de → student.uni-rostock.de
        - studnets.uni-rostock.de → students.uni-rostock.de
        """
        if 'uni-rostock.de' not in domain:
            return domain
        
        known_subdomains = [
            'student.uni-rostock.de',
            'students.uni-rostock.de',
            'uni-rostock.de',
            'mail.uni-rostock.de',
            'webmail.uni-rostock.de'
        ]
        
        for correct in known_subdomains:
            dist = self.levenshtein_distance(domain.lower(), correct)
            if 0 < dist <= 2:
                self.log_result(f"   📧 Subdomain-Korrektur: {domain} → {correct}\n")
                return correct
        
        return domain
    
    def _check_tld_typos(self, domain):
        """
        ✅ V7.8: Erkennt Tippfehler in TLDs (.de, .com, .net, etc.)
        
        Beispiele:
        - web.dee → web.de
        - gmail.comm → gmail.com
        - yahoo.nett → yahoo.net
        """
        tld_corrections = {
            'dee': 'de',
            'dde': 'de',
            'ed': 'de',
            'comm': 'com',
            'ccom': 'com',
            'ocm': 'com',
            'con': 'com',
            'nett': 'net',
            'nte': 'net',
            'orgg': 'org',
            'ogr': 'org',
            'edu': 'edu',  # Bleibt
            'co.uk': 'co.uk'  # Bleibt
        }
        
        parts = domain.split('.')
        if len(parts) < 2:
            return domain
        
        tld = parts[-1].lower()
        
        if tld in tld_corrections:
            correct_tld = tld_corrections[tld]
            corrected = '.'.join(parts[:-1]) + '.' + correct_tld
            if corrected != domain:
                self.log_result(f"   📧 TLD-Korrektur: {domain} → {corrected}\n")
                return corrected
        
        return domain
    
    def _check_known_domains(self, domain):
        """
        ✅ V7.8: Prüft gegen vordefinierte Liste bekannter Domains.
        
        Wie in V7.7, aber als separate Methode für Hybrid-Ansatz.
        """
        known_domains = [
            'uni-rostock.de',
            'student.uni-rostock.de',
            'students.uni-rostock.de',
            'gmail.com',
            'googlemail.com',
            'web.de',
            'gmx.de',
            'gmx.net',
            'outlook.com',
            'hotmail.com',
            'yahoo.com',
            'yahoo.de',
            't-online.de',
            'freenet.de',
            'posteo.de'
        ]
        
        for correct in known_domains:
            dist = self.levenshtein_distance(domain.lower(), correct)
            if 0 < dist <= 2:
                self.log_result(f"   📧 Known-Domain-Korrektur: {domain} → {correct}\n")
                return correct
        
        return domain
    
    def _check_learned_domains(self, domain, learned_domains):
        """
        ✅ V7.8: Prüft Domain gegen aus CSV gelernte häufige Domains.
        
        Nur wenn Distance ≤ 2 und gelernte Domain mindestens 3x vorkommt.
        """
        if not learned_domains:
            return domain
        
        for correct in learned_domains:
            dist = self.levenshtein_distance(domain.lower(), correct)
            if 0 < dist <= 2:
                self.log_result(f"   📊 Learned-Domain-Korrektur: {domain} → {correct}\n")
                return correct
        
        return domain
    
    def analyze_domain_frequencies(self, df):
        """
        ✅ V7.8: Analysiert alle Domains in CSV und findet häufige.
        
        Returns: Liste von Domains die mindestens 3x vorkommen
        """
        from collections import Counter
        
        domains = []
        for email in df['_email_clean'].dropna():
            if '@' in str(email):
                domain = str(email).split('@')[-1].lower()
                if domain and len(domain) > 3:  # Mindestlänge
                    domains.append(domain)
        
        # Zähle Häufigkeiten
        domain_counts = Counter(domains)
        
        # Nur Domains die mindestens 3x vorkommen
        learned_domains = [d for d, count in domain_counts.items() if count >= 3]
        
        if learned_domains:
            self.log_result(f"📊 {len(learned_domains)} häufige Domain(s) gefunden: {', '.join(learned_domains[:5])}\n")
            if len(learned_domains) > 5:
                self.log_result(f"   ... und {len(learned_domains)-5} weitere\n")
        
        return learned_domains
    
    def suggest_domain_correction(self, email, learned_domains=[]):
        """
        ✅ V7.8: 3-Stufen Hybrid Domain-Korrektur
        
        Stufe 1: Pattern-Check (Subdomains, TLD-Typos)
        Stufe 2: Known-Domains-Check
        Stufe 3: Learned-Domains-Check (aus CSV)
        
        Beispiele:
        - studnet.uni-rostock.de → student.uni-rostock.de (Pattern)
        - web.dee → web.de (TLD)
        - uni-rostok.de → uni-rostock.de (Known)
        - rare-company.dee → rare-company.de (TLD + Learning)
        """
        if '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        original_domain = domain
        
        # Stufe 1: Pattern-Check
        # 1a) Uni-Rostock Subdomains
        domain = self._check_uni_rostock_subdomains(domain)
        if domain != original_domain:
            return f"{local}@{domain}"
        
        # 1b) TLD-Typos
        domain = self._check_tld_typos(domain)
        if domain != original_domain:
            return f"{local}@{domain}"
        
        # Stufe 2: Known-Domains
        domain = self._check_known_domains(domain)
        if domain != original_domain:
            return f"{local}@{domain}"
        
        # Stufe 3: Learned-Domains
        domain = self._check_learned_domains(domain, learned_domains)
        if domain != original_domain:
            return f"{local}@{domain}"
        
        return email
    
    def remove_titles(self, text):
        """
        V7.2: Entfernt akademische Titel aus Namen
        
        Beispiele:
        - Dr. Max Mustermann → Max Mustermann
        - Prof. Dr. med. Lisa Musterfrau → Lisa Musterfrau
        """
        if pd.isna(text) or text is None:
            return text
        
        text = str(text).strip()
        
        # Splitte in Wörter
        words = text.split()
        
        # Entferne alle Titel (case-insensitive)
        filtered_words = [
            word for word in words 
            if word.lower() not in self.titles_to_remove
        ]
        
        return ' '.join(filtered_words)
    
    def normalize_apostrophes(self, text):
        """
        V7.2: Normalisiert verschiedene Apostroph-Varianten zu Standard-Apostroph
        
        Beispiele:
        - O'Connor (typografisch U+2019) → O'Connor (standard U+0027)
        
        Apostroph-Varianten:
        - U+2019 (RIGHT SINGLE QUOTATION MARK) '
        - U+2018 (LEFT SINGLE QUOTATION MARK) '
        - U+02BC (MODIFIER LETTER APOSTROPHE) ʼ
        - U+0060 (GRAVE ACCENT) `
        - U+00B4 (ACUTE ACCENT) ´
        """
        if pd.isna(text) or text is None:
            return text
        
        text = str(text)
        
        # Ersetze alle Apostroph-Varianten durch Standard-Apostroph
        apostrophe_variants = [
            '\u2019',  # RIGHT SINGLE QUOTATION MARK
            '\u2018',  # LEFT SINGLE QUOTATION MARK
            '\u02BC',  # MODIFIER LETTER APOSTROPHE
            '\u0060',  # GRAVE ACCENT
            '\u00B4',  # ACUTE ACCENT
        ]
        
        for variant in apostrophe_variants:
            text = text.replace(variant, "'")
        
        return text
    
    def flip_lastname_firstname(self, name):
        """
        V7.2: Erkennt "Nachname, Vorname" Format und dreht es um zu "Vorname Nachname"
        
        Beispiele:
        - "Mustermann, Max" → "Max Mustermann"
        - "Meyer-Lüdenscheidt, Lisa Maria" → "Lisa Maria Meyer-Lüdenscheidt"
        
        Sicherheits-Checks:
        - Nur bei genau 1 Komma
        - Max 3 Wörter pro Teil
        - Beide Teile nicht-leer
        """
        if pd.isna(name) or name is None:
            return name
        
        name = str(name).strip()
        
        # Prüfe ob genau 1 Komma vorhanden
        if name.count(',') != 1:
            return name
        
        parts = name.split(',')
        if len(parts) != 2:
            return name
        
        nachname = parts[0].strip()
        vorname = parts[1].strip()
        
        # Sicherheits-Checks
        if not nachname or not vorname:
            return name
        
        # Max 3 Wörter pro Teil (Sicherheitscheck)
        if len(nachname.split()) > 3 or len(vorname.split()) > 3:
            return name
        
        # Drehe um
        return f"{vorname} {nachname}"
    
    def normalize_text(self, text):
        """
        Normalisiert Text für Vergleich
        V7.2: Erweitert mit Titel-Entfernung, Apostroph-Normalisierung, 
              Nachname/Vorname-Erkennung und Bindestrich-Normalisierung
        V7.9: Sonderzeichen-Filter für Distance-Berechnung
        """
        if pd.isna(text) or text is None:
            return ""
        text = str(text).strip()
        
        # ✅ V7.5 FIX: Non-Breaking Space → normales Space
        text = text.replace('\u00A0', ' ')
        
        # V7.2: Apostroph-Normalisierung (VOR allem anderen)
        text = self.normalize_apostrophes(text)
        
        # V7.2: Erkenne "Nachname, Vorname" und drehe um
        text = self.flip_lastname_firstname(text)
        
        # V7.2: Entferne akademische Titel
        text = self.remove_titles(text)
        
        # ✅ V7.9: Sonderzeichen für Vergleich entfernen
        # (Original bleibt für Anzeige erhalten)
        text = self.clean_name_for_comparison(text)
        
        # ✅ V7: Entferne mehrfache Leerzeichen
        text = re.sub(r'\s+', ' ', text)
        
        # V7.2: Bindestrich = Leerzeichen (für Namen wie "Meyer-Lüdenscheidt")
        text = text.replace('-', ' ')
        
        # ✅ V7.1: Normalisiere deutsche Umlaute für bessere Duplikat-Erkennung
        # Behandelt Fälle wie "Schröder" vs "Schroeder" oder "Meyer" vs "Meier"
        # WICHTIG: Umlaut-Normalisierung VOR Lowercase-Konvertierung!
        umlaut_map = {
            'Ä': 'Ae',
            'Ö': 'Oe',
            'Ü': 'Ue',
            'ä': 'ae',
            'ö': 'oe',
            'ü': 'ue',
            'ß': 'ss'
        }
        for umlaut, replacement in umlaut_map.items():
            text = text.replace(umlaut, replacement)
        
        if not self.case_sensitive.get():
            text = text.lower()
        
        # V7.2: Entferne mehrfache Leerzeichen nochmal nach allen Transformationen
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_name_from_email(self, email):
        """
        Extrahiert den Namen aus dem Local-Part einer Email.
        
        Beispiel (anonymisiert):
            max.mustermann@uni.de → max mustermann
            m.mustermann@uni.de   → m mustermann
        
        Args:
            email (str): Email-Adresse
            
        Returns:
            str: Normalisierter Name aus Email (lowercase, ohne Sonderzeichen)
        """
        if not email or '@' not in email:
            return ""
        
        local_part = email.split('@')[0]
        
        # Ersetze Trennzeichen durch Leerzeichen
        name = local_part.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        
        # Normalisiere (gleiche Logik wie normalize_text)
        return self.normalize_text(name)
    
    def phonetic_key(self, text):
        """
        ✅ V7.7: Einfacher Soundex-ähnlicher Key für deutsche Namen
        
        Erstellt einen phonetischen Schlüssel zur Erkennung ähnlich klingender Namen.
        Dies wird NUR für Verdachtsfälle verwendet, NICHT für automatisches Löschen!
        
        Beispiele:
        - "Meyer" → "MYR"
        - "Meier" → "MR"
        - "Möller" → "MLR"
        - "Schmidt" → "SCHMT"
        - "Schmitt" → "SCHMT"
        
        Args:
            text: Der zu konvertierende Text (normalerweise ein Name)
        
        Returns:
            str: Phonetischer Schlüssel (Großbuchstaben ohne Vokale und Doppelkonsonanten)
        """
        if not text:
            return ""
        
        # Nutze bestehende Normalisierung (Umlaute werden bereits normalisiert)
        text = self.normalize_text(text)
        
        # Entferne Vokale (außer am Anfang)
        if len(text) > 1:
            first = text[0]
            rest = ''.join([c for c in text[1:] if c not in 'aeiou'])
            text = first + rest
        
        # Entferne Doppelkonsonanten
        text = re.sub(r'(.)\1+', r'\1', text)
        
        return text.upper()
    
    def extract_names_from_begleitung(self, text):
        """
        V7.6: Extrahiert Namen aus Begleitungsfeld mit verbesserter Komma-Erkennung
        Splittet bei Komma, Semikolon, "und", "&", Zeilenumbrüche.
        Nutzt flip_lastname_firstname() für "Nachname, Vorname" Erkennung
        
        V7.6 NEU: Heuristik für Komma-Listen wie "Max Mustermann, Maria Musterfrau"
        - Wenn ein Segment MEHRERE Wörter VOR dem Komma hat → wahrscheinlich Komma-Liste
        - Wenn ein Segment nur 1-2 Wörter hat → wahrscheinlich "Nachname, Vorname"
        
        Beispiele:
        - "Mustermann, Max" → ["Max Mustermann"] (1 Wort vor Komma → gedreht)
        - "Max Mustermann, Maria Musterfrau" → ["Max Mustermann", "Maria Musterfrau"] (2 Wörter vor Komma → Liste)
        - "Mustermann, Max; Meyer, Lisa" → ["Max Mustermann", "Lisa Meyer"]
        - "Dr. Max (Begleitung)" → ["Max"]
        
        Returns: Liste normalisierter Namen
        """
        if pd.isna(text) or text is None:
            return []
        
        text = str(text).strip()
        
        # V7.6: Erst prüfen ob Komma-Liste (multiple Vollnamen) oder "Nachname, Vorname"
        # Heuristik: Splitte temporär bei Komma und schaue auf Struktur
        if ',' in text:
            # Prüfe ob es eine Komma-Liste von Vollnamen sein könnte
            comma_parts = text.split(',')
            # Wenn es 2+ Teile gibt und der erste Teil 2+ Wörter hat → wahrscheinlich Liste
            if len(comma_parts) >= 2:
                first_part_words = len(comma_parts[0].strip().split())
                # Wenn >= 2 Wörter vor dem Komma → wahrscheinlich Vollname-Liste
                if first_part_words >= 2:
                    # V7.6: Behandle als Komma-Liste, splitte bei Komma
                    text = text.replace(',', ';')  # Ersetze Komma durch Semikolon für einheitliche Behandlung
        
        # Splitte bei gängigen Trennern
        # Trenne bei: ; & "und" "Und" Zeilenumbruch / + | (und jetzt auch Komma wenn als Liste erkannt)
        # \b für Wortgrenzen um "und" auch am Anfang/Ende zu matchen
        parts = re.split(r'[;&\n/+|]|\bund\b', text, flags=re.IGNORECASE)  # ✅ V7.5 FIX: Mehr Trenner
        
        # Normalisiere jeden Teil
        names = []
        for part in parts:
            part_clean = part.strip()
            # Entferne Klammer-Inhalte wie "(Begleitung)"
            part_clean = re.sub(r'\([^)]*\)', '', part_clean).strip()
            
            if part_clean:
                # Normalisiere wie andere Namen (nutzt intern flip_lastname_firstname)
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
    
    def levenshtein_distance(self, s1, s2):
        """
        ✅ V7.5: Berechnet Levenshtein-Distance zwischen zwei Strings.
        
        Die Levenshtein-Distance ist die minimale Anzahl von Einfüge-, 
        Lösch- und Ersetzungsoperationen, um einen String in den anderen zu transformieren.
        
        Beispiele:
        - "Mustermann" vs "Musterman" → Distance 1 (1 Buchstabe gelöscht)
        - "Meyer" vs "Meier" → Distance 1 (nach Normalisierung)
        
        Args:
            s1: Erster String
            s2: Zweiter String
        
        Returns:
            int: Levenshtein-Distance
        """
        if s1 == s2:
            return 0
        
        len1, len2 = len(s1), len(s2)
        
        # Optimierung: Wenn einer leer ist
        if len1 == 0:
            return len2
        if len2 == 0:
            return len1
        
        # Matrix für Dynamic Programming
        # Verwende nur zwei Zeilen statt der vollen Matrix (Speicheroptimierung)
        previous_row = list(range(len2 + 1))
        current_row = [0] * (len2 + 1)
        
        for i in range(1, len1 + 1):
            current_row[0] = i
            
            for j in range(1, len2 + 1):
                # Kosten für Ersetzung
                cost = 0 if s1[i-1] == s2[j-1] else 1
                
                current_row[j] = min(
                    previous_row[j] + 1,      # Löschung
                    current_row[j-1] + 1,      # Einfügung
                    previous_row[j-1] + cost   # Ersetzung
                )
            
            # Tausche Zeilen
            previous_row, current_row = current_row, previous_row
        
        return previous_row[len2]
    
    def clean_name_for_comparison(self, name):
        """
        ✅ V7.9: Entfernt Sonderzeichen für Distance-Berechnung
        
        Erlaubt nur:
        - Buchstaben (a-z, A-Z, Umlaute)
        - Leerzeichen
        - Apostroph (für O'Connor)
        - Bindestrich (für Meyer-Müller)
        
        🔒 Beispiele (ANONYMISIERT):
        - "Max!!! Mustermann" → "Max Mustermann"
        - "Max 😊 Mustermann" → "Max Mustermann"
        - "Max (Extern)" → "Max Extern"
        
        WICHTIG: Nur für Vergleich, nicht für Anzeige!
        """
        if pd.isna(name) or name is None:
            return ""
        
        name = str(name).strip()
        
        # Erlaubte Zeichen: Buchstaben, Space, Apostroph, Bindestrich
        # Umlaute explizit erlauben
        cleaned = re.sub(r"[^a-zA-ZäöüÄÖÜßáéíóúàèìòùâêîôû\s'\-]", "", name)
        
        # Mehrfache Leerzeichen normalisieren
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip()
    
    def get_email_comparison_reason(self, email1, email2):
        """
        ✅ V7.9: Unterscheidet zwischen Typo und Variante
        
        Returns:
        - "Typo erkannt" (Distance 1-2, ähnliche Länge)
        - "Email-Variante (beide valide)" (beide valide, z.B. max@ vs m@)
        - "Unterschiedliche Emails" (Distance > 2)
        
        🔒 Beispiele (ANONYMISIERT):
        - max.mustermann@ vs max.musermann@ → "Typo erkannt"
        - max.mustermann@ vs m.mustermann@ → "Email-Variante (beide valide)"
        """
        if '@' not in email1 or '@' not in email2:
            return "Unterschiedliche Emails"
        
        local1, domain1 = email1.split('@', 1)
        local2, domain2 = email2.split('@', 1)
        
        if domain1 != domain2:
            return "Unterschiedliche Domains"
        
        dist = self.levenshtein_distance(local1, local2)
        
        if dist == 0:
            return "Identische Emails"
        elif dist <= 2:
            # Prüfe ob es eine Abkürzung/Variante sein könnte
            # Heuristik 1: Prüfe ob die kürzere Email eine Abkürzungsform sein könnte
            # z.B. "max.mustermann" vs "m.mustermann" → eine Komponente ist verkürzt
            parts1 = local1.split('.')
            parts2 = local2.split('.')
            
            # Wenn gleiche Anzahl Teile und ein Teil ist deutlich kürzer → wahrscheinlich Abkürzung
            if len(parts1) == len(parts2):
                for p1, p2 in zip(parts1, parts2):
                    if len(p1) > 2 and len(p2) > 0 and len(p2) <= 2 and p2[0] == p1[0]:
                        # Ein Teil ist auf Initial gekürzt (z.B. max → m)
                        return "Email-Variante (beide valide)"
                    elif len(p2) > 2 and len(p1) > 0 and len(p1) <= 2 and p1[0] == p2[0]:
                        # Umgekehrt
                        return "Email-Variante (beide valide)"
            
            # Heuristik 2: Große Längendifferenz → eine ist Kurzform
            len_diff = abs(len(local1) - len(local2))
            if len_diff > 3:
                return "Email-Variante (beide valide)"
            
            # Ähnliche Länge, kleine Distance → wahrscheinlich Typo
            return "Typo erkannt"
        else:
            return "Unterschiedliche Emails"
    
    def email_matches_name_better(self, email1, email2, name_normalized):
        """
        ✅ V7.7: Prüft welche Email besser zum Namen passt (Typo-Erkennung)
        
        Vergleicht zwei Email-Adressen und prüft, welche besser zum normalisierten Namen passt.
        Nutzt Levenshtein-Distance um Tippfehler zu erkennen.
        
        V7.6: Nur Distance 0 vs >0 wurde erkannt
        V7.7: Jetzt auch Distance 1 vs 2+ wird erkannt!
        
        Beispiele:
        - Name: "Mustermann", Email1: "musterman@uni.de" (Distance 1), Email2: "mustermn@uni.de" (Distance 2)
          → Gibt 1 zurück (email1 ist besser)
        - Name: "Schmidt", Email1: "schmitt@uni.de" (Distance 1), Email2: "schmidt@uni.de" (Distance 0)
          → Gibt 2 zurück (email2 ist perfekt)
        
        Args:
            email1: Erste Email-Adresse
            email2: Zweite Email-Adresse
            name_normalized: Normalisierter Name für Vergleich
        
        Returns:
            int: 1 wenn email1 besser ist, 2 wenn email2 besser ist, 0 wenn unklar
        """
        if not email1 or not email2 or not name_normalized or '@' not in email1 or '@' not in email2:
            return 0
        
        # Extrahiere lokalen Teil (vor @)
        local1 = email1.split('@')[0].lower()
        local2 = email2.split('@')[0].lower()
        
        # Entferne Punkt und Underscore aus lokalem Teil für Vergleich
        local1_clean = local1.replace('.', '').replace('_', '')
        local2_clean = local2.replace('.', '').replace('_', '')
        
        # Normalisiere Namen (entferne Leerzeichen für Email-Vergleich)
        name_for_email = name_normalized.lower().replace(' ', '')
        
        # Berechne Levenshtein-Distance
        dist1 = self.levenshtein_distance(local1_clean, name_for_email)
        dist2 = self.levenshtein_distance(local2_clean, name_for_email)
        
        # Perfekter Match (Distance 0)
        if dist2 == 0 and dist1 > 0:
            return 2  # email2 perfekt
        elif dist1 == 0 and dist2 > 0:
            return 1  # email1 perfekt
        
        # ✅ V7.7 NEU: Deutlich besserer Match (Distance 1 vs 2+)
        elif dist2 == 1 and dist1 >= 2:
            return 2  # email2 deutlich besser
        elif dist1 == 1 and dist2 >= 2:
            return 1  # email1 deutlich besser
        
        return 0  # Unklar oder gleich gut
    
    def calculate_email_quality_score(self, email, all_emails_in_group, person_name=""):
        """
        ✅ V2.0.1: Berechnet Quality-Score für Email-Typo-Erkennung
        
        Score-System (basierend auf Email-zu-Email und Email-zu-Person Vergleich):
        - Niedriger Score = Bessere Email
        - Vergleicht mit anderen Emails in der Gruppe
        - NEU: Vergleicht Email-Namen mit Personenname
        
        ✅ Beispiel (ANONYMISIERT):
        - max.musermann@uni-rostock.de (Typo) → höherer Score
        - max.mustermann@uni-rostock.de (korrekt) → niedriger Score
        
        🔒 WICHTIG: Nur anonymisierte Beispiele in Docstrings!
        
        Args:
            email: Die zu prüfende Email-Adresse
            all_emails_in_group: Liste aller Email-Adressen in der Gruppe
            person_name: Vollständiger Name der Person (optional)
        
        Returns:
            int: Quality-Score (niedriger = besser)
        """
        if '@' not in email:
            return 999  # Ungültige Email
        
        score = 0
        local_part, domain = email.split('@', 1)
        
        # Alter Email-zu-Email-Vergleich (bleibt erhalten)
        typo_distance = 0
        for other_email in all_emails_in_group:
            if other_email == email or '@' not in other_email:
                continue
            
            other_local, other_domain = other_email.split('@', 1)
            
            # Nur gleiche Domain vergleichen
            if domain != other_domain:
                continue
            
            dist = self.levenshtein_distance(local_part, other_local)
            
            if dist > 0 and (typo_distance == 0 or dist < typo_distance):
                typo_distance = dist
        
        score = typo_distance
        
        # NEU V2.0.1: Email-Name-vs-Person-Name-Check
        if person_name:
            email_name = self.extract_name_from_email(email)
            person_name_norm = self.normalize_text(person_name)
            
            # Vergleiche Namen
            distance = self.levenshtein_distance(email_name, person_name_norm)
            
            if distance == 0:
                # Email-Name perfekt (max.mustermann@... und "Max Mustermann")
                score -= 5
            elif 1 <= distance <= 2:
                # Email-Name hat Typo (max.musermann@... statt mustermann)
                score += 10
            # distance > 2: Abkürzung (m.mustermann@...), neutral (Score +0)
        
        return score
    
    def find_best_email_for_person(self, group, person_name_norm):
        """
        ✅ V2.0.2: Findet die beste Email-Adresse für eine Person aus allen ihren Einträgen.
        
        Priorität:
        1. Höchster Email-Quality-Score (uni-rostock.de, kein Typo)
        2. Bei gleichem Score: Frühestes Datum
        
        Args:
            group (DataFrame): Alle Einträge der Person
            person_name_norm (str): Normalisierter Name
            
        Returns:
            str: Beste Email-Adresse
        """
        best_email = None
        best_score = 999999
        best_date = None
        
        # Hole Personenname für Email-Qualitäts-Berechnung
        person_name = group.iloc[0]['Vollständiger Name'] if len(group) > 0 else ""
        all_emails = group['_email_clean'].tolist()
        
        for idx, row in group.iterrows():
            email = row['_email_clean']
            date = row['_datum_parsed']
            
            # Berechne Quality-Score
            score = self.calculate_email_quality_score(email, all_emails, person_name)
            
            # Wähle beste Email (niedrigster Score = beste Qualität)
            if score < best_score or (score == best_score and pd.notna(date) and (best_date is None or date < best_date)):
                best_email = email
                best_score = score
                best_date = date
        
        return best_email
    
    def correct_email_typos(self, df):
        """
        ✅ V2.0.2: Korrigiert Email-Typos bei Personen mit mehreren Einträgen.
        
        - Findet beste Email für jede Person
        - Korrigiert Typo-Emails auf beste Email
        - Erstellt Korrektur-Report
        
        Args:
            df (DataFrame): Eingabe-Daten mit normalisierten Spalten
            
        Returns:
            tuple: (korrigiertes DataFrame, Korrektur-Report DataFrame)
        """
        df_corrected = df.copy()
        corrections = []
        
        # Gruppiere nach normalisiertem Namen
        for name_norm, group in df_corrected.groupby('_name_norm'):
            if len(group) == 1:
                continue  # Nur eine Anmeldung, keine Korrektur nötig
            
            # Finde beste Email
            best_email = self.find_best_email_for_person(group, name_norm)
            
            # Korrigiere alle Einträge mit schlechterer Email
            for idx, row in group.iterrows():
                current_email = row['_email_clean']
                
                if current_email != best_email and best_email is not None:
                    # Email-Typo erkannt → Korrigiere
                    original_email = row['Uni-Mail']
                    df_corrected.at[idx, 'Uni-Mail'] = best_email
                    df_corrected.at[idx, '_email_clean'] = best_email
                    
                    # Speichere Korrektur für Report
                    corrections.append({
                        'ID': row['ID'],
                        'Vollständiger Name': row['Vollständiger Name'],
                        'Alte Email': original_email,
                        'Neue Email (korrigiert)': best_email,
                        'Datum': row['Datum'],
                        'Begründung': f'Email-Typo korrigiert (beste Email: {best_email})'
                    })
        
        corrections_df = pd.DataFrame(corrections)
        return df_corrected, corrections_df
    
    def prioritize_within_name_group(self, group):
        """
        ✅ V7.8: Intelligente Priorisierung bei gleichem Namen
        ✅ V7.9: Fügt behalten_grund-Spalte hinzu
        
        Neue Prioritäts-Reihenfolge:
        1. Uni-Email > Private Email
        2. Email-Qualität (Distance 0 > Distance 1 > Distance 2+) ← NEU!
        3. Frühestes Datum
        4. Niedrigste ID
        
        ✅ Beispiel (ANONYMISIERT):
        - ID 100: Max Mustermann, max.musermann@uni-rostock.de (Typo, früher)
        - ID 101: Max Mustermann, max.mustermann@uni-rostock.de (korrekt, später)
        → ID 101 wird behalten! (bessere Email-Qualität)
        
        🔒 WICHTIG: Nur anonymisierte Beispiele!
        
        Args:
            group: DataFrame-Gruppe mit gleichem Namen
        
        Returns:
            tuple: (beste_anmeldung, group_with_scores) - Die beste Anmeldung und die Gruppe mit berechneten Scores
        """
        # Schritt 1: Uni-Email-Check (wie bisher)
        group = group.copy()
        group['_has_uni_email'] = group['_email_clean'].apply(self.is_uni_email)
        
        uni_emails = group[group['_has_uni_email']]
        uni_email_preferred = False
        if not uni_emails.empty and len(group) > len(uni_emails):
            group = uni_emails
            uni_email_preferred = True
        
        # ✅ NEU: Schritt 2: Email-Qualitäts-Check
        # Berechne Scores für ALLE Emails in der Gruppe (wird später wiederverwendet)
        group = group.copy()
        
        # V2.0.1: Hole Personenname für Email-Name-Vergleich
        person_name = group.iloc[0]['Vollständiger Name'] if len(group) > 0 else ""
        
        group['_email_quality_score'] = group['_email_clean'].apply(
            lambda email: self.calculate_email_quality_score(email, group['_email_clean'].tolist(), person_name)
        )
        
        email_quality_better = False
        if len(group) > 1:
            # Behalte nur Email(s) mit bestem Score
            best_score = group['_email_quality_score'].min()
            group_filtered = group[group['_email_quality_score'] == best_score]
            if len(group_filtered) < len(group):
                email_quality_better = True
        else:
            group_filtered = group
        
        # Schritt 3: Datum & ID (wie bisher)
        group_sorted = group_filtered.sort_values(['_datum_parsed', '_id_num'], ascending=[True, True], na_position='last')
        
        kept_row = group_sorted.iloc[0].copy()
        
        # ✅ V7.9: Grund speichern
        if len(group) > 1:
            if uni_email_preferred:
                kept_row['behalten_grund'] = 'Uni-Email bevorzugt'
            elif email_quality_better:
                kept_row['behalten_grund'] = 'Beste Email-Qualität'
            elif pd.notna(kept_row['_datum_parsed']) and any(pd.notna(group['_datum_parsed'])):
                # Prüfe ob es tatsächlich ein früheres Datum ist
                earliest_date = group['_datum_parsed'].min()
                if kept_row['_datum_parsed'] == earliest_date:
                    kept_row['behalten_grund'] = 'Früheste Anmeldung'
                else:
                    kept_row['behalten_grund'] = 'Niedrigste ID (Fallback)'
            else:
                kept_row['behalten_grund'] = 'Niedrigste ID (Fallback)'
        else:
            kept_row['behalten_grund'] = 'Einzige Anmeldung'
        
        return kept_row, group
    
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
        V7.2: Findet doppelte Anmeldungen derselben Person
        V7.9: Fügt behalten_grund-Tracking hinzu
        PRIMÄR: Gleicher Name = gleiche Person (wichtig für Mediball)
        SEKUNDÄR: Auch gleiche Email prüfen (zusätzlich, wenn aktiviert)
        PERFORMANCE: Typo-Check nur innerhalb Email-Gruppen (500x schneller!)
        """
        zu_entfernen = []
        details = []
        behalten_gruende = {}  # ✅ V7.9: Speichere Gründe für behaltene Einträge
        
        df_work = df.copy()
        
        df_work['_name_norm'] = df_work['Vollständiger Name'].apply(self.normalize_text)
        # V7.2: Verwende clean_email statt normalize_text für Emails
        df_work['_email_clean'] = df_work['Uni-Mail'].apply(self.clean_email)
        df_work['_datum_parsed'] = df_work['Datum'].apply(self.parse_datetime)
        df_work['_id_num'] = pd.to_numeric(df_work['ID'], errors='coerce').fillna(10**18)
        
        # === PRIMÄR: Name-basierte Duplikate (WICHTIG für Mediball) ===
        for name, group in df_work[df_work['_name_norm'] != ''].groupby('_name_norm'):
            if len(group) > 1:
                # ✅ V7.8: Nutze intelligente Priorisierung mit Email-Quality-Scoring
                beste_anmeldung, group_with_scores = self.prioritize_within_name_group(group)
                
                # ✅ V7.9: Speichere Grund für behaltene Anmeldung
                if 'behalten_grund' in beste_anmeldung:
                    behalten_gruende[beste_anmeldung.name] = beste_anmeldung['behalten_grund']
                
                # Alle anderen sind Duplikate
                for idx, dup_row in group_with_scores.iterrows():
                    if idx == beste_anmeldung.name:  # .name gibt den Index zurück
                        continue
                        
                    if idx not in zu_entfernen:
                        zu_entfernen.append(idx)
                        
                        # Datum-Info
                        if pd.notna(dup_row['_datum_parsed']):
                            dup_datum_info = dup_row['Datum']
                        else:
                            dup_datum_info = f"ohne Datum (ID: {dup_row['ID']})"
                        
                        if pd.notna(beste_anmeldung['_datum_parsed']):
                            beste_datum_info = beste_anmeldung['Datum']
                        else:
                            beste_datum_info = f"ohne Datum (ID: {beste_anmeldung['ID']})"
                        
                        # V7.2: Prüfe Emails mit clean_email
                        email_unterschiedlich = (
                            (dup_row['_email_clean'] != beste_anmeldung['_email_clean']) and 
                            (dup_row['_email_clean'] != '') and 
                            (beste_anmeldung['_email_clean'] != '')
                        )
                        
                        # V7.9: Email-Vergleichs-Hinweis mit Unterscheidung zwischen Typo und Variante
                        email_hinweis = ""
                        if email_unterschiedlich:
                            dup_email = dup_row['_email_clean']
                            beste_email = beste_anmeldung['_email_clean']
                            
                            # Prüfe ob eine Uni-Email und die andere nicht
                            dup_is_uni = self.is_uni_email(dup_email)
                            beste_is_uni = self.is_uni_email(beste_email)
                            
                            if dup_is_uni and not beste_is_uni:
                                email_hinweis = f" 🎓 HINWEIS: Uni-Email ({dup_row['Uni-Mail']}) vs. Private Email ({beste_anmeldung['Uni-Mail']}) - Uni-Email hat Priorität!"
                            elif beste_is_uni and not dup_is_uni:
                                email_hinweis = f" 🎓 HINWEIS: Private Email ({dup_row['Uni-Mail']}) vs. Uni-Email ({beste_anmeldung['Uni-Mail']}) - Uni-Email hat Priorität!"
                            else:
                                # ✅ V7.9: Verwende neue Email-Vergleichsfunktion
                                reason = self.get_email_comparison_reason(dup_email, beste_email)
                                
                                # ✅ V7.8: Verwende bereits berechnete Email-Qualität (keine Neuberechnung!)
                                dup_quality = dup_row['_email_quality_score']
                                beste_quality = beste_anmeldung['_email_quality_score']
                                
                                if dup_quality > beste_quality:
                                    email_hinweis = f" 📧 HINWEIS: {reason} ({dup_row['Uni-Mail']} Score={dup_quality}) vs. ({beste_anmeldung['Uni-Mail']} Score={beste_quality})"
                                    # Log zur Runtime (erlaubt mit echten Namen)
                                    self.log_result(f"   📧 Email-Qualität: {name} - {dup_row['Uni-Mail']} (Score {dup_quality}) → {beste_anmeldung['Uni-Mail']} (Score {beste_quality})\n")
                                else:
                                    # Gleiche Qualität (beide Emails haben Distance 0 oder gleichen Typo-Score) oder keine Typos gefunden
                                    email_hinweis = f" ⚠️ ACHTUNG: {reason} ({dup_row['Uni-Mail']} vs {beste_anmeldung['Uni-Mail']})"
                        
                        details.append({
                            'modus': 'person_name',  # ✅ V7: modus-Spalte
                            'entfernt_id': dup_row['ID'],
                            'entfernt_name': dup_row['Vollständiger Name'],
                            'entfernt_email': dup_row['Uni-Mail'],
                            'entfernt_datum': dup_row['Datum'],
                            'grund': f"Doppelte Anmeldung (gleicher Name). Angemeldet am {dup_datum_info}. Beste Anmeldung war am {beste_datum_info} (ID: {beste_anmeldung['ID']}){email_hinweis}",
                            'behalten_id': beste_anmeldung['ID'],
                            'behalten_name': beste_anmeldung['Vollständiger Name'],
                            'behalten_email': beste_anmeldung['Uni-Mail']
                        })
        
        # === SEKUNDÄR: Email-basierte Duplikate (nur wenn noch nicht erfasst) ===
        if self.check_email_duplicates.get():
            # V7.2: Typo-Check nur innerhalb Email-Gruppen für Performance
            for email, group in df_work[df_work['_email_clean'] != ''].groupby('_email_clean'):
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
                            
                            # V7.6: Typo-Check mit Levenshtein-Distance (konsistenter!)
                            # Prüfe ob Namen ähnlich sind (z.B. Freytagg vs Freytag)
                            name1 = dup_row['_name_norm']
                            name2 = erste_anmeldung['_name_norm']
                            
                            typo_hint = ""
                            if len(name1) > 0 and len(name2) > 0:
                                # V7.6: Nutze Levenshtein-Distance für präzisen Typo-Check
                                distance = self.levenshtein_distance(name1, name2)
                                if distance <= 2:
                                    typo_hint = f" (Möglicher Tippfehler im Namen! Ähnlichkeit: Distanz={distance})"
                            
                            details.append({
                                'modus': 'person_email',  # ✅ V7: modus-Spalte
                                'entfernt_id': dup_row['ID'],
                                'entfernt_name': dup_row['Vollständiger Name'],
                                'entfernt_email': dup_row['Uni-Mail'],
                                'entfernt_datum': dup_row['Datum'],
                                'grund': f"⚠️ Doppelte Anmeldung (gleiche Email, unterschiedlicher Name: '{dup_row['Vollständiger Name']}' vs '{erste_anmeldung['Vollständiger Name']}'){typo_hint}. Angemeldet am {dup_datum_info}. Erste Anmeldung war am {erste_datum_info} (ID: {erste_anmeldung['ID']}).",
                                'behalten_id': erste_anmeldung['ID'],
                                'behalten_name': erste_anmeldung['Vollständiger Name'],
                                'behalten_email': erste_anmeldung['Uni-Mail']
                            })
        
        return zu_entfernen, details, behalten_gruende
    
    def find_verdachtsfaelle(self, df):
        """
        ✅ V7.7: Findet ähnliche Namen (Distance 1-2 oder phonetisch ähnlich) mit unterschiedlichen Emails.
        Diese werden NICHT gelöscht, sondern nur im Report ausgegeben.
        
        V7.7 NEU: Phonetische Ähnlichkeit wird ebenfalls erkannt (z.B. Meyer vs Meier)
        
        FIX: Verwendet Nachname-Blocking, um auch UNTERSCHIEDLICHE normalisierte Namen zu vergleichen.
        
        Beispiel:
        - "Schmidt" vs "Schmitt" (Distance 1) + unterschiedliche Emails → Verdachtsfall
        - "Mustermann" vs "Musterman" (Distance 1) + unterschiedliche Emails → Verdachtsfall
        - "Meyer" vs "Meier" (phonetisch ähnlich) + unterschiedliche Emails → Verdachtsfall
        
        Args:
            df: DataFrame mit den Anmeldungen (muss bereits _name_norm, _email_clean haben)
        
        Returns: 
            Liste von Verdachtsfällen (Dictionaries)
        """
        verdachtsfaelle = []
        
        # Arbeite auf dem gleichen normalisierten DF
        seen_pairs = set()  # Vermeide Duplikate im Report
        
        # V7.6: Extrahiere Nachname (letztes Token) für Blocking
        df_work = df.copy()
        df_work['_nachname_block'] = df_work['_name_norm'].apply(
            lambda x: x.split()[-1] if x and len(x.split()) > 0 else ''
        )
        
        # V7.6: Gruppiere nach Nachname-Block (nur Personen mit ähnlichem Nachname vergleichen)
        for nachname_block, group in df_work[df_work['_nachname_block'] != ''].groupby('_nachname_block'):
            if len(group) < 2:
                continue
            
            # Prüfe alle Paare innerhalb dieses Blocks
            group_list = list(group.iterrows())
            
            for i, (idx1, row1) in enumerate(group_list):
                for j in range(i + 1, len(group_list)):
                    idx2, row2 = group_list[j]
                    
                    # Skip wenn GLEICHER normalisierter Name (das sind echte Duplikate, keine Verdachtsfälle)
                    if row1['_name_norm'] == row2['_name_norm']:
                        continue
                    
                    # Prüfe ob unterschiedliche Emails
                    if row1['_email_clean'] == row2['_email_clean']:
                        continue  # Gleiche Email → kein Verdachtsfall
                    
                    if row1['_email_clean'] == '' or row2['_email_clean'] == '':
                        continue  # Leere Email → skip
                    
                    # V7.6: Berechne Distance zwischen normalisierten Namen
                    dist = self.levenshtein_distance(row1['_name_norm'], row2['_name_norm'])
                    
                    # ✅ V7.7 NEU: Phonetischer Check
                    phonetic1 = self.phonetic_key(row1['_name_norm'])
                    phonetic2 = self.phonetic_key(row2['_name_norm'])
                    
                    # Verdachtsfall wenn Distance 1-2 ODER phonetisch identisch (aber Distance > 2)
                    is_suspicious = False
                    grund = ""
                    
                    if 1 <= dist <= 2:
                        is_suspicious = True
                        grund = f"⚠️ Verdachtsfall: Ähnliche Namen (Levenshtein-Distance {dist}), aber unterschiedliche Emails. Bitte manuell prüfen ob gleiche Person oder echter Tippfehler!"
                    elif phonetic1 == phonetic2 and phonetic1 != '' and dist > 2:
                        # ✅ V7.7 NEU: Phonetisch identisch, aber große Schreibweise-Unterschiede
                        is_suspicious = True
                        grund = f"⚠️ Phonetisch ähnlich ({phonetic1}), aber Levenshtein-Distance {dist}. Unterschiedliche Schreibweise - bitte manuell prüfen!"
                    
                    if is_suspicious:
                        # Vermeide Duplikate im Report
                        pair_key = tuple(sorted([row1['ID'], row2['ID']]))
                        if pair_key in seen_pairs:
                            continue
                        seen_pairs.add(pair_key)
                        
                        verdachtsfaelle.append({
                            'modus': 'suspicious_phonetic' if phonetic1 == phonetic2 and dist > 2 else 'suspicious',
                            'distance': dist,
                            'phonetic_key': phonetic1 if phonetic1 == phonetic2 else '',
                            'id1': row1['ID'],
                            'name1': row1['Vollständiger Name'],
                            'email1': row1['Uni-Mail'],
                            'datum1': row1['Datum'],
                            'id2': row2['ID'],
                            'name2': row2['Vollständiger Name'],
                            'email2': row2['Uni-Mail'],
                            'datum2': row2['Datum'],
                            'grund': grund
                        })
        
        return verdachtsfaelle
    
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
            
            # ✅ V2.0.2 NEU: Email-Typo-Korrektur (VOR Duplikat-Erkennung)
            corrections_df = pd.DataFrame()
            if mode in ['person', 'alle'] and self.correct_email_typos_var.get():
                self.log_result("📧 Korrigiere Email-Typos...\n")
                
                # Vorbereite DataFrame mit normalisierten Werten
                df_for_correction = df.copy()
                df_for_correction['_name_norm'] = df_for_correction['Vollständiger Name'].apply(self.normalize_text)
                
                # Domain-Learning für Email-Cleaning
                df_for_correction['_email_clean'] = df_for_correction['Uni-Mail'].apply(self.clean_email)
                learned_domains = self.analyze_domain_frequencies(df_for_correction)
                df_for_correction['_email_clean'] = df_for_correction['Uni-Mail'].apply(
                    lambda x: self.clean_email(x, learned_domains)
                )
                
                # Füge _datum_parsed für find_best_email_for_person hinzu
                df_for_correction['_datum_parsed'] = df_for_correction['Datum'].apply(self.parse_datetime)
                
                # Korrigiere Email-Typos
                df_corrected, corrections_df = self.correct_email_typos(df_for_correction)
                
                # Übertrage korrigierte Emails zurück zum Haupt-DataFrame
                df['Uni-Mail'] = df_corrected['Uni-Mail']
                
                if not corrections_df.empty:
                    self.log_result(f"   ✅ {len(corrections_df)} Email-Typos korrigiert\n\n")
                    # Zeige max 3 Beispiele
                    for i, corr in corrections_df.head(3).iterrows():
                        self.log_result(f"   📧 ID {corr['ID']}: {corr['Alte Email']} → {corr['Neue Email (korrigiert)']}\n")
                    if len(corrections_df) > 3:
                        self.log_result(f"   ... und {len(corrections_df)-3} weitere (siehe Email-Korrekturen-Report)\n")
                    self.log_result("\n")
                else:
                    self.log_result("   ✓ Keine Email-Korrekturen nötig\n\n")
            
            # Personen-Duplikate
            behalten_gruende = {}  # ✅ V7.9: Tracke Gründe für behaltene Einträge
            if mode in ['person', 'alle']:
                self.log_result("🔍 Prüfe doppelte Personen (primär: Name)...\n")
                if self.check_email_duplicates.get():
                    self.log_result("   ✓ Email-basierte Duplikate werden zusätzlich geprüft\n")
                personen_entfernen, personen_details, behalten_gruende = self.find_personen_duplikate(df)
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
            
            # ✅ V7.5 NEU: Finde Verdachtsfälle (werden NICHT gelöscht!)
            verdachtsfaelle = []
            if mode in ['person', 'alle']:
                # Vorbereite DataFrame mit normalisierten Werten für Verdachtsfälle-Check
                df_work = df.copy()
                df_work['_name_norm'] = df_work['Vollständiger Name'].apply(self.normalize_text)
                
                # ✅ V7.8: Domain-Learning VOR dem Email-Cleaning
                # Erste Pass: Email-Cleaning ohne learned_domains für Frequenz-Analyse
                self.log_result("📊 Analysiere Domain-Häufigkeiten...\n")
                df_work['_email_clean'] = df_work['Uni-Mail'].apply(self.clean_email)
                learned_domains = self.analyze_domain_frequencies(df_work)
                self.log_result("\n")
                
                # Zweite Pass: Email-Cleaning MIT learned_domains für finale Korrektur
                df_work['_email_clean'] = df_work['Uni-Mail'].apply(
                    lambda x: self.clean_email(x, learned_domains)
                )
                
                self.log_result("🔍 Prüfe Verdachtsfälle (ähnliche Namen, unterschiedliche Emails)...\n")
                verdachtsfaelle = self.find_verdachtsfaelle(df_work)
                
                if verdachtsfaelle:
                    self.log_result(f"⚠️  {len(verdachtsfaelle)} Verdachtsfälle gefunden:\n")
                    self.log_result(f"   → Diese Personen wurden NICHT automatisch gelöscht!\n")
                    self.log_result(f"   → Bitte manuell im Verdachtsfälle-Report prüfen!\n\n")
                    
                    # Zeige max 3 Beispiele im Log
                    for vf in verdachtsfaelle[:3]:
                        self.log_result(f"   ⚠️ '{vf['name1']}' ({vf['email1']}) vs '{vf['name2']}' ({vf['email2']}) - Distance {vf['distance']}\n")
                    if len(verdachtsfaelle) > 3:
                        self.log_result(f"   ... und {len(verdachtsfaelle)-3} weitere (siehe Verdachtsfälle-Report)\n")
                    self.log_result("\n")
                else:
                    self.log_result("   ✓ Keine Verdachtsfälle gefunden\n\n")
            
            # Entferne Duplikate
            alle_zu_entfernen = sorted(list(set(alle_zu_entfernen)))
            df_bereinigt = df.drop(index=alle_zu_entfernen).reset_index(drop=True)
            
            # ✅ V7.9: Füge behalten_grund-Spalte hinzu
            df_bereinigt['behalten_grund'] = 'Einzige Anmeldung'
            
            # Übertrage Gründe aus behalten_gruende (Index aus df_work zu Index in df_bereinigt mappen)
            if behalten_gruende:
                # Erstelle Mapping von alten Indizes zu neuen
                alte_zu_neue_index = {}
                neue_idx = 0
                for alte_idx in df.index:
                    if alte_idx not in alle_zu_entfernen:
                        alte_zu_neue_index[alte_idx] = neue_idx
                        neue_idx += 1
                
                # Übertrage Gründe
                for alte_idx, grund in behalten_gruende.items():
                    if alte_idx in alte_zu_neue_index:
                        neue_idx = alte_zu_neue_index[alte_idx]
                        df_bereinigt.at[neue_idx, 'behalten_grund'] = grund
            
            # Statistik
            self.log_result(f"{'='*85}\n")
            self.log_result(f"📊 ZUSAMMENFASSUNG:\n\n")
            self.log_result(f"   Original Anmeldungen:      {original_count}\n")
            self.log_result(f"   Entfernte Duplikate:       {len(alle_zu_entfernen)}\n")
            self.log_result(f"   Bereinigte Anmeldungen:    {len(df_bereinigt)}\n")
            self.log_result(f"   {'─'*40}\n")
            self.log_result(f"   Verfügbare Ticketplätze:   {len(df_bereinigt)} 🎫\n")
            
            # V2.0.2: Erweiterte Info über verwendete Normalisierungen
            self.log_result(f"\n{'='*85}\n")
            self.log_result(f"ℹ️  V2.0.2 - Email-Korrektur + Hybrid Domain:\n\n")
            self.log_result(f"  ✅ V2.0.2 NEU: Email-Typo-Korrektur (Warteplatz-Erhaltung)\n")
            self.log_result(f"  ✅ V7.8: Pattern-Check (Subdomains + TLD)\n")
            self.log_result(f"  ✅ V7.8: Domain-Learning (häufige Domains aus CSV)\n")
            self.log_result(f"  ✅ V7.7: Known-Domains (uni-rostock.de, gmail.com, etc.)\n")
            self.log_result(f"  ✅ V7.7: Email Distance 1 vs 2+ Erkennung\n")
            self.log_result(f"  ✅ V7.7: Phonetische Ähnlichkeit (Meyer vs Meier)\n")
            self.log_result(f"  ⚠️ Verdachtsfälle-Report (ähnliche Namen werden gemeldet)\n")
            self.log_result(f"  🎓 Uni-Email-Priorität (@uni-rostock.de)\n")
            self.log_result(f"  ⚡ Performance-optimiert\n\n")
            self.log_result(f"   ✅ Email-Säuberung (mailto:, Leerzeichen, mehrere Emails)\n")
            self.log_result(f"   ✅ Titel-Entfernung (Dr., Prof., etc.)\n")
            self.log_result(f"   ✅ Apostroph-Normalisierung (O'Connor)\n")
            self.log_result(f"   ✅ \"Nachname, Vorname\" Erkennung\n")
            self.log_result(f"   ✅ Bindestrich = Leerzeichen (Meyer-Lüdenscheidt)\n")
            self.log_result(f"   ✅ Umlaut-Normalisierung (ä→ae, ö→oe, ü→ue, ß→ss)\n")
            self.log_result(f"   ✅ Uni-Email Priorität (uni-rostock.de > gmx.de)\n")
            self.log_result(f"   ⚡ Typo-Check Performance-Optimierung\n")
            
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
            
            # ✅ V7.5 NEU: Verdachtsfälle-Report speichern
            if verdachtsfaelle:
                verdacht_file = str(Path(self.output_file).parent / (Path(self.output_file).stem + "_verdachtsfaelle.csv"))
                df_verdacht = pd.DataFrame(verdachtsfaelle)
                
                # Spalten-Reihenfolge
                cols = ['modus', 'distance', 'id1', 'name1', 'email1', 'datum1', 'id2', 'name2', 'email2', 'datum2', 'grund']
                df_verdacht = df_verdacht[cols]
                
                df_verdacht.to_csv(verdacht_file, index=False, encoding='utf-8-sig', sep=output_sep)
                self.log_result(f"⚠️  Verdachtsfälle-Report gespeichert: {Path(verdacht_file).name}\n")
                self.log_result(f"   ({len(verdachtsfaelle)} Fälle, die manuell geprüft werden sollten)\n")
            
            # ✅ V2.0.2 NEU: Email-Korrekturen-Report speichern
            if not corrections_df.empty:
                corrections_file = str(Path(self.output_file).parent / (Path(self.output_file).stem + "_email_korrekturen.csv"))
                corrections_df.to_csv(corrections_file, index=False, encoding='utf-8-sig', sep=output_sep)
                self.log_result(f"📧 Email-Korrekturen-Report gespeichert: {Path(corrections_file).name}\n")
                self.log_result(f"   ({len(corrections_df)} Email-Korrekturen durchgeführt)\n")
            
            messagebox.showinfo("Erfolg! 🎉", 
                f"V2.0.2 - Duplikat-Filterung abgeschlossen!\n\n"
                f"Original: {original_count} Anmeldungen\n"
                f"Entfernt: {len(alle_zu_entfernen)} Duplikate\n"
                f"Bereinigt: {len(df_bereinigt)} gültige Anmeldungen\n"
                f"Email-Korrekturen: {len(corrections_df) if not corrections_df.empty else 0}\n"
                f"Verdachtsfälle: {len(verdachtsfaelle) if verdachtsfaelle else 0}\n\n"
                f"V2.0.2 Features:\n"
                f"📧 Email-Typo-Korrektur (NEU)\n"
                f"✅ Hybrid Domain-Korrektur\n"
                f"📊 Domain-Learning aktiv\n"
                f"🎓 Uni-Mail-Priorität\n"
                f"⚡ Production-Ready")
            
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
