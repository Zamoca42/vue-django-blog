<template>
  <v-container fluid style="width: 1200px">
    <v-row class="mb-6" style="height: 200px" align="center" justify="center">
      <v-col cols="12" lg="10" align="center" class="mt-10 text-h3">
        <span>Post</span>
      </v-col>
      <!-- category -->
      <v-col cols="12" lg="12" align="center">
        <v-btn variant="text">new</v-btn>
        <v-btn variant="text">Review</v-btn>
        <v-btn variant="text">log</v-btn>
        <v-btn variant="text">project</v-btn>
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
    <!-- <template v-if="category">
      <p class="mb-2 text-subtitle-2">
        <span>Category: </span>
        <span>
          Category
        </span>
      </p>
    </template> -->
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
        <v-pagination
          v-model="page"
          :length="4"
          rounded="circle"
        ></v-pagination>
      </div>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
// import { user } from "./globals.js";
// import image from 'https://picsum.photos/900/300?grayscale'

export default {
  setup() {
    // return { user };
  },

  data: () => ({
    postList: [],
    cateList: [],
    tagname: "",
    category: "",
    pageCnt: 1,
    curPage: 1,
    // image: "",
    defaultImageUrl: "https://picsum.photos/500/150?grayscale",
  }),

  computed: {
    // imageSrc() {
    //   return this.image || this.defaultImageUrl;
  },

  created() {
    // console.log("created(PostList.vue)...", this.user);
    const params = new URL(location).searchParams;
    this.tagname = params.get("tagname");
    this.category = params.get("category");
    this.fetchPostList();
    console.log("async.1 in created()...");
  },

  mounted() {
    // console.log("mounted(PostList.vue)...", this.user);
  },

  methods: {
    async fetchPostList() {
      console.log("fetchPostList()...", this.tagname);

      let getUrl = "";
      if (this.tagname) getUrl = `/api2/post/?tagname=${this.tagname}`;
      else if (this.category) getUrl = `/api2/post/?category=${this.category}`;
      else getUrl = `/api2/post/`;

      axios
        .get(getUrl)
        .then((res) => {
          console.log("FETCH POSTLIST GET RES", res);
          this.postList = res.data.postList;
          this.pageCnt = res.data.pageCnt;
          this.curPage = res.data.curPage;
        })
        .catch((err) => {
          console.log("POST LIST GET ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
        });
      // try {
      //   const res = await axios.get(getUrl);
      //   console.log("POST LIST GET RES", res);
      //   this.posts = res.data.postList;
      //   this.pageCnt = res.data.pageCnt;
      //   this.curPage = res.data.curPage;
      // } catch (err) {
      //   console.log("POST LIST GET ERR.RESPONSE", err);
      //   alert(err.response.status + " " + err.response.statusText);
      // }
      console.log("async.2 in fetchPostList()...", this.user);
    },

    serverPage(item) {
      console.log("serverPage()...", item);
      location.href = `/blog/post_detail.html?id=${item}`;
    },
  },
};
</script>

<style scoped>
.mywrap {
  word-break: keep-all;
}
</style>
