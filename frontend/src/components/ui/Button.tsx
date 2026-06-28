import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import type { ButtonHTMLAttributes } from "react";

import { cn } from "../../utils/cn";

const buttonVariants = cva(
  "inline-flex h-10 items-center justify-center gap-2 rounded-md px-4 text-sm font-medium transition focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-emerald-600 text-white shadow-sm hover:bg-emerald-700",
        secondary: "border border-stone-200 bg-white text-stone-900 hover:bg-stone-50 dark:border-stone-800 dark:bg-stone-900 dark:text-stone-100",
        ghost: "text-stone-600 hover:bg-stone-100 hover:text-stone-950 dark:text-stone-300 dark:hover:bg-stone-900",
      },
      size: {
        default: "h-10 px-4",
        icon: "h-10 w-10 px-0",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "default",
    },
  },
);

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  };

export function Button({ className, variant, size, asChild = false, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";

  return <Comp className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}

