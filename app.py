import os
import time
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.makedirs('static', exist_ok=True)

app = Flask(__name__)

# ---- Construcción del sistema difuso ----
def build_fuzzy_system():
    temperatura = ctrl.Antecedent(np.arange(0, 51, 1), 'temperatura')
    humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
    velocidad = ctrl.Consequent(np.arange(0, 101, 1), 'velocidad')


    temperatura['baja'] = fuzz.trimf(temperatura.universe, [0, 0, 20])
    temperatura['media'] = fuzz.trimf(temperatura.universe, [15, 25, 35])
    temperatura['alta'] = fuzz.trimf(temperatura.universe, [30, 50, 50])


    humedad['baja'] = fuzz.trimf(humedad.universe, [0, 0, 40])
    humedad['media'] = fuzz.trimf(humedad.universe, [30, 50, 70])
    humedad['alta'] = fuzz.trimf(humedad.universe, [60, 100, 100])


    velocidad['baja'] = fuzz.trimf(velocidad.universe, [0, 0, 40])
    velocidad['media'] = fuzz.trimf(velocidad.universe, [30, 50, 70])
    velocidad['alta'] = fuzz.trimf(velocidad.universe, [60, 100, 100])


    # Reglas
    rule1 = ctrl.Rule(temperatura['alta'] & humedad['alta'], velocidad['alta'])
    rule2 = ctrl.Rule(temperatura['baja'] & humedad['baja'], velocidad['baja'])
    rule3 = ctrl.Rule(temperatura['media'] & humedad['media'], velocidad['media'])
    rule4 = ctrl.Rule(temperatura['alta'] & humedad['baja'], velocidad['media'])
    rule5 = ctrl.Rule(temperatura['media'] & humedad['alta'], velocidad['alta'])
    rule6 = ctrl.Rule(temperatura['baja'] & humedad['alta'], velocidad['media'])


    sistema = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
    simulador = ctrl.ControlSystemSimulation(sistema)


    return {
    'temperatura': temperatura,
    'humedad': humedad,
    'velocidad': velocidad,
    'simulador': simulador
    }


# Genera y guarda gráficos de las funciones de membresía
def plot_membership(temperatura, humedad, velocidad):
    timestamp = str(int(time.time()))
    # Temperatura
    fig1, ax1 = plt.subplots()
    for label in temperatura.terms:
        mf = temperatura[label].mf
        ax1.plot(temperatura.universe, mf, label=label)
    ax1.set_title('Funciones de membresía - Temperatura (°C)')
    ax1.set_xlabel('°C')
    ax1.legend()
    temp_path = f'static/mf_temp_{timestamp}.png'
    fig1.tight_layout()
    fig1.savefig(temp_path)
    plt.close(fig1)


    # Humedad
    fig2, ax2 = plt.subplots()
    for label in humedad.terms:
        mf = humedad[label].mf
        ax2.plot(humedad.universe, mf, label=label)
    ax2.set_title('Funciones de membresía - Humedad (%)')
    ax2.set_xlabel('%')
    ax2.legend()
    hum_path = f'static/mf_hum_{timestamp}.png'
    fig2.tight_layout()
    fig2.savefig(hum_path)
    plt.close(fig2)


    # Velocidad (solo las funciones de membresía)
    fig3, ax3 = plt.subplots()
    for label in velocidad.terms:
        mf = velocidad[label].mf
        ax3.plot(velocidad.universe, mf, label=label)
    ax3.set_title('Funciones de membresía - Velocidad (%)')
    ax3.set_xlabel('%')
    ax3.legend()
    vel_path = f'static/mf_vel_{timestamp}.png'
    fig3.tight_layout()
    fig3.savefig(vel_path)
    plt.close(fig3)


    return temp_path, hum_path, vel_path


@app.route('/', methods=['GET', 'POST'])
def index():
    fs = build_fuzzy_system()
    temperatura = fs['temperatura']
    humedad = fs['humedad']
    velocidad = fs['velocidad']
    simulador = fs['simulador']


    if request.method == 'POST':
        try:
            T = float(request.form.get('temperatura', 0))
            H = float(request.form.get('humedad', 0))
        except ValueError:
            return render_template('index.html', error='Introduce valores numéricos válidos.')


        # Limitar a los universos definidos
        T = max(min(T, 50), 0)
        H = max(min(H, 100), 0)


        simulador.input['temperatura'] = T
        simulador.input['humedad'] = H
        simulador.compute()


        output_vel = simulador.output['velocidad']


        # Generar gráficos y guardarlos
        temp_path, hum_path, vel_path = plot_membership(temperatura, humedad, velocidad)


        # Además, generar figura mostrando la defuzzificación (área recortada)
        # Construimos la figura de output con la activación
        fig, ax = plt.subplots()
        ax.plot(velocidad.universe, velocidad['baja'].mf, linestyle='--', label='baja')
        ax.plot(velocidad.universe, velocidad['media'].mf, linestyle='--', label='media')
        ax.plot(velocidad.universe, velocidad['alta'].mf, linestyle='--', label='alta')


        # Calcular agregación final (método de centroid ya aplicado por skfuzzy).
        # Para visualizar la activación, re-evaluamos con las reglas (aproximación simple):
        # No usamos internals de skfuzzy; en cambio pintamos una línea vertical en el valor defuzz.
        ax.axvline(output_vel, color='k', linewidth=2, label=f'Defuzz: {output_vel:.2f}%')
        ax.set_title('Salida - Velocidad (defuzzificación)')
        ax.set_xlabel('%')
        ax.legend()
        out_path = f'static/output_{int(time.time())}.png'
        fig.tight_layout()
        fig.savefig(out_path)
        plt.close(fig)


        return render_template('result.html', temperatura=T, humedad=H,
        velocidad=output_vel,
        mf_temp=temp_path, mf_hum=hum_path, mf_vel=vel_path, out_img=out_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)