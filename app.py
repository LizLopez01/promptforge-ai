import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PromptForge AI · ITJOLI", page_icon="⚡", layout="centered")

# Lee desde Streamlit Cloud secrets o desde .env local
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

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
                "rewrite": None, "show_rewrite": False, "language": "Español"}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── TRADUCCIONES ─────────────────────────────────────────────────────────────
TEXTS = {
    "Español": {
        "lang_label": "🌐 Elige tu idioma",
        "area_label": "¿en qué área trabajas?",
        "area_hint": "Selecciona una opción o escribe tu profesión. La IA adaptará cada ejercicio a tu contexto real.",
        "profession_input": T("profession_input"),
        "profession_placeholder": T("profession_placeholder"),
        "start_btn": "🚀 Comenzar mi entrenamiento",
        "warning_profession": T("warning_profession"),
        "why_label": T("why_label"),
        "why_1_title": T("why_1_title"),
        "why_1_desc": T("why_1_desc"),
        "why_2_title": T("why_2_title"),
        "why_2_desc": T("why_2_desc"),
        "why_3_title": T("why_3_title"),
        "why_3_desc": T("why_3_desc"),
        "exercise_label": "📋 tu ejercicio",
        "prompt_label": "✍️ escribe tu prompt",
        "prompt_placeholder": "Escribe aquí tu prompt...\n\nTip: sé específico, da contexto, define el tono y el formato.",
        "chars_ready": "· ¡Listo!",
        "chars_min": "· Mínimo 10 caracteres",
        "chars_label": "caracteres",
        "eval_btn": "⭐ Evaluar prompt",
        "new_ex_btn": T("new_ex_btn"),
        "tips_label": T("tips_label"),
        "tip_1_title": T("tip_1_title"), "tip_1_desc": T("tip_1_desc"),
        "tip_2_title": T("tip_2_title"), "tip_2_desc": T("tip_2_desc"),
        "tip_3_title": T("tip_3_title"), "tip_3_desc": T("tip_3_desc"),
        "tip_4_title": T("tip_4_title"), "tip_4_desc": T("tip_4_desc"),
        "session_label": T("session_label"),
        "done_label": T("done_label"), "avg_label": T("avg_label"), "level_label": "Nivel",
        "spinner_ex": T("spinner_ex"),
        "spinner_eval": T("spinner_eval"),
        "spinner_rw": T("spinner_rw"),
        "error_connect": "❌ Error al conectar:",
        "eval_section": T("eval_section"),
        "improve_lbl": T("improve_lbl"), "suggest_lbl": T("suggest_lbl"), "good_lbl": T("good_lbl"),
        "rewrite_btn": T("rewrite_btn"),
        "next_btn": T("next_btn"),
        "progress_btn": T("progress_btn"),
        "rewrite_hdr": T("rewrite_hdr"),
        "orig_lbl": T("orig_lbl"), "improved_lbl": T("improved_lbl"),
        "progress_label": T("progress_label"),
        "exercises_lbl": T("exercises_lbl"), "best_lbl": T("best_lbl"), "level_curr": T("level_curr"),
        "history_lbl": T("history_lbl"),
        "export_btn": T("export_btn"),
        "clear_btn": T("clear_btn"),
        "continue_btn": "🚀 Seguir practicando",
        "empty_history": T("empty_history"),
        "lv1": "⚡ Nivel Básico", "lv2": "🔥 Nivel Intermedio", "lv3": "💎 Nivel Avanzado",
        "steps": ["🎯 Profesión", "📝 Ejercicio", "⭐ Evaluación", "📊 Progreso"],
        "clase_badge": T("clase_badge"),
    },
    "English": {
        "lang_label": "🌐 Choose your language",
        "area_label": "What field do you work in?",
        "area_hint": "Select an option or type your profession. AI will adapt each exercise to your real context.",
        "profession_input": "✏️ Or type your profession:",
        "profession_placeholder": "E.g.: UX Designer, Accountant, Lawyer, Chef...",
        "start_btn": "🚀 Start my training",
        "warning_profession": "⚠️ Please enter your profession first.",
        "why_label": "💡 Why learn prompt engineering?",
        "why_1_title": "Skill #1 emerging",
        "why_1_desc": "WEF 2025 and Forrester 2026: the most in-demand skill.",
        "why_2_title": "Real work exercises",
        "why_2_desc": "AI generates situations from your specific profession.",
        "why_3_title": "Level up automatically",
        "why_3_desc": "Basic → Intermediate → Advanced based on your progress.",
        "exercise_label": "📋 your exercise",
        "prompt_label": "✍️ write your prompt",
        "prompt_placeholder": "Write your prompt here...\n\nTip: be specific, give context, define tone and format.",
        "chars_ready": "· Ready!",
        "chars_min": "· Minimum 10 characters",
        "chars_label": "characters",
        "eval_btn": "⭐ Evaluate prompt",
        "new_ex_btn": "🔄 New exercise",
        "tips_label": "🎯 tips for a good prompt",
        "tip_1_title": "Be specific", "tip_1_desc": "Define exactly what you want.",
        "tip_2_title": "Give context", "tip_2_desc": "Explain who you are and why.",
        "tip_3_title": "Define tone", "tip_3_desc": "Formal, technical, simple...",
        "tip_4_title": "Ask for format", "tip_4_desc": "List, table, paragraph, steps...",
        "session_label": "📊 current session",
        "done_label": "Done", "avg_label": "Average", "level_label": "Level",
        "spinner_ex": "✨ Generating your personalized exercise...",
        "spinner_eval": "🤖 Analyzing your prompt...",
        "spinner_rw": "🪄 Improving your prompt...",
        "error_connect": "❌ Connection error:",
        "eval_section": "prompt evaluation",
        "improve_lbl": "⚠ What to improve", "suggest_lbl": "💡 Suggestion", "good_lbl": "✅ What you did well",
        "rewrite_btn": "✨ Rewrite with AI",
        "next_btn": "➡️ Next exercise",
        "progress_btn": "📊 View my progress",
        "rewrite_hdr": "✨ AI improved version",
        "orig_lbl": "Your original prompt", "improved_lbl": "Improved version",
        "progress_label": "📊 session summary",
        "exercises_lbl": "Exercises", "best_lbl": "Best score", "level_curr": "Current level",
        "history_lbl": "🕐 history",
        "export_btn": "⬇️ Export JSON",
        "clear_btn": "🗑️ Clear history",
        "continue_btn": "🚀 Keep practicing",
        "empty_history": "🎯 Complete your first exercise to see history here.",
        "lv1": "⚡ Basic Level", "lv2": "🔥 Intermediate Level", "lv3": "💎 Advanced Level",
        "steps": ["🎯 Profession", "📝 Exercise", "⭐ Evaluation", "📊 Progress"],
        "clase_badge": "🎓 AI Class",
    },
    "Português": {
        "lang_label": "🌐 Escolha seu idioma",
        "area_label": "Em que área você trabalha?",
        "area_hint": "Selecione uma opção ou escreva sua profissão. A IA adaptará cada exercício ao seu contexto real.",
        "profession_input": "✏️ Ou escreva sua profissão:",
        "profession_placeholder": "Ex: Designer UX, Contador, Advogado, Chef...",
        "start_btn": "🚀 Começar meu treinamento",
        "warning_profession": "⚠️ Por favor, insira sua profissão primeiro.",
        "why_label": "💡 Por que aprender prompt engineering?",
        "why_1_title": "Habilidade #1 emergente",
        "why_1_desc": "WEF 2025 e Forrester 2026: a skill mais demandada.",
        "why_2_title": "Exercícios do seu trabalho real",
        "why_2_desc": "A IA gera situações da sua profissão específica.",
        "why_3_title": "Suba de nível automaticamente",
        "why_3_desc": "Básico → Intermediário → Avançado conforme seu progresso.",
        "exercise_label": "📋 seu exercício",
        "prompt_label": "✍️ escreva seu prompt",
        "prompt_placeholder": "Escreva seu prompt aqui...\n\nDica: seja específico, dê contexto, defina tom e formato.",
        "chars_ready": "· Pronto!",
        "chars_min": "· Mínimo 10 caracteres",
        "chars_label": "caracteres",
        "eval_btn": "⭐ Avaliar prompt",
        "new_ex_btn": "🔄 Novo exercício",
        "tips_label": "🎯 dicas para um bom prompt",
        "tip_1_title": "Seja específico", "tip_1_desc": "Defina exatamente o que quer.",
        "tip_2_title": "Dê contexto", "tip_2_desc": "Explique quem você é e para quê.",
        "tip_3_title": "Defina o tom", "tip_3_desc": "Formal, técnico, simples...",
        "tip_4_title": "Peça formato", "tip_4_desc": "Lista, tabela, parágrafo, passos...",
        "session_label": "📊 sessão atual",
        "done_label": "Feitos", "avg_label": "Média", "level_label": "Nível",
        "spinner_ex": "✨ Gerando seu exercício personalizado...",
        "spinner_eval": "🤖 Analisando seu prompt...",
        "spinner_rw": "🪄 Melhorando seu prompt...",
        "error_connect": "❌ Erro de conexão:",
        "eval_section": "avaliação do seu prompt",
        "improve_lbl": "⚠ O que melhorar", "suggest_lbl": "💡 Sugestão", "good_lbl": "✅ O que você fez bem",
        "rewrite_btn": "✨ Reescrever com IA",
        "next_btn": "➡️ Próximo exercício",
        "progress_btn": "📊 Ver meu progresso",
        "rewrite_hdr": "✨ Versão melhorada pela IA",
        "orig_lbl": "Seu prompt original", "improved_lbl": "Versão melhorada",
        "progress_label": "📊 resumo da sessão",
        "exercises_lbl": "Exercícios", "best_lbl": "Melhor pontuação", "level_curr": "Nível atual",
        "history_lbl": "🕐 histórico",
        "export_btn": T("export_btn"),
        "clear_btn": "🗑️ Limpar histórico",
        "continue_btn": "🚀 Continuar praticando",
        "empty_history": "🎯 Complete seu primeiro exercício para ver o histórico aqui.",
        "lv1": "⚡ Nível Básico", "lv2": "🔥 Nível Intermediário", "lv3": "💎 Nível Avançado",
        "steps": ["🎯 Profissão", "📝 Exercício", "⭐ Avaliação", "📊 Progresso"],
        "clase_badge": "🎓 Aula de IA",
    },
    "Français": {
        "lang_label": "🌐 Choisissez votre langue",
        "area_label": "Dans quel domaine travaillez-vous?",
        "area_hint": "Sélectionnez une option ou écrivez votre profession. L'IA adaptera chaque exercice à votre contexte réel.",
        "profession_input": "✏️ Ou écrivez votre profession:",
        "profession_placeholder": "Ex: Designer UX, Comptable, Avocat, Chef...",
        "start_btn": "🚀 Commencer ma formation",
        "warning_profession": "⚠️ Veuillez entrer votre profession d'abord.",
        "why_label": "💡 Pourquoi apprendre le prompt engineering?",
        "why_1_title": "Compétence #1 émergente",
        "why_1_desc": "WEF 2025 et Forrester 2026: la compétence la plus demandée.",
        "why_2_title": "Exercices de votre vrai travail",
        "why_2_desc": "L'IA génère des situations de votre profession spécifique.",
        "why_3_title": "Montez de niveau automatiquement",
        "why_3_desc": "Basique → Intermédiaire → Avancé selon vos progrès.",
        "exercise_label": "📋 votre exercice",
        "prompt_label": "✍️ écrivez votre prompt",
        "prompt_placeholder": "Écrivez votre prompt ici...\n\nConseil: soyez précis, donnez du contexte, définissez le ton et le format.",
        "chars_ready": "· Prêt!",
        "chars_min": "· Minimum 10 caractères",
        "chars_label": "caractères",
        "eval_btn": "⭐ Évaluer le prompt",
        "new_ex_btn": "🔄 Nouvel exercice",
        "tips_label": "🎯 conseils pour un bon prompt",
        "tip_1_title": "Soyez précis", "tip_1_desc": "Définissez exactement ce que vous voulez.",
        "tip_2_title": "Donnez du contexte", "tip_2_desc": "Expliquez qui vous êtes et pourquoi.",
        "tip_3_title": "Définissez le ton", "tip_3_desc": "Formel, technique, simple...",
        "tip_4_title": "Demandez un format", "tip_4_desc": "Liste, tableau, paragraphe, étapes...",
        "session_label": "📊 session actuelle",
        "done_label": "Faits", "avg_label": "Moyenne", "level_label": "Niveau",
        "spinner_ex": "✨ Génération de votre exercice personnalisé...",
        "spinner_eval": "🤖 Analyse de votre prompt...",
        "spinner_rw": "🪄 Amélioration de votre prompt...",
        "error_connect": "❌ Erreur de connexion:",
        "eval_section": "évaluation de votre prompt",
        "improve_lbl": "⚠ À améliorer", "suggest_lbl": "💡 Suggestion", "good_lbl": "✅ Ce que vous avez bien fait",
        "rewrite_btn": "✨ Réécrire avec l'IA",
        "next_btn": "➡️ Exercice suivant",
        "progress_btn": "📊 Voir mes progrès",
        "rewrite_hdr": "✨ Version améliorée par l'IA",
        "orig_lbl": "Votre prompt original", "improved_lbl": "Version améliorée",
        "progress_label": "📊 résumé de la session",
        "exercises_lbl": "Exercices", "best_lbl": "Meilleur score", "level_curr": "Niveau actuel",
        "history_lbl": "🕐 historique",
        "export_btn": "⬇️ Exporter JSON",
        "clear_btn": "🗑️ Effacer l'historique",
        "continue_btn": "🚀 Continuer à pratiquer",
        "empty_history": "🎯 Complétez votre premier exercice pour voir l'historique ici.",
        "lv1": "⚡ Niveau Basique", "lv2": "🔥 Niveau Intermédiaire", "lv3": "💎 Niveau Avancé",
        "steps": ["🎯 Profession", "📝 Exercice", "⭐ Évaluation", "📊 Progrès"],
        "clase_badge": "🎓 Cours IA",
    }
}

def T(key):
    lang = st.session_state.get("language", "Español")
    return TEXTS.get(lang, TEXTS["Español"]).get(key, key)


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
.steps-wrap{display:flex;align-items:center;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:10px 12px;margin-bottom:1.5rem;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch;}
.steps-wrap::-webkit-scrollbar{display:none;}
.sp{display:flex;align-items:center;gap:5px;font-size:clamp(10px,2.5vw,13px);font-weight:500;padding:5px 10px;border-radius:12px;color:rgba(200,210,255,0.4);white-space:nowrap}
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
div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea{background:rgba(20,20,50,0.9)!important;border:1px solid rgba(255,255,255,0.12)!important;border-radius:12px!important;color:#E8EEFF!important;font-size:14px!important;caret-color:#00D4FF!important}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus{border-color:rgba(0,212,255,0.5)!important;box-shadow:0 0 0 2px rgba(0,212,255,0.1)!important;color:#E8EEFF!important}
div[data-testid="stTextInput"] input::placeholder,div[data-testid="stTextArea"] textarea::placeholder{color:rgba(200,210,255,0.3)!important}
div[data-testid="stTextInput"] label,div[data-testid="stTextArea"] label{color:rgba(200,210,255,0.5)!important;font-size:12px!important}
textarea{color:#E8EEFF!important;background:rgba(20,20,50,0.9)!important}
.stButton>button{
  border-radius:50px!important;
  font-weight:700!important;
  font-size:13px!important;
  transition:all 0.25s ease!important;
  letter-spacing:0.5px!important;
  padding:0.5rem 1.2rem!important;
  text-transform:uppercase!important;
}
.stButton>button[kind="primary"]{
  background:linear-gradient(135deg,#0066FF,#00C8FF)!important;
  border:none!important;
  color:white!important;
  box-shadow:0 0 15px rgba(0,180,255,0.5),0 4px 20px rgba(0,100,255,0.4)!important;
}
.stButton>button[kind="primary"]:hover{
  transform:translateY(-2px) scale(1.02)!important;
  box-shadow:0 0 25px rgba(0,200,255,0.7),0 6px 25px rgba(0,100,255,0.5)!important;
  background:linear-gradient(135deg,#0080FF,#00E0FF)!important;
}
.stButton>button[kind="secondary"]{
  background:rgba(0,100,255,0.08)!important;
  border:1px solid rgba(0,180,255,0.35)!important;
  color:#00C8FF!important;
}
.stButton>button[kind="secondary"]:hover{
  background:rgba(0,180,255,0.15)!important;
  border-color:rgba(0,220,255,0.6)!important;
  color:#00E0FF!important;
  box-shadow:0 0 12px rgba(0,200,255,0.3)!important;
  transform:translateY(-1px)!important;
}
.stDownloadButton>button{
  background:linear-gradient(135deg,rgba(0,255,157,0.1),rgba(0,200,255,0.1))!important;
  border:1px solid rgba(0,255,157,0.4)!important;
  color:#00FF9D!important;
  border-radius:50px!important;
  font-weight:700!important;
  box-shadow:0 0 10px rgba(0,255,157,0.2)!important;
}
.stDownloadButton>button:hover{
  box-shadow:0 0 20px rgba(0,255,157,0.4)!important;
  transform:translateY(-1px)!important;
}
div[data-testid="stAlert"]{background:rgba(64,80,255,0.08)!important;border:1px solid rgba(64,80,255,0.25)!important;border-radius:12px!important;color:rgba(200,210,255,0.85)!important}
.stSpinner>div{border-top-color:#00D4FF!important}
div[data-testid="stMarkdownContainer"] p{color:rgba(200,210,255,0.7);font-size:13px}
/* Hide Ctrl+Enter hint */
.stTextArea [data-baseweb="textarea"] + div,
.stTextArea div[class*="hint"],
small[class*="hint"]{display:none!important}
textarea + small{display:none!important}
[data-testid="InputInstructions"]{display:none!important}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div style="
  background: linear-gradient(135deg, #0D1B3E 0%, #0A2050 50%, #0D1B3E 100%);
  border: 1px solid rgba(0,180,255,0.3);
  border-radius: 24px;
  padding: 1.2rem 1.4rem;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 0 40px rgba(0,100,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
  flex-wrap: nowrap;
  overflow: hidden;
">
  <img src="data:image/png;base64,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"
    width="90" height="90"
    style="border-radius:50%;
           box-shadow:0 0 30px rgba(0,180,255,0.8), 0 0 60px rgba(0,100,255,0.4);
           border:2px solid rgba(0,200,255,0.4);
           flex-shrink:0;">
  <div style="flex:1;">
    <div style="
      font-size:clamp(18px, 4vw, 30px);
      font-weight:900;
      letter-spacing:-0.5px;
      line-height:1.1;
      margin-bottom:4px;
      font-family:Inter,sans-serif;
      white-space:nowrap;
    ">
      <span style="color:#FFFFFF;">Prompt</span><span style="
        color:#00C8FF;
        text-shadow: 0 0 20px rgba(0,200,255,0.8);
      ">Forge</span>
      <span style="color:#FFFFFF;"> AI</span>
    </div>
    <div style="
      font-size:13px;
      color:rgba(150,200,255,0.7);
      font-weight:500;
      letter-spacing:0.5px;
      font-family:Inter,sans-serif;
    ">ITJOLI · Intelligence & AI Group</div>
    <div style="
      font-size:11px;
      color:rgba(0,200,255,0.5);
      font-weight:600;
      letter-spacing:2px;
      text-transform:uppercase;
      margin-top:3px;
      font-family:Inter,sans-serif;
    ">Clase de Inteligencia Artificial</div>
  </div>
  <div style="
    background: linear-gradient(135deg, rgba(0,100,255,0.2), rgba(0,200,255,0.15));
    border: 1px solid rgba(0,200,255,0.4);
    color: #00C8FF;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 18px;
    border-radius: 50px;
    white-space: nowrap;
    box-shadow: 0 0 15px rgba(0,180,255,0.2);
    letter-spacing: 0.5px;
    font-family:Inter,sans-serif;
  ">🎓 Clase de IA</div>
</div>
""", unsafe_allow_html=True)

# STEPS
def render_steps():
    s = st.session_state.step
    items = list(zip(["🎯","📝","⭐","📊"], T("steps")))
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

    st.markdown('<div class="lbl">🌐 elige tu idioma / choose your language</div>', unsafe_allow_html=True)
    lang_options = {
        "🇪🇸 Español": "Español",
        "🇺🇸 English": "English",
        "🇧🇷 Português": "Português",
        "🇫🇷 Français": "Français"
    }
    selected_lang = st.radio(
        label="idioma",
        label_visibility="collapsed",
        options=list(lang_options.keys()),
        horizontal=True,
        index=0
    )
    st.session_state.language = lang_options[selected_lang]
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f'<div class="lbl">{T("area_label")}</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    chips = [("📣","Marketing Digital"),("🏥","Salud y Medicina"),("💼","Administración"),
             ("📚","Educación"),("👥","Recursos Humanos"),("💻","Tecnología")]
    for i,(icon,label) in enumerate(chips):
        col = [c1,c2,c3][i%3]
        with col:
            if st.button(f"{icon} {label}", key=f"c{i}", use_container_width=True):
                st.session_state.profession = label
                st.rerun()

    profession = st.text_input(T("profession_input"), value=st.session_state.profession,
                                placeholder=T("profession_placeholder"))
    st.session_state.profession = profession
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(T("start_btn"), type="primary", use_container_width=True):
        if not profession.strip():
            st.warning(T("warning_profession"))
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
    lv_labels = {1:T("lv1"), 2:T("lv2"), 3:T("lv3")}
    lv_cls    = {1:"lv1", 2:"lv2", 3:"lv3"}
    lv_desc   = {1:"básico (simple y directo)",
                 2:"intermedio (con contexto y restricciones específicas)",
                 3:"avanzado (complejo, multi-paso)"}

    if not st.session_state.exercise:
        with st.spinner(T("spinner_ex")):
            try:
                lang = st.session_state.language
                ex = call_ai(
                    f"Generate ONE prompt engineering exercise at level {lv_desc[level]} "
                    f"for someone who works in: {st.session_state.profession}. "
                    f"Real work situation. Max 3-4 sentences. Only the exercise text, no titles. "
                    f"IMPORTANT: Write the entire response in {lang}. "
                    f"If {lang} is Español, respond in Spanish. "
                    f"If {lang} is English, respond in English. "
                    f"If {lang} is Português, respond in Portuguese. "
                    f"If {lang} is Français, respond in French."
                )
                st.session_state.exercise = ex
            except Exception as e:
                st.error(f"{T('error_connect')} {e}")
                st.stop()

    col_ex, col_tips = st.columns([3, 2])

    with col_ex:
        st.markdown(f'<div class="{lv_cls[level]}">{lv_labels[level]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="lbl">{T("exercise_label")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exbox">{st.session_state.exercise}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="lbl">{T("prompt_label")}</div>', unsafe_allow_html=True)
        user_prompt = st.text_area(
            label="prompt", label_visibility="collapsed",
            placeholder=T("prompt_placeholder"),
            height=140
        )
        chars = len(user_prompt)
        st.caption(f"{'🟢' if chars>30 else '🔴'} {chars} caracteres {T("chars_ready") if chars>=10 else T("chars_min")}")

        ca, cb = st.columns(2)
        with ca:
            eval_clicked = st.button(T("eval_btn"), type="primary",
                                      use_container_width=True, disabled=chars < 10)
        with cb:
            if st.button(T("new_ex_btn"), use_container_width=True):
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
            <div><div style="font-size:22px;font-weight:800;color:#00D4FF">{done}</div><div style="font-size:11px;color:rgba(200,210,255,0.4)">{T("done_label")}</div></div>
            <div><div style="font-size:22px;font-weight:800;color:#00FF9D">{avg if scores else '—'}</div><div style="font-size:11px;color:rgba(200,210,255,0.4)">Promedio</div></div>
            <div><div style="font-size:22px;font-weight:800;color:#FB923C">{level}</div><div style="font-size:11px;color:rgba(200,210,255,0.4)">Nivel</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    if eval_clicked and chars >= 10:
        with st.spinner(T("spinner_eval")):
            try:
                lang = st.session_state.language
                raw = call_ai(
                    f"You are a STRICT and HONEST prompt engineering evaluator. "
                    f"Evaluate rigorously if the prompt is good or bad. "
                    f"Vague, short, context-free prompts MUST score below 40. "
                    f"Only well-structured, specific, contextualized prompts deserve above 70. "
                    f'Exercise: "{st.session_state.exercise}" | '
                    f"Profession: {st.session_state.profession} | "
                    f'User prompt: "{user_prompt}" | '
                    f"Criteria: (1) Specificity, (2) Context, (3) Format requested, (4) Relevance to exercise. "
                    f"If prompt is less than 20 words or vague, score CANNOT exceed 45. "
                    f"IMPORTANT: Write all text fields in {lang}. "
                    f'Respond ONLY with JSON no markdown: '
                    f'{{"score":30,"title":"honest title","description":"one sentence","improve":"critical aspect","suggest":"concrete suggestion","good":"enthusiastic if good, motivating message if not"}}'
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
                st.error(f"{T('error_connect')} {e}")

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
            if st.button(T("rewrite_btn"), use_container_width=True):
                with st.spinner(T("spinner_rw")):
                    try:
                        lang = st.session_state.language
                        rw = call_ai(
                            f"You are a prompt engineering expert. "
                            f"Profession: {st.session_state.profession} | "
                            f'Exercise: "{st.session_state.exercise}" | '
                            f'Original prompt: "{user_prompt}" | '
                            f"Rewrite improving: specificity, context, tone and format. "
                            f"Respond ONLY with the improved prompt. "
                            f"Write the improved prompt in {lang}."
                        )
                        st.session_state.rewrite = rw.strip()
                        st.session_state.show_rewrite = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"{T('error_connect')} {e}")
        with c2:
            if st.button(T("next_btn"), use_container_width=True):
                st.session_state.exercise = ""
                st.session_state.feedback = None
                st.session_state.rewrite = None
                st.session_state.show_rewrite = False
                st.session_state.step = 2
                st.rerun()
        with c3:
            if st.button(T("progress_btn"), use_container_width=True):
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
        st.info(T("empty_history"))

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.download_button(
            label=T("export_btn"),
            data=json.dumps({"profesion":st.session_state.profession,"ejercicios_completados":done,
                              "puntaje_promedio":avg,"mejor_puntaje":best,"nivel_alcanzado":level,
                              "historial":st.session_state.history}, indent=2, ensure_ascii=False),
            file_name="promptforge_progreso.json", mime="application/json", use_container_width=True
        )
    with c2:
        if st.button(T("clear_btn"), use_container_width=True):
            for k in ["scores","history"]: st.session_state[k] = []
            st.session_state.done = 0
            st.session_state.level = 1
            st.session_state.feedback = None
            st.session_state.rewrite = None
            st.rerun()
    with c3:
        if st.button(T("continue_btn"), type="primary", use_container_width=True):
            st.session_state.exercise = ""
            st.session_state.feedback = None
            st.session_state.rewrite = None
            st.session_state.show_rewrite = False
            st.session_state.step = 2
            st.rerun()
