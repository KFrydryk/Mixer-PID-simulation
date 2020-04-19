import matplotlib.pyplot as plt
import randompy
import matplotlib
from matplotlib.widgets import TextBox
import numpy as np

V = 0
CA = 0


class PID:

    def __init__(self, P=1.0, I=0.0, D=0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.set_point = 0.0
        self.error = 0.0
        self.Derivator = 0.0
        self.Integrator = 0.0
        self.Integrator_max = 500
        self.Integrator_min = -500

    def reset(self):
        self.error = 0.0
        self.Derivator = 0.0
        self.Integrator = 0.0
        self.Integrator_max = 500
        self.Integrator_min = -500

    def update(self, current_value):

        self.error = self.set_point - current_value
        self.P_val = self.Kp * self.error
        self.D_val = self.Kd * (self.error - self.Derivator)
        self.Derivator = self.error
        self.Integrator += self.error
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        if self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min
        self.I_val = self.Integrator * self.Ki
        PID = self.P_val + self.I_val + self.D_val
        return PID

    def setPoint(self, set_point):
        self.set_point = set_point
        self.Integrator = 0
        self.Derivator = 0


class Obiekt:

    def __init__(self, CA1=0.2, CA2=1, Q1=2, Q2=1, Q3=1, Tp=0.1):

        self.V = 0
        self.CA = 0
        self.CA1 = CA1
        self.CA2 = CA2
        self.Q1 = Q1
        self.Q2 = Q2
        self.Q3 = Q3
        self.Tp = Tp

    def reset(self):
        self.V = 0
        self.CA = 0

    def liczobj(self, v):

        v = v + self.Q1 * self.Tp + self.Q2 * self.Tp - self.Q3 * self.Tp
        return v

    def liczstez(self, c):

        c = (self.Q1 * (self.CA1 - c) + self.Q2 * (self.CA2 - c)) * self.Tp / self.V + c
        return c

    def licz(self, n):

        if self.Q2 > 10:
            self.Q2 = 10
        if self.Q3 > 10:
            self.Q3 = 10
        if self.Q2 < 0:
            self.Q2 = 0
        if self.Q3 < 0:
            self.Q3 = 0

        self.V = self.liczobj(self.V)
        self.CA = self.liczstez(self.CA)

        if self.V < 0:
            self.V = 0.01
            self.CA = 0

        print("t: " + str(self.Tp * n) + " V: " + str(self.V) + " C: " + str(self.CA))


def rysuj():
    wykresy.clf()
    stez = [0]
    t = [0]
    r = [0]
    sp = [reg.set_point]
    for n in range(0, 1000):
        Ob.Q2 = reg.update(Ob.CA)
        Ob.licz(n)
        stez.append(Ob.CA)
        t.append(n * Ob.Tp)
        r.append(Ob.Q2)
        sp.append(reg.set_point)

    ax1 = plt.subplot2grid((2, 3), (0, 0), colspan=2)
    plt.plot(t, r, 'g')
    plt.ylabel('regulator')
    ax2 = plt.subplot2grid((2, 3), (1, 0), colspan=2)
    plt.plot(t, stez, 'r', t, sp, 'b')
    plt.ylabel('r-stez, b-cel')
    plt.ylabel('r-stez, b-cel')

    Q1box = plt.axes([0.7, 0.8, 0.2, 0.075])
    text_boxQ1 = TextBox(Q1box, 'Q1', initial=str(Ob.Q1))
    text_boxQ1.on_submit(submitQ1)

    Q3box = plt.axes([0.7, 0.7, 0.2, 0.075])
    text_boxQ3 = TextBox(Q3box, 'Q3', initial=str(Ob.Q3))
    text_boxQ3.on_submit(submitQ3)

    CA1box = plt.axes([0.7, 0.6, 0.2, 0.075])
    text_boxCA1 = TextBox(CA1box, 'CA1', initial=str(Ob.CA1))
    text_boxCA1.on_submit(submitCA1)

    CA2box = plt.axes([0.7, 0.5, 0.2, 0.075])
    text_boxCA2 = TextBox(CA2box, 'CA2', initial=str(Ob.CA2))
    text_boxCA2.on_submit(submitCA2)

    Pbox = plt.axes([0.7, 0.4, 0.2, 0.075])
    text_boxP = TextBox(Pbox, 'KP', initial=str(reg.Kp))
    text_boxP.on_submit(submitKp)

    Ibox = plt.axes([0.7, 0.3, 0.2, 0.075])
    text_boxI = TextBox(Ibox, 'KI', initial=str(reg.Ki))
    text_boxI.on_submit(submitKi)

    Dbox = plt.axes([0.7, 0.2, 0.2, 0.075])
    text_boxD = TextBox(Dbox, 'KD', initial=str(reg.Kd))
    text_boxD.on_submit(submitKd)

    Buttonbox = plt.axes([0.7, 0.1, 0.2, 0.075])
    Button_box = plt.Button(Buttonbox, 'Rysuj')
    Button_box.on_clicked(submitButton)

    plt.show()


def submitQ1(text):
    print(text)
    # reg.reset()
    # Ob.reset()
    Ob.Q1 = float(text)
    # rysuj()


def submitCA1(text):
    print(text)
    Ob.CA1 = float(text)


def submitCA2(text):
    print(text)
    Ob.CA2 = float(text)


def submitQ3(text):
    print(text)
    Ob.Q3 = float(text)


def submitKp(text):
    print(text)
    reg.Kp = float(text)


def submitKi(text):
    print(text)
    reg.Ki = float(text)


def submitKd(text):
    print(text)
    reg.Kd = float(text)


def submitButton(text):
    reg.reset()
    Ob.reset()
    rysuj()


reg = PID(9, 4, 1)
reg.setPoint(0.8)
Ob = Obiekt()
stez = [0]
t = [0]
r = [0]
sp = [reg.set_point]

wykresy = plt.figure(1, figsize=(12, 6))

rysuj()

plt.show()
