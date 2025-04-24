import { POSITION } from "vue-toastification";

export const toastConfig = {
  position: POSITION.BOTTOM_RIGHT,
  timeout: 5048,
  closeOnClick: true,
  pauseOnFocusLoss: false,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 2,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button" as keyof HTMLElementTagNameMap,
  icon: true,
  rtl: false
};
