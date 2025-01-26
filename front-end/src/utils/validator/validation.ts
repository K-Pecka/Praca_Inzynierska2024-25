import { ValidationRule, ValidationRules } from './validationRules';
import { defaultMessages } from './validationMessages';

export class Validator {
  private rules: ValidationRule[] = [];
  private errorMessage: ValidationRules = {};
  private rulesBase: ValidationRule[] = [];
  public constructor(errorMessage?: ValidationRules, rules?: ValidationRule[]) {
    if (rules) {
      this.rules = rules;
    }
    this.errorMessage = {
      ...defaultMessages,
      ...errorMessage,
    };
  }
  private formatMessage(template: string, ...args: any[]): string {
    return template.replace(/{(\d+)}/g, (_, index) => args[index] || '');
  }

  isEmpty(): this {
    this.rules.push((value: string,accept = false) => {
      return value.trim() === ''? this.errorMessage.required : null;
    });
    return this;
  }

  minLength(length: number): this {
    this.rules.push((value: string) => {
      return value.length < length
        ? this.formatMessage(this.errorMessage.minLength, length)
        : null;
    });
    return this;
  }

  maxLength(length: number): this {
    this.rules.push((value: string) => {
      return value.length > length
        ? this.formatMessage(this.errorMessage.maxLength, length)
        : null;
    });
    return this;
  }

  equalLength(length: number): this {
    this.rules.push((value: string) => {
      return value.length !== length
        ? this.formatMessage(this.errorMessage.equalLength, length)
        : null;
    });
    return this;
  }

  forbiddenChars(chars: string[]): this {
    this.rules.push((value: string) => {
      const found = chars.find((char) => value.includes(char));
      return found
        ? this.formatMessage(this.errorMessage.forbiddenChars, found)
        : null;
    });
    return this;
  }

  pattern(regex: RegExp): this {
    this.rules.push((value: string) => {
      return !regex.test(value) ? this.errorMessage.pattern : null;
    });
    return this;
  }

  email(): this {
    this.rules.push((value: string) => {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return !emailRegex.test(value) ? this.errorMessage.email : null;
    });
    return this;
  }

  number(): this {
    this.rules.push((value: string) => {
      return isNaN(Number(value)) ? this.errorMessage.number : null;
    });
    return this;
  }

  startsWith(prefix: string): this {
    this.rules.push((value: string) => {
      return !value.startsWith(prefix) ? this.formatMessage(this.errorMessage.startsWith, prefix) : null;
    });
    return this;
  }

  endsWith(suffix: string): this {
    this.rules.push((value: string) => {
      return !value.endsWith(suffix) ? this.formatMessage(this.errorMessage.endsWith, suffix) : null;
    });
    return this;
  }

  isEqual(compareValue: string): this {
    this.rules.push((value: string) => {
      return value !== compareValue ? this.errorMessage.isEqual : null;
    });
    return this;
  }

  isInRange(min: number, max: number): this {
    this.rules.push((value: string) => {
      const numericValue = Number(value);
      return numericValue < min || numericValue > max
        ? this.formatMessage(this.errorMessage.isInRange, min, max)
        : null;
    });
    return this;
  }

  addCustomRule(rule: ValidationRule, message: string): this {
    this.rules.push((value: string) => {
      const error = rule(value);
      return error ? message : null;
    });
    return this;
  }
  save(): Validator {
    this.rulesBase = [...this.rules];
    return this;
  }
  createNew(): Validator {
    return new Validator(this.errorMessage, [...this.rulesBase]);
  }

  validate(value: string): string[] {
    return this.rules
      .map((rule) => rule(value))
      .filter((error): error is string => error !== null);
  }
}
