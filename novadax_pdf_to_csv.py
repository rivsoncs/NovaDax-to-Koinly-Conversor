import pdfplumber
import csv
import unicodedata
import re

def normalize_text(text):
    """
    Normaliza texto removendo caracteres especiais e
    substituindo caracteres acentuados por suas versões sem acento.
    """
    if text is None:
        return ""
    
    # Normaliza os caracteres especiais
    normalized = unicodedata.normalize('NFKD', text)
    # Remove diacríticos (acentos)
    cleaned = ''.join(c for c in normalized if not unicodedata.combining(c))
    return cleaned

def is_table_header(row):
    """
    Verifica se a linha é um cabeçalho de tabela.
    Na Novadax os cabeçalhos típicos têm termos como 'Tipo', 'Moeda', 'Valor', 'Status'.
    """
    if not row or len(row) < 3:
        return False
    
    header_terms = ['tipo', 'moeda', 'valor', 'status', 'data', 'historytrades']
    row_text = ' '.join([str(cell).lower() for cell in row if cell is not None])
    
    # Verificar se pelo menos 2 termos de cabeçalho estão presentes
    matches = sum(1 for term in header_terms if term in row_text)
    return matches >= 2

def is_date_format(cell):
    """
    Verifica se o texto corresponde a um formato de data esperado.
    """
    if cell is None:
        return False
    return bool(re.search(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', str(cell)))

def is_valid_transaction_row(row):
    """
    Verifica se a linha é uma transação válida da tabela.
    """
    if not row or len(row) < 4:  # Precisa ter pelo menos data, tipo, moeda e valor
        return False
    
    # Verifica se começa com data válida (sem texto adicional)
    first_cell = str(row[0]).strip()
    if not is_date_format(first_cell) or len(first_cell) > 19:  # Data formato: DD/MM/YYYY HH:MM:SS
        return False
    
    # Verifica se não é um texto fora da tabela
    for cell in row:
        cell_text = str(cell).lower()
        if "historico:" in cell_text or "histórico:" in cell_text:
            return False
        
    return True

def join_broken_text(text1, text2):
    """
    Junta textos quebrados de forma inteligente.
    """
    if not text1 or not text2:
        return text1 or text2
        
    text1 = str(text1).strip()
    text2 = str(text2).strip()
    
    # Se o primeiro texto termina com hífen, remove-o antes de juntar
    if text1.endswith('-'):
        return text1[:-1] + text2
    
    # Para valores monetários e números
    if any(char.isdigit() for char in text1) and any(char.isdigit() for char in text2):
        # Remove qualquer parte de valor aproximado antes de juntar
        text1 = text1.rstrip('(≈R$')
        return text1 + text2
    
    # Para textos normais, junta com espaço se necessário
    if text1.endswith(' ') or text2.startswith(' '):
        return text1 + text2
    return text1 + ' ' + text2

def should_combine_rows(current_row, next_row):
    """
    Determina se duas linhas devem ser combinadas.
    """
    if not next_row or not any(str(cell).strip() for cell in next_row):
        return False
        
    # Se a próxima linha começa com data, é uma nova transação
    if next_row[0] and is_date_format(str(next_row[0]).strip()):
        return False
        
    # Se a próxima linha contém "Histórico:", não combinar
    if any("historico:" in str(cell).lower() for cell in next_row):
        return False
        
    # Se a linha atual está incompleta (tem menos células que o esperado)
    if len(current_row) < 5:
        return True
        
    # Se alguma célula da linha atual parece estar incompleta
    for i, cell in enumerate(current_row):
        cell_text = str(cell).strip().lower()
        if cell_text:
            # Verifica padrões comuns de texto quebrado
            if cell_text.endswith('-'):
                return True
            if "taxa de" in cell_text and i == 1:  # Coluna de tipo
                return True
            if any(cell_text.endswith(suffix) for suffix in ['(', '≈', '≈R$', '+']):
                return True
    
    return False

def combine_row_cells(current_text, next_text):
    """
    Combina duas células de texto de forma inteligente.
    """
    if not current_text or not next_text:
        return current_text or next_text
        
    current_text = str(current_text).strip()
    next_text = str(next_text).strip()
    
    # Se o texto atual está vazio
    if not current_text:
        return next_text
        
    # Se o texto atual termina com hífen
    if current_text.endswith('-'):
        return current_text[:-1] + next_text
        
    # Se é uma taxa de saque quebrada
    if "taxa de" in current_text.lower() and "saque" in next_text.lower():
        return current_text + " " + next_text
        
    # Se é um valor numérico quebrado
    if (any(c.isdigit() for c in current_text) and 
        any(c.isdigit() for c in next_text)):
        # Remove marcadores de valor aproximado se estiverem no final
        current_text = current_text.rstrip('(≈R$')
        # Se o próximo texto começa com parênteses ou ≈, adiciona espaço
        if next_text.startswith('(') or next_text.startswith('≈'):
            return current_text + ' ' + next_text
        return current_text + next_text
        
    # Para outros casos, adiciona espaço entre os textos
    return current_text + ' ' + next_text

def extract_complete_row(raw_rows, start_idx):
    """
    Extrai uma linha completa da tabela, combinando linhas quebradas.
    """
    if start_idx >= len(raw_rows):
        return None, start_idx
    
    current_row = list(raw_rows[start_idx])
    next_idx = start_idx + 1
    
    # Se não começa com data válida, pula
    if not (current_row and current_row[0] and is_date_format(str(current_row[0]).strip())):
        return None, start_idx + 1
    
    # Enquanto houver linhas para combinar
    while next_idx < len(raw_rows) and should_combine_rows(current_row, raw_rows[next_idx]):
        next_row = raw_rows[next_idx]
        
        # Combina as células
        for i in range(min(len(current_row), len(next_row))):
            if next_row[i] and str(next_row[i]).strip():
                current_row[i] = combine_row_cells(current_row[i], next_row[i])
        
        # Se a próxima linha tem mais células, adiciona as extras
        if len(next_row) > len(current_row):
            current_row.extend(next_row[len(current_row):])
        
        next_idx += 1
    
    return current_row, next_idx

def clean_value(value):
    """
    Limpa e normaliza um valor específico, mantendo a estrutura de números grandes
    e valores aproximados em reais.
    """
    if value is None or str(value).strip() == "":
        return ""
    
    value = str(value).strip()
    
    # Remove espaços extras entre números e vírgulas
    value = re.sub(r'(\d)\s+([,.])', r'\1\2', value)
    value = re.sub(r'([,.])\s+(\d)', r'\1\2', value)
    
    # Remove quebras de linha
    value = value.replace('\n', ' ').replace('\r', '')
    
    # Junta partes separadas de valores com parênteses
    value = re.sub(r'\(\s+', '(', value)
    value = re.sub(r'\s+\)', ')', value)
    
    # Remove espaços extras
    value = ' '.join(value.split())
    
    return value

def clean_table_row(row):
    """
    Limpa e normaliza uma linha de tabela.
    """
    cleaned_row = []
    for i, cell in enumerate(row):
        if cell is None:
            cleaned_row.append("")
            continue
            
        cell_text = str(cell).strip()
        
        # Remove qualquer texto de histórico da data
        if i == 0 and "historico:" in cell_text.lower():
            cell_text = cell_text.split("historico:")[0].strip()
        
        # Limpa valores numéricos e monetários
        if any(char in cell_text for char in '0123456789R$'):
            cleaned_value = clean_value(cell_text)
        else:
            cleaned_value = normalize_text(cell_text)
            
            # Correções específicas para tipos comuns
            if i == 1:  # Coluna de tipo
                if "taxa de saque" in cleaned_value.lower():
                    cleaned_value = "Taxa de saque de criptomoedas"
                elif "taxa de transacao" in cleaned_value.lower():
                    cleaned_value = "Taxa de transacao"
        
        cleaned_row.append(cleaned_value)
    
    return cleaned_row

def novadax_pdf_to_csv(pdf_path="novadax.pdf", csv_path="extrato_novadax.csv"):
    """
    Extrai tabelas do PDF da Novadax e salva em CSV.
    """
    with pdfplumber.open(pdf_path) as pdf:
        all_raw_rows = []
        
        for i, page in enumerate(pdf.pages):
            print(f"Processando página {i+1} de {len(pdf.pages)}...")
            tables = page.extract_tables()
            
            for table in tables:
                # Filtra linhas vazias e linhas de histórico
                for row in table:
                    if row and any(cell is not None and str(cell).strip() != "" for cell in row):
                        # Ignora explicitamente linhas com "Histórico:"
                        if not any("historico:" in str(cell).lower() for cell in row):
                            all_raw_rows.append(row)
        
        print("Combinando linhas quebradas...")
        
        # Processa as linhas
        transactions = []
        idx = 0
        while idx < len(all_raw_rows):
            row, next_idx = extract_complete_row(all_raw_rows, idx)
            if row and is_date_format(row[0]):  # Garante que só aceita linhas que começam com data
                cleaned_row = clean_table_row(row)
                if len(cleaned_row) >= 4:  # Garante que tem pelo menos data, tipo, moeda e valor
                    transactions.append(cleaned_row)
            idx = next_idx
        
        # Define o cabeçalho
        header = ["Data", "Tipo", "Moeda", "Valor", "Status"]
        
        # Cria o CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            
            for row in transactions:
                # Ajusta o número de colunas
                while len(row) < len(header):
                    row.append("")
                writer.writerow(row[:len(header)])
        
        print(f"Extração concluída! Arquivo CSV salvo em: {csv_path}")
        print(f"Total de transações extraídas: {len(transactions)}")


if __name__ == "__main__":
    # Exemplo de uso básico
    novadax_pdf_to_csv()
    
    # Para usar com caminhos diferentes, descomente e ajuste:
    # novadax_pdf_to_csv(pdf_path="meu_extrato.pdf", csv_path="resultado.csv") 