import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# data


mitjana = pd.read_csv(
    "mitjana_faltants.csv",

)
proporcio = pd.read_csv(
    "proporcio_faltants.csv",

)

variancia = pd.read_csv(
    "variancia_faltants.csv",
)

data = pd.read_csv(
    "df_all (2).csv",
)

drop_options = [
    {'label': 'SO2 (µg/m³)', 'value': 'SO2'},
    {'label': 'CO (mg/m³)', 'value': 'CO'},
    {'label': 'Ozó (µg/m³)', 'value': 'O3'},
    {'label': 'NO (µg/m³)', 'value': 'NO'},
    {'label': 'NO2 (µg/m³)', 'value': 'NO2'},
    {'label': 'NOx (µg/m³)', 'value': 'NOx'},
    {'label': 'PM10 (µg/m³)', 'value': 'PM10'},
    {'label': 'PM2.5 (µg/m³)', 'value': 'PM25'}
]

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

# Diccionari amb les estacions de València

list_of_locations = [
    {'label':"Viveros", 'value':"Viveros"},
    {'label':"Avenida Francia", 'value':"Avda. Francia"},
    {'label':"Bulevard Sur",  'value':"Bulevard Sud"},
    {'label':"Centro",  'value':"Valencia Centro"},
    {'label':"Molí del Sol",  'value':"Moli del Sol"},
    {'label':"Nazaret",  'value':"Nazaret Meteo"},
    {'label':"Pista de Silla",  'value':"Pista Silla"},
    {'label':"Politécnico",  'value':"Politecnico"}
]


col1, col2 = st.columns([1, 3])  # Ajusta los valores para cambiar el tamaño relativo de las columnas

# Colocar la imagen en la primera columna
with col1:
    st.image('4357542.png')  # Ajusta el width para cambiar el tamaño de la imagen

# Colocar el título en la segunda columna
with col2:
    st.write("""
    # Calidad del aire en la ciudad de Valencia
    """)

st.sidebar.title("Menú de Navegación")


opcion = st.sidebar.selectbox(
    "Elige una sección",
    ("Análisis Global", "Análisis por Estación", "Correlaciones entre variables")
)

if opcion == "Análisis Global":
    
    # Función para simular la navegación
    def navegar(seccion):
        st.session_state["pagina_actual"] = seccion

    # Inicializa el estado si no existe
    if "pagina_actual" not in st.session_state:
        st.session_state["pagina_actual"] = "Inicio"

    st.header("Análisis Global de sus Estaciones de Medición")

    col1, col2, col3 = st.columns(3)

    with col1:
        fecha_inicial = datetime(2022, 10, 1)
        fecha_minima = datetime(2018, 1, 1)
        fecha_maxima = datetime(2022, 12, 31)

        fecha_seleccionada = st.date_input(
            "Selecciona una fecha:",
            value=fecha_inicial,
            min_value=fecha_minima,
            max_value=fecha_maxima
        )

        # fecha seleccionada
        fecha = fecha_seleccionada.strftime("%B %Y")
        f=fecha.split(' ')


        month_name = f[0]
        esp=''
        month = 0

        if month_name == 'January':
            month = 1
            esp='Enero'
        elif month_name == 'February':
            month = 2
            esp='Febrero'
        elif month_name == 'March':
            month = 3
            esp='Marzo'
        elif month_name == 'April':
            month = 4
            esp='Abril'
        elif month_name == 'May':
            month = 5
            esp='Mayo'
        elif month_name == 'June':
            month = 6
            esp='Junio'
        elif month_name == 'July':
            month = 7
            esp='Julio'
        elif month_name == 'August':
            month = 8
            esp='Agosto'
        elif month_name == 'September':
            month = 9
            esp='Septiembre'
        elif month_name == 'October':
            esp='Octubre'
            month = 10
        elif month_name == 'November':
            month = 11
            esp='Noviembre'
        elif month_name == 'December':
            month = 12
            esp='Diciembre'
        else:
            print("Invalid month name")




        st.markdown(
           f"""
            <span style='font-size:14px;'>
            <b>Fecha seleccionada:</b> {esp} {f[1]}
            </span>
            
            """,
            unsafe_allow_html=True
        )


    # Controles de navegación
    
    with col2:
        st.button("Media aritmética", on_click=navegar, args=("Media",))
        st.button("Varianza", on_click=navegar, args=("Varianza",))
        st.button("Porcentaje de faltantes", on_click=navegar, args=("Proporcio",))

    with col3:

        st_drop_options = [option['label'] for option in drop_options]
        st_drop_values = {option['label']: option['value'] for option in drop_options}

        # Crear el selectbox en Streamlit
        selected_option_label = st.selectbox("Selecciona un contaminante:", st_drop_options)
        selected_option_value = st_drop_values[selected_option_label]
        col=selected_option_value.split(' ')
        # print(proporcio.columns)


       
        st.markdown(
           f"""
            <span style='font-size:14px;'>
            <b>Contaminante seleccionado:</b> {col[0]}
            </span>
            
            """,
            unsafe_allow_html=True
        )


    if st.session_state["pagina_actual"] == "Proporcio":

        st.header(f"Proporción de valores faltantes para {col[0]} en {esp} {f[1]}")
        # st.write("Aquí va el contenido de la página de inicio.")
        d = proporcio[proporcio['Year'] == int(f[1])]
       
        df=d[d['Mes'] == month]
        dff = df.dropna(subset=[col[0]])

        dff['Proporció de faltants'] = dff[col[0]].apply(lambda x: '<= 5% faltants' if x <= 5 else ('<= 10% faltants' if (x>5 and x<=10) else ('<= 20% faltants' if (x<=20 and x>10) else ('<= 30% faltants' if (x<=30 and x>20) else '>30% faltants') )))
                                                               

        # Definir mapa de colores para "color_discrete_map"
        color_map = {'<= 5% faltants': '#5b9b14', '<= 10% faltants': '#a7b726', '<= 20% faltants':'#e2cb0e', '<= 30% faltants':'#ec933e','>30% faltants':'#df3f0c' }
        
        sizes=[20 for i in range(0,len(dff))]
        fig = px.scatter_mapbox(dff, lat='lat', lon='long',size=sizes,height=560, hover_name='Estacion',
                                opacity=0.80, zoom=12,mapbox_style='open-street-map',
                        color='Proporció de faltants', color_discrete_map=color_map)
        fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},mapbox=dict(
            bearing=0,
            center=dict(
                lat=39.47057375657113,
                lon=-0.37641920323962136
            )), hovermode='closest')
        fig.update_traces(marker=dict(sizemode='area', sizemin=15),  # Establecer tamaño mínimo de 10
                              hovertemplate='<b>%{hovertext}</b>')
        
        st.plotly_chart(fig, use_container_width=True)

    
       
    elif st.session_state["pagina_actual"] == "Media":
        st.header(f"Media aritmética para {col[0]} en {esp} {f[1]}")
        # st.write("Contenido de análisis de datos.")

        d = mitjana[(mitjana['Year'] == int(f[1])) & (mitjana['Mes'] == month)]
        
        dff = d.dropna(subset=[col[0]])

        # print(dff)
        fig = px.scatter_mapbox(dff, lat='lat', lon='long', size=col[0], height=560, hover_name='Estacion',
                                opacity=0.80, size_max=30, zoom=12, mapbox_style='open-street-map',
                                color_discrete_sequence=['#5b9b14'], hover_data={'lat':False, 'long':False})

        fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                        mapbox=dict(bearing=0, center=dict(lat=39.47057375657113, lon=-0.37641920323962136)),
                        hovermode='closest')

        fig.update_traces(marker=dict(sizemode='area', sizemin=6))

        st.plotly_chart(fig, use_container_width=True)




    elif st.session_state["pagina_actual"] == "Varianza":
        st.header(f"Varianza para {col[0]} en {esp} {f[1]}")
        # st.write("Contenido de análisis de datos.")

        d = variancia[(variancia['Year'] == int(f[1])) & (variancia['Mes'] == month)]
        
        dff = d.dropna(subset=[col[0]])

        # print(dff)
       
    
        fig = px.scatter_mapbox(dff, lat='lat', lon='long', size=col[0], height=560, hover_name='Estacion',
                                opacity=0.80, size_max=30, zoom=12, mapbox_style='open-street-map',
                                color_discrete_sequence=['#5b9b14'], hover_data={'lat':False, 'long':False})

        fig.update_layout(margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                        mapbox=dict(bearing=0, center=dict(lat=39.47057375657113, lon=-0.37641920323962136)),
                        hovermode='closest')

        fig.update_traces(marker=dict(sizemode='area', sizemin=6))

        st.plotly_chart(fig, use_container_width=True)

      
elif opcion == "Análisis por Estación":
    st.header("Análisis Detallado por Estaciones")

    col1, col2, col3 = st.columns(3)

    with col1:
        fecha_inicial = datetime(2022, 10, 1)
        fecha_minima = datetime(2018, 1, 1)
        fecha_maxima = datetime(2022, 12, 31)

        fecha_seleccionada = st.date_input(
            "Selecciona una fecha:",
            value=fecha_inicial,
            min_value=fecha_minima,
            max_value=fecha_maxima
        )

        # fecha seleccionada
        fecha = fecha_seleccionada.strftime("%B %Y")
        f=fecha.split(' ')


        month_name = f[0]
        esp=''
        month = 0

        if month_name == 'January':
            month = 1
            esp='Enero'
        elif month_name == 'February':
            month = 2
            esp='Febrero'
        elif month_name == 'March':
            month = 3
            esp='Marzo'
        elif month_name == 'April':
            month = 4
            esp='Abril'
        elif month_name == 'May':
            month = 5
            esp='Mayo'
        elif month_name == 'June':
            month = 6
            esp='Junio'
        elif month_name == 'July':
            month = 7
            esp='Julio'
        elif month_name == 'August':
            month = 8
            esp='Agosto'
        elif month_name == 'September':
            month = 9
            esp='Septiembre'
        elif month_name == 'October':
            esp='Octubre'
            month = 10
        elif month_name == 'November':
            month = 11
            esp='Noviembre'
        elif month_name == 'December':
            month = 12
            esp='Diciembre'
        else:
            print("Invalid month name")

        st.markdown(
           f"""
            <span style='font-size:14px;'>
            <b>Fecha seleccionada:</b> {esp} {f[1]}
            </span>
            
            """,
            unsafe_allow_html=True
        )
    
    with col2:

        st_drop_options_est = [option['label'] for option in list_of_locations]
        st_drop_values_est = {option['label']: option['value'] for option in list_of_locations}

        selected_option_label_est = st.selectbox("Selecciona una estación:", st_drop_options_est)
        selected_option_value_est = st_drop_values_est[selected_option_label_est]
        # print(selected_option_value)

       
        st.markdown(
           f"""
            <span style='font-size:14px;'>
            <b>Estación seleccionada: </b> {selected_option_value_est}
            </span>
            
            """,
            unsafe_allow_html=True
        )

    

    with col3:

        st_drop_options = [option['label'] for option in drop_options]
        st_drop_values = {option['label']: option['value'] for option in drop_options}

        # Crear el selectbox en Streamlit
        selected_option_label = st.selectbox("Selecciona un contaminante:", st_drop_options)
        selected_option_value = st_drop_values[selected_option_label]
        col=selected_option_value.split(' ')
        # print(proporcio.columns)


       
        st.markdown(
           f"""
            <span style='font-size:14px;'>
            <b>Contaminante seleccionado:</b> {col[0]}
            </span>
            
            """,
            unsafe_allow_html=True
        )

        month_name = f[0]
        esp=''
        month = 0

        if month_name == 'January':
            month = 1
            esp='Enero'
        elif month_name == 'February':
            month = 2
            esp='Febrero'
        elif month_name == 'March':
            month = 3
            esp='Marzo'
        elif month_name == 'April':
            month = 4
            esp='Abril'
        elif month_name == 'May':
            month = 5
            esp='Mayo'
        elif month_name == 'June':
            month = 6
            esp='Junio'
        elif month_name == 'July':
            month = 7
            esp='Julio'
        elif month_name == 'August':
            month = 8
            esp='Agosto'
        elif month_name == 'September':
            month = 9
            esp='Septiembre'
        elif month_name == 'October':
            esp='Octubre'
            month = 10
        elif month_name == 'November':
            month = 11
            esp='Noviembre'
        elif month_name == 'December':
            month = 12
            esp='Diciembre'
        else:
            print("Invalid month name")
    
    data = data[(data['Year'] == int(f[1])) | (data['Month'] == int(month)) | (data['Estacion'] == selected_option_value_est)]
    col1, col2 = st.columns([1, 3])
                            
    with col1:
        dias = data.groupby('Dia de la semana')[col[0]].mean().reset_index().sort_values(by='Dia de la semana', ascending=True)
        dias[col[0]] = dias[col[0]].round(2)
        fig = px.pie(dias, values=col[0], names='Dia de la semana', color_discrete_sequence=px.colors.qualitative.Set2, hole=.5)
        fig.update_traces(textposition='inside', textinfo='value+label')
        fig.update_layout(title_text=f'Media de {col[0]} por día', showlegend=False )
        st.plotly_chart(fig,use_container_width=True)

    # print(dias)
    with col2: 
        hora = data.groupby('Hora')[col[0]].mean().reset_index().sort_values(by=col[0], ascending=True)

        fig = px.bar(hora, 
                        x='Hora', 
                        y=col[0],
                        orientation='v', color_discrete_sequence=px.colors.qualitative.Set2
                        # labels={'institution': 'Count of universities', 'continent': 'Continent'},
                        )

        fig.update_layout(title_text=f'Media de {col[0]} por hora', title_x=0.38)
        st.plotly_chart(fig,use_container_width=True)

    mes = data.groupby('Day')[col[0]].mean().reset_index().sort_values(by=col[0], ascending=True)

    fig = px.line(mes.sort_values(by='Day'), 
                x='Day', 
                y=col[0],
                 color_discrete_sequence=px.colors.qualitative.Set2)

    fig.update_layout(title_text=f'Media de {col[0]} por mes', title_x=0.38)
    st.plotly_chart(fig,use_container_width=True)

elif opcion == "Correlaciones entre variables":
    st.header("Correlaciones entre variables")
    col1, col2,col3 = st.columns(3)

    with col1:
        
        fecha_inicial = datetime(2022, 10, 1)
        fecha_minima = datetime(2018, 1, 1)
        fecha_maxima = datetime(2022, 12, 31)

        fecha_seleccionada = st.date_input(
            "Selecciona una fecha:",
            value=fecha_inicial,
            min_value=fecha_minima,
            max_value=fecha_maxima
        )

        # fecha seleccionada
        fecha = fecha_seleccionada.strftime("%B %Y")
        f=fecha.split(' ')


        month_name = f[0]
        esp=''
        month = 0

        if month_name == 'January':
            month = 1
            esp='Enero'
        elif month_name == 'February':
            month = 2
            esp='Febrero'
        elif month_name == 'March':
            month = 3
            esp='Marzo'
        elif month_name == 'April':
            month = 4
            esp='Abril'
        elif month_name == 'May':
            month = 5
            esp='Mayo'
        elif month_name == 'June':
            month = 6
            esp='Junio'
        elif month_name == 'July':
            month = 7
            esp='Julio'
        elif month_name == 'August':
            month = 8
            esp='Agosto'
        elif month_name == 'September':
            month = 9
            esp='Septiembre'
        elif month_name == 'October':
            esp='Octubre'
            month = 10
        elif month_name == 'November':
            month = 11
            esp='Noviembre'
        elif month_name == 'December':
            month = 12
            esp='Diciembre'
        else:
            print("Invalid month name")

        st.markdown(
           f"""
            <span style='font-size:14px;'>
            <b>Fecha seleccionada:</b> {esp} {f[1]}
            </span>
            
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        etiquetas = [opcion['label'] for opcion in drop_options]

        etiqueta1 = st.selectbox('Elige el primer contaminante:', etiquetas)
    
    with col3:
        etiquetas_restantes = [etiqueta for etiqueta in etiquetas if etiqueta != etiqueta1]

        etiqueta2 = st.selectbox('Elige el segundo contaminante:', etiquetas_restantes)

    valores_seleccionados = [opcion['value'] for opcion in drop_options if opcion['label'] in [etiqueta1, etiqueta2]]

    with col2:
        st.markdown(
                f"""
                    <span style='font-size:14px;'>
                    <b>Contaminantes seleccionados:</b> {valores_seleccionados[0]} y {valores_seleccionados[1]}
                    </span>
                    
                    """,
                    unsafe_allow_html=True
                )
            
        month_name = f[0]
        esp=''
        month = 0

    if month_name == 'January':
        month = 1
        esp='Enero'
    elif month_name == 'February':
        month = 2
        esp='Febrero'
    elif month_name == 'March':
        month = 3
        esp='Marzo'
    elif month_name == 'April':
        month = 4
        esp='Abril'
    elif month_name == 'May':
        month = 5
        esp='Mayo'
    elif month_name == 'June':
        month = 6
        esp='Junio'
    elif month_name == 'July':
        month = 7
        esp='Julio'
    elif month_name == 'August':
        month = 8
        esp='Agosto'
    elif month_name == 'September':
        month = 9
        esp='Septiembre'
    elif month_name == 'October':
        esp='Octubre'
        month = 10
    elif month_name == 'November':
        month = 11
        esp='Noviembre'
    elif month_name == 'December':
        month = 12
        esp='Diciembre'
    else:
        print("Invalid month name")
    print(f[1],month)
    data = data[(data['Year'] == int(f[1])) & (data['Month'] == int(month))]
    print(data['Month'].unique(), data['Year'].unique())

    if valores_seleccionados[0]=='PM25':
        valores_seleccionados[0]='PM2.5'
    elif valores_seleccionados[1]=='PM25':
        valores_seleccionados[1]='PM2.5'
    else: 
        pass
    
    fig = px.scatter(data, x=valores_seleccionados[0], y=valores_seleccionados[1],
                     labels={
                         valores_seleccionados[0]: valores_seleccionados[0],
                         valores_seleccionados[1]: valores_seleccionados[1]
                     },
                     title=f"Scatter Plot de {valores_seleccionados[0]} vs {valores_seleccionados[1]}")
    st.plotly_chart(fig)

