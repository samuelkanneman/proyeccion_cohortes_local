"""
PROYECCIÓN DE MORA - CHAIN LADDER (PyScript)
============================================
Procesamiento 100% en el navegador usando PyScript.
"""

import pandas as pd
import numpy as np
from js import document, window, Blob, URL, console
from pyodide.ffi import create_proxy
import json
import io

# Variables globales para almacenar datos
data_store = {
    'df': None,
    'df_mob': None,
    'df_pivot': None,
    'factors': None,
    'factors_detail': None,
    'df_proy': None,
    'cohorte_objetivo': None
}

# ============================================================
# FUNCIONES DE PROCESAMIENTO
# ============================================================

def parse_pct(x):
    """Parsea porcentajes con formato español"""
    if pd.isna(x) or x == '':
        return np.nan
    if isinstance(x, str):
        return float(x.replace('%', '').replace(',', '.'))
    return float(x)


def load_data_from_text(text_content):
    """Carga datos desde texto CSV"""
    try:
        df = pd.read_csv(io.StringIO(text_content), sep=';', index_col=0, encoding='utf-8-sig')
        df = df.map(parse_pct)
        return df, None
    except Exception as e:
        return None, str(e)


def create_mob_dataframe(df):
    """Convierte matriz vintage a formato MOB"""
    cohorts = df.index.tolist()
    periods = df.columns.tolist()
    
    mob_data = []
    for cohort in cohorts:
        cohort_year, cohort_month = int(cohort[:4]), int(cohort[5:7])
        for period in periods:
            period_year, period_month = int(period[:4]), int(period[5:7])
            mob = (period_year - cohort_year) * 12 + (period_month - cohort_month)
            value = df.loc[cohort, period]
            if not pd.isna(value):
                mob_data.append({
                    'cohorte': cohort,
                    'periodo': period,
                    'mob': mob,
                    'mora_pct': value
                })
    
    return pd.DataFrame(mob_data)


def calculate_development_factors(df_pivot):
    """Calcula factores de desarrollo promedio históricos"""
    factors = {}
    factors_detail = {}
    
    for mob in range(1, 25):
        prev_col = mob - 1
        curr_col = mob
        if prev_col in df_pivot.columns and curr_col in df_pivot.columns:
            valid_mask = (df_pivot[prev_col] > 0) & (~df_pivot[curr_col].isna())
            if valid_mask.sum() > 0:
                individual_factors = df_pivot.loc[valid_mask, curr_col] / df_pivot.loc[valid_mask, prev_col]
                factors[mob] = float(individual_factors.mean())
                factors_detail[mob] = {
                    'mean': float(individual_factors.mean()),
                    'std': float(individual_factors.std()),
                    'min': float(individual_factors.min()),
                    'max': float(individual_factors.max()),
                    'n': int(valid_mask.sum())
                }
    
    return factors, factors_detail


def mob_to_date(cohorte, mob):
    """Convierte cohorte + MOB a fecha calendario"""
    cohort_year, cohort_month = int(cohorte[:4]), int(cohorte[5:7])
    target_month = cohort_month + mob
    target_year = cohort_year + (target_month - 1) // 12
    target_month = ((target_month - 1) % 12) + 1
    return f"{target_year}-{target_month:02d}"


def project_cohort(df_pivot, factors, cohorte, mob_objetivo):
    """Proyecta una cohorte específica hasta el MOB objetivo"""
    
    if cohorte not in df_pivot.index:
        return None, f"Cohorte {cohorte} no encontrada"
    
    # Obtener último MOB observado
    cohort_data = df_pivot.loc[cohorte].dropna()
    last_mob = int(cohort_data.index.max())
    last_value = float(cohort_data.iloc[-1])
    
    # Construir proyección
    proyeccion = []
    
    # Agregar datos observados
    for mob in cohort_data.index:
        proyeccion.append({
            'cohorte': cohorte,
            'mob': int(mob),
            'fecha': mob_to_date(cohorte, int(mob)),
            'mora_pct': float(cohort_data[mob]),
            'tipo': 'Observado',
            'factor': None
        })
    
    # Proyectar hacia adelante
    current_value = last_value
    for future_mob in range(last_mob + 1, mob_objetivo + 1):
        if future_mob in factors:
            factor = factors[future_mob]
            current_value = current_value * factor
            proyeccion.append({
                'cohorte': cohorte,
                'mob': future_mob,
                'fecha': mob_to_date(cohorte, future_mob),
                'mora_pct': current_value,
                'tipo': 'Proyectado',
                'factor': factor
            })
    
    return pd.DataFrame(proyeccion), None


# ============================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================

def create_projection_plot():
    """Crea gráfico de proyección con Plotly.js"""
    df_proy = data_store['df_proy']
    df_pivot = data_store['df_pivot']
    cohorte = data_store['cohorte_objetivo']
    
    traces = []
    
    # Cohortes históricas (fondo)
    for c in df_pivot.index:
        if c != cohorte:
            data = df_pivot.loc[c].dropna()
            traces.append({
                'x': data.index.tolist(),
                'y': data.values.tolist(),
                'type': 'scatter',
                'mode': 'lines',
                'line': {'color': 'lightgray', 'width': 1},
                'opacity': 0.3,
                'showlegend': False,
                'hovertemplate': f'<b>{c}</b><br>MOB: %{{x}}<br>Mora: %{{y:.2f}}%<extra></extra>'
            })
    
    # Observado
    observado = df_proy[df_proy['tipo'] == 'Observado']
    traces.append({
        'x': observado['mob'].tolist(),
        'y': observado['mora_pct'].tolist(),
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Observado',
        'line': {'color': 'steelblue', 'width': 3},
        'marker': {'size': 8, 'symbol': 'circle'}
    })
    
    # Proyectado
    proyectado = df_proy[df_proy['tipo'] == 'Proyectado']
    if len(proyectado) > 0:
        traces.append({
            'x': proyectado['mob'].tolist(),
            'y': proyectado['mora_pct'].tolist(),
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Proyectado',
            'line': {'color': 'coral', 'width': 3, 'dash': 'dash'},
            'marker': {'size': 8, 'symbol': 'square'}
        })
    
    layout = {
        'title': f'Proyección de Mora - Cohorte {cohorte}',
        'xaxis': {'title': 'MOB (Meses desde operación)'},
        'yaxis': {'title': 'Mora >90d (%)'},
        'hovermode': 'closest',
        'height': 500,
        'template': 'plotly_white'
    }
    
    window.Plotly.newPlot('plotProyeccion', traces, layout)


def create_bar_chart():
    """Crea gráfico de barras"""
    df_proy = data_store['df_proy']
    
    observado = df_proy[df_proy['tipo'] == 'Observado']
    proyectado = df_proy[df_proy['tipo'] == 'Proyectado']
    
    traces = [
        {
            'x': observado['mob'].tolist(),
            'y': observado['mora_pct'].tolist(),
            'type': 'bar',
            'name': 'Observado',
            'marker': {'color': 'steelblue'}
        },
        {
            'x': proyectado['mob'].tolist(),
            'y': proyectado['mora_pct'].tolist(),
            'type': 'bar',
            'name': 'Proyectado',
            'marker': {'color': 'coral'}
        }
    ]
    
    layout = {
        'title': f'Observado vs Proyectado',
        'xaxis': {'title': 'MOB'},
        'yaxis': {'title': 'Mora >90d (%)'},
        'height': 400,
        'barmode': 'group'
    }
    
    window.Plotly.newPlot('plotBarras', traces, layout)


def create_factors_plot():
    """Crea gráfico de factores"""
    factors_detail = data_store['factors_detail']
    
    mobs = sorted(factors_detail.keys())
    means = [factors_detail[m]['mean'] for m in mobs]
    stds = [factors_detail[m]['std'] for m in mobs]
    
    upper = [m + s for m, s in zip(means, stds)]
    lower = [m - s for m, s in zip(means, stds)]
    
    traces = [
        {
            'x': mobs,
            'y': means,
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Factor promedio',
            'line': {'color': 'darkblue', 'width': 2}
        },
        {
            'x': mobs + mobs[::-1],
            'y': upper + lower[::-1],
            'fill': 'toself',
            'fillcolor': 'rgba(0,100,200,0.2)',
            'line': {'color': 'rgba(255,255,255,0)'},
            'name': '±1 Desv. Std.',
            'showlegend': True
        }
    ]
    
    layout = {
        'title': 'Factores de Desarrollo Históricos',
        'xaxis': {'title': 'MOB (Transición desde MOB anterior)'},
        'yaxis': {'title': 'Factor de Desarrollo'},
        'height': 400,
        'shapes': [{
            'type': 'line',
            'x0': min(mobs),
            'x1': max(mobs),
            'y0': 1.0,
            'y1': 1.0,
            'line': {'color': 'red', 'dash': 'dash'}
        }]
    }
    
    window.Plotly.newPlot('plotFactores', traces, layout)


# ============================================================
# FUNCIONES DE TABLA
# ============================================================

def create_detailed_table():
    """Crea tabla detallada HTML"""
    df_proy = data_store['df_proy']
    factors_detail = data_store['factors_detail']
    
    html = '<table><thead><tr>'
    html += '<th>MOB</th><th>Fecha</th><th>Mora %</th><th>Tipo</th><th>Factor</th><th>Intervalo ±1σ</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df_proy.iterrows():
        tipo_class = 'observado' if row['tipo'] == 'Observado' else 'proyectado'
        html += f'<tr class="{tipo_class}">'
        html += f'<td>{row["mob"]}</td>'
        html += f'<td>{row["fecha"]}</td>'
        html += f'<td>{row["mora_pct"]:.2f}%</td>'
        html += f'<td>{row["tipo"]}</td>'
        
        if row['tipo'] == 'Proyectado':
            html += f'<td>{row["factor"]:.3f}</td>'
            
            # Calcular intervalo
            mob = row['mob']
            if mob in factors_detail:
                std = factors_detail[mob]['std']
                factor = row['factor']
                mora = row['mora_pct']
                mora_base = mora / factor
                mora_low = mora_base * (factor - std)
                mora_high = mora_base * (factor + std)
                html += f'<td>[{mora_low:.1f}% - {mora_high:.1f}%]</td>'
            else:
                html += '<td>-</td>'
        else:
            html += '<td>-</td><td>-</td>'
        
        html += '</tr>'
    
    html += '</tbody></table>'
    
    document.getElementById('tablaDetallada').innerHTML = html


def create_summary_table():
    """Crea tabla resumen mensual"""
    df_proy = data_store['df_proy']
    proyectado = df_proy[df_proy['tipo'] == 'Proyectado']
    
    html = '<table><thead><tr>'
    html += '<th>Mes Calendario</th><th>MOB</th><th>Mora Proyectada</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in proyectado.iterrows():
        html += '<tr>'
        html += f'<td>{row["fecha"]}</td>'
        html += f'<td>{row["mob"]}</td>'
        html += f'<td>{row["mora_pct"]:.2f}%</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    
    document.getElementById('tablaResumen').innerHTML = html


def create_factors_table():
    """Crea tabla de factores"""
    factors_detail = data_store['factors_detail']
    
    html = '<table><thead><tr>'
    html += '<th>MOB</th><th>Factor Promedio</th><th>Desv. Std.</th><th>Mín</th><th>Máx</th><th>N° Obs.</th>'
    html += '</tr></thead><tbody>'
    
    for mob in sorted(factors_detail.keys()):
        detail = factors_detail[mob]
        html += '<tr>'
        html += f'<td>{mob}</td>'
        html += f'<td>{detail["mean"]:.4f}</td>'
        html += f'<td>{detail["std"]:.4f}</td>'
        html += f'<td>{detail["min"]:.4f}</td>'
        html += f'<td>{detail["max"]:.4f}</td>'
        html += f'<td>{detail["n"]}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    
    document.getElementById('tablaFactores').innerHTML = html


def create_export_table():
    """Crea tabla de export preview"""
    df_proy = data_store['df_proy']
    
    html = '<table><thead><tr>'
    html += '<th>Cohorte</th><th>MOB</th><th>Fecha</th><th>Mora %</th><th>Tipo</th><th>Factor</th>'
    html += '</tr></thead><tbody>'
    
    for _, row in df_proy.iterrows():
        html += '<tr>'
        html += f'<td>{row["cohorte"]}</td>'
        html += f'<td>{row["mob"]}</td>'
        html += f'<td>{row["fecha"]}</td>'
        html += f'<td>{row["mora_pct"]:.2f}%</td>'
        html += f'<td>{row["tipo"]}</td>'
        html += f'<td>{row["factor"]:.3f if pd.notna(row["factor"]) else "-"}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    
    document.getElementById('tablaExport').innerHTML = html


# ============================================================
# ACTUALIZACIÓN DE MÉTRICAS
# ============================================================

def update_metrics():
    """Actualiza las métricas en la UI"""
    df_proy = data_store['df_proy']
    cohorte = data_store['cohorte_objetivo']
    
    observado = df_proy[df_proy['tipo'] == 'Observado']
    
    mora_actual = float(observado['mora_pct'].iloc[-1])
    mora_final = float(df_proy['mora_pct'].iloc[-1])
    delta = mora_final - mora_actual
    fecha_final = df_proy['fecha'].iloc[-1]
    mob_actual = int(observado['mob'].max())
    
    document.getElementById('metricCohorte').textContent = cohorte
    document.getElementById('metricMobActual').textContent = str(mob_actual)
    document.getElementById('metricMoraActual').textContent = f'{mora_actual:.2f}%'
    document.getElementById('metricDelta').textContent = f'+{delta:.2f} pp proyectados'
    document.getElementById('metricProyFinal').textContent = f'{mora_final:.2f}%'
    document.getElementById('metricFecha').textContent = f'al {fecha_final}'


# ============================================================
# HANDLERS DE EVENTOS
# ============================================================

def handle_file_upload(event):
    """Maneja la carga de archivo CSV"""
    file = event.target.files.item(0)
    if not file:
        return
    
    file_reader = window.FileReader.new()
    
    def on_load(e):
        text_content = e.target.result
        
        # Cargar datos
        df, error = load_data_from_text(text_content)
        
        if error:
            status = document.getElementById('fileStatus')
            status.textContent = f'❌ Error: {error}'
            status.className = 'file-status error'
            return
        
        # Guardar en store
        data_store['df'] = df
        data_store['df_mob'] = create_mob_dataframe(df)
        data_store['df_pivot'] = data_store['df_mob'].pivot(
            index='cohorte', columns='mob', values='mora_pct'
        )
        data_store['factors'], data_store['factors_detail'] = calculate_development_factors(
            data_store['df_pivot']
        )
        
        # Actualizar UI
        status = document.getElementById('fileStatus')
        status.textContent = f'✓ Archivo cargado: {file.name} ({len(df)} cohortes)'
        status.className = 'file-status success'
        
        # Ocultar instrucciones
        document.getElementById('instructions').style.display = 'none'
        
        # Mostrar panel de configuración
        config_panel = document.getElementById('configPanel')
        config_panel.style.display = 'block'
        
        # Poblar selector de cohortes
        cohorte_select = document.getElementById('cohorteSelect')
        cohortes = sorted(df.index.tolist(), reverse=True)
        cohorte_select.innerHTML = ''
        for c in cohortes:
            option = document.createElement('option')
            option.value = c
            option.textContent = c
            cohorte_select.appendChild(option)
        
        # Actualizar slider info
        update_slider_info(None)
    
    file_reader.onload = create_proxy(on_load)
    file_reader.readAsText(file)


def update_slider_info(event):
    """Actualiza la información del slider"""
    cohorte_select = document.getElementById('cohorteSelect')
    mob_slider = document.getElementById('mobSlider')
    mob_value = document.getElementById('mobValue')
    mob_info = document.getElementById('mobInfo')
    
    if not data_store['df_pivot']:
        return
    
    cohorte = cohorte_select.value
    mob_objetivo = int(mob_slider.value)
    
    # Actualizar valor mostrado
    mob_value.textContent = str(mob_objetivo)
    
    # Obtener MOB actual de la cohorte
    if cohorte in data_store['df_pivot'].index:
        cohort_data = data_store['df_pivot'].loc[cohorte].dropna()
        mob_actual = int(cohort_data.index.max())
        mob_info.textContent = f'MOB actual de la cohorte: {mob_actual}'
        
        # Ajustar mínimo del slider
        mob_slider.min = str(mob_actual + 1)
        if mob_objetivo <= mob_actual:
            mob_slider.value = str(mob_actual + 1)
            mob_value.textContent = str(mob_actual + 1)


def handle_projection(event):
    """Maneja el botón de proyección"""
    cohorte = document.getElementById('cohorteSelect').value
    mob_objetivo = int(document.getElementById('mobSlider').value)
    
    data_store['cohorte_objetivo'] = cohorte
    
    # Mostrar spinner
    document.getElementById('loadingSpinner').style.display = 'block'
    document.getElementById('resultsPanel').style.display = 'none'
    
    # Proyectar (con pequeño delay para mostrar spinner)
    def do_projection():
        df_proy, error = project_cohort(
            data_store['df_pivot'],
            data_store['factors'],
            cohorte,
            mob_objetivo
        )
        
        if error:
            console.log(error)
            document.getElementById('loadingSpinner').style.display = 'none'
            return
        
        data_store['df_proy'] = df_proy
        
        # Actualizar métricas
        update_metrics()
        
        # Crear visualizaciones
        create_projection_plot()
        create_bar_chart()
        create_factors_plot()
        
        # Crear tablas
        create_detailed_table()
        create_summary_table()
        create_factors_table()
        create_export_table()
        
        # Mostrar resultados
        document.getElementById('loadingSpinner').style.display = 'none'
        document.getElementById('resultsPanel').style.display = 'block'
    
    window.setTimeout(create_proxy(do_projection), 100)


def handle_export_csv(event):
    """Exporta a CSV"""
    df_proy = data_store['df_proy']
    cohorte = data_store['cohorte_objetivo']
    
    csv_text = df_proy.to_csv(index=False)
    
    blob = Blob.new([csv_text], {type: 'text/csv'})
    url = URL.createObjectURL(blob)
    
    a = document.createElement('a')
    a.href = url
    a.download = f'proyeccion_{cohorte}.csv'
    a.click()
    
    URL.revokeObjectURL(url)


def handle_export_excel(event):
    """Exporta a Excel (simulado como CSV por limitaciones de PyScript)"""
    # En PyScript, openpyxl no está disponible, así que exportamos como CSV
    handle_export_csv(event)
    window.alert('Nota: La exportación Excel está limitada en el navegador. Se descargará como CSV.')


# ============================================================
# INICIALIZACIÓN
# ============================================================

def init():
    """Inicializa la aplicación"""
    # Registrar event listeners
    document.getElementById('csvFile').addEventListener(
        'change', create_proxy(handle_file_upload)
    )
    
    document.getElementById('cohorteSelect').addEventListener(
        'change', create_proxy(update_slider_info)
    )
    
    document.getElementById('mobSlider').addEventListener(
        'input', create_proxy(update_slider_info)
    )
    
    document.getElementById('projectBtn').addEventListener(
        'click', create_proxy(handle_projection)
    )
    
    document.getElementById('exportCsv').addEventListener(
        'click', create_proxy(handle_export_csv)
    )
    
    document.getElementById('exportExcel').addEventListener(
        'click', create_proxy(handle_export_excel)
    )
    
    console.log('PyScript app initialized!')


# Inicializar cuando PyScript esté listo
init()
