export type Point = [string,string];
export interface ICreatePolygon {
  points: Point[];
  hintContent: string;
  fillColor: string;
}

export interface ICreatePoint {
  adSides?: number | null;
  gender?: string | null;
  ageFrom?: number | null;
  ageTo?: number | null;
  income?: string | null;
  type?: number | null;
}

export interface option {
  text: string;
  value: string;
}

export interface IGetPoints {
  coord_value: [
    {
      coord: Point[];
      value: number;
    },
  ];
  text: string;
  error: string;
}
