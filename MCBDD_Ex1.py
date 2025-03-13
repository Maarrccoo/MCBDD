# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14:54:39 2025

@author: Marco
"""
import numpy as np
import matplotlib.pyplot as plt

def infection_prob():
    while True:
        user_input = float(input("enter number between 0.00001 and 0.5 -----> "))
        if 0.00001 <= user_input <= 0.5:
            return user_input
        else:
            print("invalid input pleas try again")
        

infected = infection_prob()

specificity = np.array((0.99,0.999,0.9999,0.99999))

sensitiviy = 0.99

Fred_actually_infected = np.zeros_like(specificity)

def Fred_is_infected(infected,specificity,sensitiviy):
    Fred_actually_infected = (sensitiviy * infected) / (sensitiviy * infected + (1 - specificity ) * (1 - infected))
    return Fred_actually_infected

plt.plot(Fred_is_infected(infected, specificity, sensitiviy),"-")
plt.ylim(0, 1)
plt.xlabel("specificity array index")
plt.ylabel("P(Infected | Positive Test)" )
plt.show()
print(Fred_is_infected(infected, specificity, sensitiviy))

# method 2
population = 100000
int_infected = int(population * infected)
healthy = population - int_infected

positive = int(sensitiviy * int_infected)
false_negative = int_infected - positive

negative = int(specificity[0] * healthy)

false_postive = healthy - negative

print(positive)
print(false_postive)
print(negative)
print(false_negative)

p_Fred_is_infected = positive / (false_postive + positive)

print(p_Fred_is_infected)

#Both methods deliver the same results. Method two is a more intuitive way of solving the problem, which can be done using the table shown in the lecture.
#Method one is the more mathematical approach to solving the problem.