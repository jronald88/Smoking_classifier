import streamlit as st
import pandas as pd
import numpy as np
from pickle import load
import json
from sklearn.preprocessing import LabelEncoder

st.title("Hello World!")

st.set_page_config(page_title="Smoking Predictor by Jason Ronald", layout="wide")

# counter 

if "counter" not in st.session_state:
    st.session_state.counter = 0
st.session_state.counter += 1
st.write(f"This page has run {st.session_state.counter} times.")
# st.button("Run it again")

# load the model
# model = load(open("../models/decision_tree_classifier_default_42.sav", "rb"))
# model = load(open("../models/randomforest_classifier_mejores parametros_42.sav", "rb"))
model = load(open("../models/random_forest_classsifier_default.sav", "rb"))
class_dict = {
    "0": "Non Smoker",
    "1": "Smoker"
}

# cargar data original para sacar categorias de variables

data = pd.read_csv('../data/processed/X_test.csv') 

# Leer los mapeos desde el archivo .json
with open('label_encoders.json', 'r') as file:
    label_mappings = json.load(file)

# Reconstruir los LabelEncoders desde los mapeos
label_encoders = {}
for column, mapping in label_mappings.items():
    encoder = LabelEncoder()
    encoder.classes_ = np.array(mapping['classes'])
    # encoder.classes_ = mapping['classes']
    label_encoders[column] = encoder

# Crear una función para obtener categorías únicas
def get_unique_values(campo):
    return label_encoders[campo].classes_


# ---------------- SIDEBAR -----------------

st.sidebar.title("Options")
st.sidebar.header('1. Quantative Parameters')

cap_d = st.sidebar.slider("Diametro del sombrero (cm)", min_value = 0.38, max_value = 62.9, step = 1.0)
stem_h = st.sidebar.slider("Altura del pie (cm)", min_value = 0.0, max_value = 33.9, step = 1.0)
stem_w = st.sidebar.slider("Ancho del pie (mm)", min_value = 10.0, max_value = 100.0, step = 1.0)

st.sidebar.header('2. Qualtitative Parameters')

# Crear selectboxes para cada variable categórica
cap_shape = st.sidebar.selectbox("Forma del sombrero", get_unique_values("cap-shape"))
gill_color = st.sidebar.selectbox("Color de las láminas", get_unique_values("gill-color"))
stem_surface = st.sidebar.selectbox("Superficie del pie", get_unique_values("stem-surface"))
stem_color = st.sidebar.selectbox("Color del pie", get_unique_values("stem-color"))
veil_color = st.sidebar.selectbox("Color del velo", get_unique_values("veil-color"))
spore_print_color = st.sidebar.selectbox("Color de las esporas", get_unique_values("spore-print-color"))
season = st.sidebar.selectbox("Temporada", get_unique_values("season"))

# Transformar los valores seleccionados usando los LabelEncoders
cap_shape_enc = label_encoders['cap-shape'].transform([cap_shape])[0]
gill_color_enc = label_encoders['gill-color'].transform([gill_color])[0]
stem_surface_enc = label_encoders['stem-surface'].transform([stem_surface])[0]
stem_color_enc = label_encoders['stem-color'].transform([stem_color])[0]
veil_color_enc = label_encoders['veil-color'].transform([veil_color])[0]
spore_print_color_enc = label_encoders['spore-print-color'].transform([spore_print_color])[0]
season_enc = label_encoders['season'].transform([season])[0]

# --------------- MAIN BODY --------------------------------------

st.header("Smokers: Machine Learning Classifier")
col1, col2 = st.columns([2,2])

with col1:
        st.image('./images/datasetas-logo_sm.jpg', width=400, use_column_width = 'auto')

with col2:
        st.write("Welcome to a Smoking Classifier page. This tool is intended to help predict whether someone is a smoker based on their body signals. Please follow the next steps:")

with st.expander("Instructions"):
        st.write("Step 1: Introduce the quantitive parameters: one the left of the screen, you will find various sliders to assist you.")
        st.write("Step 2: Introduce the qualtitative parameters: Underneath the sliders, youll find various categories to select from. Select an option from each.")
        st.write("Step 3: Make a prediction: Once all parameters have been introduced, click the Predict button in the middle of the page. The application make a prediction and diplay it.")
        st.write("Step 4: Interpret the result: The application will use the best classifier to make a prediciton whether someone is a smoker or not.") 

with st.container(border=True):
        st.write("IMPORTANT: This is a tool for educational purposes and is by no means intended for professional use.")
with st.container():
        st.write("I hope this has been useful. Enjoy!")

st.divider()

if st.button("Predict"):
  
    prediction = str(model.predict([[cap_d, stem_h, stem_w, cap_shape_enc, gill_color_enc, stem_surface_enc, stem_color_enc, veil_color_enc, spore_print_color_enc, season_enc ]])[0])
    pred_class = class_dict[prediction]
    st.write("Prediction:", pred_class)
    st.success('IMPORTANT: Bear in mind that this model has an accuracy of approximately 90% on its predictions, it is not 100% accurate!')
    # st.balloons()

st.divider()

# -------------------------------TABS --------------------------------
  
tab1, tab2, tab3 = st.tabs(["About the data y the EDA", "Machine Learning Models", "Reflections"])

tab1.write("1. About the data")
tab1.write('''
            The original dataset was downloaded from kaggle.com/kukuroo3/body-signal-of-smoking and uploaded for public use.
            Health checkup information refers to the general health of employees and dependents aged 40 or older, local 
            subscribers who are the head of household, and local subscribers aged 40 or older. Screening results and basic 
            information (gender, age group, trial code, etc.) of 1 million people in each year who have a life transition 
            period health checkup history that those who have reached the age of 40 and 66 among those subject to general 
            health checkup It is open data consisting of and examination details (height, weight, total cholesterol, hemoglobin, etc.) 
           ''')
tab1.write('''
           The data shows: 
 - High variability: All variables exhibit considerable variability, with high standard deviations relative to their means.
           
 - .

Este análisis descriptivo nos da una base para entender la distribución y las características de las variables en el dataset de setas. 
           Es un primer paso crucial antes de proceder con análisis más complejos o modelos predictivos.           
''')
tab1.write('''
 - Algunas variables tienen valor claramente predominante: habitat, ring-type, veil-color, y algo menos en otras como cap-color
           Las 3 variables numericas tienen un numero importante de outliers. 
           Dado el caracter de los datos y a su contexto de alimentación y salud pública  (aunque haya muy poco valores atipicos, 
           estos podrian ser determinantes a la hora de su comestibilidad) y el alto numero de variables que participan, 
           parece lo mas prudente mantener los outliers
   ''')
tab1.write('''
           ''')

tab1.write("2. Data graphics")
with tab1:
   st.image("./pictures/smoking_dist.jpg", use_column_width = 'auto', caption ="Distribution of Smokers")
with tab1:
   st.image("./pictures/density_rel_BMI_smoking.jpg", use_column_width = 'auto', caption ="Density Relationship BMI against Smokers")
with tab1:
   st.image("./pictures/lmplot_gender_caries_smoking-jpg.png", use_column_width = 'auto', caption ="Supervised Machine Learning Model Comparison")   



tab2.write("MACHINE LEARNING MODELS")
tab2.write('''
           Como comentamos al principio, nuestro sistema de clasificación estaría basado en los atributos de las setas visibles a simple vista.
Elegir el modelo adecuado y ajustar sus hiper parámetros son pasos críticos en cualquier proyecto de aprendizaje automático.
           ''') 
tab2.write(''' 
           Después del EDA sabemos que nuestros datos tienen distribuciones asimétricas, con valores atípicos y extremos, mucha variabilidad entre atributos, 
           y muchos valores faltantes. Esto nos sirve como indicación para saber qué algoritmo puede dar los resultados más óptimos. 
En este proyecto, varios algoritmos de ML han sido testados.
           ''') 
tab2.write(''' 
           The use of a random forest classifier was the correct option after exploring various others. It was imperative to compare with other models like K-Nearest Neighbour and Logistic 
           Regression, for example, to ensure the best model decision.
        ''')
tab2.write("MODEL 1: Random Forest Classifier:")
tab2.write(''' 
           Organiza decisiones y sus posibles consecuencias en una estructura de árbol. 
           Cada nodo interno representa una prueba en una característica (por ejemplo, si una característica es menor o mayor que un valor específico), 
           cada rama representa el resultado de la prueba, y cada nodo hoja representa una etiqueta de clase (para clasificación) o un valor continuo (para regresión). 
           El camino desde la raíz del árbol hasta una hoja representa una serie de decisiones que conducen a una predicción.
           ''')
with tab2:
   st.image("./images/output_dt.png", use_column_width = 'auto')

tab2.write("MODELO 2: RANDOM FOREST:")
tab2.write(''' 
           Se basa en la construcción de múltiples árboles de decisión durante el entrenamiento y su combinación para mejorar la precisión 
           y controlar el sobreajuste. Cada árbol en el bosque se entrena con una muestra diferente del conjunto de datos y se utiliza un subconjunto aleatorio 
           de características en cada división del árbol. La predicción final del modelo se obtiene tomando la mayoría de los votos (en el caso de la clasificación). 
            ''')        
with tab2:
   st.image("./images/rf_trees.png", use_column_width = 'auto')

tab2.write("MODELO 3: K-NEAREST NEIGHBOURS:")
tab2.write(''' 
           El algoritmo asigna una clase a un dato nuevo basándose en la clase más frecuente 
           entre sus k vecinos más cercanos en el espacio de características, donde k es un número entero predefinido.
        ''')
with tab2:
   st.image("./images/output_knn_cm.png", use_column_width = 'auto')


tab3.write("3. Reflexiones y dificultades")
tab3.write('''
           La reflexion despues de un proyecto es siempre muy enriquecedora. La metacognición (análisis del proceso de aprendizaje) 
           es un proceso clave que aporta enormemente al aprendizaje. Algunos puntos para reflexionar son:
           ''')
tab3.write('''
           1. Importancia del dominio del problema: Trabajar con datos relacionados con la alimentación y la salud pública 
           requiere un entendimiento profundo del dominio. Es crucial asegurarse de tener información precisa y actualizada 
           sobre las características de las setas y los riesgos asociados. 
           En este caso, los datos vienen con la garantia de un equipo de investigadores de la Universidad de Marburg, en Alemania
           ''')
tab3.write('''
           2. Preprocesamiento de datos: En este proyecto, el preprocesamiento de datos juega un papel crucial, 
           especialmente en la limpieza de datos y la codificación de variables categóricas. 
           Asegurarse de que los datos estén correctamente preparados y que las transformaciones como el encoding 
           se realicen de manera adecuada es fundamental para el rendimiento del modelo.
           ''')        
tab3.write('''
            3. Selección y ajuste de modelo: Elegir el modelo adecuado y ajustar sus hiperparámetros son pasos críticos 
            en cualquier proyecto de aprendizaje automático. En este proyecto, Decision Tree era una excelente opcion inicial, 
            pero es un modelo que puede tener problemas de sobrejauste. Mejorar sus resultados y compararlos con otros modelo como KNN 
            ha sido esencial para confirmar las validez de sus predicciones
            ''')
tab3.write('''
            4. Interpretación de resultados: Interpretar los resultados del modelo es clave para entender su eficacia y 
            posibles áreas de mejora. Esto incluye analizar métricas de rendimiento como precisión, recall y la matriz de confusión, 
            así como explorar errores comunes cometidos por el modelo.
            ''')
tab3.write('''
           5. Ética y responsabilidad: Dado que este modelo puede tener implicaciones directas en la salud y seguridad de las personas, 
           es fundamental abordar cuestiones éticas y de responsabilidad. Esto incluye la transparencia en la interpretación de resultados, 
           así como la educación sobre las limitaciones del modelo y la importancia de la consulta con expertos en setas antes 
           de tomar decisiones basadas en predicciones.
           ''')
tab3.write('''
           6. Mejoras futuras: Siempre hay espacio para mejorar un proyecto. Se podría considerar la expansión del conjunto de datos, 
           explorar técnicas más avanzadas de modelado como el ensamblaje de modelos o incluso aplicar técnicas de explicabilidad del modelo 
           (como SHAP, LIME, PDP), para entender mejor las decisiones del mismo.
           ''')
tab3.write('''
           En resumen, trabajar en un proyecto como este no solo implica desarrollar habilidades técnicas en aprendizaje automático, 
           sino también ser consciente del contexto y las implicaciones prácticas de los resultados.
           ''')

with tab3:
   st.image("./images/logo2.jpg", use_column_width = 'auto')
"""