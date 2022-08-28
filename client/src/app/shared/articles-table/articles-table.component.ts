import { AfterViewInit, Component, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { Subscription } from 'rxjs';
import { AppStateService } from 'src/app/core/appState';
import { Article } from '../../models/article';
import { ArticlesTableDataSource, } from './articles-table-datasource';

@Component({
  selector: 'articles-table',
  templateUrl: './articles-table.component.html',
  styleUrls: ['./articles-table.component.scss']
})
export class ArticlesTableComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatTable) table!: MatTable<Article>;
  dataSource!: MatTableDataSource<Article>;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['title', 'year', 'score']; // 
  resultSub!: Subscription | undefined;

  constructor(
    private appState: AppStateService,
  ) {
    this.dataSource = new MatTableDataSource<Article>();
  }

  ngOnInit(): void {
    this.appState.refreshResult$.subscribe((hasBeenUpdated) => {
      if(hasBeenUpdated) {
        this.dataSource.data = this.appState.articles;
       if(this.dataSource && this.table) this.setDataSource();
      }
    });
  }

  ngOnDestroy(): void {
    this.appState._refreshResult.next(false);
    this.resultSub = undefined;
  }

  ngAfterViewInit(): void {
    this.setDataSource();
  }

  setDataSource(){
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.table.dataSource = this.dataSource;
  }

  get isLoading(){
      return this.appState.isLoading;
  }
}
