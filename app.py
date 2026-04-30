import streamlit as st
import requests
import json
import os

load_dotenv()

st.set_page_config(page_title="PromptForge AI · ITJOLI", page_icon="⚡", layout="centered")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def call_ai(prompt: str) -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
        json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1000}
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

def init_state():
    defaults = {"step": 1, "profession": "", "exercise": "", "level": 1,
                "scores": [], "history": [], "done": 0, "feedback": None,
                "rewrite": None, "show_rewrite": False}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background-color:#0F0F1A!important;color:#E8EEFF!important}
.stApp{background:linear-gradient(135deg,#0F0F1A 0%,#1A1030 50%,#0F1A20 100%)!important}
.block-container{padding-top:1rem!important;max-width:820px!important}
#MainMenu,footer,header{visibility:hidden}
.stDeployButton{display:none}
.pf-hdr{background:linear-gradient(135deg,#1E1040,#0D2040);border:1px solid rgba(100,80,255,0.3);border-radius:20px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;display:flex;align-items:center;gap:16px}
.pf-ring{width:52px;height:52px;background:linear-gradient(135deg,#4050FF,#00D4FF);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;box-shadow:0 0 20px rgba(64,80,255,0.5);flex-shrink:0}
.pf-title{font-size:22px;font-weight:800;color:#FFF;margin:0;letter-spacing:-0.5px}
.pf-title span{color:#00D4FF}
.pf-sub{font-size:12px;color:rgba(200,210,255,0.5);margin:2px 0 0}
.pf-badge{margin-left:auto;background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);color:#00D4FF;font-size:11px;font-weight:600;padding:4px 12px;border-radius:20px;white-space:nowrap}
.steps-wrap{display:flex;align-items:center;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:12px 16px;margin-bottom:1.5rem}
.sp{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:500;padding:6px 14px;border-radius:12px;color:rgba(200,210,255,0.4)}
.sp.active{background:linear-gradient(135deg,rgba(64,80,255,0.2),rgba(0,212,255,0.15));border:1px solid rgba(0,212,255,0.3);color:#00D4FF;font-weight:700}
.sp.done{color:#00FF9D}
.sn{width:22px;height:22px;border-radius:50%;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}
.sp.active .sn{background:linear-gradient(135deg,#4050FF,#00D4FF);color:white;box-shadow:0 0 10px rgba(0,212,255,0.4)}
.sp.done .sn{background:#00FF9D;color:#0F1A20}
.sl{flex:1;height:1px;background:rgba(255,255,255,0.08);min-width:8px}
.lbl{font-size:10px;font-weight:700;color:rgba(200,210,255,0.4);letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;margin-top:4px}
.gc{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);border-radius:18px;padding:1.4rem;margin-bottom:1rem}
.lv1{background:rgba(64,80,255,0.15);color:#818CF8;border:1px solid rgba(64,80,255,0.3);display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;padding:4px 14px;border-radius:20px;margin-bottom:1rem}
.lv2{background:rgba(251,146,60,0.15);color:#FB923C;border:1px solid rgba(251,146,60,0.3);display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;padding:4px 14px;border-radius:20px;margin-bottom:1rem}
.lv3{background:rgba(239,68,68,0.15);color:#F87171;border:1px solid rgba(239,68,68,0.3);display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:700;padding:4px 14px;border-radius:20px;margin-bottom:1rem}
.exbox{background:linear-gradient(135deg,rgba(64,80,255,0.08),rgba(0,212,255,0.05));border:1px solid rgba(0,212,255,0.2);border-radius:14px;padding:1.2rem;font-size:15px;line-height:1.75;color:#E8EEFF;margin-bottom:1rem}
.sc-card{background:linear-gradient(135deg,rgba(0,255,157,0.06),rgba(0,212,255,0.06));border:1px solid rgba(0,255,157,0.2);border-radius:16px;padding:1.2rem 1.5rem;display:flex;align-items:center;gap:1.2rem;margin-bottom:1rem}
.sc-big{font-size:56px;font-weight:800;line-height:1}
.sg{color:#00FF9D;text-shadow:0 0 20px rgba(0,255,157,0.4)}
.sy{color:#FB923C;text-shadow:0 0 20px rgba(251,146,60,0.4)}
.sr{color:#F87171;text-shadow:0 0 20px rgba(248,113,113,0.4)}
.sc-title{font-size:17px;font-weight:700;color:#FFF;margin-bottom:4px}
.sc-desc{font-size:13px;color:rgba(200,210,255,0.6);line-height:1.5}
.fb-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:1rem}
.fb-box{padding:14px;border-radius:14px}
.fbi{background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.25);border-top:3px solid #F87171}
.fbw{background:rgba(251,146,60,0.08);border:1px solid rgba(251,146,60,0.25);border-top:3px solid #FB923C}
.fbg{background:rgba(0,255,157,0.06);border:1px solid rgba(0,255,157,0.2);border-top:3px solid #00FF9D}
.fb-lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;margin-bottom:7px}
.fbi .fb-lbl{color:#F87171}.fbw .fb-lbl{color:#FB923C}.fbg .fb-lbl{color:#00FF9D}
.fb-box p{font-size:13px;line-height:1.55;color:rgba(220,230,255,0.85);margin:0}
.rw-wrap{background:rgba(128,0,255,0.06);border:1px solid rgba(128,0,255,0.25);border-radius:16px;overflow:hidden;margin-top:1rem}
.rw-hdr{background:rgba(128,0,255,0.12);padding:10px 16px;font-size:12px;font-weight:700;color:#C084FC;letter-spacing:1px;text-transform:uppercase}
.rw-grid{display:grid;grid-template-columns:1fr 1fr}
.rw-p{padding:14px}
.rw-p:first-child{border-right:1px solid rgba(128,0,255,0.2)}
.rw-lbl{font-size:11px;font-weight:600;color:rgba(200,210,255,0.4);margin-bottom:8px;display:flex;align-items:center;gap:6px}
.rw-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.rw-p p{font-family:monospace;font-size:12px;line-height:1.7;color:rgba(220,230,255,0.85);margin:0}
.st-row{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1.2rem}
.st-box{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:14px;text-align:center}
.st-big{font-size:26px;font-weight:800;line-height:1.1}
.st-sm{font-size:11px;color:rgba(200,210,255,0.4);margin-top:3px;font-weight:500}
.hi{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.05)}
.hl{font-size:12px;color:rgba(200,210,255,0.5);width:150px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hb{flex:1;height:6px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden}
.hf{height:100%;border-radius:3px;background:linear-gradient(90deg,#4050FF,#00D4FF)}
.hs{font-size:12px;font-weight:700;color:#00D4FF;width:32px;text-align:right}
.tip-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1rem}
.ti{display:flex;gap:10px;align-items:flex-start;margin-bottom:10px}
.tn{width:22px;height:22px;border-radius:50%;background:linear-gradient(135deg,#4050FF,#00D4FF);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;flex-shrink:0}
.tt{font-size:13px;font-weight:600;color:#E8EEFF;margin-bottom:2px}
.td{font-size:12px;color:rgba(200,210,255,0.5);line-height:1.5}
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:12px!important;color:#E8EEFF!important;font-size:14px!important}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus{border-color:rgba(0,212,255,0.5)!important;box-shadow:0 0 0 2px rgba(0,212,255,0.1)!important}
div[data-testid="stTextInput"] label,div[data-testid="stTextArea"] label{color:rgba(200,210,255,0.5)!important;font-size:12px!important}
.stButton>button{border-radius:12px!important;font-weight:600!important;font-size:13px!important;transition:all 0.2s!important}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#4050FF,#00D4FF)!important;border:none!important;color:white!important;box-shadow:0 4px 15px rgba(64,80,255,0.35)!important}
.stButton>button[kind="secondary"]{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.12)!important;color:rgba(200,210,255,0.8)!important}
.stButton>button[kind="secondary"]:hover{border-color:rgba(0,212,255,0.3)!important;color:#00D4FF!important}
.stDownloadButton>button{background:rgba(0,255,157,0.08)!important;border:1px solid rgba(0,255,157,0.3)!important;color:#00FF9D!important;border-radius:12px!important;font-weight:600!important}
div[data-testid="stAlert"]{background:rgba(64,80,255,0.08)!important;border:1px solid rgba(64,80,255,0.25)!important;border-radius:12px!important;color:rgba(200,210,255,0.85)!important}
.stSpinner>div{border-top-color:#00D4FF!important}
div[data-testid="stMarkdownContainer"] p{color:rgba(200,210,255,0.7);font-size:13px}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="pf-hdr">
  <div class="pf-ring">⚡</div>
  <div>
    <p class="pf-title">Prompt<span>Forge</span> AI</p>
    <p class="pf-sub">ITJOLI · Intelligence & AI Group · Powered by Groq + Llama 3.3</p>
  </div>
  <div class="pf-badge">🎓 Clase de IA</div>
</div>
""", unsafe_allow_html=True)

# STEPS
def render_steps():
    s = st.session_state.step
    items = [("🎯","Profesión"),("📝","Ejercicio"),("⭐","Evaluación"),("📊","Progreso")]
    html = '<div class="steps-wrap">'
    for i,(icon,label) in enumerate(items,1):
        cls = "sp done" if i<s else ("sp active" if i==s else "sp")
        num = "✓" if i<s else str(i)
        html += f'<div class="{cls}"><div class="sn">{num}</div>{icon} {label}</div>'
        if i<4: html += '<div class="sl"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

render_steps()

# ── PASO 1 ────────────────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown('<div class="lbl">¿en qué área trabajas?</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    chips = [("📣","Marketing Digital"),("🏥","Salud y Medicina"),("💼","Administración"),
             ("📚","Educación"),("👥","Recursos Humanos"),("💻","Tecnología")]
    for i,(icon,label) in enumerate(chips):
        col = [c1,c2,c3][i%3]
        with col:
            if st.button(f"{icon} {label}", key=f"c{i}", use_container_width=True):
                st.session_state.profession = label
                st.rerun()

    profession = st.text_input("✏️ O escribe tu profesión:", value=st.session_state.profession,
                                placeholder="Ej: Diseñador UX, Contador, Abogado, Chef...")
    st.session_state.profession = profession
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Comenzar mi entrenamiento", type="primary", use_container_width=True):
        if not profession.strip():
            st.warning("⚠️ Por favor ingresa tu profesión primero.")
        else:
            st.session_state.step = 2
            st.session_state.exercise = ""
            st.session_state.feedback = None
            st.session_state.rewrite = None
            st.session_state.show_rewrite = False
            st.rerun()

    st.markdown("""
    <br>
    <div class="tip-card">
      <div class="lbl" style="margin-bottom:12px;">💡 ¿por qué aprender prompt engineering?</div>
      <div class="ti"><div class="tn">1</div><div><div class="tt">Habilidad #1 emergente</div><div class="td">WEF 2025 y Forrester 2026: la skill más demandada.</div></div></div>
      <div class="ti"><div class="tn">2</div><div><div class="tt">Ejercicios de tu trabajo real</div><div class="td">La IA genera situaciones de tu profesión específica.</div></div></div>
      <div class="ti"><div class="tn">3</div><div><div class="tt">Sube de nivel automáticamente</div><div class="td">Básico → Intermedio → Avanzado según tu progreso.</div></div></div>
    </div>
    """, unsafe_allow_html=True)

# ── PASO 2 + 3 ────────────────────────────────────────────────────────────────
elif st.session_state.step in [2, 3]:
    level = st.session_state.level
    lv_labels = {1:"⚡ Nivel Básico", 2:"🔥 Nivel Intermedio", 3:"💎 Nivel Avanzado"}
    lv_cls    = {1:"lv1", 2:"lv2", 3:"lv3"}
    lv_desc   = {1:"básico (simple y directo)",
                 2:"intermedio (con contexto y restricciones específicas)",
                 3:"avanzado (complejo, multi-paso)"}

    if not st.session_state.exercise:
        with st.spinner("✨ Generando tu ejercicio personalizado..."):
            try:
                ex = call_ai(
                    f"Genera UN ejercicio de prompt engineering de nivel {lv_desc[level]} "
                    f"para alguien que trabaja en: {st.session_state.profession}. "
                    f"Situación REAL de su trabajo. Máximo 3-4 oraciones. "
                    f"Solo el texto del ejercicio, sin títulos ni numeración."
                )
                st.session_state.exercise = ex
            except Exception as e:
                st.error(f"❌ Error al conectar: {e}")
                st.stop()

    col_ex, col_tips = st.columns([3, 2])

    with col_ex:
        st.markdown(f'<div class="{lv_cls[level]}">{lv_labels[level]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="lbl">📋 tu ejercicio</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exbox">{st.session_state.exercise}</div>', unsafe_allow_html=True)
        st.markdown('<div class="lbl">✍️ escribe tu prompt</div>', unsafe_allow_html=True)
        user_prompt = st.text_area(
            label="prompt", label_visibility="collapsed",
            placeholder="Escribe aquí tu prompt...\n\nTip: sé específico, da contexto, define el tono y el formato.",
            height=140, key="prompt_input"
        )
        chars = len(user_prompt)
        st.caption(f"{'🟢' if chars>30 else '🔴'} {chars} caracteres {'· ¡Listo!' if chars>=10 else '· Mínimo 10 caracteres'}")

        ca, cb = st.columns(2)
        with ca:
            eval_clicked = st.button("⭐ Evaluar prompt", type="primary",
                                      use_container_width=True, disabled=chars < 10)
        with cb:
            if st.button("🔄 Nuevo ejercicio", use_container_width=True):
                st.session_state.exercise = ""
                st.session_state.feedback = None
                st.session_state.rewrite = None
                st.session_state.show_rewrite = False
                st.session_state.step = 2
                st.rerun()

    with col_tips:
        st.markdown("""
        <div class="tip-card">
          <div class="lbl" style="margin-bottom:10px;">🎯 tips para un buen prompt</div>
          <div class="ti"><div class="tn">1</div><div><div class="tt">Sé específico</div><div class="td">Define exactamente qué quieres.</div></div></div>
          <div class="ti"><div class="tn">2</div><div><div class="tt">Da contexto</div><div class="td">Explica quién eres y para qué.</div></div></div>
          <div class="ti"><div class="tn">3</div><div><div class="tt">Define el tono</div><div class="td">Formal, técnico, simple...</div></div></div>
          <div class="ti"><div class="tn">4</div><div><div class="tt">Pide formato</div><div class="td">Lista, tabla, párrafo, pasos...</div></div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        done = st.session_state.done
        scores = st.session_state.scores
        avg = round(sum(scores)/len(scores)) if scores else 0
        st.markdown(f"""
        <div class="gc" style="padding:1rem;">
          <div class="lbl" style="margin-bottom:8px;">📊 sesión actual</div>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;">
            <div><div style="font-size:22px;font-weight:800;color:#00D4FF">{done}</div><div style="font-size:11px;color:rgba(200,210,255,0.4)">Hechos</div></div>
            <div><div style="font-size:22px;font-weight:800;color:#00FF9D">{avg if scores else '—'}</div><div style="font-size:11px;color:rgba(200,210,255,0.4)">Promedio</div></div>
            <div><div style="font-size:22px;font-weight:800;color:#FB923C">{level}</div><div style="font-size:11px;color:rgba(200,210,255,0.4)">Nivel</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if eval_clicked and chars >= 10:
        with st.spinner("🤖 Analizando tu prompt..."):
            try:
                raw = call_ai(
                    f"Eres evaluador experto en prompt engineering. "
                    f'Ejercicio: "{st.session_state.exercise}" | '
                    f"Profesión: {st.session_state.profession} | "
                    f'Prompt del usuario: "{user_prompt}" | '
                    f'Responde SOLO con JSON sin markdown: '
                    f'{{"score":75,"title":"Título","description":"Una oración","improve":"Qué mejorar","suggest":"Sugerencia","good":"Qué hizo bien"}}'
                )
                result = json.loads(raw.replace("```json","").replace("```","").strip())
                st.session_state.feedback = result
                st.session_state.show_rewrite = False
                st.session_state.rewrite = None
                score = min(100, max(0, result["score"]))
                st.session_state.scores.append(score)
                st.session_state.done += 1
                st.session_state.history.append({"ex": st.session_state.exercise[:60]+"...", "score": score})
                if len(st.session_state.scores) >= 2:
                    avg2 = sum(st.session_state.scores[-2:]) / 2
                    if avg2 >= 75 and level < 3:
                        st.session_state.level += 1
                        st.balloons()
                    elif avg2 < 40 and level > 1:
                        st.session_state.level -= 1
                st.session_state.step = 3
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error al evaluar: {e}")

    if st.session_state.feedback:
        fb = st.session_state.feedback
        score = min(100, max(0, fb["score"]))
        sc = "sg" if score>=75 else "sy" if score>=50 else "sr"
        em = "🏆" if score>=75 else "📈" if score>=50 else "💪"
        st.markdown("---")
        st.markdown(f"""
        <div class="sc-card">
          <div class="sc-big {sc}">{score}</div>
          <div>
            <div class="sc-title">{em} {fb.get('title','')}</div>
            <div class="sc-desc">{fb.get('description','')}</div>
          </div>
        </div>
        <div class="fb-row">
          <div class="fb-box fbi"><div class="fb-lbl">⚠ Qué mejorar</div><p>{fb.get('improve','—')}</p></div>
          <div class="fb-box fbw"><div class="fb-lbl">💡 Sugerencia</div><p>{fb.get('suggest','—')}</p></div>
          <div class="fb-box fbg"><div class="fb-lbl">✅ Lo que hiciste bien</div><p>{fb.get('good','—')}</p></div>
        </div>
        """, unsafe_allow_html=True)

        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("✨ Reescribir con IA", use_container_width=True):
                with st.spinner("🪄 Mejorando tu prompt..."):
                    try:
                        rw = call_ai(
                            f"Eres experto en prompt engineering. "
                            f"Profesión: {st.session_state.profession} | "
                            f'Ejercicio: "{st.session_state.exercise}" | '
                            f'Prompt original: "{user_prompt}" | '
                            f"Reescribe mejorando: especificidad, contexto, tono y formato. "
                            f"Responde SOLO con el prompt mejorado."
                        )
                        st.session_state.rewrite = rw.strip()
                        st.session_state.show_rewrite = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
        with c2:
            if st.button("➡️ Siguiente ejercicio", use_container_width=True):
                st.session_state.exercise = ""
                st.session_state.feedback = None
                st.session_state.rewrite = None
                st.session_state.show_rewrite = False
                st.session_state.step = 2
                st.rerun()
        with c3:
            if st.button("📊 Ver mi progreso", use_container_width=True):
                st.session_state.step = 4
                st.rerun()

        if st.session_state.show_rewrite and st.session_state.rewrite:
            st.markdown(f"""
            <div class="rw-wrap">
              <div class="rw-hdr">✨ Versión mejorada por IA</div>
              <div class="rw-grid">
                <div class="rw-p">
                  <div class="rw-lbl"><span class="rw-dot" style="background:#F87171"></span>Tu prompt original</div>
                  <p>{user_prompt}</p>
                </div>
                <div class="rw-p">
                  <div class="rw-lbl"><span class="rw-dot" style="background:#00FF9D"></span>Versión mejorada</div>
                  <p>{st.session_state.rewrite}</p>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.code(st.session_state.rewrite, language=None)

# ── PASO 4 ────────────────────────────────────────────────────────────────────
elif st.session_state.step == 4:
    scores = st.session_state.scores
    done = st.session_state.done
    avg = round(sum(scores)/len(scores)) if scores else 0
    best = max(scores) if scores else 0
    level = st.session_state.level

    st.markdown(f"""
    <div class="lbl">📊 resumen de tu sesión</div>
    <div class="st-row">
      <div class="st-box"><div class="st-big" style="color:#00D4FF">{done}</div><div class="st-sm">Ejercicios</div></div>
      <div class="st-box"><div class="st-big" style="color:#00FF9D">{avg if scores else '—'}</div><div class="st-sm">Promedio</div></div>
      <div class="st-box"><div class="st-big" style="color:#FB923C">{best if scores else '—'}</div><div class="st-sm">Mejor puntaje</div></div>
      <div class="st-box"><div class="st-big" style="color:#C084FC">{level}</div><div class="st-sm">Nivel actual</div></div>
    </div>
    <div class="lbl" style="margin-top:8px;">🕐 historial</div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        for h in reversed(st.session_state.history):
            p = h["score"]
            c = "#00FF9D" if p>=75 else "#FB923C" if p>=50 else "#F87171"
            st.markdown(f"""
            <div class="hi">
              <div class="hl" title="{h['ex']}">{h['ex']}</div>
              <div class="hb"><div class="hf" style="width:{p}%;background:linear-gradient(90deg,#4050FF,{c})"></div></div>
              <div class="hs" style="color:{c}">{p}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎯 Completa tu primer ejercicio para ver el historial aquí.")

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.download_button(
            label="⬇️ Exportar JSON",
            data=json.dumps({"profesion":st.session_state.profession,"ejercicios_completados":done,
                              "puntaje_promedio":avg,"mejor_puntaje":best,"nivel_alcanzado":level,
                              "historial":st.session_state.history}, indent=2, ensure_ascii=False),
            file_name="promptforge_progreso.json", mime="application/json", use_container_width=True
        )
    with c2:
        if st.button("🗑️ Limpiar historial", use_container_width=True):
            for k in ["scores","history"]: st.session_state[k] = []
            st.session_state.done = 0
            st.session_state.level = 1
            st.session_state.feedback = None
            st.session_state.rewrite = None
            st.rerun()
    with c3:
        if st.button("🚀 Seguir practicando", type="primary", use_container_width=True):
            st.session_state.exercise = ""
            st.session_state.feedback = None
            st.session_state.rewrite = None
            st.session_state.show_rewrite = False
            st.session_state.step = 2
            st.rerun()
