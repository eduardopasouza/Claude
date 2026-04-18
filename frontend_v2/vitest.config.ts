/// <reference types="vitest" />
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "node:path";

/**
 * Vitest config alinhado com Next 16 / React 19 / Tailwind 4.
 *
 * Convenções:
 *   - Testes ficam colocados com o componente: foo.tsx + foo.test.tsx
 *   - Setup global em tests/setup.ts (cleanup + jest-dom)
 *   - Path alias @/ funciona como no Next (apontando pra src/)
 *   - jsdom é o env padrão (componentes React renderizam)
 *   - `vitest run` no CI, `vitest` watch no dev
 */
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    include: [
      "src/**/*.{test,spec}.{ts,tsx}",
      "tests/unit/**/*.{test,spec}.{ts,tsx}",
    ],
    exclude: [
      "node_modules",
      ".next",
      "tests/e2e/**",  // e2e usa Playwright, não Vitest
    ],
    coverage: {
      provider: "v8",
      reporter: ["text", "html", "lcov"],
      exclude: [
        "node_modules/**",
        ".next/**",
        "tests/**",
        "**/*.test.{ts,tsx}",
        "**/*.spec.{ts,tsx}",
        "**/*.d.ts",
        "next.config.*",
        "postcss.config.*",
        "tailwind.config.*",
      ],
      thresholds: {
        // Gate gradual. Eleva conforme a suite cresce.
        statements: 30,
        branches: 30,
        functions: 30,
        lines: 30,
      },
    },
  },
});
