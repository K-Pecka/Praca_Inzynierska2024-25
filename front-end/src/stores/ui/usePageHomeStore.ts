import { defineStore } from "pinia";
import { useAuthStore } from "../auth/useAuthStore";
import { computed, onMounted, ref } from "vue";
import {
  defaultNavLinks,
  loggedInNavLinks,
  guestNavLinks,
  footerData,
  heroTextAnimation,
  faqList,
  advantagesBox,
  sectionTitles,
} from "@/dataStorage";
export const usePageHomeStore = defineStore("pagHome", () => {
  const { validToken } = useAuthStore();
  const isUserLoggedIn = ref(false);

  const checkUserAuthentication = async () => {
    isUserLoggedIn.value = await validToken();
  };

  onMounted(async () => {
    await checkUserAuthentication();
  });

  const getSiteName = () => import.meta.env.VITE_APP_SITE_NAME || "Plannder";

  const navigationLinks = computed(() => {
    return [
      ...defaultNavLinks,
      ...(isUserLoggedIn.value ? loggedInNavLinks : guestNavLinks),
    ];
  });

  const getFooterData = () => ({
    links: navigationLinks.value,
    ...footerData(),
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
    getFooterData,
    getHeroBannerText,
    getFAQData,
    getAdvantagesData,
    getSectionTitle,
  };
});
