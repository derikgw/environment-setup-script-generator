from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
)
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class AddPackageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Package")
        self.package_name = ""
        self.package_version = ""
        self.repo_url = ""
        self.download_url = ""

        layout = QVBoxLayout()

        # Package Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Package Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Package Version
        version_layout = QHBoxLayout()
        version_label = QLabel("Version (optional):")
        self.version_input = QLineEdit()
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_input)
        layout.addLayout(version_layout)

        # Custom Repository URL
        repo_layout = QHBoxLayout()
        repo_label = QLabel("Custom Repository URL (optional):")
        self.repo_input = QLineEdit()
        repo_layout.addWidget(repo_label)
        repo_layout.addWidget(self.repo_input)
        layout.addLayout(repo_layout)

        # Custom Download URL
        download_layout = QHBoxLayout()
        download_label = QLabel("Custom Download URL (optional):")
        self.download_input = QLineEdit()
        download_layout.addWidget(download_label)
        download_layout.addWidget(self.download_input)
        layout.addLayout(download_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        self.package_name = self.name_input.text().strip()
        self.package_version = self.version_input.text().strip()
        self.repo_url = self.repo_input.text().strip()
        self.download_url = self.download_input.text().strip()

        if not self.package_name:
            QMessageBox.warning(self, "Input Error", "Package name is required.")
            return

        if self.repo_url and self.download_url:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please specify either a custom repository URL or a custom download URL, not both."
            )
            return

        super().accept()

    def get_package_data(self):
        return {
            'name': self.package_name,
            'version': self.package_version,
            'repo_url': self.repo_url,
            'download_url': self.download_url
        }


class AddEnvVarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Environment Variable")
        self.variable_name = ""
        self.variable_value = ""

        layout = QVBoxLayout()

        # Variable Name
        name_layout = QHBoxLayout()
        name_label = QLabel("Variable Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Variable Value
        value_layout = QHBoxLayout()
        value_label = QLabel("Variable Value:")
        self.value_input = QLineEdit()
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.value_input)
        layout.addLayout(value_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        self.variable_name = self.name_input.text().strip()
        self.variable_value = self.value_input.text().strip()

        if not self.variable_name:
            QMessageBox.warning(self, "Input Error", "Variable name is required.")
            return

        super().accept()

    def get_env_var(self):
        return self.variable_name, self.variable_value


class AddSymlinkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Symlink")
        self.link_name = ""
        self.target_path = ""

        layout = QVBoxLayout()

        # Link Name
        link_layout = QHBoxLayout()
        link_label = QLabel("Link Name:")
        self.link_input = QLineEdit()
        link_layout.addWidget(link_label)
        link_layout.addWidget(self.link_input)
        layout.addLayout(link_layout)

        # Target Path
        target_layout = QHBoxLayout()
        target_label = QLabel("Target Path:")
        self.target_input = QLineEdit()
        target_layout.addWidget(target_label)
        target_layout.addWidget(self.target_input)
        layout.addLayout(target_layout)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        self.link_name = self.link_input.text().strip()
        self.target_path = self.target_input.text().strip()

        if not self.link_name or not self.target_path:
            QMessageBox.warning(self, "Input Error", "Both link name and target path are required.")
            return

        super().accept()

    def get_symlink(self):
        return self.link_name, self.target_path

class LoadProfileDialog(QDialog):
    def __init__(self, parent=None, profiles=None):
        super().__init__(parent)
        self.setWindowTitle("Load Profile")
        self.profiles = profiles or []

        layout = QVBoxLayout()

        # Profile Dropdown
        profile_layout = QHBoxLayout()
        profile_label = QLabel("Select Profile:")
        self.profile_dropdown = QComboBox()
        self.profile_dropdown.addItems(self.profiles)
        profile_layout.addWidget(profile_label)
        profile_layout.addWidget(self.profile_dropdown)
        layout.addLayout(profile_layout)

        # Buttons
        button_layout = QHBoxLayout()
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(load_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_selected_profile(self):
        return self.profile_dropdown.currentText()
