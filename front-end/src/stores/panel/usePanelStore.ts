import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";

export const usePanelStore = defineStore("panel", () => {
    const items = ref([
        { title: 'Ustawienia konta', to: "AccountSettings" },
        { title: 'Wybór roli', to: "home" },
    ]);

    let currentPage = shallowRef();

    const handleClick = async (navigate: any) => {
        try {
            await navigate();
        } catch (error) {
            console.error("Navigation failed", error);
        }
    };

    const loadPage = (page: any) => {
        currentPage.value = page;
    };

    return {
        items,
        currentPage,
        loadPage,
        handleClick,
    };
});
