import PaymentLayout from "@/layouts/PaymentLayout.vue";
import Payment from "@/views/home/children/Payment.vue"
const paymentRoutes = {
  path: "/payment",
  name: "payment",
  component: PaymentLayout,
  meta: { title: "Home" },
  children: [
      {
        path: "success",
        name: "paymentSuccess",
        component: Payment
      }
  ],
};

export default paymentRoutes;
