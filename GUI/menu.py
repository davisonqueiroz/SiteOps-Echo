import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QScrollArea, QGridLayout, QApplication
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize  # Importar QSize corretamente
from PySide6.QtGui import QIcon
from GUI.cards import Card
import acoes

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 - Navegação Modular com Toggle e Animação")
        self.resize(900, 700)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margens
        main_layout.setSpacing(0)                   # Remove o espaçamento interno entre nav_bar e scroll_area


        # NavBar lateral
        self.nav_bar = QFrame()
        self.nav_bar.setMinimumWidth(80)  # Largura mínima
        self.nav_bar.setMaximumWidth(250)  # Largura máxima
        self.nav_bar.setStyleSheet("""
            background-color: #304FFE;
            border-top-right-radius: 15px;
            border-bottom-right-radius: 15px;
        """)
        nav_layout = QVBoxLayout(self.nav_bar)

        # Botão de toggle
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                color: #F5F5F5;
                background-color: #304FFE;
                border: none;
                font-size: 18px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3d566e;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_navbar)
        nav_layout.addWidget(self.toggle_button)

        # Botões de navegação com ícones do Qt
        self.btn_home = QPushButton("Home")
        self.btn_home.setIcon(QIcon.fromTheme("user-home"))  # Ícone padrão Qt
        self.btn_home.setIconSize(QSize(40, 40))  # Define o tamanho do ícone
        self.btn_settings = QPushButton("Configurações")
        self.btn_settings.setIcon(QIcon.fromTheme("configure"))  # Ícone mais confiável
        self.btn_settings.setIconSize(QSize(40, 40))  # Define o tamanho do ícone
        self.btn_about = QPushButton("Sobre")
        self.btn_about.setIcon(QIcon.fromTheme("help-about"))  # Ícone padrão Qt
        self.btn_about.setIconSize(QSize(40, 40))  # Define o tamanho do ícone

        for btn in [self.btn_home, self.btn_settings, self.btn_about]:
            btn.setStyleSheet("""
                QPushButton {
                    color: #F5F5F5;
                    background-color: #304FFE;
                    border: none;
                    border-radius: 10px;
                    padding: 5px;
                    text-align: left;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background-color: #3d566e;
                }
                QPushButton::icon {
                    padding:5px;
                }
            """)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()

        # Área de conteúdo
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Aplica estilo na área de rolagem
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #F5F5F5;
                border: none;
            }
        """)

        self.content_widget = QWidget()

        # Aplica estilo no widget interno
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border-radius: 10px;
            }
        """)

        self.content_layout = QGridLayout(self.content_widget)
        self.content_layout.setContentsMargins(30, 30, 30, 30)  # margem interna
        self.content_layout.setSpacing(20)  # espaço entre os cards

        self.scroll_area.setWidget(self.content_widget)

        # Conexões dos botões de navegação
        self.btn_home.clicked.connect(self.show_home)
        self.btn_settings.clicked.connect(self.show_settings)
        self.btn_about.clicked.connect(self.show_about)

        # Adiciona ao layout principal
        main_layout.addWidget(self.nav_bar)
        main_layout.addWidget(self.scroll_area)

        self.show_home()  # Exibir Home ao iniciar

    def toggle_navbar(self):
        largura_atual = self.nav_bar.width()

        # Define largura alvo para expandir ou recolher
        if largura_atual > 80:
            nova_largura = 80  # Recolher a barra
        else:
            self.btn_home.setText("Home")
            self.btn_settings.setText("Configurações")
            self.btn_about.setText("Sobre")
            nova_largura = 250  # Expandir a barra

        # Cria a animação para alterar a largura
        self.animacao_nav = QPropertyAnimation(self.nav_bar, b"maximumWidth")
        self.animacao_nav.setDuration(1000)  # Duração da animação em milissegundos
        self.animacao_nav.setStartValue(largura_atual)
        self.animacao_nav.setEndValue(nova_largura)

        # Curva de animação
        self.animacao_nav.setEasingCurve(QEasingCurve.InOutQuad)

        self.animacao_nav.start()


        # Atualiza os textos e ícones no final da animação
        def atualizar_textos():
            if nova_largura == 80:
                for btn in [self.btn_home, self.btn_settings, self.btn_about]:
                    btn.setText("")  # Esconde os textos dos botões

        # Conecta ao evento de finalização da animação
        self.animacao_nav.finished.connect(atualizar_textos)

    def clear_content(self):
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_home(self):
        self.clear_content()
        label = QLabel("Bem-vindo à página Home!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: #0C0C0D;")
        self.content_layout.addWidget(label)

    def show_settings(self):
        self.clear_content()
        nomes = [
            "Banco de Dados", "Usuários", "Permissões",
            "Relatórios", "Backup Automático", "Atualizações"
        ]
        for i, nome in enumerate(nomes, start=1):
            card = Card(f"{nome}", f"Botão A{i}", f"Botão B{i}", card_id=i)
            card.setFixedSize(200, 300)  # Tamanho fixo para o card
            card.btn1.clicked.connect(getattr(acoes, f'funcao_botao_A{i}'))
            card.btn2.clicked.connect(getattr(acoes, f'funcao_botao_B{i}'))
            row = (i - 1) // 3  # Calcula a linha (3 cards por linha)
            col = (i - 1) % 3   # Calcula a coluna (3 cards por linha)
            self.content_layout.addWidget(card, row, col)  # Adiciona ao layout em grid

    def show_about(self):
        self.clear_content()
        nomes = [
            "Aplicativo", "Versão", "Licença",
            "Desenvolvedores", "Contato", "Agradecimentos"
        ]
        for i, nome in enumerate(nomes, start=1):
            card = Card(f"{nome}", f"Botão C{i}", f"Botão D{i}", card_id=i)
            card.setFixedSize(200, 300)  # Tamanho fixo para o card
            card.btn1.clicked.connect(getattr(acoes, f'funcao_botao_C{i}'))
            card.btn2.clicked.connect(getattr(acoes, f'funcao_botao_D{i}'))
            row = (i - 1) // 3  # Calcula a linha (3 cards por linha)
            col = (i - 1) % 3   # Calcula a coluna (3 cards por linha)
            self.content_layout.addWidget(card, row, col)  # Adiciona ao layout em grid

# Apenas se quiser rodar diretamente este arquivo para testar:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())