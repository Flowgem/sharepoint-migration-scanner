import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import csv
from typing import List, Dict
import webbrowser

class ScannerGUI:
    def __init__(self, root: tk.Tk, scanner):
        self.root = root
        self.scanner = scanner
        self.setup_ui()
        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()
        
        # Main application style
        style.configure('TFrame', background='#f5f6f7')  # Lighter background
        
        # Header styles
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 14, 'bold'),
                       background='#f5f6f7',
                       padding=5)
        
        # Stats panel style
        style.configure('Stats.TFrame',
                       background='#ffffff',
                       relief='solid')
        style.configure('Stats.TLabel',
                       font=('Segoe UI', 11),
                       background='#ffffff',
                       padding=8)
        
        # Button styles
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10),
                       padding=10)
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 10),
                       padding=10)
        
        # Creator styles
        style.configure('Creator.TLabel',
                       font=('Segoe UI', 12),
                       background='#f5f6f7',
                       padding=3)
        style.configure('CreatorLink.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#0078d4',
                       background='#f5f6f7',
                       padding=3)
        
        # Path label style
        style.configure('Path.TLabel',
                       font=('Segoe UI', 11),
                       background='#f5f6f7',
                       padding=3)
        
        # Treeview styles
        style.configure("Treeview",
                       font=('Segoe UI', 10),
                       rowheight=30,
                       background="#ffffff",
                       fieldbackground="#ffffff")
        style.configure("Treeview.Heading",
                       font=('Segoe UI', 10, 'bold'),
                       padding=5)
        style.map('Treeview', 
                 background=[('selected', '#e5f3ff')],
                 foreground=[('selected', '#000000')])

    def setup_ui(self):
        # Main container with padding
        self.main_frame = ttk.Frame(self.root, padding="20", style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Header frame
        header_frame = ttk.Frame(self.main_frame, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # Current path with icon (📁)
        path_frame = ttk.Frame(header_frame, style='TFrame')
        path_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(
            path_frame,
            text="📁",
            style='Path.TLabel'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.current_path_label = ttk.Label(
            path_frame,
            text="No directory selected",
            style='Path.TLabel',
            wraplength=800
        )
        self.current_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Developer info
        dev_container = ttk.Frame(header_frame, style='TFrame')
        dev_container.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(
            dev_container,
            text="Created by ",
            style='Creator.TLabel'
        ).pack(side=tk.LEFT)
        
        dev_label = ttk.Label(
            dev_container,
            text="Flowgem.io",
            style='CreatorLink.TLabel',
            cursor="hand2"
        )
        dev_label.pack(side=tk.LEFT)
        dev_label.bind("<Button-1>", lambda e: webbrowser.open("https://flowgem.io"))

        # Stats panel with border and background
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Inner frame for stats with border
        inner_stats_frame = ttk.Frame(
            stats_frame,
            style='Stats.TFrame',
            relief='solid',
            borderwidth=1
        )
        inner_stats_frame.pack(fill=tk.X)

        # Stats with icons in inner frame
        self.total_files_label = ttk.Label(
            inner_stats_frame,
            text="📄 Total Files: 0",
            style='Stats.TLabel'
        )
        self.total_files_label.pack(side=tk.LEFT, padx=15, pady=5)

        self.score_label = ttk.Label(
            inner_stats_frame,
            text="📊 Compliance Score: N/A",
            style='Stats.TLabel'
        )
        self.score_label.pack(side=tk.LEFT, padx=15, pady=5)

        self.issues_count_label = ttk.Label(
            inner_stats_frame,
            text="⚠️ Issues Found: 0",
            style='Stats.TLabel'
        )
        self.issues_count_label.pack(side=tk.LEFT, padx=15, pady=5)

        # Control panel
        control_frame = ttk.Frame(self.main_frame, style='TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Primary action button
        self.scan_btn = ttk.Button(
            control_frame,
            text="🔍 Select Directory & Scan",
            command=self.scan_directory,
            style='Primary.TButton'
        )
        self.scan_btn.pack(side=tk.LEFT, padx=5)

        # Secondary action buttons
        self.manage_ext_btn = ttk.Button(
            control_frame,
            text="⚙️ Manage Extensions",
            command=self.manage_extensions,
            style='Secondary.TButton'
        )
        self.manage_ext_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = ttk.Button(
            control_frame,
            text="📥 Export Results",
            command=self.export_results,
            style='Secondary.TButton'
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)

        # Results section
        results_frame = ttk.Frame(self.main_frame, style='TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            results_frame,
            text="Scan Results",
            style='Header.TLabel'
        ).pack(anchor=tk.W, pady=(0, 10))

        self.create_treeview(results_frame)

    def create_treeview(self, parent):
        # Create treeview with striped rows
        style = ttk.Style()
        style.configure("Treeview",
                       background="#ffffff",
                       fieldbackground="#ffffff",
                       rowheight=25)
        style.map('Treeview', background=[('selected', '#0078D7')])

        # Create treeview frame
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('name', 'path', 'issue', 'suggested_fix')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            style="Treeview"
        )

        # Define headings
        self.tree.heading('name', text='Name')
        self.tree.heading('path', text='Path')
        self.tree.heading('issue', text='Issue')
        self.tree.heading('suggested_fix', text='Suggested Fix')

        # Define column widths
        self.tree.column('name', width=150)
        self.tree.column('path', width=250)
        self.tree.column('issue', width=200)
        self.tree.column('suggested_fix', width=200)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        x_scrollbar = ttk.Scrollbar(
            tree_frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )
        
        self.tree.configure(
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )

        # Pack everything
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def scan_directory(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        # Update current path label
        self.current_path_label.config(text=f"Scanning: {directory}")

        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Perform scan
        issues = self.scanner.scan_directory(directory)
        
        # Update current path label with final status
        self.current_path_label.config(text=f"Current Directory: {directory}")
        
        # Update results
        for issue in issues:
            self.tree.insert('', tk.END, values=(
                issue['name'],
                issue['path'],
                issue['issue'],
                issue['suggested_fix']
            ))

        # Update statistics
        self.total_files_label.config(
            text=f"Total Files: {self.scanner.total_files}"
        )
        self.issues_count_label.config(
            text=f"Issues Found: {len(issues)}"
        )
        score = self.scanner.get_compliance_score()
        self.score_label.config(
            text=f"Compliance Score: {score:.1f}%"
        )

        # Show found extensions count
        found_extensions = self.scanner.get_found_extensions()
        if found_extensions:
            messagebox.showinfo(
                "Scan Complete",
                f"Found {len(found_extensions)} different file extensions.\n"
                "Use 'Manage Extensions' to configure which ones to allow/block."
            )

    def export_results(self):
        if not self.tree.get_children():
            messagebox.showwarning(
                "No Data",
                "No results to export. Please perform a scan first."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv")]
        )
        
        if not filename:
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Path', 'Issue', 'Suggested Fix'])
            
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item)['values'])

        messagebox.showinfo(
            "Success",
            f"Results exported to {filename}"
        ) 

    def manage_extensions(self):
        if not self.scanner.get_current_directory():
            messagebox.showwarning(
                "No Directory Scanned",
                "Please scan a directory first before managing extensions."
            )
            return
        
        if not self.scanner.get_found_extensions():
            messagebox.showinfo(
                "No Extensions Found",
                "No files with extensions were found in the scanned directory."
            )
            return
        
        dialog = ExtensionManagerDialog(self.root, self.scanner, self)
        self.root.wait_window(dialog)

    def bind_extension_updates(self):
        """This method will be called when initializing, but we'll implement the actual
        binding in the ExtensionManagerDialog"""
        pass

    def update_filtered_results(self):
        """Recalculate compliance score and issues based on filtered extensions"""
        # Get the current scan results from the scanner
        if not hasattr(self.scanner, 'current_directory') or not self.scanner.current_directory:
            return

        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get new filtered results
        issues = self.scanner.get_filtered_issues()
        
        # Update results in treeview
        for issue in issues:
            self.tree.insert('', tk.END, values=(
                issue['name'],
                issue['path'],
                issue['issue'],
                issue['suggested_fix']
            ))

        # Update statistics
        total_files = self.scanner.total_files
        total_issues = len(issues)
        
        if total_files > 0:
            compliant_files = total_files - total_issues
            compliance_score = (compliant_files / total_files) * 100
        else:
            compliance_score = 100

        self.total_files_label.config(text=f"📄 Total Files: {total_files}")
        self.score_label.config(text=f"📊 Compliance Score: {compliance_score:.1f}%")
        self.issues_count_label.config(text=f"⚠️ Issues Found: {total_issues}")

class ExtensionManagerDialog(tk.Toplevel):
    def __init__(self, parent, scanner, main_gui):
        super().__init__(parent)
        self.scanner = scanner
        self.parent = parent
        self.main_gui = main_gui
        
        self.title("Manage Extensions")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Store original extension states for cancel operation
        self.original_unsupported = self.scanner.get_unsupported_extensions()
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Store checkbutton variables
        self.check_vars = {}
        
        self.setup_ui()
        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()
        
        # Extension manager specific styles
        style.configure('ExtManager.TFrame',
                       background='#f5f6f7',
                       relief='flat')
        style.configure('ExtManager.TLabel',
                       font=('Segoe UI', 11),
                       background='#f5f6f7',
                       padding=5)
        style.configure('ExtManagerHeader.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       background='#f5f6f7',
                       padding=5)
        style.configure('ExtManager.TCheckbutton',
                       font=('Segoe UI', 10),
                       background='#ffffff')
        style.configure('ExtManagerSearch.TEntry',
                       font=('Segoe UI', 10))
        style.configure('ExtManager.TButton',
                       font=('Segoe UI', 10),
                       padding=8)
        
    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self, padding="20", style='ExtManager.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header with icon and title
        header_frame = ttk.Frame(main_frame, style='ExtManager.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            header_frame,
            text="⚙️ Extension Manager",
            style='ExtManagerHeader.TLabel'
        ).pack(side=tk.LEFT)

        # Current directory info
        current_dir = self.scanner.get_current_directory() or "No directory scanned"
        dir_frame = ttk.Frame(main_frame, style='ExtManager.TFrame')
        dir_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            dir_frame,
            text="📁 Current Directory:",
            style='ExtManager.TLabel'
        ).pack(anchor=tk.W)
        
        ttk.Label(
            dir_frame,
            text=current_dir,
            style='ExtManager.TLabel',
            wraplength=550
        ).pack(anchor=tk.W, padx=(20, 0))

        # Search frame with modern styling
        search_frame = ttk.Frame(main_frame, style='ExtManager.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            search_frame,
            text="🔍",
            style='ExtManager.TLabel'
        ).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_extensions)
        
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            style='ExtManagerSearch.TEntry'
        )
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        search_entry.insert(0, "Search extensions...")
        search_entry.bind('<FocusIn>', lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "Search extensions..." else None)
        search_entry.bind('<FocusOut>', lambda e: search_entry.insert(0, "Search extensions...") if not search_entry.get() else None)

        # Extensions list in a white frame with border
        list_frame = ttk.Frame(main_frame, style='ExtManager.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollable frame
        self.canvas = tk.Canvas(
            list_frame,
            bg='#ffffff',
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        # Create frame for checkboxes
        self.checkbox_frame = tk.Frame(
            self.canvas,
            bg='#ffffff'
        )

        # Configure scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create window in canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.checkbox_frame,
            anchor='nw'
        )

        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure canvas window resizing
        self.checkbox_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # Button frame with modern styling
        btn_frame = ttk.Frame(main_frame, style='ExtManager.TFrame')
        btn_frame.pack(fill=tk.X, pady=(15, 0))

        # Action buttons
        ttk.Button(
            btn_frame,
            text="🚫 Block All",
            command=self.select_all,
            style='ExtManager.TButton'
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="✅ Allow All",
            command=self.deselect_all,
            style='ExtManager.TButton'
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Apply Changes",
            command=self.apply_changes,
            style='ExtManager.TButton'
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel_changes,
            style='ExtManager.TButton'
        ).pack(side=tk.RIGHT, padx=5)

        # Populate checkboxes
        self.refresh_list()

    def refresh_list(self):
        print("\nStarting refresh_list in ExtensionManagerDialog")
        
        # Clear existing checkboxes
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()
        
        # Get found extensions
        found_extensions = sorted(self.scanner.get_found_extensions())
        print(f"Retrieved extensions from scanner: {found_extensions}")
        
        if not found_extensions:
            print("No extensions found, displaying message...")
            label = ttk.Label(
                self.checkbox_frame,
                text="No files found in the scanned directory",
                style='ExtManagerHeader.TLabel'
            )
            label.pack(pady=20)
            return
        
        print(f"Creating checkboxes for {len(found_extensions)} extensions...")
        # Add checkboxes for found extensions
        for ext in found_extensions:
            print(f"Creating checkbox for extension: {ext}")
            frame = tk.Frame(
                self.checkbox_frame,
                bg='#ffffff'
            )
            frame.pack(fill=tk.X, padx=10, pady=3)
            
            # Create variable for checkbox - set to True if extension is unsupported
            is_blocked = ext in self.scanner.unsupported_extensions
            var = tk.BooleanVar(value=is_blocked)  # Changed from True to is_blocked
            self.check_vars[ext] = var
            
            # Create checkbox
            cb = ttk.Checkbutton(
                frame,
                text=f"{ext}",
                variable=var,
                style='ExtManager.TCheckbutton',
                command=self.on_checkbox_change
            )
            cb.pack(side=tk.LEFT, padx=(5, 0))

        print("Finished creating checkboxes")
        # Update the canvas scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        print("Canvas scroll region updated")
    
    def filter_extensions(self, *args):
        search_text = self.search_var.get().lower()
        for frame in self.checkbox_frame.winfo_children():
            if isinstance(frame, ttk.Frame):
                checkbox = frame.winfo_children()[0]  # Get the checkbutton from the frame
                if search_text in checkbox['text'].lower():
                    frame.pack(fill=tk.X, padx=5, pady=2)
                else:
                    frame.pack_forget()
    
    def on_checkbox_change(self):
        """Called when any checkbox state changes"""
        # Update scanner's unsupported extensions based on current checkbox states
        new_unsupported = set()
        for ext, var in self.check_vars.items():
            if var.get():  # If checkbox is checked, extension is unsupported
                new_unsupported.add(ext)
        
        self.scanner.unsupported_extensions = new_unsupported
        
        # Update the main GUI's display
        self.main_gui.update_filtered_results()
    
    def select_all(self):
        for var in self.check_vars.values():
            var.set(True)
    
    def deselect_all(self):
        for var in self.check_vars.values():
            var.set(False)
    
    def add_extension(self):
        extension = simpledialog.askstring(
            "Add Extension",
            "Enter file extension (with or without dot):",
            parent=self
        )
        if extension:
            self.scanner.add_unsupported_extension(extension)
            self.refresh_list()
            
    def reset_extensions(self):
        if messagebox.askyesno(
            "Reset Extensions",
            "Are you sure you want to reset to default extensions?"
        ):
            self.scanner.reset_unsupported_extensions()
            self.refresh_list()
    
    def apply_changes(self):
        # Update scanner's unsupported extensions based on checkbox states
        new_unsupported = set()
        for ext, var in self.check_vars.items():
            if var.get():
                new_unsupported.add(ext)
        
        self.scanner.unsupported_extensions = new_unsupported
        
        # Rescan the current directory and update main window
        if self.scanner.current_directory:
            # Clear previous results
            for item in self.main_gui.tree.get_children():
                self.main_gui.tree.delete(item)

            # Perform scan
            issues = self.scanner.scan_directory(self.scanner.current_directory)
            
            # Update results
            for issue in issues:
                self.main_gui.tree.insert('', tk.END, values=(
                    issue['name'],
                    issue['path'],
                    issue['issue'],
                    issue['suggested_fix']
                ))

            # Update statistics in main window
            self.main_gui.total_files_label.config(
                text=f"Total Files: {self.scanner.total_files}"
            )
            self.main_gui.issues_count_label.config(
                text=f"Issues Found: {len(issues)}"
            )
            score = self.scanner.get_compliance_score()
            self.main_gui.score_label.config(
                text=f"Compliance Score: {score:.1f}%"
            )

        messagebox.showinfo(
            "Changes Applied",
            "Extension filters have been updated and results refreshed."
        )
        self.destroy()

    def cancel_changes(self):
        # Restore original extension states
        self.scanner.unsupported_extensions = self.original_unsupported.copy()
        self.destroy() 