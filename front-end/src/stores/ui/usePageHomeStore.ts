import { defineStore } from "pinia";
import { useAuthStore } from "../auth/useAuthStore";
import { onMounted, ref, watchEffect } from "vue";
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
  const auth = useAuthStore();

  type NavLink = {
    label: string;
    href: string | { name: string };
    className?: string[];
    active?: boolean;
  };

  const navigationLinks = ref<NavLink[]>([]);
  const isLoggedIn = ref(false);

  const updateNavigation = async () => {
    if (!auth.token) {
      isLoggedIn.value = false;
      navigationLinks.value = [...defaultNavLinks, ...guestNavLinks];
      return;
    }

    isLoggedIn.value = await auth.validToken();
    navigationLinks.value = [
      ...defaultNavLinks,
      ...(isLoggedIn.value ? loggedInNavLinks : guestNavLinks),
    ];
  };

  onMounted(updateNavigation);

  watchEffect(updateNavigation);

  const getSiteName = () => import.meta.env.VITE_APP_SITE_NAME || "Plannder";

  const getFooterData = () => ({
    links: defaultNavLinks,
    ...footerData(),
  });

  const getHeroBannerText = () => heroTextAnimation;

  const getFAQData = (limit?: number) =>
      limit ? faqList.slice(0, limit) : faqList;

  const getAdvantagesData = (type?: string) => {
    if (!type) return advantagesBox;
    return type === "tourist" ? [advantagesBox[0]] : [advantagesBox[1]];
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
