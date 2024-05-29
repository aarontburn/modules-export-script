/*
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
    'npm run export', or 'node node_modules/modules-export-script/export.js'
    
Expected Result: 
    In the root directory, a directory 'output/' will be created containing required files for the module.
*/





const path = require("path");
const fs = require("fs");

// File name of the info file for the module.
const MODULE_INFO_FILE = "moduleinfo.json";

// The path of the root directory of this module.
const PWD = path.join(__dirname, "../", "../");

const FOLDER_NAME = (() => {
    const srcPath = path.join(PWD, "src");
    for (const file of fs.readdirSync(srcPath, { withFileTypes: true })) {
        if (file.isDirectory() && fs.readdirSync(path.join(file.path, file.name)).includes(MODULE_INFO_FILE)) {
            return file.name;
        }
    }
})();

if (FOLDER_NAME === undefined) {
    throw new Error(`Could not locate '${MODULE_INFO_FILE}'. Ensure your module folder contains it.`);
}

// The path of the output directory in the output folder
const OUTPUT_FOLDER_PATH = PWD + "/output/" + FOLDER_NAME + "/";

// The path to the node_modules directory in the output folder.
const NODE_MODULES_PATH = PWD + "/node_modules";


function main() {
    fs.rmSync(OUTPUT_FOLDER_PATH, { recursive: true, force: true });
    modifyModuleInfoJSON();
    createDirectories();
    copyFiles();
    checkAndCopyDependencies();

    console.log("\n\tFINISHING BUNDLING MODULE");
}

function modifyModuleInfoJSON() {
    const jsonPath = PWD + "/src/" + FOLDER_NAME + "/" + MODULE_INFO_FILE;
    const json = JSON.parse(fs.readFileSync(jsonPath));
    json["build_version"] += 1
    fs.writeFileSync(jsonPath, JSON.stringify(json));
}

function createDirectories() {
    function mkdir(directoryName) {
        fs.mkdirSync(directoryName, { recursive: true })
    }

    console.log("\n\tCREATING FOLDERS\n");
    mkdir(OUTPUT_FOLDER_PATH);
    mkdir(OUTPUT_FOLDER_PATH + "module_builder");
    mkdir(OUTPUT_FOLDER_PATH + "node_modules");
}

function copyFiles() {
    console.log("\n\tCOPYING FILES\n");

    const dir = PWD + "/src/" + FOLDER_NAME + "/";
    for (const file of fs.readdirSync(dir, { withFileTypes: true })) {
        if (file.isDirectory() && file.name === "module_builder") {
            continue;
        }

        console.log(`Copying '${path.join(file.path, file.name)}' to output folder (${path.join(OUTPUT_FOLDER_PATH, file.name)})`);
        fs.cpSync(path.join(file.path, file.name), path.join(OUTPUT_FOLDER_PATH, file.name), { recursive: true });
    }
}

function checkAndCopyDependencies() {
    const json = JSON.parse(fs.readFileSync(PWD + "/package.json"));

    const dependencies = json["dependencies"];

    const dependencyNames = Object.keys(dependencies);
    if (dependencyNames.length > 1) {
        console.log("\n\tBUNDLING DEPENDENCIES\n");
    }

    const nodeModules = fs.readdirSync(NODE_MODULES_PATH);

    for (const dependencyName of dependencyNames) {
        if (dependencyName === "modules-export-script") {
            continue
        }

        if (!nodeModules.includes(dependencyName)) {
            console.log(dependencyName + " was not found in 'node_modules'. Skipping...")
            continue;
        }
        const dependencyPath = path.join(NODE_MODULES_PATH, dependencyName);
        console.log("Copying '" + dependencyPath + "' to '" + OUTPUT_FOLDER_PATH + "node_modules/'")
        fs.cpSync(dependencyPath, path.join(OUTPUT_FOLDER_PATH, "node_modules/" + dependencyName), { recursive: true });

    }

}

main();