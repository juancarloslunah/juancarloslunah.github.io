import pandas as pd
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive
import ipywidgets as widgets
import numpy as np
from IPython.core.display import HTML, display

url="https://datosabiertos.bogota.gov.co/dataset/44eacdb7-a535-45ed-be03-16dbbea6f6da/resource/b64ba3c4-9e41-41b8-b3fd-2da21d627558/download/osb_enftransm-covid-19.csv"
df=pd.read_csv(url,encoding='latin1',error_bad_lines=False,sep =';')
df = df.dropna()
df = df.reset_index(drop=True)
df=df[df['Fecha de inicio de síntomas'].str.contains("/")]
#df=pd.read_csv(url,encoding='latin1')
df["Estado"]=[i.replace("Fallecido No aplica No causa Directa","Fallecido") for i in df["Estado"]]# Armando una lista que corrige el error de digitación
df["Estado"]=[i.replace(" ","") for i in df["Estado"]]

### Primer Widget

def f(localidad):
    df2=df[df["Localidad de residencia"]==localidad].groupby("Estado").count()
    ind=df2.index
    data=df2["Edad"]
    fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(data,wedgeprops=dict(width=0.5), 
                                      startangle=-40)
    pct=["{:.2%}".format(da/sum(data)) for da in data]
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))        
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(ind[i]+"  "+pct[i], xy=(x, y),
                    xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)
    ax.set_title("Distribución de casos en "+localidad+
                 "\n\n"+str(sum(data))+" casos confirmados"+"\n")

    plt.show()
    return
Liloc=list(df["Localidad de residencia"].unique()) # Extraemos la lista de localidades

W1=interactive(f, localidad=widgets.Dropdown(options=Liloc,value="Usme", 
                                       description="Localidad:", 
                                       disabled=False,))

### Segundo Widget

def filtroedad(edades):    
    Edad_Filtro=df[df["Edad"]>=edades[0]][df[df["Edad"]>=edades[0]]["Edad"]<=edades[1]]
    Casos=Edad_Filtro.groupby("Localidad de residencia").count()
    Casos=Casos.sort_values("Edad")
    fig, ax = plt.subplots(figsize=(10, 8))
    # Una función para poner la cantidad de casos
    def autolabel(rects):
        for rect in rects:
            width = rect.get_width()
            ax.annotate('{}'.format(width),
                        xy=(width,rect.get_y() + rect.get_height() / 2),
                        xytext=(3,0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='left', va='center')

    rects=ax.barh(Casos.index,Casos["Edad"])
    ax.set(xlim=(0, max(Casos["Edad"])*1.12))
    plt.title("En total hay "+str(sum(Casos["Edad"]))+" en Bogotá")
    autolabel(rects)
    plt.show()
    return
wid=widgets.IntRangeSlider(
    value=[10, 70],
    min=0,
    max=120,
    step=1,
    description='Edades:',
    orientation='horizontal',
    readout=True,
    readout_format='d',
)
W2=interactive(filtroedad,edades=wid)


#### Dashboard

def miprimerdashboard():
    display(HTML(             '<h2>Casos distribuidos por localidades en Bogotá</h2>'+
                '<p>El siguiente gráfico muestra las distribuciones por localidades en Bogotá:</p>'))
    Casos=df.groupby("Localidad de residencia").count()
    Casos=Casos.sort_values("Edad")
    fig, ax = plt.subplots(figsize=(10, 8))
    # Una función para poner la cantidad de casos
    def autolabel(rects):
        for rect in rects:
            width = rect.get_width()
            ax.annotate('{}'.format(width),
                        xy=(width,rect.get_y() + rect.get_height() / 2),
                        xytext=(3,0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='left', va='center')

    rects=ax.barh(Casos.index,Casos["Edad"])
    ax.set(xlim=(0, max(Casos["Edad"])+2000))
    plt.title("En total hay "+str(sum(Casos["Edad"]))+" en Bogotá")
    autolabel(rects)
    plt.show()
    display(HTML('<h2>Proporción de casos en cada una de las localidades en Bogotá</h2>'+
                '<p>Seleccione la localidad e identifique cuántos casos hay en cada Localidad Bogotana:</p>'))
  
    display(W1)
    display(HTML('<h2>Distribución por edades</h2>'+
                '<p>Ahora veamos como se dsitribuyen por edades:</p>'))
  
    display(W2)
    
    return
