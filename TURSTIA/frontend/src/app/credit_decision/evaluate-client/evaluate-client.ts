import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EvaluateService } from '../../services/evaluate.service';
import { RiskFactorsPanel } from '../risk-factors-panel/risk-factors-panel';
import { ScenarioSimulatorTable } from '../scenario-simulator-table/scenario-simulator-table';
import { FinalDecisionCard } from '../final-decision-card/final-decision-card';
import { ConditionsList } from '../conditions-list/conditions-list';

@Component({
  selector: 'app-evaluate-client',
  standalone: true,
  imports: [CommonModule, FormsModule, RiskFactorsPanel, ScenarioSimulatorTable, FinalDecisionCard, ConditionsList],
  templateUrl: './evaluate-client.html'
})
export class EvaluateClientComponent {
  clientProfile = {
    monthly_income: 0,
    monthly_expenses: 0,
    debt_ratio: 0,
    job_stability: 0,
    top_similarity: 0
  };

  result: any = null;
  loading = false;

  constructor(private evaluateService: EvaluateService) {}

  onSubmit() {
    this.loading = true;
    this.evaluateService.evaluateClient(this.clientProfile).subscribe(res => {
      this.result = res;
      this.loading = false;
    }, err => {
      console.error(err);
      this.loading = false;
    });
  }
}
