"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

interface SourceBlockProps {
  title: string;
  source: string;
  data: unknown;
  isReference?: boolean;
}

export function SourceBlock({
  title,
  source,
  data,
  isReference,
}: SourceBlockProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="rounded-lg border border-[var(--border)] bg-agrojus-surface overflow-hidden">
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="w-full flex items-center justify-between p-4 hover:bg-agrojus-elevated transition-colors"
      >
        <div className="flex items-center gap-3 min-w-0">
          {isOpen ? (
            <ChevronDown className="w-4 h-4 shrink-0" />
          ) : (
            <ChevronRight className="w-4 h-4 shrink-0" />
          )}
          <span className="font-medium text-sm truncate">{title}</span>
          <span className="text-[var(--muted-foreground)] text-xs shrink-0">
            {source}
          </span>
        </div>
        {isReference && (
          <span className="text-[10px] border border-risk-medium/30 text-risk-medium rounded-full px-2 py-0.5 shrink-0 ml-2">
            Referencia
          </span>
        )}
      </button>

      {isOpen && (
        <div className="border-t border-[var(--border)] px-4 pb-4 pt-3">
          <pre className="text-xs font-mono text-[var(--muted-foreground)] overflow-auto max-h-64 whitespace-pre-wrap break-words">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
