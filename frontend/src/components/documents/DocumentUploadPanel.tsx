import { useRef, useState, type ChangeEvent, type DragEvent } from "react";
import { Loader2, UploadCloud } from "lucide-react";

import { Button } from "../ui/Button";
import { Panel } from "../ui/Panel";
import { cn } from "../../utils/cn";

type DocumentUploadPanelProps = {
  isUploading: boolean;
  onUpload: (files: File[]) => void;
};

export function DocumentUploadPanel({ isUploading, onUpload }: DocumentUploadPanelProps) {
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);

  function handleFiles(files: FileList | null) {
    const pdfs = Array.from(files ?? []).filter((file) => file.type === "application/pdf" || file.name.endsWith(".pdf"));
    if (pdfs.length > 0) {
      onUpload(pdfs);
    }
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);
    handleFiles(event.dataTransfer.files);
  }

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    handleFiles(event.target.files);
    event.target.value = "";
  }

  return (
    <Panel className="p-5">
      <input ref={inputRef} type="file" accept="application/pdf" multiple className="hidden" onChange={handleInputChange} />
      <div
        onDragEnter={() => setIsDragging(true)}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={cn(
          "rounded-lg border border-dashed border-stone-300 bg-stone-50 p-8 text-center transition dark:border-stone-700 dark:bg-stone-900/60",
          isDragging && "border-emerald-500 bg-emerald-50 dark:border-emerald-400 dark:bg-emerald-950/40",
        )}
      >
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-lg bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
          {isUploading ? <Loader2 className="animate-spin" size={28} /> : <UploadCloud size={30} />}
        </div>
        <h3 className="mt-4 text-lg font-semibold">Upload PDFs</h3>
        <p className="mt-2 text-sm text-stone-500 dark:text-stone-400">Drop one or more PDF files here.</p>
        <Button className="mt-5" disabled={isUploading} onClick={() => inputRef.current?.click()}>
          {isUploading ? "Uploading" : "Choose files"}
        </Button>
      </div>
    </Panel>
  );
}

