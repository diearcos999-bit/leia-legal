import type { Metadata } from "next";
import { Inter, Lora, Dancing_Script, Playfair_Display, Montserrat, Space_Grotesk, Sora, Great_Vibes, Pacifico } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
  weight: ["300", "400", "500", "600", "700"],
});

const lora = Lora({
  subsets: ["latin"],
  variable: "--font-lora",
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const dancingScript = Dancing_Script({
  subsets: ["latin"],
  variable: "--font-dancing",
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  display: "swap",
  weight: ["400", "500", "600", "700", "800", "900"],
});

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-montserrat",
  display: "swap",
  weight: ["300", "400", "500", "600", "700", "800", "900"],
});

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space",
  display: "swap",
  weight: ["300", "400", "500", "600", "700"],
});

const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sora",
  display: "swap",
  weight: ["300", "400", "500", "600", "700", "800"],
});

const greatVibes = Great_Vibes({
  subsets: ["latin"],
  variable: "--font-great-vibes",
  display: "swap",
  weight: "400",
});

const pacifico = Pacifico({
  subsets: ["latin"],
  variable: "--font-pacifico",
  display: "swap",
  weight: "400",
});

export const metadata: Metadata = {
  title: "LEIA - Tu asistente legal con IA",
  description: "Plataforma de servicios legales con IA + Marketplace de abogados verificados. Orientación legal inteligente 24/7.",
  keywords: ["abogados chile", "consulta legal", "IA legal", "justicia", "derecho chileno", "LEIA"],
  authors: [{ name: "LEIA" }],
  openGraph: {
    title: "LEIA - Tu asistente legal con IA",
    description: "Orientación legal inteligente 24/7 + Marketplace de abogados verificados",
    type: "website",
    locale: "es_CL",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${inter.variable} ${lora.variable} ${dancingScript.variable} ${playfair.variable} ${montserrat.variable} ${spaceGrotesk.variable} ${sora.variable} ${greatVibes.variable} ${pacifico.variable}`}>
      <body className="min-h-screen bg-background font-sans antialiased">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
