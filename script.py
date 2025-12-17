import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select

# --- CONFIGURAÇÕES ---
LASTFM_USER = "SEU_USUARIO_AQUI"
PERIOD = "1month"  # Opções do tapmusic: 7day, 1month, 3month, 6month, 12month, overall
SIZE = "3x3"       # Tamanho do grid
PASTA_DESTINO = "./biblioteca_mosaicos"

def main():
    # 1. Cria a pasta se não existir (Sua "Mini Biblioteca")
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)
        print(f"Pasta '{PASTA_DESTINO}' criada.")

    print("🤖 Iniciando o robô...")
    
    # Configura o navegador (instala o driver automaticamente)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Descomente se quiser rodar sem ver a janela abrindo
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # 2. Acessa o Tapmusic
        print("🌍 Acessando tapmusic.net...")
        driver.get("https://tapmusic.net/")

        # 3. Preenche o formulário (Insere o usuário)
        input_user = driver.find_element(By.NAME, "user")
        input_user.clear()
        input_user.send_keys(LASTFM_USER)

        # Seleciona o período (1 mês)
        select_period = Select(driver.find_element(By.NAME, "type"))
        select_period.select_by_value(PERIOD)

        # Seleciona o tamanho (3x3)
        select_size = Select(driver.find_element(By.NAME, "size"))
        select_size.select_by_value(SIZE)

        # Clica no botão de gerar
        print("🎨 Gerando mosaico...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        # 4. Espera a imagem carregar e pega o Link
        # O Tapmusic carrega uma nova página ou atualiza a img. Vamos dar um tempo.
        time.sleep(5) 
        
        # Encontra a imagem gerada (geralmente tem um ID ou está dentro de uma div específica)
        # Nota: A estrutura do site pode mudar, mas geralmente a imagem principal está numa tag img clara
        img_element = driver.find_element(By.CSS_SELECTOR, "#img-creation") 
        img_url = img_element.get_attribute("src")
        
        print(f"🔗 Link da imagem encontrado: {img_url}")

        # 5. Baixa a imagem para sua pasta (Biblioteca/Drive)
        response = requests.get(img_url)
        
        if response.status_code == 200:
            # Cria um nome automático: mosaico_2023-10-25.jpg
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            nome_arquivo = f"mosaico_{PERIOD}_{data_hoje}.jpg"
            caminho_completo = os.path.join(PASTA_DESTINO, nome_arquivo)

            with open(caminho_completo, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Sucesso! Imagem salva em: {caminho_completo}")
        else:
            print("❌ Erro ao baixar a imagem final.")

    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()