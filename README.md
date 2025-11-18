# API para automação de OCR (Optical Character Recognition)

## 🎯 Objetivo

API para automatizar a realização de OCR em arquivos jpeg e png.

## 📦 Dependências Técnicas
- Python 3.12
- FastAPI
- Pillow
- pytesseract
- Tesseract OCR (instalação manual)

## ⚙️ Instalação e Configuração do Tesseract

### 1. Instalação
Baixe e instale o Tesseract OCR no Windows a partir do [UB Mannheim Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki).  
Instale no local padrão: C:\Program Files\Tesseract-OCR

### 2. Atualização das Variáveis de Ambiente
1. Abra **Configurações do Sistema → Variáveis de Ambiente**.
2. Edite a variável `Path` e adicione: C:\Program Files\Tesseract-OCR
3. Crie uma nova variável de sistema:
- Nome: `TESSDATA_PREFIX`
- Valor: `C:\Program Files\Tesseract-OCR`

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

## 🌐 Endpoints da API

Segue descrição de cada *endpoint* da API:

### 🔗 /ocr/texto

Recebe um arquivo e devolve o texto contido no arquivo.

### 🔗 /ocr/texto-arquivos
Recupera texto de vários arquivos compactados (.zip).


### 🔗 /ocr/pesquisa-texto
Pesquisa palavras em um arquivo e retorna quais estão presentes.


### 🔗 /ocr/pesquisa-texto-arquivos
Pesquisa palavras em vários arquivos compactados (.zip) e retorna quais arquivos têm quais palavras.


## Estrutura

```
template/
├── src/
│   ├── api/
│   │   └── main.py          # Endpoints da API
│   ├── models/
│   │   └── schemas.py       # Modelos Pydantic
│   └── config.py            # Configurações
├── tests/
│   └── test_template.py     # Testes automatizados
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

## 🔧 Customização

### Passo 1: Adapte os Schemas

Edite `src/models/schemas.py` com seus modelos de dados.

### Passo 2: Implemente sua Lógica

Edite `src/api/main.py` e substitua a lógica do endpoint `/calcular`.

### Passo 3: Crie Testes

Edite `tests/test_template.py` para testar sua lógica.

## Exemplo Atual

API de soma simples:
- **POST /calcular**: Soma dois números

Substitua isso pela sua lógica de negócio!


# Tasks
- [ ] 1. Separar endpoints de OCR do arquivo main.py
- [ ] 2.Endpoint 1 -> /ocr/texto
- [ ] 3.Endpoint 2 -> /ocr/texto-arquivos
- [ ] 4.Endpoint 3 -> /ocr/pesquisa-texto
- [ ] 5.Endpoint 4 -> Pesquisa palavras em vários arquivos compactados (.zip)
- [ ] 6. Validação endpoint 1
- [ ] 7. Validação endpoint 2
- [ ] 8. Validação endpoint 3
- [ ] 9. Validação endpoint 4
- [ ] 10. Criar log para a aplicação
- [ ] 11. Configurar CORS
- [ ] 12. Configurar variáveis de ambiente em arquivo separado
- [ ] 13. Finalizar README.md