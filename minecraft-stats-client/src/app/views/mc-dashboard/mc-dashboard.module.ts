import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlayerTimeComponent } from './components/player-time/player-time.component';
import { HistoricalPlayerTimeComponent } from './components/historical-player-time/historical-player-time.component';



@NgModule({
  declarations: [PlayerTimeComponent, HistoricalPlayerTimeComponent],
  imports: [
    CommonModule
  ],
  exports: [
    PlayerTimeComponent,
    HistoricalPlayerTimeComponent
  ]
})
export class McDashboardModule { }
