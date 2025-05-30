import heroImg from '@/assets/images/hero/hero-section.svg';
import logoImg from '@/assets/images/logo/page.svg';

import touristRoleImg from '@/assets/images/roles/tourist.svg';
import guideRoleImg from '@/assets/images/roles/guide.svg';

import tripBackgroundImg from '@/assets/images/backgrounds/trip-background.svg';

import touristExpenseControlImg from '@/assets/images/benefits/tourist/expense-control.svg';
import touristFlexiblePlannerImg from '@/assets/images/benefits/tourist/flexible-planner.svg';
import touristTicketStorageImg from '@/assets/images/benefits/tourist/ticket-storage.svg';

import guideCommunicationImg from '@/assets/images/benefits/guide/communication.svg';
import guideCommunicationChannelImg from '@/assets/images/benefits/guide/communication-channel.svg';
import guideFlexiblePlannerImg from '@/assets/images/benefits/guide/flexible-planner.svg';

import emptyTripImg from '@/assets/images/emptyState/empty-state-trip.svg';
import emptyPlanImg from '@/assets/images/emptyState/empty-state-plan.svg';
import emptyTicketImg from '@/assets/images/emptyState/empty-state-ticket.svg';

import myAccountImg from '@/assets/images/icons/my-account.svg';

import MW_avatar from '@/assets/images/avatar/MW_avatar.png';
import JP_avatar from '@/assets/images/avatar/JP_avatar.png';
import AE_avatar from '@/assets/images/avatar/AE_avatar.png';
import KP_avatar from '@/assets/images/avatar/KP_avatar.png';
export const images = {
  hero: {
    img: heroImg,
    alt: 'hero banner',
  },
  logo: {
    img: logoImg,
    alt: 'logo',
  },
  role: {
    tourist: {
      img: touristRoleImg,
      alt: 'tourist',
    },
    guide: {
      img: guideRoleImg,
      alt: 'guide',
    },
  },
  backgrounds: {
    trip: {
      img: tripBackgroundImg,
      alt: 'trip background',
    },
  },
  benefits: {
    tourist: {
      expenseControl: {
        img: touristExpenseControlImg,
        alt: 'expense control',
      },
      flexiblePlanner: {
        img: touristFlexiblePlannerImg,
        alt: 'flexible planner',
      },
      ticketStorage: {
        img: touristTicketStorageImg,
        alt: 'ticket storage',
      },
    },
    guide: {
      communication: {
        img: guideCommunicationImg,
        alt: 'communication',
      },
      communicationChannel: {
        img: guideCommunicationChannelImg,
        alt: 'communication channel',
      },
      flexiblePlanner: {
        img: guideFlexiblePlannerImg,
        alt: 'flexible planner',
      },
    },
  },
  emptyState: {
    trip: {
      img: emptyTripImg,
      alt: 'empty trip',
    },
    plan: {
      img: emptyPlanImg,
      alt: 'empty plan',
    },
    ticket: {
      img: emptyTicketImg,
      alt: 'empty ticket',
    },
  },
  icon: {
    menu: {
      back: 'mdi-arrow-left',
      dashboard: 'mdi-home-outline',
      plan: 'mdi-note-text-outline',
      ticket: 'mdi-ticket-confirmation-outline',
      budget: 'mdi-currency-usd',
      participant: 'mdi-account-multiple-outline',
      setting: 'mdi-cog-outline',
      myAccount: 'mdi-account-circle-outline',
    },
    myAccount: {
      img: myAccountImg,
      alt: 'my account',
    },
  },
  teamMembers:{
    MateuszWisniewski:{
      src: MW_avatar,
      alt: 'Mateusz Wiśniewski',
    },
    JakubPoblocki:{
      src: JP_avatar,
      alt: 'Jakub Pobłocki',
    },
    AndrzejEbertowski:{
      src: AE_avatar,
      alt: 'Andrzej Ebertowski',
    },
    KacperPecka:{
      src: KP_avatar,
      alt: 'Kacper Pecka',
    },
  }
};
