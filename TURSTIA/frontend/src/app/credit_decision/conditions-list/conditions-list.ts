import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';     // ← for <mat-card>, <mat-card-content>
import { MatIconModule } from '@angular/material/icon';


@Component({
  selector: 'app-conditions-list',
  standalone: true,
  imports: [CommonModule,MatCardModule,MatIconModule],
  templateUrl: './conditions-list.html',
  styleUrls: ['./conditions-list.css']
})
export class ConditionsList {
  @Input() conditions: string[] = [];
}
