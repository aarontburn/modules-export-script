'''
Author: 
    aarontburn (https://github.com/aarontburn)
Title:
    Module Export Script
Purpose:
    Properly export developed module to use with parent application
        (https://github.com/aarontburn/modules)

Repository: 
    https://github.com/aarontburn/modules-export-script
    
Usage: 
    'npm run export', or 'python node_modules/modules-export-script/EXPORT.py'
    
Expected Result: 
    In the root directory, a directory 'output/' will be created containing required files for the module.
'''

import os
import pathlib
import shutil
import json
import time

'''The path of the root directory of this module.'''
PWD: str = str(pathlib.Path(__file__).parent.parent.parent.resolve())

def locateModule() -> str:
    '''
    Scans "src" folder for a directory containing "ref.DAT", which should
    be located in the module directory.
    
    Returns the name of the directory.
    '''
    src_path: str = PWD + "/src/"
    for file in os.listdir(src_path):
        file_path = src_path + file
        if os.path.isdir(file_path) and os.listdir(file_path).count("ref.DAT") > 0:
            return file

'''The name of the directory containing the module to export.'''
FOLDER_NAME: str = locateModule()

'''The path of the output directory in the output folder.'''
OUTPUT_FOLDER_PATH: str = PWD + "/output/" + FOLDER_NAME + "/"

'''The path to the node_modules directory in the output folder.'''
NODE_MODULES_PATH: str = PWD + "/node_modules"


def main() -> None:
    ''' Entry point. '''
    shutil.rmtree(OUTPUT_FOLDER_PATH, ignore_errors=True)
    
    createDirectories()
    copyFiles()
    checkAndCopyDependencies()
    print("\n\tFINISHED BUNDLING MODULE\n")
    


def createDirectories() -> None:
    '''Creates folders required for the export.'''
    
    def mkdir(directoryName: str) -> None:
        '''Helper function to create directories.'''
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
    '''Copies files into the output folder.'''
    
    print("\n\tCOPYING FILES\n")
    path: str = PWD + "/src/" + FOLDER_NAME + "/"

    for file in os.listdir(path):
        full_file_path = path + file
        output_file_path = OUTPUT_FOLDER_PATH + file
        
        if (os.path.isfile(full_file_path)):
            print("Copying '" + full_file_path + "' to output folder ('" + output_file_path + "')")
            shutil.copyfile(full_file_path, output_file_path)


def checkAndCopyDependencies() -> None:
    '''Checks the dependencies and bundles them with output folder.'''
    
    file_text: str = ''
    with open("package.json", "r") as file:
        file_text = file.read()

    if file_text == '':
        print("Could not open package.json")
        return

    package_json: any = json.loads(file_text)
    dependencies: any = package_json['dependencies']

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