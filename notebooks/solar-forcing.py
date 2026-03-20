# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import os
import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import xarray as xr

# %%
# load in CMIP6 solar data
cmip6 = xr.load_dataset('../data/solarforcing-ref-mon_input4MIPs_solar_CMIP_SOLARIS-HEPPA-3-2_gn_185001-229912.nc')

# %%
cmip6

# %%
# get array of month lengths
monthlengths = (cmip6.time_bnds[:, 1] - cmip6.time_bnds[:, 0]).astype('timedelta64[D]') / np.timedelta64(1, 'D')

# %%
# now we want to average annually by month lengths
# not pretty :)

cmip6_tsi_annual = np.ones(cmip6.tsi.shape[0]//12) * np.nan
for year in np.arange(len(cmip6_tsi_annual)):
    cmip6_tsi_annual[year] = np.sum(cmip6.tsi[year*12:year*12+12] * monthlengths[year*12:year*12+12]) / np.sum(monthlengths[year*12:year*12+12])

# %%
# cmip6_tsi_annual = np.ones(cmip6.tsi.shape[0]//12) * np.nan
# cmip6_tsi_annual
# cmip6.tsi[year*12:year*12+12]
# monthlengths[year*12:year*12+12]
# np.sum(monthlengths[year*12:year*12+12])
# cmip6.tsi[year*12:year*12+12] * monthlengths[year*12:year*12+12] / np.sum(monthlengths[year*12:year*12+12])

# %%
cmip6_tsi_annual

# %%
pl.plot(np.arange(1850.5, 2300), cmip6_tsi_annual)

# %%
# load in CMIP7 solar data
cmip7 = xr.load_dataset('../data/multiple_input4MIPs_solar_CMIP_SOLARIS-HEPPA-CMIP-4-6_gn_185001-202312.nc')

# %%
cmip7

# %%
monthlengths = (cmip7.time_bnds[:, 1] - cmip7.time_bnds[:, 0]).astype('timedelta64[D]') / np.timedelta64(1, 'D')

# %%
cmip7_tsi_annual = np.ones(cmip7.tsi.shape[0]//12) * np.nan
for year in np.arange(len(cmip7_tsi_annual)):
    cmip7_tsi_annual[year] = np.sum(cmip7.tsi[year*12:year*12+12] * monthlengths[year*12:year*12+12]) / np.sum(monthlengths[year*12:year*12+12])

# %%
# cmip7_tsi_annual = np.ones(cmip7.tsi.shape[0]//12) * np.nan
# cmip7_tsi_annual
# cmip7.tsi[year*12:year*12+12]
# monthlengths[year*12:year*12+12]
# np.sum(monthlengths[year*12:year*12+12])
# cmip7.tsi[year*12:year*12+12] * monthlengths[year*12:year*12+12] / np.sum(monthlengths[year*12:year*12+12])

# %%
cmip7_tsi_annual

# %%
pl.plot(np.arange(1850.5, 2300), cmip6_tsi_annual)
pl.plot(np.arange(1850.5, 2024), cmip7_tsi_annual)

# %%
cmip5 = pd.read_csv('../data/TSI_WLS_ann_1610_2008.txt', sep="\s+", skipinitialspace=True, skiprows=2)
cmip5 = cmip5.iloc[:, :3]
cmip5 = cmip5.set_index("YEAR")
cmip5.columns = ['no_background', 'with_background']
cmip5

# %%
pl.plot(cmip5)

# %%
pl.plot(cmip5['with_background'], label='CMIP5 TSI')
pl.plot(np.arange(1850.5, 2300), cmip6_tsi_annual, label='CMIP6 TSI')
pl.plot(np.arange(1850.5, 2024), cmip7_tsi_annual, label='CMIP7 TSI')

# %% [markdown]
# From https://www.solarisheppa.kit.edu/85.php, accessed 8 July 2025
#
# ## Recommendations for CMIP5 solar forcing data
#
# This section provides links solar irradiance data that should be used in CMIP5 simulations. A description of how the data were reconstructed by Judith Lean can be found here, and some guidelines for their use are also provided. For some models, use of the spectrally-resolved data, which accounts for the wavelength dependent changes in solar irradiance, is unwarranted. For these models, the total irradiance time series should be used.
#
# ### What to prescribe in the pre-industrial control simulation?
# Use the TSI and/or spectrally resolved values for a mean representative of 1850 conditions, i.e. cycle average from year 1844 to 1856. Note that 1850 is a year near the peak of the solar cycle.
#
# It is recommended to use the TSI time series with varying background (second column in ascii files) for the CMIP5 runs and if desired perform additional sensitivity experiments without the varying background.

# %%
cmip5_baseline = cmip5.loc[1844.5:1856.5,'with_background'].mean()
cmip5_baseline

# %% [markdown]
# ### What to prescribe in the CMIP6 pre-industrial control simulation (part of CMIP6 DECK)?
# piControl forcing (~42kB)
# The pre-industrial control forcing (pictrontrol) is constructed of time-averaged historical data (see below) corresponding to 1850-1873 (solar cycle 9+10) mean conditions. See metadata file for more details.

# %%
cmip6_baseline = cmip6_tsi_annual[:24].mean()
cmip6_baseline

# %% [markdown]
# ### What to prescribe in the CMIP7 pre-industrial control simulation (part of CMIP7 DECK)?
#
# piControl solar forcing (48 kB)
# The pre-industrial control forcing (pictrontrol) is constructed from time-averaged historical data (see below) corresponding to 1850-1873 (solar cycle 9+10) mean conditions. See metadata file for more details.

# %%
cmip7_baseline = cmip7_tsi_annual[:24].mean()
cmip7_baseline

# %%
cmip5_forcing = (cmip5['with_background'] - cmip5_baseline) * 0.25 * 0.72 * 0.71
cmip6_forcing = (cmip6_tsi_annual - cmip6_baseline) * 0.25 * 0.72 * 0.71
cmip7_forcing = (cmip7_tsi_annual - cmip7_baseline) * 0.25 * 0.72 * 0.71

# %%
pl.plot(cmip5_forcing, label='CMIP5 TSI')
pl.plot(np.arange(1850.5, 2300), cmip6_forcing, label='CMIP6 TSI')
pl.plot(np.arange(1850.5, 2024), cmip7_forcing, label='CMIP7 TSI')
pl.xlim(1850, 2023)
pl.ylabel("W m$^{-2}$")
pl.legend()
pl.tight_layout()

os.makedirs('../plots', exist_ok=True)
pl.savefig('../plots/solar_erf_across_cmips.png')

# %%
fig = pl.figure(figsize=(11/2.54, 11/2.54))
pl.plot(cmip5_forcing, label='CMIP5 TSI')
pl.plot(np.arange(1850.5, 2300), cmip6_forcing, label='CMIP6 TSI')
pl.plot(np.arange(1850.5, 2024), cmip7_forcing, label='CMIP7 TSI')
pl.xlim(1995, 2023)
pl.ylabel("W m$^{-2}$")
pl.title("Solar ERF")
pl.legend()
pl.tight_layout()

os.makedirs('../plots', exist_ok=True)
pl.savefig('../plots/solar_erf_across_cmips_1995-2023.png')

# %%
cmip5_forcing.loc[1849.5:]

# %%
cmip6_forcing

# %%
cmip7_forcing

# %%
data_out = np.ones((175, 3)) * np.nan
data_out[:160, 0] = cmip5_forcing.loc[1849.5:]
data_out[:, 1] = np.concatenate((cmip6_forcing[0:1], cmip6_forcing[:174]))
data_out[:, 2] = np.concatenate((cmip7_forcing[0:1], cmip7_forcing))

# %%
df_out = pd.DataFrame(
    data = data_out,
    index=np.arange(1850, 2025),
    columns = ['cmip5', 'cmip6', 'cmip7']
)

# %%
df_out

# %%
os.makedirs('../output', exist_ok=True)

# %%
df_out.to_csv('../output/solar_forcing.csv')

# %%
