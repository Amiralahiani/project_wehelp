import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'app-risk-factors-panel',
  standalone: true,
  imports: [CommonModule,MatCardModule,MatIconModule],
  templateUrl: './risk-factors-panel.html',
  styleUrls: ['./risk-factors-panel.css']
})
export class RiskFactorsPanel {
  @Input() riskSummary: any;


  getRiskLevelClass(factor: string): string {
    const lower = factor.toLowerCase();

    if (
      lower.includes('élevé') ||
      lower.includes('high') ||
      lower.includes('critique') ||
      lower.includes('important') ||
      lower.includes('grave')
    ) {
      return 'high';
    }

    if (
      lower.includes('moyen') ||
      lower.includes('medium') ||
      lower.includes('modéré')
    ) {
      return 'medium';
    }

    // default = low / faible / négligeable / etc.
    return 'low';
  }

  getRiskLevelLabel(factor: string): string | null {
    const lower = factor.toLowerCase();

    if (
      lower.includes('élevé') ||
      lower.includes('high') ||
      lower.includes('critique')
    ) {
      return 'Élevé';
    }

    if (
      lower.includes('moyen') ||
      lower.includes('medium') ||
      lower.includes('modéré')
    ) {
      return 'Moyen';
    }

    if (
      lower.includes('faible') ||
      lower.includes('low') ||
      lower.includes('négligeable')
    ) {
      return 'Faible';
    }

    // Si on ne détecte rien → on affiche rien (le fallback 'Risque moyen' est déjà dans le template)
    return null;
  }
}
