import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Painel de Rastreamento de Tráfego",
  description: "Dashboard para monitoramento de tráfego e cliques inválidos",
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="bg-gray-800 text-white p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-xl font-semibold">Painel de Rastreamento</h1>
          <nav>
            <Link href="/dashboard" className="px-3 py-2 hover:bg-gray-700 rounded">
              Visão Geral
            </Link>
            {/* Adicionar mais links de navegação aqui (Métricas, Logs, Configurações) */}
          </nav>
        </div>
      </header>
      <main className="flex-grow container mx-auto p-4 md:p-6 lg:p-8">
        {children}
      </main>
      <footer className="bg-gray-200 text-center p-4 text-sm text-gray-600">
        © 2025 Manus Team - Sistema de Rastreamento de Tráfego
      </footer>
    </div>
  );
}

