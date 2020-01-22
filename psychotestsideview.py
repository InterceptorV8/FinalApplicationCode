import tkinter as Tk

class PsychoTestSideView:
    def __init__(self, root):
        self.PsychoTestFrame2 = Tk.Frame(root)
        # przyciski
        self.PsychoBtn1 = Tk.Button(root, text="Start", state="normal")
        self.PsychoBtn1.place(x=0, y=0, height=100, width=300)

        self.PsychoBtn2 = Tk.Button(root, text="Stop", state="normal")
        self.PsychoBtn2.place(x=0, y=100, height=100, width=300)

        # obsługa wyświetlania
        self.VoltageShow = Tk.Entry(root, state='disabled')
        self.VoltageShow.place(x=450, y=40)

        self.VoltageShowlabel = Tk.Label(root, text="Napięcie:")
        self.VoltageShowlabel.place(x=375, y=40)

        self.HeartRateShow = Tk.Entry(root, state='disabled')
        self.HeartRateShow.place(x=450, y=140)

        self.HeartRateShowlabel = Tk.Label(root, text="Tętno:")
        self.HeartRateShowlabel.place(x=375, y=140)

        self.GSRShow = Tk.Entry(root, state='disabled')
        self.GSRShow.place(x=450, y=240)

        self.GSRShowlabel = Tk.Label(root, text="GSR:")
        self.GSRShowlabel.place(x=375, y=240)

        self.GSRShowContinuity = Tk.Entry(root, state='disabled')
        self.GSRShowContinuity.place(x=720, y=140)

        self.GSRShowContinuitylabel = Tk.Label(root, text="Numer próbki GSR:")
        self.GSRShowContinuitylabel.place(x=600, y=140)

        self.HeartRateContinuity = Tk.Entry(root, state='disabled')
        self.HeartRateContinuity.place(x=720, y=240)

        self.HeartRateContinuitylabel = Tk.Label(root, text="Numer próbki tętna:")
        self.HeartRateContinuitylabel.place(x=600, y=240)

        self.StateNameLabel = Tk.Label(root, text='Stan badania:')
        self.StateNameLabel.place(x=600, y=40)

        self.StateLabel = Tk.Label(root, text="wyłączone", fg="red")
        self.StateLabel.place(x=720, y=40)

        # opis danych
        self.DataLabel = Tk.Label(root, text="Dane do komunikacji")
        self.DataLabel.place(x=25, y=325)

        self.mqttserveraddressfield = Tk.Entry(root)
        self.mqttserveraddressfield.place(x=125, y=375)

        self.mqttserverlabel = Tk.Label(root, text="Adres IP serwera")
        self.mqttserverlabel.place(x=25, y=375)

        self.mqttserverusernamefield = Tk.Entry(root)
        self.mqttserverusernamefield.place(x=125, y=425)

        self.mqttserverusernamelabel = Tk.Label(root, text="Login serwera")
        self.mqttserverusernamelabel.place(x=25, y=425)

        self.mqttserverpasswordfield = Tk.Entry(root)
        self.mqttserverpasswordfield.place(x=450, y=375)

        self.mqttserverpasswordlabel = Tk.Label(root, text="Hasło serwera")
        self.mqttserverpasswordlabel.place(x=350, y=375)

        self.mqttclientidfield = Tk.Entry(root)
        self.mqttclientidfield.place(x=450, y=425)

        self.mqttclientidlabel = Tk.Label(root, text="ID Klienta")
        self.mqttclientidlabel.place(x=350, y=425)
