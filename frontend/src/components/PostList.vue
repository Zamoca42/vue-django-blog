<template>
  <v-container fluid style="width: 1200px">
    <v-row class="mb-6" style="height: 200px" align="center" justify="center">
      <v-col cols="12" lg="10" align="center">
        <a class="text-h3 text-high-emphasis text-decoration-none" href="/"
          >Post</a
        >
      </v-col>
      <v-col cols="12" lg="12" align="center">
        <v-btn
          variant="text"
          v-for="(cate, index) in cateList"
          :key="index"
          @click="categoryPage(cate.text)"
        >
          {{ cate.text }}
        </v-btn>
      </v-col>
    </v-row>
    <template v-if="tagname">
      <p class="mb-2 text-subtitle-2">
        <span>Tag: </span>
        <span>
          {{ tagname }}
        </span>
      </p>
    </template>
    <template v-if="category">
      <p class="mb-2 text-subtitle-2">
        <span>Category: </span>
        <span>
          {{ category }}
        </span>
      </p>
    </template>
    <template v-else>
      <div class="mb-2"></div>
    </template>
    <v-row cols="12" lg="10">
      <v-col
        v-for="post in postList"
        :key="post.id"
        lg="3"
        md="4"
        sm="6"
        cols="12"
      >
        <v-card
          elevation="0"
          @click="serverPage(post.id)"
          :ripple="false"
          class="rounded-xl fill-height"
        >
          <template v-if="post.image === null">
            <v-img
              :src="defaultImageUrl"
              class="rounded-xl"
              style="height: 150px"
              cover
            ></v-img>
          </template>
          <template v-else>
            <v-img
              :src="post.image"
              class="rounded-xl"
              style="height: 150px"
              cover
            ></v-img>
          </template>
          <v-card-text>
            <v-row>
              <v-col sm="10" cols="12" class="text-sm-left text-center">
                <p class="text-caption text-disabled">{{ post.create_dt }}</p>
                <p class="text-body-1 mywrap" v-html="post.title"></p>
                <div
                  class="mt-3 text-body-2 text-disabled mb-3 mywrap"
                  v-html="post.description"
                ></div>
              </v-col>
            </v-row>
          </v-card-text>
          <v-chip
            v-for="(tag, index) in post.tags"
            :key="index"
            class="ml-2 mb-3 text-disabled"
            size="x-small"
          >
            {{ tag }}
          </v-chip>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <div class="text-center">
        <template v-if="pageCnt === 1"> </template>
        <template v-else>
          <v-pagination
            v-model="page"
            :length="pageCnt"
            :total-visible="4"
            rounded="circle"
            @click.stop="pageChange(page)"
          >
          </v-pagination>
        </template>
      </div>
    </v-row>
  </v-container>
</template>

<script>
import axios from "../plugins/axios-serverURL.js";
import _ from 'lodash';

export default {
  setup() {},

  data: () => ({
    postList: [],
    cateList: [{ text: "Log" }, { text: "Project" }, { text: "Review" }],
    tagname: "",
    category: "",
    page: 1,
    pageCnt: 1,
    curPage: 1,
    defaultImageUrl: "https://picsum.photos/id/366/400/200",
  }),

  computed: {},

  created() {
    this.tagname = this.$route.query.tagname;
    this.category = this.$route.query.category;
    this.fetchPostList();
  },

  beforeRouteUpdate(to, from, next) {
    this.tagname = to.query.tagname;
    this.category = to.query.category;
    this.fetchPostList();
    next();
  },

  methods: {
    fetchPostList(page = 1) {
      let getUrl = `/api2/post/?page=${page}`;
      if (this.tagname) getUrl += `&tagname=${this.tagname}`;
      if (this.category) getUrl += `&category=${this.category}`;

      axios
        .get(getUrl)
        .then((res) => {
          this.postList = res.data.postList;
          this.pageCnt = res.data.pageCnt;
          this.curPage = res.data.curPage;
        })
        .catch((err) => {
          this.$router.push({ name: "NotFound" });
        });
    },

    serverPage(item) {
      this.$router.push({ name: "Detail", params: { id: item } });
    },

    categoryPage: _.debounce(function (category) {
      this.$router.push({ name: "Blog", query: { category } });
    }, 300),

    pageChange(page) {
      if (this.curPage === page) return;
      else {
        this.curPage = page;
        this.fetchPostList(page);
      }
    },
  },
};
</script>

<style scoped>
.mywrap {
  word-break: keep-all;
}
</style>
