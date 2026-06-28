import { FileText, Loader2, Trash2 } from "lucide-react";

import { Button } from "../ui/Button";
import { Panel } from "../ui/Panel";
import { formatBytes, formatDateTime } from "../../utils/format";
import type { StoredDocument } from "../../types/documents";

type DocumentListPanelProps = {
  documents: StoredDocument[];
  isLoading: boolean;
  deletingFilename?: string;
  onDelete: (storedFilename: string) => void;
};

export function DocumentListPanel({ documents, isLoading, deletingFilename, onDelete }: DocumentListPanelProps) {
  return (
    <Panel className="p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-stone-500 dark:text-stone-400">Library</p>
          <h3 className="mt-1 text-lg font-semibold">Uploaded documents</h3>
        </div>
        {isLoading && <Loader2 className="animate-spin text-stone-400" size={20} />}
      </div>

      <div className="mt-5 space-y-3">
        {documents.length === 0 && !isLoading ? (
          <div className="rounded-lg border border-stone-200 bg-stone-50 p-6 text-sm text-stone-500 dark:border-stone-800 dark:bg-stone-900/60 dark:text-stone-400">
            No PDFs uploaded yet.
          </div>
        ) : null}

        {documents.map((document) => (
          <div
            key={document.stored_filename}
            className="flex items-center justify-between gap-4 rounded-lg border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-950"
          >
            <div className="flex min-w-0 items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-emerald-50 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300">
                <FileText size={19} />
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium">{document.stored_filename}</p>
                <p className="mt-1 text-xs text-stone-500 dark:text-stone-400">
                  {formatBytes(document.size_bytes)} · {formatDateTime(document.modified_at)}
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              aria-label={`Delete ${document.stored_filename}`}
              disabled={deletingFilename === document.stored_filename}
              onClick={() => onDelete(document.stored_filename)}
            >
              {deletingFilename === document.stored_filename ? <Loader2 className="animate-spin" size={17} /> : <Trash2 size={17} />}
            </Button>
          </div>
        ))}
      </div>
    </Panel>
  );
}

