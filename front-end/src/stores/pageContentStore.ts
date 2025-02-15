import { defineStore } from "pinia";

export const usePageStore = defineStore("page", () => {
  const baseList = [
    { label: "Oferta", href: "/", className: ["navbar__link--base"] },
    { label: "O nas", href: "/", className: ["navbar__link--base"] },
    { label: "Kontakt", href: "/", className: ["navbar__link--base"] },
  ];

  const SiteName = () => import.meta.env.VITE_APP_SITE_NAME || "Plannder";
  const isLogin = () => !!localStorage.getItem("jwt") || false;

  const navLinks = () => {
    let baseList = [
      { label: "Oferta", href: "/", className: ["navbar__link--base"] },
      { label: "O nas", href: "/", className: ["navbar__link--base"] },
      { label: "Kontakt", href: "/", className: ["navbar__link--base"] },
    ];
    return [
      ...baseList,
      ...(isLogin()
        ? [{ label: "wyloguj się", href: "/logOut" },{label: "Panel", href: "/panel", active: true }]
        : [
            { label: "Zaloguj się", href: "/logIn" },
            { label: "Zarejestruj się", href: "/register", active: true },
          ]),
    ];
  };

  const footerData = () => {
    return {
      links: [...baseList, { label: "Panel", href: "/" }],
      footerText: `© 2025 Plannder Wszystkie prawa zastrzeżone `,
      subSection: `ostatnia modyfikacja: ${new Date().toLocaleDateString()}`,
    };
  };

  const heroTestData = () => [
    { word: "Zaplanuj" },
    { word: ["przygodę", "podróż"], animation: true },
    { word: "która" },
    { word: "zapadnie" },
    { word: "w pamięć" },
    { word: "na zawsze" },
  ];
  const FQAData = (limit?: number) => {
    let fqa = [
      {
        question: "Czy mogę zaplanować podróż grupową?",
        answer:
          "Tak! Aplikacja umożliwia planowanie podróży grupowych. Możesz zaprosić inne osoby, aby razem edytować plan, głosować nad miejscami do odwiedzenia lub śledzić wspólne wydatki.",
      },
      {
        question: "Czy aplikacja jest płatna?",
        answer:
          "Aplikacja oferuje darmowy plan z podstawowymi funkcjami. Możesz także wykupić subskrypcję premium, która odblokowuje dodatkowe opcje, takie jak zaawansowane mapy, wskazówki offline i personalizowane rekomendacje.",
      },
      {
        question: "Czy aplikacja śledzi mój budżet podróży?",
        answer:
          "Tak, w aplikacji znajduje się funkcja budżetowania, która pozwala dodawać wydatki i monitorować koszty w czasie rzeczywistym. Możesz także ustawić limit budżetu na całą podróż.",
      },
    ];
    return limit && limit < fqa.length ? fqa.slice(0, limit) : fqa;
  };
  const advantagesData = (type?: string) => {
    let data = [
      {
        title: "Jako Turysta",
        items: [
          {
            image: "picture/p1.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
          {
            image: "picture/p2.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
          {
            image: "picture/p3.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
          {
            image: "picture/p4.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
        ],
      },
      {
        title: "Jako Przewodnik",
        items: [
          {
            image: "picture/p1.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
          {
            image: "picture/p2.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
          {
            image: "picture/p3.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
          {
            image: "picture/p4.svg",
            alt: "picture",
            caption: "Elastyczny planer podróży",
          },
        ],
      },
    ];
    return type == undefined ? data : type == "tourist" ? [data[0]] : [data[1]];
  };
  const getSectionTitle = (type: string): string | undefined => {
    const pageTitles: Record<string, string> = {
      login: "Zaloguj się",
      register: "Zarejestruj się",
    };

    return pageTitles[type] || "";
  };
  const errorMessage = () => {
    return {
      unknow: "Nieznany błąd",
      required: "Pole nie może być puste",
      minLength: "Minimalna wymagana długość to {0} znaków",
      maxLength: "Pole nie może być dłuższe niż {0} znaków",
      forbiddenChars: "Pole zawiera niedozwolony znak: {0}",
      equalLength: "Pole musi mieć dokładnie {0} znaków",
      pattern: "Pole nie pasuje do wymaganego wzorca",
      email: "Nieprawidłowy format emaila",
      number: "Pole musi być liczbą",
      startsWith: "Pole musi zaczynać się od {0}",
      endsWith: "Pole musi kończyć się na {0}",
      isEqual: "Pola muszą być równe",
      isInRange: "Pole musi mieścić się w zakresie od {0} do {1}",
      minValue: "Wartość musi być większa niż {0}"
    };
  };
  return {
    SiteName,
    navLinks,
    footerData,
    heroTestData,
    FQAData,
    advantagesData,
    getSectionTitle,
    errorMessage
  };
});
