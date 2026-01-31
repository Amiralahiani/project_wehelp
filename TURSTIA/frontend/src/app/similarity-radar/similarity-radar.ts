import { Component, Input, OnChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-similarity-radar',
  standalone: true,
  imports: [CommonModule, MatIconModule],
  templateUrl: './similarity-radar.html',
  styleUrl: './similarity-radar.css',
})
export class SimilarityRadar implements OnChanges {

  @Input() radarPoints: any[] = [];

  hoveredPoint: any = null;

  CENTER_X = 200;
  CENTER_Y = 200;
  MAX_RADIUS = 150;

  positionedPoints: any[] = [];

  // ngOnChanges() {
  //   if (this.radarPoints && this.radarPoints.length > 0) {
  //     this.positionedPoints = this.computeRadarPositions(this.radarPoints);
  //   }
  // }


  ngOnChanges() {
  console.log('Radar received:', this.radarPoints);

  if (this.radarPoints && this.radarPoints.length > 0) {
    this.positionedPoints = this.computeRadarPositions(this.radarPoints);
    console.log('Positioned:', this.positionedPoints);
  }
}



  // Retourne la couleur en fonction du type de point (tolère lowercase et nul)
  getColor(p: any): string {
    const t = (p?.type || '').toString().toUpperCase();
    if (t === 'CURRENT') return '#2ecc71'; // vert
    if (t === 'NORMAL')  return '#3498db'; // bleu
    if (t === 'FRAUD')   return '#e74c3c'; // rouge
    return '#95a5a6'; // gris
  }

  computeRadarPositions(radarPoints: any[]) {

    // Normaliser et filtrer les points invalides
    const normalized = (radarPoints || []).map(p => ({
      ...p,
      type: (p?.type || '').toString().toUpperCase(),
      score: Number(p?.score ?? 0)
    })).filter(p => {
      if (Number.isNaN(p.score)) {
        console.warn('[SimilarityRadar] skipping point with invalid score:', p);
        return false;
      }
      // clamp score between 0 and 1
      p.score = Math.max(0, Math.min(1, p.score));
      return true;
    });

    const current = normalized.find(p => p.type === 'CURRENT');
    const others = normalized.filter(p => p.type !== 'CURRENT');

    if (others.length === 0 && !current) return [];

    let i = 0;

    const positionedOthers = others.map((p) => {

      const angle = i * (2 * Math.PI / others.length);
      i++;

      const minRadius = 20; // pour ne pas coller au centre
      const radius = minRadius + (this.MAX_RADIUS - minRadius) * (1 - p.score);


      return {
        ...p,
        x: this.CENTER_X + radius * Math.cos(angle),
        y: this.CENTER_Y + radius * Math.sin(angle)
      };
    });

    // ✅ CURRENT TOUJOURS DESSINÉ EN DERNIER (AU-DESSUS)
    if (current) {
      positionedOthers.push({
        ...current,
        x: this.CENTER_X,
        y: this.CENTER_Y
      });
    }

    return positionedOthers;
  }



  // Gestion du survol des points 
  onMouseEnter(point: any) {
  this.hoveredPoint = point;
  }

  onMouseLeave() {
    this.hoveredPoint = null;
  }


}



  // computeRadarPositions(radarPoints: any[]) {

  //   const current = radarPoints.find(p => p.type === 'CURRENT');
  //   const others = radarPoints.filter(p => p.type !== 'CURRENT');
  //   let i = 0;

  //   return radarPoints.map((p) => {

  //     // CURRENT toujours au centre
  //     if (p.type === 'CURRENT') {
  //       return {
  //         ...p,
  //         x: this.CENTER_X,
  //         y: this.CENTER_Y
  //       };
  //     }

  //     // Angle réparti uniformément
  //     const angle = i * (2 * Math.PI / others.length);
  //     i++;

  //     const score = p.score ?? 0;
  //     const radius = this.MAX_RADIUS * (1 - score);

  //     return {
  //       ...p,
  //       x: this.CENTER_X + radius * Math.cos(angle),
  //       y: this.CENTER_Y + radius * Math.sin(angle)
  //     };
  //   });
  // }
