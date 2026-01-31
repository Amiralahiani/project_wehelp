import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimilarityRadar } from './similarity-radar';

describe('SimilarityRadar', () => {
  let component: SimilarityRadar;
  let fixture: ComponentFixture<SimilarityRadar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SimilarityRadar]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SimilarityRadar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
