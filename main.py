##################################################################

serialID = "T4620165"

##################################################################


import sondehub
import pandas as pd
import numpy as np
from metpy.plots import SkewT
import metpy.calc as clc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from metpy.units import units



frames = sondehub.download(serial=serialID)
df = pd.DataFrame(frames)

#only rising
df = df.sort_values('datetime').reset_index()
index = df["pressure"].idxmin()
df = df[:index]

#values
dt = df['datetime'].values.tolist()
T = df['temp'].values.tolist() * units.degC
RH = df["humidity"].values.tolist() * units.percent
p=df["pressure"].values.tolist() * units.hPa
Td = clc.dewpoint_from_relative_humidity(T, RH)


#plot
fig = plt.figure(figsize=(20, 20))
skew = SkewT(fig, rotation=45)
skew.plot(p, T,'r')
skew.plot(p, Td,'b')

plt.title(df["datetime"][0])

skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

plt.savefig(df["datetime"][0]+".png")

#export netcdf
exportDF = pd.DataFrame({'datetime':dt,'p':p,'T':T,'Td':Td,'RH':RH}).set_index('p')
exportDF.to_csv(df["datetime"][0]+".csv")



