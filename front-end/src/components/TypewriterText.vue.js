import { ref, onMounted } from "vue";
import Typewriter from "typewriter-effect/dist/core";
const props = defineProps({
    phrases: {
        type: Array,
        required: true,
    }
});
const typewriterRef = ref(null);
const animateText = () => {
    const typewriter = new Typewriter(typewriterRef.value, {
        loop: true,
        delay: 75,
    });
    props.phrases.forEach((item) => {
        if (Array.isArray(item.word)) {
            item.word.forEach((word) => {
                typewriter.typeString(word).pauseFor(1000).deleteAll();
            });
        }
        else {
            typewriter
                .typeString(item.word)
                .pauseFor(1000)
                .deleteAll()
                .start();
        }
    });
    typewriter.start();
};
onMounted(() => {
    animateText();
});
; /* PartiallyEnd: #3632/scriptSetup.vue */
function __VLS_template() {
    const __VLS_ctx = {};
    let __VLS_components;
    let __VLS_directives;
    // CSS variable injection 
    // CSS variable injection end 
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({
        ref: ("typewriterRef"),
    });
    // @ts-ignore navigation for `const typewriterRef = ref()`
    /** @type { typeof __VLS_ctx.typewriterRef } */ ;
    __VLS_elementAsFunction(__VLS_intrinsicElements.div, __VLS_intrinsicElements.div)({});
    for (const [item, index] of __VLS_getVForSourceType((__VLS_ctx.phrases))) {
        __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            key: ((index)),
        });
        __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
            ...{ class: ("animated word") },
        });
        for (const [word, wordIndex] of __VLS_getVForSourceType((Array.isArray(item.word)
            ? item.word
            : [item.word]))) {
            __VLS_elementAsFunction(__VLS_intrinsicElements.span, __VLS_intrinsicElements.span)({
                key: ((wordIndex)),
            });
            (word);
        }
    }
    ['animated', 'word',];
    var __VLS_slots;
    var $slots;
    let __VLS_inheritedAttrs;
    var $attrs;
    const __VLS_refs = {
        'typewriterRef': __VLS_nativeElements['div'],
    };
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
            typewriterRef: typewriterRef,
        };
    },
    props: {
        phrases: {
            type: Array,
            required: true,
        }
    },
});
export default (await import('vue')).defineComponent({
    setup() {
        return {};
    },
    props: {
        phrases: {
            type: Array,
            required: true,
        }
    },
    __typeRefs: {},
    __typeEl: {},
});
; /* PartiallyEnd: #4569/main.vue */
