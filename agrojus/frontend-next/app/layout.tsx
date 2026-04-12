import type { Metadata } from "next";
import { Providers } from "./providers";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgroJus — Inteligencia Fundiaria e de Mercado",
  description:
    "Plataforma de inteligencia fundiaria, juridica, ambiental e de mercado para o agronegocio",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className="dark">
      <body className="min-h-screen antialiased">
        <Providers>
          <div className="flex">
            <Sidebar />
            <div className="flex-1 ml-60">
              <Topbar />
              <main className="p-6">{children}</main>
            </div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
