"""
Demo video recorder v3 - Fixed selectors
Records the complete LEIA flow with all UX improvements
"""
import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import os

# Config
BASE_URL = "http://localhost:3000"
VIDEO_DIR = "/Users/solangemendez/Desktop/Leia/justiciaai-mvp/videos"

async def record_demo():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join(VIDEO_DIR, f"leia_demo_v3_{timestamp}.webm")

    print(f"🎬 Iniciando grabacion demo v3...")
    print(f"📁 Video: {video_path}")

    async with async_playwright() as p:
        # Launch browser with slower motion for demo
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=150
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=VIDEO_DIR,
            record_video_size={"width": 1280, "height": 720}
        )

        page = await context.new_page()

        try:
            # ===== STEP 1: Landing Page =====
            print("📍 1. Landing Page")
            await page.goto(BASE_URL, wait_until="networkidle")
            await asyncio.sleep(3)  # Let animations finish

            # Scroll to show features
            await page.evaluate("window.scrollTo({ top: 400, behavior: 'smooth' })")
            await asyncio.sleep(2)

            # Show legal areas
            print("📍 2. Areas legales")
            await page.evaluate("window.scrollTo({ top: 800, behavior: 'smooth' })")
            await asyncio.sleep(2)

            # Back to top
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            await asyncio.sleep(1.5)

            # ===== STEP 2: Use HeroSearch to go to chat =====
            print("📍 3. Usando HeroSearch")
            # Type in the hero search
            hero_input = page.locator("input[placeholder*='Cuentame'], textarea[placeholder*='Cuentame']").first
            await hero_input.click()
            await asyncio.sleep(0.5)
            await hero_input.fill("Me despidieron sin finiquito")
            await asyncio.sleep(1)

            # Press enter or click search button
            await hero_input.press("Enter")
            await asyncio.sleep(2)

            # Wait for navigation to chat
            print("📍 4. Navegando al chat")
            await page.wait_for_url("**/chat**", timeout=10000)
            await asyncio.sleep(2)

            # ===== STEP 3: Chat with LEIA =====
            print("📍 5. Esperando respuesta de LEIA...")

            # Wait for chat messages to appear
            try:
                await page.wait_for_selector("[class*='message'], [class*='chat']", timeout=15000)
                await asyncio.sleep(8)  # Let the AI response fully render
            except:
                print("   ⚠️  Chat area no encontrada exactamente, esperando...")
                await asyncio.sleep(5)

            # Scroll down to see full response
            chat_container = page.locator("[class*='overflow-y-auto']").first
            await chat_container.evaluate("el => el.scrollTo(0, el.scrollHeight)")
            await asyncio.sleep(2)

            # ===== STEP 4: Look for lawyer connection button =====
            print("📍 6. Boton de abogados")
            try:
                await page.wait_for_selector("text=Conectar con Abogado", timeout=5000)
                lawyer_button = page.locator("text=Conectar con Abogado").first
                await lawyer_button.click()
                await asyncio.sleep(3)

                # Close modal
                print("📍 7. Cerrando modal")
                close_button = page.locator("button:has-text('×'), [aria-label='Close']").first
                if await close_button.is_visible():
                    await close_button.click()
                    await asyncio.sleep(1)
            except:
                print("   ⚠️  Boton de abogados no visible aun")

            # ===== STEP 5: Dashboard - Login =====
            print("📍 8. Navegando a login")
            await page.goto(f"{BASE_URL}/auth/login", wait_until="networkidle")
            await asyncio.sleep(2)

            # Fill login form
            print("📍 9. Login con credenciales demo")
            email_input = page.locator("input[type='email']")
            await email_input.fill("demo@leia.cl")
            await asyncio.sleep(0.5)

            password_input = page.locator("input[type='password']")
            await password_input.fill("Demo1234")
            await asyncio.sleep(0.5)

            # Submit
            submit_button = page.locator("button[type='submit']")
            await submit_button.click()
            await asyncio.sleep(3)

            # ===== STEP 6: Dashboard =====
            print("📍 10. Dashboard")
            try:
                await page.wait_for_url("**/dashboard**", timeout=10000)
            except:
                await page.goto(f"{BASE_URL}/dashboard", wait_until="networkidle")
            await asyncio.sleep(3)

            # Navigate through dashboard sections
            print("📍 11. Explorando secciones del dashboard")

            # Abogados
            try:
                await page.click("text=Abogados")
                await asyncio.sleep(3)
            except:
                await page.goto(f"{BASE_URL}/dashboard/abogados", wait_until="networkidle")
                await asyncio.sleep(2)

            # Mensajes
            try:
                await page.click("text=Mensajes")
                await asyncio.sleep(3)
            except:
                await page.goto(f"{BASE_URL}/dashboard/mensajes", wait_until="networkidle")
                await asyncio.sleep(2)

            # Tramites
            try:
                await page.click("text=Tramites")
                await asyncio.sleep(2)
            except:
                await page.goto(f"{BASE_URL}/dashboard/tramites", wait_until="networkidle")
                await asyncio.sleep(2)

            # Back to dashboard home
            print("📍 12. Dashboard home")
            await page.goto(f"{BASE_URL}/dashboard", wait_until="networkidle")
            await asyncio.sleep(3)

            print("✅ Grabacion completada!")

        except Exception as e:
            print(f"❌ Error durante grabacion: {e}")
            import traceback
            traceback.print_exc()

        finally:
            # Close and get video path
            await page.close()
            video = page.video
            if video:
                final_path = await video.path()
                print(f"📹 Video guardado: {final_path}")

            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(record_demo())
