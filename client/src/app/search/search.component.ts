import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { AppStateService } from '../core/appState';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  searchForm = new FormGroup({searchTxt: new FormControl('Lecture Notes in Machine Learning')});

  constructor(
    private appState: AppStateService,
  ) { }

  ngOnInit(): void {
    // this.search(); // for initial load, but this has been replaced by dummy sample json response.
   }


  search(){
    let txt = this.searchForm.get('searchTxt')?.value;
    if(!txt) return;
    this.appState.fetchArticles(txt);
  }
}
