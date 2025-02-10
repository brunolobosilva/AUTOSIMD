{# RELATÓRIO DE ALTERAÇÕES - VERSÃO 1.07

# Este relatório descreve as principais mudanças implementadas na versão 1.07 do programa
# em comparação com a versão anterior (1.06). As alterações visam melhorar a funcionalidade,
# robustez e experiência do usuário.

## 1. Adição de Botões para Copiar Municípios por Mesorregião
# - Implementação de botões para copiar os municípios afetados de cada mesorregião individualmente para facilitar na elaboração do boletim de alertas.
#   - Foram adicionados botões para as seguintes mesorregiões:
#       - Baixo Amazonas
#       - Metropolitana de Belém
#       - Marajó
#       - Nordeste Paraense
#       - Sudeste Paraense
#       - Sudoeste Paraense
#   - Cada botão copia os municípios da respectiva mesorregião para a área de transferência.
#   - Mensagens de sucesso ou erro são registradas no log.
#   - Os botões estão organizados em um grid de 3 colunas para melhor aproveitamento do espaço.

## 2. Coleta Automática de Dados Gerais
# - A coleta dos dados gerais do alerta foi automatizada, eliminando a necessidade de inserção manual.
#   - Os rótulos são identificados dinamicamente usando o seletor XPATH automático quando possível.
#   - com excessão do resultado do "aviso de:" que teve ser usado um script JavaScript para acessar o nó de texto irmão.
#   - Os dados coletados são armazenados em um dicionário (`self.dados_gerais`) e exibidos no log.
#   - Exemplo de estrutura dos dados gerais:
#     self.dados_gerais = {
#         "Aviso de:": "Chuvas Intensas",
#         "Nível de Risco:": "Perigo",
#     }
# - Adição de tratamento para ignorar campos desnecessários, como "Municípios:", "Áreas Afetadas:",
#   "Instruções:", "Início:", "Fim:" e "Perigo".

## 3. Melhorias no Tratamento de Erros
# - Refatoração dos blocos `try-except` para fornecer mensagens de erro mais claras e específicas.
#   - Exemplo:
#     try:
#         coletor.coletar_dados_gerais()
#     except Exception as e:
#         self.log(f"Falha na etapa de coleta de dados gerais: {str(e)}")
# - Estou investigando uma forma de remover o erro do log quando o programa termina de rodar e fecha o browser mas o selenium continua tentando acessar.

## 4. Organização do Código
# - Reorganização do código para melhor legibilidade e manutenção.
#   - Agrupamento lógico de funções e classes.
#   - Remoção de comentários redundantes e adição de outros explicativos
#   - Padronização dos logs para facilitar a leitura e depuração.

## 5. Atualização do Botão "Copiar Relatório Completo"
# - Atualização do botão "Copiar Relatório Completo" no frame direito da interface gráfica.
#   - O botão copia o conteúdo completo do relatório gerado para a área de transferência.
#   - Mensagens de sucesso ou erro são registradas no log.

## 6. Pequenas Refatorações
# - Ajustes nas importações para melhor organização.
# - Correção de pequenos bugs relacionados à navegação entre páginas da tabela de municípios.
# - Melhoria na formatação do relatório final para garantir consistência.

# Resumo das Principais Mudanças:
# 1. Adição de botões para copiar municípios por mesorregião.
# 2. Coleta automática de dados gerais do alerta.
# 3. Melhorias no tratamento de erros.
# 4. Organização e refatoração do código para melhor legibilidade.
# 5. Adição do botão "Copiar Relatório Completo".
# 6. Correção de bugs e ajustes na navegação entre páginas.

# Essas alterações tornaram o programa mais funcional, robusto e amigável para o usuário.
}

import tkinter as tk
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import os
import sys

def get_chromedriver_path(): # Função para obter o caminho correto do ChromeDriver
    """Retorna o caminho correto para o ChromeDriver."""
    if getattr(sys, 'frozen', False):  # Verifica se o script está sendo executado como executável
        application_path = sys._MEIPASS  # Obtém o caminho temporário do PyInstaller
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
    return os.path.join(application_path, "chromedriver.exe")  # Retorna o caminho completo do ChromeDriver

def get_resource_path(relative_path): # Função para obter o caminho absoluto de recursos (imagens, ícones, etc.)
    """Retorna o caminho absoluto para o recurso, funcional tanto no desenvolvimento quanto no executável."""
    try:
        base_path = sys._MEIPASS  # Obtém o caminho temporário do PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # Obtém o diretório atual
    return os.path.join(base_path, relative_path)  # Retorna o caminho completo do recurso


class Mesorregiao: # Classe para gerenciar as mesorregiões do Pará
    def __init__(self): #Inicializa a classe com um dicionário contendo as mesorregiões e seus municípios.
        self.mesorregioes = { # Dicionário com as mesorregiões e suas respectivas listas de municípios
            "Marajó": [
                "Bagre", "Gurupá", "Melgaço", "Portel", "Afuá", "Anajás", "Breves", 
                "Curralinho", "São Sebastião da Boa Vista", "Cachoeira do Arari", 
                "Chaves", "Muaná", "Ponta de Pedras", "Salvaterra", "Santa Cruz do Arari", 
                "Soure"
            ],
            "Metropolitana de Belém": [
                "Ananindeua", "Barcarena", "Belém", "Benevides", "Marituba", 
                "Santa Bárbara do Pará", "Bujaru", "Castanhal", "Inhangapi", 
                "Santa Izabel do Pará", "Santo Antônio do Tauá"
            ],
            "Nordeste Paraense": [
                "Colares", "Curuçá", "Magalhães Barata", "Maracanã", "Marapanim", 
                "Salinópolis", "São Caetano de Odivelas", "São João da Ponta", 
                "São João de Pirabas", "Terra Alta", "Vigia", "Augusto Corrêa", 
                "Bonito", "Bragança", "Capanema", "Igarapé-Açu", "Nova Timboteua", 
                "Peixe-Boi", "Primavera", "Quatipuru", "Santa Maria do Pará", 
                "Santarém Novo", "São Francisco do Pará", "Tracuateua", "Abaetetuba", 
                "Baião", "Cametá", "Igarapé-Miri", "Limoeiro do Ajuru", "Mocajuba", 
                "Oeiras do Pará", "Acará", "Concórdia do Pará", "Moju", "Tailândia", 
                "Tomé-Açu", "Aurora do Pará", "Cachoeira do Piriá", "Capitão Poço", 
                "Garrafão do Norte", "Ipixuna do Pará", "Irituia", "Mãe do Rio", 
                "Nova Esperança do Piriá", "Ourém", "Santa Luzia do Pará", 
                "São Domingos do Capim", "São Miguel do Guamá", "Viseu"
            ],
            "Sudoeste Paraense": [
                "Aveiro", "Itaituba", "Jacareacanga", "Novo Progresso", "Rurópolis", 
                "Trairão", "Altamira", "Anapu", "Brasil Novo", "Medicilândia", 
                "Pacajá", "Senador José Porfírio", "Uruará", "Vitória do Xingu"
            ],
            "Sudeste Paraense": [
                "Breu Branco", "Itupiranga", "Jacundá", "Nova Ipixuna", 
                "Novo Repartimento", "Tucuruí", "Abel Figueiredo", 
                "Bom Jesus do Tocantins", "Dom Eliseu", "Goianésia do Pará", 
                "Paragominas", "Rondon do Pará", "Ulianópolis", "Bannach", 
                "Cumaru do Norte", "Ourilândia do Norte", "São Félix do Xingu", 
                "Tucumã", "Água Azul do Norte", "Canaã dos Carajás", 
                "Curionópolis", "Eldorado do Carajás", "Parauapebas", 
                "Brejo Grande do Araguaia", "Marabá", "Palestina do Pará", 
                "São Domingos do Araguaia", "São João do Araguaia", "Pau D'Arco", 
                "Piçarra", "Redenção", "Rio Maria", "São Geraldo do Araguaia", 
                "Sapucaia", "Xinguara", "Conceição do Araguaia", 
                "Floresta do Araguaia", "Santa Maria das Barreiras", 
                "Santana do Araguaia"
            ],
            "Baixo Amazonas": [
                "Alenquer", "Almeirim", "Belterra", "Curuá", "Faro", "Juruti", 
                "Mojuí dos Campos", "Monte Alegre", "Oriximiná", "Placas", 
                "Porto de Moz", "Prainha", "Santarém", "Terra Santa", "Óbidos"
            ]
        }

    def obter_mesorregiao(self, municipio): # Retorna a mesorregião de um município específico.
        for regiao, municipios in self.mesorregioes.items():  # Itera sobre as mesorregiões
            if municipio in municipios:  # Verifica se o município pertence à mesorregião
                return regiao
        return None  # Retorna None se o município não for encontrado


class ColetorDados: # Classe principal para coletar dados dos alertas do INMET
    def __init__(self, url, log_callback): # Inicializa o coletor de dados com a URL do alerta e uma função de callback para logs.
        self.url = url  # URL da página do alerta
        self.driver = None  # Driver do Selenium (inicializado posteriormente)
        self.municipios_afetados = []  # Lista para armazenar municípios afetados
        self.dados_gerais = {}  # Dicionário para armazenar os dados gerais do alerta
        self.log_callback = log_callback  # Função para registrar logs na interface

    def iniciar_driver(self): # Inicia o driver do Selenium para navegação automatizada.
        try:
            service = Service(get_chromedriver_path())  # Configura o serviço do ChromeDriver
            self.driver = webdriver.Chrome(service=service)  # Inicializa o driver
            self.log_callback("Driver do Selenium iniciado com sucesso.")  # Registra sucesso no log
        except Exception as e:
            self.log_callback(f"Falha ao iniciar o driver: {str(e)}")  # Registra falha no log
            raise  # Lança a exceção para interromper o fluxo

    def acessar_pagina(self): #Acessa a página inicial do alerta usando o driver do Selenium.
        try:
            self.driver.get(self.url)  # Navega para a URL fornecida
            self.log_callback(f"Página acessada com sucesso: {self.url}")  # Registra sucesso no log
        except Exception as e:
            self.log_callback(f"Falha ao acessar a página: {str(e)}")  # Registra falha no log
            raise  # Lança a exceção para interromper o fluxo

    def execute_js_xpath(self, xpath): #Executa um script JavaScript para acessar um nó de texto ou elemento via XPath. Retorna o valor do nó ou elemento encontrado.
        script = f"""
            const result = document.evaluate(
                '{xpath}',  # XPath para o nó desejado
                document,
                null,
                XPathResult.STRING_TYPE,
                null
            );
            return result.stringValue.trim();  // Retorna o valor do nó como string
        """
        try:
            return self.driver.execute_script(script)  # Executa o script no navegador
        except Exception as e:
            self.log_callback(f"Falha ao executar JavaScript para XPath '{xpath}': {str(e)}")  # Registra falha no log
            return None  # Retorna None em caso de erro

    def coletar_dados_gerais(self): #Coleta os dados gerais do alerta antes de clicar no botão 'Veja Mais'.
        try:
            self.log_callback("Coletando dados gerais do alerta...")
            dados_gerais = {}
            wait = WebDriverWait(self.driver, 30)  # Define um tempo máximo de espera de 20 segundos
            
            # Definindo constantes para os XPaths
            XPATH_AVISO_DE = "//*[@id='root']/div/div[2]/div[2]/div/font[1]"  # XPath para o rótulo "Aviso de:"
            XPATH_GRAU_SEVERIDADE = "//*[@id='root']/div/div[2]/div[2]/div/font[2]"
            XPATH_RESULTADO_GRAU_SEVERIDADE = "//*[@id='root']/div/div[2]/div[2]/div/font[3]/font"
            XPATH_RISCOS_POTENCIAIS = "//*[@id='root']/div/div[2]/div[2]/div/font[6]"
            XPATH_RESULTADO_RISCOS_POTENCIAIS = "//*[@id='root']/div/div[2]/div[2]/div/p[1]/div"

            try: # Coleta do "Aviso de:
                aviso_de = self.driver.find_element(By.XPATH, XPATH_AVISO_DE).text.strip()

                # Script JavaScript para acessar o nó de texto irmão
                script_aviso_de = """
                    const xpathResult = document.evaluate(
                        '//*[@id="root"]/div/div[2]/div[2]/div/text()[2]',
                        document,
                        null,
                        XPathResult.STRING_TYPE,
                        null
                    );
                    return xpathResult.stringValue.trim();
                """
                resultado_aviso_de = self.driver.execute_script(script_aviso_de)

                if resultado_aviso_de:
                    dados_gerais[f"{aviso_de}:"] = resultado_aviso_de
                    self.log_callback(f"'Aviso de:' coletado com sucesso: {resultado_aviso_de}")
                else:
                    dados_gerais["Aviso de:"] = "Não encontrado"
                    self.log_callback("'Aviso de:' não encontrado ou vazio.")
            except Exception as e:
                dados_gerais["Aviso de:"] = "Não encontrado"
                self.log_callback(f"Falha ao coletar 'Aviso de:': {str(e)}")

            try: # Coleta do "Grau de Severidade
                grau_severidade = self.driver.find_element(By.XPATH, XPATH_GRAU_SEVERIDADE).text.strip()
                resultado_grau_severidade = self.driver.find_element(By.XPATH, XPATH_RESULTADO_GRAU_SEVERIDADE).text.strip()
                if resultado_grau_severidade:
                    dados_gerais[f"{grau_severidade}:"] = resultado_grau_severidade
                    self.log_callback(f"'Grau de Severidade:' coletado com sucesso: {resultado_grau_severidade}")
                else:
                    dados_gerais["Grau de Severidade:"] = "Não encontrado"
                    self.log_callback("'Grau de Severidade:' não encontrado ou vazio.")
            except Exception as e:
                dados_gerais["Grau de Severidade:"] = "Não encontrado"
                self.log_callback(f"Falha ao coletar 'Grau de Severidade:': {str(e)}")
          
            try: # Coleta dos "Riscos Potenciais"
                riscos_potenciais = self.driver.find_element(By.XPATH, XPATH_RISCOS_POTENCIAIS).text.strip()
                resultado_riscos_potenciais = self.driver.find_element(By.XPATH, XPATH_RESULTADO_RISCOS_POTENCIAIS).text.strip()
                if resultado_riscos_potenciais:
                    dados_gerais[f"{riscos_potenciais}:"] = resultado_riscos_potenciais
                    self.log_callback(f"'Riscos Potenciais:' coletado com sucesso: {resultado_riscos_potenciais}")
                else:
                    dados_gerais["Riscos Potenciais:"] = "Não encontrado"
                    self.log_callback("'Riscos Potenciais:' não encontrado ou vazio.")
            except Exception as e:
                dados_gerais["Riscos Potenciais:"] = "Não encontrado"
                self.log_callback(f"Falha ao coletar 'Riscos Potenciais:': {str(e)}")

            # Armazena os dados gerais no atributo da classe
            self.dados_gerais = dados_gerais
            self.log_callback("Dados gerais coletados com sucesso.")
            self.log_callback(str(dados_gerais))

        except Exception as e:
            self.log_callback(f"Falha crítica na coleta de dados gerais: {str(e)}")
        
        
    def clicar_veja_mais(self): # Clica no botão 'Veja Mais'.
        try:
            wait = WebDriverWait(self.driver, 20)
            botao_veja_mais = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='MuiButton-label' and text()='Veja Mais']")))
            time.sleep(3) #adiciona um tempo a mais de espera por conta do script em javascript para coletar o resultado do "aviso de:"
            botao_veja_mais.click()
            self.log_callback("Botão 'Veja Mais' clicado.")
        except Exception as e:
            self.log_callback(f"Falha ao clicar no botão 'Veja Mais': {str(e)}")
            raise

    def alterar_linhas_por_pagina(self): #Altera o número de linhas exibidas por página para 100.
        try:
            wait = WebDriverWait(self.driver, 20)
            select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select.custom-select")))
            select = Select(select_element)
            select.select_by_value("100")
            self.log_callback("Alterado para 100 linhas por página.")
        except Exception as e:
            self.log_callback(f"Falha ao alterar o número de linhas por página: {str(e)}")
            raise

    def coletar_dados_tabela(self): # Coleta os dados das dos municípios do Pará da tabela.
        try:
            wait = WebDriverWait(self.driver, 20)
            table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table"))) #aguarda até o carregamento da tabela
            numero_pagina = 1
            while True:
                self.log_callback(f"Lendo a página {numero_pagina}...") #retorna o log "lendo a página..."
                linhas = table.find_elements(By.TAG_NAME, "tr") # tr: o código do xpath para a linha
                for linha in linhas:
                    colunas = linha.find_elements(By.TAG_NAME, "td") # td: o código do xpath para as colunas "nm_mun"[0], "geocode"[1], "uf"[2]
                    if colunas:  # Ignora linhas vazias
                        estado = colunas[2].text.strip() # colunas[2] faz referência a coluna das uf
                        if estado == "PA": # se uf for igual a "PA"...
                            municipio = colunas[0].text.strip() #capture o nome do município
                            self.municipios_afetados.append(municipio) #adicione o município à lista de municípios afetados
                try:
                    botao_proxima_pagina = self.driver.find_element(By.XPATH, "//span[text()='Próximo']")
                    if "disabled" in botao_proxima_pagina.find_element(By.XPATH, "..").get_attribute("class"):
                        self.log_callback("Não há mais páginas.")
                        break
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", botao_proxima_pagina)
                    time.sleep(1)
                    botao_proxima_pagina.click()
                    numero_pagina += 1
                    time.sleep(3)
                    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
                except Exception as e:
                    if "no such window" in str(e):
                        self.log_callback("A janela do navegador foi fechada prematuramente.")
                    else:
                        self.log_callback(f"Erro ao tentar ir para a próxima página: {e}")
                    break
        except Exception as e:
            self.log_callback(f"Falha ao coletar dados: {str(e)}")
                

class Relatorio: # Classe para gerar o relatório final
    def __init__(self, municipios_afetados, mesorregiao, log_callback, relatorio_callback, dados_gerais, titulo_programa):
        
        """Inicializa a classe de relatório com os dados necessários."""
        self.municipios_afetados = municipios_afetados  # Municípios afetados pelo alerta
        self.mesorregiao = mesorregiao  # Instância da classe Mesorregiao
        self.log_callback = log_callback  # Função para registrar logs
        self.relatorio_callback = relatorio_callback  # Função para atualizar o relatório na interface
        self.dados_gerais = dados_gerais  # Dados gerais do alerta
        self.titulo_programa = titulo_programa  # Título do programa

    def classificar_municipios(self): # Classifica os municípios por mesorregião.
        grupos = {}  # Dicionário para armazenar municípios por mesorregião
        nao_classificados = []  # Lista para municípios que não foram classificados
        for municipio in set(self.municipios_afetados):  # Itera sobre os municípios únicos
            regiao = self.mesorregiao.obter_mesorregiao(municipio)  # Obtém a mesorregião do município
            if regiao:
                if regiao not in grupos:
                    grupos[regiao] = []  # Cria uma lista para a mesorregião se ainda não existir
                grupos[regiao].append(municipio)  # Adiciona o município à sua mesorregião
            else:
                nao_classificados.append(municipio)  # Adiciona o município à lista de não classificados
        return grupos, nao_classificados  # Retorna os grupos e municípios não classificados

    def gerar_relatorio(self): # Gera o relatório final no formato especificado.
        grupos, nao_classificados = self.classificar_municipios()  # Classifica os municípios
        relatorio_texto = ""  # String para armazenar o conteúdo do relatório
        data_atual = datetime.now().strftime("%d/%m/%Y")  # Data atual
        hora_atual = datetime.now().strftime("%H:%M")  # Hora atual

        # Cabeçalho do relatório
        relatorio_texto += f"{self.titulo_programa} \n"  # Adiciona o título do programa
        relatorio_texto += "-" * len(self.titulo_programa) + "\n"  # Linha separadora

        # Seção de Dados Gerais do Alerta
        relatorio_texto += "Dados Gerais do Alerta\n"
        relatorio_texto += "-" * 50 + "\n"
        for chave, valor in sorted(self.dados_gerais.items()):  # Itera sobre os dados gerais
            relatorio_texto += f"{chave}: {valor}\n"  # Adiciona cada dado ao relatório
        relatorio_texto += "\n"

        # Seção de Municípios Afetados Pelo Alerta
        relatorio_texto += "Lista dos Municípios Afetados Pelo Alerta\n"
        relatorio_texto += "-" * 50 + "\n"
        for regiao, municipios in sorted(grupos.items()):  # Itera sobre as mesorregiões
            relatorio_texto += f"Mesorregião: {regiao}\n"  # Adiciona o nome da mesorregião
            relatorio_texto += ", ".join(sorted(municipios)) + "\n\n"  # Adiciona os municípios ordenados

        # Seção de Municípios Não Classificados
        if nao_classificados:
            relatorio_texto += "Municípios Não Classificados\n"
            relatorio_texto += ", ".join(sorted(nao_classificados)) + "\n\n"  # Adiciona os municípios não classificados

        # Resumo do relatório
        relatorio_texto += f"Total de municípios afetados: {len(self.municipios_afetados)}\n"
        relatorio_texto += f"Municípios não classificados: {len(nao_classificados)}\n"
        relatorio_texto += f"Hora da coleta: {data_atual} {hora_atual}\n"

        # Atualiza a área do relatório na interface
        self.relatorio_callback(relatorio_texto)  # Chama a função de callback para atualizar o relatório
        self.log_callback(f"Total de municípios afetados: {len(self.municipios_afetados)}")  # Registra no log
        self.log_callback(f"Municípios não classificados: {len(nao_classificados)}")  # Registra no log


class App: # Classe principal da aplicação
    def __init__(self, root):
        self.root = root  # Janela principal do Tkinter
        self.titulo_programa = "AUTOSIMD (1.07) - Relatório de Alertas INMET (CBMPA E DEFESA CIVIL)"  # Título do programa
        self.root.title(self.titulo_programa)  # Define o título da janela
        self.root.geometry("1200x800")  # Define o tamanho da janela
        self.municipios_afetados = []  # Inicializa como uma lista vazia
     
        try: # Configuração do ícone da janela
            self.root.iconbitmap(r"D:\07_GEOPROCESSAMENTO\AUTOMATIZAÇÃO\icones\Log_Sala_BM.ico")
        except Exception as e:
            print(f"Erro ao carregar o ícone: {str(e)}")
            
        # Frame principal
        frame_principal = tk.Frame(root)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Cabeçalho Fixo
        self.cabecalho_frame = tk.Frame(frame_principal, relief=tk.RIDGE, borderwidth=2, height=60)
        self.cabecalho_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        self.exibir_cabecalho()

        # Frame central (Log + Link + Botão + Relatório)
        frame_central = tk.Frame(frame_principal, relief=tk.RIDGE, borderwidth=2)
        frame_central.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=3)

        # Frame esquerdo (Link + Log)
        frame_esquerdo = tk.Frame(frame_central, width=400, relief=tk.RIDGE, borderwidth=2)
        frame_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Frame direito (Relatório)
        frame_direito = tk.Frame(frame_central, width=800, relief=tk.RIDGE, borderwidth=2)
        frame_direito.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        # Caixa de entrada para o link
        tk.Label(frame_esquerdo, text="Insira o link do alerta:", font=("Arial", 12)).pack(pady=10)
        self.link_entry = tk.Entry(frame_esquerdo, width=50, font=("Arial", 12))
        self.link_entry.pack(pady=5)

        # Botão para iniciar o processo
        tk.Button(frame_esquerdo, text="Gerar Relatório", command=self.gerar_relatorio, font=("Arial", 12)).pack(pady=10)

        # Área de log
        tk.Label(frame_esquerdo, text="Log do Programa:", font=("Arial", 12)).pack(pady=10)
        self.log_area = scrolledtext.ScrolledText(frame_esquerdo, wrap=tk.WORD, width=50, height=20, font=("Arial", 10))
        self.log_area.pack(pady=10)

        # Relatório Gerado
        tk.Label(frame_direito, text="Relatório Gerado:", font=("Arial", 12)).pack(pady=10)
        self.relatorio_area = scrolledtext.ScrolledText(frame_direito, wrap=tk.WORD, width=80, height=20, font=("Arial", 10))
        self.relatorio_area.pack(pady=10)

        # Frame para botões de cópia
        frame_botoes_copiar = tk.Frame(frame_direito, relief=tk.RIDGE, borderwidth=2)
        frame_botoes_copiar.pack(pady=10, fill=tk.X)

        # Criar um grid para organizar os botões de cópia por mesorregião
        mesorregioes = ["Baixo Amazonas", "Metropolitana de Belém", "Marajó", "Nordeste Paraense", "Sudeste Paraense", "Sudoeste Paraense"]
        self.botoes_copiar = {}

        for i, mesorregiao in enumerate(mesorregioes):
            btn_text = f"Copiar {mesorregiao}"
            btn = tk.Button(
                frame_botoes_copiar,
                text=btn_text,
                command=lambda m=mesorregiao: self.copiar_municipios_mesoregiao(m),
                font=("Arial", 9),  # Reduz o tamanho da fonte
                width=25,  # Define uma largura fixa para os botões
                height=1  # Define uma altura fixa para os botões
            )
            # Posiciona os botões em 3 colunas
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=2)
            self.botoes_copiar[mesorregiao] = btn

        # Botão para copiar o relatório completo
        btn_copiar_relatorio = tk.Button(
            frame_botoes_copiar,
            text="Copiar Relatório Completo",
            command=self.copiar_relatorio,
            font=("Arial", 10, "bold"),
            width=78,  # Largura para ocupar as 3 colunas
            height=1
        )
        btn_copiar_relatorio.grid(row=2, column=0, columnspan=3, pady=10)  # Posiciona abaixo dos outros botões

        # Rodapé Fixo
        self.rodape_frame = tk.Frame(frame_principal, relief=tk.RIDGE, borderwidth=2, height=60)
        self.rodape_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        self.exibir_rodape()

    def copiar_municipios_mesoregiao(self, mesorregiao):
        """Copia os municípios de uma mesorregião específica para a área de transferência."""
        try:
            # Verifica se há municípios afetados disponíveis
            if not self.municipios_afetados:
                self.log("Nenhum dado de município disponível. Gere o relatório primeiro.")
                return

            # Obtém os municípios classificados por mesorregião
            grupos, _ = self.classificar_municipios()
            if mesorregiao in grupos:
                municipios = grupos[mesorregiao]
                municipios_texto = ", ".join(sorted(municipios))
                # Copia para a área de transferência
                self.root.clipboard_clear()
                self.root.clipboard_append(municipios_texto)
                self.root.update()  # Garante que o clipboard seja atualizado
                self.log(f"Municípios da mesorregião '{mesorregiao}' copiados para a área de transferência.")
            else:
                self.log(f"Nenhum município encontrado para a mesorregião '{mesorregiao}'.")
        except Exception as e:
            self.log(f"Falha ao copiar municípios da mesorregião '{mesorregiao}': {str(e)}")

    def classificar_municipios(self):
        """Classifica os municípios por mesorregião."""
        grupos = {}
        nao_classificados = []
        mesorregiao = Mesorregiao()
        for municipio in set(self.municipios_afetados):  # Usa o atributo inicializado
            regiao = mesorregiao.obter_mesorregiao(municipio)
            if regiao:
                if regiao not in grupos:
                    grupos[regiao] = []
                grupos[regiao].append(municipio)
            else:
                nao_classificados.append(municipio)
        return grupos, nao_classificados

    def exibir_cabecalho(self): # Exibe o cabeçalho fixo.
        # Define a altura do cabeçalho
        cabecalho_altura = 60

        # Carrega as imagens e redimensiona para a altura do cabeçalho
        logo_cbmpa = tk.PhotoImage(file=get_resource_path("icones/CBM-E-CEDEC_2.png"))
        logo_simd = tk.PhotoImage(file=get_resource_path("icones/Log_Sala_BM.png"))

        # Calcula o fator de redimensionamento com base na altura desejada
        fator_cbmpa = logo_cbmpa.height() // cabecalho_altura
        fator_simd = logo_simd.height() // cabecalho_altura

        # Redimensiona as imagens
        logo_cbmpa = logo_cbmpa.subsample(fator_cbmpa)
        logo_simd = logo_simd.subsample(fator_simd)

        # Exibe as imagens no cabeçalho
        logo_label_cbmpa = tk.Label(self.cabecalho_frame, image=logo_cbmpa)
        logo_label_cbmpa.image = logo_cbmpa  # Mantém a referência para evitar garbage collection
        logo_label_cbmpa.pack(side=tk.LEFT, padx=10)

        # Texto centralizado e em negrito
        cabecalho_texto = (
            "CORPO DE BOMBEIROS MILITAR DO ESTADO DO PARÁ (CBMPA)\n"
            "COORDENADORIA DE DEFESA CIVIL (CEDEC)\n"
            "SALA DE INFORMAÇÕES DE MONITORAMENTO DE DESASTRES (SIMD)\n"
            "AUTOSIMD - AUTOMAÇÃO DE COLETA DE MUNICÍPIOS NOS ALERTAS DO INMET"
        )
        cabecalho_label = tk.Label(self.cabecalho_frame, text=cabecalho_texto, font=("Arial", 12, "bold"), justify=tk.CENTER)
        cabecalho_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Exibe a segunda imagem no cabeçalho
        logo_label_simd = tk.Label(self.cabecalho_frame, image=logo_simd)
        logo_label_simd.image = logo_simd  # Mantém a referência para evitar garbage collection
        logo_label_simd.pack(side=tk.RIGHT, padx=10)

    def exibir_rodape(self): # Exibe o rodapé fixo.
        rodape = (
            "\n"
            "* Software projetado por Bruno Lobão da Silva\n"
            "* Dados coletados automaticamente via webscrapping com código python desenvolvido inteiramente por inteligência artificial\n"
            "* Fonte dos dados: INMET - https://alertas2.inmet.gov.br\n"
            "* Plataforma DeepSeek: https://www.deepseek.com\n"
            "* Plataforma Qwen: https://qwen.aliyun.com\n"
        )
        tk.Label(self.rodape_frame, text=rodape, font=("Arial", 10), justify=tk.LEFT).pack(anchor=tk.W)

    def log(self, mensagem): # Atualiza a área de log.
        self.log_area.insert(tk.END, mensagem + "\n")
        self.log_area.see(tk.END)
        
    def copiar_relatorio(self): # Copia o conteúdo do relatório para a área de transferência.
        try: # Obtém o texto do relatório
            relatorio_texto = self.relatorio_area.get(1.0, tk.END).strip()
            if relatorio_texto: # Copia para a área de transferência
                self.root.clipboard_clear()
                self.root.clipboard_append(relatorio_texto)
                self.root.update()  # Garante que o clipboard seja atualizado
                self.log("Relatório completo copiado para a área de transferência.")
            else:
                self.log("O relatório está vazio. Nada para copiar.")
        except Exception as e:
            self.log(f"Falha ao copiar o relatório completo: {str(e)}")

    def atualizar_relatorio(self, relatorio_texto): # Atualiza a área do relatório.
        self.relatorio_area.delete(1.0, tk.END)
        self.relatorio_area.insert(tk.END, relatorio_texto)

    def gerar_relatorio(self):
        url = self.link_entry.get().strip()
        if not url:
            self.log("Nenhuma URL fornecida. Por favor, insira o link do alerta.")
            return
        self.log("Iniciando o processo...")
        try:
            inicio = time.time()
            # Inicializa as classes
            mesorregiao = Mesorregiao()
            coletor = ColetorDados(url, self.log)
            try:
                # Etapa 1: Coletar dados gerais
                coletor.iniciar_driver()
                coletor.acessar_pagina()
                coletor.coletar_dados_gerais()
            except Exception as e:
                self.log(f"Falha na etapa de coleta de dados gerais: {str(e)}")
            try:
                # Etapa 2: Coletar municípios afetados
                coletor.clicar_veja_mais()
                coletor.alterar_linhas_por_pagina()
                coletor.coletar_dados_tabela()
            except Exception as e:
                self.log(f"Falha na etapa de coleta de municípios: {str(e)}")
            # Atualiza o atributo municipios_afetados
            self.municipios_afetados = coletor.municipios_afetados
            # Gera o relatório dos municípios
            relatorio = Relatorio(
                coletor.municipios_afetados,
                mesorregiao,
                self.log,
                self.atualizar_relatorio,
                coletor.dados_gerais,
                self.titulo_programa
            )
            relatorio.gerar_relatorio()
            # Calcula o tempo total de execução
            fim = time.time()
            tempo_total = fim - inicio
            self.log(f"Tempo total de execução: {tempo_total:.2f} segundos.")
        except Exception as e:
            self.log(f"Erro crítico: {str(e)}")
        finally:
            if coletor.driver:
                coletor.driver.quit()



if __name__ == "__main__":
    root = tk.Tk()  # Cria a janela principal do Tkinter
    app = App(root)  # Inicializa a aplicação
    root.mainloop()  # Inicia o loop principal da interface gráfica