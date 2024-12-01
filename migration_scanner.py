import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from scanner import SharePointScanner
from gui import ScannerGUI

def main():
    root = tk.Tk()
    root.title("SharePoint Migration Scanner")
    root.geometry("1024x768")
    root.configure(bg='#f0f0f0')
    
    # Make the window resizable
    root.minsize(800, 600)
    
    scanner = SharePointScanner()
    app = ScannerGUI(root, scanner)
    
    # Bind the extension filter update to recalculate scores
    app.bind_extension_updates()
    
    root.mainloop()

if __name__ == "__main__":
    main() 