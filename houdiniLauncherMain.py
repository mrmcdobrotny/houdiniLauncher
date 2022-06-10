#!/studio/afanasy/bin/python
import sys, os, glob, platform, json


from PySide2.QtWidgets import *
from PySide2.QtCore import QDir, Qt, QSortFilterProxyModel, QCoreApplication
from PySide2.QtUiTools import loadUiType

# This works on PySide2 or Qt6, PySide2 is put into /media/white/python_local/python3.8/site-packages
# to make this work on every machine $PYTHONPATH should be appended with
# /media/white/python_local/python3.8/site-packages in common environment setup
# also pyside2-uic executable has been placed to /media/white/python_local/bin
# which has to be present in PATH env variable

generated_class, base_class = loadUiType(os.path.join(sys.path[0], 'uiHoudiniLauncher.ui'))


class MainWindow(base_class, generated_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # init attributes
        self.hdaLoaderRoot = '/media/white/tools/scripts/houdini/houdiniLoadHda'
        self.houdini_otls = '/media/white/tools/otls'
        self.os = 'Linux'  # default
        self.hda_folders = []
        self.hda_labels = []
        self.project_path = ''
        self.shotsModel = QFileSystemModel()
        self.project = ''
        self.preset_path = ''
        self.preset = {}
        self.presetContent = None

        # init table
        self.checkOS()
        self.initTable()
        self.initPresetList()
        self.onStart()

        # Setup completer
        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())
        self.completer = QCompleter(self.projects_location)
        self.completer.setModel(model)
        self.completer.setCompletionColumn(0)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionPrefix(self.projects_location.text())
        self.projects_location.setCompleter(self.completer)

        ###

        self.checkLoad()
        self.checkLoadFile.stateChanged.connect(self.checkLoad)

        ###
        self.presetList.currentTextChanged.connect(self.updatePresetContent)

        self.projects_location.editingFinished.connect(self.updateProjectsList)

        self.projects_list.currentTextChanged.connect(self.updateTasksList)
        self.projects_list.currentTextChanged.connect(self.updateShotsList)
        self.projects_list.currentTextChanged.connect(self.updateTaskTypeList)
        self.projects_list.currentTextChanged.connect(self.populateBrowser)

        self.tasksList.currentTextChanged.connect(self.updateShotsList)
        self.tasksList.currentTextChanged.connect(self.updateTaskTypeList)
        self.tasksList.currentTextChanged.connect(self.populateBrowser)

        self.shotsList.currentTextChanged.connect(self.populateBrowser)

        self.taskTypeList.currentTextChanged.connect(self.populateBrowser)

        self.checkLoadFile.stateChanged.connect(self.updateTaskTypeList)

        # self.savePreset.clicked.connect(self.onQuit)
        # self.launch_project.clicked.connect(self.onQuit)
        self.launch_project.clicked.connect(self.launchHoudini)
        self.launch_project.clicked.connect(self.close)

    def checkOS(self):
        system = platform.system()
        if system == 'Windows':
            self.projects_location.setText("T:\\projects\\")
            self.os = 'Windows'

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.launchHoudini()
            self.close()

    def initTable(self):
        self.hda_folders = glob.glob(os.path.join(self.houdini_otls, "hda_*"))
        self.hda_labels = []
        [self.hda_labels.append(os.path.split(path)[1][4:]) for path in self.hda_folders]

        for row, label in enumerate(self.hda_labels):
            
            item = QListWidgetItem("{}".format(label))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            # item.setCheckable(True)
            # if inHdaFolder:
            #    item.setCheckState(QtCore.Qt.CheckState.Checked)
            self.listWidget.addItem(item)

    def onStart(self):
        try:
            settings = json.load(open(os.path.join(os.environ["HOME"], ".houdiniLauncher.conf")))
            
            for index in range(self.listWidget.count()):
                item = self.listWidget.item(index)
                if settings["check{}".format(item.text())]:
                    state = Qt.Checked
                else:
                    state = Qt.Unchecked
                item.setCheckState(state)

            self.checkFx.setChecked(settings["checkFx"])
            self.projects_location.setText(settings["projects_location"])
            self.updateProjectsList()

            self.projects_list.setCurrentIndex(settings["projects_list_current"])
            self.updateTasksList()

            self.tasksList.setCurrentIndex(settings["tasksList_current"])
            self.updateTaskTypeList()

            self.updateShotsList()

            self.shotsList.setCurrentIndex(settings["shotsList_current"])

            self.checkLoadPreset.setChecked(settings["checkLoadPreset"])

            self.presetList.setCurrentText(settings["presetName"])
            self.checkLoadFile.setChecked(settings["checkLoadFile"])
            self.checkLoad()
            self.updateShotsList()
            self.updateTaskTypeList()
            self.taskTypeList.setCurrentIndex(settings["taskTypeList_current"])
            self.populateBrowser()

        except (FileExistsError, KeyError, FileNotFoundError) as e:
            print("Exception")
            self.updateProjectsList()
            self.updateTasksList()
            self.updateTaskTypeList()
            self.updateShotsList()
            self.populateBrowser()

    def closeEvent(self, event):
        self.onQuit()
        
    def onQuit(self):
        settings = dict()
        settings["projects_location"] = self.projects_location.text()
        settings["projects_list_current"] = self.projects_list.currentIndex()
        settings["checkLoadFile"] = self.checkLoadFile.isChecked()
        settings["tasksList_current"] = self.tasksList.currentIndex()
        settings["taskTypeList_current"] = self.taskTypeList.currentIndex()
        settings["shotsList_current"] = self.shotsList.currentIndex()
        settings["checkFx"] = self.checkFx.isChecked()
        settings["presetName"] = self.presetList.currentText()
        settings["checkLoadPreset"] = self.checkLoadPreset.isChecked()

        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            isChecked = item.checkState() == Qt.Checked
            settings["check{}".format(item.text())] = isChecked

        f = open(os.path.join(os.environ["HOME"], ".houdiniLauncher.conf"), "w")
        jsn = json.dumps(settings, indent = 4)
        f.write(jsn)
        f.close()

    def launchHoudini(self):
        prj = self.projects_list.currentData()
        houdini_otlscan_path = os.environ["HOUDINI_OTLSCAN_PATH"]
        prependHoudiniPath = ""
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            isChecked = item.checkState() == Qt.Checked
            otl_dir_name = "hda_{}".format(item.text())
            otl_path = os.path.join(self.houdini_otls, otl_dir_name)
            if isChecked and otl_path not in os.environ["HOUDINI_OTLSCAN_PATH"]:
                prependHoudiniPath += "{};".format(otl_path)

        os.environ["HOUDINI_OTLSCAN_PATH"] = "{};{}".format(prependHoudiniPath, os.environ["HOUDINI_OTLSCAN_PATH"])
        print("HOUDINI_OTLSCAN_PATH={}\n".format(os.environ["HOUDINI_OTLSCAN_PATH"]))

        # -----------------
        # HOUDINI_OTL_USERPRESET environment variable is used by
        # /media/white/tools/scripts/houdini/houdiniOnSceneStartupScripts/scripts/456.py script
        # to install hda's from /media/white/tools/scripts/houdini/houdiniLoadHda/.userpresets

        os.putenv("HOUDINI_OTL_USERPRESET", self.presetList.currentText())
        if self.checkFx.isChecked():
            houdini = "houdinifx"
        else:
            houdini = "houdini"
        print("run '{}'".format(houdini))
        if not self.checkLoadFile.isChecked():
            os.system('/bin/bash -c "{}"'.format(houdini))
        else:
            index = self.treeViewShots.currentIndex()
            file = self.shotsModel.filePath(index)
            os.system('/bin/bash -c "{} {}"'.format(houdini, file))

    def checkLoad(self):
        if not self.checkLoadFile.isChecked():
            self.tasksList.hide()
            self.shotsList.hide()
            self.label_5.hide()
            self.label_6.hide()
            self.treeViewShots.hide()
            self.label_3.hide()
            self.label_7.hide()
            self.taskTypeList.hide()
            self.adjustSize()

        else:
            self.tasksList.show()
            self.shotsList.show()
            self.label_5.show()
            self.label_6.show()
            self.treeViewShots.show()
            self.label_3.show()
            self.label_7.show()
            self.taskTypeList.show()
            
        if self.tasksList.currentText() == "LOOKDEV" or not self.checkLoadFile.isChecked():
            self.shotsList.hide()
            self.label_5.hide()
        else:
            self.shotsList.show()
            self.label_5.show()

    def setDefaultPath(self):
        self.project_path = self.projects_list.currentData()

    def setPath(self):
        path = self.model.filePath(index)
        self.projects_location.setText(path)

    def updateTaskTypeList(self):
        taskType = self.tasksList.currentText()
        defaultTasks = ["animation", "fx", "lighting", "layout"]
        self.taskTypeList.clear()
        if taskType == "LOOKDEV" or not self.checkLoadFile.isChecked():
            defaultTasks = os.listdir(self.tasksList.currentData())
            self.shotsList.hide()
            self.label_5.hide()
        else:
            self.shotsList.show()
            self.label_5.show()
        for task in defaultTasks:
            self.taskTypeList.addItem(task)

    def updateProjectsList(self):
        listd = QDir.entryList(QDir(self.projects_location.text()), QDir.Dirs)
        self.projects_list.clear()
        for d in listd:
            if d != "." and d != ".." and not d.startswith('!'):
                self.projects_list.addItem(d, str(os.path.join(self.projects_location.text(), d)))

    def updateShotsList(self):
        path = [self.projects_list.currentData(), self.tasksList.currentText()]
        try:
            path = os.path.join(*path)
        except TypeError:
            pass
        self.shotsList.clear()
        try:
            listdir = os.listdir(path)
            for shot in listdir:
                if not shot.startswith('.'):
                    self.shotsList.addItem(shot, os.path.join(path, shot))
        except TypeError:
            pass

    def populateBrowser(self):

        self.shotsModel.setRootPath(self.projects_list.currentData())
        self.treeViewShots.setModel(self.shotsModel)
        if self.tasksList.currentText() == 'CGI' and self.shotsList.currentData() is not None:
            root = os.path.join(self.shotsList.currentData(), self.taskTypeList.currentText())
        else:
            root = ''
        if self.tasksList.currentText() == 'LOOKDEV':
            root = os.path.join(self.tasksList.currentData(), self.taskTypeList.currentText())
        self.treeViewShots.setRootIndex(self.shotsModel.index(root))
        self.treeViewShots.setSortingEnabled(True)
        self.treeViewShots.sortByColumn(0, Qt.AscendingOrder)
        self.treeViewShots.setColumnHidden(2, True)
        self.treeViewShots.setColumnHidden(1, True)

    def updateTasksList(self):
        filter_tasks = ['CGI', 'LOOKDEV']
        self.tasksList.clear()
        for task in filter_tasks:
            self.tasksList.addItem(task, os.path.join(self.projects_list.currentData(), task))

    def setProject(self):
        self.project = self.projects_list.currentText()
        self.project_path = self.projects_list.currentData()

    def initPresetList(self):
        self.preset_path = os.path.join(self.hdaLoaderRoot, ".userpresets")
        try:
            with open(self.preset_path, 'r') as f:
                try:
                    self.preset = json.load(f)
                except ValueError:
                    self.preset = {}
            for presetName in self.preset.keys():
                self.presetList.addItem(presetName)
        except IOError:
            self.preset = {}
        self.updatePresetContent()

    def updatePresetContent(self):
        self.presetContent = self.preset[self.presetList.currentText()]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)