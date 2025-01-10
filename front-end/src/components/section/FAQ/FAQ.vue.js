import { ref } from "vue";
const props = defineProps({
    faqList: {
        type: Array,
        required: true,
    },
});
const openIndex = ref(null);
const toggle = (index) => {
    openIndex.value = openIndex.value === index ? null : index;
};
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    ['faq-item', 'faq-question',];
    // CSS variable injection 
    // CSS variable injection end 
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("faq") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("faq-items") },
    });
    for (const [item, index] of __VLS_getVForSourceType((__VLS_ctx.faqList))) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            key: ((index)),
            ...{ class: ("faq-item") },
            ...{ class: (({ open: __VLS_ctx.openIndex === index })) },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ onClick: (...[$event]) => {
                    __VLS_ctx.toggle(index);
                } },
            ...{ class: ("faq-question") },
        });
        var __VLS_0 = {
            question: ((item.question)),
        };
        (item.question);
        __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            ...{ class: ("toggle-icon") },
        });
        (__VLS_ctx.openIndex === index ? "-" : "+");
        if (__VLS_ctx.openIndex === index) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
                ...{ class: ("faq-answer") },
            });
            var __VLS_1 = {
                answer: ((item.answer)),
            };
            (item.answer);
        }
    }
    ['faq', 'faq-items', 'faq-item', 'open', 'faq-question', 'toggle-icon', 'faq-answer',];
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
            openIndex: openIndex,
            toggle: toggle,
        };
    },
    props: {
        faqList: {
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
        faqList: {
            type: Array,
            required: true,
        },
    },
    __typeEl: {},
});
export default {};
; /* PartiallyEnd: #4569/main.vue */
