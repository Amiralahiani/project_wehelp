import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FinalDecisionCard } from '../final-decision-card/final-decision-card';
import { RiskFactorsPanel } from '../risk-factors-panel/risk-factors-panel';
import { ScenarioSimulatorTable } from '../scenario-simulator-table/scenario-simulator-table';
import { ConditionsList } from '../conditions-list/conditions-list';
import { SimilarityRadar } from 'src/app/similarity-radar/similarity-radar';
import { CommonModule } from '@angular/common';

import { RiskComparisonPanel } from '../risk-comparison-panel/risk-comparison-panel';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    FinalDecisionCard,
    RiskFactorsPanel,
    ScenarioSimulatorTable,
    ConditionsList,
    SimilarityRadar,
    RiskComparisonPanel
  ],

  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {

  radarPoints: any[] = [];
  decisionResult: any;

  constructor(private router: Router) {
    const nav = this.router.getCurrentNavigation();
    this.decisionResult = nav?.extras?.state?.['decisionResult'];
  }

  ngOnInit(): void {

    if (!this.decisionResult) {
      this.router.navigate(['/submission']);
      return;
    }

    // ✅ UTILISER DIRECTEMENT CE QUE LE BACKEND FOURNIT
    this.radarPoints = this.decisionResult.radar_points || [];

    console.log('RADAR POINTS FROM BACKEND:', this.radarPoints);
  }

}