# Conversor Novadax para Koinly

Este projeto oferece ferramentas para converter extratos da corretora **Novadax** para o formato CSV aceito pelo **Koinly**, facilitando a importação e análise das transações de compra, venda, taxas e saques.

## 🚀 Funcionalidades

- Conversão de extratos PDF da Novadax para CSV
- Conversão de extratos CSV da Novadax para o formato Koinly
- Suporte para diversos tipos de transações:
  - Compra e Venda
  - Convert (conversão entre criptomoedas)
  - Depósitos e Saques (em reais e criptomoedas)
  - Taxas de transação
  - Staking rewards
  - Airdrops

## 📋 Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas Python (listadas em `requirements.txt`):
  - pdfplumber (para extração de PDF)
  - outras bibliotecas padrão do Python

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor.git
cd NovaDax-to-Koinly-Conversor
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Convertendo PDF para CSV

1. Coloque seu extrato PDF da Novadax no diretório do projeto
2. Execute o script de conversão PDF para CSV:
```bash
python novadax_pdf_to_csv.py
```
3. O script irá gerar um arquivo `extrato_novadax.csv`

### Convertendo CSV para formato Koinly

1. Com o arquivo CSV da Novadax (seja gerado do PDF ou baixado diretamente), execute:
```bash
python converter_novadax_koinly.py
```
2. O script irá gerar um arquivo `novadax_koinly_custom.csv`

## 📊 Formato do CSV Koinly

O arquivo CSV gerado seguirá o formato exigido pelo Koinly com as seguintes colunas:
- Date (YYYY-MM-DD HH:MM UTC)
- Sent Amount
- Sent Currency
- Received Amount
- Received Currency
- Fee Amount
- Fee Currency
- Net Worth Amount
- Net Worth Currency
- Label
- Description
- TxHash

## 🔍 Logs e Depuração

O script gera um arquivo de log `converter_novadax_koinly.log` que contém informações detalhadas sobre o processamento de cada transação, incluindo:
- Transações processadas com sucesso
- Erros encontrados
- Detalhes sobre valores e moedas
- Resumo final da conversão

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Reportar bugs
2. Sugerir novas funcionalidades
3. Enviar pull requests

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✨ Agradecimentos

- À comunidade de usuários que contribuiu com feedback e sugestões
- Aos desenvolvedores das bibliotecas utilizadas no projeto
