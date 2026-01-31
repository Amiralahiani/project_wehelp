import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RiskFactorsPanel } from './risk-factors-panel';

describe('RiskFactorsPanel', () => {
  let component: RiskFactorsPanel;
  let fixture: ComponentFixture<RiskFactorsPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RiskFactorsPanel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RiskFactorsPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
