# **AUTOSIMD (1.07)** - Relatório de Alertas INMET

O **AUTOSIMD** é uma ferramenta automatizada projetada por Bruno Lobão da Silva e desenvolvida inteiramente com suporte de inteligência artificial em Python para coletar dados de alertas meteorológicos do Instituto Nacional de Meteorologia (INMET) e gerar relatórios detalhados sobre municípios afetados no estado do Pará, classificados por mesoregião para facilitar a elaboração de boletins de alerta. O programa utiliza o Selenium para realizar web scraping e classifica os municípios por mesorregiões, facilitando a análise e tomada de decisões por parte do Corpo de Bombeiros Militar do Estado do Pará (CBMPA) e da Coordenadoria de Defesa Civil (CEDEC).

---

## **Recursos Principais**
- **Coleta Automática de Dados**: Extrai informações de alertas do INMET, incluindo avisos, grau de severidade e riscos potenciais.
- **Classificação por Mesorregião**: Organiza os municípios afetados por mesorregiões do estado do Pará.
- **Relatório Gerado Automaticamente**: Produz um relatório estruturado com todos os municípios afetados, dados gerais do alerta e resumo estatístico.
- **Interface Gráfica Amigável**: Fornece uma interface simples para inserir links de alertas e visualizar logs e relatórios.
- **Botões de Cópia**: Permite copiar rapidamente os municípios de cada mesorregião ou o relatório completo para a área de transferência.

---

## **Requisitos**

### **Dependências**
Certifique-se de que as seguintes bibliotecas estejam instaladas:

- `tkinter`: Para a interface gráfica.
- `selenium`: Para automação de navegador.
- `webdriver-manager`: Para gerenciar o ChromeDriver automaticamente (opcional).
- `datetime`: Para manipulação de datas e horas.

Instale as dependências necessárias com o seguinte comando:
```bash
pip install selenium
```

### **ChromeDriver**
O programa utiliza o Selenium com o Google Chrome. Certifique-se de ter o [Google Chrome](https://www.google.com/chrome/) instalado e baixe o [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatível com sua versão do navegador. Alternativamente, você pode usar o `webdriver-manager` para gerenciar automaticamente o ChromeDriver.

---

## **Como Executar**

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. **Instale as Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o ChromeDriver**:
   - Coloque o executável do ChromeDriver na mesma pasta do script ou configure o caminho no código usando a função `get_chromedriver_path()`.

4. **Execute o Programa**:
   ```bash
   python nome_do_arquivo.py
   ```

5. **Insira o Link do Alerta**:
   - Na interface gráfica, insira o link do alerta do INMET e clique em "Gerar Relatório".

---

## **Estrutura do Código**

### **Classes Principais**
1. **`Mesorregiao`**:
   - Gerencia as mesorregiões do estado do Pará e seus respectivos municípios.
   - Método `obter_mesorregiao(municipio)`: Retorna a mesorregião de um município específico.

2. **`ColetorDados`**:
   - Realiza o web scraping dos dados do INMET.
   - Métodos principais:
     - `iniciar_driver()`: Inicializa o driver do Selenium.
     - `acessar_pagina()`: Acessa a página do alerta.
     - `coletar_dados_gerais()`: Coleta informações gerais do alerta.
     - `clicar_veja_mais()`: Clica no botão "Veja Mais" para acessar a tabela de municípios.
     - `coletar_dados_tabela()`: Coleta os municípios afetados da tabela.

3. **`Relatorio`**:
   - Gera o relatório final com os municípios classificados por mesorregião.
   - Método `gerar_relatorio()`: Produz o relatório formatado.

4. **`App`**:
   - Interface gráfica principal do programa.
   - Permite inserir links, visualizar logs e relatórios, e copiar dados.

---

## **Exemplo de Relatório Gerado**

```
AUTOSIMD (1.07) - Relatório de Alertas INMET (CBMPA E DEFESA CIVIL)
------------------------------------------------------------------

Dados Gerais do Alerta
--------------------------------------------------
Aviso de: Chuva Intensa
Grau de Severidade: Alto
Riscos Potenciais: Alagamentos, Deslizamentos

Lista dos Municípios Afetados Pelo Alerta
--------------------------------------------------
Mesorregião: Metropolitana de Belém
Ananindeua, Belém, Marituba, Santa Bárbara do Pará

Mesorregião: Nordeste Paraense
Bragança, Castanhal, São Francisco do Pará

Municípios Não Classificados
--------------------------------------------------
Altamira, Novo Progresso

Total de municípios afetados: 10
Municípios não classificados: 2
Hora da coleta: 01/10/2023 14:30
```

---

## **Contribuições**
Contribuições são bem-vindas! Se você deseja melhorar o programa ou corrigir bugs, siga estas etapas:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m "Adiciona descrição da feature"
   ```
4. Envie as alterações para o GitHub:
   ```bash
   git push origin feature/nome-da-feature
   ```
5. Abra um pull request no repositório original.

---

## **Licença**
Este projeto está licenciado sob a **MIT License**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## **Créditos**
- **Desenvolvimento**: Bruno Lobão da Silva.
- **Fonte dos Dados**: [INMET - Alertas](https://alertas2.inmet.gov.br).
- **Plataformas de IA Utilizadas**:
  - [DeepSeek](https://www.deepseek.com)
  - [Qwen](https://qwen.aliyun.com)

---

Se precisar de ajuda ou tiver dúvidas, entre em contato! 😊
