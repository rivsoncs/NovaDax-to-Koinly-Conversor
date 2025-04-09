import argparse
import os
import sys
from .converter import convert_novadax_to_koinly
from .pdf_converter import novadax_pdf_to_csv

def main():
    parser = argparse.ArgumentParser(
        description='Conversor de relatórios da NovaDax para formato Koinly'
    )
    
    parser.add_argument(
        'input_file',
        help='Arquivo de entrada (CSV da NovaDax ou PDF)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Arquivo de saída (formato Koinly)',
        default=None
    )
    
    parser.add_argument(
        '--pdf',
        action='store_true',
        help='Força o processamento como PDF, mesmo se a extensão não for .pdf'
    )
    
    parser.add_argument(
        '--csv',
        action='store_true',
        help='Força o processamento como CSV, mesmo se a extensão não for .csv'
    )
    
    args = parser.parse_args()
    
    # Verifica se o arquivo de entrada existe
    if not os.path.isfile(args.input_file):
        print(f"Erro: Arquivo {args.input_file} não encontrado.")
        sys.exit(1)
    
    # Determina o tipo de arquivo
    file_ext = os.path.splitext(args.input_file)[1].lower()
    is_pdf = file_ext == '.pdf' or args.pdf
    is_csv = file_ext == '.csv' or args.csv
    
    if args.pdf and args.csv:
        print("Erro: Não é possível especificar --pdf e --csv ao mesmo tempo.")
        sys.exit(1)
    
    if not (is_pdf or is_csv):
        print(f"Erro: Tipo de arquivo não suportado: {file_ext}")
        print("Use arquivos .csv ou .pdf, ou especifique --pdf ou --csv.")
        sys.exit(1)
    
    # Define o arquivo de saída padrão se não for especificado
    if args.output is None:
        if is_pdf:
            # Para PDF, o padrão é salvar primeiro o CSV intermediário e depois o Koinly
            csv_output = os.path.splitext(args.input_file)[0] + "_extraido.csv"
            koinly_output = os.path.splitext(args.input_file)[0] + "_koinly.csv"
        else:
            # Para CSV, o padrão é salvar apenas o Koinly
            koinly_output = os.path.splitext(args.input_file)[0] + "_koinly.csv"
    else:
        # Se o usuário especificou o arquivo de saída
        if is_pdf:
            # Para PDF, o arquivo de saída é o CSV final (Koinly)
            csv_output = os.path.splitext(args.output)[0] + "_extraido.csv"
            koinly_output = args.output
        else:
            # Para CSV, o arquivo de saída é o Koinly
            koinly_output = args.output
    
    # Processa o arquivo
    if is_pdf:
        print(f"Processando PDF: {args.input_file}")
        result = novadax_pdf_to_csv(args.input_file, csv_output)
        print(f"Extraídas {result['total_rows']} transações para {csv_output}")
        
        print(f"Convertendo para formato Koinly: {csv_output}")
        result = convert_novadax_to_koinly(csv_output, koinly_output)
        print(f"Conversão concluída: {result['converted_rows']} transações convertidas para {koinly_output}")
    
    else:  # is_csv
        print(f"Convertendo CSV para formato Koinly: {args.input_file}")
        result = convert_novadax_to_koinly(args.input_file, koinly_output)
        print(f"Conversão concluída: {result['converted_rows']} transações convertidas para {koinly_output}")
    
    print("\nProcessamento concluído com sucesso!")

if __name__ == "__main__":
    main() 