# Importando a biblioteca 'requests' para realizar requisições HTTP
import requests

# URL do código remoto hospedado no GitHub que contém a classe de scraping
url = "https://raw.githubusercontent.com/rianlucascs/linkedin-scraping-project/main/extracetd_data.py"

# Realizando a requisição HTTP para baixar o conteúdo do script
# A URL aponta para o código remoto no GitHub e com 'requests.get()', estamos baixando esse código.
response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
# Se o código de status for 200, significa que o conteúdo foi baixado com sucesso.
if response.status_code == 200:
    # Usando 'exec()' para executar o código baixado
    # O conteúdo do código remoto será executado no contexto atual, tornando a classe 'ScrapingLinkedin' disponível para uso.
    exec(response.text)

    # Definindo o cargo da vaga que será buscada
    # Aqui você pode alterar o valor de 'cargo' para buscar diferentes tipos de vagas no LinkedIn.
    cargo = "Data Engineer"

    # Criando uma instância da classe 'ScrapingLinkedin'
    # A classe será inicializada com o cargo desejado como parâmetro.
    scraping_linkedin = ScrapingLinkedin(cargo)

    # Executando o processo de scraping
    # O método 'main()' inicia todo o processo de busca e extração de dados.
    scraping_linkedin.main()
else:
    # Exibindo uma mensagem de erro caso a requisição falhe
    print(f"Erro ao acessar o código remoto. Status code: {response.status_code}")
