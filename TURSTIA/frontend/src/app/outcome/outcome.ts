import { Component, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators,ReactiveFormsModule  } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OutcomeService } from '../services/outcome';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button'; 
import { MatSnackBarModule } from '@angular/material/snack-bar'; 
import { MatIconModule } from '@angular/material/icon';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { trigger, transition, style, animate } from '@angular/animations';
import { Router } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { RouterModule } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';


@Component({
  selector: 'app-outcome',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    HttpClientModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatSnackBarModule,
    MatIconModule,
    CommonModule,
    RouterModule
],
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(-5px)' }),
        animate('200ms ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
      ])
    ])
  ],
  templateUrl: './outcome.html',
  styleUrl: './outcome.css',
})
export class Outcome implements OnDestroy {
  outcomeForm: FormGroup;
  loading = false;
  successMessage: string | null = null;
  private destroy$ = new Subject<void>();

  constructor(
    private fb: FormBuilder,
    private outcomeService: OutcomeService,
    private snackBar: MatSnackBar,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {
    this.outcomeForm = this.fb.group({
      case_id: ['', Validators.required],
      outcome: ['', Validators.required],
      loss_amount: [0]
    });
  }

  onOutcomeChange() {
    const outcome = this.outcomeForm.get('outcome')?.value;

    if (outcome === 'DEFAULT') {
      this.outcomeForm.get('loss_amount')?.setValidators([Validators.required, Validators.min(1)]);
    } else {
      this.outcomeForm.get('loss_amount')?.clearValidators();
      this.outcomeForm.get('loss_amount')?.setValue(0);
    }

    this.outcomeForm.get('loss_amount')?.updateValueAndValidity();
  }

  submit() {
    if (this.outcomeForm.invalid) {
      this.successMessage = null;
      this.snackBar.open(
        'Please fill all required fields',
        'Close',
        { duration: 3000 }
      );
      return;
    }

    setTimeout(() => {
      this.loading = true;
    });

    this.outcomeService.submitOutcome(this.outcomeForm.value)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: () => {
          this.successMessage = 'Outcome successfully updated';
          this.snackBar.open('Outcome successfully updated', 'Close', { duration: 3000 });
          this.outcomeForm.reset({
            case_id: '',
            outcome: '',
            loss_amount: 0
          });

          Object.keys(this.outcomeForm.controls).forEach(key => {
            this.outcomeForm.get(key)?.setErrors(null);
          });

          setTimeout(() => {
            this.loading = false;
          });
        },
        error: (err) => {
          console.error('Error submitting outcome:', err);
          this.successMessage = null;
          this.snackBar.open('Error while updating outcome: ' + (err?.error?.detail || 'Unknown error'), 'Close', { duration: 5000 });
          setTimeout(() => {
            this.loading = false;
          });
        }
      });
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  goToAudit() {
    this.router.navigate(['/audit']);
  }
}
