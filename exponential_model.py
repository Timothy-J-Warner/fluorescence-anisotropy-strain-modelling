import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lmfit import Model, Parameters

# Set font size
plt.rcParams.update({'font.size': 14})

# Import input data
try:
    plot_data = pd.read_csv('strain_vs_anisotropy_data.csv')
except FileNotFoundError:
    print("Error: 'strain_vs_anisotropy_data.csv' not found.")
    exit()
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty or improperly formatted.")
    exit()

# Convert input data to numpy arrays
strain = plot_data['Strain'].to_numpy()
anisotropy = plot_data['Anisotropy'].to_numpy()

# Define exponential function
def exponential(x, b, c, r0):
    return -(c - r0)*np.exp(-b * x) + c

# Convert to lmfit model
exp_model = Model(exponential)

# Define initial parameter values and bounds
exp_params = Parameters()
exp_params.add('b', value=0.01, min=0)
exp_params.add('c', value=0.5, min=-0.5, max=1)
exp_params.add('r0', value=anisotropy[0], vary=False, min=-0.5, max=1)

# Define x values for model plotting
x = np.linspace(min(strain), max(strain), 100)

# Compute non-linear regression
try:
    exp_result = exp_model.fit(anisotropy, exp_params, x=strain, method='least_squares')
except RuntimeError as e:
    print(f"Error during curve fitting: {e}")
    exit()
b = exp_result.params['b'].value
min_b = exp_result.params['b'].value - (2 * exp_result.params['b'].stderr)
max_b = exp_result.params['b'].value + (2 * exp_result.params['b'].stderr)
c = exp_result.params['c'].value
min_c = exp_result.params['c'].value - (2 * exp_result.params['c'].stderr)
max_c = exp_result.params['c'].value + (2 * exp_result.params['c'].stderr)
r0 = exp_result.params['r0'].value
residuals = exp_result.residual
r_squared = exp_result.rsquared
print(f'\nExponential model fitting statistics:\n\n{exp_result.fit_report()}')

# Create the exponential model plot
fig1 = plt.figure(layout="constrained")
points, = plt.plot(strain, anisotropy, 's', c='k')
trend = plt.plot(x, exp_result.eval(exp_result.params, x=x), '--r', label='Exponential model')
plt.fill_between(x, exp_model.eval(x=x, b=min_b, c=min_c, r0=r0),
                     exp_model.eval(x=x, b=max_b, c=max_c, r0=r0), color="0.8", label=r'2-$\sigma$ uncertainty band')

plt.xlabel('True Strain')
plt.ylabel('Fluorescence Anisotropy')
plt.axis((0, max(strain) * 1.2, 0, max(anisotropy) * 1.2))
plt.legend(loc='lower right')
plt.savefig(f'exponential_outputs/jpg_files/exponential_model.jpg', dpi=300)
plt.savefig(f'exponential_outputs/svg_files/exponential_model.svg')
plt.close()

# Create residual plot
fig2 = plt.figure(layout="constrained")

res_points, = plt.plot(strain, residuals, 's', c='k')

plt.xlabel('True Strain')
plt.ylabel('Residual')
plt.xlim(-0.1, max(strain) * 1.10)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.savefig(f'exponential_outputs/jpg_files/residuals.jpg', dpi=300)
plt.savefig(f'exponential_outputs/svg_files/residuals.svg')
plt.close()

print(f'\nExponential modelling result saved as "exponential_model.jpg/.svg".'
      f'\nResidual result saved as "residual.csv/.svg".'
      )

# save model parameters
output_description = ['b', 'c', 'r0', 'R2']
model_parameters = [b, c, r0, r_squared]
parameters_sd = [exp_result.params['b'].stderr, exp_result.params['c'].stderr, float("nan"), float("nan")]
max_model_parameters = [max_b, max_c, float("nan"), float("nan")]


output_data = {
        f'Model Parameters': output_description, u'Parameter Values': model_parameters,
    'Parameter Standard Deviation': parameters_sd,
}

df_outputs = pd.DataFrame(output_data)
df_outputs.to_csv(f"exponential_outputs/exponential_model_parameters.csv", index=False)

print('\nModel parameters saved as "exponential_model_parameters.csv".')
print('\nExponential modelling results saved in directory "exponential_outputs".')
