import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ApiModule, DefaultService } from './api';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SharedModule } from './shared/shared.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ContentComponent } from './content/content.component';
import { SearchComponent } from './search/search.component';
import { MaterialModule } from './shared/material.module';
import { AppStateService } from './core/appState';

@NgModule({
  declarations: [
    AppComponent,
    ContentComponent,
    SearchComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    ApiModule,
    BrowserAnimationsModule,
    MaterialModule,
    SharedModule,
  ],
  providers: [
    AppStateService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
