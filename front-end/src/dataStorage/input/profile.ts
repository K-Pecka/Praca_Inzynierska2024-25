import { InputType } from '@/type/enum';
import { Validator } from '@/utils/validator/validation';

const base = (err: Record<string,string>) => new Validator(err).isEmpty().save();

export const profileInput = (err: Record<string,string>) => [
    {
        name : 'first_name',
        label: 'Imię',
        type : InputType.TEXT,
        placeholder: 'Jan',
        validation : base(err).minLength(3),
        error: [],
    },
    {
        name : 'last_name',
        label: 'Nazwisko',
        type : InputType.TEXT,
        placeholder: 'Kowalski',
        validation : base(err).minLength(3),
        error: [],
    },
    {
        name : 'current_password',
        label: 'Aktualne hasło',
        type : InputType.PASSWORD,
        placeholder: '*****',
        validation : base(err).minLength(6),
        error: [],
    },
    {
        name : 'new_password',
        related: ['pass_2'],
        label: 'Nowe hasło',
        type : InputType.PASSWORD,
        placeholder: '*****',
        validation : base(err).minLength(6),
        error: [],
    },
    {
        name : 'pass_2',
        related: ['new_password'],
        label: 'Powtórz nowe hasło',
        type : InputType.PASSWORD,
        placeholder: '*****',
        validation : base(err).isEmpty(),
        error: [],
    },
];
