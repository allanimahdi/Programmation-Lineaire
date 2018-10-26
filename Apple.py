from pulp import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import seaborn as sns

sns.set_color_codes('deep')


# Startup -->

# AppMobile = 60000 $  x1
# AppWeb = 40000 $   x2

# Appmobile 40h de developpement
# AppWeb 20h de developpement

# AppMobile necessite 15 Employee #
# ### AppWeb necessite 20 Employee ###

# Maximum d'heure de travail / mois = 140 h

problem = LpProblem("Startup", LpMaximize)


x1 = LpVariable("x1", lowBound=0)
x2 = LpVariable("x2", lowBound=0)

problem += 60*x1 + 40*x2            # profit

problem += 40*x1 + 20*x2 <= 140     # contrainte de temps

problem += 15*x1 + 20*x2 <= 100       # contrainte d'employee

print problem

status = problem.solve()
print LpStatus[status]

print "application mobile : ", value(x1)
print "application web : ", value(x2)
print value(problem.objective)

# Creation de Courbes

fig, ax = plt.subplots(figsize=(10, 10))
x1 = np.linspace(0, 100)

# Contrainte de Temps x2 <= 140/20 - 40x1/20
plt.plot(x1, 140/20 - 40*x1/20, linewidth=3, label='Contrainte de temps')
plt.fill_between(x1, 0, 140/20 - 40*x1/20, alpha=0.1)

# Contrainte de employee: x2 <= 100/20 - 15x1/20
plt.plot(x1, 100/20 - 15*x1/20, linewidth=3, label='Contrainte deffectif')
plt.fill_between(x1, 0, 100/20 - 15*x1/20, alpha=0.1)

# Contrainte de negativitee
plt.plot(np.zeros_like(x1), x1, linewidth=3, label='$x_2$ restriction')
plt.plot(x1, np.zeros_like(x1), linewidth=3, label='$x_1$ restriction')

# Coloration de zone de faisabilite
path = Path([
    (0., 0.),
    (3.5, 0.),  # C1 pour X2 = 0
    (1.6, 3.8),
    (0, 5),     # C2 pour X1 = 0
    (0., 0.)])
patch = PathPatch(path, label='Zone de fesabilite', alpha=0.5)
ax.add_patch(patch)

# Labels and stuff
plt.xlabel('Application Mobile')
plt.ylabel('Application Web')
plt.xlim(-0.5, 10)
plt.ylim(-0.5, 10)
plt.legend()
plt.show()

