import TermTk as ttk
from TermTk import pyTTkSlot
import dice


def test1():
    root = ttk.TTk(layout=ttk.TTkVBoxLayout())

    # Attach 4 buttons to the root widget
    ttk.TTkButton(parent=root, border=True, text="Button1")
    ttk.TTkButton(parent=root, border=True, text="Button2")
    ttk.TTkButton(parent=root, border=True, text="Button3")
    ttk.TTkButton(parent=root, border=True, text="Button4")
    return root

def test2():
    root = ttk.TTk()

    ikkuna = ttk.TTkWindow(parent=root, pos=(1, 1), size=(50, 30), title='oof', border=True)

    ttk.TTkLabel(parent=ikkuna, pos=(5, 2), text="prööööööt")

    ttk.TTkButton(parent=ikkuna, pos=(0, 0), size=(15, 5), border=True, text="Button1")
    ttk.TTkButton(parent=ikkuna, pos=(0, 5), size=(10, 4), border=True, text="Button2")
    ttk.TTkButton(parent=ikkuna, pos=(10, 6), size=(10, 3), border=True, text="Button3")
    ttk.TTkButton(parent=ikkuna, pos=(16, 1), size=(15, 3), border=True, text="Button4")

    return root

def test3():
    gridLayout = ttk.TTkGridLayout(columnMinHeight=0, columnMinWidth=2)
    root = ttk.TTk(layout=gridLayout)

    # Attach 2 buttons to the root widget using the default method
    # this will append them to the first row
    ttk.TTkButton(parent=root, border=True, text="Button1")
    ttk.TTkButton(parent=root, border=True, text="Button2")
    # Attach 2 buttons to a specific position in the grid
    gridLayout.addWidget(ttk.TTkButton(parent=root, border=True, text="Button3"), 1, 2)
    gridLayout.addWidget(ttk.TTkButton(parent=root, border=True, text="Button4"), 3, 4)
    return root

def test4():
    root = ttk.TTk()

    gridLayout = ttk.TTkGridLayout()
    root.setLayout(gridLayout)

    # Attach 2 buttons to the root widget using the default method
    # this will append them to the first row
    # NOTE: it is not recommended to use this legacy method in a gridLayout
    ttk.TTkButton(parent=root, border=True, text="Button1")
    ttk.TTkButton(parent=root, border=True, text="Button2")
    # Attach 2 buttons to a specific position in the grid
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button3"), 2, 2)
    gridLayout.addWidget(ttk.TTkButton(border=True, text="Button4"), 2, 4)

    # Create a VBoxLayout and add it to the gridLayout
    vboxLayout = ttk.TTkVBoxLayout()
    gridLayout.addItem(vboxLayout, 1, 3)
    # Attach 2 buttons to the vBoxLayout
    vboxLayout.addWidget(ttk.TTkButton(border=True, text="Button5"))
    vboxLayout.addWidget(ttk.TTkButton(border=True, text="Button6"))

    return root

def test5():
    root = ttk.TTk()

    # Create a window with a logviewer
    logWin = ttk.TTkWindow(parent=root, pos=(10, 0), size=(80, 20), title="The Net", border=True,
                           layout=ttk.TTkVBoxLayout())
    #ttk.TTkLogViewer(parent=logWin)


    dice_table = ttk.TTkWindow(parent=root, pos=(80, 15), size=(40, 20), title="Dice", border=True,
                               layout=ttk.TTkVBoxLayout())
    dice_btn = ttk.TTkButton(parent=dice_table, text="Roll")
    dice_history = ttk.TTkTextEdit(text="", parent=dice_table, maxHeight=10)

    @pyTTkSlot()
    def roll():
        res = dice.rollWithCrit(skip_luck=True, std=dice_history)
        res_txt = f"Rolled {res}"
        dice_history.append(res_txt)

    dice_btn.clicked.connect(roll)





    inputRow = ttk.TTkLineEdit(parent=logWin, text=">", pos=(0, 0), size=(3,3,), border=True)
    historyRow = ttk.TTkTextEdit(text="", parent=logWin, maxHeight=10)

    txt = ""

    @pyTTkSlot()
    def setText():
        txt = inputRow.text()
        inputRow.setText("")
        historyRow.append(txt)


    inputRow.returnPressed.connect(setText)

    # Create 2 buttons
    btnShow = ttk.TTkButton(parent=root, text="Show", pos=(0, 0), size=(10, 3), border=True)
    btnHide = ttk.TTkButton(parent=root, text="Hide", pos=(0, 3), size=(10, 3), border=True)
    #btnClose = ttk.TTkButton(parent=root, text="Close", pos=(0,6), size=(10,3), border=True)

    # Connect the btnShow's "clicked" signal with the window's "show" slot
    btnShow.clicked.connect(logWin.show)
    # Connect the btnHide's "clicked" signal with the window's "hide" slot
    btnHide.clicked.connect(logWin.hide)

    #btnClose.clicked.connect(logWin.close)
    return root
