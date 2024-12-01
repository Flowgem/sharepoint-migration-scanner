# **SharePoint Migration Scanner**

The **SharePoint Migration Scanner** is a tool designed to analyze files and folders to ensure they meet the requirements for migration to SharePoint. It scans directories for compatibility issues, generates detailed reports, and provides actionable suggestions to resolve problems before migration.

---
![image](https://github.com/user-attachments/assets/d64eb9ed-b90d-4a01-ad43-bc6aef0b68e3)
---

## **Features**

- **Path Length Validation**  
  Checks that file and folder paths do not exceed SharePoint's maximum length (260-400 characters, depending on configuration).

- **Invalid Character Detection**  
  Identifies filenames containing prohibited characters, such as `~ " # % & * : < > ? / \ { | }`.

- **Unsupported File Types**  
  Flags files with extensions that may be restricted or unsupported in SharePoint.

- **Conflict Management**  
  Detects duplicate or conflicting file and folder names that could cause issues during migration.

- **Compatibility Score**  
  Provides a score to indicate how suitable a folder is for migration to SharePoint.

- **Detailed Reporting**  
  Displays problematic files and folders along with explanations of the issues and suggested fixes. Reports can be exported in CSV format for further analysis.

---

## **Requirements**

- **Python 3.8 or higher**  
  This project is built using Python and requires Python 3.8 or later. Ensure you have Python installed on your system before running the scanner.  
  You can download Python from the official [Python website](https://www.python.org/).

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sharepoint-scanner.git
   cd sharepoint-scanner

2. Run the application:
   ```bash
   python sharepoint_scanner.py

---

## **Usage**

1. Launch the application.
2. Select a directory to scan.
3. View the scan results in the GUI, including:
   - A detailed table of incompatible files and folders.
   - A compatibility score for the scanned directory.
4. Export the results as a CSV file for documentation or follow-up.

---

## **How the SharePoint Scanner Works**

The SharePoint Scanner scans files and folders within a selected directory and validates them against SharePoint's requirements. Specifically, it checks for:

1. **Path Length**: Ensures that file paths do not exceed SharePoint's limits, which are typically 260-400 characters depending on the version.
2. **Invalid Characters**: Detects forbidden characters in file and folder names such as `~ " # % & * : < > ? / \ { | }`.
3. **Unsupported File Types**: Flags files with extensions that are restricted or unsupported in SharePoint.
4. **Duplicate or Conflicting Names**: Identifies files or folders that may cause conflicts during migration.

The scanner provides a clear summary of issues, a compatibility score, and recommendations for fixing problems. Users can export the results as a CSV for further review.

---

## **Configuration**

You can customize the scanner's behavior by modifying the `config.json` file:
- Set the **maximum path length**.
- Define additional **invalid characters**.
- Add or remove **restricted file types**.
