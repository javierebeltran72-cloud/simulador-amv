import streamlit as st
import pandas as pd

# ==========================
# CONFIGURACIÓN
# ==========================

st.set_page_config(
    page_title="Simulador AMV",
    layout="wide"
)

st.title("📈 Simulador AMV")

# ==========================
# CARGAR EXCEL
# ==========================

preguntas = pd.read_excel(
    "preguntas.xlsx",
    sheet_name=0
)

respuestas = pd.read_excel(
    "preguntas.xlsx",
    sheet_name=1
)

# ==========================
# VARIABLES DE SESIÓN
# ==========================

if "indice" not in st.session_state:
    st.session_state.indice = 0

if "aciertos" not in st.session_state:
    st.session_state.aciertos = 0

if "respondida" not in st.session_state:
    st.session_state.respondida = False

if "resultado" not in st.session_state:
    st.session_state.resultado = ""

# ==========================
# DATOS GENERALES
# ==========================

total = len(preguntas)

st.success(f"Preguntas cargadas: {total}")

st.info(
    f"Pregunta {st.session_state.indice + 1} de {total}"
)

st.info(
    f"Aciertos: {st.session_state.aciertos}"
)

# ==========================
# OBTENER PREGUNTA ACTUAL
# ==========================

fila = preguntas.iloc[st.session_state.indice]

st.markdown(
    f"## Pregunta {fila['ID']}"
)

st.markdown(
    f"### {fila['Pregunta']}"
)

# ==========================
# OPCIONES
# ==========================

opciones = {
    "A": fila["A"],
    "B": fila["B"],
    "C": fila["C"],
    "D": fila["D"]
}

respuesta_usuario = st.radio(
    "Seleccione una respuesta:",
    options=list(opciones.keys()),
    format_func=lambda x: f"{x}) {opciones[x]}",
    key=f"pregunta_{st.session_state.indice}"
)

# ==========================
# BOTÓN VERIFICAR
# ==========================

if st.button("✅ Verificar") and not st.session_state.respondida:

    respuesta_correcta = respuestas.loc[
        respuestas["ID"] == fila["ID"],
        "RespuestaCorrecta"
    ].values[0]

    if respuesta_usuario == respuesta_correcta:

        st.session_state.resultado = "correcto"
        st.session_state.aciertos += 1

    else:

        st.session_state.resultado = (
            f"incorrecto|{respuesta_correcta}"
        )

    st.session_state.respondida = True
    st.rerun()

# ==========================
# MOSTRAR RESULTADO
# ==========================

if st.session_state.respondida:

    if st.session_state.resultado == "correcto":

        st.success("✅ Correcto")

    else:

        respuesta_correcta = (
            st.session_state.resultado.split("|")[1]
        )

        st.error(
            f"❌ Incorrecto. La respuesta correcta era: {respuesta_correcta}"
        )

# ==========================
# SIGUIENTE PREGUNTA
# ==========================

if st.session_state.respondida:

    if st.button("➡️ Siguiente"):

        if st.session_state.indice < total - 1:

            st.session_state.indice += 1
            st.session_state.respondida = False
            st.session_state.resultado = ""

            st.rerun()

        else:

            st.balloons()

            st.success(
                f"Examen terminado. "
                f"Aciertos: {st.session_state.aciertos} de {total}"
            )

# ==========================
# REINICIAR EXAMEN
# ==========================

st.divider()

if st.button("🔄 Reiniciar examen"):

    st.session_state.indice = 0
    st.session_state.aciertos = 0
    st.session_state.respondida = False
    st.session_state.resultado = ""

    st.rerun()
    