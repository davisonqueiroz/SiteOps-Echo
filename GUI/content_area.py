from GUI.qt_core import *

class ContentArea(QFrame):
    def __init__(self,color,type = "HBox"):
        super().__init__()
        self.setStyleSheet(f"background-color: {color}")
        if type == "HBox":
            self.content = QHBoxLayout(self)
        else:
            self.content = QVBoxLayout(self)
        
    def set_cards_area(self,color,layout_to_add):
        top = ContentArea(color,"HBox")
        self.top_layout = top.layout()
        self.top_layout.setContentsMargins(80,0,0,0)
        self.top_layout.setSpacing(80)
        self.top_layout.setAlignment(Qt.AlignLeft)

        bottom =ContentArea(color,"HBox")
        self.bottom_layout = bottom.layout()
        self.bottom_layout.setContentsMargins(80,0,0,0)
        self.bottom_layout.setSpacing(80)
        self.bottom_layout.setAlignment(Qt.AlignLeft)
        
        self.content.addWidget(top)
        self.content.addWidget(bottom)
        layout_to_add.addWidget(self)

    def get_top_layout(self):
        return self.top_layout
    
    def get_bottom_layout(self):
        return self.bottom_layout