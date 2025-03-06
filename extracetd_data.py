
import logging
import unicodedata
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from typing import List

__python__ = '3.10.0'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('scraping_log.txt', mode='w', encoding='utf-8')
    ]
)

class ScrapingLinkedin:

    def __init__(self, cargo: str):
        self.cargo = cargo
        self.url = f'https://www.linkedin.com/jobs/search/?keywords={cargo}&geoId=106057199'
        self._id__dinamico_acesso_pagina = None
        self._qtd__vagas = None
        logging.info(f'Iniciando ScrapingLinkedin para a URL: {self.url}')

    def _wait_for_element_to_be_present(self, driver: WebDriver, by: By, value: str, timeout: int) -> WebElement:
        try:
            logging.info(f'Aguardando o elemento {by} = {value} por até {timeout} segundos.')
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logging.info(f'Elemento {by} = {value} encontrado com sucesso.')
            return element
        except TimeoutException:
            logging.error(f"Timeout: Elemento com {by} = '{value}' não encontrado após {timeout} segundos.")
            raise 

    def _find_element(self, driver: WebDriver, by: By, value: str) -> WebElement:
        try:
            logging.info(f'Buscando o elemento {by} = {value}.')
            element = driver.find_element(by, value)
            logging.info(f'Elemento {by} = {value} encontrado.')
            return element
        except NoSuchElementException:
            logging.error(f"Erro: Elemento com {by} = '{value}' não encontrado.")
            raise 
    
    def _find_elements(self, driver: WebDriver, by: By, value: str) -> List[WebElement]:
        try:
            logging.info(f'Buscando os elementos {by} = {value}.')
            elements = driver.find_elements(by, value)
            
            if not elements:
                logging.warning(f"Não foram encontrados elementos com {by} = '{value}'.")
            
            logging.info(f'Elementos encontrados com {by} = {value}. Total de elementos: {len(elements)}')
            return elements
        except Exception as e:
            logging.error(f"Erro ao buscar elementos com {by} = '{value}': {str(e)}")
            raise 
            
    def _extract_pagination_items(self, pagination_container: List[WebElement]) -> List[WebElement]:
        try:
            logging.info('Iniciando a extração dos itens de paginação.')
            
            # Encontra todos os itens de paginação dentro do contêiner
            pagination_items = self._find_elements(pagination_container, By.TAG_NAME, 'li')

            # Processa cada item de paginação encontrado
            for item in pagination_items:
                item_id = item.get_attribute('id')
                item_class = item.get_attribute('class')
                item_text = item.text

                # Loga as informações de cada item de paginação
                logging.info(f'ID: {item_id} | CLASS: {item_class} | TEXT: {item_text}')

            return pagination_items
        
        except Exception as e:
            logging.error(f'Erro ao extrair os itens de paginação: {str(e)}')
            raise
        
    #XXX##
    def _pagination_exibir_tudo(self, pagination_container):
        pass

    def _quantidade_de_vagas(self, driver: WebDriver) -> str:
        qtd_vagas = self._find_element(driver, By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/header/div[1]/small/div/span')
        logging.info(f"Quantidade de vagas: '{qtd_vagas.text}' para {self.cargo}.")
        if int(qtd_vagas.text[:1]) < 25:
            logging.info("Paginação desativada.")
            return "< 25"
        logging.info("Paginação ativada.")
        return "> 25"

    def _get_dynamic_page_id(self, pagination_container: List[WebElement]) -> str:
        try:

            # Localiza o container de paginação
            pagination_divs = self._find_elements(pagination_container, By.TAG_NAME, 'div')

            # exibir_tudo_id = pagination_divs[2].get_attribute('id')
            # print(f"aaaaa {exibir_tudo_id}")
            # sleep(1000)
            # exibir_tudo_button = self._find_element(pagination_container, By.XPATH,
            #                                  f'//*[@id="{exibir_tudo_id}"]/div/div[4]/div[2]/a')
            # exibir_tudo_button.click()
            # sleep(10000)

            # Verifica se existe pelo menos dois elementos na lista 
            if len(pagination_divs) > 1:

                dynamic_page_id = pagination_divs[1].get_attribute('id')

                # # Salvar Log dos id dinâmicos encontrados
                # for i, item in enumerate(pagination_divs):
                #     item = item.get_attribute('id')
                #     logging.info(f"pagination_divs | Index {i}: | ID: {item}")
                
                # # Seleciona apenas os que não gera erro na chamda
                
                # for item in pagination_divs:
                #     dynamic_page_id = item.get_attribute('id')
                #     try:
                #         self._find_element(pagination_container, By.XPATH, f'//*[@id="{dynamic_page_id}"]/div')
                #         logging.info(f"ID dinâmico da página: {dynamic_page_id}")
                #         return dynamic_page_id
                #     except:
                #         pass
                
                logging.info(f"ID dinâmico da página: {dynamic_page_id}")
                return dynamic_page_id
            else:
                logging.warning("Não foi possível encontrar o índice esperado de elementos de paginação.")
                raise
        except NoSuchElementException as e:
            logging.error(f"Erro ao tentar localizar o elemento de paginação: {e}")
            raise
    
    def _get_pagination_info(self, pagination_container: WebDriver) -> dict:
        try:
            # Localiza o contêiner de paginação e obtém o HTML completo do item
            pagination_element = self._find_element(pagination_container, By.XPATH, 
                                                    f'//*[@id="{self._id__dinamico_acesso_pagina}"]/div')
            outer_html = pagination_element.get_attribute("outerHTML")
            
            # Extração dos valores de página atual e total
            split_html = str(outer_html).split(' ')

            # Verifica se os índices são válidos
            if len(split_html) > 10:
                current_page = int(split_html[8])
                total_pages = int(split_html[10][:2])

                # Cria um dicionário com as informações
                pagination_info = {
                    'pagina_atual': current_page,
                    'quantidade_de_paginas': total_pages
                }

                logging.info(f'Informações de paginação: {pagination_info}')
                return pagination_info
            else:
                logging.warning("Não foi possível extrair as informações de paginação corretamente.")
                raise

        except NoSuchElementException as e:
            logging.error(f'Erro ao tentar localizar o contêiner de paginação: {e}')
            raise
        except Exception as e:
            logging.error(f'Erro ao extrair as informações de paginação: {str(e)}')
            raise

    def _get_job_list(self, pagination_container: List[WebElement]):
        try:
            # Localiza o contêiner de vagas 
            job_list_container = self._find_element(pagination_container, By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')

            # Encontra todas os itens de lista de vagas dentro do contêiner
            job_items = self._find_elements(job_list_container, By.TAG_NAME, 'li')

            if len(job_items) >= 1:
                logging.info(f'Número de vagas encontradas na página: {len(job_items)}')

                return job_items
            else:
                logging.info(f'Nenhuma vaga encontrada na página.')
                raise
        except NoSuchElementException as e:
            logging.error(f'Erro ao localizar o contêiner de vagas: {e}')
            raise
        except Exception as e:
            logging.error(f'Erro inesperado ao processar as vagas: {e}')
            raise

    def remove_accent_and_special_chars(self, text: str) -> str:
        """
        Remove acentos, transforma em minúsculas, e elimina caracteres especiais de uma string.

        Parâmetros:
        - text (str): A string de entrada.

        Retorna:
        - str: A string sem acentos, caracteres especiais e em minúsculas, com espaços substituídos por '_'.
        """
        # Normaliza o texto para decompor os acentos e caracteres especiais
        nfkd_form = unicodedata.normalize('NFKD', text)
        
        # Converte o texto para minúsculas e substitui espaços por '_'
        normalized_text = nfkd_form.lower().replace(' ', '_')
        
        # Remove caracteres especiais usando regex
        clean_text = re.sub(r'[^a-z0-9_]', '', normalized_text)

        # Substitui múltiplos underscores por um único
        clean_text = re.sub(r'__+', '_', clean_text)

        return clean_text

    def _save_data(self, job_title: str, company_name: str, job_description: str) -> None:
        """
        Salva a descrição de uma vaga em um arquivo, utilizando o título da vaga e o nome da empresa para criar o nome do arquivo.

        Parâmetros:
        - job_title (str): Título da vaga.
        - company_name (str): Nome da empresa.
        - job_description (str): Descrição da vaga a ser salva no arquivo.

        Cria uma pasta 'data' se não existir e armazena o arquivo de texto com o nome da vaga e da empresa.
        """
        try:
            # Obtém o caminho absoluto do diretório atual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Define o caminho para a pasta 'data'
            data_dir = os.path.join(current_dir, 'data', 'extracted_data', self.cargo)
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            # Remover acentos e caracteres especiais do título da vaga e do nome da empresa
            sanitized_job_title = self.remove_accent_and_special_chars(job_title)
            sanitized_company_name = self.remove_accent_and_special_chars(company_name)

            # Cria o nome do arquivo a partir do título da vaga e da empresa
            file_name = f"{sanitized_job_title}-{sanitized_company_name}.txt"
            file_path = os.path.join(data_dir, file_name)

            # Verifica se o arquivo já existe, e cria um novo arquivo com o conteúdo da descrição da vaga
            if not os.path.exists(file_path):
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(job_description)
            
                logging.info(f"Arquivo salvo em: {file_path}")
            else:
                logging.info(f"Arquivo já existe em: {file_path}")
        
        except Exception as e:
            logging.error(f"Erro ao salvar os dados: {str(e)}")

    def main(self):
        options = webdriver.ChromeOptions()
        with webdriver.Chrome(options=options) as driver:
            driver.get(self.url)
            self.driver = driver

            logging.info(f'Página {self.url} carregada com sucesso.')

            # Espera até que o login seja feito "manualmente"
            self._wait_for_element_to_be_present(driver, By.XPATH, '//*[@id="searchFilter_timePostedRange"]', 6*50)

            # Espera a página caregar
            self._wait_for_element_to_be_present(driver, By.XPATH, '//*[@id="searchFilter_timePostedRange"]', 6*50)

            # Verifica a quantidade de vagas
            self._qtd__vagas = self._quantidade_de_vagas(driver)

            # Localiza o contêiner que contém os itens de paginação
            pagination_container = self._find_element(driver, By.ID, 'jobs-search-results-footer')

            # ID paginação "_get_pagination_info"
            self._id__dinamico_acesso_pagina = self._get_dynamic_page_id(pagination_container)

            if self._qtd__vagas == "> 25":
                logging.info(f"Quantidade de vagas maior que 25.")
                qtd_paginas_disponiveis = self._get_pagination_info(pagination_container)["quantidade_de_paginas"] + 1
            else:
                # Caso não tenha um número suficiente de vagas para gerar paginas
                qtd_paginas_disponiveis = 2
                logging.info("Quantidade de vagas menor que 25.")

            # Loop range paginas disponíveis
            for numero_pagina in range(1, qtd_paginas_disponiveis):

                # Localiza o contêiner que contém os itens de paginação
                pagination_container = self._find_element(driver, By.ID, 'jobs-search-results-footer')

                for obj_vaga in self._get_job_list(pagination_container):
                    
                    # Removendo tags que não tem ID. Essas não tem conteúdo de vagas
                    try:
                        id_obj_vaga = obj_vaga.get_attribute("id")
                    except:
                        id_obj_vaga = None
                        
                    if id_obj_vaga:
                        
                        logging.info(f'obj_vaga = {obj_vaga}')

                        obj_vaga.click()

                        sleep(3)

                        self._wait_for_element_to_be_present(driver, By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[4]/article', 15)

                        info = self._find_element(driver, By.XPATH, f'//*[@id="{id_obj_vaga}"]').text
                        info = info.split('\n')[1:3]

                        if len(info) >= 2:
                            job_title = info[0]
                            company_name = info[1]
                            job_description = self._find_element(driver, By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[4]/article').text

                            self._save_data(job_title, company_name, job_description)

                        logging.info(f"página: {numero_pagina} | id: {id_obj_vaga} | info: {info}")

                        sleep(3)

                # Paginação

                # Pega o número da proxíma página

                if self._qtd__vagas == "> 25":
                    numero_proxima_pagina = self._get_pagination_info(pagination_container)["pagina_atual"] + 1

                    try:
                        self._wait_for_element_to_be_present(pagination_container, By.CSS_SELECTOR, 
                                                            f'[data-test-pagination-page-btn="{numero_proxima_pagina}"]', 
                                                            timeout=10).click()
                    except:
                        self._extract_pagination_items(pagination_container)[8].click()
                else:
                    pass

if __name__ == "__main__":

    cargo = "Engenheiro de Dados SR Sênior"
    scraping_linkedin = ScrapingLinkedin(cargo)
    scraping_linkedin.main()

