# Tool for modelling relationship between fluorescence anisotropy and true strain in polymer films

## Table of Contents

- About The Project
- Publication Details
- Built With
- Features
- Installation
- Usage
- License
- Contact
- Acknowledgements

## About The Project

The project contains two scripts used to model the relationship between fluorescence anisotropy and true strain in 
polymer films containing fluorescent nanocrystals. It was developed for the publication "Effect of 
luminescent nanocrystal alignment on fluorescence anisotropy and light guiding in polymer films". One is a script to 
model fluorescence anisotropy vs true strain data with an exponential model and the other models the same data with a 
series of linear models.
\
\
Please cite "Effect of luminescent nanocrystal alignment on fluorescence anisotropy and light guiding in polymer films"
when using this tool.

## Publication Details

Title: "Effect of luminescent nanocrystal alignment on fluorescence anisotropy and light guiding in polymer films"
\
\
Authors: Timothy Warner, Michael Rinaudo, Yang Xu, Jiho Han, Arun Ashokan, Nicholas Kirkwood, Asaph Widmer-Cooper, 
Trevor A. Smith, Kenneth P. Ghiggino*, and Gary Rosengarten
\
\
Corresponding Author: Kenneth P. Ghiggino (ghiggino@unimelb.edu.au)

### Built With

- [Python](https://www.python.org/) - A high-level programming language used for general-purpose programming.

## Features

- Feature 1: Exponential modelling of fluorescence anisotropy vs true strain data.
- Feature 2: Fit and analyze the same data using a series of linear models.

## Getting Started

### Prerequisites

- Python 3.7+
- Libraries:
  - numpy
  - pandas
  - matplotlib
  - scipy

### Installation

Access the project and releases on GitHub at https://github.com/Timothy-J-Warner/fluorescence-anisotropy-vs-strain-modelling

## Usage

- Modify the "strain_vs_anisotropy_data.csv" file with your dataset.
- Choose your model:
  - Run "exponential_model.py" to model exponential relationship.
  - Run "linear_model.py" to model a series of possible linear relationships.
- View the results in the outputs folders.

## Licence

This software is licensed under the MIT License. See LICENSE for more details.

## Contact

Timothy Warner - warnet2@mcmaster.ca
GitHub: Timothy-J-Warner

## Acknowledgements

- Project contributors: Timothy Warner, Negar Takhsha
