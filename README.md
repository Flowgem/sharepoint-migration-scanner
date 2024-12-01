SharePoint Scanner
The SharePoint Scanner is a tool designed to analyze files and folders to ensure they meet the requirements for migration to SharePoint. It scans directories for compatibility issues, generates detailed reports, and provides actionable suggestions to resolve problems before migration.

Features
Path Length Validation
Checks that file and folder paths do not exceed SharePoint's maximum length (260-400 characters, depending on configuration).

Invalid Character Detection
Identifies filenames containing prohibited characters, such as ~ " # % & * : < > ? / \ { | }.

Unsupported File Types
Flags files with extensions that may be restricted or unsupported in SharePoint.

Conflict Management
Detects duplicate or conflicting file and folder names that could cause issues during migration.

Compatibility Score
Provides a score to indicate how suitable a folder is for migration to SharePoint.

Detailed Reporting
Displays problematic files and folders along with explanations of the issues and suggested fixes. Reports can be exported in CSV format for further analysis.

Installation
Clone the repository:

bash
Code kopiëren
git clone https://github.com/your-username/sharepoint-scanner.git
cd sharepoint-scanner
Install the required dependencies:

bash
Code kopiëren
pip install -r requirements.txt
Run the application:

bash
Code kopiëren
python sharepoint_scanner.py
Usage
Launch the application.
Select a directory to scan.
View the scan results in the GUI, including:
A detailed table of incompatible files and folders.
A compatibility score for the scanned directory.
Export the results as a CSV file for documentation or follow-up.
Configuration
You can customize the scanner's rules by modifying the configuration file (config.json), including:

Maximum path length.
List of invalid characters.
Restricted file types.
