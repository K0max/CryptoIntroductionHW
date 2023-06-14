import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QFileDialog
from PySide6.QtUiTools import QUiLoader
from collections import Counter
import DecryptFunction as deFunc

class DecryptionTool(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load('./tool_ui.ui')

        self.setCentralWidget(self.ui)
        self.prevKey = "abcdefghijklmnopqrstuvwxyz"

        self.browse_button = self.ui.browseButton
        self.browse_button.clicked.connect(self.browse_file)

        self.cipher_text = self.ui.cipherTextEdit
        self.cipher_text.setPlaceholderText("请输入密文")
        self.plain_text = self.ui.plainTextEdit
        self.plain_text.setPlaceholderText("这里是明文")
        self.key_input = self.ui.keyInput
        self.key_input.setPlaceholderText("这里输入密钥")

        self.generate_button = self.ui.generateButton
        self.generate_button.clicked.connect(self.key_generate)
        self.submit_button = self.ui.submitButton
        self.submit_button.clicked.connect(self.submit)
        
        self.preimage_text = self.ui.preimageText
        self.preimage_text.setPlaceholderText("这里是原像（明文）")
        self.image_text = self.ui.imageText
        self.image_text.setPlaceholderText("这里是像（密文）")
        self.addMapping_button = self.ui.addMappingButton
        self.addMapping_button.clicked.connect(self.addMapping)
        self.undo_button = self.ui.undoButton
        self.undo_button.clicked.connect(self.undo)

        self.target_word = self.ui.targetWordText
        self.target_word.setPlaceholderText("待提示的目标单词")
        self.wordTip_button = self.ui.wordTipButton
        self.wordTip_button.clicked.connect(self.word_tip)
        self.improve_button = self.ui.improveButton
        self.improve_button.clicked.connect(self.improve_key)
        self.check_process_button = self.ui.checkProcessButton
        self.check_process_button.clicked.connect(self.check_process)
        
        self.tip_text = self.ui.tipText
        self.tip_text.setPlaceholderText("这里是提示")

    def browse_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec():
            file_path = dialog.selectedFiles()[0] 
            with open(file_path, 'r') as f:
                text = f.read()
                # print text to cipher_text
                self.cipher_text.setPlainText(text)

    def submit(self):
        key = self.key_input.text()
        cipher = self.cipher_text.toPlainText()
        cipherWordFrequency = deFunc.countWordFrequency(self.cipher_text.toPlainText())
        ENGLISH_FREQUENT_WORDS, cipherWordFrequencyRank = deFunc.wordFrequencyAnalysis(cipherWordFrequency)
        this_plain_text = deFunc.decrypt(cipher, key)
        self.plain_text.setPlainText(this_plain_text)
        tip_text = "密文与此次破译后的单词对频率排序：\n"
        this_plain_text_word_frequency = deFunc.countWordFrequency(this_plain_text)
        ENGLISH_FREQUENT_WORDS, thisPlainTextWordFrequencyRank = deFunc.wordFrequencyAnalysis(this_plain_text_word_frequency)
        wordNum = len(cipherWordFrequencyRank.split())
        for i in range(wordNum):
            tip_text += cipherWordFrequencyRank.split()[i] + " " + thisPlainTextWordFrequencyRank.split()[i] + "\t"
        tip_text += "\n\n"
        tip_text += "英文单词及其排序：\n" + ENGLISH_FREQUENT_WORDS + "\n\n"
        self.tip_text.setPlainText(tip_text)
        
    def key_generate(self):
        cipherLetterFrequency = deFunc.countLetterFrequency(self.cipher_text.toPlainText())
        key, letterFrequencyRank = deFunc.letterFrequencyAnalysis(cipherLetterFrequency)
        cipherWordFrequency = deFunc.countWordFrequency(self.cipher_text.toPlainText())
        ENGLISH_FREQUENT_WORDS, wordFrequencyRank = deFunc.wordFrequencyAnalysis(cipherWordFrequency)
        ENGLISH_FREQUENT_WORDS = str(ENGLISH_FREQUENT_WORDS)
        ENGLISH_FREQUENT_LETTERS = "etaoinsrhdlcumwfgypbvkjxqz"
        self.key_input.setText(str(key))
        tip_text = "密文字母频率排序：" + letterFrequencyRank + "\n"
        tip_text += "英语字母及其排序：" + ENGLISH_FREQUENT_LETTERS + "\n已按照密文字母频率排序和英语字母频率初步建立密钥映射\n\n"
        tip_text += "密文单词频率排序：\n" + wordFrequencyRank + "\n\n"
        tip_text += "英文单词及其排序：\n" + ENGLISH_FREQUENT_WORDS + "\n\n"
        self.tip_text.setPlainText(tip_text)
        
    def addMapping(self):
        key = self.key_input.text()
        preimage = self.preimage_text.text()
        image = self.image_text.text()
        key, self.prevKey = deFunc.addMapping(key, preimage, image)
        self.key_input.setText(str(key))
        
    def undo(self):
        self.key_input.setText(str(self.prevKey))

    def word_tip(self):
        key = self.key_input.text()
        targetWord = self.target_word.text()
        cipherText = self.cipher_text.toPlainText()
        wordTip_text = deFunc.wordTip(cipherText, key, targetWord)
        self.tip_text.setPlainText(wordTip_text)
    
    def improve_key(self):
        self.prevKey = self.key_input.text()
        key = self.key_input.text()
        key = deFunc.improveKey(self.cipher_text.toPlainText(), key)
        self.key_input.setText(str(key))

    def check_process(self):
        plainText = self.plain_text.toPlainText()
        process, wrongWords = deFunc.checkProcess(plainText)
        tip_text = "破译进度：" + str(process) + "%\n"
        tip_text += "可能还存在的错误单词：\n"
        tip_text += wrongWords
        self.tip_text.setPlainText(tip_text)
        
            
if __name__ == '__main__': 
    app = QApplication(sys.argv)
    window = DecryptionTool()
    # window.resize(600, 400)
    # window.move(300, 300)
    window.show()
    sys.exit(app.exec())
