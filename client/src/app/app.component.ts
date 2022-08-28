import { Component, OnInit } from '@angular/core';
import { DefaultService } from './api';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'UluRecsys: Hibrit Makale Öneri Sistemine Yönelik Derin Dikkat ve Çevrimiçi Öğrenme';

  constructor(
    private apiService: DefaultService,
  ){}

  ngOnInit(): void {
    
  }

  

}
