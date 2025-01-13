import Hero from "@/components/Hero.vue";
const heroPhrases = [
    { word: "Zaplanuj" },
    { word: ["przygodę", "podróż"], animation: true },
    { word: "która" },
    { word: "zapadnie" },
    { word: "w pamięć" },
    { word: "na zawsze" },
];
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    // @ts-ignore
    /** @type { [typeof Hero, typeof Hero, ] } */ ;
    // @ts-ignore
    const __VLS_0 = __VLS_asFunctionalComponent(Hero, new Hero({
        phrases: ((__VLS_ctx.heroPhrases)),
    }));
    const __VLS_1 = __VLS_0({
        phrases: ((__VLS_ctx.heroPhrases)),
    }, ...__VLS_functionalComponentArgsRest(__VLS_0));
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { hero: __VLS_thisSlot } = __VLS_4.slots;
        __VLS_elementAsFunction(__VLS_intrinsicElements.img)({
            src: ("@/assets/vue.svg"),
            alt: ("Hero image"),
        });
    }
    var __VLS_4;
    const __VLS_5 = {}.Sections;
    /** @type { [typeof __VLS_components.Sections, ] } */ ;
    // @ts-ignore
    const __VLS_6 = __VLS_asFunctionalComponent(__VLS_5, new __VLS_5({}));
    const __VLS_7 = __VLS_6({}, ...__VLS_functionalComponentArgsRest(__VLS_6));
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
            Hero: Hero,
            heroPhrases: heroPhrases,
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
