from GUI.menu import menu_window
from GUI.cards import card_frame

window = menu_window("teste",930,700,"#EEEEEE","#304FFE","#DDDDDD")
card = card_frame(window)
# window.create_menu_bar()
window.create_sub_menu_button("btn_home",180,"ASSETS/ICONS/home_icon.png",bg_color="#EEEEEE")
window.create_sub_menu_button("btn_cruzeiro",235,"ASSETS/ICONS/cruzeiro_icon.png")
card.create_card("Técnico","MSP:",0,0,6,32)
card.create_card("Cruzeiro","EXP:",0,1,6,32)
# card.create_card("teste",1,0,10,32)
# card.create_card("teste",0,3,10,32)
window.display()
