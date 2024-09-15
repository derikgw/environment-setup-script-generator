from PyQt5.QtWidgets import (
    QMainWindow, QAction, QVBoxLayout, QWidget, QInputDialog, QMessageBox, QComboBox,
    QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QDialog,
    QMenu, QAbstractItemView
)
from PyQt5.QtCore import Qt
from gui.settings_dialog import AddPackageDialog, AddEnvVarDialog, AddSymlinkDialog, LoadProfileDialog
from backend.package_manager import PackageManager
from backend.script_generator import ScriptGenerator
from backend.archive_builder import ArchiveBuilder
from database.db_manager import DBManager
import os
import logging
import re

# Import for sanitizing file names
logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DBManager()  # Initialize the database manager
        # Default target platform
        self.platform = "ubuntu"
        # Data storage for packages, env vars, and symlinks
        self.packages = []
        self.env_vars = {}
        self.symlinks = []
        # Current profile name
        self.current_profile_name = "default"
        # Set up the window
        self.setWindowTitle("Environment Setup Tool")
        self.setGeometry(100, 100, 800, 600)
        # Create menu
        self._create_menu()
        # Set central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        # Add OS selection dropdown
        self.os_dropdown = QComboBox(self)
        self.os_options = ["Ubuntu", "Debian", "RHEL", "CentOS", "Fedora", "Arch", "macOS"]
        self.os_dropdown.addItems(self.os_options)
        self.os_dropdown.currentIndexChanged.connect(self._update_platform)
        layout.addWidget(self.os_dropdown)
        # Add buttons and tables for displaying/modifying profile data
        self._create_profile_tables(layout)
        central_widget.setLayout(layout)
        # Initialize the package manager based on the selected platform
        self.package_manager = PackageManager(self.platform)

    def _create_menu(self):
        menu_bar = self.menuBar()
        # File Menu
        file_menu = menu_bar.addMenu("File")
        generate_action = QAction("Generate Setup", self)
        generate_action.triggered.connect(self._generate_setup)
        file_menu.addAction(generate_action)
        save_profile_action = QAction("Save Profile", self)
        save_profile_action.triggered.connect(self.save_profile)
        file_menu.addAction(save_profile_action)
        load_profile_action = QAction("Load Profile", self)
        load_profile_action.triggered.connect(self.load_profile)
        file_menu.addAction(load_profile_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        # Settings Menu
        settings_menu = menu_bar.addMenu("Settings")
        add_package_action = QAction("Add Package", self)
        add_package_action.triggered.connect(self._add_package)
        settings_menu.addAction(add_package_action)
        add_env_var_action = QAction("Add Environment Variable", self)
        add_env_var_action.triggered.connect(self._add_env_var)
        settings_menu.addAction(add_env_var_action)
        add_symlink_action = QAction("Add Symlink", self)
        add_symlink_action.triggered.connect(self._add_symlink)
        settings_menu.addAction(add_symlink_action)
        # Help Menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

    def _create_profile_tables(self, layout):
        # Packages Table
        self.packages_table = QTableWidget(0, 4)  # Four columns: Package, Version, Repo URL, Download URL
        self.packages_table.setHorizontalHeaderLabels(["Package", "Version", "Repo URL", "Download URL"])
        self.packages_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.packages_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.packages_table.customContextMenuRequested.connect(self._package_table_context_menu)
        self.packages_table.itemChanged.connect(self._package_item_changed)
        layout.addWidget(self.packages_table)

        # Environment Variables Table
        self.env_vars_table = QTableWidget(0, 2)
        self.env_vars_table.setHorizontalHeaderLabels(["Variable", "Value"])
        self.env_vars_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.env_vars_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.env_vars_table.customContextMenuRequested.connect(self._env_var_table_context_menu)
        self.env_vars_table.itemChanged.connect(self._env_var_item_changed)
        layout.addWidget(self.env_vars_table)

        # Symlinks Table
        self.symlinks_table = QTableWidget(0, 2)
        self.symlinks_table.setHorizontalHeaderLabels(["Link", "Target"])
        self.symlinks_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.symlinks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.symlinks_table.customContextMenuRequested.connect(self._symlink_table_context_menu)
        self.symlinks_table.itemChanged.connect(self._symlink_item_changed)
        layout.addWidget(self.symlinks_table)

        # Buttons to Add Entries
        btn_layout = QHBoxLayout()
        self.add_package_btn = QPushButton("Add Package")
        self.add_package_btn.clicked.connect(self._add_package)
        btn_layout.addWidget(self.add_package_btn)
        self.add_env_var_btn = QPushButton("Add Env Var")
        self.add_env_var_btn.clicked.connect(self._add_env_var)
        btn_layout.addWidget(self.add_env_var_btn)
        self.add_symlink_btn = QPushButton("Add Symlink")
        self.add_symlink_btn.clicked.connect(self._add_symlink)
        btn_layout.addWidget(self.add_symlink_btn)
        layout.addLayout(btn_layout)

    def _package_table_context_menu(self, position):
        menu = QMenu()
        remove_action = menu.addAction("Remove")
        action = menu.exec_(self.packages_table.viewport().mapToGlobal(position))
        if action == remove_action:
            row = self.packages_table.currentRow()
            if row >= 0:
                self.packages_table.removeRow(row)
                del self.packages[row]  # Remove from data structure

    def _package_item_changed(self, item):
        row = item.row()
        col = item.column()
        if row < len(self.packages):
            name = self.packages_table.item(row, 0).text()
            version = self.packages_table.item(row, 1).text()
            repo_url = self.packages_table.item(row, 2).text() if self.packages_table.item(row, 2) else ''
            download_url = self.packages_table.item(row, 3).text() if self.packages_table.item(row, 3) else ''
            self.packages[row] = {
                'name': name,
                'version': version,
                'repo_url': repo_url,
                'download_url': download_url
            }
            logging.info(
                f"Updated package at row {row}: {name}, version: {version}, repo_url: {repo_url}, download_url: {download_url}")

    def _env_var_table_context_menu(self, position):
        menu = QMenu()
        remove_action = menu.addAction("Remove")
        action = menu.exec_(self.env_vars_table.viewport().mapToGlobal(position))
        if action == remove_action:
            row = self.env_vars_table.currentRow()
            if row >= 0:
                key = self.env_vars_table.item(row, 0).text()
                self.env_vars_table.removeRow(row)
                if key in self.env_vars:
                    del self.env_vars[key]  # Remove from data structure

    def _env_var_item_changed(self, item):
        row = item.row()
        if self.env_vars_table.item(row, 0) and self.env_vars_table.item(row, 1):
            key = self.env_vars_table.item(row, 0).text()
            value = self.env_vars_table.item(row, 1).text()
            self.env_vars[key] = value
            logging.info(f"Updated environment variable: {key}={value}")

    def _symlink_table_context_menu(self, position):
        menu = QMenu()
        remove_action = menu.addAction("Remove")
        action = menu.exec_(self.symlinks_table.viewport().mapToGlobal(position))
        if action == remove_action:
            row = self.symlinks_table.currentRow()
            if row >= 0:
                self.symlinks_table.removeRow(row)
                del self.symlinks[row]  # Remove from data structure

    def _symlink_item_changed(self, item):
        row = item.row()
        col = item.column()
        if row < len(self.symlinks):
            link = self.symlinks_table.item(row, 0).text()
            target = self.symlinks_table.item(row, 1).text()
            self.symlinks[row] = (link, target)
            logging.info(f"Updated symlink at row {row}: {link} -> {target}")

    def _update_tables(self):
        """Updates the tables to display the current profile values."""
        # Disconnect signals to prevent recursive updates
        self.packages_table.blockSignals(True)
        self.env_vars_table.blockSignals(True)
        self.symlinks_table.blockSignals(True)

        # Update Packages Table
        self.packages_table.setRowCount(0)  # Clear existing rows
        for package in self.packages:
            row_position = self.packages_table.rowCount()
            self.packages_table.insertRow(row_position)
            package_name = package['name']
            package_version = package['version']
            repo_url = package['repo_url']
            download_url = package['download_url']
            self.packages_table.setItem(row_position, 0, QTableWidgetItem(package_name))
            self.packages_table.setItem(row_position, 1, QTableWidgetItem(package_version))
            self.packages_table.setItem(row_position, 2, QTableWidgetItem(repo_url))
            self.packages_table.setItem(row_position, 3, QTableWidgetItem(download_url))

        # Update Environment Variables Table
        self.env_vars_table.setRowCount(0)  # Clear existing rows
        for var, value in self.env_vars.items():
            row_position = self.env_vars_table.rowCount()
            self.env_vars_table.insertRow(row_position)
            self.env_vars_table.setItem(row_position, 0, QTableWidgetItem(var))
            self.env_vars_table.setItem(row_position, 1, QTableWidgetItem(value))

        # Update Symlinks Table
        self.symlinks_table.setRowCount(0)  # Clear existing rows
        for link, target in self.symlinks:
            row_position = self.symlinks_table.rowCount()
            self.symlinks_table.insertRow(row_position)
            self.symlinks_table.setItem(row_position, 0, QTableWidgetItem(link))
            self.symlinks_table.setItem(row_position, 1, QTableWidgetItem(target))

        # Reconnect signals
        self.packages_table.blockSignals(False)
        self.env_vars_table.blockSignals(False)
        self.symlinks_table.blockSignals(False)

    def _add_package(self):
        dialog = AddPackageDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            package_data = dialog.get_package_data()
            self.packages.append(package_data)
            logging.info(f"Added package: {package_data}")
            self._update_tables()

    def _add_env_var(self):
        key, ok1 = QInputDialog.getText(self, "Add Environment Variable", "Enter variable name:")
        if ok1 and key:
            value, ok2 = QInputDialog.getText(self, "Add Environment Variable", f"Enter value for '{key}':")
            if ok2:
                self.env_vars[key] = value
                logging.info(f"Added environment variable: {key}={value}")
                self._update_tables()

    def _add_symlink(self):
        link, ok1 = QInputDialog.getText(self, "Add Symlink", "Enter link name:")
        if ok1 and link.strip():
            target, ok2 = QInputDialog.getText(self, "Add Symlink", f"Enter target for '{link}':")
            if ok2 and target.strip():
                self.symlinks.append((link.strip(), target.strip()))
                logging.info(f"Added symlink: {link.strip()} -> {target.strip()}")
                self._update_tables()
            else:
                QMessageBox.warning(self, "Invalid Input", "Symlink target cannot be empty.")
        else:
            QMessageBox.warning(self, "Invalid Input", "Symlink link cannot be empty.")

    def load_profile(self):
        profiles = self.db_manager.get_all_profiles()
        dialog = LoadProfileDialog(self, profiles)
        if dialog.exec_() == QDialog.Accepted:
            profile_name = dialog.get_selected_profile()
            try:
                profile_data = self.db_manager.load_profile(profile_name)
                if profile_data:
                    self.platform = profile_data['os']
                    self.packages = profile_data['packages']
                    self.env_vars = profile_data['env_vars']
                    self.symlinks = profile_data['symlinks']
                    # Update UI elements to reflect the loaded data
                    self._update_tables()
                    QMessageBox.information(self, "Profile Loaded", f"Profile '{profile_name}' loaded successfully!")
                    logging.info(f"Profile '{profile_name}' loaded and UI updated.")
                else:
                    QMessageBox.warning(self, "Load Failed", f"Profile '{profile_name}' not found.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while loading the profile: {str(e)}")
                logging.error(f"Error loading profile '{profile_name}': {str(e)}")

    def save_profile(self):
        """Save the current profile."""
        profile_name, ok = QInputDialog.getText(self, "Save Profile", "Enter profile name:")
        if ok and profile_name:
            try:
                # Gather the necessary data to save the profile
                os_name = self.platform
                packages = self.packages
                env_vars = self.env_vars
                symlinks = self.symlinks

                # Call db_manager to save the profile
                success = self.db_manager.save_profile(
                    profile_name, os_name, packages, env_vars, symlinks
                )
                if success:
                    QMessageBox.information(self, "Profile Saved", f"Profile '{profile_name}' saved successfully!")
                    logging.info(f"Profile '{profile_name}' saved.")
                else:
                    QMessageBox.warning(self, "Save Failed", "Failed to save the profile.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while saving the profile: {str(e)}")
                logging.error(f"Error saving profile '{profile_name}': {str(e)}")

    def _update_platform(self):
        selected_os = self.os_dropdown.currentText()
        self.platform = selected_os.lower()
        logging.info(f"Platform set to: {self.platform}")
        # Re-initialize the package manager when the platform changes
        self.package_manager = PackageManager(self.platform)

    def _generate_setup(self):
        if not self.packages and not self.env_vars and not self.symlinks:
            QMessageBox.warning(self, "No Configuration", "No packages, environment variables, or symlinks added.")
            return
        try:
            # Initialize the package manager and script generator based on selected platform
            package_manager = PackageManager(self.platform)
            script_generator = ScriptGenerator(package_manager, self.symlinks, self.env_vars)
            # Create output directory if it doesn't exist
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            # Clean up the output directory
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    logging.info(f"Removed old file '{file_path}' from output directory.")
                except Exception as e:
                    logging.error(f"Error removing file '{file_path}': {str(e)}")
            # Generate the install script
            script_name = "install.sh" if self.platform != "macos" else "install.command"
            script_path = os.path.join(output_dir, script_name)
            script_generator.generate_script(self.packages, script_path)
            # Create the archive with the generated files
            archive_builder = ArchiveBuilder(output_dir)
            # Sanitize profile name and OS for file name
            safe_profile_name = re.sub(r'[^\w\-]', '_', self.current_profile_name)
            safe_os_name = re.sub(r'[^\w\-]', '_', self.platform)
            archive_name = f"{safe_profile_name}_{safe_os_name}_environment_setup.zip"
            # Archive will be created in the current directory
            archive_builder.create_archive(archive_name)
            QMessageBox.information(self, "Setup Generated", f"Setup generated and archived at {archive_name}")
            logging.info(f"Setup script and archive generated at {archive_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during setup generation: {str(e)}")
            logging.error(f"Error during setup generation: {str(e)}")
