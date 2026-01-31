import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';

@Component({
    selector: 'app-risk-comparison-panel',
    standalone: true,
    imports: [CommonModule, MatCardModule, MatIconModule, MatProgressBarModule],
    templateUrl: './risk-comparison-panel.html',
    styleUrls: ['./risk-comparison-panel.css']
})
export class RiskComparisonPanel {
    @Input() riskComparison: any;

    getScoreColor(score: number): string {
        if (score < 0.2) return '#4caf50'; // Green
        if (score < 0.4) return '#ffeb3b'; // Yellow
        if (score < 0.6) return '#ff9800'; // Orange
        return '#f44336'; // Red
    }

    getRiskLevelLabel(score: number): string {
        if (score < 0.2) return 'Faible';
        if (score < 0.4) return 'Modéré';
        if (score < 0.6) return 'Sérieux';
        return 'Élevé';
    }
}
