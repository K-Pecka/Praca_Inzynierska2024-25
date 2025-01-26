export type ValidationRule = (value: string) => string | null;

export interface ValidationRules {
  [key: string]: string;
}
