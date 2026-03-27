import { ButtonHTMLAttributes, ReactNode } from "react";
import { motion, HTMLMotionProps } from "framer-motion";
import { twMerge } from "tailwind-merge";

type Variant = "primary" | "secondary" | "ghost" | "outline";
type Size = "sm" | "md" | "lg";

type ButtonProps = HTMLMotionProps<"button"> & {
  children: ReactNode;
  variant?: Variant;
  size?: Size;
};

const variants: Record<Variant, string> = {
  primary: "bg-primary-500 text-white shadow-soft hover:bg-primary-600 border-transparent transition-all",
  secondary: "bg-white border border-surface-border text-surface-text-secondary hover:border-primary-400 hover:text-primary-600 shadow-sm transition-all",
  outline: "bg-transparent border border-surface-border text-secondary-muted hover:bg-background-alt hover:border-surface-border transition-all",
  ghost: "bg-transparent text-secondary-muted hover:text-surface-text-primary hover:bg-background-alt transition-all"
};

const sizes: Record<Size, string> = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-5 py-2.5 text-sm",
  lg: "px-8 py-4 text-base"
};

export function Button({
  children,
  className = "",
  variant = "primary",
  size = "md",
  ...props
}: ButtonProps) {
  return (
    <motion.button
      whileHover={{ y: -1 }}
      whileTap={{ scale: 0.98 }}
      className={twMerge(
        "rounded-2xl font-bold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500/20 disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </motion.button>
  );
}
