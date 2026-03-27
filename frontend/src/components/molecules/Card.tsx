import { ReactNode } from "react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

type CardProps = {
  title?: string;
  children: ReactNode;
  className?: string;
  noPadding?: boolean;
};

export function Card({ title, children, className, noPadding = false }: CardProps) {
  return (
    <section 
      className={twMerge(
        "rounded-[32px] border border-surface-border bg-white shadow-sm overflow-hidden transition-all duration-300 hover:shadow-md",
        !noPadding && "p-8 md:p-12",
        className
      )}
    >
      {title && (
        <div className="mb-8 border-b border-surface-border pb-6">
          <h2 className="text-2xl font-black text-slate-800 tracking-tight">
            {title}
          </h2>
        </div>
      )}
      <div className="text-slate-600 leading-relaxed font-medium">{children}</div>
    </section>
  );
}
