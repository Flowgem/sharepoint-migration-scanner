import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set

class SharePointScanner:
    MAX_PATH_LENGTH = 260
    INVALID_CHARS = r'[~"#%&*:<>?/\\{|}]'
    
    # Updated set of unsupported extensions (potentially dangerous files)
    DEFAULT_UNSUPPORTED = {
        '.exe',  # Executable files
        '.bat',  # Batch files
        '.cmd',  # Command files
        '.dll',  # Dynamic Link Libraries
        '.vbs'   # Visual Basic Scripts
    }

    def __init__(self):
        self.issues = []
        self.total_files = 0
        self.compliant_files = 0
        self.unsupported_extensions = self.DEFAULT_UNSUPPORTED.copy()
        self.found_extensions = set()  # Track extensions found in scanned directory
        self.current_directory = None  # Track current directory being scanned

    def add_unsupported_extension(self, extension: str) -> None:
        """Add a single extension to the unsupported list"""
        if not extension.startswith('.'):
            extension = f'.{extension}'
        self.unsupported_extensions.add(extension.lower())

    def add_unsupported_extensions(self, extensions: List[str]) -> None:
        """Add multiple extensions to the unsupported list"""
        for ext in extensions:
            self.add_unsupported_extension(ext)

    def remove_unsupported_extension(self, extension: str) -> None:
        """Remove a single extension from the unsupported list"""
        if not extension.startswith('.'):
            extension = f'.{extension}'
        self.unsupported_extensions.discard(extension.lower())

    def reset_unsupported_extensions(self) -> None:
        """Reset to default unsupported extensions"""
        self.unsupported_extensions = self.DEFAULT_UNSUPPORTED.copy()

    def get_unsupported_extensions(self) -> Set[str]:
        """Get the current set of unsupported extensions"""
        return self.unsupported_extensions.copy()

    def scan_directory(self, directory: str) -> List[Dict]:
        self.issues = []
        self.total_files = 0
        self.compliant_files = 0
        self.found_extensions = set()
        self.current_directory = directory
        
        print(f"Starting scan of directory: {directory}")
        
        # First pass: collect all extensions
        print("Starting first pass - collecting extensions...")
        for root, dirs, files in os.walk(directory):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext:  # Only add if extension exists
                    self.found_extensions.add(ext)
                    print(f"Found file: {file} with extension: {ext}")
        
        print(f"First pass complete. Found extensions: {sorted(self.found_extensions)}")
        print(f"Total unique extensions found: {len(self.found_extensions)}")
        
        # Second pass: check for issues and count files
        print("Starting second pass - checking for issues...")
        for root, dirs, files in os.walk(directory):
            for file in files:
                self.total_files += 1
                full_path = os.path.join(root, file)
                self._check_item(full_path, False)
            
            # Check directory names
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                self._check_item(dir_path, True)
        
        print(f"Scan complete. Total files: {self.total_files}, Issues found: {len(self.issues)}")
        print(f"Compliant files: {self.compliant_files}")
        return self.issues

    def _check_item(self, path: str, is_dir: bool) -> None:
        issues_found = []
        
        # Check path length
        path_length = len(path)
        if path_length > self.MAX_PATH_LENGTH:
            excess_length = path_length - self.MAX_PATH_LENGTH
            issues_found.append(f"Path exceeds 260 characters (by {excess_length} characters)")

        # Check invalid characters
        name = os.path.basename(path)
        if re.search(self.INVALID_CHARS, name):
            issues_found.append("Contains invalid characters")

        # Check file extension for files only
        if not is_dir:
            ext = os.path.splitext(path)[1].lower()
            if ext in self.unsupported_extensions:
                issues_found.append(f"Unsupported file type ({ext})")

        # Only add to issues list if there are actual issues
        if issues_found:
            self.issues.append({
                'name': os.path.basename(path),
                'path': path,
                'issue': '; '.join(issues_found),
                'suggested_fix': self._suggest_fix(issues_found, name, path_length)
            })

        # Update compliant files count
        if not is_dir:  # Only count files, not directories
            if not issues_found:  # If no issues were found
                self.compliant_files += 1

    def _suggest_fix(self, issues: List[str], name: str, path_length: int = 0) -> str:
        fixes = []
        
        if any("Path exceeds" in issue for issue in issues):
            excess = path_length - self.MAX_PATH_LENGTH
            fixes.append(f"Move to a shorter path (need to reduce by at least {excess} characters)")
            
        if "Contains invalid characters" in issues:
            fixed_name = re.sub(self.INVALID_CHARS, '_', name)
            fixes.append(f"Rename to: {fixed_name}")
            
        if any("Unsupported file type" in issue for issue in issues):
            fixes.append("Convert to supported format or exclude from migration")
            
        return '; '.join(fixes)

    def get_compliance_score(self) -> float:
        """Calculate compliance score based on migratable files"""
        if self.total_files == 0:
            return 100.0
        
        # Calculate percentage of compliant files
        score = (self.compliant_files / self.total_files) * 100
        
        # Ensure score doesn't exceed 100%
        return min(100.0, score)

    def get_found_extensions(self) -> Set[str]:
        """Get the set of extensions found in the last scanned directory"""
        print(f"get_found_extensions called. Current extensions: {sorted(self.found_extensions)}")
        if not self.found_extensions:
            print("WARNING: found_extensions set is empty!")
        return self.found_extensions.copy()

    def get_current_directory(self) -> str:
        """Get the currently scanned directory"""
        return self.current_directory

    def get_filtered_issues(self):
        """Return issues filtered by current unsupported extensions"""
        if not self.issues:
            return []
        
        filtered_issues = []
        for issue in self.issues:
            file_path = issue['path']
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Only include issues for files with unsupported extensions
            if file_ext in self.unsupported_extensions:
                filtered_issues.append(issue)
                
        return filtered_issues