import streamlit as st

st.title("Sistema de Seguimiento Académico")

# Inicialización de sesión de ramos
if 'ramos' not in st.session_state:
    st.session_state.ramos = {}

# Agregar ramos
st.header("Agregar nuevo ramo")
nuevo_ramo = st.text_input("Nombre del ramo:", key="nuevo_ramo")
if st.button("Agregar ramo"):
    if nuevo_ramo and nuevo_ramo not in st.session_state.ramos:
        st.session_state.ramos[nuevo_ramo] = []

# Mostrar ramos
st.header("Ramos existentes")
for ramo in st.session_state.ramos.keys():
    with st.expander(ramo):
        st.subheader("Evaluaciones")

        nombre_eval = st.text_input(f"Nombre evaluación ({ramo})", key=f"eval_{ramo}")
        nota_eval = st.number_input(f"Nota (10-70)", min_value=10, max_value=70, key=f"nota_{ramo}")
        peso_eval = st.number_input(f"Peso (%)", min_value=0, max_value=100, key=f"peso_{ramo}")

        if st.button("Agregar evaluación", key=f"add_eval_{ramo}"):
            st.session_state.ramos[ramo].append({
                'evaluacion': nombre_eval,
                'nota': nota_eval,
                'peso': peso_eval
            })

        total_peso = sum(ev['peso'] for ev in st.session_state.ramos[ramo])
        suma_ponderada = sum(ev['nota'] * ev['peso'] / 100 for ev in st.session_state.ramos[ramo])

        st.write(f"Suma de pesos: {total_peso}%")
        st.write(f"Presentación: {suma_ponderada:.1f}")

        if total_peso == 100:
            if suma_ponderada > 50:
                st.success("Eximido")
                nota_final = suma_ponderada
            else:
                examen = st.number_input(f"Nota Examen (10-70) ({ramo})", min_value=10, max_value=70, key=f"examen_{ramo}")
                nota_final = suma_ponderada * 0.7 + examen * 0.3
            st.write(f"Nota Final: {nota_final:.1f}")
        else:
            st.warning("Los pesos deben sumar 100% para calcular el resultado final.")

# Resumen general
st.header("Resumen General")
total_presentaciones = [
    sum(ev['nota'] * ev['peso'] / 100 for ev in evaluaciones)
    for evaluaciones in st.session_state.ramos.values()
    if sum(ev['peso'] for ev in evaluaciones) == 100
]

if total_presentaciones:
    promedio_actual = sum(total_presentaciones) / len(total_presentaciones)
    st.write(f"Promedio Actual de Presentación: {promedio_actual:.1f}")
else:
    st.write("Aún no hay ramos con presentación completa.")
