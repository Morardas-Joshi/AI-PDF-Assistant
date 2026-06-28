import type { HTMLAttributes } from "react";

import { cn } from "../../utils/cn";

export function Panel({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <section
      className={cn(
        "rounded-lg border border-stone-200 bg-white/86 shadow-soft backdrop-blur dark:border-stone-800 dark:bg-stone-950/72",
        className,
      )}
      {...props}
    />
  );
}

