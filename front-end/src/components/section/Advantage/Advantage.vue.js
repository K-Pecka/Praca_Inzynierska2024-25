import SubSection from '@/components/section/Advantage/SubSection.vue';
const __VLS_props = defineProps({
    subSections: {
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
    __VLS_elementAsFunction(__VLS_intrinsicElements.section, __VLS_intrinsicElements.section)({
        ...{ class: ("section-with-subsections") },
    });
    for (const [subSection, index] of __VLS_getVForSourceType((__VLS_ctx.subSections))) {
        // @ts-ignore
        /** @type { [typeof SubSection, typeof SubSection, ] } */ ;
        // @ts-ignore
        const __VLS_0 = __VLS_asFunctionalComponent(SubSection, new SubSection({
            key: ((index)),
            items: ((subSection.items)),
        }));
        const __VLS_1 = __VLS_0({
            key: ((index)),
            items: ((subSection.items)),
        }, ...__VLS_functionalComponentArgsRest(__VLS_0));
        __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
        {
            const { title: __VLS_thisSlot } = __VLS_4.slots;
            (subSection.title);
        }
        var __VLS_4;
    }
    ['section-with-subsections',];
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
            SubSection: SubSection,
        };
    },
    props: {
        subSections: {
            type: Array,
            required: true,
        },
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    props: {
        subSections: {
            type: Array,
            required: true,
        },
    },
    __typeEl: {},
});
; /* PartiallyEnd: #4569/main.vue */
