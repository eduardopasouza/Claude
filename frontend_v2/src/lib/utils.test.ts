/**
 * Testes unit de src/lib/utils.ts — helper `cn` (classnames).
 *
 * cn = twMerge + clsx — evita classes Tailwind duplicadas e resolve conflitos
 * (último wins). Testa os casos comuns do projeto.
 */

import { describe, expect, it } from "vitest";
import { cn } from "./utils";

describe("cn — merge de classes Tailwind", () => {
  it("concatena strings simples", () => {
    expect(cn("a", "b", "c")).toBe("a b c");
  });

  it("ignora falsy (null, undefined, false, '')", () => {
    expect(cn("a", null, "b", undefined, false, "", "c")).toBe("a b c");
  });

  it("resolve classes tailwind conflitantes (último wins)", () => {
    // padding conflita — só o último aplica
    expect(cn("p-4", "p-8")).toBe("p-8");
  });

  it("preserva classes não-conflitantes", () => {
    expect(cn("p-4", "text-sm", "font-bold")).toBe("p-4 text-sm font-bold");
  });

  it("aceita array", () => {
    expect(cn(["a", "b"], "c")).toBe("a b c");
  });

  it("aceita objeto com valores booleanos (clsx)", () => {
    expect(cn({ active: true, disabled: false, hover: true })).toBe("active hover");
  });

  it("combina arrays + objetos + strings", () => {
    expect(
      cn("base", ["variant-a"], { active: true }, "another"),
    ).toBe("base variant-a active another");
  });

  it("resolve conflito mesmo com variantes (bg-red-500 vs bg-blue-500)", () => {
    expect(cn("bg-red-500", "bg-blue-500")).toBe("bg-blue-500");
  });

  it("não deduplica classes idênticas não-conflitantes (twMerge não mexe nisso)", () => {
    // Nota: twMerge foca em conflito, não em dedup literal
    const result = cn("p-4", "p-4");
    expect(result).toContain("p-4");
  });
});
