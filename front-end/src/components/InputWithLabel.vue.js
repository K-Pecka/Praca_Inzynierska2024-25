const __VLS_props = defineProps({
    inputData: {
        type: Object,
        required: true,
    },
    modelValue: {
        type: String,
        required: true,
    },
});
const emit = defineEmits(['update:modelValue']);
const updateValue = (event) => {
    emit('update:modelValue', event.target.value);
};
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    // CSS variable injection 
    // CSS variable injection end 
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("input-wrapper") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.label, __VLS_intrinsicElements.label)({
        for: ((__VLS_ctx.inputData.name)),
        ...{ class: ("input-label") },
    });
    (__VLS_ctx.inputData.label);
    __VLS_elementAsFunction(__VLS_intrinsicElements.input)({
        ...{ onInput: (__VLS_ctx.updateValue) },
        id: ((__VLS_ctx.inputData.name)),
        type: ((__VLS_ctx.inputData.type)),
        placeholder: ((__VLS_ctx.inputData.placeholder)),
        value: ((__VLS_ctx.modelValue)),
        ...{ class: ("input") },
    });
    ['input-wrapper', 'input-label', 'input',];
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
            updateValue: updateValue,
        };
    },
    emits: {},
    props: {
        inputData: {
            type: Object,
            required: true,
        },
        modelValue: {
            type: String,
            required: true,
        },
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    emits: {},
    props: {
        inputData: {
            type: Object,
            required: true,
        },
        modelValue: {
            type: String,
            required: true,
        },
    },
    __typeEl: {},
});
; /* PartiallyEnd: #4569/main.vue */
