import type { Metadata } from "next";
import { Inter, Outfit, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const fontSans = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

const fontHeading = Outfit({
  variable: "--font-heading",
  subsets: ["latin"],
});

const fontMono = JetBrains_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AgroJus Enterprise",
  description: "Plataforma de inteligência fundiária, ambiental e de mercado para o agronegócio.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="pt-BR"
      className={`dark ${fontSans.variable} ${fontHeading.variable} ${fontMono.variable} antialiased`}
    >
      <body className="min-h-screen bg-background font-sans text-foreground overflow-x-hidden">
         {children}
      </body>
    </html>
  );
}
