import os
import commands
import wnsrc


projectName = "PyWNS--main--1.0"

sandboxPath = ARGUMENTS.get('sandboxDir', wnsrc.pathToSandbox)
if sandboxPath == "":
    sandboxPath = wnsrc.pathToSandbox

sandboxSrcSubDir = os.path.join("default", "lib", "python2.4", "site-packages", "pywns")
sourceDir = "pywns"

srcTargetPath = os.path.join(sandboxPath, sandboxSrcSubDir)
docTargetPath = os.path.join(sandboxPath, "default", "doc", projectName)

def filterFiles(files, extension):
    return [filename for filename in files if os.path.isfile(filename) and filename.endswith(extension)]

def addSrcInstallTarget(root, files):
    if ".arch-ids" not in root:
        subTargetPath = os.path.join(srcTargetPath, *root.split("/")[1:])
        pythonFiles = filterFiles([os.path.join(root, filename) for filename in files], ".py")
        Install(subTargetPath, pythonFiles)

pythonFileList = []
for root, dirs, files in os.walk(sourceDir):
    addSrcInstallTarget(root, files)
    pythonFileList += filterFiles([os.path.join(root, filename) for filename in files], ".py")

doxyCommand = Command("doxydoc/html/index.htm", ["config/Doxyfile"] + pythonFileList, "doxygen config/Doxyfile")

if os.path.exists("doxydoc/html"):
    Install(docTargetPath, [os.path.join("doxydoc/html", filename) for filename in os.listdir("doxydoc/html")])

Alias("install-python", srcTargetPath)
Alias("docu", doxyCommand)
Alias("install-docu", docTargetPath)

Default("install-python")
