import 'pinia';
import { Role } from './enum';

declare module 'pinia' {
  export interface PiniaCustomProperties {
    initialize: () => void;
    reset: () => void;
  }
}