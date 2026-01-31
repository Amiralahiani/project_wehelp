import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { AuditService } from '../services/audit';
import { ChangeDetectorRef } from '@angular/core';
import { debounceTime, takeUntil } from 'rxjs/operators';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';


@Component({
  selector: 'app-audit',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    CommonModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule
],
  templateUrl: './audit.html',
  styleUrl: './audit.css',
})
export class Audit implements OnInit {

  auditForm: FormGroup;
  loading = false;
  events: any[] = [];
  allEvents: any[] = []; 
  sortAsc = true;
  caseId: string = '';

  constructor(
    private fb: FormBuilder, 
    private auditService: AuditService,     
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer
  ) {
    this.auditForm = this.fb.group({
      case_id: ['']
    });
  }

  ngOnInit() {
    // Charger TOUS les audits dès l'ouverture de la page
    this.loadAllAudits();

    this.auditForm.get('case_id')?.valueChanges
      .pipe(
        debounceTime(300),
        
      )
      .subscribe(value => {
        console.log('valueChanges triggered with value:', value);

        if (!value || value.trim() === '') {
          console.log('Loading all audits');
          this.loadAllAudits();
        } else {
          console.log('Searching by case:', value);
          this.searchByCase();
        }
      });

    this.auditForm.get('case_id')?.setValue('', { emitEvent: false });
  }


  // Charger tous les audits
  loadAllAudits() {
    this.auditService.getAllAudits().subscribe({
      next: (data) => {
        this.allEvents = data;
        this.events = data; 
        this.cdr.markForCheck();
      },
      error: (error) => {
        console.error('Error loading audits:', error);
        this.allEvents = [];
        this.events = [];
        this.cdr.markForCheck();
      }
    });
  }

  highlightMatch(text: string, search: string): SafeHtml {
    if (!search || !text) return text;

    const escaped = search.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    const regex = new RegExp(`(${escaped})`, 'ig');
    const highlighted = text.replace(regex, `<span class="highlight">$1</span>`);

    return this.sanitizer.bypassSecurityTrustHtml(highlighted);
  }

  // Filtrer les événements localement
  filterEvents(searchTerm: string) {
    const term = (searchTerm ?? '').toLowerCase().trim();

    if (!term) {
      this.events = [...this.allEvents];
      return;
    }

    this.events = this.allEvents.filter(e =>
      (e.case_id ?? '').toLowerCase().includes(term)
    );

    this.cdr.markForCheck();
  }

  // Rechercher par case_id
  searchByCase() {
    const caseId = (this.auditForm.get('case_id')?.value ?? '').toString();
    this.filterEvents(caseId);
  }

  // Trier par date
  sortByDate() {
    this.sortAsc = !this.sortAsc;

    this.events.sort((a, b) => {
      const da = new Date(a.timestamp).getTime();
      const db = new Date(b.timestamp).getTime();
      return this.sortAsc ? da - db : db - da;
    });
  }

  sortByLossAmount() {
    // Inverser l'ordre à chaque clic
    this.sortAsc = !this.sortAsc;

    this.events.sort((a, b) => {
      // Récupérer loss_amount (ou 0 s'il n'existe pas)
      const la = a.payload_update?.loss_amount ?? 0;
      const lb = b.payload_update?.loss_amount ?? 0;

      return this.sortAsc ? la - lb : lb - la;
    });
  }
}