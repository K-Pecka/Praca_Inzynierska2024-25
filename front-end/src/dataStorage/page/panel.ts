import { image } from "@/lib";
import router from "@/router";
import { Btn } from "@/type";
import { Role } from "@/type/enum";
export const getTouristNav = (tripId: string) => [
  {
    label: "Powrót",
    icon: image.icon.menu.back,
    name: "goBack",
    route: { name: "yourTrip" },
  },
  {
    label: "Panel",
    icon: image.icon.menu.dashboard,
    name: "panel",
    route: { name: "tripDashboard", params: { tripId: tripId } },
  },
  {
    label: "Plany",
    name: "plan",
    icon: image.icon.menu.plan,
    children: [
      {
        label: "Utworzone",
        name: "yourPlan",
        route: { name: "yourPlan", params: { tripId: tripId } },
      },
      {
        label: "Dodaj",
        name: "PlanForm",
        route: { name: "PlanForm", params: { tripId: tripId } },
      },
    ],
  },
  {
    label: "Bilety",
    name: "ticket",
    icon: image.icon.menu.ticket,
    route: { name: "TicketsView", params: { tripId: tripId } },
  },
  {
    label: "Budżet",
    name: "budget",
    icon: image.icon.menu.budget,
    children: [
      {
        label: "Pokaż",
        name: "budgetShow",
        route: { name: "ExpenseTracker", params: { tripId: tripId } },
      },
      {
        label: "Zmień budżet",
        name: "budgetChange",
        route: { name: "budget", params: { tripId: tripId } },
      },
    ],
  },
  {
    label: "Uczestnicy",
    name: "participant",
    icon: image.icon.menu.participant,
    route: { name: "ParticipantsView", params: { tripId: tripId } },
  },
  {
    label: "Ustawienia",
    name: "setting",
    icon: image.icon.menu.setting,
    children: [
      {
        label: "Edycja wycieczki",
        name: "settingEdit",
        route: { name: "TripEdit", params: { tripId: tripId } },
      },
    ],
  },
];
export const getGudieNav = (tripId: string) => [
  {
    label: "Panel",
    icon: image.icon.menu.dashboard,
    name: "panel",
    route: { name: "tripDashboard", params: { tripId: tripId } },
  },
  {
    label: "Plany",
    name: "plan",
    icon: image.icon.menu.plan,
    children: [
      {
        label: "Utworzone",
        name: "yourPlan",
        route: { name: "yourPlan", params: { tripId: tripId } },
      },
      {
        label: "Dodaj",
        name: "PlanForm",
        route: { name: "PlanForm", params: { tripId: tripId } },
      },
    ],
  },
  {
    label: "Bilety",
    name: "ticket",
    icon: image.icon.menu.ticket,
    route: { name: "TicketsView", params: { tripId: tripId } },
  },
  {
    label: "Zaległości",
    name: "budget",
    icon: image.icon.menu.budget,
    children: [
      {
        label: "Pokaż",
        name: "budgetShow",
        route: { name: "ExpenseTracker", params: { tripId: tripId } },
      },
      {
        label: "Zmień budżet",
        name: "budgetChange",
        route: { name: "budget", params: { tripId: tripId } },
      },
    ],
  },
  {
    label: "Uczestnicy",
    name: "participant",
    icon: image.icon.menu.participant,
    route: { name: "ParticipantsView", params: { tripId: tripId } },
  },
  {
    label: "Ustawienia",
    name: "setting",
    icon: image.icon.menu.setting,
    children: [
      {
        label: "Edycja wycieczki",
        name: "settingEdit",
        route: { name: "TripEdit", params: { tripId: tripId } },
      },
    ],
  },
  {
    label: "Powrót",
    icon: image.icon.menu.back,
    name: "goBack",
    route: { name: "yourTripGuide" },
  },
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
