"""
Demo video recorder final - Fixed URLs
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
    video_path = os.path.join(VIDEO_DIR, f"leia_demo_final_{timestamp}.webm")

    print(f"🎬 Iniciando grabacion demo final...")
    print(f"📁 Video: {video_path}")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=100
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

            # Scroll to show content
            await page.evaluate("window.scrollTo({ top: 300, behavior: 'smooth' })")
            await asyncio.sleep(2)

            # Back to top
            await page.evaluate("window.scrollTo({ top: 0, behavior: 'smooth' })")
            await asyncio.sleep(1.5)

            # ===== STEP 2: Use textarea to search =====
            print("📍 2. Usando barra de busqueda")

            # Wait for any textarea to appear and click it
            await page.wait_for_selector("textarea", timeout=10000)
            textarea = page.locator("textarea").first
            await textarea.click()
            await asyncio.sleep(0.5)

            # Type query
            await textarea.fill("Me despidieron sin finiquito")
            await asyncio.sleep(1)

            # Click send button
            send_button = page.locator("button[type='submit']").first
            await send_button.click()
            await asyncio.sleep(2)

            # ===== STEP 3: Chat page =====
            print("📍 3. Pagina de chat")
            try:
                await page.wait_for_url("**/chat**", timeout=10000)
            except:
                # Navigate directly if redirect didn't work
                await page.goto(f"{BASE_URL}/chat?q=Me%20despidieron%20sin%20finiquito", wait_until="networkidle")
            await asyncio.sleep(2)

            # ===== STEP 4: Wait for LEIA response =====
            print("📍 4. Esperando respuesta de LEIA...")
            await asyncio.sleep(10)  # Give time for AI response

            # Scroll to see content
            await page.evaluate("window.scrollTo({ top: 500, behavior: 'smooth' })")
            await asyncio.sleep(3)

            # ===== STEP 5: Dashboard Login =====
            print("📍 5. Navegando a login")
            # Correct URL is /login, not /auth/login
            await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
            await asyncio.sleep(3)

            # Fill login form
            print("📍 6. Login con credenciales demo")
            # Wait for form to load
            await page.wait_for_selector("input[type='email']", timeout=10000)

            await page.fill("input[type='email']", "demo@leia.cl")
            await asyncio.sleep(0.5)
            await page.fill("input[type='password']", "Demo1234")
            await asyncio.sleep(0.5)

            # Submit login
            await page.click("button[type='submit']")
            await asyncio.sleep(3)

            # ===== STEP 6: Dashboard =====
            print("📍 7. Dashboard principal")
            try:
                await page.wait_for_url("**/dashboard**", timeout=10000)
            except:
                await page.goto(f"{BASE_URL}/dashboard/usuario", wait_until="networkidle")
            await asyncio.sleep(3)

            # ===== STEP 7: Navigate sections =====
            print("📍 8. Seccion Abogados")
            await page.goto(f"{BASE_URL}/dashboard/abogados", wait_until="networkidle")
            await asyncio.sleep(3)

            print("📍 9. Seccion Mensajes")
            await page.goto(f"{BASE_URL}/dashboard/mensajes", wait_until="networkidle")
            await asyncio.sleep(3)

            print("📍 10. Seccion Tramites")
            await page.goto(f"{BASE_URL}/dashboard/tramites", wait_until="networkidle")
            await asyncio.sleep(2)

            # Final view
            print("📍 11. Vista final dashboard")
            await page.goto(f"{BASE_URL}/dashboard/usuario", wait_until="networkidle")
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
