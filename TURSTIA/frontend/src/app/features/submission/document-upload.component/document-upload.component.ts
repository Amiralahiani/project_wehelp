import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-document-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './document-upload.component.html',
  styleUrls: ['./document-upload.component.css']
})
export class DocumentUploadComponent {

  @Output() documentsChange = new EventEmitter<any[]>();

  documents: any[] = [];
  @Input() submitted = false;


  toBase64(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const base64String = (reader.result as string).split(',')[1];
        resolve(base64String);
      };
      reader.onerror = error => reject(error);
    });
  }

  onFileSelected(event: Event, docType: string) {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    const reader = new FileReader();

    reader.onload = () => {
      const base64 = (reader.result as string).split(',')[1];

      const document = {
        doc_id: 'D' + (this.documents.length + 1),
        type: docType,
        filename: file.name,
        content: base64
      };

      this.documents.push(document);
      this.documentsChange.emit(this.documents);

      console.log('📎 Document ajouté :', document);
    };

    reader.readAsDataURL(file);
  }

  removeFile(index: number) {
    this.documents = this.documents.filter((_, i) => i !== index);
  }


}