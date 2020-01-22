import tkinter as Tk
from psychotestsideview import PsychoTestSideView
from model import PsychoTest

class PsychoTestMainView:
    def __init__(self):

        self.root = Tk.Tk()
        self.psychotestframe = Tk.Frame(self.root)
        self.root.geometry('900x500')
        self.root.title("Okno pomiarowe testu")
        self.sideview = PsychoTestSideView(self.root)






