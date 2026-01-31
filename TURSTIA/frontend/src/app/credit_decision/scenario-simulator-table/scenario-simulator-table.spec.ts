import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-scenario-simulator-table',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './scenario-simulator-table.html',
  styleUrls: ['./scenario-simulator-table.css']
})
export class ScenarioSimulatorTable {
  @Input() scenarios: any[] = [];
}
