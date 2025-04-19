export const defaultNavLinks = [
    { label: "Oferta", href: "pricing-section", className: ["navbar__link--base"] },
    { label: "O nas", href: {name: "aboutUs"}, className: ["navbar__link--base"] },
    { label: "Kontakt", href: "contact-us", className: ["navbar__link--base"] },
  ];
  
  export const loggedInNavLinks = [
    { label: "Wyloguj się", href: { name: "logOut" } },
    { label: "Panel", href: { name: "roleSelection" }, active: true },
  ];
  
  export const guestNavLinks = [
    { label: "Zaloguj się", href: { name: "logIn" } },
    { label: "Zarejestruj się", href: { name: "register" }, active: true },
  ];
  export const heroTextAnimation =[
    { word: "Zaplanuj" },
    { word: ["przygodę", "podróż"], animation: true },
    { word: "która zapadnie" },
    { word: "w pamięć na" },
    { word: "zawsze" },
  ];
  export const faqList =[
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
  export const advantagesBox=[
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
          caption: "Precyzyjna kontrola wydatków",
        },
        {
          image: "picture/p3.svg",
          alt: "picture",
          caption: "Wygodny schowek na bilety",
        }
      ],
    },
    {
      title: "Jako Przewodnik",
      items: [
        {
          image: "picture/p1.svg",
          alt: "picture",
          caption: "Proste planowanie i udostępnianie",
        },
        {
          image: "picture/p4.svg",
          alt: "picture",
          caption: "Skuteczna forma komunikacji",
        },
        {
          image: "picture/p5.svg",
          alt: "picture",
          caption: "Praktyczny kanał ogłoszeniowy",
        }
      ],
    },
  ];
  export const sectionTitles:Record<string,string> = {
    login: "Zaloguj się",
    register: "Zarejestruj się",
  };
  export const footerData = () => ({
    footerText: `© 2025 Plannder Wszystkie prawa zastrzeżone`,
    lastUpdated: `Ostatnia modyfikacja:`,
  });

export const pricingPlans = [
  {
    name: "Podstawowy",
    price: "Darmowy",
    features: ["Tekst", "Tekst", "Tekst"],
    buttonVariant: "secondary" as "secondary",
  },
  {
    name: "Turysta",
    price: "15.0 zł / miesiąc",
    features: ["Tekst", "Tekst", "Tekst"],
    buttonVariant: "primary" as "primary",
  },
  {
    name: "Podróżnik",
    price: "40.0 zł / miesiąc",
    features: ["Tekst", "Tekst", "Tekst"],
    buttonVariant: "secondary" as "secondary",
  },
];
