# Plot moment summaries

from pyproj import Proj
from netCDF4 import Dataset
import netCDF4
import numpy
import datetime
from matplotlib import pyplot, mpl
import matplotlib.ticker as mticker

#from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, WeekdayLocator

dlb2 = ["","(-5,-3)","","(-2,-1)","","(-0.5,0)", \
        "","(0.5,1)","","(2,3)","","> 5"]

# GLM Model
gfl = "../BayesMixVar_EOF_201007/MixVar_PPSummary_Chol.nc"
fgrp = Dataset(gfl)
gfrq = fgrp.variables['CatFreq_Quantile'][:,:]
prbs = fgrp.variables['Prob'][:]
fgrp.close()
print prbs
# 0.025 is index 2
# 0.5 is index 6
# 0.975 is index 10 

# Constant Model
gfl = "ConsVar_PPSummary_Chol.nc"
fgrp = Dataset(gfl)
cfrq = fgrp.variables['CatFreq_Quantile'][:,:]
fgrp.close()

# Open up Data File
cfl = "ObsMCMCDat_BSqrEOF_201007.nc"
fgrp = Dataset(cfl,"r")
obsfrq = fgrp.variables['CatFreq'][:]
fgrp.close()

cts = numpy.arange(12)
xst = [-0.5,1.5,3.5,5.5,7.5,9.5]
yst = [0.04,0.04,0.04,0.04,0.04,0.04]

fig = pyplot.figure(figsize=(9,6))
p1 = pyplot.subplot(111)
p1.set_ylim(0.04,0.16)
p1.set_xlim(-0.5,11.5)
p1.set_ylabel('Proportion')
p1.set_xlabel('Divergence Category [mm]')
p1.yaxis.set_major_locator(mticker.FixedLocator(numpy.arange(0.04,0.18,0.02)))
p1.xaxis.set_major_locator(mticker.FixedLocator(cts))
p1.set_xticklabels(dlb2)

for i in range(len(xst)):
    rect = pyplot.Rectangle((xst[i],yst[i]),1,52, \
                             facecolor="#CCCCCC",edgecolor='none')
    pyplot.gca().add_patch(rect)

p1.yaxis.grid(color='#777777',linestyle='dotted')
#p1.plot([-0.5,11.5],[0,0],'k-',lw=1.2, zorder=5)
p1.plot([5.5,5.5],[0.04,0.16],'k-',lw=1.2, zorder=5)
oln = p1.plot(cts,obsfrq,'kx',zorder=5,markersize=6,label='Obs')
gln = p1.plot(cts-0.2,gfrq[6,:],'k^',zorder=5,markersize=6,label='GLM')
cln = p1.plot(cts+0.2,cfrq[6,:],'k^',zorder=5,markersize=6, \
        label='Constant',markeredgecolor='k',markerfacecolor='w')
p1.errorbar(cts - 0.2,gfrq[6,:],yerr=[gfrq[6,:]-gfrq[2,:], \
                                      gfrq[10,:]-gfrq[6,:]], fmt=None, \
            ecolor='k',barsabove=True,zorder=8,markersize=6,capsize=4)
p1.errorbar(cts + 0.2,cfrq[6,:],yerr=[cfrq[6,:]-cfrq[2,:], \
                                      cfrq[10,:]-cfrq[6,:]], fmt=None, \
            ecolor='k',barsabove=True, \
            zorder=8,markersize=6,capsize=4)
leg = p1.legend((oln,gln,cln),('Obs','GLM','Constant'),'upper center', \
                numpoints=1, \
                borderpad=0.15,labelspacing=0.05,handletextpad=0.2)
leg.set_zorder(10)
for t in leg.get_texts():
    t.set_fontsize(10)

pyplot.title('Proportion of Locations',size=12)
fig.savefig('PPComp_Freq_201007.pdf')


#for i in range(3):
#    vrxpl = z5vl[5-i] * 100.0 / 2501.0
#    tstr = 'EOF %d: %.1f%% of Variance' % (i+1,vrxpl)
#    p1 = pyplot.subplot(2,2,i+1)
#    mp = Basemap(projection='cyl',resolution='l',  \
#                 llcrnrlat=30.0, urcrnrlat=50.0, \
#                 llcrnrlon=-110.0, urcrnrlon=-80.0, \
#                 rsphere=6371200.0,area_thresh=10000.0)
#    mp.drawcoastlines()
#    mp.drawcountries()
#    mp.drawstates(color="#888888")
#    xg, yg = mp(xsq,ysq)
#    vcshp = z5vc[5-i,:]
#    vcshp.shape = (41,61)
#    print numpy.amin(vcshp)
#    print numpy.amax(vcshp)
#    print vcshp[20,20]
#    cs = mp.contour(xg,yg,vcshp[:,:],clvs,colors='k',linewidths=1.5)
#    pyplot.clabel(cs,fmt='%.2f',fontsize=6)
#    pyplot.title(tstr,size=10)

# Time series for 201007
#cfl = "Z500_July_EOFScores.nc"
#fgrp = Dataset(cfl,"r")
#scrs10 = fgrp.variables['EOFScore'][3,0:3,:]
#fgrp.close()

#dt1 = datetime.date(2010,7,1)
#dtlst = []
#for i in range(31): 
#    dtlst.append(dt1 + datetime.timedelta(days=i))

#dsq = numpy.arange(1,32)
#lbsq = numpy.arange(-80.0,100.0,20.0)

#p1 = pyplot.subplot(2,2,4)
#p1.plot(dtlst,scrs10[0,:],'k-', \
#        dtlst,scrs10[1,:],'k--', \
#        dtlst,scrs10[2,:],'k-.',lw=1.5)
#p1.xaxis.grid(color='#777777',linestyle='dotted')
#p1.yaxis.grid(color='#777777',linestyle='dotted')
#p1.xaxis.set_major_formatter(DateFormatter('%m-%d'))
#p1.xaxis.set_major_locator(WeekdayLocator(byweekday=1))
#for lb in p1.xaxis.get_ticklabels():
#    lb.set_fontsize(9)
#p1.yaxis.set_ticks(lbsq,minor=False)
#for lb in p1.yaxis.get_ticklabels():
#    lb.set_fontsize(9)
#leg = p1.legend(('EOF 1','EOF 2','EOF 3'),'upper left',numpoints=3, \
#                borderpad=0.05,labelspacing=0.05,handletextpad=0.5)
#for t in leg.get_texts():
#    t.set_fontsize(9)
#for l in leg.get_lines():
#    l.set_linewidth(1.5)


