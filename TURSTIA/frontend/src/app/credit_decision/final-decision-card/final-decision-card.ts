import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-final-decision-card',
  standalone: true,
  imports: [CommonModule,MatCardModule,MatIconModule],
  templateUrl: './final-decision-card.html',
  styleUrls: ['./final-decision-card.css']
})
export class FinalDecisionCard {
  @Input() decision: any;

  getDecisionClass(decision: string): string {
    const d = decision?.toUpperCase();

    if (d === 'ACCEPT' || d === 'APPROVED' || d === 'ACCEPT_WITH_GUARANTEE') {
      return 'APPROVED';
    }

    if (d === 'REJECT' || d === 'REJECTED') {
      return 'REJECTED';
    }

    if (d === 'HUMAN_REVIEW' || d === 'MANUAL') {
      return 'MANUAL';
    }

    return 'NEUTRAL';
  }

}
