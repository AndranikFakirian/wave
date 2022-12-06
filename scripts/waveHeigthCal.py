import os
files=('14', '34', '54', '81')
dat_dir=os.getcwd()
os.chdir("..")
dat_dir=os.getcwd()
dat_dir+='\\data\\calibration\\'
av=[]
def sum(p):
    s=0
    for i in p:
        s+=i
    return s
def average(p):
    s=sum(p)
    l=len(p)
    return s/l
for i in files:
    f=open(dat_dir+i+' mm.txt')
    for i in range(0, 4):
        s=f.readline()
    i=[]
    while True:
        s=f.readline()
        if s=='':
            f.close()
            break
        i.append(int(s))
    av.append(average(i))
import math as m
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
fig, ax = plt.subplots()
mm=[]
for i in files:
    mm.append(int(i))
mml=[]
for i in mm:
    mml.append(m.log(i))
avl=[]
for i in av:
    avl.append(m.log(i))
def minsqr(x, y):
    xy=[]
    x2=[]
    y2=[]
    l=len(x)
    for i in range(0, l):
        xy.append(x[i]*y[i])
        x2.append(x[i]**2)
        y2.append(y[i]**2)
    avx=average(x)
    avy=average(y)
    avxy=average(xy)
    avx2=average(x2)
    avy2 = average(y2)
    a=(avxy-avx*avy)/(avx2-avx**2)
    b=avy-avx*a
    aerr=(1/(l)**(1/2))*(((avy2-avy**2)/(avx2-avx**2)-a**2)**(1/2))
    berr=aerr*((avx2-avx**2)**(1/2))
    return [a, b, aerr, berr]
args=minsqr(avl, mml)
x, y = [], []
ma=max(avl)
mi=min(avl)
i=0
while ma*(i+50)/1000<=mi:
    i+=1
for j in range(i, 1051):
    x.append(ma*j/1000)
    y.append(args[0]*x[j-i]+args[1])
ax.plot(x, y, linestyle='-', linewidth = 1.5,  color= 'forestgreen', label='ln(height)=({0:.4f}±{2:.4f})ln(adc_value)-({1:.4f}±{3:.4f})'.format(args[0], args[1]*(-1), args[2], args[3]), zorder=1)
ax.scatter(avl, mml, s=7, c='crimson', label='Логарифмы уровней воды при различных логарифмах значений АЦП', zorder=2)
ax.legend(loc=0)
ax.set_ylabel('ln(height), ln(мм)')
ax.set_xlabel('ln(adc_value)')
ax.set_title('Логарифмическая зависимость уровня воды от показаний АЦП', loc='center', pad=10)
ax.set_xlim([3.92, 5.4])
ax.set_ylim([2.1, 4.85])
ax.yaxis.set_minor_locator(tic.MultipleLocator(0.02))
ax.xaxis.set_minor_locator(tic.MultipleLocator(0.01))
ax.yaxis.set_major_locator(tic.MultipleLocator(0.2))
ax.xaxis.set_major_locator(tic.MultipleLocator(0.1))
ax.grid(axis= 'both', which = 'minor', linestyle='--', linewidth=0.5, color='lightgrey', alpha=0.4, zorder=0)
ax.grid(axis= 'both', which = 'major', linestyle='-', linewidth=1, color='lightgrey', alpha=0.4, zorder=0)
plt.show()
dat_dir=os.getcwd()
fig.savefig(dat_dir+'\\plots\\height_calibration_plot_1.png')
del fig, ax
def coeff(x, y):
    return m.exp(average(y)-average(x)*2)
c=coeff(avl, mml)
x, y=[], []
ma=max(av)
del i
for i in range(0, 10501):
    x.append(ma*i/10000)
    y.append(c*(x[i]**2))
fig, ax = plt.subplots()
ax.plot(x, y, linestyle='-', linewidth = 1.5,  color= 'gold', label='height={0:.4f}*adc_value^2'.format(c), zorder=1)
ax.scatter(av, mm, s=7, c='deepskyblue', label='Уровни воды при различных значениях АЦП', zorder=2)
ax.legend(loc=0)
ax.set_ylabel('height, мм')
ax.set_xlabel('adc_value')
ax.set_title('Зависимость уровня воды от показаний АЦП', loc='center', pad=10)
ax.set_xlim([-2, 179])
ax.set_ylim([-2, 89])
ax.yaxis.set_minor_locator(tic.MultipleLocator(1))
ax.xaxis.set_minor_locator(tic.MultipleLocator(1))
ax.yaxis.set_major_locator(tic.MultipleLocator(10))
ax.xaxis.set_major_locator(tic.MultipleLocator(10))
ax.grid(axis= 'both', which = 'minor', linestyle='--', linewidth=0.5, color='lightgrey', alpha=0.4, zorder=0)
ax.grid(axis= 'both', which = 'major', linestyle='-', linewidth=1, color='lightgrey', alpha=0.4, zorder=0)
plt.show()
fig.savefig(dat_dir+'\\plots\\height_calibration_plot_2.png')
f=open(dat_dir+'\\data\\coeff.txt', 'w')
f.write(str(c))
f.close()