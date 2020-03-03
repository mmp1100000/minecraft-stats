import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChartsModule } from 'ng2-charts';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { ButtonsModule } from 'ngx-bootstrap/buttons';

import { DashboardComponent } from './dashboard.component';
import { DashboardRoutingModule } from './dashboard-routing.module';
import { PlayerTimeComponent } from '../mc-dashboard/components/player-time/player-time.component';
import {CommonModule} from '@angular/common';
import { McDashboardModule } from '../mc-dashboard/mc-dashboard.module';

@NgModule({
  imports: [
    FormsModule,
    DashboardRoutingModule,
    ChartsModule,
    BsDropdownModule,
    ButtonsModule.forRoot(),
    CommonModule,
    McDashboardModule
  ], exports: [
  ], declarations: [ DashboardComponent]
})
export class DashboardModule { }
