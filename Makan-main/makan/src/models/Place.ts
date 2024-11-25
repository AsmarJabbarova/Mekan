export interface Place {
    id: number;
  name: string;
  location: string;
  latitude?: number;
  longitude?: number;
  rating: number;
  description: string;
  entertainment_type_id: number;
  category_id?: number; 
  default_price?: number;
  images: string[];
  city: string;
}
  