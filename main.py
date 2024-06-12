import streamlit as st
from openai import OpenAI
import json


st.set_page_config(
    layout="wide"
)


st.markdown('''
            <style>
                .header {
                    background-color: green;
                    color: white;
                    margin: auto;
                    text-align: center;
                }
                .red {
                    background-color: red;
                    color: white;
                    margin: auto;
                    text-align: center;
                }
                #turno-do-chat {
                    background-color: green;
                    color: white;
                    margin: auto;
                    text-align: center;
                }
                .game { 
                    display: grid; 
                    grid-template-columns: 1fr 1fr 1fr; 
                    grid-template-rows: 1fr 1fr 1fr; 
                    grid-gap: 5px;
                    width: 100%;
                    margin: 20px auto ;
                    }
                .cell {
                    background-color: black;
                    color: white;
                    font-size: 30px;
                    font-style: bold;
                    text-align: center;
                    border: solid 1px white;
                    }
                .cell:hover{
                    background-color: green;
                    border: solid 1px;
                    color: white;
                    cursor: pointer;
                }
                .cell-2 {
                    background-color: green;
                    color: white;
                    font-size: 30px;
                    font-style: bold;
                    text-align: center;
                    border: solid 1px white;
                    }
                .cell-2:hover{
                    background-color: black;
                    border: solid 1px;
                    color: white;
                    cursor: pointer;
                }
                .divider{
                    margin: 5px auto;
                }
            </style>
            ''', unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Configurando os estados iniciais
if 'posicoes' not in st.session_state:
    st.session_state.posicoes = [0,1,2,3,4,5,6,7,8]

if 'turno' not in st.session_state:
    st.session_state.turno = 1

if 'vencedor' not in st.session_state:
    st.session_state.vencedor = 0
if 'chat' not in st.session_state:
    st.session_state.chat = 0

# Função para atualizar a velha   
def validacao(posicoes):
    #Verificar vitória do jogador desafiante
    if st.session_state.turno == 1:
        if (posicoes[0] == 'X' and posicoes[1] == 'X' and posicoes[2] == 'X') or (posicoes[3] == 'X' and posicoes[4] == 'X' and posicoes[5] == 'X') or (posicoes[6] == 'X' and posicoes[7] == 'X' and posicoes[8] == 'X'): 
            st.session_state.vencedor += 1
            return st.session_state.vencedor
        elif (posicoes[0] == 'X' and posicoes[3] == 'X' and posicoes[6] == 'X') or (posicoes[1] == 'X' and posicoes[4] == 'X' and posicoes[7] == 'X') or (posicoes[2] == 'X' and posicoes[5] == 'X' and posicoes[8] == 'X'):
            st.session_state.vencedor += 1
            return st.session_state.vencedor
        elif (posicoes[0] == 'X' and posicoes[4] == 'X' and posicoes[8] == 'X') or (posicoes[2] == 'X' and posicoes[4] == 'X' and posicoes[6] == 'X'): 
            st.session_state.vencedor += 1
            return st.session_state.vencedor
    
    #Verficar vitória do chat
    if st.session_state.turno == 2:
        if (posicoes[0] == 'O' and posicoes[1] == 'O' and posicoes[2] == 'O') or (posicoes[3] == 'O' and posicoes[4] == 'O' and posicoes[5] == 'O') or (posicoes[6] == 'O' and posicoes[7] == 'O' and posicoes[8] == 'O'): 
            st.session_state.chat += 1
            return st.session_state.chat
        elif (posicoes[0] == 'O' and posicoes[3] == 'O' and posicoes[6] == 'O') or (posicoes[1] == 'O' and posicoes[4] == 'O' and posicoes[7] == 'O') or (posicoes[2] == 'O' and posicoes[5] == 'O' and posicoes[8] == 'O'):
            st.session_state.chat += 1
            return st.session_state.chat
        elif (posicoes[0] == 'O' and posicoes[4] == 'O' and posicoes[8] == 'O') or (posicoes[2] == 'O' and posicoes[4] == 'O' and posicoes[6] == 'O'): 
            st.session_state.chat += 1
            return st.session_state.chat
            
def update_posicoes(index):
    if st.session_state.turno == 1:
        try:
            if 0 <= index < len(st.session_state.posicoes):
                st.session_state.posicoes[index] = 'X'
                posicoes = st.session_state.posicoes
                return posicoes
            
        except Exception as e:
            st.error(f"Erro ao atualizar posição: {e}")
    
    if st.session_state.turno == 2:
        try:
            if 0 <= index < len(st.session_state.posicoes):
                st.session_state.posicoes[index] = 'O'
                posicoes = st.session_state.posicoes
                return posicoes
        except Exception as e:
            st.error(f"Erro ao atualizar posição: {e}")

client = OpenAI()

def ask_openai(posicoes):
    if posicoes == "" and st.session_state.turno == 1:
        return "Faça sua jogada"
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": '''
                                                You are a tic-tac-toe player. Your goal is to form a line (vertical, horizontal, or diagonal) before your opponent does.
                                                    Evaluate the board represented by an array of 9 positions, following these rules:
                                                    1st Never play in the same position as your opponent.
                                                    2nd Never repeat a move.
                                                    3rd Always respond with a number only.
                                                    4th Choose a number between 0 and 8 that corresponds to a free position (one that contains a number).
                                                    5th Always try to block the opponent's move
                                                    
                                                    Example of response = 3
                                              '''},
                {"role": "user", "content": f'''
                                                Review the array {posicoes} and choose one number
                                                Answer with only one number
                                                Example of an answer = 3
                                             '''}
            ],
            temperature=0.1,
            max_tokens=500,
            top_p=0.25,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = completion.choices[0].message.content
        return answer
    
    except Exception as e:
        st.error(f"Erro ao consultar OpenAI: {e}")
        return None
# Função de callback para atualizar a posição escolhida
if st.session_state.turno == 1:
    with col1:
        
        st.write("<h1 class='header'>Turno do desafiante</h1>",unsafe_allow_html=True)
        st.write(f''' 
            <div class='game'>
                <div class='cell'>{st.session_state.posicoes[0]}</div>
                <div class='cell'>{st.session_state.posicoes[1]}</div>
                <div class='cell'>{st.session_state.posicoes[2]}</div>
                <div class='cell'>{st.session_state.posicoes[3]}</div>
                <div class='cell'>{st.session_state.posicoes[4]}</div>
                <div class='cell'>{st.session_state.posicoes[5]}</div>
                <div class='cell'>{st.session_state.posicoes[6]}</div>
                <div class='cell'>{st.session_state.posicoes[7]}</div>
                <div class='cell'>{st.session_state.posicoes[8]}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        #Verificando se há um ganhador
        if st.session_state.chat == 1:
            st.write("<h2 class='red'> O chat ganhou!</h2>",unsafe_allow_html=True)
            st.stop()
        elif st.session_state.vencedor == 1:
            st.write("<h2 class='header'> O desafiante ganhou!</h2>",unsafe_allow_html=True)
            st.stop()
    
    with col2:
        with st.container():
            st.write(f"<h1 class='header'>Controle do desafiante</h1>", unsafe_allow_html=True)
            st.write("<div class='divider'></div>", unsafe_allow_html=True)
            with st.form(key="form_escolha"):
                escolha = st.number_input('Selecione uma posição (0-8)', step=1, min_value=0, max_value=8)
                enviar = st.form_submit_button(label="Enviar")
                if enviar:
                    posicoes = update_posicoes(escolha)
                    validacao(posicoes)
                    
                    if st.session_state.vencedor == 1:
                        vencedor = st.session_state.vencedor
                        st.session_state.turno += 1
                        st.rerun()    
                        
                    st.session_state.turno += 1
                    st.rerun()
else:    
    with col1:       
        #Carregando a velha    
        st.write("<h1 class='header'>Turno do chat</h1>",unsafe_allow_html=True)
        st.write(f''' 
                    <div class='game'>
                        <div class='cell-2'>{st.session_state.posicoes[0]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[1]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[2]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[3]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[4]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[5]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[6]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[7]}</div>
                        <div class='cell-2'>{st.session_state.posicoes[8]}</div>
                    </div>
            ''', unsafe_allow_html=True)
        #Verificando o ganhador
        if st.session_state.vencedor == 1:
            st.write("<h2 class='header'> O desafiante ganhou!</h2>",unsafe_allow_html=True)
            st.stop()     
        
    with col2:    
        # Cria um formulário para selecionar uma posição
        posicoes = st.session_state.posicoes
        print(f"turno: {st.session_state.turno}")
        
        #Fazer requisições para o chatGPT
        resposta = ask_openai(posicoes)
        print(f"Resposta: {resposta}")
        
        if resposta == None:
            resposta = ask_openai(posicoes)
        
        #Atualizando posições
        posicoes = update_posicoes(int(resposta))
        
        #Verificando o vencedor        
        validacao(posicoes)
        
        if st.session_state.chat == 1:
            st.session_state.turno -= 1
            st.rerun()
            
        st.session_state.turno -= 1
        st.rerun()
        

# Mostra o estado atual das posições
#st.write(f"Posições atuais: {st.session_state.posicoes}")
#st.write(f"Vencedor: {st.session_state.vencedor}")
#st.write(f"Chat: {st.session_state.chat}")