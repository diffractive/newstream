from zipfile import ZipFile
import os
import subprocess

def get_translation_files():
    file_paths = []
    for root, directories, files in os.walk('./'):
        for filename in files:
            if 'django.po' in filename:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
    return file_paths

def main():

    file_paths = get_translation_files()

    with ZipFile('translation_files.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file)
    print('Zip file generated')

if __name__ == "__main__":
    try:
        subprocess.run(["python", "manage.py", "makemessages", "-a"])
    except:
        print('error generating po files')
    main()