"use client";

import { useState, KeyboardEvent } from "react";
import { Loader2, Search } from "lucide-react";

interface DocInputProps {
  onSubmit: (value: string) => void;
  isLoading: boolean;
}

export function DocInput({ onSubmit, isLoading }: DocInputProps) {
  const [value, setValue] = useState("");

  function handleSubmit() {
    const digits = value.replace(/\D/g, "");
    if (digits.length >= 11) {
      onSubmit(digits);
    }
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      handleSubmit();
    }
  }

  return (
    <div className="flex gap-3 w-full">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="CPF (11 digitos) ou CNPJ (14 digitos)"
        disabled={isLoading}
        className="bg-agrojus-elevated border-[var(--border)] text-lg h-12 font-mono rounded-lg px-4 w-full text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-agrojus-emerald border"
      />
      <button
        onClick={handleSubmit}
        disabled={isLoading}
        className="h-12 px-6 bg-agrojus-emerald hover:bg-agrojus-emerald/80 text-white font-semibold rounded-lg flex items-center gap-2 shrink-0 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : (
          <Search className="w-5 h-5" />
        )}
        Auditar
      </button>
    </div>
  );
}
