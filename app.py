import streamlit as st
import pandas as pd
from PIL import Image
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis do arquivo .env local
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# ==========================================
# 1. CONFIGURAÇÕES DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Assistente Financeiro com Groq",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Assistente Financeiro Pessoal (Groq IA)")
st.caption("Respostas ultra-rápidas powered by Llama 3 & Groq Cloud.")

# Sidebar - Configuração e Chave de API
st.sidebar.header("⚙️ Configurações")
user_name = st.sidebar.text_input("Nome do Usuário", value="Alex")

# Função para inicializar o cliente da API do Groq
def get_groq_client(key):
    if not key:
        return None
    return Groq(api_key=key)

client = get_groq_client(api_key)

# ==========================================
# 2. PROMPT DE SISTEMA (PERSONALIDADE DA IA)
# ==========================================
SYSTEM_INSTRUCTION = f"""
Você é um especialista em finanças pessoais e educação financeira moderno, empático e acolhedor.
Seu objetivo é ajudar {user_name} a organizar o orçamento sem julgamentos nem jargões bancários.
Fale de forma leve, direta, motivadora e prática. Use emojis estrategicamente.
Sempre trate erros financeiros com naturalidade e ofereça soluções acionáveis.
"""

# Aba de navegação
tab1, tab2 = st.tabs(["💬 Atendimento & Chat", "📊 Planejamento de Metas"])

# ------------------------------------------
# TAB 1: Chat de Atendimento
# ------------------------------------------
with tab1:
    st.subheader(f"Olá, {user_name}! Como posso ajudar o seu bolso hoje?")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe o histórico de mensagens
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Ex: 'Comprei por impulso' ou 'Não sei pra onde vai meu dinheiro'"):
        if not client:
            st.error("Por favor, insira sua API Key do Groq na barra lateral para continuar!")
        else:
            # Salva e exibe a mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Chama o modelo via Groq
            with st.chat_message("assistant"):
                with st.spinner("Processando resposta ultra-rápida..."):
                    # Construção das mensagens enviadas ao Groq
                    messages_to_send = [
                        {"role": "system", "content": SYSTEM_INSTRUCTION}
                    ]
                    for m in st.session_state.messages:
                        messages_to_send.append({"role": m["role"], "content": m["content"]})

                    # Requisição à API do Groq
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=messages_to_send,
                        temperature=0.7,
                        max_tokens=1024,
                    )
                    
                    response_text = completion.choices[0].message.content
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})

# ------------------------------------------
# TAB 2: Simulação de Metas
# ------------------------------------------
with tab2:
    st.subheader("🚀 Planejador de Metas Financeiras")
    
    col1, col2 = st.columns(2)
    with col1:
        meta_nome = st.text_input("Qual é a sua meta?", value="Reserva de Emergência")
        meta_valor = st.number_input("Valor total estimado (R$)", value=2000.0, step=100.0)
    with col2:
        meses = st.slider("Em quantos meses quer realizar?", min_value=1, max_value=24, value=5)
        
    valor_mensal = meta_valor / meses
    st.metric(label=f"Aporte mensal necessário para '{meta_nome}'", value=f"R$ {valor_mensal:.2f}")
    
    if st.button("Gerar Plano com Groq IA"):
        if not client:
            st.error("Insira sua API Key do Groq na barra lateral.")
        else:
            with st.spinner("Analisando metas..."):
                prompt_meta = f"""
                O usuário {user_name} quer guardar R$ {meta_valor:.2f} em {meses} meses para a meta '{meta_nome}'.
                Isso exige R$ {valor_mensal:.2f} por mês.
                Crie um plano motivacional em 3 passos simples para economizar esse valor no dia a dia.
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": prompt_meta}
                    ],
                    temperature=0.7
                )
                
                st.markdown(completion.choices[0].message.content)