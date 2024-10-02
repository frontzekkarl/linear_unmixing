# Linear Unmixing of Human Brain Autofluorescence

This repository contains code for performing linear unmixing of autofluorescence in human brain tissue using **Independent Component Analysis (ICA)** and **Non-negative Matrix Factorization (NMF)**. These techniques are used to separate autofluorescent signals from biological signals in multi-channel fluorescence microscopy images.

## Features

- Spectral unmixing using ICA and NMF.
- Rolling ball background subtraction.
- Colocalization analysis using Pearson's Correlation Coefficient.

## Requirements

The following Python packages are required to run the code:

- `numpy`
- `matplotlib`
- `scipy`
- `scikit-learn`
- `scikit-image`

You can install the necessary dependencies with:

```bash
pip install numpy matplotlib scipy scikit-learn scikit-image
