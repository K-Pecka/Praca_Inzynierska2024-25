import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";

export const usePanelStore = defineStore("panel", () => {
    const items = ref([
        { title: 'Ustawienia konta', to: "AccountSettings" },
        { title: 'Wybór roli', to: "home" },
    ]);

    const handleClick = async (navigate: any) => {
        try {
            await navigate();
        } catch (error) {
            //console.error("Navigation failed", error);
        }
    };

    return {
        items,
        handleClick,
    };
});
