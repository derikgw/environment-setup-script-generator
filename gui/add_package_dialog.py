# Add imports
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

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
            QMessageBox.warning(self, "Input Error", "Please specify either a custom repository URL or a custom download URL, not both.")
            return

        super().accept()

    def get_package_data(self):
        return {
            'name': self.package_name,
            'version': self.package_version,
            'repo_url': self.repo_url,
            'download_url': self.download_url
        }
