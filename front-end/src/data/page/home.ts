import { images } from "../ui/image";

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
          image: images.benefits.tourist.flexiblePlanner,
          caption: "Elastyczny planer podróży",
        },
        {
          image: images.benefits.tourist.expenseControl,
          caption: "Precyzyjna kontrola wydatków",
        },
        {
          image: images.benefits.tourist.ticketStorage,
          caption: "Wygodny schowek na bilety",
        }
      ],
    },
    {
      title: "Jako Przewodnik",
      items: [
        {
          image: images.benefits.guide.flexiblePlanner,
          caption: "Proste planowanie i udostępnianie",
        },
        {
          image:  images.benefits.guide.communication,
          caption: "Skuteczna forma komunikacji",
        },
        {
          image:  images.benefits.guide.communicationChannel,
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
    contentVariant: "secondary" as "secondary",
    buttonVariant: "primary" as "primary",
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
    contentVariant: "secondary" as "secondary",
    buttonVariant: "primary" as "primary",
  },
];
export const aboutTeam ={
  mainTitle: "Dowiedź się więcej o nas",
  subTitle: "Nasz zespół",
  paragraphs: [
    {
      title: "Nasz zespół",
      paragraph:
        "Jesteśmy grupą studentów, których połączyła pasja do podróży i chęć ułatwienia życia sobie i innym. Z własnego doświadczenia wiemy, jak trudno czasem zorganizować wspólny wyjazd — dlatego stworzyliśmy aplikację, która to upraszcza. Nie chcemy nikomu nic narzucać – dajemy jedynie narzędzia, które pozwalą zaplanować podróż dokładnie tak, jak chcecie. Prosto, wygodnie i po swojemu."
    },
    {
      title: "Mobilność i wygoda użytkowania",
      paragraph:
        "Poza wersją na komputer przygotowaliśmy też aplikację mobilną. Dzięki niej możesz szybko dodać nowy wydatek, sprawdzić plan podróży czy podejrzeć bilety – wszystko pod ręką. Jeśli jesteś przewodnikiem, masz też dostęp do funkcji zarządzania grupą, ogłoszeń i wspólnego budżetu. Organizacja wyjazdu staje się dzięki temu o wiele łatwiejsza, a kontakt z uczestnikami – prostszy i wygodniejszy."
    },
  ],
  teamMembers: [
    {
      name: "Andrzej Ebertowski",
      role: "Specjalista ds. Dokumentacji",
      description: "Tworzenie dokumentacji, testowanie funkcjonalności, wspieranie frontendu.",
      photo:"/src/assets/images/avatar/AE_avatar.jpg"
    },
    {
      name: "Kacper Pecka",
      role: "Główny Frontend Developer",
      description: "Projektowanie interfejsu, wdrażanie responsywności, integracja frontendu z API.",
      photo:"/src/assets/images/avatar/AE_avatar.jpg"
    },
    {
      name: "Jakub Pobłocki",
      role: "Główny Backend Developer",
      description: "Budowanie API, dostosowywanie logiki serwera do potrzeb aplikacji.",
      photo:"/src/assets/images/avatar/JP_avatar.png"
    },
    {
      name: "Mateusz Wiśniewski",
      role: "Project Manager",
      description: "Koordynowanie zespołu, zarządzanie sprintami, kontrolowanie realizacji zadań.",
      photo:"/src/assets/images/avatar/MW_avatar.png"
    },
  ],
};