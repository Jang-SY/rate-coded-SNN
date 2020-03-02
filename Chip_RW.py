# Random_Walk
# Leakage RC time constant : 10ms = 0.01s
# Clock speed for random bit scan chain : 10us = 0.00001s
# Refractory time : 20us = 0.00002s
# Clock:Refractory:RC time constant = 1:2:1000
# Random walk step size : 20mV
# Resting potential : 0.7 V
# Threshold voltage : 0.37 V


import numpy as np
import math as m
from matplotlib import pyplot as plt

class Randomwalk(object):
    def __init__(self, LC = 1000, Vstep = 0.02, Vrest = 0.7, Vth = 0.37, re_time = 2, fire_count = 0, re_count = 0, enable_refractory = False):
        self.LC = LC
        self.Vstep = Vstep
        self.Vrest = Vrest
        self.Vth = Vth
        self.re_time = re_time                              # refractory time
        self.fire_count = fire_count
        self.re_count = re_count                            # refractory_count
        self.enable_refractory = enable_refractory
    
    def random_walk(self):
        # 50% 확률로 -Vstep or Vstep
        rand_num = np.random.rand()
        if rand_num >= 0.5:
            return self.Vstep
        else:
            return -self.Vstep

    def main(self, Vinit, num):
        time = []
        potential = []
        thres_pot = []
        rest_pot = []
        for i in range(num): 
            potential.append(Vinit)
            if not self.enable_refractory:
                Vcur = Vinit + self.random_walk()
                # threshold 이하면 fire 후 refractory time으로 들어감
                if Vcur <= self.Vth:
                    self.fire_count += 1
                    potential.append(Vcur)
                    Vcur = self.Vrest
                    self.enable_refractory = True
                # potential은 resting potential을 넘을 수 없음
                elif Vcur > self.Vrest:
                    Vcur = self.Vrest
                    potential.append(Vcur)
                # 위 2가지 경우가 아니면 R_leak에 의한 leak potential 계산
                else:
                    Vleak = Vcur-Vcur*(m.exp(-1/self.LC))
                    Vcur = Vcur + Vleak
                    if Vcur > self.Vrest:
                        Vcur = self.Vrest
                    potential.append(Vcur)
                
                Vinit = Vcur

            elif self.enable_refractory:
                potential.append(Vcur)
                self.re_count += 1
                if self.re_count == 2:
                    self.enable_refractory = False
                    self.re_count = 0

        for i in range(num*2):
            time.append(i)
            thres_pot.append(self.Vth)
            rest_pot.append(self.Vrest)

        # plt.plot(time, potential)
        # plt.plot(time, thres_pot)
        # plt.plot(time, rest_pot)
        # plt.xlabel('time')
        # plt.ylabel('Membrane_Potential')
        # plt.title('Membrane_Potential')
        # plt.show()

        print('The number of firing : ', self.fire_count)
        print('Firing rate : ', self.fire_count / num)
        return self.fire_count

def Thres_compare():
        potential = [0.02, 0.03, 0.04, 0.05, 0.06]
        count = []
        for i in potential:
            RW = Randomwalk(Vstep = i)
            fire = RW.main(0.5,100000)
            count.append(fire)
        plt.plot(potential, count,'rs--')
        plt.xlabel('Threshold_potential')
        plt.ylabel('The number of firing')
        plt.title('The number of firing vs Vth')
        plt.xlim(0.01, 0.07)
        plt.ylim(0, 3000)
        plt.show() 
        
def Vinit_compare():
        potential = [0.60, 0.55, 0.50, 0.45, 0.40]
        count = []
        for i in potential:
            RW = Randomwalk()
            fire = RW.main(i, 100000)
            count.append(fire)
        plt.plot(potential, count,'rs--')
        plt.xlabel('Initial_potential')
        plt.ylabel('The number of firing')
        plt.title('The number of firing vs Vinit')
        plt.xlim(0.30, 0.80)
        plt.ylim(0, 500)
        plt.show()  

def LC_compare():
        LC = [100, 500, 1000, 5000, 10000, 15000]
        count = []
        for i in LC:
            RW = Randomwalk(LC=i)
            fire = RW.main(0.5,100000)
            count.append(fire)
        plt.plot(LC, count,'rs--')
        plt.xlabel('Leakage constant')
        plt.ylabel('The number of firing')
        plt.title('The number of firing vs LC')
        plt.xlim(0, 16000)
        plt.ylim(0, 500)
        plt.show()  

if __name__ == "__main__":     
    # Thres_compare()
    # Vinit_compare()
    LC_compare()
