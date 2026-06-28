import { apiRequest } from "./apiClient";
import type { DocumentDeleteResponse, DocumentListResponse, DocumentUploadResult } from "../types/documents";

export function listDocuments() {
  return apiRequest<DocumentListResponse>("/documents");
}

export function uploadDocuments(files: File[]) {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }

  return apiRequest<DocumentUploadResult>("/documents/upload", {
    method: "POST",
    body: formData,
  });
}

export function deleteDocument(storedFilename: string) {
  return apiRequest<DocumentDeleteResponse>(`/documents/${encodeURIComponent(storedFilename)}`, {
    method: "DELETE",
  });
}

