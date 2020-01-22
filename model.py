import time
import paho.mqtt.client as mqtt
import csv


class PsychoTest:

    def __init__(self):

        self.HeartRateValue = 0
        self.VoltageValue = 0
        self.GSRValue = 0

        self.GSRNumber = 0
        self.HeartRateNumber = 0

        self.HeartRateDate = 0
        self.GSRDate = 0

        self.start = False
        self.stop = False
        self.start_sent = False

        self.rccode = 0
        self.badauthentication = False

        self.divided = '\0'
        self.GSRFile = 0
        self.HRFile = 0

        self.HRwrite = False
        self.GSRwrite = False

        self.LowVoltage = False

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('message received')

    def on_connect(self, client, userdata, flags, rc):
        print("on connect with result code " + str(rc))
        self.rccode = rc
        if rc == 0:
            print("connected")
            print(self.rccode)
        elif rc == 5:
            print("connection impossible - bad authentication")
            self.badauthentication = True

    def on_publish(self, client, userdata, mid):
        print('data sent')

    def on_message(self, client, userdata, message):
        print("Received message: " + str(message.payload) + "on Topic: " + message.topic + " with QoS " + str(message.qos))
        if message.topic == 'GSRTopic':
            divided = (str(message.payload)).replace("'", ";")
            divided = divided.split(';')
            self.gsrvaluesmanager(divided[1], (divided[2]), divided[3])

        if message.topic == 'HRTopic':
            divided = (str(message.payload)).replace("'", ";")
            divided = divided.split(';')
            self.heartratevaluesmanager(divided[1], divided[2], divided[3])

        if message.topic == 'VoltageTopic':
            divided = (str(message.payload)).replace("'", ";")
            divided = divided.split(';')
            self.voltagevaluesmanager(divided[3])

    def on_disconnect(self, client, userdata, rc):
        if rc == 0 and self.start:
            print("disconnect clean")
        elif rc != 0 and self.start:
            #print(rc)
            print("violent disconnect")

    def psychotestconnecttoserver(self, clientid, username, passwd, brokername, portnum, rettime):

        self.client = mqtt.Client(client_id=clientid, clean_session=True, userdata=None)
        self.client.username_pw_set(username, passwd)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(brokername, portnum, rettime)

        return self.client

    def psychotestauthentication(self):

        print(self.badauthentication)
        self.client.loop_start()
        time.sleep(0.1)

        if self.start and self.badauthentication:
            self.client.loop_stop()
            return

    def psychotestmessageserver(self, control, pubtpcnm, subtpcnm1, subtpcnm2, subtpcnm3):

        with open("GSRFile.csv", mode="w") as self.GSRFile:
            gsrwriter = csv.writer(self.GSRFile, delimiter=';')
            gsrwriter.writerow([str("numer probki"), str("godzina"), str("wartosc")])

        with open("HRFile.csv", mode="w") as self.HRFile:
            hrwriter = csv.writer(self.HRFile, delimiter=';')
            hrwriter.writerow([str("numer probki"), str("godzina"), str("wartosc")])

        while True:

            if self.start and not self.start_sent:
                self.client.publish(pubtpcnm, 'start', 2, False)
                self.start_sent = True
                time.sleep(0.05)

            if self.start:
                self.client.subscribe(subtpcnm1, 2)
                time.sleep(0.05)

            if self.HRwrite:
                self.HRFile = open("HRFile.csv", mode='a', newline='')

                with self.HRFile:
                    hrwriter = csv.writer(self.HRFile, delimiter=';')
                    hrwriter.writerow([str(self.HeartRateNumber), str(self.HeartRateDate), str(self.HeartRateValue)])

                self.HRwrite = False
                time.sleep(0.05)

            if self.start:
                self.client.subscribe(subtpcnm2, 2)
                time.sleep(0.05)

            if self.GSRwrite:
                self.GSRFile = open("GSRFile.csv", mode='a', newline='')
                with self.GSRFile:
                    gsrwriter = csv.writer(self.GSRFile, delimiter=';')
                    gsrwriter.writerow([str(self.GSRNumber), str(self.GSRDate), str(self.GSRValue)])

                self.GSRwrite = False
                time.sleep(0.05)

            if self.start:
                self.client.subscribe(subtpcnm3, 2)
                time.sleep(0.05)

            if self.stop:
                self.client.publish(pubtpcnm, 'stop', 2, False)
                time.sleep(0.5)
                self.client.loop_stop()
                self.client.disconnect()
                break

        if self.stop and not self.badauthentication:
            control.set()

    def gsrvaluesmanager(self, controlnumber, date, value):
        self.GSRNumber = controlnumber
        self.GSRDate = date
        self.GSRValue = value
        self.GSRwrite = True

    def heartratevaluesmanager(self, controlnumber, date, value):

        self.HeartRateNumber = controlnumber
        self.HeartRateValue = value
        self.HeartRateDate = date
        self.HRwrite = True

    def voltagevaluesmanager(self, value):
        self.VoltageValue = value
        if float(self.VoltageValue) < 6.8:
            self.stop = True
            self.LowVoltage = True


