import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-scenario-simulator-table',
  standalone: true,
  imports: [CommonModule,MatCardModule,MatIconModule],
  templateUrl: './scenario-simulator-table.html',
  styleUrls: ['./scenario-simulator-table.css'],
})
export class ScenarioSimulatorTable {
  @Input() scenarios: any[] = [];


  getVerdictClass(verdict: string): string {
  const v = verdict?.toUpperCase();

  if (v === 'BEST' || v === 'ACCEPT') return 'verdict-accept';
  if (v === 'REJECT') return 'verdict-reject';
  if (v === 'TRADE-OFF') return 'verdict-tradeoff';

  return 'verdict-neutral';
}


}
