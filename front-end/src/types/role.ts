import type { Image } from './ui';

export interface Role {
  type: string;
  title: string;
  description: string;
  image: Image;
  path: string | { name: string; params?: Record<string, string> };
}
