import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def main():
    print("--- 🎵 GERADOR DE MOSAICO LAST.FM 🎵 ---")
    
    user_input = input("\n👤 Digite seu usuário do Last.fm: ").strip()
    if not user_input:
        print("❌ Usuário é obrigatório!")
        return

    print("\n📅 Escolha o Período:")
    print("1 - 1 Semana (7 dias)")
    print("2 - 1 Mês")
    print("3 - 3 Meses")
    print("4 - 6 Meses")
    print("5 - 1 Ano")
    print("6 - Tudo (Desde o início)")
    
    op_period = input("👉 Digite o número da opção (Padrão: 2): ").strip()
    
    period_map = {
        "1": "7day",
        "2": "1month",
        "3": "3month",
        "4": "6month",
        "5": "12month",
        "6": "overall"
    }
    period_value = period_map.get(op_period, "1month")
    print(f"✅ Selecionado: {period_value}")

    print("\n🖼️ Escolha o Tamanho do Mosaico:")
    print("1 - 3x3 (9 álbuns)")
    print("2 - 4x4 (16 álbuns)")
    print("3 - 5x5 (25 álbuns)")
    print("4 - 10x10 (100 álbuns)")
    
    op_size = input("👉 Digite o número da opção (Padrão: 1): ").strip()
    
    size_map = {
        "1": "3x3",
        "2": "4x4",
        "3": "5x5",
        "4": "10x10"
    }
    size_value = size_map.get(op_size, "3x3")
    print(f"✅ Selecionado: {size_value}")

    pasta_destino = "./biblioteca_mosaicos"
    if not os.path.exists(pasta_destino): os.makedirs(pasta_destino)

    print("\n🦊 Iniciando Firefox...")
    options = Options()
    
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        print("🌍 Acessando tapmusic.net...")
        driver.get("https://tapmusic.net/")
        
        url_inicial = driver.current_url

        input_user = driver.find_element(By.NAME, "user")
        input_user.clear()
        input_user.send_keys(user_input)

        dropdown_period = driver.find_element(By.NAME, "type")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_period)
        Select(dropdown_period).select_by_value(period_value)

        dropdown_size = driver.find_element(By.NAME, "size")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_size)
        Select(dropdown_size).select_by_value(size_value)

        print("🎨 Clicando em gerar...")
    
        btn_submit = driver.find_element(By.XPATH, "//*[@type='submit']")
        driver.execute_script("arguments[0].click();", btn_submit)

        print("⏳ Aguardando redirecionamento para a imagem (20s)...")

        WebDriverWait(driver, 20).until(lambda d: d.current_url != url_inicial)
        
        img_url = driver.current_url
        print(f"🔗 URL Capturada: {img_url}")

        if "tapmusic.net" in img_url:
            print("⬇️ Baixando arquivo...")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(img_url, headers=headers)
            
            if response.status_code == 200:
                nome = f"{user_input}_{period_value}_{size_value}_{datetime.now():%Y-%m-%d}.jpg"
                caminho = os.path.join(pasta_destino, nome)
                
                with open(caminho, 'wb') as f:
                    f.write(response.content)
                print(f"\n✅ SUCESSO! Salvo em: {caminho}")
            else:
                print(f"❌ Erro no download. Status: {response.status_code}")
        else:
            print("❌ A URL final não parece ser uma imagem.")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()