<template>
  <v-container fluid style="width: 1200px">
    <v-row class="mb-6" style="height: 200px" align="center" justify="center">
      <v-col cols="12" lg="10" align="center" class="mt-10">
        <a class="text-h3 text-high-emphasis text-decoration-none" href="/">Post</a>
      </v-col>
      <!-- category -->
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
    <!-- category or tag -->
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
    <!-- PostList -->
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
                <p class="text-caption text-disabled">{{ post.modify_dt }}</p>
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
        <!-- Pagination -->
        <template v-if="pageCnt === 1">
        </template>
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
// import axios from "axios";
// import { user } from "./globals.js";
import axios from "./index.js";

export default {
  setup() {
    // return { user };
  },

  data: () => ({
    postList: [],
    cateList: [
      { text: "Log" },
      { text: "Project" },
      { text: "Review" },
    ],
    tagname: "",
    category: "",
    page: 1,
    pageCnt: 1,
    curPage: 1,
    defaultImageUrl: "https://picsum.photos/id/366/400/200",
  }),

  computed: {},

  created() {
    // console.log("created(PostList.vue)...", this.user);
    const params = new URL(location).searchParams;
    this.tagname = params.get("tagname");
    this.category = params.get("category");
    this.fetchPostList();
    // console.log("async.1 in created()...");
  },

  mounted() {
    // console.log("mounted(PostList.vue)...", this.user);
    // this.fetchCateList();
  },

  methods: {
    async fetchPostList(page = 1) {
      // console.log("fetchPostList()...", page, this.tagname, this.category);

      let getUrl = "";
      if (this.tagname) getUrl = `/api2/post/?page=${page}&tagname=${this.tagname}`;
      else if (this.category) getUrl = `/api2/post/?page=${page}&category=${this.category}`;
      else getUrl = `/api2/post/?page=${page}`;

      axios
        .get(getUrl)
        .then((res) => {
          // console.log("FETCH POSTLIST GET RES", res);
          this.postList = res.data.postList;
          this.pageCnt = res.data.pageCnt;
          this.curPage = res.data.curPage;
        })
        .catch((err) => {
          console.log("POST LIST GET ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
        });
      // console.log("async.2 in fetchPostList()...", this.user);
    },

    serverPage(item) {
      // console.log("serverPage()...", item);
      location.href = `/blog/post_detail.html?id=${item}`;
    },

    // async fetchCateList() {
    //   console.log("fetchCateList()...");
    //   axios
    //     .get("/api2/category/")
    //     .then((res) => {
    //       console.log("CATEGORY GET RES", res);
    //       this.cateList = res.data.cateList;
    //     })
    //     .catch((err) => {
    //       console.log("CATEGORY GET ERR.RESPONSE", err.response);
    //       alert(err.response.status + " " + err.response.statusText);
    //     });
    // },

    categoryPage(category) {
      // console.log("serverPage()...", category);
      location.href = `/blog/post_list.html?category=${category}`;
    },

    pageChange(page) {
      // console.log("pageChanged()...", page);
      if (this.curPage === page) return
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
