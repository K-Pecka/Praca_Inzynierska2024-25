<script lang="ts" setup>
import { FooterData} from "@/types/interface";
import lastModified from "@/assets/last-modified.txt?raw";
import { useUtilStore } from "@/stores";
 defineProps({
  footerData: {
    type: Object as () => FooterData,
    required: true,
  },
});
const {formatDate} = useUtilStore();
const lastModifiedDate = formatDate(new Date(lastModified));
</script>

<template>
  <footer class="footer-bg">
    <v-container class="footer">
      <v-row>
        <v-col class="footer__top" cols="12" sm="12" md="10" offset-sm="0" offset-md="1">
          <div class="footer__top__logo">
            <slot name="logo"> </slot>
          </div>

          <div
            class="footer__top__links "
            v-if="footerData.links && footerData.links.length > 0"
          >
            <ul>
              <li v-for="(link, index) in footerData.links" :key="index">
                <router-link :to="link.href">{{ link.label }}</router-link>
              </li>
            </ul>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col
          class="footer__bottom"
          cols="12"
          md="10"
          offset-md="1"
          v-if="footerData.footerText"
        >
          <hr />
          <p v-if="footerData.footerText">{{ footerData.footerText }}</p>
          <p v-if="lastModifiedDate">{{ `${footerData.lastUpdated} ${lastModifiedDate}` }}</p>
        </v-col>
      </v-row>
    </v-container>
  </footer>
</template>

<style scoped lang="scss">
@use "@/assets/style.scss" as *;
.footer-bg{
  background-color: rgb(var(--v-theme-secondary));
}
.v-row + .v-row {
  margin-top: 0.25rem;
}
* {
  color: rgb(var(--v-theme-text));
  font-family: var(--v-fontFamily);
}

.footer {
  @include section-width;
  padding: 3rem 1rem 1rem 1rem;
  background-color: rgb(var(--v-theme-secondary));
  font-family: var(--v-fontFamily);

  &__top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    &__logo {
      @include font-large;
      @include gradient-text;
      font-size: 2rem;
      display: flex;
      align-items: center;
      @media (max-width: 600px) {
        font-size: 1rem;
      }
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
      @media (max-width: 600px) {
        ul {
          flex-direction: column;
          gap: 0.5rem;
          padding: 0;
          margin: 0;
        }
      }
      li {
        margin: 5px 0;
        @include font-regular;
        @media (max-width: 600px) {
        font-size: 0.75rem;
      }
      }

      a {
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
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
    border-top: 1px solid #0000001c;
    @media (max-width: 600px) {
      font-size: 0.75rem;
    }
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

</style>
