import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../services/auth-service';
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, MatIconModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {

  loginForm: FormGroup;
  showPassword = false;
  isRegisterMode = false;
  errorMsg = '';
  successMsg = '';

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });
  }

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  toggleMode(event: any) {
    event.preventDefault();
    this.isRegisterMode = !this.isRegisterMode;
    this.errorMsg = '';
    this.successMsg = '';
  }

  submit() {
    if (this.loginForm.invalid) return;

    if (this.isRegisterMode) {
      this.auth.register(this.loginForm.value).subscribe({
        next: (res: any) => {
          this.successMsg = 'Compte créé avec succès ! Connectez-vous.';
          this.isRegisterMode = false;
          this.errorMsg = '';
        },
        error: (err) => {
          this.errorMsg = err.error?.detail || 'Erreur lors de la création du compte';
        }
      });
    } else {
      this.auth.login(this.loginForm.value).subscribe({
        next: (res: any) => {
          this.auth.saveToken(res.access_token);
          this.router.navigate(['/expanded-submission']);
        },
        error: (err) => {
          this.errorMsg = 'Email ou mot de passe incorrect';
        }
      });
    }
  }
}
