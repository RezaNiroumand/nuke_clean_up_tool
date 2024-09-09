from PySide6 import QtCore, QtUiTools, QtWidgets
import os
import sys
app = QtWidgets.QApplication([])
class nuke_clean_up_UI(QtWidgets.QWidget):

    def __init__(self):

        ui_name = 'nuke_clean_up_tool.ui'
        help_name = "USER_MANUAL.pdf"
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)

        ui_path = os.path.join(application_path, ui_name)
        
        self.help_path = os.path.join(application_path, help_name)


        super(nuke_clean_up_UI, self).__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle('nuke clean up')


        self.resize(600, 100)
        self.setAcceptDrops(True)
        self.ui = ui_path
        loader = QtUiTools.QUiLoader()
        ui_file = QtCore.QFile(self.ui)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.theMainWidget = loader.load(ui_file)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.theMainWidget)
        self.setLayout(main_layout)


        self.listWidget = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.listWidget.setAcceptDrops(True)

        self.start_pushButton = self.findChild(QtWidgets.QPushButton, "start_pushButton")
        self.start_pushButton.clicked.connect(self.start_copy)

        self.copy_file_label = self.findChild(QtWidgets.QLabel, "copy_file_label")
        
        
        menu_bar = self.theMainWidget.menuBar()
        menu_help = menu_bar.findChild(QtWidgets.QMenu, "menuHelp")
        help_action = menu_help.actions()[0]
        help_action.triggered.connect(self.showHelp)


        self.files_list = []

    def showHelp(self):
        if sys.platform == 'win32':
            os.startfile(self.help_path)
        else:
            os.system(f'open "{self.help_path}"')

    def start_copy(self):

        if self.listWidget.count() == 0:
            message_box = QtWidgets.QMessageBox()
            message_box.setWindowTitle('Warning')
            message_box.setText("Please Drag Nuke files in the box.")
            message_box.exec_()
        else:
            for x in range(self.listWidget.count()):
                self.files_list.append(self.listWidget.item(x).text())
            self.clean_up()


    def clean_up(self):
        print(self.files_list)
        for item in self.files_list:
            input_file_name = item
            output_file_name = item.rsplit('.', 1)[0]+'_cleaned.nk'
            with open(input_file_name, 'r') as f:
                lines = f.readlines()
            with open(output_file_name, 'w') as f:
                for line in lines:
                    if line.startswith('Root {'):
                        starts_root = True
                    if line.startswith(' addUserKnob {') and starts_root == True:
                        continue
                    if line.startswith('}'):
                        starts_root = False
                    f.write(line)
                f.close()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.path().endswith('.nk'):
                    self.listWidget.addItem(url.path()[1:])
            event.accept()
        else:
            event.ignore()

UI = nuke_clean_up_UI()
UI.show()
app.exec()


