import { DataSource } from '@angular/cdk/collections';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { map } from 'rxjs/operators';
import { Observable, of as observableOf, merge } from 'rxjs';
import { Article } from '../../models/article';
import { AppStateService } from 'src/app/core/appState';

/**
 * Data source for the ArticlesTable view. This class
 * encapsulates all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class ArticlesTableDataSource extends DataSource<Article> {
  data: Article[] = this.articles;
  paginator: MatPaginator | undefined;
  sort: MatSort | undefined;

  constructor(
      private appState: AppStateService,
    ) {
    super();
  }

  /**
   * Connect this data source to the table. The table will only update when
   * the returned stream emits new items.
   * @returns A stream of the items to be rendered.
   */
  connect(): Observable<Article[]> {
    if (this.paginator && this.sort) {
      // Combine everything that affects the rendered data into one update
      // stream for the data-table to consume.
      return merge(observableOf(this.data), this.paginator.page, this.sort.sortChange)
        .pipe(map(() => {
          return this.getPagedData(this.getSortedData([...this.data ]));
        }));
    } else {
      throw Error('Please set the paginator and sort on the data source before connecting.');
    }
  }


  disconnect(): void {}

  private getPagedData(data: Article[]): Article[] {
    if (this.paginator) {
      const startIndex = this.paginator.pageIndex * this.paginator.pageSize;
      return data.splice(startIndex, this.paginator.pageSize);
    } else {
      return data;
    }
  }


  private getSortedData(data: Article[]): Article[] {
    if (!this.sort || !this.sort.active || this.sort.direction === '') {
      return data;
    }

    return data.sort((a, b) => {
      const isAsc = this.sort?.direction === 'asc';
      switch (this.sort?.active) {
        case 'title': return compare(a.title, b.title, isAsc);
        case 'year': return compare(+a.year, +b.year, isAsc);
        case 'score': return compare(+a.score, +b.score, isAsc);
        default: return 0;
      }
    });
  }

  private get articles(){
    return this.appState.articles??[];
  }
}

function compare(a: string | number, b: string | number, isAsc: boolean): number {
  return (a < b ? -1 : 1) * (isAsc ? 1 : -1);
}
