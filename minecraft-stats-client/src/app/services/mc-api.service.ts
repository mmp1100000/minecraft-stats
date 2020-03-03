import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class McApiService {
  private hostPrefix = 'http://127.0.0.1:5000/api';
  constructor(private http: HttpClient) { }

  getPlayersTime(day: string) {
    return this.http.get(`${this.hostPrefix}/players/time/${day}`);
  }

  getPlayersTimeCurrent() {
    return this.http.get(`${this.hostPrefix}/players/time/current`);
  }
  msToTime(duration) {
    // tslint:disable-next-line:prefer-const
    let milliseconds = parseInt(String((duration % 1000) / 100))
      , seconds: string | number = parseInt(String((duration / 1000) % 60))
      , minutes: string | number = parseInt(String((duration / (1000 * 60)) % 60))
      , hours: string | number = parseInt(String((duration / (1000 * 60 * 60)) % 24));

    hours = (hours < 10) ? '0' + hours : hours;
    minutes = (minutes < 10) ? '0' + minutes : minutes;
    seconds = (seconds < 10) ? '0' + seconds : seconds;

    return hours + ':' + minutes + ':' + seconds + '.' + milliseconds;
  }

}
