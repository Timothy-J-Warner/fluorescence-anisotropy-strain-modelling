import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import t

# set font size
plt.rcParams.update({'font.size': 14})

# import input data
try:
    plot_data = pd.read_csv('strain_vs_anisotropy_data.csv')
except FileNotFoundError:
    print("Error: 'strain_vs_anisotropy_data.csv' not found.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty or improperly formatted.")
    exit()

# convert input data to numpy arrays
strain = plot_data['Strain'].to_numpy()
polarisation = plot_data['Anisotropy'].to_numpy()

# define exponential function
def func(x, a, b, c):
    return -a * np.exp(-b * x) + c

# set parameter bounds and guesses
parameter_bounds = ([0, 0, -0.5], [0.5, np.inf, 1])
initial_guess = [0.25, 0.01, 0.5]
maxfev = 800

# calculate non-linear regression
try:
    popt, pcov = curve_fit(func, strain, polarisation, p0=initial_guess, bounds=parameter_bounds, maxfev=maxfev)
except RuntimeError as e:
    print(f"Error during curve fitting: {e}")
    exit()
residuals = polarisation - func(strain, *popt)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((polarisation - np.mean(polarisation)) ** 2)
r_squared = 1 - (ss_res / ss_tot)

alpha = 0.05 # 95% confidence interval = 100*(1-alpha)

x = np.linspace(0, max(strain), 100)

n = len(strain)  # number of data points
p = len(popt)  # number of parameters

dof = max(0, n - p)  # number of degrees of freedom

# student-t value for the dof and confidence level
tval = t.ppf(1.0-alpha/2., dof)

# List to store confidence intervals
confidence_intervals = []

# Calculate confidence intervals
for i, (p, var) in enumerate(zip(popt, np.diag(pcov))):
    sigma = var**0.5  # Standard deviation
    lower_bound = p - sigma * tval
    upper_bound = p + sigma * tval
    confidence_intervals.append((lower_bound, upper_bound))


# create the exponential model plot
fig1 = plt.figure(layout="constrained")
points, = plt.plot(strain, polarisation, 's', c='k', label='Exponential Fit')
exp_trend = plt.plot(x, func(x, *popt), '--', c='r')
upper_limit = plt.plot(x, func(x, confidence_intervals[0][1], popt[1], confidence_intervals[2][1]), ':', c='r')
lower_limit = plt.plot(x, func(x, confidence_intervals[0][0], popt[1], confidence_intervals[2][0]), ':', c='r')

plt.xlabel('True Strain')
plt.ylabel('Fluorescence Anisotropy')
plt.axis((0, max(strain) * 1.2, 0, max(polarisation) * 1.2))
plt.savefig(f'exponential_outputs/jpg_files/exponential_model.jpg', dpi=300)
plt.savefig(f'exponential_outputs/svg_files/exponential_model.svg')

plt.close()

# save model parameters
model_param = np.concatenate((popt, [r_squared]))
output_description = ['a', 'b', 'c', 'R2']

output_data = {
        f'Model Parameters': output_description, u'Parameter Values': model_param
}

df_outputs = pd.DataFrame(output_data)
df_outputs.to_csv(f"exponential_outputs/exponential_model_parameters.csv", index=False)

# create residual plot
fig2 = plt.figure(layout="constrained")

residual = polarisation - func(strain, *popt)
res_points, = plt.plot(strain, residual, 's', c='k')


plt.xlabel('True Strain')
plt.ylabel('Residual')
plt.xlim(-0.1, max(strain) * 1.10)
plt.axhline(0, color='black', linewidth=.5)
plt.savefig(f'exponential_outputs/jpg_files/residuals.jpg', dpi=300)
plt.savefig(f'exponential_outputs/svg_files/residuals.svg')

plt.close()

print(f'\nExponential modelling result saved as "exponential_model.jpg/.svg".'
      f'\nResidual result saved as "residual.csv/.svg".'
      )

print('\nModel parameters saved as "exponential_model_parameters.csv".')

print('\nExponential modelling results saved in directory "exponential_outputs".')
