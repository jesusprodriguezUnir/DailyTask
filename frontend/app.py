import streamlit as st
import pandas as pd
from datetime import date, datetime, time
from streamlit_calendar import calendar
from utils.api_client import APIClient

st.set_page_config(page_title="DailyTask 2026", layout="wide")

api = APIClient()

# Inicializar estado para pre-selección desde el calendario
if "pre_selection" not in st.session_state:
    st.session_state.pre_selection = None

CATEGORY_COLORS = {
    "Sin Categoría": "#9E9E9E",      # Gris
    "Reunion Desarrollo": "#2196F3", # Azul
    "Reunion con Pablo": "#9C27B0",  # Morado
    "Reunion con Cesar": "#673AB7",  # Indigo
    "Reunion con Cliente": "#FF9800",# Naranja
    "Daily": "#4CAF50",              # Verde
    "Planning": "#E91E63"            # Rosa
}

CATEGORIES = list(CATEGORY_COLORS.keys())

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

# Botón para descargar plantilla
if st.sidebar.button("Descargar Plantilla TXT"):
    template = api.download_template()
    st.sidebar.download_button(
        label="📄 Bajar Plantilla",
        data=template,
        file_name="plantilla_tareas.txt",
        mime="text/plain"
    )

uploaded_file = st.sidebar.file_uploader("Subir archivo de tareas", type=["txt"])
if uploaded_file and st.sidebar.button("Importar"):
    res = api.import_tasks(uploaded_file.getvalue())
    st.sidebar.success(res.get("message", "Importado"))
    st.rerun()

# Pestañas principales
tab1, tab2 = st.tabs(["� Calendario de Tareas", "➕ Nueva Tarea"])

with tab1:
    tasks = api.get_tasks(start_date, end_date)
    
    if tasks:
        # Formatear eventos para el calendario
        calendar_events = []
        for task in tasks:
            start_dt = f"{task['date']}T{task.get('start_time', '09:00')}:00"
            end_dt = f"{task['date']}T{task.get('end_time', '10:00')}:00"
            
            calendar_events.append({
                "id": str(task["id"]),
                "title": f"[{task.get('category', 'Tarea')}] {task['description'][:20]}...",
                "start": start_dt,
                "end": end_dt,
                "color": CATEGORY_COLORS.get(task.get('category', 'Sin Categoría'), "#9E9E9E"),
                "extendedProps": {
                    "description": task["description"],
                    "category": task.get("category", "N/A"),
                    "status": task["status"],
                    "tags": task["tags"]
                }
            })

        calendar_options = {
            "editable": True,
            "selectable": True,
            "selectMirror": True,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timeGridWeek,timeGridDay,dayGridMonth",
            },
            "initialView": "timeGridWeek",
            "slotMinTime": "07:00:00",
            "slotMaxTime": "21:00:00",
            "firstDay": 1, # Lunes
            "locale": "es",
            "allDaySlot": False
        }

        col_cal, col_details = st.columns([3, 1])

        with col_cal:
            state = calendar(
                events=calendar_events,
                options=calendar_options,
                key="daily_calendar",
            )
            
            # Capturar selección de rango (click y arrastrar)
            if state.get("select"):
                try:
                    # El formato suele ser 2026-01-08T09:00:00Z o similar
                    start_str = state["select"]["start"].replace("Z", "")
                    end_str = state["select"]["end"].replace("Z", "")
                    
                    start_dt = datetime.fromisoformat(start_str)
                    end_dt = datetime.fromisoformat(end_str)
                    
                    st.session_state.pre_selection = {
                        "date": start_dt.date(),
                        "start_time": start_dt.time(),
                        "end_time": end_dt.time()
                    }
                    st.toast(f"📍 Horario seleccionado: {start_dt.time().strftime('%H:%M')} - {end_dt.time().strftime('%H:%M')}. ¡Ve a 'Nueva Tarea'!", icon="📌")
                except Exception as e:
                    st.error(f"Error procesando selección: {e}")

        with col_details:
            st.subheader("🔍 Detalle de Tarea")
            if state.get("eventClick"):
                event_data = state["eventClick"]["event"]
                props = event_data.get("extendedProps", {})
                
                st.info(f"**ID:** {event_data['id']}")
                st.markdown(f"### {props.get('category', 'Sin Categoría')}")
                st.write(f"**Descripción:** {props.get('description')}")
                st.write(f"**Estado:** {props.get('status')}")
                st.write(f"**Etiquetas:** {props.get('tags')}")
                st.write(f"**Inicio:** {event_data['start']}")
                st.write(f"**Fin:** {event_data['end']}")
                
                if st.button("🗑️ Eliminar esta tarea"):
                    api.delete_task(event_data['id'])
                    st.toast("Tarea eliminada")
                    st.rerun()
            else:
                st.write("Haz clic en una tarea del calendario para ver sus detalles.")
        
        st.divider()
        st.subheader("📊 Vista de Tabla")
        df = pd.DataFrame(tasks)
        available_cols = df.columns.tolist()
        desired_cols = ["id", "date", "category", "start_time", "end_time", "duration", "description", "status"]
        cols_to_show = [c for c in desired_cols if c in available_cols]
        st.dataframe(df[cols_to_show], width="stretch")
    else:
        st.info("No hay tareas registradas en este rango de fechas.")

with tab2:
    st.subheader("📝 Registrar Nueva Tarea")
    
    # Valores por defecto (normales o desde selección de calendario)
    pre = st.session_state.pre_selection
    
    if pre:
        st.info(f"✨ Usando horario seleccionado en calendario: **{pre['date']}** de **{pre['start_time'].strftime('%H:%M')}** a **{pre['end_time'].strftime('%H:%M')}**")
        if st.button("Limpiar selección del calendario"):
            st.session_state.pre_selection = None
            st.rerun()

    with st.form("new_task", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            default_date = pre["date"] if pre else date.today()
            t_date = st.date_input("Fecha", default_date)
            t_category = st.selectbox("Categoría", CATEGORIES)
        with col2:
            from datetime import datetime, time
            default_start = pre["start_time"] if pre else time(9, 0)
            default_end = pre["end_time"] if pre else time(10, 0)
            t_start = st.time_input("Hora Inicio", default_start)
            t_end = st.time_input("Hora Fin", default_end)
        with col3:
            t_status = st.selectbox("Estado", ["pendiente", "en progreso", "completada"])
            t_tags = st.text_input("Etiquetas", "reunión")
        
        t_desc = st.text_area("Descripción de la tarea")
        
        submit = st.form_submit_button("💾 Guardar Tarea", use_container_width=True)
        
        if submit:
            if not t_desc:
                st.error("La descripción es obligatoria")
            else:
                # Calcular duración
                start_dt = datetime.combine(date.today(), t_start)
                end_dt = datetime.combine(date.today(), t_end)
                duration = (end_dt - start_dt).seconds / 3600.0
                
                new_task = {
                    "date": str(t_date),
                    "description": t_desc,
                    "start_time": t_start.strftime("%H:%M"),
                    "end_time": t_end.strftime("%H:%M"),
                    "duration": round(duration, 2),
                    "category": t_category if t_category != "Sin Categoría" else None,
                    "tags": t_tags,
                    "status": t_status
                }
                res = api.create_task(new_task)
                if "error" not in res:
                    st.success(f"✅ Tarea guardada correctamente (ID: {res.get('id')})")
                    # Limpiar pre-selección tras guardar con éxito
                    st.session_state.pre_selection = None
                    # No hacemos rerun inmediato para que el usuario vea el mensaje
                else:
                    st.error(f"❌ Error al guardar: {res.get('error')}")
