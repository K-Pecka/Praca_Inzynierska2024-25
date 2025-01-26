<template>
  <footer>
    <v-container fluid class="footer full-width-container">
      <v-row>
        <v-col class="footer__top"  cols="12" md="10" offset-md="1">
          <div class="footer__logo">
            <slot name="logo"> </slot>
          </div>

          <div
            class="footer__links"
            v-if="footerData.links && footerData.links.length > 0"
          >
            <ul>
              <li v-for="(link, index) in footerData.links" :key="index">
                <a :href="link.href">{{ link.label }}</a>
              </li>
            </ul>
          </div>
        </v-col>
      </v-row>
     
      <v-row>
        <v-col class="footer__bottom"  cols="12" md="10" offset-md="1" v-if="footerData.footerText">
          <hr>
          <p v-if="footerData.footerText">{{ footerData.footerText }}</p>
          <p v-if="footerData.subSection">{{ footerData.subSection }}</p>
        </v-col>
      </v-row>
    </v-container>
  </footer>
</template>

<script lang="ts" setup>
import { PropType } from "vue";

interface Link {
  href: string;
  label: string;
}

interface FooterData {
  links: Link[];
  footerText?: string;
  subSection?: string;
}

const props = defineProps({
  footerData: {
    type: Object as PropType<FooterData>,
    required: true,
  },
});
</script>

<style scoped lang="scss">
@use "@/assets/style.scss" as *;

.v-row + .v-row {
    margin-top: 0.25rem;
}
* {
  color: var(--text-color);
  font-family: var(--font-family);
}

.footer {
  @include section-width;
  padding: 3rem 0 1rem 0;
  background-color: var(--secondary-color);
  font-family: var(--font-family);
  &__top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  &__logo {
    @include font-large;
    @include gradient-text;
    font-size: 2rem;
    display: flex;
    align-items: center;

    img {
      width: 50px;
      height: 50px;
      margin-right: 10px;
    }
  }

  &__name {
    font-size: 1.5rem;
    font-weight: bold;
  }

  &__links {
    ul {
      display: flex;
      list-style: none;
      gap: 2rem;
      padding: 0.5rem;
      margin: 0;
    }

    li {
      margin: 5px 0;
      @include font-regular;
    }

    a {
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }

  &__bottom {
    line-height: 3rem;
    display: flex;
    justify-content: center;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: center;
    @media screen and (min-width: 768px) {
      flex-direction: column;
      &::after {
        content: "";
        margin: 0.5rem 0;
      }
      display: flex;
      justify-content: center;
      flex-direction: row;
      p {
        &:not(:last-child)::after {
          content: " | ";
          margin: 0 0.5rem;
        }
        margin: 0;
        font-size: 1rem;
      }
    }
  }
}

hr {
  color: #0000001c;
  width: 100%;
  margin-bottom: 0.2rem;
}
</style>
