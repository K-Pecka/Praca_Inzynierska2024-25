import 'pinia';
import { Role } from './enum';

declare module 'pinia' {
  export interface PiniaCustomProperties {
    initialize: (payload: string) => void;
    reset: () => void;
  }
}