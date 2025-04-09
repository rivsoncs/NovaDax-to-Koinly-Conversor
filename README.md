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
- Instalação simplificada com comando único (`nova2k`)

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
  - ✅ Staking rewards e Bônus
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

### Método 1: Instalação via pip (recomendado)

```bash
# Na pasta do projeto
pip install .
```

Após a instalação, você terá dois comandos disponíveis:
- `nova2k` (versão simplificada)
- `novadax-koinly` (nome completo)

Ambos funcionam da mesma forma, mas `nova2k` é mais rápido de digitar!

### Método 2: Clonando o repositório

```bash
# Clone o repositório
git clone https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor.git

# Navegue até a pasta
cd NovaDax-to-Koinly-Conversor

# Instale o pacote
pip install .
```

### Método 3: Instalação direta do GitHub (sem clonar)

```bash
# Instale diretamente do GitHub
pip install git+https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor.git
```

### Como desinstalar

Se precisar remover o conversor, use o pip para desinstalar:

```bash
pip uninstall novadax-koinly
```

### Como atualizar

Para atualizar para a versão mais recente:

```bash
# Se instalou do GitHub
pip install --upgrade git+https://github.com/rivsoncs/NovaDax-to-Koinly-Conversor.git

# Se você clonou o repositório
cd NovaDax-to-Koinly-Conversor
git pull
pip install --upgrade .
```

## 📖 Como Usar

### Forma simplificada (recomendada)

Após instalar o pacote, use o comando `nova2k` seguido do nome do arquivo:

```bash
# Para converter um PDF
nova2k meu_extrato.pdf

# Para converter um CSV
nova2k novadax.csv

# Com opções personalizadas
nova2k meu_extrato.pdf -o resultado_koinly.csv
```

### Forma completa

Se preferir, você também pode usar o comando completo:

```bash
# Para converter um PDF
novadax-koinly meu_extrato.pdf -o resultado_koinly.csv

# Para converter um CSV
novadax-koinly novadax.csv -o resultado_koinly.csv
```

### Opções disponíveis

```
nova2k [-h] [-o OUTPUT] [--pdf] [--csv] input_file

Conversor de relatórios da NovaDax para formato Koinly

Argumentos posicionais:
  input_file            Arquivo de entrada (CSV da NovaDax ou PDF)

Argumentos opcionais:
  -h, --help            Exibe esta mensagem de ajuda
  -o OUTPUT, --output OUTPUT
                        Arquivo de saída (formato Koinly)
  --pdf                 Força o processamento como PDF
  --csv                 Força o processamento como CSV
```

### Usando os scripts manualmente

Se preferir, você ainda pode usar os scripts diretamente:

```bash
# Para extrair CSV de um PDF
python novadax_pdf_to_csv.py

# Para converter CSV para formato Koinly
python converter_novadax_koinly.py
```

## 🔄 Como funciona a conversão

O conversor detecta automaticamente o tipo de arquivo pela extensão e executa o fluxo apropriado:

### Para arquivos PDF:
1. **Extração do PDF**: O conversor analisa o PDF e extrai as tabelas de transações
2. **Geração de CSV intermediário**: Cria um arquivo CSV com os dados brutos extraídos
3. **Conversão para Koinly**: Transforma os dados no formato compatível com Koinly
4. **Arquivo final**: Gera o arquivo CSV pronto para importação no Koinly

### Para arquivos CSV:
1. **Leitura do CSV**: Lê diretamente o arquivo CSV da NovaDax
2. **Conversão para Koinly**: Transforma os dados no formato compatível com Koinly
3. **Arquivo final**: Gera o arquivo CSV pronto para importação no Koinly

### Processamento de transações:
- Cada linha do extrato é analisada individualmente
- O tipo de transação é identificado (compra, venda, depósito, etc.)
- Os valores são convertidos para o formato adequado
- As taxas de transação são associadas às operações correspondentes
- Transações de bônus e staking são marcadas como "reward"

Tudo isso é feito automaticamente com um único comando. O usuário não precisa se preocupar com qual script chamar ou qual sequência de passos seguir - o `nova2k` cuida de tudo!

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
- Verifique se o PDF foi gerado corretamente pela NovaDax
- Certifique-se de que a biblioteca pdfplumber está instalada corretamente

### Valores incorretos no CSV final
- Verifique o arquivo de log para identificar problemas
- Confirme se o PDF/CSV original está no formato esperado
- Compare os valores manualmente com o extrato original

### Erros ao executar o comando `nova2k`
- Verifique se o pacote foi instalado corretamente
- Tente reinstalar usando `pip install --force-reinstall .`
- Verifique se você está usando Python 3.6 ou superior

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
