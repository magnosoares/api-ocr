# API para automação de OCR (Optical Character Recognition)

## 🎯 Objetivo

API para automatizar a realização de OCR em arquivos jpeg e png.

## 🏆 Equipe de Desenvolvimento/Projeto
- Magno Santana Soares
- Lucia Helena Dutra Magalhães
- Thiago Lobo Leite
- Tiago André da Silveira Fialho 

## 📦 Dependências Técnicas
- Python 3.12
- FastAPI
- Pillow
- pytesseract
- Tesseract OCR (instalação manual)
- Poppler (instalação manual)
- pdf2image

## ⚙️ Instalação e Configuração do Tesseract

### 1. Instalação
Baixe e instale o Tesseract OCR no Windows a partir do [UB Mannheim Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki).  
Instale no local padrão: C:\Program Files\Tesseract-OCR

### 2. Atualização das Variáveis de Ambiente
1. Abra **Configurações do Sistema → Variáveis de Ambiente**.
2. Edite a variável `Path` e adicione: C:\Program Files\Tesseract-OCR
3. Crie uma nova variável de sistema:
- Nome: `TESSDATA_PREFIX`
- Valor: `C:\Program Files\Tesseract-OCR\tessdata`

### 3. Download dos Pacotes de Idioma
Os pacotes de idioma podem ser obtidos no repositório oficial:  
👉 [Tesseract tessdata](https://github.com/tesseract-ocr/tessdata)

Baixe os arquivos `.traineddata` correspondentes a:
- **Português** → `por.traineddata`
- **Inglês** → `eng.traineddata`
- **Espanhol** → `spa.traineddata`
- **Francês** → `fra.traineddata`

### 4. Cópia dos Pacotes para o Tessdata
Copie os arquivos baixados para a pasta: C:\Program Files\Tesseract-OCR\tessdata

### 5. Verificação
No terminal, execute:
```bash
tesseract --list-langs
```

A saída deve listar os idiomas instalados, por exemplo:

```bash
List of available languages in "C:\Program Files\Tesseract-OCR/" (4):
tessdata\eng
tessdata\fra
tessdata\por
tessdata\spa
```

## ⚙️ Instalação e Configuração do Poppler (necessário para utilização do pacote pdf2image)

### 1. Instalação
Baixe o [Poppler](https://github.com/conda-forge/poppler-feedstock) para Windows a partir do [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows).  
Extraia o conteúdo do pacote em um diretório de sua escolha. Ex.: C:\poppler

### 2. Atualização das Variáveis de Ambiente
1. Abra **Configurações do Sistema → Variáveis de Ambiente**.
2. Edite a variável `Path` e adicione o caminho para o diretório Library\bin do Poppler. Ex.: C:\poppler\poppler-25.11.0\Library\bin

## 🌐 Endpoints da API

Segue descrição de cada *endpoint* da API:

### 🔗 /recognition/img-file

Recebe um arquivo com uma imagem (jpeg ou png) e devolve o texto contido no arquivo.


### 🔗 /recognition/zip-files
Recupera texto de vários arquivos compactados (.zip).


### 🔗 /recognition/pdf-file
Recupera texto de arquivo pdf.


### 🔗 /search/img-file
Pesquisa palavras em um arquivo de imagem (jpeg ou png) e retorna quais estão presentes.


### 🔗 /search/zip-files
Pesquisa palavras em vários arquivos compactados (.zip) e retorna quais arquivos contém quais palavras.


## Estrutura

```
template/
├── src/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── about.py        # Endpoints da rota about
│   │   │   ├── health.py       # Endpoints da rota health
│   │   │   ├── recognition.py  # Endpoints da rota recognition
│   │   │   └── search.py       # Endpoints da rota search
│   │   └── main.py             # Criação da API e configuração das rotas
│   ├── models/
│   │   └── schemas.py          # Modelos Pydantic
│   └── config.py               # Configurações
├── services/
│   └── ocr_service.py          # Serviço para execução do OCR
├── tests/
│   └── test_template.py        # Testes automatizados
├── requirements.txt
└── .gitignore
```

## Como Usar

```bash
pip install -r requirements.txt
```

### 2. Rodar a API

```bash
uvicorn src.api.main:app --reload
```

### 3. Acessar documentação

http://localhost:8000/docs

### 4. Rodar testes

```bash
pytest tests/ -v
```

## 🛠️ TO-DO List
- [X] 1. Separar endpoints de OCR do arquivo main.py
- [X] 2. Configurar CORS
- [X] 3. Configurar variáveis de ambiente em arquivo separado
- [X] 4. Endpoint 1 -> /recognition/img-file
  - [X] 4.1 Validação pydantic para endpoint 1
  - [X] 4.2 Implementar testes para endpoint 1
  - [X] 4.3 Implementar logs para o endpoint 1
- [X] 5. Endpoint 2 -> /recognition/zip-files
  - [X] 5.1 Validação pydantic para endpoint 2
  - [X] 5.2 Implementar testes para endpoint 2
  - [X] 5.3 Implementar logs para o endpoint 2
- [X] 6. Endpoint 3 -> /recognition/pdf-file
  - [X] 6.1 Validação pydantic para endpoint 3
  - [X] 6.2 Implementar testes para endpoint 3
  - [X] 6.3 Implementar logs para o endpoint 3
- [X] 7. Endpoint 4 -> /search/img-file
  - [X] 7.1 Validação pydantic para endpoint 4
  - [X] 7.2 Implementar testes para endpoint 4
  - [X] 7.3 Implementar logs para o endpoint 4
- [X] 8. Endpoint 5 -> /search/zip-files
  - [X] 8.1 Validação pydantic para endpoint 5
  - [X] 8.2 Implementar testes para endpoint 5
  - [X] 8.3 Implementar logs para o endpoint 5
- [X] 9. Criar log para a aplicação
- [X] 10. Alterar visualização dos logs: escrita em arquivo
- [X] 10. Finalizar README.md
