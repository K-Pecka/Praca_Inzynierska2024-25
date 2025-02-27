<script lang="ts" setup>
import { FooterData} from "@/type/interface";
import { onMounted, ref } from "vue";

const lastModified = ref<string>(new Date().toLocaleDateString());
onMounted(async () => {
  try {
    const response = await fetch('/last-modified.txt');
    lastModified.value = await response.text();
  } catch (error) {
    lastModified.value = 'Brak danych';
  }
});
const props = defineProps({
  footerData: {
    type: Object as () => FooterData,
    required: true,
  },
});
</script>

<template>
  <footer>
    <v-container fluid class="footer full-width-container">
      <v-row>
        <v-col class="footer__top" cols="12" md="10" offset-md="1">
          <div class="footer__top__logo">
            <slot name="logo"> </slot>
          </div>

          <div
            class="footer__top__links"
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
          <p v-if="footerData.lastUpdated">{{ lastModified }}</p>
        </v-col>
      </v-row>
    </v-container>
  </footer>
</template>

<style scoped lang="scss">
@use "@/assets/style.scss" as *;

.v-row + .v-row {
  margin-top: 0.25rem;
}
* {
  color: rgb(var(--v-theme-text));
  font-family: var(--v-fontFamily);
}

.footer {
  @include section-width;
  padding: 3rem 0 1rem 0;
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
  }
  &__bottom {
    line-height: 3rem;
    display: flex;
    justify-content: center;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: center;
    border-top: 1px solid #0000001c;
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
