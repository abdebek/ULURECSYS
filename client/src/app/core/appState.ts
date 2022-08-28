import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { DefaultService } from '../api';
import { Article } from '../models/article';
import { Result } from '../shared/articles-table/result';

@Injectable({providedIn: 'root'})
export class AppStateService {
    _refreshResult = new BehaviorSubject<boolean>(true);
    refreshResult$ = this._refreshResult.asObservable();
    articles: Array<Article>  = Result as unknown as Array<Article>;
    _loading: boolean = false;
    constructor(
        private defaultService: DefaultService,
    ) { }

    get isLoading(){
      return this._loading;
    }

    fetchArticles(txt?: string){
      this._loading =  true;
      this.articles = [];
      this._refreshResult.next(true);
      this.defaultService.searchApiSearchPost(txt).subscribe((res =>{
        if(res) {
            this.articles = res;
            this._loading = false;
            this._refreshResult.next(true);
        }
      }));
    }
}