# Plot moment summaries

from pyproj import Proj
from netCDF4 import Dataset
import netCDF4
import numpy
import datetime
from matplotlib import pyplot, mpl
import matplotlib.ticker as mticker

#from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, WeekdayLocator

dlb2 = ["","(-1.5,-1.0)","","(-0.5,-0.2)","","(0.2,0.5)", \
        "","(1.0,1.5)",""]

# GLM Model
gfl = "SpatVar_PPSummaryB_Chol.nc"
fgrp = Dataset(gfl)
gskw = fgrp.variables['CatSkew_Quantile'][:,:]
prbs = fgrp.variables['Prob'][:]
fgrp.close()
print prbs
# 0.025 is index 2
# 0.5 is index 6
# 0.975 is index 10 

# Constant Model
gfl = "../BayesCons_HrRate_201007/ConsVar_PPSummaryB_Chol.nc"
fgrp = Dataset(gfl)
cskw = fgrp.variables['CatSkew_Quantile'][:,:]
fgrp.close()

# Open up Data File
cfl = "../Data/ObsMCMCDat_VAR_201007.nc"
fgrp = Dataset(cfl,"r")
obskew = fgrp.variables['CatSkew'][:]
fgrp.close()


cts = numpy.arange(9)
xst = [-0.5,1.5,3.5,5.5,7.5]
yst = [-3,-3,-3,-3,-3,-3]

fig = pyplot.figure(figsize=(9,6))
p1 = pyplot.subplot(111)
p1.set_ylim(-3,3)
p1.set_xlim(-0.5,8.5)
p1.set_ylabel('Skewness')
p1.set_xlabel('Divergence Category [mm]')
p1.yaxis.set_major_locator(mticker.FixedLocator(numpy.arange(-3,4,1)))
p1.xaxis.set_major_locator(mticker.FixedLocator(cts))
p1.set_xticklabels(dlb2)

for i in range(len(xst)):
    rect = pyplot.Rectangle((xst[i],yst[i]),1,6, \
                             facecolor="#CCCCCC",edgecolor='none')
    pyplot.gca().add_patch(rect)

#p1.xaxis.grid(color='#777777',linestyle='dotted')
p1.yaxis.grid(color='#777777',linestyle='dotted')
p1.plot([-0.5,11.5],[0,0],'k-',lw=1.2, zorder=5)
p1.plot([4.0,4.0],[-3,3],'k-',lw=1.2, zorder=5)
oln = p1.plot(cts,obskew,'kx',zorder=5,markersize=6,label='Obs')
gln = p1.plot(cts-0.2,gskw[6,:],'k^',zorder=5,markersize=6,label='Spatial Variance')
cln = p1.plot(cts+0.2,cskw[6,:],'k^',zorder=5,markersize=6, \
        label='Constant',markeredgecolor='k',markerfacecolor='w')
p1.errorbar(cts - 0.2,gskw[6,:],yerr=[gskw[6,:]-gskw[2,:], \
                                      gskw[10,:]-gskw[6,:]], fmt=None, \
            ecolor='k',barsabove=True,zorder=8,markersize=6,capsize=4)
p1.errorbar(cts + 0.2,cskw[6,:],yerr=[cskw[6,:]-cskw[2,:], \
                                      cskw[10,:]-cskw[6,:]], fmt=None, \
            ecolor='k',barsabove=True, \
            zorder=8,markersize=6,capsize=4)
leg = p1.legend((oln,gln,cln),('Obs','Spatial Variance','Constant'), \
                'upper center', \
                numpoints=1, \
                borderpad=0.15,labelspacing=0.05,handletextpad=0.2)
leg.set_zorder(10)
for t in leg.get_texts():
    t.set_fontsize(10)
#for l in leg.get_lines():
#    l.set_linewidth(1.5)

pyplot.title('Empirical Conditional Skewness',size=12)
fig.savefig('PPComp_Skew_201007.pdf')

# Re-scaled version
#fig = pyplot.figure(figsize=(9,6))
#p1 = pyplot.subplot(111)
#p1.set_ylim(-3,3)
#p1.set_xlim(-0.5,11.5)
#p1.set_ylabel('Skewness')
#p1.set_xlabel('Divergence Category [mm]')
#p1.yaxis.set_major_locator(mticker.FixedLocator(numpy.arange(-3,4,1)))
#p1.xaxis.set_major_locator(mticker.FixedLocator(cts))
#p1.set_xticklabels(dlb2)

#for i in range(len(xst)):
#    rect = pyplot.Rectangle((xst[i],yst[i]),1,20, \
#                             facecolor="#DBDBDB",edgecolor='none')
#    pyplot.gca().add_patch(rect)

#p1.xaxis.grid(color='#777777',linestyle='dotted')
#p1.yaxis.grid(color='#777777',linestyle='dotted')
#p1.plot([-0.5,11.5],[0,0],'k-',lw=1.2, zorder=5)
#p1.plot([5.5,5.5],[-3,3],'k-',lw=1.2, zorder=5)
#oln = p1.plot(cts,obskew,'ko',zorder=5,markersize=8,label='Obs', \
#              markerfacecolor="#009C5C",markeredgecolor="#009C5C", \
#              markeredgewidth=1.25)
#gln = p1.plot(cts-0.2,gskw[6,:],'k^',zorder=5,markersize=8,label='GLM', \
#              markeredgecolor="#000000",markerfacecolor="#C16E41", \
#              markeredgewidth=1.25 )
#cln = p1.plot(cts+0.2,cskw[6,:],'ks',zorder=5,markersize=6, \
#        label='Constant',markeredgecolor='#000000',markerfacecolor='#8477D4', \
#                         markeredgewidth=1.25)
#p1.errorbar(cts - 0.2,gskw[6,:],yerr=[gskw[6,:]-gskw[2,:], \
#                                      gskw[10,:]-gskw[6,:]], fmt=None, \
#            ecolor='#C16E41',barsabove=True,zorder=8,markersize=8,capsize=8, \
#            markeredgewidth=1.25,elinewidth=1.25)
#p1.errorbar(cts + 0.2,cskw[6,:],yerr=[cskw[6,:]-cskw[2,:], \
#                                      cskw[10,:]-cskw[6,:]], fmt=None, \
#            ecolor='#8477D4',barsabove=True, \
#            zorder=8,markersize=8,capsize=8, \
#            markeredgewidth=1.25,elinewidth=1.25)
#leg = p1.legend((oln,gln,cln),('Obs','GLM','Constant'),'upper center', \
#                numpoints=1, \
#                borderpad=0.15,labelspacing=0.05,handletextpad=0.2)
#leg.set_zorder(10)
#for t in leg.get_texts():
#    t.set_fontsize(10)
#for l in leg.get_lines():
#    l.set_linewidth(1.5)

#pyplot.title('Skewness',size=12)
#fig.savefig('PPComp_Skew_Scl_201007.pdf')




