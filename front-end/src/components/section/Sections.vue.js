import Section from "@/components/Section.vue";
import FAQ from "@/components/section/FAQ/FAQ.vue";
import Advantage from "@/components/section/Advantage/Advantage.vue";
const faqList = [
    {
        question: "?",
        answer: "...",
    },
    {
        question: "?",
        answer: "...",
    },
    {
        question: "?",
        answer: "...",
    },
];
const subSections = [
    {
        title: "Jako Turysta",
        items: [
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
        ],
    },
    {
        title: "Jako Przewodnik",
        items: [
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
            {
                image: "@/assets/vue.svg",
                alt: "picture",
                caption: "Elastyczny planer podróży",
            },
        ],
    },
];
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    // @ts-ignore
    /** @type { [typeof Section, typeof Section, ] } */ ;
    // @ts-ignore
    const __VLS_0 = __VLS_asFunctionalComponent(Section, new Section({}));
    const __VLS_1 = __VLS_0({}, ...__VLS_functionalComponentArgsRest(__VLS_0));
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { title: __VLS_thisSlot } = __VLS_4.slots;
        __VLS_elementAsFunction(__VLS_intrinsicElements.h1, __VLS_intrinsicElements.h1)({
            ...{ class: ("gradient-text") },
        });
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { content: __VLS_thisSlot } = __VLS_4.slots;
        // @ts-ignore
        /** @type { [typeof Advantage, typeof Advantage, ] } */ ;
        // @ts-ignore
        const __VLS_5 = __VLS_asFunctionalComponent(Advantage, new Advantage({
            subSections: ((__VLS_ctx.subSections)),
        }));
        const __VLS_6 = __VLS_5({
            subSections: ((__VLS_ctx.subSections)),
        }, ...__VLS_functionalComponentArgsRest(__VLS_5));
        __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
        {
            const { 'main-title': __VLS_thisSlot } = __VLS_9.slots;
        }
        var __VLS_9;
    }
    var __VLS_4;
    // @ts-ignore
    /** @type { [typeof Section, typeof Section, ] } */ ;
    // @ts-ignore
    const __VLS_10 = __VLS_asFunctionalComponent(Section, new Section({}));
    const __VLS_11 = __VLS_10({}, ...__VLS_functionalComponentArgsRest(__VLS_10));
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { title: __VLS_thisSlot } = __VLS_14.slots;
        __VLS_elementAsFunction(__VLS_intrinsicElements.h2, __VLS_intrinsicElements.h2)({});
        __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({});
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { content: __VLS_thisSlot } = __VLS_14.slots;
        // @ts-ignore
        /** @type { [typeof FAQ, typeof FAQ, ] } */ ;
        // @ts-ignore
        const __VLS_15 = __VLS_asFunctionalComponent(FAQ, new FAQ({
            faqList: ((__VLS_ctx.faqList)),
        }));
        const __VLS_16 = __VLS_15({
            faqList: ((__VLS_ctx.faqList)),
        }, ...__VLS_functionalComponentArgsRest(__VLS_15));
        __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
        {
            const { question: __VLS_thisSlot } = __VLS_19.slots;
            const [{ question }] = __VLS_getSlotParams(__VLS_thisSlot);
            __VLS_elementAsFunction(__VLS_intrinsicElements.strong, __VLS_intrinsicElements.strong)({});
            (question);
        }
        __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
        {
            const { answer: __VLS_thisSlot } = __VLS_19.slots;
            const [{ answer }] = __VLS_getSlotParams(__VLS_thisSlot);
            __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
            (answer);
        }
        var __VLS_19;
    }
    var __VLS_14;
    ['gradient-text',];
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
            Section: Section,
            FAQ: FAQ,
            Advantage: Advantage,
            faqList: faqList,
            subSections: subSections,
        };
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
});
; /* PartiallyEnd: #4569/main.vue */
