import { InputType } from "@/types/enum";
import { Validator } from "@/utils/validator/validation";

const getValidator = (errorMessage: Record<string, string>): Validator => {
    return new Validator(errorMessage).save();
};

export const profilePersonalInput = (errorMessage: Record<string, string>) => [
    {
        name: "first_name",
        label: "Imię:",
        type: InputType.TEXT,
        placeholder: "Wprowadź imię",
        validation: getValidator(errorMessage).minLength(1),
        config: { required: true },
        error: [],
    },
    {
        name: "last_name",
        label: "Nazwisko:",
        type: InputType.TEXT,
        placeholder: "Wprowadź nazwisko",
        validation: getValidator(errorMessage).minLength(1),
        config: { required: true },
        error: [],
    },
];

export const profilePasswordInput = (errorMessage: Record<string, string>) => [
    {
        name: "new_pass",
        related: ["repeat_pass"],
        label: "Nowe hasło:",
        type: InputType.PASSWORD,
        placeholder: "Wprowadź nowe hasło",
        validation: getValidator(errorMessage).minLength(6),
        config: { required: true },
        error: [],
    },
    {
        name: "repeat_pass",
        related: ["new_pass"],
        label: "Powtórz nowe hasło:",
        type: InputType.PASSWORD,
        placeholder: "Wprowadź ponownie hasło",
        validation: getValidator(errorMessage).minLength(6),
        config: { required: true },
        error: [],
    },
];