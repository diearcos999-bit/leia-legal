import type { Metadata } from "next";
import { Inter, Lora } from "next/font/google";
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
    <html lang="es" className={`${inter.variable} ${lora.variable}`}>
      <body className="min-h-screen bg-background font-sans antialiased">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
