import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class PackageManager:
    def __init__(self, platform):
        self.platform = platform.lower()

    def is_version_available(self, package_name, version):
        if self.platform in ["ubuntu", "debian"]:
            import subprocess
            try:
                result = subprocess.check_output(
                    ["apt-cache", "policy", package_name], universal_newlines=True
                )
                return version in result
            except Exception as e:
                logging.error(f"Error checking package version: {str(e)}")
                return False
        elif self.platform in ["rhel", "centos", "fedora"]:
            import subprocess
            try:
                result = subprocess.check_output(
                    ["yum", "--showduplicates", "list", package_name], universal_newlines=True
                )
                return version in result
            except Exception as e:
                logging.error(f"Error checking package version: {str(e)}")
                return False
        else:
            # For platforms where version validation is not supported
            return True  # Assume it's available

    def get_install_command(self, packages):
        if not packages:
            return "# No packages to install."

        # Prepare packages with versions etc.
        formatted_packages = self.format_packages(packages)

        if self.platform in ["ubuntu", "debian"]:
            return f"sudo apt-get update && sudo apt-get install -y {' '.join(formatted_packages)}"
        elif self.platform in ["rhel", "centos", "fedora"]:
            # RHEL/CentOS use yum or dnf
            return f"sudo yum install -y {' '.join(formatted_packages)}"
        elif self.platform == "arch":
            return f"sudo pacman -Syu {' '.join(formatted_packages)} --noconfirm"
        elif self.platform == "macos":
            # Homebrew does not support specifying versions directly
            packages_no_version = [pkg['name'] for pkg in packages]
            install_commands = [
                "# Check for Homebrew",
                "if ! command -v brew &>/dev/null; then",
                " echo \"Homebrew not found. Installing Homebrew...\"",
                ' /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                " echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> ~/.zprofile",
                " eval \"$(/opt/homebrew/bin/brew shellenv)\"",
                "fi",
                f"brew install {' '.join(packages_no_version)}"
            ]
            return "\n".join(install_commands)
        else:
            return "# Unsupported platform for package installation."

    def format_packages(self, packages):
        formatted_packages = []
        for pkg in packages:
            name = pkg.get('name', '')
            version = pkg.get('version', '')
            if version:
                if self.platform in ["ubuntu", "debian"]:
                    # APT: package=version
                    formatted_packages.append(f"{name}={version}")
                elif self.platform in ["rhel", "centos", "fedora"]:
                    # YUM/DNF: package-version
                    formatted_packages.append(f"{name}-{version}")
                elif self.platform == "arch":
                    # Pacman doesn't support specifying versions during install
                    formatted_packages.append(name)
                elif self.platform == "macos":
                    # Homebrew does not support specifying versions directly
                    formatted_packages.append(name)
                else:
                    formatted_packages.append(name)
            else:
                formatted_packages.append(name)
        return formatted_packages

    def generate_install_script(self, packages, output_file):
        # Use the appropriate shebang line based on the platform
        shebang = "#!/bin/bash\n" if self.platform != "macos" else "#!/bin/zsh\n"
        with open(output_file, "w") as f:
            f.write(shebang)
            # No package installation commands here; they will be added later

        # Make script executable for UNIX-based systems
        os.chmod(output_file, 0o755)
        logging.info(f"Install script '{output_file}' generated.")