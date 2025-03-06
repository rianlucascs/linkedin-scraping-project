![linkedin](https://www.edigitalagency.com.au/wp-content/uploads/Linkedin-logo-blue-png-medium-size.png) 


# LINKEDIN SCRAPING PROJECT

Este projeto tem como objetivo realizar o scraping de vagas do LinkedIn com base em um cargo específico.

## Como usar

### Tenha o projeto na sua máquina

1. Clone o repositório:
   ```bash
   git clone https://github.com/rianlucascs/linkedin-scraping-project.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd linkedin-scraping-project
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o arquivo:
   ```bash
   python extracetd_data.py
   ```

---

### Ou execute apenas o script diretamente sem clonar o repositório

1. Instale as dependências:
   ```bash
   python -m pip install -r https://raw.githubusercontent.com/rianlucascs/linkedin-scraping-project/main/requirements.txt
   ```

2. Execute o código diretamente no seu projeto:
   ```python
   # Importando a biblioteca 'requests' para realizar requisições HTTP
   import requests

   # URL do código remoto hospedado no GitHub que contém a classe de scraping
   url = "https://raw.githubusercontent.com/rianlucascs/linkedin-scraping-project/main/extracetd_data.py"

   # Realizando a requisição HTTP para baixar o conteúdo do script
   response = requests.get(url)

   # Verificando se a requisição foi bem-sucedida
   if response.status_code == 200:
       # Usando 'exec()' para executar o código baixado
       exec(response.text)

       # Definindo o cargo da vaga que será buscada
       cargo = "Data Engineer"

       # Criando uma instância da classe 'ScrapingLinkedin'
       scraping_linkedin = ScrapingLinkedin(cargo)

       # Executando o processo de scraping
       scraping_linkedin.main()
   else:
       print(f"Erro ao acessar o código remoto. Status code: {response.status_code}")
   ```

---

### Autor
[Rian Lucas](https://github.com/rianlucascs)
