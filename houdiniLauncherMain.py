import sys
from PySide2.QtWidgets import QMainWindow, QApplication
from uiHoudiniLauncher import Ui_HoudiniLauncher
from os import path, environ, system
import glob, platform



class MainWindow(QMainWindow, Ui_HoudiniLauncher):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setupUi(self)
        self.checkOS()
        self.scanDir()
        self.projects_location.editingFinished.connect(self.scanDir)
        self.launch_project.clicked.connect(self.launchHoudini)
        self.os = "Linux"


    def scanDir(self):
        scandir = self.projects_location.text()
        projects = glob.glob(scandir+"*")
        self.projects_list.clear()
        for prj in projects:
            if(path.isdir(prj)):
                self.projects_list.addItem(path.split(prj)[1], prj)

    def launchHoudini(self):
        prj = self.projects_list.currentData()
        houdini_tools = path.join(prj, "houdini_tools")
        houdini_path = environ["HOUDINI_PATH"]
        if(not houdini_tools in houdini_path):
            environ["HOUDINI_PATH"] = houdini_tools + ";" + houdini_path
            print("env modified for {} project\n\n".format(self.projects_list.currentText()))
        print("{}\n".format(environ["HOUDINI_PATH"]))
        system('/bin/bash -c "ls"')

    def checkOS(self):
        system = platform.system()
        if(system == "Windows"):
            self.projects_location.setText("T:\\projects\\")
            self.os = "Windows"



        #print(system)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    sys.exit( ret )