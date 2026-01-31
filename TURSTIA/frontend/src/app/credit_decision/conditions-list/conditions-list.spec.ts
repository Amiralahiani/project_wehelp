import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConditionsList } from './conditions-list';

describe('ConditionsList', () => {
  let component: ConditionsList;
  let fixture: ComponentFixture<ConditionsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConditionsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConditionsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
