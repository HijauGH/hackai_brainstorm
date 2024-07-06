import { NgModule } from '@angular/core';
import { SelectComponent } from './select/select.component';
import { CommonModule } from '@angular/common';
import { ButtonComponent } from './button/button.component';

@NgModule({
  imports: [CommonModule],
  exports: [SelectComponent, ButtonComponent],
  declarations: [SelectComponent, ButtonComponent],
  providers: [],
})
export class UIModule {}
