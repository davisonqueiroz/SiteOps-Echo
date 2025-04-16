from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class Card(QFrame):
    def __init__(self, title, button1_text, button2_text, card_id):
        super().__init__()
        self.card_id = card_id
        self.setStyleSheet("""
            QFrame {
                color: #F5F5F5;
                background-color: #304FFE;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton {
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.card_id = card_id
        
        # Layout principal do card (QVBoxLayout)
        layout = QVBoxLayout(self)
        
        # Título do card
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #F5F5F5;")
        
        # Botão 1
        self.btn1 = QPushButton(button1_text)
        self.btn1.setStyleSheet("""
            QPushButton {
                background-color: #F5F5F5;
                color: #0C0C0D;
                border: none;
            }
            QPushButton:hover {
                background-color: #CCCCCC;
            }
        """)
        
        # Botão 2
        self.btn2 = QPushButton(button2_text)
        self.btn2.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #F5F5F5;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        
        # Adicionando widgets no layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        
        # Definindo o layout no QFrame
        self.setLayout(layout)

