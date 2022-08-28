import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticlesTableComponent } from './articles-table/articles-table.component';
import { MaterialModule } from './material.module';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';

@NgModule({
    imports: [
    CommonModule,
    MaterialModule,
  ],
  declarations: [ArticlesTableComponent,  HeaderComponent, FooterComponent, ],
  exports:[ArticlesTableComponent,  HeaderComponent, FooterComponent,  ],
})
export class SharedModule { }
