import { Component, OnInit } from '@angular/core';
import { McApiService } from '../../../../services/mc-api.service';

@Component({
  selector: 'app-historical-player-time',
  templateUrl: './historical-player-time.component.html',
  styleUrls: ['./historical-player-time.component.css']
})
export class HistoricalPlayerTimeComponent implements OnInit {
  public user: any;
  times = [];
  public selectedDay: string;
  public days;
  public loading = false;
  public daySelectorIndex = -1;
  public daySelectorOffset = 5;
  constructor(public mcApi: McApiService) {
    this.getHistoricalDays();
  }

  ngOnInit(): void {
  }

  private getHistoricalDays() {
    return this.mcApi.getPlayersHistoricalDays().subscribe( (res: string[]) => {
      this.days = res;
      this.selectedDay = this.days[this.days.length - 2];
      this.getPlayerTimesHistorical(this.days[this.days.length - 2]);
    } );
  }

  public getPlayerTimesHistorical(date) {
    this.selectedDay = date;
    this.loading = true;
    return this.mcApi.getPlayersTime(date).subscribe( (res: any) => {
      res = JSON.parse(res);
      this.times = [];
      // tslint:disable-next-line:forin
      for (const key in res.users) {
        this.times.push({
          player: res.users[key],
          startTime: res.start_time[key],
          endTime: res.end_time[key],
          delta: res.delta[key]
        });
      }
      this.loading = false;
    });
  }

  public prevDay() {
    if (this.daySelectorIndex > this.days.length * -1 + this.daySelectorOffset) {
      this.daySelectorIndex--;
    }
  }

  public nextDay() {
    if (this.daySelectorIndex < -1) {
      this.daySelectorIndex++;
    }
  }

}
