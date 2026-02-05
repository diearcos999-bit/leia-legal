"""
Demo video recorder v2 - More robust version
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
    video_path = os.path.join(VIDEO_DIR, f"leia_demo_v2_{timestamp}.webm")

    print(f"🎬 Iniciando grabacion demo v2...")
    print(f"📁 Video: {video_path}")

    async with async_playwright() as p:
        # Launch browser with slower motion for demo
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
            print("📍 1. Landing Page (nuevo tagline)")
            await page.goto(BASE_URL, wait_until="networkidle")
            await asyncio.sleep(2)

            # Scroll to show features
            await page.evaluate("window.scrollTo(0, 300)")
            await asyncio.sleep(1.5)

            # Back to top
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(1)

            # ===== STEP 2: Go to Chat =====
            print("📍 2. Navegando al chat")
            await page.click("text=Consultar Gratis")
            await page.wait_for_url("**/chat**", timeout=10000)
            await asyncio.sleep(2)

            # ===== STEP 3: Chat with LEIA =====
            print("📍 3. Chat con LEIA")

            # Wait for chat interface
            await page.wait_for_selector("textarea, input[type='text']", timeout=10000)
            await asyncio.sleep(1)

            # Type a message
            chat_input = page.locator("textarea, input[type='text']").first
            await chat_input.fill("Me despidieron sin pagar finiquito, que puedo hacer?")
            await asyncio.sleep(1)

            # Send message
            send_button = page.locator("button[type='submit']").first
            await send_button.click()
            await asyncio.sleep(1)

            # Wait for response (look for assistant message)
            print("📍 4. Esperando respuesta de LEIA...")
            try:
                await page.wait_for_selector("[class*='assistant'], [class*='bg-white'][class*='rounded']", timeout=30000)
                await asyncio.sleep(5)  # Let the full response render
            except:
                print("   ⚠️  Timeout esperando respuesta, continuando...")
                await asyncio.sleep(3)

            # Scroll to see full response
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

            # ===== STEP 4: Try Lawyer Button =====
            print("📍 5. Boton de abogados")
            try:
                lawyer_button = page.locator("text=Conectar con Abogado").first
                if await lawyer_button.is_visible():
                    await lawyer_button.click()
                    await asyncio.sleep(2)

                    # Close modal if open
                    close_button = page.locator("[class*='close'], button:has-text('×')").first
                    if await close_button.is_visible():
                        await close_button.click()
                        await asyncio.sleep(1)
            except:
                print("   ⚠️  Boton de abogados no encontrado")

            # ===== STEP 5: Dashboard - Login =====
            print("📍 6. Navegando a dashboard")
            await page.goto(f"{BASE_URL}/auth/login", wait_until="networkidle")
            await asyncio.sleep(2)

            # Fill login form
            print("📍 7. Login con credenciales demo")
            await page.fill("input[type='email']", "demo@leia.cl")
            await asyncio.sleep(0.5)
            await page.fill("input[type='password']", "Demo1234")
            await asyncio.sleep(0.5)

            # Submit
            await page.click("button[type='submit']")
            await asyncio.sleep(3)

            # ===== STEP 6: Dashboard =====
            print("📍 8. Dashboard")
            await page.wait_for_url("**/dashboard**", timeout=10000)
            await asyncio.sleep(2)

            # Navigate through dashboard sections
            sections = [
                ("Abogados", "abogados"),
                ("Mensajes", "mensajes"),
                ("Tramites", "tramites"),
            ]

            for name, path in sections:
                print(f"📍 9. Seccion: {name}")
                try:
                    await page.click(f"text={name}")
                    await asyncio.sleep(2)
                except:
                    # Try direct navigation
                    await page.goto(f"{BASE_URL}/dashboard/{path}", wait_until="networkidle")
                    await asyncio.sleep(2)

            # Final dashboard view
            await page.goto(f"{BASE_URL}/dashboard", wait_until="networkidle")
            await asyncio.sleep(2)

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
