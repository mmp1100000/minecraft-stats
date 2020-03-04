/* tslint:disable:radix */
import { Component, OnInit } from '@angular/core';
import {McApiService} from '../../../../services/mc-api.service';

@Component({
  selector: 'app-player-time',
  templateUrl: './player-time.component.html',
  styleUrls: ['./player-time.component.css']
})
export class PlayerTimeComponent implements OnInit {
  public user: any;
  times = [];

  constructor(public mcApi: McApiService) {
    this.getPlayerTimesDelta();
  }
  ngOnInit(): void {
  }

  private getPlayerTimesDelta() {
    return this.mcApi.getPlayersTimeCurrent().subscribe( (res: any) => {
      res = JSON.parse(res);
      // tslint:disable-next-line:forin
      for (const key in res.users) {
        this.times.push({
          player: res.users[key],
          startTime: res.start_time[key],
          endTime: res.end_time[key],
          delta: res.delta[key]
        });
      }
    });
  }
}
