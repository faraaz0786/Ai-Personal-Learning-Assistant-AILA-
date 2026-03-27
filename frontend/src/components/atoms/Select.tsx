import { SelectHTMLAttributes } from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function Select({ className, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={twMerge(
        "w-full rounded-xl border border-surface-border bg-white px-4 py-3 text-sm text-surface-text-primary shadow-sm",
        "outline-none transition-all duration-300 appearance-none cursor-pointer",
        "focus:bg-white focus:border-primary-500/50 focus:ring-4 focus:ring-primary-500/10",
        className
      )}
      {...props}
    />
  );
}
