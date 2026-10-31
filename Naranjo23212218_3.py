"""
Práctica 3: Modelado y control del sistema muscoesqueletico.

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Marcos Ancelmo Naranjo Rivera
Número de control: 23212218
Correo institucional: l23212218@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx

"""
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# Datos generales de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
u = np.zeros(N); u[round(1/dt):round(2/dt)] = 1

def sis(R, nombre):
    Cs, Cp, a = 10E-6,100E-6,0.25
    num = [Cs*R, 1-a]
    den = [R*(Cp+Cs),1]
    sys = ctrl.tf(num, den)
    print(f"Función de transferencia {nombre}: {sys}\n")
    return sys

sysControl = sis(100, "Control")
sysCaso = sis(10E3, "Caso")

# Componentes del controlador
kP,kI = 0.021504,42202.0256
Cr = 1E-6
Re = 1/(Cr*kI)
Rr = kP*Re
numPID = [Rr*Cr, 1]
denPID = [Re*Cr,0]
PI = ctrl.tf(numPID,denPID)

# Sistema de control en lazo cerrado
sysPI = ctrl.feedback(ctrl.series(PI,sysCaso),1,sign = -1)
print(f"Función de transferencia en lazo cerrado: {sysPI}\n")

#Colores 
clr1 = np.array([(118, 196, 87)])/255
clr2 = np.array([(27, 44, 193)])/255
clr3 = np.array([(147, 112, 219)])/255
clr4 = np.array([(221, 113, 113)])/255

# Funciones del sistema en lazo abierto y lazo cerrado
def openloop(t,sys,u):
    _,Fs = ctrl.forced_response(sys,t,u,x0)
    return Fs
    
def closedloop(t,sys,u):
    _,tratamientoPI = ctrl.forced_response(sys,t,u,x0)
    return tratamientoPI

#Respuestas: Simulaciones numéricas
Control = openloop(t,sysControl,u)
Caso = openloop(t,sysCaso,u)
Tratamiento = closedloop(t,sysPI,Control)
fg = plt.figure()
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,u,'-',linewidth=1.5,color=clr1,label='F(t)')
plt.plot(t,Control,'-',linewidth=1.5,color=clr2,label='Fs(t): Control')
plt.plot(t,Caso,'--',linewidth=1.5,color=clr3,label='Fs(t): Caso')
plt.plot(t,Tratamiento,'--',linewidth=1.5,color=clr4,label='Fs(t): Tratamiento PI')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.1,0.1))
plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
plt.show()
fg.savefig('Control_caso_python3.pdf',bbox_inches='tight')