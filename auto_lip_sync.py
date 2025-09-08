'''
Name: auto_lip_sync

Description: A tool used for generating automated lip sync animation on a facial rig in Autodesk: Maya.
 
Author: Joar Engberg 2021

Installation:
1. Add the auto_lip_sync folder or auto_lip_sync.py to your Maya scripts folder (Username\Documents\maya*version*\scripts).
2. Download the dependencies needed to run this tool (Download the dependencies from: https://github.com/joaen/maya_auto_lip_sync/releases/tag/v1.0.0 or read the Dependencies section further down).
3. To start the auto lipsync tool in Maya simply execute the following lines of code in the script editor or add them as a shelf button:

import auto_lip_sync
auto_lip_sync.start()

'''
import shutil
import os
import sys
import json
import subprocess
import webbrowser
import traceback
import re

from maya import OpenMaya, OpenMayaUI, mel, cmds
from shiboken2 import wrapInstance
from collections import OrderedDict 
from PySide2 import QtCore, QtGui, QtWidgets

# Import Textgrid. If the module doesn't exist let the user decide if they want to download the dependencies zip.
try:
    import textgrid
except ImportError:
    traceback.print_exc()
    confirm = cmds.confirmDialog(title="Missing dependencies", message="To be able to run this tool you need to download the required dependencies. Do you want go to the download page?", button=["Yes","Cancel"], defaultButton="Yes", cancelButton="Cancel", dismissString="Cancel")
    if confirm == "Yes":
        webbrowser.open_new("https://github.com/joaen/maya-auto-lip-sync#dependencies")
    else:
        pass

# Language settings for English and Chinese with different MFA versions
language_settings = {
    "English": {
        "lexicon": os.path.join(cmds.internalVar(userScriptDir=True), "librispeech-lexicon.txt"),
        "model": os.path.join(cmds.internalVar(userScriptDir=True), "montreal-forced-aligner/pretrained_models/english.zip"),
        "mfa_version": "v1.0.1",
        "mfa_path": os.path.join(cmds.internalVar(userScriptDir=True), "montreal-forced-aligner/bin"),
        "mfa_align_cmd": "mfa_align.exe",
        "mfa_train_cmd": "mfa_train_and_align.exe",
        "phone_dict": {
            "AA0": "AI", "AA1": "AI", "AA2": "AI", "AE0": "AI", "AE1": "AI", "AE2": "AI", 
            "AH0": "AI", "AH1": "AI", "AH2": "AI", "AO0": "AI", "AO1": "AI", "AO2": "AI",
            "AW0": "WQ", "AW1": "WQ", "AW2": "WQ", "AY0": "AI", "AY1": "AI", "AY2": "AI",
            "EH0": "E", "EH1": "E", "EH2": "E", "ER0": "O", "ER1": "O", "ER2": "O", "EY0": "E",
            "EY1": "E", "EY2": "E", "IH0": "AI", "IH1": "AI", "IH2": "AI", "IY0": "E", "IY1": "E",
            "IY2": "E", "OW0": "O", "OW1": "O", "OW2": "O", "OY0": "O", "OY1": "O", "OY2": "O",
            "UH0": "U", "UH1": "U", "UH2": "U", "UW0": "U", "UW1": "U", "UW2": "U", "B": "MBP",
            "CH": "etc", "D": "etc", "DH": "etc", "F": "FV", "G": "etc", "HH": "E", "JH": "E",
            "K": "etc", "L": "L", "M": "MBP", "N": "etc", "NG": "etc", "P": "MBP", "R": "etc",
            "S": "etc", "SH": "etc", "T": "etc", "TH": "etc", "V": "FV", "W": "WQ", "Y": "E",
            "Z": "E", "ZH": "etc", "sil": "rest", "None": "rest", "sp": "rest", "spn": "rest", "": "rest"
        },
        "phone_path_dict": OrderedDict([
            ("AI", ""),
            ("O", ""),
            ("E", ""),
            ("U", ""),
            ("etc", ""),
            ("L", ""),
            ("WQ", ""),
            ("MBP", ""),
            ("FV", ""),
            ("rest", "")
        ])
    },
    "Chinese": {
        "lexicon": os.path.join(cmds.internalVar(userScriptDir=True), "MFA_3.2.3/mandarin_china_mfa3.0.0.dict"),
        "model": os.path.join(cmds.internalVar(userScriptDir=True), "MFA_3.2.3/mandarin_mfa v3.0.0.zip"),
        "mfa_version": "v3.2.3",
        "mfa_path": r"D:\Users\Eric\miniconda3\envs\mfa-323",
        "mfa_align_cmd": "python.exe",
        "mfa_train_cmd": "python.exe",
        "phone_dict": {
            # Basic vowels with tones
            "a": "AI", "a˥": "AI", "a˥˩": "AI", "a˧": "AI", "a˧˥": "AI", "a˨˩˦": "AI", "a˩": "AI",
            "e": "E", "e˥": "E", "e˥˩": "E", "e˧": "E", "e˧˥": "E", "e˨˩˦": "E", "e˩": "E",
            "i": "E", "i˥": "E", "i˥˩": "E", "i˧": "E", "i˧˥": "E", "i˨˩˦": "E", "i˩": "E",
            "o": "O", "o˥": "O", "o˥˩": "O", "o˧": "O", "o˧˥": "O", "o˨˩˦": "O", "o˩": "O",
            "u": "U", "u˥": "U", "u˥˩": "U", "u˧": "U", "u˧˥": "U", "u˨˩˦": "U", "u˩": "U",
            "y": "U", "y˥": "U", "y˥˩": "U", "y˧": "U", "y˧˥": "U", "y˨˩˦": "U", "y˩": "U",  # ü sound
            "ə": "E", "ə˥": "E", "ə˥˩": "E", "ə˧": "E", "ə˧˥": "E", "ə˨˩˦": "E", "ə˩": "E",
            
            # Diphthongs with tones
            "aj": "AI", "aj˥": "AI", "aj˥˩": "AI", "aj˧": "AI", "aj˧˥": "AI", "aj˨˩˦": "AI", "aj˩": "AI",
            "aw": "WQ", "aw˥": "WQ", "aw˥˩": "WQ", "aw˧": "WQ", "aw˧˥": "WQ", "aw˨˩˦": "WQ", "aw˩": "WQ",
            "ej": "E", "ej˥": "E", "ej˥˩": "E", "ej˧": "E", "ej˧˥": "E", "ej˨˩˦": "E", "ej˩": "E",
            "ow": "O", "ow˥": "O", "ow˥˩": "O", "ow˧": "O", "ow˧˥": "O", "ow˨˩˦": "O", "ow˩": "O",
            
            # Consonants
            "p": "MBP", "pʰ": "MBP", "pʲ": "MBP", "pʷ": "MBP",
            "t": "L", "tʰ": "L", "tʲ": "L", "tʷ": "L",
            "k": "GK", "kʰ": "GK", "kʷ": "GK",
            "b": "MBP", "d": "L", "g": "GK",
            
            # Fricatives and affricates
            "f": "FV", "s": "ZCS", "x": "ZCS", "xʷ": "ZCS",
            "ɕ": "ZCS", "ɕʷ": "ZCS", "ʂ": "ZCS",
            "ts": "ZCS", "tsʰ": "ZCS",
            "tɕ": "JQ", "tɕʰ": "JQ", "tɕʷ": "JQ",
            "ʈʂ": "ZH", "ʈʂʰ": "ZH",
            
            # Nasals and liquids
            "m": "MBP", "mʲ": "MBP", "m̩": "MBP", "m̩˥": "MBP", "m̩˥˩": "MBP", "m̩˧": "MBP", "m̩˧˥": "MBP", "m̩˨˩˦": "MBP",
            "n": "L", "n̩˥˩": "L", "n̩˧˥": "L", "n̩˨˩˦": "L",
            "ŋ": "GK", "ŋ̍": "GK", "ŋ̍˥˩": "GK", "ŋ̍˧˥": "GK", "ŋ̍˨˩˦": "GK",
            "l": "L", "ɲ": "L", "ʎ": "L",
            
            # Glides and approximants
            "j": "E", "w": "WQ", "ɥ": "U", "ɻ": "ZH",
            
            # Syllabic consonants
            "z̩": "ZCS", "z̩˥": "ZCS", "z̩˥˩": "ZCS", "z̩˧": "ZCS", "z̩˧˥": "ZCS", "z̩˨˩˦": "ZCS", "z̩˩": "ZCS",
            "ʐ": "ZH", "ʐ̩": "ZH", "ʐ̩˥": "ZH", "ʐ̩˥˩": "ZH", "ʐ̩˧": "ZH", "ʐ̩˧˥": "ZH", "ʐ̩˨˩˦": "ZH", "ʐ̩˩": "ZH",
            
            # Glottal stop
            "ʔ": "rest",
            
            # Special symbols
            "sil": "rest", "None": "rest", "sp": "rest", "spn": "rest", "<eps>": "rest", "": "rest"
        },
        "phone_path_dict": OrderedDict([
            ("MBP", ""),
            ("FV", ""),
            ("L", ""),
            ("GK", ""),
            ("JQ", ""),
            ("ZH", ""),
            ("ZCS", ""),
            ("AI", ""),
            ("O", ""),
            ("E", ""),
            ("U", ""),
            ("WQ", ""),
            ("rest", "")
        ])
    }
}

class PoseConnectWidget(QtWidgets.QWidget):
    def __init__(self, label, parent=None):
        super(PoseConnectWidget, self).__init__(parent)
        self.combo_label = label
        self.create_ui_widgets()
        self.create_ui_layout()

    def create_ui_widgets(self):
        self.save_pose_combo = QtWidgets.QComboBox()
        self.pose_key_label = QtWidgets.QLabel(self.combo_label)
        self.pose_key_label.setFixedWidth(30)
        self.pose_key_label.setStyleSheet("border: 1px solid #303030;")
    
    def create_ui_layout(self):
        combo_row = QtWidgets.QHBoxLayout(self)
        combo_row.addWidget(self.pose_key_label)
        combo_row.addWidget(self.save_pose_combo)
        combo_row.setContentsMargins(0, 0, 0, 0)
    
    def set_text(self, value):
        self.save_pose_combo.addItems(value)

    def get_text(self):
        return self.save_pose_combo.currentText()
    
    def clear_box(self):
        self.save_pose_combo.clear()


class LipSyncDialog(QtWidgets.QDialog):

    WINDOW_TITLE = "Auto lip sync"
    PYTHON_VERSION = float(re.search(r'\d+\.\d+', sys.version).group())

    USER_SCRIPT_DIR = cmds.internalVar(userScriptDir=True)
    OUTPUT_FOLDER_PATH = USER_SCRIPT_DIR+"output"
    INPUT_FOLDER_PATH = USER_SCRIPT_DIR+"input"
    
    MFA_PATH = USER_SCRIPT_DIR+"montreal-forced-aligner/bin"
    if os.path.exists(MFA_PATH) == False:
        cmds.confirmDialog(title="Path doesn't exsist!", message="This path doesn't exsist: "+MFA_PATH)
    
    def __init__(self):
        # Initialize instance variables first!
        self.current_language = "English"
        self.LEXICON_PATH = language_settings[self.current_language]["lexicon"]
        self.LANGUAGE_PATH = language_settings[self.current_language]["model"]
        self.phone_dict = language_settings[self.current_language]["phone_dict"]
        self.phone_path_dict = language_settings[self.current_language]["phone_path_dict"]
        self.current_mfa_path = language_settings[self.current_language]["mfa_path"]
        self.current_mfa_align_cmd = language_settings[self.current_language]["mfa_align_cmd"]
        self.current_mfa_train_cmd = language_settings[self.current_language]["mfa_train_cmd"]

        self.sound_clip_path = ""
        self.text_file_path = ""
        self.pose_folder_path = ""
        self.active_controls = []

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if sys.version_info.major < 3:
            maya_main_window = wrapInstance(long(main_window), QtWidgets.QWidget) # type: ignore
        else:
            maya_main_window = wrapInstance(int(main_window), QtWidgets.QWidget)
        
        super(LipSyncDialog, self).__init__(maya_main_window)

        self.widget_list = []
        self.counter = 0
        self.maya_color_list = [13, 18, 14, 17]
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.resize(380, 100)
        self.create_ui_widgets()
        self.create_ui_layout()
        self.create_ui_connections()
 
    def create_ui_widgets(self):
        self.sound_text_label = QtWidgets.QLabel("Input wav.file:")
        self.sound_filepath_line = QtWidgets.QLineEdit()
        self.sound_filepath_button = QtWidgets.QPushButton()
        self.sound_filepath_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.sound_filepath_line.setText(self.sound_clip_path)

        self.text_input_label = QtWidgets.QLabel("Input txt.file:")
        self.text_filepath_line = QtWidgets.QLineEdit()
        self.text_filepath_button = QtWidgets.QPushButton()
        self.text_filepath_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.text_filepath_line.setText(self.text_file_path)

        self.pose_folder_label = QtWidgets.QLabel("Pose folder:")
        self.pose_filepath_line = QtWidgets.QLineEdit()
        self.pose_filepath_button = QtWidgets.QPushButton()
        self.pose_filepath_button.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.pose_refresh_button = QtWidgets.QPushButton()
        self.pose_refresh_button.setIcon(QtGui.QIcon(":refresh.png"))
        self.pose_filepath_line.setText(self.pose_folder_path)

        self.generate_keys_button = QtWidgets.QPushButton("Generate keyframes")
        self.generate_keys_button.setStyleSheet("background-color: lightgreen; color: black")
        self.save_pose_button = QtWidgets.QPushButton("Save pose")
        self.help_button = QtWidgets.QPushButton("?")
        self.help_button.setFixedWidth(25)
        self.help_button.setToolTip("Open the README web page")
        self.load_pose_button = QtWidgets.QPushButton("Load pose")
        self.close_button = QtWidgets.QPushButton("Close")

        self.separator_line = QtWidgets.QFrame(parent=None)
        self.separator_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator_line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.language_label = QtWidgets.QLabel("Language:")
        self.language_combo = QtWidgets.QComboBox()
        self.language_combo.addItems(["English", "Chinese"])

    def create_ui_layout(self):
        language_row = QtWidgets.QHBoxLayout()
        language_row.addWidget(self.language_label)
        language_row.addWidget(self.language_combo)

        sound_input_row = QtWidgets.QHBoxLayout()
        sound_input_row.addWidget(self.sound_text_label)
        sound_input_row.addWidget(self.sound_filepath_line)
        sound_input_row.addWidget(self.sound_filepath_button)

        text_input_row = QtWidgets.QHBoxLayout()
        text_input_row.addWidget(self.text_input_label)
        text_input_row.addWidget(self.text_filepath_line)
        text_input_row.addWidget(self.text_filepath_button)

        pose_input_row = QtWidgets.QHBoxLayout()
        pose_input_row.addWidget(self.pose_folder_label)
        pose_input_row.addWidget(self.pose_filepath_line)
        pose_input_row.addWidget(self.pose_filepath_button)
        pose_input_row.addWidget(self.pose_refresh_button)
        
        pose_buttons_row = QtWidgets.QHBoxLayout()
        pose_buttons_row.addWidget(self.load_pose_button)
        pose_buttons_row.addWidget(self.save_pose_button)

        bottom_buttons_row = QtWidgets.QHBoxLayout()
        bottom_buttons_row.addWidget(self.generate_keys_button)
        bottom_buttons_row.addWidget(self.close_button)
        bottom_buttons_row.addWidget(self.help_button)

        # Add connection between pose file and phoneme
        pose_widget_layout = QtWidgets.QVBoxLayout()
        for key in list(self.phone_path_dict.keys()):
            pose_connect_widget = PoseConnectWidget(key)
            pose_widget_layout.addWidget(pose_connect_widget)
            pose_connect_widget.set_text(self.get_pose_paths())
            self.widget_list.append(pose_connect_widget)
            
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(language_row)
        main_layout.addLayout(sound_input_row)
        main_layout.addLayout(text_input_row)
        main_layout.addWidget(self.separator_line)
        main_layout.addLayout(pose_input_row)
        main_layout.addLayout(pose_buttons_row)
        main_layout.addLayout(pose_widget_layout)
        main_layout.addLayout(bottom_buttons_row)
        main_layout.setAlignment(QtCore.Qt.AlignTop)

    def create_ui_connections(self):
        self.sound_filepath_button.clicked.connect(self.input_sound_dialog)
        self.text_filepath_button.clicked.connect(self.input_text_dialog)
        self.pose_filepath_button.clicked.connect(self.pose_folder_dialog)
        self.save_pose_button.clicked.connect(self.save_pose_dialog)
        self.load_pose_button.clicked.connect(self.load_pose_dialog)
        self.pose_refresh_button.clicked.connect(self.refresh_pose_widgets)
        self.close_button.clicked.connect(self.close_window)
        self.generate_keys_button.clicked.connect(self.generate_animation)
        self.help_button.clicked.connect(self.open_readme)
        self.language_combo.currentTextChanged.connect(self.update_language)

    def pose_folder_dialog(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select pose folder path", "")
        if folder_path:
            self.pose_filepath_line.setText(folder_path)
            self.pose_folder_path = folder_path
            self.refresh_pose_widgets()

    def input_sound_dialog(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select sound clip", "", "Wav (*.wav);;All files (*.*)")
        if file_path[0]:
            self.sound_filepath_line.setText(file_path[0])
            self.sound_clip_path = file_path[0]

    def save_pose_dialog(self):
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save pose file", self.pose_folder_path, "Pose file (*.json);;All files (*.*)")
        if file_path[0]:
            self.save_pose(file_path[0])
            print("Saved pose: "+file_path[0])

    def load_pose_dialog(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Save pose file", self.pose_folder_path, "Pose file (*.json);;All files (*.*)")
        if file_path[0]:
            self.load_pose(file_path[0])
            print("Loaded pose: "+file_path[0])

    def input_text_dialog(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Select dialog transcript", "", "Text (*.txt);;All files (*.*)")
        if file_path[0]:
            self.text_filepath_line.setText(file_path[0])
            self.text_file_path = file_path[0]

    def find_textgrid_file(self):
        path = self.OUTPUT_FOLDER_PATH
        textgrid_file = ""
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".TextGrid"):
                    textgrid_file = root+"/"+file
        return textgrid_file

    def open_readme(self):
        webbrowser.open_new("https://github.com/joaen/maya_auto_lip_sync/blob/main/README.md")

    def generate_animation(self):
        number_of_operations = 12
        current_operation = 0
        p_dialog = QtWidgets.QProgressDialog("Analyzing the input data and generating keyframes...", "Cancel", 0, number_of_operations, self)
        p_dialog.setWindowFlags(p_dialog.windowFlags() ^ QtCore.Qt.WindowCloseButtonHint)
        p_dialog.setWindowFlags(p_dialog.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        p_dialog.setWindowTitle("Progress...")
        p_dialog.setValue(0)
        p_dialog.setWindowModality(QtCore.Qt.WindowModal)
        p_dialog.show()
        QtCore.QCoreApplication.processEvents()

        self.create_clean_input_folder()
        self.update_phone_paths()
        p_dialog.setValue(current_operation + 1)

        try:
            self.import_sound()
        except:
            traceback.print_exc()
            cmds.warning("Could not import sound file.")
        p_dialog.setValue(current_operation + 1)

        # Run force aligner
        print(f"[DEBUG] Running MFA for language: {self.current_language}")
        print(f"[DEBUG] Using LEXICON_PATH: {self.LEXICON_PATH}")
        print(f"[DEBUG] Using LANGUAGE_PATH: {self.LANGUAGE_PATH}")
        print("MFA_PATH:", self.MFA_PATH)
        print("INPUT_FOLDER_PATH:", self.INPUT_FOLDER_PATH)
        print("OUTPUT_FOLDER_PATH:", self.OUTPUT_FOLDER_PATH)
        print("Command to run:")
        
        # Use different MFA versions based on language
        if self.current_language == "English":
            # MFA 1.0.1 command format
            mfa_cmd = os.path.join(self.current_mfa_path, self.current_mfa_align_cmd)
            command = '"{}" "{}" "{}" "{}" "{}"'.format(
                mfa_cmd,
                self.INPUT_FOLDER_PATH,
                self.LEXICON_PATH,
                self.LANGUAGE_PATH,
                self.OUTPUT_FOLDER_PATH
            )
        else:
            # MFA 3.2.3 command format for Chinese
            mfa_cmd = os.path.join(self.current_mfa_path, self.current_mfa_align_cmd)
            # Set environment variables for MFA 3.2.3
            env = os.environ.copy()
            env['PATH'] = os.path.join(self.current_mfa_path, 'Library', 'bin') + os.pathsep + env.get('PATH', '')
            
            command = '"{}" -m montreal_forced_aligner.command_line.mfa align "{}" "{}" "{}" "{}"'.format(
                mfa_cmd,
                self.INPUT_FOLDER_PATH,
                self.LEXICON_PATH,
                self.LANGUAGE_PATH,
                self.OUTPUT_FOLDER_PATH
            )
        print("Running command:", command)  # For debugging
        
        # Use environment variables for Chinese MFA 3.2.3
        if self.current_language == "Chinese":
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                env=env
            )
        else:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
        
        for line in process.stdout:
            if line.strip():
                current_operation += 1
                p_dialog.setValue(current_operation)
                print(line)

        for line in process.stderr:
            if line.strip():
                print(line)
    
        process.wait()

        try:
            self.create_keyframes()
            print("Successfully generated keyframes.")
            p_dialog.setValue(number_of_operations)
            p_dialog.close()
        except:
            traceback.print_exc()
            p_dialog.setValue(number_of_operations)
            p_dialog.close()
        
        self.delete_input_folder()

    def import_sound(self):
        cmds.sound(file=self.sound_clip_path, name="SoundFile")
        gPlayBackSlider = mel.eval("$tmpVar=$gPlayBackSlider")
        cmds.timeControl( gPlayBackSlider, edit=True, sound="SoundFile")

    def delete_input_folder(self):
        try:
            shutil.rmtree(self.INPUT_FOLDER_PATH)
            shutil.rmtree(self.OUTPUT_FOLDER_PATH)
        except:
            pass

    def create_clean_input_folder(self):

        self.delete_input_folder()

        # Create folder
        os.mkdir(self.INPUT_FOLDER_PATH)
        sound_source = self.sound_clip_path
        text_source = self.text_file_path
        destination = self.INPUT_FOLDER_PATH

        # Copy sound file
        shutil.copy(sound_source, destination)
        
        # Copy and encode text file with UTF-8
        sound_name = ""
        for file in os.listdir(destination):
            if file.endswith(".wav"):
                sound_name = file.split(".")[0]
        
        # Try different encodings
        encodings = ['utf-8', 'gb18030', 'big5', 'gbk']
        text_content = None
        
        for enc in encodings:
            try:
                with open(text_source, 'r', encoding=enc) as source_file:
                    text_content = source_file.read()
                break  # If successful, break the loop
            except UnicodeDecodeError:
                continue
        
        if text_content is None:
            cmds.error("Could not decode the text file with any of the supported encodings. Please ensure the file is encoded in UTF-8, GB18030, Big5, or GBK.")
            return
        
        # Write the text file in UTF-8
        target_path = os.path.join(destination, sound_name + ".txt")
        with open(target_path, 'w', encoding='utf-8') as target_file:
            target_file.write(text_content)

    def create_keyframes(self):
        print("[DEBUG] Entered create_keyframes")
        textgrid_path = self.find_textgrid_file()
        print(f"[DEBUG] TextGrid path: {textgrid_path}")

        if not textgrid_path:
            cmds.error("No TextGrid file found. This usually means the Montreal Forced Aligner failed to run. Please check that:")
            cmds.error("1. Montreal Forced Aligner is properly installed")
            cmds.error("2. Input audio file is 16kHz, single channel WAV format")
            cmds.error("3. Input text file is properly formatted")
            return

        if not os.path.exists(textgrid_path):
            cmds.error(f"TextGrid file not found at: {textgrid_path}")
            return

        try:
            print("[DEBUG] Loading TextGrid file")
            tg = textgrid.TextGrid.fromFile(textgrid_path)
            print(f"[DEBUG] TextGrid loaded. Number of tiers: {len(tg)}")
            iterations = len(tg[1])
            print(f"[DEBUG] Number of intervals in phones tier: {iterations}")

            for i in range(iterations):
                min_time = str(tg[1][i].minTime)
                max_time = str(tg[1][i].maxTime)
                phone = tg[1][i].mark

                key_value = self.phone_dict.get(phone)
                pose_path = None
                for k in self.phone_path_dict:
                    if key_value in k:
                        pose_path = self.phone_path_dict.get(k)
                print(f"[DEBUG] Interval {i}: {min_time}-{max_time}, phone: {phone}, key_value: {key_value}, pose_path: {pose_path}")

                if not pose_path or not os.path.exists(pose_path):
                    print(f"[ERROR] Skipping phone '{phone}' (key_value: {key_value}) - no valid pose path.")
                    continue

                self.load_pose(pose_path)
                cmds.setKeyframe(self.active_controls, time=[min_time+"sec", max_time+"sec"])
                cmds.keyTangent(self.active_controls, inTangentType="spline", outTangentType="spline")
            print("[DEBUG] Finished creating keyframes")
        except Exception as e:
            print(f"[DEBUG] Exception in create_keyframes: {e}")
            cmds.error(f"Error reading TextGrid file: {str(e)}")
            return

    def save_pose(self, pose_path):
        controllers = cmds.ls(sl=True)
        controller_dict = OrderedDict()
        attr_dict = OrderedDict()

        for ctrl in controllers:
            keyable_attr_list = cmds.listAttr(ctrl, keyable=True, unlocked=True)

            for attr in keyable_attr_list:
                attr_value = cmds.getAttr(ctrl+"."+attr)
                attr_dict[attr] = attr_value

            controller_dict[ctrl] = attr_dict
            attr_dict = {}
        save_path = pose_path

        with open(save_path, "w", encoding='utf-8') as jsonFile:
            json.dump(controller_dict, jsonFile, indent=4, ensure_ascii=False)

    def load_pose(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            pose_data = json.load(f)
        self.active_controls = []

        if self.PYTHON_VERSION < 3:
            for ctrl, input in pose_data.iteritems():
                for attr, value in input.iteritems():
                    cmds.setAttr(ctrl+"."+attr, value)
                self.active_controls.append(ctrl)
        else:
            for ctrl, input in pose_data.items():
                for attr, value in input.items():
                    cmds.setAttr(ctrl+"."+attr, value)
                self.active_controls.append(ctrl)

    def get_pose_paths(self):
        pose_list = []
        folder_path = self.pose_folder_path
        try:
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    pose_list.append(folder_path+"/"+file)
            return pose_list
        except:
            return pose_list

    def refresh_pose_widgets(self):
        for w in self.widget_list:
            w.clear_box()
            w.set_text(self.get_pose_paths())

    def update_phone_paths(self):
        for index, key in enumerate(self.phone_path_dict):
            self.phone_path_dict[key] = self.widget_list[index].get_text()

    def close_window(self):
        self.close()
        self.deleteLater()

    def update_language(self, language):
        print(f"[DEBUG] Switching language to: {language}")
        settings = language_settings[language]
        self.current_language = language
        self.LEXICON_PATH = settings["lexicon"]
        self.LANGUAGE_PATH = settings["model"]
        self.phone_dict = settings["phone_dict"]
        self.phone_path_dict = settings["phone_path_dict"]
        # Update MFA version-specific settings
        self.current_mfa_path = settings["mfa_path"]
        self.current_mfa_align_cmd = settings["mfa_align_cmd"]
        self.current_mfa_train_cmd = settings["mfa_train_cmd"]
        print(f"[DEBUG] LEXICON_PATH set to: {self.LEXICON_PATH}")
        print(f"[DEBUG] LANGUAGE_PATH set to: {self.LANGUAGE_PATH}")
        print(f"[DEBUG] MFA Version: {settings['mfa_version']}")
        print(f"[DEBUG] MFA Path: {self.current_mfa_path}")
        print(f"[DEBUG] MFA Commands: {self.current_mfa_align_cmd}, {self.current_mfa_train_cmd}")
        
        # Clear and rebuild the pose widgets with new phoneme categories
        for widget in self.widget_list:
            widget.deleteLater()
        self.widget_list.clear()
        
        # Rebuild pose widgets with new phoneme categories
        # Find the main layout and get the pose widget layout (6th item in main layout)
        main_layout = self.layout()
        if main_layout and main_layout.count() >= 7:
            pose_widget_layout = main_layout.itemAt(6).layout()  # pose_widget_layout is the 7th item
            if pose_widget_layout:
                for key in list(self.phone_path_dict.keys()):
                    pose_connect_widget = PoseConnectWidget(key)
                    pose_widget_layout.addWidget(pose_connect_widget)
                    pose_connect_widget.set_text(self.get_pose_paths())
                    self.widget_list.append(pose_connect_widget)
        
        # Refresh the pose widgets to show current paths
        self.refresh_pose_widgets()


def start():
    global lip_sync_ui
    try:
        lip_sync_ui.close() # type: ignore
        lip_sync_ui.deleteLater() # type: ignore
    except:
        pass
    lip_sync_ui = LipSyncDialog()
    lip_sync_ui.show()

if __name__ == "__main__":
    start()
