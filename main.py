from GUI.menu import menu_window

window = menu_window("teste",930,700)
# window.create_menu_bar()
window.create_sub_menu_button("btn_home",180,"ASSETS/ICONS/home_icon.png",bg_color="#EEEEEE")
window.create_sub_menu_button("btn_cruzeiro",235,"ASSETS/ICONS/cruzeiro_icon.png")
window.display()
