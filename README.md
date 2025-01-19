# 🥷 DevSamurai Download 

### 📃 __Obejtivo:__
Recentemente foi anunciado que a plataforma de ensino 'DevSamurai' está encerrando suas atividades e com isso liberaram para download varios cursos de diferentes assuntos, esse projeto tem o intuito de ser um facilitador para baixar os arquivos disponiveis. 

[__Comunicado Oficial__](https://class.devsamurai.com.br/)

### 📺 __Demo:__
![](assets/clip.gif)

---
### 📒 __Metodologia:__
Foi usado um método de download assincrono utilizando os protocolos HTTP/2 e HTTP/3 via chucks para processamento dos bytes em pequenos lotes

---
### 💻 __Stack:__
- Python 3.12
- httpx (HTTP/2)
- niquests (HTTP/3)
- aiofiles (async save bytes)
- rich (show progress bar)
- csv (persist data)
- asyncio (run event loop)
- ruff (formater and linter)
- uv (dependency manager)

---
### ⚡ __Como instalar o projeto:__

usando uv
```bash
git clone https://github.com/Gpocas/devsamurai.git
cd devsamurai
uv sync
```

usando python puro
```bash
git clone https://github.com/Gpocas/devsamurai.git
cd devsamurai
python -m venv .venv 
source .venv/bin/activate
python install -r requirements.txt
```

> [!NOTE]  
> Os comandos mostrados acima se referem a um ambiente linux e bash

---
### 🚀 __Como rodar o projeto:__

usando uv
```bash
uv run task start
```

usando python puro
```bash
source .venv/bin/activate
task start
```
> [!NOTE]  
> Os comandos mostrados acima se referem a um ambiente linux e bash

---
### 🔍 __Observações:__

- Existe algumas variaveis de ambiente que podem ser configuradas
    - `CSV_PATH` o caminho onde está localizado seu arquivo csv
    - `DOWNLOAD_PATH` a pasta onde deverá ser salvos os arquivos baixados
    - `PARALLEL_DOWNLOADS` a quantidade de arquivos simultaneos que serão baixados

> [!IMPORTANT]  
> Não existe um minimo ou um máximo para a configuração de `PARALLEL_DOWNLOADS`, porém vale lembrar que valores altos vão aumentar o tempo de conexão com o servidor o que pode ocasionar no encerramento da stream por parte do servidor. 

- Na pasta `data/aulas.csv` contem todos os links já extraidos e higienizados para facilitar o processo, porém caso voce queira pode gerar esse arquivo voce mesmo execuntando:

usando uv:
```bash
uv run devsamurai/utils/extract.py
```

usando python puro:
```bash
python devsamurai/utils/extract.py
```


 
