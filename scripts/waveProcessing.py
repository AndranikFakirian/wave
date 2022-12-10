import os
import matplotlib.ticker as tic
import matplotlib.pyplot as plt
import math as m
files=('35', '60', '81')
dat_dir=os.getcwd()
os.chdir("..")
dat_dir=os.getcwd()
dat_dir+='\\data\\'
f=open(dat_dir+'coeff.txt')
c=float(f.readline())
f.close()
t=[]
heigt=[]
def sum(p):
    s=0
    for i in p:
        s+=i
    return s
def average(p):
    s=sum(p)
    l=len(p)
    return s/l
def minsqr(x, y):
    xy=[]
    x2=[]
    y2=[]
    l=len(x)
    for i in range(0, l):
        xy.append(x[i]*y[i])
        x2.append(x[i]**2)
        y2.append(y[i]**2)
    avx = average(x)
    avy = average(y)
    avxy = average(xy)
    avx2 = average(x2)
    avy2 = average(y2)
    a = (avxy - avx * avy) / (avx2 - avx ** 2)
    b = avy - avx * a
    aerr = (1 / (l) ** (1 / 2)) * (((avy2 - avy ** 2) / (avx2 - avx ** 2) - a ** 2) ** (1 / 2))
    berr = aerr * ((avx2 - avx ** 2) ** (1 / 2))
    return [a, b, aerr, berr]
dat_dir2=os.getcwd()+'\\plots\\'
for i in files:
    f=open(dat_dir+i+' mm mea.txt')
    s=f.readline()
    s=f.readline()
    s=f.readline()
    s=list(map(str, s.split()))
    atime=float(s[2])
    s=f.readline()
    h=[]
    while True:
        s=f.readline()
        if s=='':
            break
        h.append(c*(int(s)**2))
    l=len(h)
    time=[]
    for j in range(1, l+1):
        time.append(j*atime/l)
    fig, ax = plt.subplots()
    index1=0
    index2=0
    xmax=0
    ymax=0
    ymin=0
    if i=='35':
        index1=25
        index2=51
        xmax=15.13
        ymin=-0.5
        ymax=40
    elif i=='60':
        index1=19
        index2=44
        xmax = 15.16
        ymax=70
        ymin=-0.5
    else:
        index1=14
        index2=22
        xmax = 15.14
        ymax=96.5
        ymin=-1
    x=[time[j] for j in range(0, l)]
    av=average([h[j] for j in range(0, index1+1)])
    y1=[av for j in range(0, l)]
    args=minsqr([time[j] for j in range(index1+1, index2+1)], [h[j] for j in range(index1+1, index2+1)])
    y2=[args[0]*time[j]+args[1] for j in range(0, l)]
    to=(av-args[1])/args[0]
    heigt.append(av/1000)
    t.append(to)
    ax.plot(x, y1, linestyle='-', linewidth = 1.5,  color= 'deepskyblue', alpha=0.3, label='Аппроксимированный первый участок графика', zorder=2)
    ax.plot(x, y2, linestyle='-', linewidth = 1.5,  color= 'forestgreen', alpha=0.3, label='Аппроксимированная начальная часть воторого участка графика', zorder=3)
    ax.scatter(to, av, s=7, c='crimson', alpha=0.3, label='Точка пересечения аппроксимаций в прямые ({0:.4f} с; {1:.4f} мм)'.format(to, av), zorder=4)
    ax.plot(time, h, linestyle='-', linewidth = 1.5,  color= 'gold', label='Зависимость текущего регистрируемого уровня воды от времени', zorder=1)
    ax.legend(loc=0)
    ax.set_ylabel('Уровень воды, мм')
    ax.set_xlabel('Время, с')
    ax.set_title('График изменения уровня воды в течение времени при начальном уровне {} мм'.format(i), loc='center', pad=10)
    ax.set_xlim([-0.05, xmax])
    ax.set_ylim([ymin, ymax])
    ax.yaxis.set_minor_locator(tic.MultipleLocator(1))
    ax.xaxis.set_minor_locator(tic.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(tic.MultipleLocator(5))
    ax.xaxis.set_major_locator(tic.MultipleLocator(1))
    ax.grid(axis='both', which='minor', linestyle='--', linewidth=0.5, color='lightgrey', alpha=0.4, zorder=0)
    ax.grid(axis='both', which='major', linestyle='-', linewidth=1, color='lightgrey', alpha=0.4, zorder=0)
    plt.show()
    fig.savefig(dat_dir2+('height_from_time_for_initial_{}_mm.png'.format(i)))
    del fig, ax
f=open(dat_dir+'l.txt')
s=f.readline()
s=list(map(str, s.split()))
length=float(float(s[0]))
f.close()
vel=[]
for i in t:
    vel.append(length/i)
vell, heigtl=[], []
for i in vel:
    vell.append(m.log(i))
for i in heigt:
    heigtl.append(m.log(i))
args=minsqr(heigtl, vell)
ma=max(heigtl)
mi=min(heigtl)
mi=int(1000*mi/ma)
x=[ma*i/1000 for i in range(950, mi+51)]
y=[args[0]*x[i]+args[1] for i in range(0, mi-899)]
fig, ax = plt.subplots()
ax.plot(x, y, linestyle='-', linewidth = 1.5,  color= 'orchid', label='ln(velocity)=({0:.4f}±{2:.4f})ln(heigth)+({1:.4f}±{3:.4f})\ng≈{4:.4f} — {5:.4f} м/с^2'.format(args[0], args[1], args[2], args[3], m.exp(2*(args[1]-args[3])), m.exp(2*(args[1]+args[3]))), zorder=1)
ax.scatter(heigtl, vell, s=7, c='navy', label='Логарифмы скоростей возмущений при различных логарифмах начальных уровней воды', zorder=2)
ax.set_ylabel('ln(velocity), ln(м/с)')
ax.set_xlabel('ln(height), ln(м)')
ax.set_title('График логарифмической зависимости скорости возмущений от начального уровня воды', loc='center', pad=10)
ax.legend(loc=0)
ax.set_xlim([-3.43, -2.4])
ax.set_ylim([-0.29, 0.28])
ax.yaxis.set_minor_locator(tic.MultipleLocator(0.005))
ax.xaxis.set_minor_locator(tic.MultipleLocator(0.005))
ax.yaxis.set_major_locator(tic.MultipleLocator(0.05))
ax.xaxis.set_major_locator(tic.MultipleLocator(0.05))
ax.grid(axis= 'both', which = 'minor', linestyle='--', linewidth=0.5, color='lightgrey', alpha=0.4, zorder=0)
ax.grid(axis= 'both', which = 'major', linestyle='-', linewidth=1, color='lightgrey', alpha=0.4, zorder=0)
plt.show()
fig.savefig(dat_dir2+'velocity_from_height_log.png')
del fig, ax
def coeff(x, y):
    return m.exp(average(y)-average(x)/2)
coef=coeff(heigtl, vell)
ma=max(heigt)
x=[ma*i/10000 for i in range(0, 10501)]
y=[coef*(x[i]**(1/2)) for i in range(0, 10501)]
fig, ax = plt.subplots()
ax.plot(x, y, linestyle='-', linewidth = 1.5,  color= 'olive', label='velocity={:.4f}*height^(1/2)'.format(coef), zorder=1)
ax.scatter(heigt, vel, s=7, c='orange', label='Скорости возмущений при различных начальных уровнях', zorder=2)
ax.set_ylabel('velocity, м/с')
ax.set_xlabel('height, м')
ax.set_title('График зависимости скорости возмущений от начального уровня воды', loc='center', pad=10)
ax.legend(loc=0)
ax.set_xlim([-0.001, 0.085])
ax.set_ylim([-0.05, 1.34])
ax.yaxis.set_minor_locator(tic.MultipleLocator(0.01))
ax.xaxis.set_minor_locator(tic.MultipleLocator(0.001))
ax.yaxis.set_major_locator(tic.MultipleLocator(0.1))
ax.xaxis.set_major_locator(tic.MultipleLocator(0.005))
ax.grid(axis= 'both', which = 'minor', linestyle='--', linewidth=0.5, color='lightgrey', alpha=0.4, zorder=0)
ax.grid(axis= 'both', which = 'major', linestyle='-', linewidth=1, color='lightgrey', alpha=0.4, zorder=0)
plt.show()
fig.savefig(dat_dir2+'velocity_from_height.png')