from datetime import datetime

def log(msg):
    """Registra uma mensagem no console e em um arquivo de log."""
    linha = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(linha)
    with open('app.log', 'a', encoding='utf-8') as f:
        f.write(linha + '\n')
