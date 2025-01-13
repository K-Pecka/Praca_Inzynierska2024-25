import { defineProps } from "vue";
const props = defineProps({
    footerData: {
        type: Object,
        required: true,
    },
});
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    ['footer__logo', 'footer__links', 'footer__links', 'footer__links', 'footer__bottom',];
    // CSS variable injection 
    // CSS variable injection end 
    __VLS_elementAsFunction(__VLS_intrinsicElements.footer, __VLS_intrinsicElements.footer)({});
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("footer") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("footer__top") },
    });
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("footer__logo") },
    });
    var __VLS_0 = {};
    if (__VLS_ctx.footerData.links && __VLS_ctx.footerData.links.length > 0) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("footer__links") },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.ul, __VLS_intrinsicElements.ul)({});
        for (const [link, index] of __VLS_getVForSourceType((__VLS_ctx.footerData.links))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.li, __VLS_intrinsicElements.li)({
                key: ((index)),
            });
            __VLS_elementAsFunction(__VLS_intrinsicElements.a, __VLS_intrinsicElements.a)({
                href: ((link.href)),
            });
            (link.label);
        }
    }
    __VLS_elementAsFunction(__VLS_intrinsicElements.hr)({});
    if (__VLS_ctx.footerData.footerText) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
            ...{ class: ("footer__bottom") },
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.p, __VLS_intrinsicElements.p)({});
        (__VLS_ctx.footerData.footerText);
    }
    ['footer', 'footer__top', 'footer__logo', 'footer__links', 'footer__bottom',];
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
        return {};
    },
    props: {
        footerData: {
            type: Object,
            required: true,
        },
    },
});
const __VLS_component = (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    props: {
        footerData: {
            type: Object,
            required: true,
        },
    },
    __typeEl: {},
});
export default {};
; /* PartiallyEnd: #4569/main.vue */
