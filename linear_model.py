import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lmfit import Parameters
from lmfit.models import LinearModel

# Set font size
plt.rcParams.update({'font.size': 14})

# Import input data
try:
    plot_data = pd.read_csv('strain_vs_anisotropy_data.csv')
except FileNotFoundError:
    print("Error: CSV file not found.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: CSV file is empty or improperly formatted.")
    exit()

# Import linear model from lmfit
lin_model = LinearModel()

# Define initial parameter values
lin_params = Parameters()
lin_params.add('slope', value=0.3, min=0)
lin_params.add('intercept', value=0.1, min=0, max=1)

# Convert input data to numpy arrays
strain = plot_data['Strain'].to_numpy()
anisotropy = plot_data['Anisotropy'].to_numpy()

# Preallocate vectors for storing regression results
data_intercept = np.zeros(np.size(strain)-1)
data_slope = np.zeros(np.size(strain)-1)
data_r2 = np.zeros(np.size(strain)-1)

# Begin loop for plotting range of possible linear models
for i in range(2, np.size(strain)+1):

    # Define data range for linear and non-linear region
    strain_lin = strain[0:i]
    anisotropy_lin = anisotropy[0:i]
    strain_nonlin = strain[i:np.size(strain)]
    anisotropy_nonlin = anisotropy[i:np.size(anisotropy)]

    # Calculate linear regression with 2-standard deviation uncertainty range
    lin_result = lin_model.fit(anisotropy_lin, lin_params, x=strain_lin, method='least_squares')
    data_intercept[i-2] = lin_result.params['intercept'].value
    min_intercept = lin_result.params['intercept'].value - (2 * lin_result.params['intercept'].stderr)
    max_intercept = lin_result.params['intercept'].value + (2 * lin_result.params['intercept'].stderr)
    data_slope[i-2] = lin_result.params['slope'].value
    min_slope = lin_result.params['slope'].value - (2 * lin_result.params['slope'].stderr)
    max_slope = lin_result.params['slope'].value + (2 * lin_result.params['slope'].stderr)
    data_r2[i-2] = lin_result.rsquared

    # Create the linear model plots
    fig1 = plt.figure(layout="constrained")
    lin_points, = plt.plot(strain_lin, anisotropy_lin, 's', c='k', label='Linear range')
    nonlin_points, = plt.plot(strain_nonlin, anisotropy_nonlin, 's', c='#BE93D4', label='Non-linear range')
    trend, = plt.plot(strain_lin, lin_result.eval(lin_result.params, x=strain_lin), '--r', label='Linear model')
    plt.fill_between(strain_lin, lin_model.eval(x=strain_lin, slope=min_slope, intercept=min_intercept),
                     lin_model.eval(x=strain_lin, slope=max_slope, intercept=max_intercept), color="0.8", label=r'2-$\sigma$ uncertainty band')

    plt.xlabel('True Strain')
    plt.ylabel('Fluorescence Anisotropy')
    plt.axis((0, max(strain) * 1.2, 0, max(anisotropy) * 1.2))
    plt.legend(loc='lower right')
    plt.savefig(f'linear_outputs/jpg_files/linear_model_{i}.jpg', dpi=300)
    plt.savefig(f'linear_outputs/svg_files/linear_model_{i}.svg', dpi=300)
    plt.close()

    # Create residual plots
    fig2 = plt.figure(layout="constrained")

    residual_lin = lin_result.residual
    res_lin_points, = plt.plot(strain_lin, residual_lin, 's', c='k')

    plt.xlabel('True Strain')
    plt.ylabel('Residual')
    plt.xlim(-0.1, strain[i - 1] * 1.10)
    plt.ylim(min(-0.0025, min(residual_lin)*1.1), max(0.0025, max(residual_lin)*1.1))
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.savefig(f'linear_outputs/jpg_files/residuals_{i}.jpg', dpi=300)
    plt.savefig(f'linear_outputs/svg_files/residuals_{i}.svg', dpi=300)
    plt.close()
    print(f'\nLinear modelling result saved as "linear_model_{i}.jpg/.svg".'
          f'\nResidual result saved as "residual_{i}.jpg/.svg".'
          )

# Create R2 plot
fig3 = plt.figure(layout="constrained")

R2_points, = plt.plot(strain[1:(len(strain))], data_r2, 's', c='k')

plt.xlabel('Linear Approximation Range')
plt.ylabel(u'R\u00b2')
plt.xlim(0, max(strain) * 1.1)
plt.savefig(f'linear_outputs/jpg_files/r2_plot.jpg', dpi=300)
plt.savefig(f'linear_outputs/svg_files/r2_plot.svg')

print(u'\nR\u00b2 plot saved as "r2_plot.csv/.svg".')

# Save linear regression data
data_set = {'Slope': data_slope, 'Intercept': data_intercept, 'R2': data_r2
            }
regression_data = pd.DataFrame(data=data_set)
regression_data.to_csv('linear_outputs/linear_model_parameters.csv', index=False)

print('\nLinear regression data saved as "linear_regression_data.csv".')
print('\nLinear modelling results saved in directory "linear_outputs".')
