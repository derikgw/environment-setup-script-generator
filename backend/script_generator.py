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

    def generate_script(self, packages, output_path):
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

            # Environment Variables
            if self.env_vars:
                script_lines.append('echo "Setting environment variables..."\n')
                shell_config_file = self._get_shell_config_file()
                for key, value in self.env_vars.items():
                    script_lines.append(f'export {key}="{value["value"]}"\n')
                    if value["append"]:
                        script_lines.append(f'echo \'export {key}="{value["value"]}"\' >> {shell_config_file}\n')
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

    def _get_shell_config_file(self):
        if self.package_manager.platform in ["ubuntu", "debian", "rhel", "centos", "fedora", "arch"]:
            return "~/.bashrc"
        elif self.package_manager.platform == "macos":
            return "~/.zshrc"
        else:
            return "~/.bashrc"