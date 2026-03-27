import { InputHTMLAttributes } from "react";
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Input({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={twMerge(
        "w-full rounded-xl border border-surface-border bg-white px-4 py-3 text-sm text-surface-text-primary placeholder:text-secondary-muted shadow-sm",
        "outline-none transition-all duration-300",
        "focus:bg-white focus:border-primary-500/50 focus:ring-4 focus:ring-primary-500/10 focus:shadow-sm",
        className
      )}
      {...props}
    />
  );
}
