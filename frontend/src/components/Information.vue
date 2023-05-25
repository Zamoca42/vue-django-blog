<template>
  <v-container fluid style="width: 600px">
    <v-row class="mb-6" align="center" justify="center">
      <v-col cols="12" lg="10" align="center">
        <div class="mt-4">
          <p class="text-h3">Zamoca Space</p>
        </div>
      </v-col>
      <v-col cols="12" lg="10" align="left">
        <p class="mt-10 text-body-2 mb-1">Introduce</p>
        <p v-for="(intro, i) in intros" :key="i" :value="intro"
        class="text-body-2 font-weight-light mb-2">
          {{intro.text}}
        </p>
        <div>
          <a v-for="(item, i) in items" :key="i" :value="item" :href="item.href"
            class="text-body-2 text-decoration-none font-weight-light mr-2">
            {{ item.text }}
          </a>
        </div>
      </v-col>
      <v-col cols="12" lg="10" align="left">
        <p class="mt-2 text-body-2 mb-1">Blog Tech Stack</p>
        <p class="text-body-2 font-weight-light">Django 4.1, Vue 3, S3, EC2, RDS </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    items: [
      { text: "Resume", href: "https://zamoca.notion.site/CHU-YEON-KYU-cf8504c6c6c14f2481828d7177b85aa7" },
      { text: "GitHub", href: "https://github.com/zamoca42" },
      { text: "E-mail", href: "mailto:suntail93@naver.com" },
    ],
    intros: [
      { text: "안녕하세요, 저는 백엔드 개발자를 지향하는 추연규입니다." },
      { text: "효율성과 생산성에 대한 높은 가치를 인식하고 그러한 가치를 실현하기 위해 꾸준히 고민하고 배우며 성장해나가는 것을 추구합니다. 특히 업무 프로세스와 도구의 편의성을 개선하는 방식에 집중하면서, 그것이 얼마나 효율적인 업무 수행과 생산성 향상에 도움되는지 체감하고 있습니다." },
      { text: "이런 경험들을 바탕으로, 저는 개발 과정에서 배운 지식과 인사이트를 블로그로 공유하고자 합니다." },
    ]
  }),

};
</script>
