import { ref } from "vue";
import InputWithLabel from "@/components/InputWithLabel.vue";
import Section from "@/components/Section.vue";
import Btn from "@/components/Btn.vue";
const inputStyle = {
    color: "var(--primary-color)",
    fontSize: "2rem",
};
const moreOption = [
    { icon: "@/assets/vue.svg", text: "Zaloguj się za pomocą Google" },
];
const inputs = ref([
    {
        name: "email",
        label: "Podaj Email:",
        type: "email",
        placeholder: "Wprowadź email",
    },
    {
        name: "password",
        label: "Podaj Hasło:",
        type: "password",
        placeholder: "Wprowadź hasło",
    },
]);
const extraOption = [
    { label: "Zapomniałeś hasła?", href: "/" },
    { label: "Nie masz konta? Zarejestruj się.", href: "/" },
];
const formValues = ref(Object.fromEntries(inputs.value.map((input) => [input.name, ""])));
const handleSubmit = () => {
    console.log("Wartości formularza:", formValues.value);
};
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    ['extraOption',];
    // CSS variable injection 
    // CSS variable injection end 
    // @ts-ignore
    /** @type { [typeof Section, typeof Section, ] } */ ;
    // @ts-ignore
    const __VLS_0 = __VLS_asFunctionalComponent(Section, new Section({
        ...{ class: ("logIn") },
    }));
    const __VLS_1 = __VLS_0({
        ...{ class: ("logIn") },
    }, ...__VLS_functionalComponentArgsRest(__VLS_0));
    var __VLS_5 = {};
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { title: __VLS_thisSlot } = __VLS_4.slots;
        __VLS_elementAsFunction(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({
            ...{ style: ((__VLS_ctx.inputStyle)) },
        });
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { content: __VLS_thisSlot } = __VLS_4.slots;
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("container") },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("form-container") },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("wrapper") },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.form, __VLS_intrinsicElements.form)({
            ...{ onSubmit: (__VLS_ctx.handleSubmit) },
        });
        for (const [inputsData, index] of __VLS_getVForSourceType((__VLS_ctx.inputs))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
                key: ((index)),
            });
            // @ts-ignore
            /** @type { [typeof InputWithLabel, ] } */ ;
            // @ts-ignore
            const __VLS_6 = __VLS_asFunctionalComponent(InputWithLabel, new InputWithLabel({
                inputData: ((inputsData)),
                modelValue: ((__VLS_ctx.formValues[inputsData.name])),
            }));
            const __VLS_7 = __VLS_6({
                inputData: ((inputsData)),
                modelValue: ((__VLS_ctx.formValues[inputsData.name])),
            }, ...__VLS_functionalComponentArgsRest(__VLS_6));
        }
        __VLS_elementAsFunction(__VLS_intrinsicElements.button, __VLS_intrinsicElements.button)({
            type: ("submit"),
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("extraOption") },
        });
        for (const [option, index] of __VLS_getVForSourceType((__VLS_ctx.extraOption))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
                key: ((index)),
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.a, __VLS_intrinsicElements.a)({
                href: ((option.href)),
            });
            (option.label);
        }
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("more-action") },
        });
        for (const [option, index] of __VLS_getVForSourceType((__VLS_ctx.moreOption))) {
            // @ts-ignore
            /** @type { [typeof Btn, typeof Btn, ] } */ ;
            // @ts-ignore
            const __VLS_11 = __VLS_asFunctionalComponent(Btn, new Btn({
                key: ((index)),
            }));
            const __VLS_12 = __VLS_11({
                key: ((index)),
            }, ...__VLS_functionalComponentArgsRest(__VLS_11));
            __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
            {
                const { icon: __VLS_thisSlot } = __VLS_15.slots;
                __VLS_elementAsFunction(__VLS_intrinsicElements.img)({
                    src: ("@/assets/vue.svg"),
                });
            }
            __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
            {
                const { text: __VLS_thisSlot } = __VLS_15.slots;
                (option.text);
            }
            var __VLS_15;
        }
    }
    var __VLS_4;
    ['logIn', 'container', 'form-container', 'wrapper', 'extraOption', 'more-action',];
    var __VLS_slots;
    var $slots;
    let __VLS_inheritedAttrs;
    var $attrs;
    const __VLS_refs = {};
    var $refs;
    var $el;
    return {
        attrs: {},
        slots: __VLS_slots,
        refs: $refs,
        rootEl: $el,
    };
}
;
const __VLS_self = (await import('vue')).defineComponent({
    setup() {
        return {
            InputWithLabel: InputWithLabel,
            Section: Section,
            Btn: Btn,
            inputStyle: inputStyle,
            moreOption: moreOption,
            inputs: inputs,
            extraOption: extraOption,
            formValues: formValues,
            handleSubmit: handleSubmit,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    __typeEl: {},
});
; /* PartiallyEnd: #4569/main.vue */
