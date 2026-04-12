"use client";

import { User } from "lucide-react";
import { cn } from "@/lib/utils";

interface TopbarProps {
  className?: string;
}

export function Topbar({ className }: TopbarProps) {
  return (
    <header
      className={cn(
        "flex h-16 items-center px-4 gap-4 glass border-b border-[var(--border)]",
        className
      )}
    >
      {/* Placeholder spacer — future OmniSearch */}
      <div className="flex-1" />

      {/* User avatar */}
      <div
        className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-agrojus-elevated"
        aria-label="User menu"
      >
        <User size={16} className="text-[var(--muted-foreground)]" />
      </div>
    </header>
  );
}
