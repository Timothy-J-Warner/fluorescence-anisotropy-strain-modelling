import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

# set font size
plt.rcParams.update({'font.size': 14})

# import input data
plot_data = pd.read_csv('strain_vs_anisotropy_data.csv')

# convert input data to numpy arrays
strain = plot_data['Strain'].to_numpy()
polarisation = plot_data['Anisotropy'].to_numpy()

# preallocate vectors
data_intercept = np.zeros(np.size(strain)-2)
data_slope = np.zeros(np.size(strain)-2)
data_r2 = np.zeros(np.size(strain)-2)

# begin loop for plotting range of possible linear models
for i in range(2, np.size(strain)):
    # define data range for linear and non-linear region
    strain_lin = strain[0:i]
    strain_nonlin = strain[i:np.size(strain)]
    anisotropy_lin = polarisation[0:i]
    anisotropy_nonlin = polarisation[i:np.size(polarisation)]

    # calculate linear regression
    lin_reg = stats.linregress(strain_lin, anisotropy_lin)
    data_intercept[i-2] = lin_reg.intercept
    data_slope[i - 2] = lin_reg.slope
    data_r2[i-2] = lin_reg.rvalue ** 2

    # create the exponential model plots
    fig1 = plt.figure()
    lin_points, = plt.plot(strain_lin, anisotropy_lin, 's', c='k', label='Linear Range')
    nonlin_points, = plt.plot(strain_nonlin, anisotropy_nonlin, 's', c='0.6', label='Non-linear Range')
    trend, = plt.plot(strain, lin_reg.slope * strain + lin_reg.intercept, '--r')
    upper_trend, = plt.plot(strain, lin_reg.slope * strain + lin_reg.stderr * strain +
                            lin_reg.intercept + lin_reg.intercept_stderr, ':r')
    lower_trend, = plt.plot(strain, lin_reg.slope * strain - lin_reg.stderr * strain +
                            lin_reg.intercept - lin_reg.intercept_stderr, ':r')

    plt.xlabel('True Strain')
    plt.ylabel('Fluorescence Anisotropy')
    plt.axis((0, max(strain) * 1.2, 0, max(polarisation) * 1.2))
    plt.legend(loc='lower right')
    plt.savefig(f'linear_outputs/jpg_files/linear_model_{i}.jpg', dpi=300)
    plt.savefig(f'linear_outputs/svg_files/linear_model_{i}.svg', dpi=300)

    plt.close()

    # create residual plots
    fig2 = plt.figure()

    residual_lin = polarisation[0:i] - (lin_reg.slope * strain[0:i] + lin_reg.intercept)
    residual_nonlin = polarisation[i:np.size(polarisation)] - (lin_reg.slope * strain[i:np.size(strain)] +
                                                               lin_reg.intercept)

    res_lin_points, = plt.plot(strain_lin, residual_lin, 's', c='k', label='Linear Range')

    plt.xlabel('True Strain')
    plt.ylabel('Residual')
    plt.xlim(-0.1, strain[i - 1] * 1.10)
    plt.axhline(0, color='black', linewidth=.5)
    plt.savefig(f'linear_outputs/jpg_files/residuals_{i}.jpg', dpi=300)
    plt.savefig(f'linear_outputs/svg_files/residuals_{i}.svg', dpi=300)

    plt.close()

# create R2 plot
fig3 = plt.figure(layout="constrained")

R2_points, = plt.plot(strain[1: 8], data_r2, 's', c='k', label='Linear Range')

plt.xlabel('Linear Approximation Range')
plt.ylabel(u'R\u00b2')
plt.xlim(0, 1.895)
plt.savefig(f'linear_outputs/jpg_files/r2_plot.jpg', dpi=300)
plt.savefig(f'linear_outputs/svg_files/r2_plot.svg')

# save linear regression data
data_set = {'Slope': data_slope, 'Intercept': data_intercept, 'R2': data_r2
            }

regression_data = pd.DataFrame(data=data_set)

regression_data.to_csv('linear_outputs/linear_regression_data.csv', index=False)
