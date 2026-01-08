import streamlit as st
import pandas as pd
from datetime import date
from utils.api_client import APIClient

st.set_page_config(page_title="DailyTask 2026", layout="wide")

api = APIClient()

st.title("📌 Control de Tareas Diarias 2026")

# Sidebar para filtros e importar
st.sidebar.header("Opciones")
start_date = st.sidebar.date_input("Fecha Inicio", date(2026, 1, 1))
end_date = st.sidebar.date_input("Fecha Fin", date(2026, 12, 31))

if st.sidebar.button("Descargar Reporte PDF"):
    pdf_content = api.get_pdf_report(start_date, end_date)
    st.sidebar.download_button(
        label="📥 Guardar PDF",
        data=pdf_content,
        file_name=f"reporte_{start_date}_{end_date}.pdf",
        mime="application/pdf"
    )

st.sidebar.divider()
st.sidebar.subheader("Importar Tareas (.txt)")
uploaded_file = st.sidebar.file_uploader("Formato: YYYY-MM-DD;Desc;Dur;Tags;Estado", type=["txt"])
if uploaded_file and st.sidebar.button("Importar"):
    res = api.import_tasks(uploaded_file.getvalue())
    st.sidebar.success(res.get("message", "Importado"))
    st.rerun()

# Pestañas principales
tab1, tab2 = st.tabs(["📋 Listado de Tareas", "➕ Nueva Tarea"])

with tab1:
    tasks = api.get_tasks(start_date, end_date)
    if tasks:
        df = pd.DataFrame(tasks)
        # Mostrar tabla bonita
        st.dataframe(df[["date", "description", "duration", "tags", "status"]], use_container_width=True)
        
        # Opción de eliminar (simple)
        task_to_del = st.selectbox("Seleccionar ID para eliminar", df["id"] if not df.empty else [])
        if st.button("Eliminar Tarea"):
            api.delete_task(task_to_del)
            st.success(f"Tarea {task_to_del} eliminada")
            st.rerun()
    else:
        st.info("No hay tareas registradas en este rango de fechas.")

with tab2:
    with st.form("new_task"):
        col1, col2 = st.columns(2)
        with col1:
            t_date = st.date_input("Fecha", date.today())
            t_duration = st.number_input("Duración (horas)", min_value=0.1, max_value=24.0, value=1.0)
        with col2:
            t_status = st.selectbox("Estado", ["pendiente", "en progreso", "completada"])
            t_tags = st.text_input("Etiquetas (sep. por comas)", "reunión, desarrollo")
        
        t_desc = st.text_area("Descripción de la tarea")
        
        if st.form_submit_button("Guardar Tarea"):
            new_task = {
                "date": str(t_date),
                "description": t_desc,
                "duration": t_duration,
                "tags": t_tags,
                "status": t_status
            }
            api.create_task(new_task)
            st.success("Tarea guardada correctamente")
            st.rerun()
