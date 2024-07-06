import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MapModule } from './widgets/map/map.module';
import { HomeComponent } from './pages/home/home.component';

import { ReactiveFormsModule } from '@angular/forms';
import { UIModule } from './shared/ui/ui.module';
import { HeaderComponent } from './widgets/header/header.component';
import { CurrencyDirective } from './shared/directives/inputCurrency.directive';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    HeaderComponent,
    CurrencyDirective,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MapModule,
    ReactiveFormsModule,
    UIModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
