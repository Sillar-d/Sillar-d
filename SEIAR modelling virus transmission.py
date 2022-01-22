# Daniel Sillar 26879026
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# constant conditions
N = 1000
transmission_rate = 0.001
infectious_rate = 0.1
recovery_rate = 0.3
birth_rate = 12  # approximate birth rate in australia for 2019 was 0.012
death_rate = 0.007  # approximate death rate in australia for 2019
asymptomatic_recovery_rate = 0.4        # must be > recovery rate
asymptomatic_transmission_rate = 4/3000     # must be < infectious rate
p = 0.5


# ODE
def seiar_system(P, t=0):
    return np.array([birth_rate - P[0]*P[2]*transmission_rate - P[0]*P[3]*asymptomatic_transmission_rate
                     - P[0]*death_rate,
                    P[0]*P[2]*transmission_rate + P[0]*P[3]*asymptomatic_transmission_rate
                     - P[1]*infectious_rate - P[1]*death_rate,
                    P[1]*infectious_rate*p - P[2]*recovery_rate - P[2]*death_rate,
                    P[1]*infectious_rate*(1-p) - P[3]*asymptomatic_recovery_rate - P[3]*death_rate,
                    P[2]*recovery_rate + P[3]*asymptomatic_recovery_rate - P[4]*death_rate])


# set function bounds
t = np.linspace(0, 200, 1000)
P0 = np.array([N - 1, 1, 0, 0, 0])
P = odeint(seiar_system, P0, t)

# split populations
susceptible = []
exposed = []
infected = []
asymptomatic = []
recovered = []
total_pop = []
both_infected = []
for i in range(len(P)):
    susceptible.append(P[i][0])
    exposed.append(P[i][1])
    infected.append(P[i][2])
    asymptomatic.append(P[i][3])
    recovered.append(P[i][4])
    both_infected.append(P[i][2] + P[i][3])
    total_pop.append(P[i][0] + P[i][1] + P[i][2] + P[i][3] + P[i][4])

# plot
plt.plot(t, susceptible, color='b', label='susceptible')
plt.plot(t, exposed, color='tab:orange', label='exposed')
plt.plot(t, infected, color='r', label='infected')
plt.plot(t, asymptomatic, color='peru', label='asymptomatic')
plt.plot(t, both_infected, color='maroon', label='asymptomatic + infected')
plt.plot(t, recovered, color='g', label='recovered')
plt.plot(t, total_pop, color='k', label='total population')
plt.legend()
plt.xlabel('time')
plt.ylabel('population')
plt.title('SEIAR model')
plt.show()
