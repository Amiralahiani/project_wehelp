export interface ApplicantForm {
  age: number;
  employment_type: 'Employee' | 'Freelance' | 'Unemployed';
  monthly_income_declared: number;
  monthly_expenses_declared: number;
  sector: string;
  late_payments_declared: number;
}
