import { InputType } from "@/type/enum";
import { Validator } from "@/utils/validator/validation";


export const participantAddInputs = () => {
    const baseValidator = new Validator().isEmpty().save();
    return [
        {
            name: "participantName",
            label: "Imię i nazwisko",
            type: InputType.TEXT,
            placeholder: "np. Jan Kowalski",
            validation: baseValidator,
            error: [],
        },
        {
            name: "participantEmail",
            label: "Adres email",
            type: InputType.EMAIL,
            placeholder: "np. jan.kowalski@gmail.com",
            validation: new Validator().isEmpty().email().save(),
            error: [],
        },
    ];
};
