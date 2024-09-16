from database.models import Profile, SessionLocal, initialize_database
import logging

logging.basicConfig(level=logging.INFO)

class DBManager:
    def __init__(self):
        # Initialize the database and create tables if they don't exist
        initialize_database()
        self.session = SessionLocal()

    def save_profile(self, profile_name, os_name, packages, env_vars, symlinks, custom_commands):
        try:
            packages_str = ",".join([f"{pkg['name']}:{pkg['version']}:{pkg['repo_url']}:{pkg['download_url']}" for pkg in packages])
            custom_commands_str = ",".join([f"{cmd['description']}:{cmd['command']}" for cmd in custom_commands])
            existing_profile = self.session.query(Profile).filter_by(profile_name=profile_name).first()
            if existing_profile:
                existing_profile.os = os_name
                existing_profile.packages = packages_str
                existing_profile.environment_variables = ",".join([f"{k}={v}" for k, v in env_vars.items()])
                existing_profile.symlinks = ",".join([f"{link}:{target}" for link, target in symlinks])
                existing_profile.custom_commands = custom_commands_str
            else:
                new_profile = Profile(
                    profile_name=profile_name,
                    os=os_name,
                    packages=packages_str,
                    environment_variables=",".join([f"{k}={v}" for k, v in env_vars.items()]),
                    symlinks=",".join([f"{link}:{target}" for link, target in symlinks]),
                    custom_commands=custom_commands_str
                )
                self.session.add(new_profile)
            self.session.commit()
            logging.info(f"Profile '{profile_name}' saved to database.")
            return True
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error saving profile '{profile_name}': {str(e)}")
            raise e

    def load_profile(self, profile_name):
        try:
            profile = self.session.query(Profile).filter_by(profile_name=profile_name).first()
            if profile:
                packages = [
                    dict(zip(['name', 'version', 'repo_url', 'download_url'], pkg.split(':'))) for pkg in profile.packages.strip().split(',')
                ]
                env_vars = {}
                if profile.environment_variables:
                    env_vars = dict(var.split('=', 1) for var in profile.environment_variables.split(','))
                symlinks = []
                if profile.symlinks:
                    symlinks = [tuple(link.split(':', 1)) for link in profile.symlinks.split(',')]
                custom_commands = []
                if profile.custom_commands:
                    custom_commands = [dict(zip(['description', 'command'], cmd.split(':', 1))) for cmd in profile.custom_commands.split(',')]

                logging.info(f"Profile '{profile_name}' loaded from database.")
                return {
                    'os': profile.os,
                    'packages': packages,
                    'env_vars': env_vars,
                    'symlinks': symlinks,
                    'custom_commands': custom_commands
                }
            else:
                logging.warning(f"Profile '{profile_name}' not found in database.")
                return None
        except Exception as e:
            logging.error(f"Error loading profile '{profile_name}': {str(e)}")
            raise e

    def get_all_profiles(self):
        try:
            profiles = self.session.query(Profile).all()
            profile_names = [profile.profile_name for profile in profiles]
            logging.info("Retrieved all profile names from database.")
            return profile_names
        except Exception as e:
            logging.error(f"Error retrieving profiles: {str(e)}")
            raise e