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
        "Nasz zespół to czterech studentów informatyki, którzy połączyli swoje pasje i doświadczenie, by stworzyć aplikację, która zmienia sposób organizowania podróży grupowych. Zdecydowaliśmy się zaprojektować narzędzie, które pozwoli na łatwiejsze planowanie wyjazdów, dając użytkownikom pełną swobodę działania. W odróżnieniu od innych rozwiązań dostępnych na rynku, które często narzucają gotowe plany wyjazdów, nasza aplikacja umożliwia elastyczne dostosowanie podróży do indywidualnych potrzeb.",
    },
    {
      title: "Inspiracja do stworzenia aplikacji",
      paragraph:
        "Pomysł na naszą aplikację zrodził się z osobistych doświadczeń. Wiele razy, podczas planowania wspólnych wyjazdów z przyjaciółmi, napotykaliśmy na problemy związane z chaosem, brakiem komunikacji i trudnościami w podziale kosztów. Dotychczasowe aplikacje nie dawały nam wystarczającej kontroli nad procesem planowania – były sztywne, wymuszały określony sposób działania i nie pozwalały na dostosowanie planu do naszych potrzeb. Dlatego postanowiliśmy stworzyć narzędzie, które umożliwi użytkownikom pełną swobodę w planowaniu wyjazdów – od ustalania trasy, przez budżet, po organizowanie harmonogramu i listy uczestników.",
    },
    {
      title: "Nasze podejście do tworzenia aplikacji",
      paragraph:
        "Podzieliliśmy się zadaniami według naszych umiejętności: frontend, backend oraz dokumentacja. Dzięki takiemu podziałowi pracy udało nam się stworzyć aplikację, która nie tylko działa sprawnie, ale jest również przyjazna dla użytkownika i responsywna. Każdy z nas wniósł coś cennego do projektu, co pozwoliło stworzyć narzędzie, które jest proste w obsłudze, ale równocześnie potężne w zakresie funkcjonalności.",
    },
    {
      title: "Mobilność i wygoda użytkowania",
      paragraph:
        "Oprócz wersji na komputer, stworzyliśmy także aplikację mobilną. Dzięki niej użytkownicy mogą na bieżąco dodawać wydatki, podglądać zaplanowane podróże, a także wyświetlać bilety. Dla przewodników przygotowaliśmy możliwość zarządzania grupą, tworzenia kanału ogłoszeniowego oraz dzielenia się wydatkami z uczestnikami. Dzięki temu cała organizacja wyjazdu staje się prostsza, a komunikacja w grupie – bardziej efektywna.",
    },
    {
      title: "Nasza wizja",
      paragraph:
        "Naszym celem było stworzenie narzędzia, które daje użytkownikom pełną swobodę i kontrolę nad każdym etapem planowania wyjazdu. W odróżnieniu od innych aplikacji, które narzucają sztywne zasady, nasza aplikacja pozwala na dostosowanie wszystkiego do własnych potrzeb, co sprawia, że organizowanie podróży staje się przyjemnością. Dzięki temu możemy zaoferować coś, czego brakuje w konkurencyjnych rozwiązaniach – pełną elastyczność, która pozwala na swobodę działania.",
    },
  ],
  teamMembers: [
    {
      name: "Andrzej Ebertowski",
      role: "...",
      description: "...",
    },
    {
      name: "Kacper Pecka",
      role: "Frontend Developer",
      description: "...",
    },
    {
      name: "Jakub Pobłocki",
      role: "Backend Developer",
      description: "...",
    },
    {
      name: "Mateusz Wiśniewski",
      role: "...",
      description: "...",
    },
  ],
};