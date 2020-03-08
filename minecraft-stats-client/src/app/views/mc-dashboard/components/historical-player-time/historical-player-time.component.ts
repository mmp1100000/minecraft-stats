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
  public groupingChecked = true;
  constructor(public mcApi: McApiService) {
    this.getHistoricalDays();
  }

  private dataFunction: any;

  ngOnInit(): void {
  }

  private getHistoricalDays() {
    return this.mcApi.getPlayersHistoricalDays().subscribe( (res: string[]) => {
      this.days = res;
      this.days.push('');
      this.selectedDay = this.days[this.days.length - 2];
      this.getPlayerTimesHistorical(this.days[this.days.length - 2]);
    } );
  }

  public getPlayerTimesHistorical(date) {
    this.selectedDay = date;
    this.loading = true;
    return this.getDataFunction(date).subscribe( (res: any) => {
      res = JSON.parse(res);
      this.times = [];
      if (this.groupingChecked === true) {
        console.log(res);
        // tslint:disable-next-line: forin
        for (const key in res.delta) {
          this.times.push({
            player: key,
            delta: res.delta[key]
          });
        }
      } else {
        // tslint:disable-next-line: forin
        for (const key in res.users) {
          this.times.push({
            player: res.users[key],
            startTime: res.start_time[key],
            endTime: res.end_time[key],
            delta: res.delta[key]
          });
        }
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

  public changeGrouping(event) {
    this.groupingChecked = event.currentTarget.checked;
    this.getPlayerTimesHistorical(this.selectedDay);
  }


  private getDataFunction(date) {
    if (this.groupingChecked === true ) {
      return this.mcApi.getPlayersTimeGrouped(date);
    } else {
      return this.mcApi.getPlayersTime(date);
    }
  }

}
