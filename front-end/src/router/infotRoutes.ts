import InfoLayout from "@/layouts/InfoLayout.vue";
import Payment from "@/views/home/Payment.vue"
import Info from "@/views/home/Info.vue"
const paymentRoutes = {
  path: "/",
  name: "info",
  component: InfoLayout,
  meta: { title: "Informacje" },
  children: [
      {
       path: "/payment/:status",
      name: "paymentResult",
      component: Payment,
      props: true
      },
      {
       path: ":type",
      name: "/paymentResult",
      component: Info,
      props: true
      },
  ],
};

export default paymentRoutes;
