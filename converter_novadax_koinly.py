import csv
from datetime import datetime
import re
import unicodedata
import logging
from typing import List, Optional

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('converter_novadax_koinly.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def normalize_str(s: str) -> str:
    """
    Remove acentos e caracteres especiais, retornando texto em ascii basico,
    tudo em minúsculo, p/ facilitar comparação.
    """
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()

def convert_date(novadax_date: str) -> str:
    """
    Converte data/hora do formato 'DD/MM/YYYY HH:MM:SS' para 'YYYY-MM-DD HH:MM UTC'.
    Se falhar, retorna 'Invalid Date'.
    """
    try:
        dt = datetime.strptime(novadax_date, "%d/%m/%Y %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except ValueError:
        return "Invalid Date"

def extract_numeric_value(text: str) -> str:
    """
    Extrai o primeiro número (podendo ter sinal + ou -), remove separadores de milhar,
    converte vírgula em ponto decimal, sem arredondar.
    Se não encontrar nenhum número, retorna string vazia.
    """
    # Remove o trecho '(≈R$...)' que confunde a extração
    temp = re.sub(r'\(≈R\\$[^)]*\)', '', text)

    # Localiza todos os números (c/ ou s/ sinal)
    matches = re.findall(r'[+-]?\s*\d[\d.,]*', temp)
    if not matches:
        return ""  # Nenhum número encontrado

    # Por padrão, pega o PRIMEIRO número
    raw_val = matches[0]

    # Remove espaços internos: '- 1,234' -> '-1,234'
    raw_val = re.sub(r'\s+', '', raw_val)

    # Troca vírgula decimal por ponto
    raw_val = raw_val.replace(',', '.')

    # Se houver mais de um ponto, pode ser separador de milhar
    parts = raw_val.split('.')
    if len(parts) > 2:
        # Último item = parte decimal, o resto = milhar
        decimal_part = parts[-1]
        thousand_parts = parts[:-1]
        raw_val = ''.join(thousand_parts) + '.' + decimal_part

    return raw_val

def extract_trading_pair(tipo_str: str) -> tuple:
    """
    Extrai o par de trading de strings como 'Compra(BTC/BRL)' ou 'Venda(ETH/BRL)'.
    Retorna uma tupla (moeda_base, moeda_cotacao).
    """
    match = re.search(r'\(([A-Z0-9]+)/([A-Z0-9]+)\)', tipo_str.upper())
    if match:
        return match.group(1), match.group(2)
    return None, None

def log_transaction(row: List[str], koinly_row: List[str], error: Optional[str] = None) -> None:
    """
    Registra informações sobre o processamento de uma transação.
    """
    if len(row) >= 5:
        data, tipo, moeda, valor, status = row[:5]
        if error:
            logging.warning(f"ERRO - Data: {data}, Tipo: {tipo}, Moeda: {moeda}, Valor: {valor}, Status: {status}")
            logging.warning(f"Detalhes do erro: {error}")
        else:
            sent = f"{koinly_row[1]} {koinly_row[2]}" if koinly_row[1] else "nada"
            received = f"{koinly_row[3]} {koinly_row[4]}" if koinly_row[3] else "nada"
            fee = f"{koinly_row[5]} {koinly_row[6]}" if koinly_row[5] else "sem taxa"
            
            logging.info(f"Processado - Data: {data}, Tipo: {tipo}")
            logging.info(f"-> Enviado: {sent}, Recebido: {received}, Taxa: {fee}, Label: {koinly_row[9]}")
    else:
        logging.error(f"Linha inválida (menos de 5 campos): {row}")

def process_novadax_row(row):
    """
    Converte uma linha do CSV da Novadax em uma linha do CSV no padrão Koinly,
    mantendo campos vazios quando não há dados.
    """
    if len(row) < 5:
        error_msg = f"Linha com formato inválido (menos de 5 campos): {row}"
        logging.error(error_msg)
        return ["Invalid Row"] * 12

    data_str, tipo_str, moeda, valor_str, status = row[:5]

    # Converte data
    date = convert_date(data_str)
    if date == "Invalid Date":
        error_msg = f"Data inválida: {data_str}"
        logging.error(error_msg)

    # Normaliza o texto de tipo p/ facilitar comparação (remove acentos, lowercase)
    tipo_normalizado = normalize_str(tipo_str)

    # Extrai valor numérico principal
    valor = extract_numeric_value(valor_str)
    if not valor:
        logging.warning(f"Valor não encontrado em: {valor_str}")

    # Inicializa campos do Koinly
    sent_amount = ""
    sent_currency = ""
    received_amount = ""
    received_currency = ""
    fee_amount = ""
    fee_currency = ""
    label = ""
    description = tipo_str  # Texto original na descrição

    # Extrai par de trading se existir
    moeda_base, moeda_cotacao = extract_trading_pair(tipo_str)

    # Verifica qual tipo de operação
    if "taxa de transacao" in tipo_normalizado:
        fee_amount = valor
        fee_currency = moeda
        label = "fee"
    elif "taxa de saque" in tipo_normalizado:
        fee_amount = valor
        fee_currency = moeda
        label = "withdrawal-fee"
    elif "deposito em reais" in tipo_normalizado:
        received_amount = valor.lstrip("+")
        received_currency = moeda
        label = "deposit"
    elif "saque em reais" in tipo_normalizado:
        sent_amount = valor.lstrip("-")
        sent_currency = moeda
        label = "withdrawal"
    elif "deposito de criptomoedas" in tipo_normalizado:
        received_amount = valor.lstrip("+")
        received_currency = moeda
        label = "deposit"
    elif "redeemed bonus" in tipo_normalizado or "staking" in tipo_normalizado:
        received_amount = valor.lstrip("+")
        received_currency = moeda
        label = "reward"
    elif "airdrop" in tipo_normalizado:
        received_amount = valor.lstrip("+")
        received_currency = moeda
        label = "airdrop"
    elif "convert" in tipo_normalizado or "troca" in tipo_normalizado:
        # Para conversão/troca, o valor negativo é o sent e o positivo é o received
        if valor.startswith("-"):
            sent_amount = valor.lstrip("-")
            sent_currency = moeda
        else:
            received_amount = valor.lstrip("+")
            received_currency = moeda
        label = "trade"
    elif "compra" in tipo_normalizado:
        # Se temos o par de trading, usamos ele para determinar a direção
        if moeda_base and moeda_cotacao:
            if moeda == moeda_cotacao:
                sent_amount = valor.lstrip("-")
                sent_currency = moeda_cotacao
            else:
                received_amount = valor.lstrip("+")
                received_currency = moeda_base
        else:
            # Fallback para o comportamento anterior
            if moeda.upper() == "BRL":
                sent_amount = valor.lstrip("-")
                sent_currency = "BRL"
            else:
                received_amount = valor.lstrip("+")
                received_currency = moeda
        label = "buy"
    elif "venda" in tipo_normalizado:
        # Se temos o par de trading, usamos ele para determinar a direção
        if moeda_base and moeda_cotacao:
            if moeda == moeda_cotacao:
                received_amount = valor.lstrip("+")
                received_currency = moeda_cotacao
            else:
                sent_amount = valor.lstrip("-")
                sent_currency = moeda_base
        else:
            # Fallback para o comportamento anterior
            if moeda.upper() == "BRL":
                received_amount = valor.lstrip("+")
                received_currency = "BRL"
            else:
                sent_amount = valor.lstrip("-")
                sent_currency = moeda
        label = "sell"
    elif "saque de criptomoedas" in tipo_normalizado:
        sent_amount = valor.lstrip("-")
        sent_currency = moeda
        label = "withdrawal"

    # Limpa os valores (remove + ou - do início)
    if sent_amount:
        sent_amount = sent_amount.lstrip("+-")
    if received_amount:
        received_amount = received_amount.lstrip("+-")
    if fee_amount:
        fee_amount = fee_amount.lstrip("+-")

    # Retorna a linha no formato do Koinly
    koinly_row = [
        date,
        sent_amount,
        sent_currency,
        received_amount,
        received_currency,
        fee_amount,
        fee_currency,
        "",  # Net Worth Amount
        "",  # Net Worth Currency
        label,
        description,
        "",  # TxHash
    ]

    # Verifica se os campos essenciais estão preenchidos
    if not label:
        logging.warning(f"Tipo de transação não identificado: {tipo_str}")
    if not (sent_amount or received_amount):
        logging.warning(f"Nenhum valor de envio ou recebimento encontrado para: {tipo_str}")

    return koinly_row

def convert_novadax_to_koinly(input_file, output_file):
    """
    Lê o CSV da Novadax (input_file) e gera um CSV no formato Koinly (output_file).
    """
    logging.info(f"Iniciando conversão de {input_file} para {output_file}")
    
    total_rows = 0
    converted_rows = 0
    error_rows = 0
    
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Cabeçalho Koinly
        writer.writerow([
            "Date", "Sent Amount", "Sent Currency",
            "Received Amount", "Received Currency",
            "Fee Amount", "Fee Currency",
            "Net Worth Amount", "Net Worth Currency",
            "Label", "Description", "TxHash"
        ])

        # Pula a linha de cabeçalho do CSV da Novadax
        next(reader, None)

        # Buffer para armazenar transações relacionadas
        current_convert = None
        convert_fee = None
        
        for row in reader:
            total_rows += 1
            
            if len(row) < 5:
                error_rows += 1
                logging.error(f"Linha {total_rows}: formato inválido (menos de 5 campos)")
                continue
                
            data_str, tipo_str, moeda, valor_str, status = row[:5]
            tipo_normalizado = normalize_str(tipo_str)
            
            try:
                # Se é uma taxa de Convert
                if "taxa de convert" in tipo_normalizado:
                    convert_fee = {
                        'amount': extract_numeric_value(valor_str).lstrip("-"),
                        'currency': moeda,
                        'date': data_str
                    }
                    logging.info(f"Taxa de Convert encontrada: {convert_fee['amount']} {convert_fee['currency']}")
                    continue

                # Se é uma operação Convert
                if "convert" in tipo_normalizado:
                    if current_convert is None:
                        # Primeira parte do Convert
                        current_convert = process_novadax_row(row)
                        current_convert[10] = tipo_str  # Mantém a descrição original
                        
                        # Se tiver uma taxa de Convert pendente da mesma data, aplica
                        if convert_fee and convert_fee['date'] == data_str:
                            current_convert[5] = convert_fee['amount']
                            current_convert[6] = convert_fee['currency']
                            logging.info(f"Taxa aplicada ao Convert: {convert_fee['amount']} {convert_fee['currency']}")
                            convert_fee = None
                    else:
                        # Segunda parte do Convert - complementa a transação
                        valor = extract_numeric_value(valor_str)
                        if valor.startswith("-"):
                            current_convert[1] = valor.lstrip("-")
                            current_convert[2] = moeda
                        else:
                            current_convert[3] = valor.lstrip("+")
                            current_convert[4] = moeda
                        
                        # Escreve a transação Convert completa
                        writer.writerow(current_convert)
                        log_transaction(row, current_convert)
                        converted_rows += 1
                        current_convert = None
                else:
                    # Para outras operações (não Convert), processa normalmente
                    if current_convert:
                        # Se havia um Convert incompleto, escreve ele antes
                        writer.writerow(current_convert)
                        log_transaction(row, current_convert)
                        converted_rows += 1
                        current_convert = None
                    
                    row_data = process_novadax_row(row)
                    writer.writerow(row_data)
                    log_transaction(row, row_data)
                    converted_rows += 1
                    
            except Exception as e:
                error_rows += 1
                logging.error(f"Erro ao processar linha {total_rows}: {str(e)}")
                logging.error(f"Conteúdo da linha: {row}")
        
        # Se sobrou algum Convert incompleto
        if current_convert:
            writer.writerow(current_convert)
            converted_rows += 1
    
    logging.info(f"\nResumo da conversão:")
    logging.info(f"Total de linhas processadas: {total_rows}")
    logging.info(f"Linhas convertidas com sucesso: {converted_rows}")
    logging.info(f"Linhas com erro: {error_rows}")
    logging.info(f"Arquivo convertido salvo em: {output_file}")

if __name__ == "__main__":
    input_file = "novadax.csv"
    output_file = "novadax_koinly_custom.csv"
    convert_novadax_to_koinly(input_file, output_file)
