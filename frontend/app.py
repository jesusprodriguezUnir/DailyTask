import streamlit as st
import pandas as pd
from datetime import date, datetime, time, timedelta
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

st.sidebar.divider()
st.sidebar.subheader("Duplicar Tareas")
source_date_dup = st.sidebar.date_input("De (Origen)", date.today(), key="src_dup")
target_date_dup = st.sidebar.date_input("A (Destino)", date.today() + timedelta(days=1), key="tgt_dup")

if st.sidebar.button("🚀 Duplicar Tareas"):
    if source_date_dup == target_date_dup:
        st.sidebar.warning("La fecha de origen y destino deben ser diferentes.")
    else:
        res = api.duplicate_tasks(source_date_dup, target_date_dup)
        if "error" in res:
            st.sidebar.error(res["error"])
        else:
            st.sidebar.success(res.get("message", "Tareas duplicadas"))
            st.rerun()

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "📅 Calendario"

tab_options = ["📅 Calendario", "➕ Nueva Tarea"]
selected_tab = st.radio("Navegación", tab_options, index=tab_options.index(st.session_state.active_tab), horizontal=True, label_visibility="collapsed")

if selected_tab != st.session_state.active_tab:
    st.session_state.active_tab = selected_tab
    st.rerun()

if st.session_state.active_tab == "📅 Calendario":
    tasks = api.get_tasks(start_date, end_date)
    
    # Formatear eventos para el calendario (incluso si la lista está vacía)
    calendar_events = []
    if tasks:
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
        "weekends": False, # Ocultar sábados y domingos
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
                start_str = state["select"]["start"].replace("Z", "")
                end_str = state["select"]["end"].replace("Z", "")
                
                start_dt = datetime.fromisoformat(start_str)
                end_dt = datetime.fromisoformat(end_str)
                
                st.session_state.pre_selection = {
                    "date": start_dt.date(),
                    "start_time": start_dt.time(),
                    "end_time": end_dt.time(),
                    "description": "",
                    "category": "Sin Categoría",
                    "status": "pendiente",
                    "tags": "reunión",
                    "id": None # Es nueva
                }
                st.toast(f"📍 Bloque seleccionado: {start_dt.time().strftime('%H:%M')} - {end_dt.time().strftime('%H:%M')}.", icon="📌")
                st.session_state.active_tab = "➕ Nueva Tarea"
                st.rerun()
            except Exception as e:
                st.error(f"Error procesando selección: {e}")

        # Capturar click simple en una fecha/hora (para creación rápida)
        if state.get("dateClick"):
            try:
                date_str = state["dateClick"]["date"].replace("Z", "")
                dt = datetime.fromisoformat(date_str)
                st.session_state.pre_selection = {
                    "date": dt.date(),
                    "start_time": dt.time(),
                    "end_time": (dt + timedelta(hours=1)).time(),
                    "description": "",
                    "category": "Sin Categoría",
                    "status": "pendiente",
                    "tags": "reunión",
                    "id": None
                }
                st.toast(f"✨ Creando tarea para el {dt.date()} a las {dt.time().strftime('%H:%M')}")
                st.session_state.active_tab = "➕ Nueva Tarea"
                st.rerun()
            except Exception as e:
                st.error(f"Error en click: {e}")

        # Capturar movimiento de tarea (drag & drop)
        if state.get("eventDrop") or state.get("eventResize"):
            event_type = "eventDrop" if state.get("eventDrop") else "eventResize"
            dropped_event = state[event_type]["event"]
            try:
                new_start = datetime.fromisoformat(dropped_event["start"].replace("Z", ""))
                new_end = datetime.fromisoformat(dropped_event["end"].replace("Z", ""))
                duration = (new_end - new_start).seconds / 3600.0
                
                update_data = {
                    "date": str(new_start.date()),
                    "start_time": new_start.time().strftime("%H:%M"),
                    "end_time": new_end.time().strftime("%H:%M"),
                    "duration": round(duration, 2)
                }
                
                res = api.update_task(dropped_event["id"], update_data)
                if "error" not in res:
                    st.toast(f"✅ Tarea reprogramada: {new_start.date()} a las {new_start.time().strftime('%H:%M')}")
                    st.rerun()
                else:
                    st.error(f"Error al mover tarea: {res.get('error')}")
            except Exception as e:
                st.error(f"Error al procesar cambio de horario: {e}")

    with col_details:
        st.subheader("🔍 Detalle de Tarea")
        if state.get("eventClick"):
            event_data = state["eventClick"]["event"]
            props = event_data.get("extendedProps", {})
            
            # Al pulsar, pre-cargamos para edición y saltamos al formulario directamente
            try:
                start_dt = datetime.fromisoformat(event_data['start'].replace("Z", ""))
                end_dt = datetime.fromisoformat(event_data['end'].replace("Z", ""))
                st.session_state.pre_selection = {
                    "id": event_data['id'],
                    "date": start_dt.date(),
                    "start_time": start_dt.time(),
                    "end_time": end_dt.time(),
                    "description": props.get('description'),
                    "category": props.get('category'),
                    "status": props.get('status'),
                    "tags": props.get('tags')
                }
                st.session_state.active_tab = "➕ Nueva Tarea"
                st.rerun()
            except Exception as e:
                st.error(f"Error al cargar tarea: {e}")

            # (El código de abajo es de respaldo si no saltara)
            st.info(f"**ID:** {event_data['id']}")
            st.markdown(f"### {props.get('category', 'Sin Categoría')}")
            st.write(f"**Descripción:** {props.get('description')}")
            st.write(f"**Estado:** {props.get('status')}")
            st.write(f"**Etiquetas:** {props.get('tags')}")
            st.write(f"**Inicio:** {event_data['start']}")
            st.write(f"**Fin:** {event_data['end']}")
            
            # Botones de Acción
            c_act1, c_act2, c_act3 = st.columns(3)
            with c_act1:
                if st.button("✏️ Editar", use_container_width=True, key=f"edit_{event_data['id']}"):
                    # (La lógica de edición ya se dispara arriba al pulsar el evento, 
                    # pero dejamos esto como respaldo visual o manual)
                    st.session_state.active_tab = "➕ Nueva Tarea"
                    st.rerun()
            with c_act2:
                if st.button("👥 Copiar", use_container_width=True, help="Usa estos datos para una nueva tarea", key=f"copy_{event_data['id']}"):
                    start_dt = datetime.fromisoformat(event_data['start'].replace("Z", ""))
                    end_dt = datetime.fromisoformat(event_data['end'].replace("Z", ""))
                    st.session_state.pre_selection = {
                        "id": None, # Importante: ID a None para que sea nueva
                        "date": start_dt.date(),
                        "start_time": start_dt.time(),
                        "end_time": end_dt.time(),
                        "description": props.get('description'),
                        "category": props.get('category'),
                        "status": props.get('status'),
                        "tags": props.get('tags')
                    }
                    st.toast("📋 Datos copiados. ¡Listo para guardar como nueva!", icon="✨")
                    st.session_state.active_tab = "➕ Nueva Tarea"
                    st.rerun()
            with c_act3:
                if st.button("🗑️ Eliminar", use_container_width=True, key=f"del_{event_data['id']}"):
                    api.delete_task(event_data['id'])
                    st.toast("Tarea eliminada")
                    st.rerun()
            
            # Widget de Replicación Rápida mejorado
            st.divider()
            st.markdown("### 🚀 Replicación Rápida")
            with st.container(border=True):
                st.info("Crea copias de esta tarea en otros días.")
                # Usamos multiselect de fechas si es posible, o simplemente permitimos varias una a una
                target_dates = st.date_input(
                    "Selecciona las fechas destino", 
                    value=[], 
                    key=f"rep_dates_{event_data['id']}",
                    help="Puedes seleccionar varios días si tu navegador lo permite"
                )
                
                if st.button("✨ Replicar en Fechas Seleccionadas", use_container_width=True, type="primary", key=f"btn_rep_{event_data['id']}"):
                    if not target_dates:
                        st.warning("Selecciona al menos una fecha.")
                    else:
                        # Si es una sola fecha (date), la metemos en lista. Si es lista/tupla, la usamos.
                        dates_to_proc = target_dates if isinstance(target_dates, (list, tuple)) else [target_dates]
                        success_count = 0
                        for d in dates_to_proc:
                            res = api.duplicate_single_task(event_data['id'], d)
                            if "error" not in res:
                                success_count += 1
                        
                        if success_count > 0:
                            st.success(f"¡Tarea replicada en {success_count} fecha(s)!")
                            st.rerun()
                        else:
                            st.error("No se pudo replicar la tarea.")
        else:
            st.write("Selecciona una tarea o arrastra en el calendario para crear una.")
    
    if tasks:
        st.divider()
        st.subheader("📊 Vista de Tabla")
        df = pd.DataFrame(tasks)
        available_cols = df.columns.tolist()
        desired_cols = ["id", "date", "category", "start_time", "end_time", "duration", "description", "status"]
        cols_to_show = [c for c in desired_cols if c in available_cols]
        st.dataframe(df[cols_to_show], width="stretch")

if st.session_state.active_tab == "➕ Nueva Tarea":
    pre = st.session_state.pre_selection
    is_editing = pre is not None and pre.get("id") is not None
    
    if is_editing:
        st.subheader(f"✏️ Editar Tarea (ID: {pre['id']})")
    else:
        st.subheader("📝 Registrar Nueva Tarea")
    
    if pre:
        msg = f"📍 Usando datos del calendario: **{pre['date']}**"
        if pre.get("start_time"):
            msg += f" de **{pre['start_time'].strftime('%H:%M')}** a **{pre['end_time'].strftime('%H:%M')}**"
        st.info(msg)
        if st.button("Limpiar datos del calendario"):
            st.session_state.pre_selection = None
            st.rerun()

    with st.form("task_form", clear_on_submit=not is_editing):
        col1, col2, col3 = st.columns(3)
        with col1:
            default_date = pre["date"] if pre else date.today()
            t_date = st.date_input("Fecha", default_date)
            
            # Ajuste de categoría por defecto
            default_cat = pre.get("category", "Sin Categoría") if pre else "Sin Categoría"
            if default_cat not in CATEGORIES: default_cat = "Sin Categoría"
            t_category = st.selectbox("Categoría", CATEGORIES, index=CATEGORIES.index(default_cat))
            
        with col2:
            default_start = pre["start_time"] if pre and pre.get("start_time") else time(9, 0)
            default_end = pre["end_time"] if pre and pre.get("end_time") else time(10, 0)
            t_start = st.time_input("Hora Inicio", default_start)
            t_end = st.time_input("Hora Fin", default_end)
            
        with col3:
            default_status = pre.get("status", "pendiente") if pre else "pendiente"
            if default_status not in ["pendiente", "en progreso", "completada"]: default_status = "pendiente"
            t_status = st.selectbox("Estado", ["pendiente", "en progreso", "completada"], index=["pendiente", "en progreso", "completada"].index(default_status))
            
            default_tags = pre.get("tags", "reunión") if pre else "reunión"
            t_tags = st.text_input("Etiquetas", default_tags)
        
        t_desc = st.text_area("Descripción de la tarea", value=pre.get("description", "") if pre else "")

        # Funcionalidad periódica (Solo para tareas nuevas)
        repeat_week = False
        if not is_editing:
            repeat_week = st.checkbox("🔁 Repetir esta misma tarea de Lunes a Viernes", help="Creará la tarea para todos los días laborables de la semana seleccionada")
        
        btn_label = "💾 Actualizar Tarea" if is_editing else "💾 Guardar Tarea"
        
        c_btn1, c_btn2 = st.columns(2) if is_editing else (st.container(), None)
        
        with c_btn1:
            submit = st.form_submit_button(btn_label, use_container_width=True, type="primary")
        
        if is_editing:
            with c_btn2:
                delete_btn = st.form_submit_button("🗑️ Eliminar Tarea", use_container_width=True)
                if delete_btn:
                    api.delete_task(pre["id"])
                    st.toast("✅ Tarea eliminada")
                    st.session_state.pre_selection = None
                    st.session_state.active_tab = "📅 Calendario"
                    st.rerun()

    # Formulario de replicación dedicado dentro de la edición
    if is_editing:
        st.divider()
        st.subheader("🚀 Replicar esta tarea a otros días")
        with st.container(border=True):
            col_rep1, col_rep2 = st.columns([2, 1])
            with col_rep1:
                rep_dates_form = st.date_input(
                    "¿A qué otros días quieres copiar esta tarea?", 
                    value=[], 
                    key="rep_dates_form"
                )
            with col_rep2:
                st.write("") # Espaciado
                st.write("") 
                if st.button("🚀 Replicar Ahora", use_container_width=True):
                    if not rep_dates_form:
                        st.warning("Selecciona al menos una fecha")
                    else:
                        dates_to_proc = rep_dates_form if isinstance(rep_dates_form, (list, tuple)) else [rep_dates_form]
                        count = 0
                        for d in dates_to_proc:
                            res = api.duplicate_single_task(pre["id"], d)
                            if "error" not in res:
                                count += 1
                        st.success(f"✅ Tarea replicada en {count} fecha(s)")
                        st.rerun()

        if submit:
            if not t_desc:
                st.error("La descripción es obligatoria")
            else:
                # Calcular duración
                start_dt = datetime.combine(date.today(), t_start)
                end_dt = datetime.combine(date.today(), t_end)
                duration = (end_dt - start_dt).seconds / 3600.0
                
                task_data = {
                    "date": str(t_date),
                    "description": t_desc,
                    "start_time": t_start.strftime("%H:%M"),
                    "end_time": t_end.strftime("%H:%M"),
                    "duration": round(duration, 2),
                    "category": t_category if t_category != "Sin Categoría" else None,
                    "tags": t_tags,
                    "status": t_status
                }
                
                if is_editing:
                    res = api.update_task(pre["id"], task_data)
                    verbo = "actualizada"
                elif repeat_week:
                    # Lógica para repetir toda la semana laborable
                    # Buscamos el lunes de la semana de la fecha seleccionada
                    start_of_week = t_date - timedelta(days=t_date.weekday())
                    created_count = 0
                    for i in range(5): # De lunes (0) a viernes (4)
                        current_date = start_of_week + timedelta(days=i)
                        periodic_task = task_data.copy()
                        periodic_task["date"] = str(current_date)
                        api.create_task(periodic_task)
                        created_count += 1
                    res = {"message": f"Creadas {created_count} tareas"}
                    verbo = "creada periódicamente"
                else:
                    res = api.create_task(task_data)
                    verbo = "guardada"

                if "error" not in res:
                    st.success(f"✅ Tarea {verbo} correctamente")
                    st.session_state.pre_selection = None
                    st.session_state.active_tab = "📅 Calendario"
                    st.rerun()
                else:
                    st.error(f"❌ Error: {res.get('error')}")
