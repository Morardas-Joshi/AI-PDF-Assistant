import { X } from "lucide-react";

import { Button } from "../ui/Button";
import { cn } from "../../utils/cn";

type ToastProps = {
  message: string;
  tone: "success" | "error";
  onClose: () => void;
};

export function Toast({ message, tone, onClose }: ToastProps) {
  return (
    <div
      className={cn(
        "fixed bottom-5 right-5 z-50 flex max-w-sm items-center gap-3 rounded-lg border px-4 py-3 text-sm shadow-soft",
        tone === "success"
          ? "border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-900 dark:bg-emerald-950 dark:text-emerald-100"
          : "border-red-200 bg-red-50 text-red-900 dark:border-red-900 dark:bg-red-950 dark:text-red-100",
      )}
    >
      <span className="min-w-0">{message}</span>
      <Button variant="ghost" size="icon" className="h-7 w-7 shrink-0" onClick={onClose} aria-label="Close notification">
        <X size={15} />
      </Button>
    </div>
  );
}

