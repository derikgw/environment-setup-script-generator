# Environment Setup Tool

The Environment Setup Tool is a GUI-based application designed to generate installation scripts for various operating systems (OSs) using user-inputted data such as packages, download URLs, environment variables, symlinks, and custom commands. This tool supports saving and loading profiles to streamline the setup of environments.

## Features

- **Package Management**: Add, edit, and remove packages with versions, repository URLs, and direct download URLs.
- **Environment Variables**: Configure environment variables to be set or appended during setup, and ensure they are appropriately updated if they already exist in the shell configuration file.
- **Symlinks**: Create symbolic links from one location to another.
- **Custom Commands**: Add custom commands like `chmod`, copying files, etc.
- **Profile Management**: Save profiles with all configurations and load them as needed.
- **OS Selection**: Supports multiple operating systems, adjusting commands appropriately for each.
- **Script Generation**: Generate shell scripts that can be used to set up environments based on the given configurations, including intelligent handling of environment variables in shell configuration files.

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/environment-setup-tool.git
    cd environment-setup-tool
    ```

2. **Set Up the Virtual Environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3. **Install Requirements**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Initialize the Database**:
    ```sh
    python -c "from database.models import initialize_database; initialize_database()"
    ```

## Usage

1. **Run the Application**:
    ```sh
    python app.py
    ```

2. **Add Packages**:
    - Click the "Add Package" button to add a new package.
    - Fill in the Package Name, Version (optional), Repository URL (optional), and Download URL (optional).
    - Click "Add" to save the package.

3. **Add Environment Variables**:
    - Click the "Add Env Var" button to add a new environment variable.
    - Enter the variable name and value.
    - Specify if the variable should be appended to existing values.
    - Click "Add" to save the environment variable.

4. **Add Symlinks**:
    - Click the "Add Symlink" button to add a new symlink.
    - Enter the link name and target path.
    - Click "Add" to save the symlink.

5. **Add Custom Commands**:
    - Click the "Add Command" button to add a custom command.
    - Enter the command description and the command itself.
    - Click "Add" to save the command.

6. **Save Profile**:
    - Click the "File" menu and select "Save Profile".
    - Choose an existing profile to overwrite or enter a new profile name.
    - Click "OK" to save the profile.

7. **Load Profile**:
    - Click the "File" menu and select "Load Profile".
    - Choose a profile from the dropdown list and click "OK" to load it.
    - The configuration will be populated with the loaded profile's data.

8. **Generate Setup Script**:
    - Configure the packages, environment variables, symlinks, custom commands, and OS selection.
    - Click the "File" menu and select "Generate Setup".
    - A script will be generated in the `output` directory along with an archive containing the script.

## Directory Structure

```plaintext
environment-setup-tool/
├── app.py
├── database/
│   ├── models.py
│   └── db_manager.py
├── backend/
│   ├── package_manager.py
│   ├── script_generator.py
│   ├── archive_builder.py
├── gui/
│   ├── main_window.py
│   ├── settings_dialog.py
├── output/
├── README.md
└── requirements.txt
```

## Code Structure

### Main Window (`main_window.py`)

The `MainWindow` class is the main GUI window that handles all user interactions, such as adding packages, environment variables, symlinks, custom commands, and managing profiles.

- **Menus**: File, Settings, Help menus for various actions.
- **Tables**: Display lists of packages, environment variables, symlinks, and custom commands.
- **Buttons**: Add buttons for each type of configuration.

### Dialogs (`settings_dialog.py`)

Contains dialogs for adding packages (`AddPackageDialog`), environment variables (`AddEnvVarDialog`), symlinks (`AddSymlinkDialog`), custom commands (`AddCommandDialog`), and loading profiles (`LoadProfileDialog`).

### Database Models and Management (`models.py`, `db_manager.py`)

Defines the database schema and handles database operations for saving and loading profiles.

### Backend Logic (`package_manager.py`, `script_generator.py`, `archive_builder.py`)

Handles logic for managing packages and generating setup scripts including creating archives of the generated files.

**New Features and Enhancements**:
1. **Intelligent Environment Variable Handling**: The generated setup script now includes logic to check if an environment variable already exists in the shell configuration file and either updates its value or appends it if it doesn't exist.
2. **Improved Script Generation Process**: Integrated more robust mechanisms for environment variable management within the generated shell scripts to provide better control and avoid duplications.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Derik Wilson - [GitHub Profile](https://github.com/derikgw)
