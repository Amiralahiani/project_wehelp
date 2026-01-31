import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { OnInit } from '@angular/core';

@Component({
  selector: 'app-applicant-form',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './applicant-form.component.html',
  styleUrls: ['./applicant-form.component.css']
})
export class ApplicantFormComponent implements OnInit {

  @Output() formChange = new EventEmitter<FormGroup>();
  
  @Input() submitted = false;
  
  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      age: [null, [Validators.required, Validators.min(18), Validators.max(100)]],
      cin: [null, [Validators.required, Validators.pattern(/^[0-9]{8}$/)]],
      employment_type: ['', Validators.required],
      monthly_income_declared: [null, [Validators.required, Validators.min(0)]],
      monthly_expenses_declared: [null, [Validators.required, Validators.min(0)]],
      sector: ['', Validators.required],
      late_payments_declared: [null, [Validators.required, Validators.min(0)]]
    });

    this.form.valueChanges.subscribe(() => {
      this.formChange.emit(this.form);
    });
  }

  isInvalid(field: string): boolean {
    const control = this.form.get(field);
    return !!control && control.invalid && (this.submitted);
  }

  onSubmit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched(); // <-- force l’affichage des messages
      return;
    }
  }

  ngOnInit() {
    this.formChange.emit(this.form); 
  }

}
