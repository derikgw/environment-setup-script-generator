import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class ScriptGenerator:
    def __init__(self, package_manager, symlinks, env_vars, custom_commands):
        self.package_manager = package_manager
        self.symlinks = symlinks
        self.env_vars = env_vars
        self.custom_commands = custom_commands

    def generate_script(self, packages, output_path, app_install_path=None, overwrite=False, backup=False):
        try:
            script_lines = []

            # Shebang
            script_lines.append("#!/bin/bash\n")

            # Enable error handling
            script_lines.append("# Exit immediately if a command exits with a non-zero status\n")
            script_lines.append("set -e\n")

            # Trap errors and handle them
            script_lines.append("trap 'echo \"An error occurred. Exiting...\"; exit 1;' ERR\n")

            # User Feedback
            script_lines.append('echo "Starting environment setup..."\n')

            if app_install_path:
                script_lines.extend(self._generate_app_check_logic(app_install_path, overwrite, backup))

            shell_config_file = self._get_shell_config_file()

            # Environment Variables
            if self.env_vars:
                script_lines.append('echo "Setting environment variables..."\n')
                for key, value in self.env_vars.items():
                    if key == "PATH":
                        script_lines.append(f'if grep -q "export PATH=" {shell_config_file}; then\n')
                        script_lines.append(
                            f'  sed -i \'\' -e \'s|export PATH=.*$|export PATH="{value["value"]}:$PATH"|\' {shell_config_file}\n')
                        script_lines.append(f'  echo "Updated PATH in {shell_config_file}"\n')
                        script_lines.append('else\n')
                        script_lines.append(f'  echo \'export PATH="{value["value"]}:$PATH"\' >> {shell_config_file}\n')
                        script_lines.append(f'  echo "Added PATH to {shell_config_file}"\n')
                        script_lines.append('fi\n')
                    else:
                        script_lines.append(f'if grep -q "export {key}=" {shell_config_file}; then\n')
                        script_lines.append(
                            f'  sed -i \'\' -e \'s|export {key}=.*$|export {key}="{value["value"]}"|\' {shell_config_file}\n')
                        script_lines.append(f'  echo "Updated {key} in {shell_config_file}"\n')
                        script_lines.append('else\n')
                        script_lines.append(f'  echo \'export {key}="{value["value"]}"\' >> {shell_config_file}\n')
                        script_lines.append(f'  echo "Added {key} to {shell_config_file}"\n')
                        script_lines.append('fi\n')
                script_lines.append('echo "Environment variables set."\n')

            # Symlink Creation
            if self.symlinks:
                script_lines.append('echo "Creating symlinks..."\n')
                for link, target in self.symlinks:
                    # Ensure directories exist
                    script_lines.append(f'mkdir -p "$(dirname \\"{link}\\")"\n')
                    script_lines.append(f'ln -sf "{target}" "{link}"\n')
                script_lines.append('echo "Symlinks created."\n')

            # Package Installation
            if packages:
                script_lines.append('echo "Installing packages..."\n')
                install_command = self.package_manager.get_install_command(packages)

                # Wrap the install command to check for application existence
                for package in packages:
                    if package == 'intellij-idea':  # Example specific to IntelliJ IDEA
                        install_command = f'''if [ -d "{app_install_path}" ]; then
  read -p "It seems there is already an App at '{app_install_path}'. Do you want to overwrite it? (y/n) " choice
  case "$choice" in
    y|Y )
      echo "Overwriting the existing app..."
      rm -rf "{app_install_path}"
      {install_command}
      ;;
    n|N )
      echo "Installation aborted."
      exit 1
      ;;
    * )
      echo "Invalid choice. Installation aborted."
      exit 1
      ;;
  esac
else
  {install_command}
fi
'''
                        break

                script_lines.append(install_command + "\n")
                script_lines.append('echo "Packages installed."\n')

            # Custom Commands
            if self.custom_commands:
                script_lines.append('echo "Executing custom commands..."\n')
                for command in self.custom_commands:
                    cmd = command['command']
                    script_lines.append(cmd + "\n")
                script_lines.append('echo "Custom commands executed."\n')

            # Completion message
            script_lines.append('echo "Environment setup completed successfully."\n')

            # Write the script to the output path
            with open(output_path, 'w') as script_file:
                script_file.writelines(script_lines)

            logging.info(f"Install script generated at {output_path}")

            # Make the script executable
            os.chmod(output_path, 0o755)
        except Exception as e:
            logging.error(f"Error generating script: {str(e)}")
            raise e

    def _generate_app_check_logic(self, app_install_path, overwrite, backup):
        script_lines = []

        script_lines.append(f'APP_PATH="{app_install_path}"\n')

        if overwrite:
            script_lines += [
                'if [ -d "$APP_PATH" ]; then\n',
                '  read -p "It seems there is already an App at \'$APP_PATH\'. Do you want to overwrite it? (y/n) " choice\n',
                '  case "$choice" in\n',
                '    y|Y )\n',
                '      echo "Overwriting the existing app...";\n',
                '      rm -rf "$APP_PATH";\n',
                '      ;;\n',
                '    n|N )\n',
                '      echo "Installation aborted.";\n',
                '      exit 1;\n',
                '      ;;\n',
                '    * )\n',
                '      echo "Invalid choice. Installation aborted.";\n',
                '      exit 1;\n',
                '      ;;\n',
                '  esac\n',
                'fi\n'
            ]
        elif backup:
            script_lines += [
                'if [ -d "$APP_PATH" ]; then\n',
                '  BACKUP_PATH="${APP_PATH} Backup";\n',
                '  echo "Backing up the existing app...";\n',
                '  mv "$APP_PATH" "$BACKUP_PATH";\n',
                'fi\n'
            ]
        else:
            script_lines += [
                'if [ -d "$APP_PATH" ]; then\n',
                '  echo "Error: It seems there is already an App at \'$APP_PATH\'. Installation aborted.";\n',
                '  exit 1;\n',
                'fi\n'
            ]

        return script_lines

    def _get_shell_config_file(self):
        if self.package_manager.platform in ["ubuntu", "debian", "rhel", "centos", "fedora", "arch"]:
            return "~/.bashrc"
        elif self.package_manager.platform == "macos":
            return "~/.zshrc"
        else:
            return "~/.bashrc"


