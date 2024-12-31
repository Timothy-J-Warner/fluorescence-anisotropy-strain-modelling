# Tool for modelling relationship between fluorescence anisotropy and true strain in polymer films

## Table of Contents

- About The Project
- Publication Details
- Built With
- Features
- Version History
- Installation
- Usage
- License
- Contact
- Acknowledgements

## About The Project

The project contains two python scripts used to model the relationship between fluorescence anisotropy and true strain in 
polymer films containing fluorescent nanocrystals. It was developed for the publication "Effect of 
luminescent nanocrystal alignment on fluorescence anisotropy and light guiding in polymer films". One is a script to 
model fluorescence anisotropy vs true strain data with an exponential model and the other models the same data with a 
series of linear models.

When using this tool, please cite: Warner, T., Rinaudo, M., Xu, Y., Han, J., Ashokan, A., Kirkwood, N., Widmer-Cooper, A., 
Smith, T. A., Ghiggino, K. P., & Rosengarten, G. (2025). Effect of luminescent nanocrystal alignment on fluorescence 
anisotropy and light guiding in polymer films. Optical Materials, 159, 116606. https://doi.org/10.1016/j.optmat.2024.116606

## Publication Details

- Title: "Effect of luminescent nanocrystal alignment on fluorescence anisotropy and light guiding in polymer films"
- Authors: Timothy Warner, Michael Rinaudo, Yang Xu, Jiho Han, Arun Ashokan, Nicholas Kirkwood, Asaph Widmer-Cooper, 
Trevor A. Smith, Kenneth P. Ghiggino*, and Gary Rosengarten
- Corresponding Author: Kenneth P. Ghiggino (ghiggino@unimelb.edu.au)
- Year: 2025
- Journal: Optical Materials
- Volume: 159
- Pages: 116606
- ISSN: 0925-3467

### Built With

- [Python](https://www.python.org/) - A high-level programming language used for general-purpose programming.

## Features

- Feature 1: Exponential modelling of fluorescence anisotropy vs true strain data.
- Feature 2: Fit and analyze the same data using a series of linear fits.

## Version History

### Release 1 (v1.0.0)

This release represents the software at the time of publication of "Effect of luminescent nanocrystal alignment on fluorescence 
anisotropy and light guiding in polymer films". This includes the modelling methodology presented in the article as well
as the formatting of the figures. The equation used for exponential modelling of the data is:

$$r = -ae^{-b\epsilon} + c$$

where r is the fluorescence anisotropy of the film, $\epsilon$ is the true strain of the film and a, b, and c are fitting parameters.

### Release 2 (v1.1.0)

This release updates the initial release by improving the uncertainty of the exponential model and formatting of the 
figures. The confidence intervals are now represented by a shaded area, instead of dotted lines. The modelling is now 
performed with the 'lmfit' python package instead of the 'SciPy' package. Additionally, the uncertainty in the model is 
reduced by applying a boundary condition of $a = c - r_0$, where $r_0$ is the anisotropy of the unstretched film. 
The exponential term has a value of 1 for a true strain value of 0, therefore the y-intercept is equal to c - a. 
Consequently, the boundary condition stated above can be applied. The new equation used for exponential modelling is 
therefore:

$$r = -(c - r_0)e^{-b\epsilon} + c$$

where r is the fluorescence anisotropy of the film, $\epsilon$ is the true strain of the film, $r_0$ is the fluorescence 
anisotropy of the unstretched film, and b and c are fitting parameters.

## Getting Started

### Prerequisites

- Python 3.7+
- Libraries:
  - numpy
  - pandas
  - matplotlib
  - lmfit

### Installation

Access the project and releases on GitHub at https://github.com/Timothy-J-Warner/fluorescence-anisotropy-vs-strain-modelling

## Usage

- (Recommended) Open the software folder in your code editor or IDE of choice, such as Visual Studio Code or PyCharm.
- Modify the "strain_vs_anisotropy_data.csv" file with your dataset.
- Choose your model:
  - Run "exponential_model.py" to model exponential relationship.
  - Run "linear_model.py" to model a series of possible linear fits.
- View the results in the outputs folders.

## Licence

This software is licensed under the MIT License. See LICENSE for more details.

## Contact

- GitHub: Timothy-J-Warner

## Acknowledgements

- Project contributors: Timothy Warner, Negar Takhsha
