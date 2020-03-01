def initialize_method():
    global choose_method
    choose_method = "TKEO"


def change_method_to(method):
    global choose_method
    choose_method = method


def chosen_method():
    global choose_method
    print(choose_method)
    return choose_method
