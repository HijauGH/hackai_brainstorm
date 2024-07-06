import { NgModule } from '@angular/core';

import { MapComponent } from './map.component';
import { MapService } from './services/map.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@NgModule({
  imports: [HttpClientModule],
  exports: [MapComponent],
  declarations: [MapComponent],
  providers: [MapService],
})
export class MapModule {}
