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
  public days = ['2020-02-27', '2020-02-28', '2020-03-01', '2020-03-02'];
  public loading = false;
  constructor(public mcApi: McApiService) {
    this.getPlayerTimesHistorical(this.days[0]);
  }

  ngOnInit(): void {
  }

  public getPlayerTimesHistorical(date) {
    this.selectedDay = date;
    this.times = [];
    this.loading = true;
    return this.mcApi.getPlayersTime(date).subscribe( (res: any) => {
      res = JSON.parse(res);
      console.log(res)
      // tslint:disable-next-line:forin
      for (const key in res.users) {
        this.times.push({
          player: res.users[key],
          startTime: res.start_time[key],
          endTime: res.end_time[key],
          delta: res.delta[key]
        });
      }
      console.log(this.times);
      this.loading = false;
    });
  }

}
