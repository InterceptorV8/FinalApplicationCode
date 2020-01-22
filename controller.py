import tkinter as Tk
from tkinter import messagebox
from model import PsychoTest
from mainview import PsychoTestMainView
import threading
import time


class PsychoTestController:

    def __init__(self):

        self.badauthenticationcalled = False
        self.lowvoltagecalled = False

        self.mqttserver = 0
        self.mqttuser = 0
        self.mqttpass = 0
        self.mqttclientid = 0

        self.psychotestview = PsychoTestMainView()

        self.psychotestview.sideview.PsychoBtn1.config(command=self.psychobtn1clicked)
        self.psychotestview.sideview.PsychoBtn2.config(command=self.psychobtn2clicked)

        self.psychotestview.sideview.mqttserverusernamefield.insert(0, 'DesktopPsychotest1')
        self.psychotestview.sideview.mqttserverpasswordfield.insert(0, 'DesktopTest1')
        self.psychotestview.sideview.mqttserveraddressfield.insert(0, '192.168.0.100')
        self.psychotestview.sideview.mqttclientidfield.insert(0, 'mqttclientid')

        self.psychotestview.sideview.PsychoBtn1.config(state="normal")
        self.psychotestview.sideview.PsychoBtn2.config(state="disabled")
        self.psychotestview.root.after(400, self.setresultsonview)

        self.model = PsychoTest()

        self.cyanide = threading.Event()

        self.thread1 = threading.Thread(name='server', target=self.model.psychotestmessageserver,
                                        args=(self.cyanide, 'inTopic', 'HRTopic', 'GSRTopic', 'VoltageTopic'))

    def psychobtn1clicked(self):

        self.mqttserver = self.psychotestview.sideview.mqttserveraddressfield.get()
        self.mqttuser = self.psychotestview.sideview.mqttserverusernamefield.get()
        self.mqttpass = self.psychotestview.sideview.mqttserverpasswordfield.get()
        self.mqttclientid = self.psychotestview.sideview.mqttclientidfield.get()

        self.psychotestmessage(self.mqttuser, self.mqttpass, self.mqttclientid, self.mqttserver)

    def psychobtn2clicked(self):
        self.psychotestview.sideview.PsychoBtn2.config(state="disabled")
        self.psychotestview.sideview.PsychoBtn1.config(state="disabled")
        self.model.stop = True
        self.psychotestview.sideview.StateLabel.config(text="zakończone", fg="red")
        self.thread1.join(0.5)

    def psychotestmessage(self, mqttuser, mqttpass, mqttclientid, mqttserver):

        try:
            self.model.psychotestconnecttoserver(mqttclientid, mqttuser, mqttpass, mqttserver, 1883, 10)
        except Exception:
            self.psychotestview.sideview.PsychoBtn1.config(state="normal")
            self.psychotestview.sideview.PsychoBtn2.config(state="disabled")
            messagebox.showerror(title="Niemożliwe połączenie!", message="Nieprawidłowy adres serwera")
        else:

            self.model.start = True
            self.model.start_sent = False

            self.model.psychotestauthentication()
            time.sleep(0.25)

            if not self.model.badauthentication:

                self.thread1.start()
                self.psychotestview.sideview.PsychoBtn1.config(state="disabled")
                self.psychotestview.sideview.PsychoBtn2.config(state="normal")
                self.psychotestview.sideview.StateLabel.config(text="uruchomione", fg="green")

            else:

                self.psychotestview.sideview.PsychoBtn1.config(state="normal")
                self.psychotestview.sideview.PsychoBtn2.config(state="disabled")
                messagebox.showerror(title="Niemożliwe połączenie!", message="Nieprawidłowy login lub hasło klienta!")
                self.model.badauthentication = False

    def setresultsonview(self):

        self.psychotestview.sideview.GSRShowContinuity.config(state="normal")
        self.psychotestview.sideview.GSRShowContinuity.delete(0, Tk.END)
        self.psychotestview.sideview.GSRShowContinuity.insert(0, self.model.GSRNumber)
        self.psychotestview.sideview.GSRShowContinuity.config(state="disabled")

        self.psychotestview.sideview.HeartRateContinuity.config(state="normal")
        self.psychotestview.sideview.HeartRateContinuity.delete(0, Tk.END)
        self.psychotestview.sideview.HeartRateContinuity.insert(0, self.model.HeartRateNumber)
        self.psychotestview.sideview.HeartRateContinuity.config(state="disabled")

        self.psychotestview.sideview.HeartRateShow.config(state="normal")
        self.psychotestview.sideview.HeartRateShow.delete(0, Tk.END)
        self.psychotestview.sideview.HeartRateShow.insert(0, self.model.HeartRateValue)
        self.psychotestview.sideview.HeartRateShow.config(state="disabled")

        self.psychotestview.sideview.GSRShow.config(state="normal")
        self.psychotestview.sideview.GSRShow.delete(0, Tk.END)
        self.psychotestview.sideview.GSRShow.insert(0, self.model.GSRValue)
        self.psychotestview.sideview.GSRShow.config(state="disabled")

        self.psychotestview.sideview.VoltageShow.config(state="normal")
        self.psychotestview.sideview.VoltageShow.delete(0, Tk.END)
        self.psychotestview.sideview.VoltageShow.insert(0, self.model.VoltageValue)
        self.psychotestview.sideview.VoltageShow.config(state="disabled")

        if self.model.LowVoltage:
            self.lowvoltagehandler()

        self.psychotestview.root.after(400, self.setresultsonview)



    def badauthenticationhandler(self):

        if self.model.badauthentication:
            self.psychotestview.sideview.PsychoBtn1.config(state="disabled")
            self.psychotestview.sideview.PsychoBtn2.config(state="disabled")
            messagebox.showerror(title="Niemożliwe połączenie!", message="Nieprawidłowe dane logowania do serwera!")

    def lowvoltagehandler(self):
        if not self.lowvoltagecalled:
            self.psychotestview.sideview.PsychoBtn2.config(state="disabled")
            messagebox.showerror(title="Alarm niskiego napięcia!", message="Przerwanie z powodu zbyt niskiego napięcia baterii!")
            self.psychotestview.sideview.StateLabel.config(text="zakończone", fg="red")
            self.lowvoltagecalled = True

    def run(self):
        self.psychotestview.root.mainloop()







