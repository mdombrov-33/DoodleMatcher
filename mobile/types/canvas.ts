export interface Point {
  x: number;
  y: number;
}

export interface Stroke {
  points: Point[];
}

export type Match = {
  animal_type: string;
  confidence: number;
  photo_url: string;
  photographer: string;
};

export type SearchResult = {
  matches: Match[];
  search_time_ms: number;
};
