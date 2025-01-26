import { ValidationRules } from './validationRules';

export const defaultMessages: ValidationRules = {
  unknow: 'Unknown error',
  required: 'Field cannot be empty',
  minLength: 'Field must be at least {0} characters long',
  maxLength: 'Field cannot be longer than {0} characters',
  forbiddenChars: 'Field contains forbidden character: {0}',
  equalLength: 'Field must be exactly {0} characters long',
  pattern: 'Field does not match the required pattern',
  email: 'Invalid email format',
  number: 'Field must be a number',
  startsWith: 'Field must start with {0}',
  endsWith: 'Field must end with {0}',
  isEqual: 'Fields must be equal',
  isInRange: 'Field must be between {0} and {1}',
};
