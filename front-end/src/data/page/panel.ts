import { images } from "@/data";
import router from "@/router";

export const getTouristNav = () => [
  {
    title: 'Panel',
    page: {name: 'tripDashboard'},
    icon: 'mdi-home-outline'
  },
  {
    title: 'Plany',
    icon: 'mdi-note-text-outline',
    children: [
      {title: 'Utworzone', page: {name: 'tripPlans'}},
      {title: 'Dodaj', page: {name: 'createPlan'}, isOwner:true},
    ]
  },
  {
    title: 'Bilety',
    page: {name: 'yourTickets'},
    icon: 'mdi-ticket-confirmation-outline'
  },
  {
    title: 'Budżet',
    icon: 'mdi-currency-usd',
    page: {name: 'ExpenseTracker'},
  },
  {
    title: 'Uczestnicy',
    page: {name: 'tripParticipants'},
    icon: 'mdi-account-multiple-outline'
  },
  {
    title: 'Ustawienia',
    icon: 'mdi-cog-outline',
    isOwner:true,
    children: [
      {
        title: 'Edycja wycieczki',
        page: {name: 'editTrip'},
      }
    ]
  },
];
export const getGudieNav = () => [
  {
    title: 'Panel',
    page: {name: 'tripDashboard'},
    icon: 'mdi-home-outline'
  },
  {
    title: 'Plany',
    icon: 'mdi-note-text-outline',
    children: [
      {title: 'Utworzone', page: {name: 'tripPlans'}},
      {title: 'Dodaj', page: {name: 'createPlan'},isOwner:true},
    ]
  },
  {
    title: 'Bilety',
    page: {name: 'yourTickets'},
    icon: 'mdi-ticket-confirmation-outline'
  },
  {
    title: "Zaległości",
    name: "budget",
    icon: images.icon.menu.budget,
    children: [
      {
        title: "Pokaż",
        name: "debt",
        page: { name: "debt" },
      }
    ],
  },
  {
    title: "Uczestnicy",
    name: "participant",
    icon: images.icon.menu.participant,
    page: {name: 'tripParticipants'},
  },
  {
    title: "Ustawienia",
    name: "setting",
    icon: images.icon.menu.setting,
    isOwner:true,
    children: [
      {
        title: "Edycja wycieczki",
        name: "settingEdit",
        page: {name: 'editTrip'}
      },
    ],
  }
];
enum TypeOfButton{
    TRIP = 'trip',
}
const btnState = (option: Record<string,any>) => [
  {
    type: TypeOfButton.TRIP,
    title: "Zarządzaj wycieczką",
    class: ["primary"],
    onclick: (id: string) =>
      router.push({ name: option.btnPath, params: { tripId: id } })
  },
  {
    type: TypeOfButton.TRIP,
    title: "Usuń wycieczkę",
    class: ["accent"],
    onclick: (id: string) => option.handleDeleteTrip(id),
  }
];
export const getBtn = (option: Record<string,any>) =>
  btnState(option).filter(option.filter);
