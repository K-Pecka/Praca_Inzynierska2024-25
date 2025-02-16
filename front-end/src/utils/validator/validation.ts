import { ValidationRule, ValidationRules } from "./validationRules";
import { getDefaultMessages } from "./validationMessages";

export class Validator {
  private rules: { [key: string]: ValidationRule } = {};
  private errorMessage: ValidationRules = {};
  private rulesBase: { [key: string]: ValidationRule } = {};

  public constructor(
    errorMessage?: ValidationRules,
    rules?: { [key: string]: ValidationRule }
  ) {
    if (rules) {
      this.rules = { ...rules };
    }
    this.errorMessage = {
      ...getDefaultMessages,
      ...errorMessage,
    };
  }

  private formatMessage(template: string, ...args: any[]): string {
    return template.replace(/{(\d+)}/g, (_, index) => args[index] || "");
  }

  private addRule(key: string, rule: ValidationRule): this {
    this.rules[key] = rule;
    return this;
  }

  isEmpty(): this {
    return this.addRule("isEmpty", (value: string) => {
      return value.trim() === "" ? this.errorMessage.required : null;
    });
  }

  minLength(length: number): this {
    return this.addRule("minLength", (value: string) => {
      return value.length < length
        ? this.formatMessage(this.errorMessage.minLength, length)
        : null;
    });
  }

  maxLength(length: number): this {
    return this.addRule("maxLength", (value: string) => {
      return value.length > length
        ? this.formatMessage(this.errorMessage.maxLength, length)
        : null;
    });
  }
  minValue(minValue: number): this {
    return this.addRule("minValue", (value: string) => {
      return Number(value) <= Number(minValue)
        ? this.formatMessage(this.errorMessage.minValue, String(minValue))
        : null;
    });
  }
  equalLength(length: number): this {
    return this.addRule("equalLength", (value: string) => {
      return value.length !== length
        ? this.formatMessage(this.errorMessage.equalLength, length)
        : null;
    });
  }

  forbiddenChars(chars: string[]): this {
    return this.addRule("forbiddenChars", (value: string) => {
      const found = chars.find((char) => value.includes(char));
      return found
        ? this.formatMessage(this.errorMessage.forbiddenChars, found)
        : null;
    });
  }

  pattern(regex: RegExp): this {
    return this.addRule("pattern", (value: string) => {
      return !regex.test(value) ? this.errorMessage.pattern : null;
    });
  }

  email(): this {
    return this.addRule("email", (value: string) => {
      const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      return !emailRegex.test(value) ? this.errorMessage.email : null;
    });
  }

  number(): this {
    return this.addRule("number", (value: string) => {
      return isNaN(Number(value)) ? this.errorMessage.number : null;
    });
  }

  startsWith(prefix: string): this {
    return this.addRule("startsWith", (value: string) => {
      return !value.startsWith(prefix)
        ? this.formatMessage(this.errorMessage.startsWith, prefix)
        : null;
    });
  }

  endsWith(suffix: string): this {
    return this.addRule("endsWith", (value: string) => {
      return !value.endsWith(suffix)
        ? this.formatMessage(this.errorMessage.endsWith, suffix)
        : null;
    });
  }

  isEqual(compareValue: string): this {
    return this.addRule("isEqual", (value: string) => {
      return value !== compareValue ? this.errorMessage.isEqual : null;
    });
  }

  isInRange(min: number, max: number): this {
    return this.addRule("isInRange", (value: string) => {
      const numericValue = Number(value);
      return numericValue < min || numericValue > max
        ? this.formatMessage(this.errorMessage.isInRange, min, max)
        : null;
    });
  }
  doCheckbox(): this {
    return this.addRule("doCheckbox", (value: string) => {
      return !(value === "true" || value === "1" || value === "on")
        ? this.errorMessage.doCheckbox
        : null;
    });
  }
  addCustomRule(key: string, rule: ValidationRule, message: string): this {
    return this.addRule(key, (value: string) => {
      const error = rule(value);
      return error ? message : null;
    });
  }

  save(): Validator {
    this.rulesBase = { ...this.rules };
    return this;
  }

  createNew(): Validator {
    return new Validator(this.errorMessage, { ...this.rulesBase });
  }

  validate(value: string): string[] {
    return Object.values(this.rules)
      .map((rule) => rule(value))
      .filter((error): error is string => error !== null);
  }
}
