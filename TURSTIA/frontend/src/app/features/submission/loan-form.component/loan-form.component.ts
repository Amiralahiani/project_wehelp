import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loan-form',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './loan-form.component.html',
  styleUrls: ['./loan-form.component.css']
})
export class LoanFormComponent implements OnInit{

  @Output() formChange = new EventEmitter<FormGroup>();

  @Input() submitted = false;
  
  form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      loan_amount: [null, [Validators.required, Validators.min(1)]],
      term_months: [null, [Validators.required, Validators.min(1)]],
      other_loans: [0, [Validators.min(0)]],
      product: ['', Validators.required],
      purpose: ['', Validators.maxLength(100)]
    });

    this.form.valueChanges.subscribe(() => {
      this.formChange.emit(this.form);
    });
  }
  onSubmit() {
    if (this.form.valid) {
      console.log('Form submitted', this.form.value);
    } else {
      console.log('Form is invalid');
    }
  }

  isInvalid(field: string): boolean {
    const control = this.form.get(field);
    return !!control && control.invalid && (this.submitted);
  }

  ngOnInit() {
    this.formChange.emit(this.form);
  }

}
