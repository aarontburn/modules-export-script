import os
import pathlib
import shutil
import json
import time

# Author: aarontburn
# Module Exporter

"""
Usage Information:
Change this to the name of folder containing your module
"""
FOLDER_NAME: str = 'sample_module' # Change this to the name of folder containing your module

# This ugly line is to get to the root directory of a project from node_modules folder.
PWD: str = str(pathlib.Path(__file__).parent.parent.parent.resolve())
OUTPUT_FOLDER_PATH: str = PWD + "/output/" + FOLDER_NAME + "/"
NODE_MODULES_PATH: str = PWD + "/node_modules"

def main() -> None:
    shutil.rmtree(OUTPUT_FOLDER_PATH, ignore_errors=True)
    
    createDirectories()
    copyFiles()
    checkAndCopyDependencies()
    print("\n\tFINISHED BUNDLING MODULE\n")
    


def createDirectories() -> None:
    def mkdir(directoryName: str) -> None:
        try:
            os.makedirs(directoryName)
            print("Creating folder: " + directoryName)
        except FileExistsError:
            print("Removing existing directory: " + directoryName)
        
    print("\n\tCREATING FOLDERS\n")
    mkdir(OUTPUT_FOLDER_PATH)
    mkdir(OUTPUT_FOLDER_PATH + "module_builder")
    mkdir(OUTPUT_FOLDER_PATH + "node_modules")


def copyFiles() -> None:
    # Step 2: Copy all files from module folder into output folder
    print("\n\tCOPYING FILES\n")
    # Path of current file
    path: str = PWD + "/src/" + FOLDER_NAME+ "/"

    for file in os.listdir(path):
        full_file_path = path + file
        output_file_path = OUTPUT_FOLDER_PATH + file
        
        if (os.path.isfile(full_file_path)):
            print("Copying '" + full_file_path + "' to output folder ('" + output_file_path + "')")
            shutil.copyfile(full_file_path, output_file_path)


def checkAndCopyDependencies() -> None:
    # Step 3: Parse package.json for dependencies
    file_text: str = ''
    with open("package.json", "r") as file:
        file_text = file.read()

    if file_text == '':
        print("Could not open package.json")
        return

    package_json: any = json.loads(file_text)
    dependencies = package_json['dependencies']

    if (len(dependencies.keys()) > 0):
        print("\n\tBUNDLING DEPENDENCIES\n")


    node_modules: list[str] = os.listdir(NODE_MODULES_PATH)
    for dependency_name in dependencies.keys():
        # version = dependencies[dependency]
        try:
            node_modules.index(dependency_name)
        except ValueError:
            print(dependency_name + " was not found in node_modules. Skipping...")
            continue
        dependency_path: str = NODE_MODULES_PATH + "/" + dependency_name
        try:
            print("Copying '" + dependency_path + "' to '" + OUTPUT_FOLDER_PATH + "node_modules/'")
            shutil.copytree(dependency_path, OUTPUT_FOLDER_PATH + "node_modules/" + dependency_name)
        except FileExistsError:
            print("Replacing existing dependency from '" + dependency_path + "' to '" + OUTPUT_FOLDER_PATH + "node_modules/'")
            shutil.rmtree(OUTPUT_FOLDER_PATH + "node_modules/" + dependency_name)
            time.sleep(0.1) # Add small delay
            shutil.copytree(dependency_path, OUTPUT_FOLDER_PATH + "node_modules/" + dependency_name)  
        
    
if __name__ == "__main__":
    main()