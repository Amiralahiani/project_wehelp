export interface DocumentRef {
  doc_id: string;
  type: 'ID_CARD' | 'BANK_STATEMENT' | 'CONTRACT';
  uri: string;
}
