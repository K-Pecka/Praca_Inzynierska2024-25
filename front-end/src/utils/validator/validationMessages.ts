import { useMessageStore } from "@/stores/";
export type ValidationRule = (value: string) => string | null;

export interface ValidationRules {
  [key: string]: string;
}
export const getDefaultMessages = () => {
    const { getValidationRules } = useMessageStore();
    return getValidationRules();
  };