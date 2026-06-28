import { motion } from "framer-motion";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ArrowUpRight, FileText, MessageSquareText, Search, ShieldCheck, UploadCloud, Zap } from "lucide-react";
import { useState } from "react";

import { Button } from "../components/ui/Button";
import { Panel } from "../components/ui/Panel";
import { DocumentUploadPanel } from "../components/documents/DocumentUploadPanel";
import { DocumentListPanel } from "../components/documents/DocumentListPanel";
import { Toast } from "../components/feedback/Toast";
import { deleteDocument, listDocuments, uploadDocuments } from "../services/documents";
import { ApiError } from "../services/apiClient";

const activity = [
  "Secure upload API online",
  "PDF extraction pipeline ready",
  "Streaming chat endpoint ready",
];

export function DashboardPage() {
  const queryClient = useQueryClient();
  const [toast, setToast] = useState<{ message: string; tone: "success" | "error" } | null>(null);
  const [deletingFilename, setDeletingFilename] = useState<string | undefined>();

  const documentsQuery = useQuery({
    queryKey: ["documents"],
    queryFn: listDocuments,
  });

  const uploadMutation = useMutation({
    mutationFn: uploadDocuments,
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      setToast({ tone: "success", message: `${result.documents.length} PDF uploaded.` });
    },
    onError: (error) => {
      setToast({ tone: "error", message: getErrorMessage(error) });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteDocument,
    onMutate: (storedFilename) => setDeletingFilename(storedFilename),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents"] });
      setToast({ tone: "success", message: "PDF deleted." });
    },
    onError: (error) => {
      setToast({ tone: "error", message: getErrorMessage(error) });
    },
    onSettled: () => setDeletingFilename(undefined),
  });

  const documents = documentsQuery.data?.documents ?? [];
  const stats = [
    { label: "Documents", value: String(documents.length), icon: FileText, accent: "text-emerald-700 dark:text-emerald-300" },
    { label: "Indexed chunks", value: "0", icon: Search, accent: "text-cyan-700 dark:text-cyan-300" },
    { label: "Conversations", value: "0", icon: MessageSquareText, accent: "text-amber-700 dark:text-amber-300" },
  ];

  return (
    <div className="mx-auto grid max-w-7xl gap-5">
      {toast ? <Toast message={toast.message} tone={toast.tone} onClose={() => setToast(null)} /> : null}
      <motion.section
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="grid gap-5 xl:grid-cols-[1.35fr_0.65fr]"
      >
        <Panel className="overflow-hidden p-5 sm:p-6">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="max-w-2xl">
              <div className="mb-4 inline-flex items-center gap-2 rounded-md border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950 dark:text-emerald-200">
                <ShieldCheck size={14} />
                Local-first PDF intelligence
              </div>
              <h2 className="text-3xl font-semibold tracking-normal text-stone-950 dark:text-white sm:text-4xl">
                Upload, index, search, and chat with private PDFs.
              </h2>
              <p className="mt-3 max-w-xl text-sm leading-6 text-stone-600 dark:text-stone-300">
                A focused workspace for turning document collections into cited answers using a local Ollama stack.
              </p>
            </div>
            <div className="grid min-w-64 gap-2">
              <Button className="justify-between">
                <span className="inline-flex items-center gap-2">
                  <UploadCloud size={18} />
                  Upload PDFs
                </span>
                <ArrowUpRight size={16} />
              </Button>
              <Button variant="secondary" className="justify-between">
                <span className="inline-flex items-center gap-2">
                  <MessageSquareText size={18} />
                  Open Chat
                </span>
                <ArrowUpRight size={16} />
              </Button>
            </div>
          </div>
        </Panel>

        <Panel className="p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-stone-500 dark:text-stone-400">System status</p>
              <h3 className="mt-1 text-lg font-semibold">Backend ready</h3>
            </div>
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300">
              <Zap size={19} />
            </div>
          </div>
          <div className="mt-5 space-y-3">
            {activity.map((item) => (
              <div key={item} className="flex items-center gap-3 text-sm text-stone-700 dark:text-stone-300">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                {item}
              </div>
            ))}
          </div>
        </Panel>
      </motion.section>

      <section className="grid gap-4 md:grid-cols-3">
        {stats.map((stat) => (
          <Panel key={stat.label} className="p-5">
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-stone-500 dark:text-stone-400">{stat.label}</p>
              <stat.icon className={stat.accent} size={20} />
            </div>
            <p className="mt-3 text-3xl font-semibold">{stat.value}</p>
          </Panel>
        ))}
      </section>

      <section className="grid gap-5 xl:grid-cols-[0.9fr_1.1fr]">
        <DocumentUploadPanel isUploading={uploadMutation.isPending} onUpload={(files) => uploadMutation.mutate(files)} />
        <DocumentListPanel
          documents={documents}
          isLoading={documentsQuery.isLoading}
          deletingFilename={deletingFilename}
          onDelete={(storedFilename) => deleteMutation.mutate(storedFilename)}
        />
      </section>

      {documentsQuery.isError ? (
        <Panel className="border-red-200 bg-red-50 p-4 text-sm text-red-900 dark:border-red-900 dark:bg-red-950 dark:text-red-100">
          {getErrorMessage(documentsQuery.error)}
        </Panel>
      ) : null}

      <section>
        <Panel className="p-5">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-stone-500 dark:text-stone-400">Chat preview</p>
              <h3 className="mt-1 text-lg font-semibold">Grounded answer workspace</h3>
            </div>
            <MessageSquareText className="text-cyan-700 dark:text-cyan-300" size={22} />
          </div>
          <div className="mt-5 space-y-3">
            <div className="max-w-[80%] rounded-lg bg-stone-100 p-3 text-sm dark:bg-stone-900">
              What does this PDF say about payment totals?
            </div>
            <div className="ml-auto max-w-[86%] rounded-lg bg-emerald-600 p-3 text-sm text-white">
              Answers will stream here with source citations.
            </div>
          </div>
        </Panel>
      </section>
    </div>
  );
}

function getErrorMessage(error: unknown) {
  if (error instanceof ApiError || error instanceof Error) {
    return error.message;
  }

  return "Something went wrong.";
}
