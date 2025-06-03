import sqlite3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'chatbot.db'

def init_database():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela para consultas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            periodo TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id TEXT
        )
    ''')
    
    # Tabela para histórico de conversas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_conversas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            mensagem_usuario TEXT,
            resposta_bot TEXT,
            estado TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela para estado das conversas (para persistir entre reinicializações)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estados_conversa (
            user_id TEXT PRIMARY KEY,
            estado TEXT NOT NULL,
            dados_coletados TEXT,
            ultima_atividade TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def salvar_consulta(nome, data, periodo, user_id):
    """Salva uma consulta no banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO consultas (nome, data, periodo, user_id)
        VALUES (?, ?, ?, ?)
    ''', (nome, data, periodo, user_id))
    
    consulta_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return consulta_id

def salvar_historico(user_id, mensagem_usuario, resposta_bot, estado):
    """Salva o histórico da conversa"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO historico_conversas (user_id, mensagem_usuario, resposta_bot, estado)
        VALUES (?, ?, ?, ?)
    ''', (user_id, mensagem_usuario, resposta_bot, estado))
    
    conn.commit()
    conn.close()

def salvar_estado_conversa(user_id, estado, dados_coletados):
    """Salva o estado atual da conversa no banco"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    dados_json = json.dumps(dados_coletados)
    
    cursor.execute('''
        INSERT OR REPLACE INTO estados_conversa (user_id, estado, dados_coletados)
        VALUES (?, ?, ?)
    ''', (user_id, estado, dados_json))
    
    conn.commit()
    conn.close()

def carregar_estado_conversa(user_id):
    """Carrega o estado da conversa do banco"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT estado, dados_coletados FROM estados_conversa WHERE user_id = ?
    ''', (user_id,))
    
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        estado, dados_json = resultado
        dados = json.loads(dados_json) if dados_json else {}
        return {'estado': estado, 'dados': dados}
    
    return None

def obter_consultas():
    """Obtém todas as consultas do banco"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, nome, data, periodo, data_criacao, user_id 
        FROM consultas 
        ORDER BY data_criacao DESC
    ''')
    
    consultas = []
    for row in cursor.fetchall():
        consultas.append({
            'id': row[0],
            'nome': row[1],
            'data': row[2],
            'periodo': row[3],
            'data_criacao': row[4],
            'user_id': row[5]
        })
    
    conn.close()
    return consultas

# Controle de estado da conversa (agora com persistência)
conversas = {}

# Estados possíveis da conversa
ESTADOS = {
    'INICIAL': 'inicial',
    'AGUARDANDO_NOME': 'aguardando_nome',
    'AGUARDANDO_DATA': 'aguardando_data',
    'AGUARDANDO_PERIODO': 'aguardando_periodo',
    'FINALIZADO': 'finalizado'
}

def obter_estado_conversa(user_id):
    """Obtém o estado atual da conversa para um usuário (com persistência)"""
    if user_id not in conversas:
        # Tenta carregar do banco de dados
        estado_bd = carregar_estado_conversa(user_id)
        if estado_bd:
            conversas[user_id] = estado_bd
        else:
            conversas[user_id] = {
                'estado': ESTADOS['INICIAL'],
                'dados': {}
            }
    return conversas[user_id]

def processar_mensagem(user_id, mensagem):
    """Processa a mensagem baseada no estado atual da conversa"""
    conversa = obter_estado_conversa(user_id)
    estado_atual = conversa['estado']
    
    if estado_atual == ESTADOS['INICIAL']:
        conversa['estado'] = ESTADOS['AGUARDANDO_NOME']
        resposta = "Olá! Vou te ajudar a marcar uma consulta. 😊\n\nQual é o seu nome?"
    
    elif estado_atual == ESTADOS['AGUARDANDO_NOME']:
        conversa['dados']['nome'] = mensagem.strip()
        conversa['estado'] = ESTADOS['AGUARDANDO_DATA']
        resposta = f"Muito bem, {mensagem.strip()}! 👍\n\nAgora me diga em que data você gostaria de marcar a consulta? (exemplo: 15/06/2025)"
    
    elif estado_atual == ESTADOS['AGUARDANDO_DATA']:
        conversa['dados']['data'] = mensagem.strip()
        conversa['estado'] = ESTADOS['AGUARDANDO_PERIODO']
        resposta = f"Perfeito! Data: {mensagem.strip()} ✅\n\nQual período você prefere?\n• Digite 'manhã' para período da manhã\n• Digite 'tarde' para período da tarde"
    
    elif estado_atual == ESTADOS['AGUARDANDO_PERIODO']:
        periodo = mensagem.strip().lower()
        if periodo in ['manhã', 'manha', 'tarde']:
            conversa['dados']['periodo'] = periodo
            
            # Salva a consulta no banco de dados
            consulta_id = salvar_consulta(
                conversa['dados']['nome'],
                conversa['dados']['data'],
                conversa['dados']['periodo'],
                user_id
            )
            
            # Finaliza a conversa
            conversa['estado'] = ESTADOS['FINALIZADO']
            
            resposta = "🎉 Consulta marcada com sucesso!\n\n"
            resposta += "📋 **Resumo da sua consulta:**\n"
            resposta += f"👤 Nome: {conversa['dados']['nome']}\n"
            resposta += f"📅 Data: {conversa['dados']['data']}\n"
            resposta += f"⏰ Período: {conversa['dados']['periodo']}\n"
            resposta += f"🆔 ID da consulta: {consulta_id}\n\n"
            resposta += "✅ Sua consulta foi registrada no banco de dados! Para marcar uma nova consulta, digite 'nova' ou 'iniciar'."
        else:
            resposta = "Por favor, digite apenas 'manhã' ou 'tarde' para o período da consulta."
    
    elif estado_atual == ESTADOS['FINALIZADO']:
        if mensagem.strip().lower() in ['nova', 'iniciar', 'novo', 'começar']:
            # Reinicia a conversa
            conversa['estado'] = ESTADOS['INICIAL']
            conversa['dados'] = {}
            return processar_mensagem(user_id, mensagem)
        else:
            resposta = "Para marcar uma nova consulta, digite 'nova' ou 'iniciar'. 😊"
    
    else:
        resposta = "Desculpe, não entendi. Digite 'iniciar' para começar uma nova conversa."
    
    # Salva o estado da conversa e o histórico
    salvar_estado_conversa(user_id, conversa['estado'], conversa['dados'])
    salvar_historico(user_id, mensagem, resposta, conversa['estado'])
    
    return resposta

@app.route('/mensagem', methods=['POST'])
def mensagem():
    dados = request.json
    user_id = dados.get('user_id', 'default')
    mensagem_usuario = dados.get('mensagem', '')
    
    resposta = processar_mensagem(user_id, mensagem_usuario)
    
    return jsonify({
        'resposta': resposta,
        'user_id': user_id,
        'estado': conversas[user_id]['estado'] if user_id in conversas else ESTADOS['INICIAL']
    })

@app.route('/consultas', methods=['GET'])
def listar_consultas():
    """Lista todas as consultas do banco de dados"""
    consultas = obter_consultas()
    return jsonify(consultas)

@app.route('/consultas/<user_id>', methods=['GET'])
def consultas_usuario(user_id):
    """Lista consultas de um usuário específico"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, nome, data, periodo, data_criacao 
        FROM consultas 
        WHERE user_id = ?
        ORDER BY data_criacao DESC
    ''', (user_id,))
    
    consultas = []
    for row in cursor.fetchall():
        consultas.append({
            'id': row[0],
            'nome': row[1],
            'data': row[2],
            'periodo': row[3],
            'data_criacao': row[4]
        })
    
    conn.close()
    return jsonify(consultas)

@app.route('/historico/<user_id>', methods=['GET'])
def historico_conversa(user_id):
    """Obtém o histórico de conversas de um usuário"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT mensagem_usuario, resposta_bot, estado, timestamp 
        FROM historico_conversas 
        WHERE user_id = ?
        ORDER BY timestamp ASC
    ''', (user_id,))
    
    historico = []
    for row in cursor.fetchall():
        historico.append({
            'mensagem_usuario': row[0],
            'resposta_bot': row[1],
            'estado': row[2],
            'timestamp': row[3]
        })
    
    conn.close()
    return jsonify(historico)

@app.route('/conversa/status/<user_id>', methods=['GET'])
def status_conversa(user_id):
    """Endpoint para verificar o status da conversa de um usuário"""
    conversa = obter_estado_conversa(user_id)
    return jsonify({
        'user_id': user_id,
        'estado': conversa['estado'],
        'dados_coletados': conversa['dados']
    })

@app.route('/conversa/reiniciar/<user_id>', methods=['POST'])
def reiniciar_conversa(user_id):
    """Endpoint para reiniciar a conversa de um usuário"""
    if user_id in conversas:
        conversas[user_id] = {
            'estado': ESTADOS['INICIAL'],
            'dados': {}
        }
    
    # Remove do banco também
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM estados_conversa WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'mensagem': 'Conversa reiniciada com sucesso!'})

@app.route('/estatisticas', methods=['GET'])
def estatisticas():
    """Endpoint com estatísticas do sistema"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Total de consultas
    cursor.execute('SELECT COUNT(*) FROM consultas')
    total_consultas = cursor.fetchone()[0]
    
    # Consultas por período
    cursor.execute('SELECT periodo, COUNT(*) FROM consultas GROUP BY periodo')
    por_periodo = dict(cursor.fetchall())
    
    # Usuários únicos
    cursor.execute('SELECT COUNT(DISTINCT user_id) FROM consultas')
    usuarios_unicos = cursor.fetchone()[0]
    
    # Últimas consultas
    cursor.execute('''
        SELECT nome, data, periodo, data_criacao 
        FROM consultas 
        ORDER BY data_criacao DESC 
        LIMIT 5
    ''')
    ultimas_consultas = []
    for row in cursor.fetchall():
        ultimas_consultas.append({
            'nome': row[0],
            'data': row[1],
            'periodo': row[2],
            'data_criacao': row[3]
        })
    
    conn.close()
    
    return jsonify({
        'total_consultas': total_consultas,
        'consultas_por_periodo': por_periodo,
        'usuarios_unicos': usuarios_unicos,
        'ultimas_consultas': ultimas_consultas
    })

if __name__ == '__main__':
    # Inicializa o banco de dados
    init_database()
    print("💾 Banco de dados SQLite inicializado!")
    print("🚀 Servidor iniciando...")
    app.run(debug=True)
