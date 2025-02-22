export type ValidationRule = (value: string) => string | null;

export interface ValidationRules {
  [key: string]: string;
}
export const getDefaultMessages = () => {
  return {
    unknow: "Unknown error",
    required: "Field cannot be empty",
    minLength: "Field must be at least {0} characters long",
    maxLength: "Field cannot be longer than {0} characters",
    forbiddenChars: "Field contains forbidden character: {0}",
    equalLength: "Field must be exactly {0} characters long",
    pattern: "Field does not match the required pattern",
    email: "Invalid email format",
    number: "Field must be a number",
    startsWith: "Field must start with {0}",
    endsWith: "Field must end with {0}",
    isEqual: "Fields must be equal",
    isInRange: "Field must be between {0} and {1}",
    doCheckbox: "You must check this box.",
    minValue: "Value must be greater than {0}",
  };
};
