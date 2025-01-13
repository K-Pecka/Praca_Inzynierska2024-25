import TypewriterText from "./TypewriterText.vue";
const imageSrc = "@/assets/your-image.jpg";
const props = defineProps({
    phrases: {
        type: Array,
        required: true,
    },
});
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    // CSS variable injection 
    // CSS variable injection end 
    __VLS_elementAsFunction(__VLS_intrinsicElements.header, __VLS_intrinsicElements.header)({
        ...{ class: ("hero") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("hero__text") },
    });
    for (const [item, index] of __VLS_getVForSourceType((__VLS_ctx.phrases))) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            key: ((index)),
            ...{ class: ("phrase") },
        });
        if (item.animation) {
            // @ts-ignore
            /** @type { [typeof TypewriterText, ] } */ ;
            // @ts-ignore
            const __VLS_0 = __VLS_asFunctionalComponent(TypewriterText, new TypewriterText({
                phrases: (([item])),
                ...{ class: ("word") },
                ...{ style: ((item.styles)) },
            }));
            const __VLS_1 = __VLS_0({
                phrases: (([item])),
                ...{ class: ("word") },
                ...{ style: ((item.styles)) },
            }, ...__VLS_functionalComponentArgsRest(__VLS_0));
        }
        else {
            __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
            (item.word);
        }
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("hero__image") },
    });
    var __VLS_5 = {};
    __VLS_elementAsFunction(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({});
    ['hero', 'hero__text', 'phrase', 'word', 'hero__image',];
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
            TypewriterText: TypewriterText,
        };
    },
    props: {
        phrases: {
            type: Array,
            required: true,
        },
    },
});
const __VLS_component = (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    props: {
        phrases: {
            type: Array,
            required: true,
        },
    },
    __typeEl: {},
});
export default {};
; /* PartiallyEnd: #4569/main.vue */
