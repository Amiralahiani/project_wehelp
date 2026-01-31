import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FinalDecisionCard } from './final-decision-card';

describe('FinalDecisionCard', () => {
  let component: FinalDecisionCard;
  let fixture: ComponentFixture<FinalDecisionCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FinalDecisionCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FinalDecisionCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
