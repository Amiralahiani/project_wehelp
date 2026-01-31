import { Routes } from '@angular/router';
import { Outcome } from './outcome/outcome';
import { Audit } from './audit/audit';
import { SubmissionPage } from './features/submission/submission.page/submission.page';
import { Login } from './login/login';
import { AuthGuard } from './guards/auth';
import { SimilarityRadar } from './similarity-radar/similarity-radar';
import { EvaluateClientComponent } from './credit_decision/evaluate-client/evaluate-client';
import { Dashboard } from './credit_decision/dashboard/dashboard';
import { ExpandedSubmissionComponent } from './features/submission/expanded-submission/expanded-submission.component';

export const routes: Routes = [
    { path: 'login', component: Login, title: 'Login' },
    { path: 'outcome', component: Outcome, title: 'Outcome Update', canActivate: [AuthGuard] },
    { path: 'audit', component: Audit, title: 'Audit Logs', canActivate: [AuthGuard] },
    { path: 'submission', component: SubmissionPage, title: 'Submission', canActivate: [AuthGuard] },
    { path: 'dashboard', component: Dashboard, title: 'Dashboard' },
    { path: 'similarity', component: SimilarityRadar, title: "Similarity radar" },
    { path: 'expanded-submission', component: ExpandedSubmissionComponent, title: 'Credit Application Extended', canActivate: [AuthGuard] },
    { path: 'evaluate', component: EvaluateClientComponent },
    { path: '', redirectTo: 'login', pathMatch: 'full' },
    { path: '**', redirectTo: 'login' }

]