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
        self.completer = QCompleter(self.line_projects_location)
        self.completer.setModel(model)
        self.completer.setCompletionColumn(0)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionPrefix(self.line_projects_location.text())
        self.line_projects_location.setCompleter(self.completer)

        ###

        self.checkLoad()
        self.checkbox_load_file.stateChanged.connect(self.checkLoad)

        ###
        self.combo_presets_list.currentTextChanged.connect(self.updatePresetContent)

        self.line_projects_location.editingFinished.connect(self.update_combo_projects_list)

        self.combo_projects_list.currentTextChanged.connect(self.update_combo_types_list)
        self.combo_projects_list.currentTextChanged.connect(self.update_shots_list)
        self.combo_projects_list.currentTextChanged.connect(self.update_combo_tasks_list)
        self.combo_projects_list.currentTextChanged.connect(self.populateBrowser)

        self.combo_types_list.currentTextChanged.connect(self.update_shots_list)
        self.combo_types_list.currentTextChanged.connect(self.update_combo_tasks_list)
        self.combo_types_list.currentTextChanged.connect(self.populateBrowser)

        self.combo_shots_list.currentTextChanged.connect(self.populateBrowser)

        self.combo_tasks_list.currentTextChanged.connect(self.populateBrowser)

        self.checkbox_load_file.stateChanged.connect(self.update_combo_tasks_list)

        # self.savePreset.clicked.connect(self.onQuit)
        # self.button_launch_project.clicked.connect(self.onQuit)
        self.button_launch_project.clicked.connect(self.launchHoudini)
        self.button_launch_project.clicked.connect(self.close)

    def checkOS(self):
        system = platform.system()
        if system == 'Windows':
            self.line_projects_location.setText("T:\\projects\\")
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
            self.list_load_env.addItem(item)

    def onStart(self):
        try:
            settings = json.load(open(os.path.join(os.environ["HOME"], ".houdiniLauncher.conf")))
            
            for index in range(self.list_load_env.count()):
                item = self.list_load_env.item(index)
                if settings["check{}".format(item.text())]:
                    state = Qt.Checked
                else:
                    state = Qt.Unchecked
                item.setCheckState(state)

            self.checkbox_fx.setChecked(settings["checkbox_fx_current"])
            self.line_projects_location.setText(settings["line_projects_location_current"])
            self.update_combo_projects_list()

            self.combo_projects_list.setCurrentIndex(settings["combo_projects_list_current"])
            self.update_combo_types_list()

            self.combo_types_list.setCurrentIndex(settings["combo_types_list_current"])
            self.update_combo_tasks_list()

            self.update_shots_list()

            self.combo_shots_list.setCurrentIndex(settings["combo_shots_list_current"])

            self.checkbox_load_preset.setChecked(settings["checkbox_load_preset_current"])

            self.combo_presets_list.setCurrentText(settings["presetName"])
            self.checkbox_load_file.setChecked(settings["checkbox_load_file_current"])
            self.checkLoad()
            self.update_shots_list()
            self.update_combo_tasks_list()
            self.combo_tasks_list.setCurrentIndex(settings["combo_tasks_list_current"])
            self.populateBrowser()

        except (FileExistsError, KeyError, FileNotFoundError) as e:
            print("Exception")
            self.update_combo_projects_list()
            self.update_combo_types_list()
            self.update_combo_tasks_list()
            self.update_shots_list()
            self.populateBrowser()

    def closeEvent(self, event):
        self.onQuit()
        
    def onQuit(self):
        settings = dict()
        settings["line_projects_location_current"] = self.line_projects_location.text()
        settings["combo_projects_list_current"] = self.combo_projects_list.currentIndex()
        settings["checkbox_load_file_current"] = self.checkbox_load_file.isChecked()
        settings["combo_types_list_current"] = self.combo_types_list.currentIndex()
        settings["combo_tasks_list_current"] = self.combo_tasks_list.currentIndex()
        settings["combo_shots_list_current"] = self.combo_shots_list.currentIndex()
        settings["checkbox_fx_current"] = self.checkbox_fx.isChecked()
        settings["presetName"] = self.combo_presets_list.currentText()
        settings["checkbox_load_preset_current"] = self.checkbox_load_preset.isChecked()

        for index in range(self.list_load_env.count()):
            item = self.list_load_env.item(index)
            isChecked = item.checkState() == Qt.Checked
            settings["check{}".format(item.text())] = isChecked

        f = open(os.path.join(os.environ["HOME"], ".houdiniLauncher.conf"), "w")
        jsn = json.dumps(settings, indent=4)
        f.write(jsn)
        f.close()

    def launchHoudini(self):
        prj = self.combo_projects_list.currentData()
        houdini_otlscan_path = os.environ["HOUDINI_OTLSCAN_PATH"]
        prependHoudiniPath = ""
        for index in range(self.list_load_env.count()):
            item = self.list_load_env.item(index)
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

        os.putenv("HOUDINI_OTL_USERPRESET", self.combo_presets_list.currentText())
        if self.checkbox_fx.isChecked():
            houdini = "houdinifx"
        else:
            houdini = "houdini"
        print("run '{}'".format(houdini))
        if not self.checkbox_load_file.isChecked():
            os.system('/bin/bash -c "{}"'.format(houdini))
        else:
            index = self.treeview_shots_browser.currentIndex()
            file = self.shotsModel.filePath(index)
            os.system('/bin/bash -c "{} {}"'.format(houdini, file))

    def checkLoad(self):
        if not self.checkbox_load_file.isChecked():
            self.combo_types_list.hide()
            self.combo_shots_list.hide()
            self.label_shots_list.hide()
            self.label_types_list.hide()
            self.treeview_shots_browser.hide()
            self.label_shots_browser.hide()
            self.label_tasks_list.hide()
            self.combo_tasks_list.hide()
            self.adjustSize()

        else:
            self.combo_types_list.show()
            self.combo_shots_list.show()
            self.label_shots_list.show()
            self.label_types_list.show()
            self.treeview_shots_browser.show()
            self.label_shots_browser.show()
            self.label_tasks_list.show()
            self.combo_tasks_list.show()
            
        if self.combo_types_list.currentText() == "LOOKDEV" or not self.checkbox_load_file.isChecked():
            self.combo_shots_list.hide()
            self.label_shots_list.hide()
        else:
            self.combo_shots_list.show()
            self.label_shots_list.show()

    def setDefaultPath(self):
        self.project_path = self.combo_projects_list.currentData()

    def setPath(self):
        path = self.model.filePath(index)
        self.line_projects_location.setText(path)

    def update_combo_tasks_list(self):
        taskType = self.combo_types_list.currentText()
        defaultTasks = ["animation", "fx", "lighting", "layout"]
        self.combo_tasks_list.clear()
        if taskType == "LOOKDEV" or not self.checkbox_load_file.isChecked():
            defaultTasks = os.listdir(self.combo_types_list.currentData())
            self.combo_shots_list.hide()
            self.label_shots_list.hide()
        else:
            self.combo_shots_list.show()
            self.label_shots_list.show()
        for task in defaultTasks:
            self.combo_tasks_list.addItem(task)

    def update_combo_projects_list(self):
        listd = QDir.entryList(QDir(self.line_projects_location.text()), QDir.Dirs)
        self.combo_projects_list.clear()
        for d in listd:
            if d != "." and d != ".." and not d.startswith('!'):
                self.combo_projects_list.addItem(d, str(os.path.join(self.line_projects_location.text(), d)))

    def update_shots_list(self):
        path = [self.combo_projects_list.currentData(), self.combo_types_list.currentText()]
        try:
            path = os.path.join(*path)
        except TypeError:
            pass
        self.combo_shots_list.clear()
        try:
            listdir = os.listdir(path)
            for shot in listdir:
                if not shot.startswith('.'):
                    self.combo_shots_list.addItem(shot, os.path.join(path, shot))
        except TypeError:
            pass

    def populateBrowser(self):

        self.shotsModel.setRootPath(self.combo_projects_list.currentData())
        self.treeview_shots_browser.setModel(self.shotsModel)
        if self.combo_types_list.currentText() == 'CGI' and self.combo_shots_list.currentData() is not None:
            root = os.path.join(self.combo_shots_list.currentData(), self.combo_tasks_list.currentText())
        else:
            root = ''
        if self.combo_types_list.currentText() == 'LOOKDEV':
            root = os.path.join(self.combo_types_list.currentData(), self.combo_tasks_list.currentText())
        self.treeview_shots_browser.setRootIndex(self.shotsModel.index(root))
        self.treeview_shots_browser.setSortingEnabled(True)
        self.treeview_shots_browser.sortByColumn(0, Qt.AscendingOrder)
        self.treeview_shots_browser.setColumnHidden(2, True)
        self.treeview_shots_browser.setColumnHidden(1, True)

    def update_combo_types_list(self):
        filter_tasks = ['CGI', 'LOOKDEV']
        self.combo_types_list.clear()
        for task in filter_tasks:
            self.combo_types_list.addItem(task, os.path.join(self.combo_projects_list.currentData(), task))

    def setProject(self):
        self.project = self.combo_projects_list.currentText()
        self.project_path = self.combo_projects_list.currentData()

    def initPresetList(self):
        self.preset_path = os.path.join(self.hdaLoaderRoot, '.userpresets')
        try:
            with open(self.preset_path, 'r') as f:
                try:
                    self.preset = json.load(f)
                except ValueError:
                    self.preset = {}
            for presetName in self.preset.keys():
                self.combo_presets_list.addItem(presetName)
        except IOError:
            self.preset = {}
        self.updatePresetContent()

    def updatePresetContent(self):
        self.presetContent = self.preset[self.combo_presets_list.currentText()]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    ret = app.exec_()
    sys.exit(ret)