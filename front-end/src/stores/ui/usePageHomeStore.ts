import { defineStore } from "pinia";
import { useAuthStore } from "../auth/useAuthStore";
import {computed, onMounted, ref, watch} from "vue";
import {
  defaultNavLinks,
  loggedInNavLinks,
  guestNavLinks,
  footerData,
  heroTextAnimation,
  faqList,
  advantagesBox,
  sectionTitles,
} from "@/data";
export const usePageHomeStore = defineStore("pagHome", () => {
  const { validToken } = useAuthStore();
  const navigationLinks = ref<Array<{ label: string; href: string | { name: string }; className?: string[]; active?: boolean }>>([]);
  onMounted(async () => {
      navigationLinks.value = [
        ...defaultNavLinks,
        ...(await validToken() ? loggedInNavLinks : guestNavLinks),
      ];
    });
  watch(validToken,async (value) => {

    navigationLinks.value = [
      ...defaultNavLinks,
      ...(await value ? loggedInNavLinks : guestNavLinks),
    ];
  });
  const getSiteName = () => import.meta.env.VITE_APP_SITE_NAME || "Plannder";
  const getFooterData = () => ({
    links: defaultNavLinks,
    ...footerData(),
  });
  const isLoggedIn = ref(false);

  onMounted(async () => {
    isLoggedIn.value = await validToken();
  });

  watch(validToken, async () => {
    isLoggedIn.value = await validToken();
  });

  const getHeroBannerText = () => heroTextAnimation;

  const getFAQData = (limit?: number) =>
    limit ? faqList.slice(0, limit) : faqList;

  const getAdvantagesData = (type?: string) => {
    if (type == undefined) return advantagesBox;
    return type == "tourist" ? [advantagesBox[0]] : [advantagesBox[1]];
  };

  const getSectionTitle = (pageType: string): string | undefined => {
    return sectionTitles[pageType] || "";
  };
  return {
    getSiteName,
    navigationLinks,
    isLoggedIn,
    getFooterData,
    getHeroBannerText,
    getFAQData,
    getAdvantagesData,
    getSectionTitle,
  };
});
