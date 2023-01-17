import os
import glob


def clean_folder(folder: str):
        """
        Empties the output of the given folder.

        """

        if folder[-1] != '/':
            folder += '/'

        old_output_files = glob.glob(folder + '*')
        for file in old_output_files:
            if os.path.splitext(file)[1] == '.gitignore':
                continue
            print(f"Removed {file}")
            os.remove(file)
