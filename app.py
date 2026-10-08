import os
import pandas as pd
from PIL import Image
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Carrega as variáveis de ambiente
load_dotenv()
ENV_GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Modelo ativo e estável no Groq
MODEL_NAME = "openai/gpt-oss-120b"  # Pode trocar por "llama-3.1-8b-instant"

# ==========================================
# 1. CONFIGURAÇÕES DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="FinIA - Assistente Futurista",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. ESTILIZAÇÃO CSS FUTURISTA & GLASSMORPHISM
# ==========================================
futuristic_css = """
<style>
    /* Fundo Principal com Gradiente Tech Futurista */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #1a103c 0%, #080c1d 60%, #03050c 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Efeito de Malha/Grid no Fundo */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            linear-gradient(rgba(0, 242, 254, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 242, 254, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    /* Estilização dos Títulos com Gradiente Neon */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
    }
    
    .stApp h1 {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
    }

    /* Barra Lateral Futurista (Glassmorphism) */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(0, 242, 254, 0.2) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.5);
    }

    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(0, 242, 254, 0.15);
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        color: #94a3b8 !important;
        border: none !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.2) 0%, rgba(79, 172, 254, 0.2) 100%) !important;
        color: #00f2fe !important;
        border: 1px solid rgba(0, 242, 254, 0.5) !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.3) !important;
    }

    /* Caixas de Texto / Inputs em Vidro Fosco */
    .stTextInput input, .stNumberInput input {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 10px rgba(0, 242, 254, 0.5) !important;
    }

    /* Botão Neon Futurista */
    .stButton > button {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.8) !important;
    }

    /* Balões de Mensagem do Chat */
    [data-testid="stChatMessage"] {
        background-color: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(0, 242, 254, 0.15) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
    }

    /* Métrica de Valor Destacada */
    [data-testid="stMetricValue"] {
        color: #00f2fe !important;
        font-size: 2.2rem !important;
        text-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
    }
</style>
"""
st.markdown(futuristic_css, unsafe_allow_html=True)

# ==========================================
# 3. CONTEÚDO PRINCIPAL
# ==========================================
st.title("⚡ FIN.IA - Assistente Financeiro")
st.caption("✦ Inteligência Artificial Financeira em Alta Velocidade Powered by Groq Cloud")

# Sidebar - Configurações
st.sidebar.header("⚙️ Painel de Controle")
user_name = st.sidebar.text_input("Nome do Usuário", value="Alex")

input_api_key = st.sidebar.text_input(
    "API Key do Groq",
    value=ENV_GROQ_API_KEY,
    type="password",
    help="Insira sua chave do Groq aqui ou configure no arquivo .env"
)

def get_groq_client(key):
    if not key:
        return None
    return Groq(api_key=key)

client = get_groq_client(input_api_key)

# Prompt de Sistema
SYSTEM_INSTRUCTION = f"""
Você é um assistente financeiro futurista, inovador, altamente inteligente e empático.
Seu objetivo é ajudar {user_name} a otimizar finanças de forma prática e motivadora.
Responda com clareza, use tópicos modernos e inclua emojis futuristas (🚀, ⚡, 📊, 💎, 🛡️).
"""

# Navegação por Abas
tab1, tab2 = st.tabs(["💬 Chat de Atendimento", "📊 Metas & Simulações"])

# ------------------------------------------
# TAB 1: Chat Futurista
# ------------------------------------------
with tab1:
    st.subheader(f"👋 Conectado: Olá, {user_name}!")
    st.caption("Como posso ajudar na otimização do seu capital hoje?")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Digite sua dúvida financeiras (Ex: 'Como organizar minha reserva?')"):
        if not client:
            st.error("⚠️ API Key do Groq necessária! Insira sua chave no painel lateral.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("⚡ Processando resposta neural..."):
                    try:
                        messages_to_send = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
                        for m in st.session_state.messages:
                            messages_to_send.append({"role": m["role"], "content": m["content"]})

                        completion = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=messages_to_send,
                            temperature=0.7,
                            max_tokens=1024,
                        )
                        
                        response_text = completion.choices[0].message.content
                        st.markdown(response_text)
                        st.session_state.messages.append({"role": "assistant", "content": response_text})
                    except Exception as e:
                        st.error(f"Erro de conexão com a IA: {e}")

# ------------------------------------------
# TAB 2: Planejamento de Metas
# ------------------------------------------
with tab2:
    st.subheader("🚀 Simulador de Metas Financeiras")
    
    col1, col2 = st.columns(2)
    with col1:
        meta_nome = st.text_input("Objetivo Financeiro", value="Reserva de Emergência")
        meta_valor = st.number_input("Valor Alvo (R$)", value=3000.0, step=100.0)
    with col2:
        meses = st.slider("Prazo de Execução (Meses)", min_value=1, max_value=36, value=12)
        
    valor_mensal = meta_valor / meses
    st.metric(label=f"Aporte Mensal Requerido para '{meta_nome}'", value=f"R$ {valor_mensal:.2f}")
    
    if st.button("⚡ Gerar Estratégia de Aporte"):
        if not client:
            st.error("⚠️ Insira sua API Key do Groq na barra lateral para continuar.")
        else:
            with st.spinner("Analisando projeções financeiras..."):
                try:
                    prompt_meta = f"""
                    O usuário {user_name} deseja atingir o valor de R$ {meta_valor:.2f} em {meses} meses para a meta '{meta_nome}'.
                    Aporte diário/mensal necessário: R$ {valor_mensal:.2f} por mês.
                    Crie um plano acionável de 3 etapas inovadoras e simples para atingir este objetivo com sucesso.
                    """
                    
                    completion = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": SYSTEM_INSTRUCTION},
                            {"role": "user", "content": prompt_meta}
                        ],
                        temperature=0.7
                    )
                    
                    st.markdown(completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Erro ao sintetizar estratégia: {e}")