import shutil
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class ArchiveBuilder:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir

    def create_archive(self, archive_name="environment_setup.zip"):
        try:
            base_name = os.path.splitext(archive_name)[0]
            # Create the archive outside the output directory
            shutil.make_archive(base_name, 'zip', self.output_dir)
            logging.info(f"Archive '{archive_name}' created successfully.")
        except Exception as e:
            logging.error(f"Error creating archive '{archive_name}': {str(e)}")
            raise e

    def add_file_to_output(self, file_path):
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            # Check if the file is already in the output directory
            dest_path = os.path.join(self.output_dir, os.path.basename(file_path))
            if os.path.abspath(file_path) != os.path.abspath(dest_path):
                shutil.copy(file_path, dest_path)
                logging.info(f"File '{file_path}' copied to '{self.output_dir}'.")
            else:
                logging.info(f"File '{file_path}' is already in '{self.output_dir}'. Skipping copy.")
        except Exception as e:
            logging.error(f"Error adding file '{file_path}' to output: {str(e)}")
            raise e
