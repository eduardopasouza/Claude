# Frontend Phase 1: Scaffold + Layout + Dashboard + Consulta

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap a Next.js 14 dark-mode frontend with the core layout (sidebar + topbar), dashboard page, and consulta/due-diligence page — connected to the live FastAPI backend.

**Architecture:** Next.js 14 App Router with client-side data fetching via React Query. All API calls are client-side (no SSR for external APIs). Dark Forest/Onyx theme via TailwindCSS + shadcn/ui with custom CSS variables.

**Tech Stack:** Next.js 14, React 18, TypeScript, TailwindCSS 3, shadcn/ui, React Query (TanStack Query v5), Lucide React (icons)

**Design spec:** `agrojus/docs/plans/2026-04-11-frontend-nextjs14-design.md`

**Backend:** FastAPI running at `http://localhost:8000` (75 endpoints, 127 tests passing)

---

## File Structure (Phase 1)

```
agrojus/frontend-next/
├── app/
│   ├── layout.tsx           ← Root layout: dark theme, sidebar, topbar
│   ├── page.tsx             ← Dashboard
│   ├── consulta/page.tsx    ← Consulta / Due Diligence
│   ├── globals.css          ← Tailwind + custom CSS vars (Forest/Onyx palette)
│   └── providers.tsx        ← React Query provider
├── components/
│   ├── layout/
│   │   ├── sidebar.tsx
│   │   ├── topbar.tsx
│   │   ├── omni-search.tsx
│   │   └── api-status.tsx
│   ├── dashboard/
│   │   ├── kpi-card.tsx
│   │   └── news-feed.tsx
│   ├── consulta/
│   │   ├── doc-input.tsx
│   │   ├── risk-matrix.tsx
│   │   └── source-block.tsx
│   └── ui/                  ← shadcn/ui (auto-generated)
├── lib/
│   ├── api.ts               ← API client wrapper
│   ├── utils.ts             ← cn() helper
│   └── hooks/
│       ├── use-health.ts
│       ├── use-news.ts
│       └── use-consulta.ts
├── tailwind.config.ts
├── next.config.ts
├── tsconfig.json
├── package.json
├── postcss.config.mjs
├── components.json          ← shadcn/ui config
└── .env.local.example
```

---

### Task 1: Scaffold Next.js 14 project

**Files:**
- Create: `agrojus/frontend-next/` (entire scaffold)
- Create: `agrojus/frontend-next/.env.local.example`

- [ ] **Step 1: Create Next.js app**

```bash
cd agrojus
npx create-next-app@latest frontend-next --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*" --use-npm
```

When prompted:
- Would you like to use TypeScript? **Yes**
- Would you like to use ESLint? **Yes**
- Would you like to use Tailwind CSS? **Yes**
- Would you like your code inside a `src/` directory? **No**
- Would you like to use App Router? **Yes**
- Would you like to use Turbopack? **Yes**
- Would you like to customize the import alias? **Yes → @/***

- [ ] **Step 2: Install dependencies**

```bash
cd frontend-next
npm install @tanstack/react-query lucide-react
npm install -D @types/node
```

- [ ] **Step 3: Create .env.local.example**

```bash
# agrojus/frontend-next/.env.local.example
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Copy to `.env.local`:
```bash
cp .env.local.example .env.local
```

- [ ] **Step 4: Verify it runs**

```bash
npm run dev
```

Open http://localhost:3000 — should see default Next.js page.

- [ ] **Step 5: Commit**

```bash
cd .. && git add frontend-next/ -f
git commit -m "feat: scaffold Next.js 14 frontend with TypeScript + Tailwind"
```

---

### Task 2: Dark Forest/Onyx theme + shadcn/ui setup

**Files:**
- Modify: `agrojus/frontend-next/app/globals.css`
- Modify: `agrojus/frontend-next/tailwind.config.ts`
- Create: `agrojus/frontend-next/lib/utils.ts`
- Create: `agrojus/frontend-next/components.json`

- [ ] **Step 1: Initialize shadcn/ui**

```bash
cd agrojus/frontend-next
npx shadcn@latest init
```

When prompted:
- Style: **Default**
- Base color: **Neutral**
- CSS variables: **Yes**

- [ ] **Step 2: Replace globals.css with Forest/Onyx theme**

Replace the entire `app/globals.css` with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

@layer base {
  :root {
    --background: 150 20% 4%;
    --foreground: 140 40% 95%;
    --card: 150 18% 8%;
    --card-foreground: 140 40% 95%;
    --popover: 150 18% 8%;
    --popover-foreground: 140 40% 95%;
    --primary: 160 60% 40%;
    --primary-foreground: 140 40% 95%;
    --secondary: 150 10% 14%;
    --secondary-foreground: 140 20% 70%;
    --muted: 150 10% 14%;
    --muted-foreground: 150 12% 45%;
    --accent: 150 10% 14%;
    --accent-foreground: 140 40% 95%;
    --destructive: 0 72% 51%;
    --destructive-foreground: 0 0% 100%;
    --border: 150 10% 12%;
    --input: 150 10% 14%;
    --ring: 160 60% 40%;
    --radius: 0.75rem;

    /* Custom AgroJus tokens */
    --agrojus-bg-body: #0A0F0D;
    --agrojus-bg-surface: #111916;
    --agrojus-bg-elevated: #1A2420;
    --agrojus-bg-glass: rgba(17, 25, 22, 0.85);
    --agrojus-emerald: #10B981;
    --agrojus-emerald-glow: rgba(16, 185, 129, 0.15);
    --agrojus-risk-low: #10B981;
    --agrojus-risk-medium: #F59E0B;
    --agrojus-risk-high: #F97316;
    --agrojus-risk-critical: #EF4444;
  }
}

@layer base {
  body {
    @apply bg-[var(--agrojus-bg-body)] text-foreground;
    font-family: 'Inter', sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
  }
  code, pre {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
  }
}

/* Glassmorphism utility */
.glass {
  backdrop-filter: blur(16px);
  background: var(--agrojus-bg-glass);
  border: 1px solid hsl(var(--border));
}

/* Glow on hover */
.glow-hover:hover {
  box-shadow: 0 0 20px var(--agrojus-emerald-glow);
}

/* Scrollbar dark */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: var(--agrojus-bg-body);
}
::-webkit-scrollbar-thumb {
  background: hsl(var(--border));
  border-radius: 3px;
}
```

- [ ] **Step 3: Update tailwind.config.ts**

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        agrojus: {
          body: "var(--agrojus-bg-body)",
          surface: "var(--agrojus-bg-surface)",
          elevated: "var(--agrojus-bg-elevated)",
          emerald: "var(--agrojus-emerald)",
        },
        risk: {
          low: "var(--agrojus-risk-low)",
          medium: "var(--agrojus-risk-medium)",
          high: "var(--agrojus-risk-high)",
          critical: "var(--agrojus-risk-critical)",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        display: ["Outfit", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
```

- [ ] **Step 4: Create lib/utils.ts**

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Install clsx + tailwind-merge:
```bash
npm install clsx tailwind-merge tailwindcss-animate
```

- [ ] **Step 5: Verify — run dev and check dark background**

```bash
npm run dev
```

Open http://localhost:3000 — should see dark green-black background.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat: dark Forest/Onyx theme + shadcn/ui setup"
```

---

### Task 3: API client + React Query provider

**Files:**
- Create: `agrojus/frontend-next/lib/api.ts`
- Create: `agrojus/frontend-next/app/providers.tsx`
- Modify: `agrojus/frontend-next/app/layout.tsx`

- [ ] **Step 1: Create API client**

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  source?: string;
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const url = `${API_URL}${path}`;
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (res.status === 429) {
      const body = await res.json();
      return { data: null, error: body.detail || "Rate limit exceeded" };
    }

    if (!res.ok) {
      return { data: null, error: `HTTP ${res.status}` };
    }

    const data = await res.json();
    return { data: data as T, error: null };
  } catch (err) {
    return { data: null, error: err instanceof Error ? err.message : "Network error" };
  }
}

export async function apiGet<T>(path: string): Promise<ApiResponse<T>> {
  return apiFetch<T>(path);
}

export async function apiPost<T>(path: string, body: unknown): Promise<ApiResponse<T>> {
  return apiFetch<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function checkHealth(): Promise<{ online: boolean; latencyMs: number }> {
  try {
    const start = performance.now();
    const res = await fetch(`${API_URL}/health`);
    const latencyMs = Math.round(performance.now() - start);
    return { online: res.ok, latencyMs };
  } catch {
    return { online: false, latencyMs: 0 };
  }
}
```

- [ ] **Step 2: Create React Query provider**

```typescript
// app/providers.tsx
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
```

- [ ] **Step 3: Update root layout**

```typescript
// app/layout.tsx
import type { Metadata } from "next";
import { Providers } from "./providers";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgroJus — Inteligencia Fundiaria e de Mercado",
  description: "Plataforma de inteligencia fundiaria, juridica, ambiental e de mercado para o agronegocio",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className="dark">
      <body className="min-h-screen antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat: API client + React Query provider"
```

---

### Task 4: Sidebar + TopBar layout

**Files:**
- Create: `agrojus/frontend-next/components/layout/sidebar.tsx`
- Create: `agrojus/frontend-next/components/layout/topbar.tsx`
- Create: `agrojus/frontend-next/components/layout/api-status.tsx`
- Modify: `agrojus/frontend-next/app/layout.tsx`

- [ ] **Step 1: Install shadcn/ui components needed**

```bash
cd agrojus/frontend-next
npx shadcn@latest add button tooltip
npm install lucide-react
```

- [ ] **Step 2: Create Sidebar**

```typescript
// components/layout/sidebar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Search,
  Map,
  Shield,
  Scale,
  TrendingUp,
  Newspaper,
  Gavel,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { ApiStatus } from "./api-status";
import { useState } from "react";

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/consulta", label: "Consulta", icon: Search },
  { href: "/mapa", label: "Mapa GIS", icon: Map },
  { href: "/compliance", label: "Compliance", icon: Shield },
  { href: "/jurisdicao", label: "Jurisdicao", icon: Scale },
  { href: "/mercado", label: "Mercado", icon: TrendingUp },
  { href: "/noticias", label: "Noticias", icon: Newspaper },
  { href: "/processos", label: "Processos", icon: Gavel },
];

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 z-40 h-screen flex flex-col glass border-r border-border transition-all duration-300",
        collapsed ? "w-16" : "w-60"
      )}
    >
      {/* Brand */}
      <div className="flex items-center gap-3 px-4 h-16 border-b border-border">
        <div className="w-8 h-8 rounded-lg bg-agrojus-emerald/20 flex items-center justify-center text-agrojus-emerald font-bold text-sm">
          AJ
        </div>
        {!collapsed && (
          <div>
            <h1 className="font-display font-bold text-sm tracking-tight">AgroJus</h1>
            <span className="text-[10px] text-muted-foreground uppercase tracking-widest">
              Enterprise
            </span>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 space-y-1 px-2 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors",
                active
                  ? "bg-agrojus-emerald/15 text-agrojus-emerald"
                  : "text-muted-foreground hover:text-foreground hover:bg-agrojus-elevated"
              )}
            >
              <item.icon className="w-4 h-4 shrink-0" />
              {!collapsed && <span>{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Bottom: API Status + Collapse */}
      <div className="border-t border-border p-3 space-y-2">
        <ApiStatus collapsed={collapsed} />
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="w-full flex items-center justify-center py-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-agrojus-elevated transition-colors"
        >
          {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>
    </aside>
  );
}
```

- [ ] **Step 3: Create ApiStatus**

```typescript
// components/layout/api-status.tsx
"use client";

import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/lib/api";
import { cn } from "@/lib/utils";

export function ApiStatus({ collapsed }: { collapsed: boolean }) {
  const { data } = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 10000,
  });

  const online = data?.online ?? false;
  const latency = data?.latencyMs ?? 0;

  return (
    <div className="flex items-center gap-2 px-1">
      <div className="relative">
        <div
          className={cn(
            "w-2.5 h-2.5 rounded-full",
            online ? "bg-agrojus-emerald" : "bg-risk-critical"
          )}
        />
        {online && (
          <div className="absolute inset-0 w-2.5 h-2.5 rounded-full bg-agrojus-emerald animate-ping opacity-30" />
        )}
      </div>
      {!collapsed && (
        <div className="text-xs">
          <span className={cn("font-medium", online ? "text-agrojus-emerald" : "text-risk-critical")}>
            {online ? "Online" : "Offline"}
          </span>
          {online && (
            <span className="text-muted-foreground ml-1">{latency}ms</span>
          )}
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 4: Create TopBar**

```typescript
// components/layout/topbar.tsx
"use client";

import { User } from "lucide-react";

export function TopBar() {
  return (
    <header className="h-16 glass border-b border-border flex items-center justify-between px-6">
      {/* Placeholder for OmniSearch — Task 5 */}
      <div className="flex-1" />

      {/* User area */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-agrojus-elevated flex items-center justify-center">
          <User className="w-4 h-4 text-muted-foreground" />
        </div>
      </div>
    </header>
  );
}
```

- [ ] **Step 5: Update root layout to use Sidebar + TopBar**

```typescript
// app/layout.tsx
import type { Metadata } from "next";
import { Providers } from "./providers";
import { Sidebar } from "@/components/layout/sidebar";
import { TopBar } from "@/components/layout/topbar";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgroJus — Inteligencia Fundiaria e de Mercado",
  description: "Plataforma de inteligencia fundiaria, juridica, ambiental e de mercado para o agronegocio",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className="dark">
      <body className="min-h-screen antialiased">
        <Providers>
          <div className="flex">
            <Sidebar />
            <div className="flex-1 ml-60">
              <TopBar />
              <main className="p-6">{children}</main>
            </div>
          </div>
        </Providers>
      </body>
    </html>
  );
}
```

- [ ] **Step 6: Verify — sidebar + topbar visible with dark theme**

```bash
npm run dev
```

Open http://localhost:3000 — should see dark sidebar with 8 nav items + topbar.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "feat: sidebar + topbar layout with Forest/Onyx theme"
```

---

### Task 5: Dashboard page

**Files:**
- Create: `agrojus/frontend-next/components/dashboard/kpi-card.tsx`
- Create: `agrojus/frontend-next/components/dashboard/news-feed.tsx`
- Create: `agrojus/frontend-next/lib/hooks/use-health.ts`
- Create: `agrojus/frontend-next/lib/hooks/use-news.ts`
- Modify: `agrojus/frontend-next/app/page.tsx`

- [ ] **Step 1: Install shadcn card component**

```bash
npx shadcn@latest add card badge skeleton
```

- [ ] **Step 2: Create KpiCard**

```typescript
// components/dashboard/kpi-card.tsx
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { type LucideIcon } from "lucide-react";

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: "positive" | "negative" | "neutral";
}

export function KpiCard({ title, value, subtitle, icon: Icon, trend }: KpiCardProps) {
  return (
    <Card className="bg-agrojus-surface border-border glow-hover transition-all">
      <CardContent className="p-5">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wider">{title}</p>
            <h3 className="text-2xl font-display font-bold mt-1">{value}</h3>
            {subtitle && (
              <p
                className={cn(
                  "text-xs mt-1",
                  trend === "positive" && "text-risk-low",
                  trend === "negative" && "text-risk-critical",
                  (!trend || trend === "neutral") && "text-muted-foreground"
                )}
              >
                {subtitle}
              </p>
            )}
          </div>
          <div className="w-10 h-10 rounded-lg bg-agrojus-emerald/10 flex items-center justify-center">
            <Icon className="w-5 h-5 text-agrojus-emerald" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 3: Create useNews hook**

```typescript
// lib/hooks/use-news.ts
"use client";

import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";

interface NewsItem {
  title: string;
  summary: string;
  source: string;
  url: string;
  published: string;
  category: string;
}

interface NewsResponse {
  articles: NewsItem[];
  total: number;
}

export function useNews(limit = 6) {
  return useQuery({
    queryKey: ["news", limit],
    queryFn: async () => {
      const res = await apiGet<NewsResponse>(`/api/v1/news/?limit=${limit}`);
      return res.data;
    },
    staleTime: 5 * 60 * 1000,
  });
}
```

- [ ] **Step 4: Create NewsFeed**

```typescript
// components/dashboard/news-feed.tsx
"use client";

import { useNews } from "@/lib/hooks/use-news";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

export function NewsFeed() {
  const { data, isLoading } = useNews(6);

  if (isLoading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-16 w-full bg-agrojus-elevated" />
        ))}
      </div>
    );
  }

  const articles = data?.articles ?? [];

  return (
    <div className="space-y-2">
      {articles.map((article, i) => (
        <a
          key={i}
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="block p-3 rounded-lg bg-agrojus-surface border border-border hover:border-agrojus-emerald/30 transition-colors"
        >
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{article.title}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{article.source}</p>
            </div>
            <Badge variant="outline" className="text-[10px] shrink-0">
              {article.category}
            </Badge>
          </div>
        </a>
      ))}
    </div>
  );
}
```

- [ ] **Step 5: Build Dashboard page**

```typescript
// app/page.tsx
"use client";

import { Database, Search, FileText, Activity } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { checkHealth } from "@/lib/api";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { NewsFeed } from "@/components/dashboard/news-feed";

export default function DashboardPage() {
  const { data: health } = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    refetchInterval: 10000,
  });

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-display font-bold">Dashboard</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Visao geral da plataforma AgroJus
        </p>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="Fontes de Dados"
          value="13"
          subtitle="11/13 online"
          icon={Database}
          trend="positive"
        />
        <KpiCard
          title="Buscas Hoje"
          value="—"
          subtitle="Plano Free: 10/dia"
          icon={Search}
        />
        <KpiCard
          title="Relatorios/Mes"
          value="—"
          subtitle="Plano Free: 3/mes"
          icon={FileText}
        />
        <KpiCard
          title="Latencia API"
          value={health?.online ? `${health.latencyMs}ms` : "—"}
          subtitle={health?.online ? "Sistema online" : "Offline"}
          icon={Activity}
          trend={health?.online ? "positive" : "negative"}
        />
      </div>

      {/* News Feed */}
      <div>
        <h3 className="text-lg font-display font-semibold mb-4">Noticias Agro</h3>
        <NewsFeed />
      </div>
    </div>
  );
}
```

- [ ] **Step 6: Verify — dashboard with KPIs and news**

```bash
npm run dev
```

Start backend in another terminal:
```bash
cd agrojus/backend && uvicorn app.main:app --reload
```

Open http://localhost:3000 — should see 4 KPI cards + news feed. Latency card should show real value if backend is running.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "feat: dashboard page with KPI cards and news feed"
```

---

### Task 6: Consulta / Due Diligence page

**Files:**
- Create: `agrojus/frontend-next/components/consulta/doc-input.tsx`
- Create: `agrojus/frontend-next/components/consulta/risk-matrix.tsx`
- Create: `agrojus/frontend-next/components/consulta/source-block.tsx`
- Create: `agrojus/frontend-next/lib/hooks/use-consulta.ts`
- Create: `agrojus/frontend-next/app/consulta/page.tsx`

- [ ] **Step 1: Install shadcn input + tabs**

```bash
npx shadcn@latest add input tabs separator
```

- [ ] **Step 2: Create useConsulta hook**

```typescript
// lib/hooks/use-consulta.ts
"use client";

import { useMutation } from "@tanstack/react-query";
import { apiPost } from "@/lib/api";

export interface ConsultaResult {
  cpf_cnpj: string;
  risk_score: {
    overall: string;
    environmental: string;
    legal: string;
    labor: string;
    financial: string;
  };
  sources: Record<string, unknown>;
  [key: string]: unknown;
}

export function useConsulta() {
  return useMutation({
    mutationFn: async (cpfCnpj: string) => {
      const res = await apiPost<ConsultaResult>("/api/v1/consulta/completa", {
        cpf_cnpj: cpfCnpj,
      });
      if (res.error) throw new Error(res.error);
      return res.data!;
    },
  });
}
```

- [ ] **Step 3: Create DocInput**

```typescript
// components/consulta/doc-input.tsx
"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Loader2 } from "lucide-react";

interface DocInputProps {
  onSubmit: (value: string) => void;
  isLoading: boolean;
}

export function DocInput({ onSubmit, isLoading }: DocInputProps) {
  const [value, setValue] = useState("");

  const handleSubmit = () => {
    const clean = value.replace(/\D/g, "");
    if (clean.length >= 11) {
      onSubmit(clean);
    }
  };

  return (
    <div className="flex gap-3">
      <Input
        placeholder="CPF (11 digitos) ou CNPJ (14 digitos)"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        className="bg-agrojus-elevated border-border text-lg h-12 font-mono"
      />
      <Button
        onClick={handleSubmit}
        disabled={isLoading || value.replace(/\D/g, "").length < 11}
        className="h-12 px-6 bg-agrojus-emerald hover:bg-agrojus-emerald/80 text-white font-semibold"
      >
        {isLoading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <>
            <Search className="w-4 h-4 mr-2" />
            Auditar
          </>
        )}
      </Button>
    </div>
  );
}
```

- [ ] **Step 4: Create RiskMatrix**

```typescript
// components/consulta/risk-matrix.tsx
import { cn } from "@/lib/utils";

interface RiskMatrixProps {
  overall: string;
  environmental: string;
  legal: string;
  labor: string;
  financial: string;
}

const RISK_COLORS: Record<string, string> = {
  low: "bg-risk-low/20 text-risk-low border-risk-low/30",
  medium: "bg-risk-medium/20 text-risk-medium border-risk-medium/30",
  high: "bg-risk-high/20 text-risk-high border-risk-high/30",
  critical: "bg-risk-critical/20 text-risk-critical border-risk-critical/30",
};

function RiskCell({ label, level }: { label: string; level: string }) {
  const normalized = level?.toLowerCase() || "low";
  return (
    <div
      className={cn(
        "rounded-lg border p-4 text-center",
        RISK_COLORS[normalized] || RISK_COLORS.low
      )}
    >
      <p className="text-xs uppercase tracking-wider opacity-80">{label}</p>
      <p className="text-lg font-display font-bold mt-1 uppercase">{level || "—"}</p>
    </div>
  );
}

export function RiskMatrix({ overall, environmental, legal, labor, financial }: RiskMatrixProps) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
      <RiskCell label="Risco Geral" level={overall} />
      <RiskCell label="Ambiental" level={environmental} />
      <RiskCell label="Juridico" level={legal} />
      <RiskCell label="Trabalhista" level={labor} />
      <RiskCell label="Financeiro" level={financial} />
    </div>
  );
}
```

- [ ] **Step 5: Create SourceBlock**

```typescript
// components/consulta/source-block.tsx
"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface SourceBlockProps {
  title: string;
  source: string;
  data: unknown;
  isReference?: boolean;
}

export function SourceBlock({ title, source, data, isReference }: SourceBlockProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="rounded-lg border border-border bg-agrojus-surface overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-4 hover:bg-agrojus-elevated transition-colors"
      >
        <div className="flex items-center gap-3">
          {open ? (
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="w-4 h-4 text-muted-foreground" />
          )}
          <span className="font-medium text-sm">{title}</span>
        </div>
        <div className="flex items-center gap-2">
          {isReference && (
            <Badge variant="outline" className="text-[10px] text-risk-medium border-risk-medium/30">
              Referencia
            </Badge>
          )}
          <span className="text-xs text-muted-foreground">{source}</span>
        </div>
      </button>
      {open && (
        <div className="p-4 border-t border-border">
          <pre className="text-xs font-mono text-muted-foreground overflow-auto max-h-64">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 6: Build Consulta page**

```typescript
// app/consulta/page.tsx
"use client";

import { DocInput } from "@/components/consulta/doc-input";
import { RiskMatrix } from "@/components/consulta/risk-matrix";
import { SourceBlock } from "@/components/consulta/source-block";
import { useConsulta } from "@/lib/hooks/use-consulta";

export default function ConsultaPage() {
  const { mutate, data, isPending, error } = useConsulta();

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-display font-bold">Consulta Unificada</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Auditoria completa em 6 fontes simultaneas para qualquer CPF ou CNPJ
        </p>
      </div>

      <DocInput onSubmit={(doc) => mutate(doc)} isLoading={isPending} />

      {error && (
        <div className="p-4 rounded-lg bg-risk-critical/10 border border-risk-critical/30 text-risk-critical text-sm">
          {error.message}
        </div>
      )}

      {data && (
        <div className="space-y-6">
          {/* Risk Matrix */}
          <RiskMatrix
            overall={data.risk_score?.overall || "—"}
            environmental={data.risk_score?.environmental || "—"}
            legal={data.risk_score?.legal || "—"}
            labor={data.risk_score?.labor || "—"}
            financial={data.risk_score?.financial || "—"}
          />

          {/* Source Blocks */}
          <div className="space-y-3">
            <h3 className="text-lg font-display font-semibold">Fontes Consultadas</h3>
            {data.sources &&
              Object.entries(data.sources).map(([key, value]) => (
                <SourceBlock
                  key={key}
                  title={key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                  source={key}
                  data={value}
                  isReference={(value as Record<string, unknown>)?.is_reference === true}
                />
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 7: Verify — consulta page with live backend**

```bash
npm run dev
```

Navigate to http://localhost:3000/consulta. Type a CNPJ (e.g. `11222333000181`) and click Auditar. Should see risk matrix + collapsible source blocks.

- [ ] **Step 8: Commit**

```bash
git add -A && git commit -m "feat: consulta/due-diligence page with risk matrix and source blocks"
```

---

## Summary

| Task | What it builds | Est. time |
|------|---------------|-----------|
| 1 | Next.js 14 scaffold | 5 min |
| 2 | Dark Forest/Onyx theme + shadcn/ui | 10 min |
| 3 | API client + React Query | 5 min |
| 4 | Sidebar + TopBar layout | 15 min |
| 5 | Dashboard (KPIs + news) | 15 min |
| 6 | Consulta / Due Diligence | 20 min |

**Total: ~70 min for a working dark-mode frontend with 2 functional pages connected to live backend.**

Phase 2 (Mapa GIS, Compliance, Jurisdicao, Mercado, Noticias, Processos) will be planned after Phase 1 is running.
