import time
import os
from datetime import datetime, timedelta
import shutil
import locale
from pathlib import Path
from cryptography.fernet import Fernet
import sys
sys.path.append(r"R:\RPA\OwnBibliotecas\SistemaDeFilas")
from playwright.sync_api import sync_playwright
PATH_CODIGO = Path(__file__).resolve().parent
PATH_BACKLOG = Path(os.path.join(PATH_CODIGO,"backlog.txt"))
PATH_LOGS =  Path(os.path.join(PATH_CODIGO,"LOGS"))
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

usuario = os.getenv("FULLTRACK_USER")
senha = os.getenv("FULLTRACK_PASSWORD")
url = os.getenv("FULLTRACK_URL")

print(usuario)
print(url)
# pasta_download = fr"C:\Users\guilherme.henrique\OneDrive - 40205 - ASTERSEG ELETRONICA LTDA\Qualidade - Documentos\RESTRITO\11 - BASE DE DADOS\01 - RONDAS\02 - FULLTRACK"
pasta_download = os.path.join(PATH_CODIGO,"AmbDesenvolvi")
temp = r"C:\Temp"
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
data_ontem = datetime.now() - timedelta(days=1)
dia_ontem = data_ontem.strftime("%d")
mes_de_ontem = data_ontem.strftime("%m")
ano_de_ontem = data_ontem.strftime('%Y')
dia_ontem = (datetime.now() - timedelta(days=1)).strftime("%d") 
mes_extenso = data_ontem.strftime('%B')


def loginSite(p):
    browser = p.chromium.launch(headless=False, args=["--start-maximized", "--disable-blink-features=AutomationControlled"])
    context = browser.new_context(no_viewport=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")
    context.grant_permissions(
    ['notifications'],
    origin=(url)
    )
    pagina = context.new_page()
    pagina.goto(url, wait_until="commit", timeout=100000)
    pagina.get_by_role("textbox", name="Usuário").click()
    pagina.get_by_role("textbox", name="Usuário").fill(usuario)
    pagina.get_by_role("textbox", name="Senha").click()
    pagina.get_by_role("textbox", name="Senha").fill(senha)
    pagina.get_by_role("button", name="Entrar").click()
    return pagina

def relatorioPermanenciaEmPonto(pagina, posto):
    pagina.wait_for_load_state("networkidle")
    pagina.locator("a").nth(3).click()
    pagina.get_by_role("link", name=" Relatórios ").click()
    pagina.get_by_role("link", name=" Permanência em ponto").click()
    pagina.locator("#select2-id_grupo-container").click()
    pagina.get_by_role("treeitem", name=f"{posto}").click()
    pagina.locator(".icon.fa.fa-arrow-down").click()
    pagina.wait_for_timeout(3000)
    pagina.get_by_text("Ontem").click()
    pagina.get_by_role("button", name="Filtros").click()
    time.sleep(5)
    pagina.evaluate("window.scrollTo(0, 0)")
    pagina.locator("#btn_exportar_relatorio_em_massa").click()
    pagina.get_by_title("PDF").click()
    pagina.get_by_role("treeitem", name=" CSV").click()
    checkboxEmail = pagina.locator("#exportar_email")
    checkboxDownload = pagina.locator("#exportar_download")
    if not checkboxDownload.is_checked():
        checkboxDownload.check()
    if checkboxEmail.is_checked():
        checkboxEmail.uncheck()
    pagina.get_by_role("button", name=" Exportar").click()
    pagina.get_by_role("button", name="OK").click()

def relatorioTrajetoPercorrido(pagina, veiculo, posto):
    pagina.wait_for_load_state("networkidle")
    pagina.locator("a").nth(3).click()
    pagina.get_by_role("link", name=" Relatórios ").click()
    pagina.get_by_role("link", name=" Trajeto percorrido").click()
    pagina.locator("#select2-id_ativo-container").click()
    pagina.locator("input[type=\"search\"]").fill(f"{posto}")
    pagina.get_by_role("treeitem", name=f"{veiculo}").click()
    pagina.locator(".icon.fa.fa-arrow-down").click()
    pagina.get_by_text("Ontem").click()
    pagina.get_by_role("button", name="Filtros").click()
    time.sleep(5)
    pagina.evaluate("window.scrollTo(0, 0)")
    pagina.locator("#btn_exportar_relatorio_em_massa").click()
    pagina.get_by_title("PDF").click()
    pagina.get_by_role("treeitem", name=" CSV").click()
    checkboxEmail = pagina.locator("#exportar_email")
    checkboxDownload = pagina.locator("#exportar_download")
    if not checkboxDownload.is_checked():
        checkboxDownload.check()
    if checkboxEmail.is_checked():
        checkboxEmail.uncheck()
    pagina.get_by_role("button", name=" Exportar").click()
    pagina.get_by_role("button", name="OK").click()

def baixarRelatorioPermanencia(pagina, posto):
    for tentativa in range(100):
        try:
            pagina.locator("#btnMenuAvisos").click()
            item = pagina.locator("li.aviso-template", has_text="permanencia").last
            link = item.get_attribute("data-link-arquivo")
            with pagina.expect_download(timeout=300000) as download_info:
                pagina.evaluate(f"window.location.href = '{link}'")
            pagina.locator(".fa.fa-trash-o").first.click(force=True)
            pagina.get_by_role("button", name="Sim").dblclick()
            break
        except:
            print("Elemento não encontrado... Tentando novamente.")
            pagina.reload()
            time.sleep(2)
    download = download_info.value
    arquivoTemporario = os.path.join(temp, download.suggested_filename)
    arquivoFinal = os.path.join(pasta_download, fr"{ano_de_ontem}\{posto}\{mes_de_ontem} - {mes_extenso}\TEMPO DE PERMANÊNCIA", f"Permanência em Ponto - dia {dia_ontem}.csv")
    criarPasta = os.path.join(pasta_download, fr"{ano_de_ontem}\{posto}\{mes_de_ontem} - {mes_extenso}\TEMPO DE PERMANÊNCIA")
    criarPastaFinal = os.path.join(criarPasta)
    download.save_as(arquivoTemporario)
    os.makedirs(criarPastaFinal, exist_ok=True)
    shutil.move(arquivoTemporario, arquivoFinal)
    time.sleep(5)

def baixarRelatorioTrajeto(pagina, posto, veiculo):
    for tentativa in range(100):
        try:
            pagina.locator("#btnMenuAvisos").click()
            item = pagina.locator("li.aviso-template", has_text="trajeto").last
            link = item.get_attribute("data-link-arquivo")
            with pagina.expect_download(timeout=300000) as download_info:
                pagina.evaluate(f"window.location.href = '{link}'")
            pagina.locator(".fa.fa-trash-o").first.click(force=True)
            pagina.get_by_role("button", name="Sim").dblclick()
            break
        except:
            print("Elemento não encontrado... Tentando novamente.")
            pagina.reload()
            time.sleep(2)
    download = download_info.value
    arquivoTemporario = os.path.join(temp, download.suggested_filename)
    arquivoFinal = os.path.join(pasta_download, fr"{ano_de_ontem}\{posto}\{mes_de_ontem} - {mes_extenso}\TRAJETO PERCORRIDO", f"Trajeto Percorrido - {veiculo} - dia {dia_ontem}.csv")
    criarPasta = os.path.join(pasta_download, fr"{ano_de_ontem}\{posto}\{mes_de_ontem} - {mes_extenso}\TRAJETO PERCORRIDO")
    criarPastaFinal = os.path.join(criarPasta)
    download.save_as(arquivoTemporario)
    os.makedirs(criarPastaFinal, exist_ok=True)
    shutil.move(arquivoTemporario, arquivoFinal)
    time.sleep(5)

with sync_playwright() as p:
    # Login
    pagina = loginSite(p)
    
    ## Relatório de Trajeto Percorrido
    
    # Vila Nova Conceição
    '''relatorioTrajetoPercorrido(pagina, "GAW6H83", "vila nova concei")
    baixarRelatorioTrajeto(pagina, "VILA NOVA CONCEICAO", "GAW6H83")
    relatorioTrajetoPercorrido(pagina, "GEP - 4F35", "vila nova concei")
    baixarRelatorioTrajeto(pagina, "VILA NOVA CONCEICAO", "GEP4F35")'''
    
    ## Relatório de Permanência em Ponto
    
    # Vila Nova Conceição
    relatorioPermanenciaEmPonto(pagina, "Vila Nova Conceição")
    baixarRelatorioPermanencia(pagina, "VILA NOVA CONCEICAO")
    
    # Vila Madalena
    relatorioPermanenciaEmPonto(pagina, "Vila Madalena")
    baixarRelatorioPermanencia(pagina, "VILA MADALENA")
    
    # Jardim Lusitânia - Sojal
    relatorioPermanenciaEmPonto(pagina, "Sojal")
    baixarRelatorioPermanencia(pagina, "JARDIM LUSITANIA")
    
    # Fechar a pagina
    pagina.close()