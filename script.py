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
    print("--- 🎵 GERADOR DE MOSAICO (ANTI-ADS) 🎵 ---")
    
    user_input = input("1. Digite seu usuário do Last.fm: ").strip()
    if not user_input: return

    period_input = input("2. Período (Enter para '1month'): ").strip() or "1month"
    size_input = input("3. Tamanho (Enter para '3x3'): ").strip() or "3x3"
    
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
        Select(dropdown_period).select_by_value(period_input)

        dropdown_size = driver.find_element(By.NAME, "size")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_size)
        Select(dropdown_size).select_by_value(size_input)

        print("🎨 Clicando em gerar (Forçando via JS)...")
        
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
                nome = f"{user_input}_{period_input}_{size_input}_{datetime.now():%Y-%m-%d}.jpg"
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
        driver.save_screenshot("ERRO_NOVO.png")
        print("📸 Print do erro salvo como ERRO_NOVO.png")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()