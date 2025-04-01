# 📊 Conversor Novadax para Koinly

Este projeto facilita a importação de transações da Novadax para o Koinly, uma plataforma de rastreamento de criptomoedas e geração de relatórios fiscais.

## 📝 Histórico e Evolução

### Versão Original (1.0)
- Suportava apenas arquivos CSV baixados diretamente da Novadax
- Conversão básica de transações para o formato Koinly
- Tratamento limitado de tipos de transações

### Versão Atual (2.0)
- **Nova funcionalidade**: Extração direta de PDFs da Novadax
- Suporte aprimorado para diversos tipos de transações
- Sistema de logs para rastreamento de problemas
- Tratamento inteligente de transações complexas

## 🚀 Funcionalidades

### Extração de PDF
- Converte extratos em PDF da Novadax para CSV
- Preserva toda a estrutura e dados das transações
- Trata corretamente tabelas em múltiplas páginas

### Conversão para Koinly
- Suporta todos os tipos de transações:
  - ✅ Compra e Venda
  - ✅ Convert (conversão entre criptomoedas)
  - ✅ Depósitos e Saques (em reais e criptomoedas)
  - ✅ Taxas de transação
  - ✅ Staking rewards
  - ✅ Airdrops

## 📋 Pré-requisitos

1. **Python**: Versão 3.6 ou superior
   - Para verificar se você tem o Python instalado, abra o terminal (ou prompt de comando) e digite:
     ```bash
     python --version
     ```
   - Se não tiver o Python, baixe em: https://www.python.org/downloads/

2. **Git** (opcional, apenas se quiser clonar o repositório):
   - Windows: https://git-scm.com/download/win
   - Mac: `brew install git`
   - Linux: `sudo apt-get install git`

## 🛠️ Instalação

### Método 1: Download Direto (Mais fácil)
1. Clique no botão verde "Code" acima
2. Selecione "Download ZIP"
3. Extraia o arquivo ZIP para uma pasta de sua preferência

### Método 2: Usando Git
```bash
git clone https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor.git
cd NovaDax-to-Koinly-Conversor
```

### Instalando Dependências
Abra o terminal (ou prompt de comando), navegue até a pasta do projeto e execute:
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### 1. Convertendo PDF para CSV
1. Coloque seu extrato PDF da Novadax na mesma pasta do projeto
2. Renomeie o arquivo para `novadax.pdf`
3. Abra o terminal na pasta do projeto e execute:
   ```bash
   python novadax_pdf_to_csv.py
   ```
4. Será gerado um arquivo `extrato_novadax.csv`

### 2. Convertendo CSV para formato Koinly
1. Se você já tem o CSV da Novadax (seja gerado do PDF ou baixado do site):
   - Renomeie para `novadax.csv` e coloque na pasta do projeto
2. Execute:
   ```bash
   python converter_novadax_koinly.py
   ```
3. Será gerado um arquivo `novadax_koinly_custom.csv`

### 3. Importando no Koinly
1. Acesse sua conta no Koinly
2. Vá em "Wallets" → "Add Wallet" → "Import from File"
3. Selecione o arquivo `novadax_koinly_custom.csv` gerado

## 🔍 Logs e Depuração

O script gera um arquivo `converter_novadax_koinly.log` que contém informações detalhadas sobre o processamento:
- Transações processadas
- Erros encontrados
- Valores e moedas
- Resumo da conversão

Se encontrar algum problema:
1. Verifique o arquivo de log
2. Compare os valores no CSV gerado com o extrato original
3. [Abra uma issue](https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor/issues) se precisar de ajuda

## ❓ Solução de Problemas

### Erro ao instalar dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Arquivo PDF não é reconhecido
- Certifique-se de que o PDF não está protegido por senha
- Verifique se o nome do arquivo está correto: `novadax.pdf`
- Confirme que o arquivo está na mesma pasta do script

### Valores incorretos no CSV final
- Verifique o arquivo de log para identificar problemas
- Confirme se o PDF/CSV original está no formato esperado
- Compare os valores manualmente com o extrato original

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você encontrou um bug ou tem uma sugestão:
1. [Abra uma issue](https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor/issues)
2. Faça um fork do projeto
3. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
4. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
5. Push para a branch (`git push origin feature/MinhaFeature`)
6. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✨ Agradecimentos

- À comunidade de usuários que contribuiu com feedback
- Aos desenvolvedores das bibliotecas utilizadas
- A todos que ajudaram a testar e melhorar o projeto

## 📬 Contato

Se você encontrou algum problema ou tem sugestões, por favor:
1. Abra uma [issue](https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor/issues)
2. Envie um pull request
3. Entre em contato através das issues do GitHub
