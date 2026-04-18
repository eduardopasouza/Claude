/**
 * Setup global do Vitest.
 *
 * - @testing-library/jest-dom adiciona matchers (toBeInTheDocument etc.)
 * - cleanup automático após cada teste (desmonta DOM)
 * - mock de matchMedia (alguns componentes usam)
 * - fetch é mockado explicitamente em cada teste via vi.spyOn ou msw
 */

import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeAll, vi } from "vitest";

afterEach(() => {
  cleanup();
});

beforeAll(() => {
  // matchMedia — não existe no jsdom
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: vi.fn().mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  });

  // IntersectionObserver (alguns componentes de scroll/viewport)
  class MockIntersectionObserver {
    observe = vi.fn();
    unobserve = vi.fn();
    disconnect = vi.fn();
    takeRecords = vi.fn().mockReturnValue([]);
    root = null;
    rootMargin = "";
    thresholds: readonly number[] = [];
  }
  window.IntersectionObserver =
    MockIntersectionObserver as unknown as typeof IntersectionObserver;

  // ResizeObserver (recharts, leaflet)
  class MockResizeObserver {
    observe = vi.fn();
    unobserve = vi.fn();
    disconnect = vi.fn();
  }
  window.ResizeObserver =
    MockResizeObserver as unknown as typeof ResizeObserver;
});
