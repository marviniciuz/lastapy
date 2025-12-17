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
    print("--- 🎵 CONFIGURAÇÃO DO MOSAICO (MODO DEBUG) 🎵 ---")
    
    user_input = input("1. Digite seu usuário do Last.fm: ").strip()
    if not user_input: return

    print("\nOpções: 7day, 1month, 3month, 6month, 12month, overall")
    period_input = input("2. Digite o período (padrão '1month'): ").strip() or "1month"

    print("\nOpções: 3x3, 4x4, 5x5, 10x10")
    size_input = input("3. Digite o tamanho (padrão '3x3'): ").strip() or "3x3"

    pasta_destino = "./biblioteca_mosaicos"
    if not os.path.exists(pasta_destino): os.makedirs(pasta_destino)

    print("\n🦊 Iniciando o Firefox...")
    options = Options()
    
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    try:
        print("🌍 Acessando tapmusic.net...")
        driver.get("https://tapmusic.net/")

        driver.find_element(By.NAME, "user").send_keys(user_input)
        Select(driver.find_element(By.NAME, "type")).select_by_value(period_input)
        Select(driver.find_element(By.NAME, "size")).select_by_value(size_input)

        print("🎨 Clicando em gerar...")
        driver.find_element(By.XPATH, "//*[@type='submit']").click()

        print("⏳ Aguardando resultado (até 20s)...")
        
        try:
            img_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#img-creation"))
            )
            
            img_url = img_element.get_attribute("src")
            print(f"🔗 Link gerado: {img_url}")

            response = requests.get(img_url)
            if response.status_code == 200:
                nome = f"{user_input}_{period_input}_{size_input}_{datetime.now():%Y-%m-%d}.jpg"
                caminho = os.path.join(pasta_destino, nome)
                with open(caminho, 'wb') as f:
                    f.write(response.content)
                print(f"\n✅ SUCESSO! Salvo em: {caminho}")
            
        except Exception as e_wait:
            
            print("\n❌ A imagem não apareceu. Tirando print da tela para investigar...")
            
            caminho_erro = os.path.join(pasta_destino, "ERRO_TELA.png")
            driver.save_screenshot(caminho_erro)
            
            with open(os.path.join(pasta_destino, "ERRO_PAGINA.html"), "w", encoding="utf-8") as f:
                f.write(driver.page_source)
                
            print(f"⚠️  VERIFIQUE O ARQUIVO: {caminho_erro}")
            print("Abra essa imagem para ler a mensagem de erro que o site deu.")
            print(f"Erro técnico: {e_wait}")

    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()