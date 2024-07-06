import {
  Directive,
  ElementRef,
  HostBinding,
  HostListener,
  Renderer2,
} from '@angular/core';

@Directive({ selector: '[currency]' })
export class CurrencyDirective {
  constructor(
    private el: ElementRef<HTMLInputElement>,
    private renderer: Renderer2
  ) {}
  @HostListener('focus') focus() {
    this.renderer.setAttribute(this.el.nativeElement, 'type', 'number');
  }
  @HostListener('blur') blur() {
    this.renderer.setAttribute(this.el.nativeElement, 'type', 'text');
    if (this.el.nativeElement.value) {
      this.el.nativeElement.value = `${this.formatNumber(this.el.nativeElement.value)} руб.`;
    } else {
      this.el.nativeElement.value = '';
    }
  }
  private formatNumber(s: string) {
    return s.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ',');
  }
}
