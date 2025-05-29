import {images} from "../ui/image";

export const defaultNavLinks = [
    {label: "Oferta", href: "pricing-section", className: ["navbar__link--base"]},
    {label: "O nas", href: {name: "aboutUs"}, className: ["navbar__link--base"]},
    {label: "Kontakt", href: "contact-us", className: ["navbar__link--base"]},
];

export const loggedInNavLinks = [
    {label: "Wyloguj się", href: {name: "logOut"}},
    {label: "Panel", href: {name: "roleSelection"}, active: true},
];

export const guestNavLinks = [
    {label: "Zaloguj się", href: {name: "logIn"}},
    {label: "Zarejestruj się", href: {name: "register"}, active: true},
];
export const heroTextAnimation = [
    {word: "Zaplanuj"},
    {word: ["przygodę", "podróż"], animation: true},
    {word: "która zapadnie"},
    {word: "w pamięć na"},
    {word: "zawsze"},
];
export const faqList = [
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
export const advantagesBox = [
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
                image: images.benefits.guide.communication,
                caption: "Skuteczna forma komunikacji",
            },
            {
                image: images.benefits.guide.communicationChannel,
                caption: "Praktyczny kanał ogłoszeniowy",
            }
        ],
    },
];
export const sectionTitles: Record<string, string> = {
    login: "Zaloguj się",
    register: "Zarejestruj się",
};
export const footerData = () => ({
    footerText: `© 2025 Plannder Wszystkie prawa zastrzeżone`,
    lastUpdated: `Ostatnia modyfikacja:`,
});

export const pricingPlans = [
    {
        type: "tourist",
        name: "Podstawowy",
        price: "Darmowy",
        features: ["3 wycieczki w skali roku", "1 plan na wycieczkę", "brak możliwości zapraszania uczestników"],
        contentVariant: "secondary" as "secondary",
        buttonVariant: "primary" as "primary",
    },
    {
        type: "premium",
        name: "Turysta",
        price: "15.0 zł / miesiąc",
        features: ["Nielimitowane wycieczki", "Nielimitowane plany", "do 5 uczestników"],
        buttonVariant: "primary" as "primary",
    },
    {
        type: "guide",
        name: "Podróżnik",
        price: "45.0 zł / miesiąc",
        features: ["Tekst", "Tekst", "Tekst"],
        contentVariant: "secondary" as "secondary",
        buttonVariant: "primary" as "primary",
    },
];
export const aboutTeam = {
    mainTitle: "Nasz Zespół",
    paragraphs: [
        {
            paragraph:
                "Jesteśmy grupą studentów, których połączyła pasja do podróży i chęć ułatwienia życia sobie i innym. Z własnego doświadczenia wiemy, jak trudno czasem zorganizować wspólny wyjazd — dlatego stworzyliśmy aplikację, która to upraszcza. Nie chcemy nikomu nic narzucać – dajemy jedynie narzędzia, które pozwalą zaplanować podróż dokładnie tak, jak chcecie. Prosto, wygodnie i po swojemu."
        },
    ],
    teamMembers: [
        {
            name: "Mateusz Wiśniewski",
            role: "Team Leader",
            description: "Koordynowanie zespołu, zarządzanie sprintami, kontrolowanie realizacji zadań, tworzenie dokumentacji, projektowanie interfejsu, regularne testowanie aplikacji webowej,  programista aplikacji mobilnej i backendu.",
            photo: images.teamMembers.MateuszWisniewski,
            github: "https://github.com/s24893-pj"
        },
        {
            name: "Jakub Pobłocki",
            role: "Główny Backend Developer",
            description: "Główny programista backendu, zarządzenie strukturą bazy danych, dokumentacja API, wspieranie frontendu",
            photo: images.teamMembers.JakubPoblocki,
            github: "https://github.com/s25770-pj"
        },
        {
            name: "Andrzej Ebertowski",
            role: "Specjalista ds. Dokumentacji",
            description: "Tworzenie dokumentacji, testowanie funkcjonalności, wspieranie frontendu.",
            photo: images.teamMembers.AndrzejEbertowski,
            github: "https://github.com/AndrzejjE"
        },
        {
            name: "Kacper Pecka",
            role: "Główny Frontend Developer",
            description: "Główny programista frontendu, wdrażanie responsywności, integracja z API.",
            photo: images.teamMembers.KacperPecka,
            github: "https://github.com/K-Pecka"
        },
    ],
};
export const contacts = [
  {
    icon: 'mdi-email-outline',
    bgClass: 'contact-accent-bg',
    title: 'Wyślij nam maila',
    content: 'Odpowiemy w ciągu 24 godzin',
    footer: 'kontakt@plannder.com',
  },
  {
    icon: 'mdi-phone-outline',
    bgClass: 'contact-orange-bg',
    title: 'Zadzwoń do nas',
    content: 'Pon-Pt od 9:00 do 18:00',
    footer: '+48 000 000 000',
  },
  {
    icon: 'mdi-map-marker-outline',
    bgClass: 'contact-cyan-bg',
    title: 'Odwiedź nas',
    content: 'Przywitaj się z nami osobiście w naszym biurze',
    footer: 'Targ drzewny 14, Gdańsk, PL',
  },
]