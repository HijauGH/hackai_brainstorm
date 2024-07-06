/* eslint-disable @typescript-eslint/no-empty-function */
import {
  Component,
  ElementRef,
  forwardRef,
  Input,
  OnInit,
  Renderer2,
  ViewChild,
} from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

@Component({
  selector: 'app-select',
  templateUrl: './select.component.html',
  styleUrls: ['./select.component.scss'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => SelectComponent),
      multi: true,
    },
  ],
})
export class SelectComponent implements ControlValueAccessor {
  constructor(private renderer: Renderer2) {}
  @ViewChild('dropdown') dropdown!: ElementRef<HTMLDivElement>;
  @ViewChild('list') list!: ElementRef<HTMLDivElement>;
  @Input()
  options: { value: string }[] = [];
  @Input() placeholder = '';
  public isDropdownOpen = false;
  public value = '';
  public isTouched = false;
  private onChange: (value: string) => void = () => {};
  private onTouched: () => void = () => {};
  writeValue(value: string): void {
    this.value = value;
  }
  registerOnChange(fn: any): void {
    this.onChange = fn;
  }
  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }
  public setValue(value: string) {
    this.value = value;
    this.isTouched = true;
    this.onChange(value);
    this.onTouched();
    this.toggleDropdown();
  }
  public toggleDropdown() {
    const h = this.list.nativeElement.offsetHeight;

    if (this.isDropdownOpen) {
      this.renderer.setStyle(this.dropdown.nativeElement, 'height', '0px');
    } else {
      this.renderer.setStyle(this.dropdown.nativeElement, 'height', `${h}px`);
    }
    this.isDropdownOpen = !this.isDropdownOpen;
  }
}