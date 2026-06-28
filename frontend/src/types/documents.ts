export type UploadedDocument = {
  id: string;
  original_filename: string;
  stored_filename: string;
  content_type: string;
  size_bytes: number;
  uploaded_at: string;
};

export type StoredDocument = {
  stored_filename: string;
  size_bytes: number;
  modified_at: string;
};

export type DocumentUploadResult = {
  documents: UploadedDocument[];
};

export type DocumentListResponse = {
  documents: StoredDocument[];
};

export type DocumentDeleteResponse = {
  stored_filename: string;
  deleted: boolean;
};

