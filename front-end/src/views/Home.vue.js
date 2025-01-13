import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
const navLinksBase = [
    { label: "Oferta", href: "/" },
    { label: "Kontakt", href: "/" },
];
const user = false;
const navLinks = [
    ...navLinksBase,
    ...(user
        ? [{ label: "Panel", href: "/", active: true }]
        : [
            { label: "Zaloguj się", href: "/logIn" },
            { label: "Zarejestruj się", href: "/", active: true },
        ]),
];
const footerData = {
    links: [
        { label: "Oferta", href: "/" },
        { label: "Kontakt", href: "/" },
        { label: "Panel", href: "/" },
    ],
    footerText: "© 2024 Plannder Wszystkie prawa zastrzeżone",
};
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ...{ class: ("app") },
    });
    // @ts-ignore
    /** @type { [typeof Navbar, typeof Navbar, ] } */ ;
    // @ts-ignore
    const __VLS_0 = __VLS_asFunctionalComponent(Navbar, new Navbar({
        links: ((__VLS_ctx.navLinks)),
    }));
    const __VLS_1 = __VLS_0({
        links: ((__VLS_ctx.navLinks)),
    }, ...__VLS_functionalComponentArgsRest(__VLS_0));
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { logo: __VLS_thisSlot } = __VLS_4.slots;
        __VLS_elementAsFunction(__VLS_intrinsicElements.img)({
            src: ("@/assets/vue.svg"),
            alt: ("App Logo"),
        });
    }
    var __VLS_4;
    __VLS_elementAsFunction(__VLS_intrinsicElements.main, __VLS_intrinsicElements.main)({});
    const __VLS_5 = {}.RouterView;
    /** @type { [typeof __VLS_components.RouterView, typeof __VLS_components.routerView, ] } */ ;
    // @ts-ignore
    const __VLS_6 = __VLS_asFunctionalComponent(__VLS_5, new __VLS_5({}));
    const __VLS_7 = __VLS_6({}, ...__VLS_functionalComponentArgsRest(__VLS_6));
    // @ts-ignore
    /** @type { [typeof Footer, typeof Footer, ] } */ ;
    // @ts-ignore
    const __VLS_11 = __VLS_asFunctionalComponent(Footer, new Footer({
        footerData: ((__VLS_ctx.footerData)),
    }));
    const __VLS_12 = __VLS_11({
        footerData: ((__VLS_ctx.footerData)),
    }, ...__VLS_functionalComponentArgsRest(__VLS_11));
    __VLS_elementAsFunction(__VLS_intrinsicElements.template, __VLS_intrinsicElements.template)({});
    {
        const { logo: __VLS_thisSlot } = __VLS_15.slots;
    }
    var __VLS_15;
    ['app',];
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
            Navbar: Navbar,
            Footer: Footer,
            navLinks: navLinks,
            footerData: footerData,
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
