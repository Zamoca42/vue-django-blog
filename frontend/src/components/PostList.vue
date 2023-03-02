<template>
  <v-container style="width: 75%">
    <v-row class="mb-6" style="height: 200px" align="center" justify="center">
      <v-col cols="12" lg="12" align="center" class="mt-10 text-h3">
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
    <h5><div class="mb-2 text-subtitle-2">category or tag</div></h5>
    <v-row>
      <v-col
        v-for="post in posts"
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
          <v-img
            :src="post.image"
            class="rounded-xl"
            style="height: 150px"
            cover
          ></v-img>
          <v-card-text>
            <v-row>
              <v-col sm="10" cols="12" class="text-sm-left text-center">
                <p class="text-caption text-disabled">{{ post.modify_dt }}</p>
                <p class="text-body-1 mywrap" v-html="post.title"></p>
                <div class="mt-3 text-body-2 text-disabled mb-3 mywrap" v-html="post.description"></div>
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

export default {
  setup() {
    // return { user };
  },

  data: () => ({
    posts: [],
    cateList: [],
    tagname: "",
    page: 1,
  }),

  computed: {},

  created() {
    // console.log("created(PostList.vue)...", this.user);
    const params = new URL(location).searchParams;
    this.tagname = params.get("tagname");
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
      if (this.tagname) getUrl = `/api/post/list/?tagname=${this.tagname}`;
      else getUrl = "/api/post/list/";

      try {
        const res = await axios.get(getUrl);
        console.log("POST LIST GET RES", res);
        this.posts = res.data;
      } catch (err) {
        console.log("POST LIST GET ERR.RESPONSE", err);
        alert(err.response.status + " " + err.response.statusText);
      }

      console.log("async.2 in fetchPostList()...", this.user);
    },

    // fetchCateTagList() {
    //     console.log("fetchCateTagList()...");

    //     axios
    //       .get(`/api/catetag`)
    //       .then((res) => {
    //         console.log("FETCH CATE-TAG-LIST GET RES", res);
    //         this.cateList = res.data.cateList;
    //         // this.tagList = res.data.tagList;
    //       })
    //       .catch((err) => {
    //         console.log("FETCH CATE-TAG-LIST GET ERR.RESPONSE", err.response);
    //         alert(`${err.response.status} ${err.response.statusText}`);
    //       });
    //   },
    serverPage(item) {
      console.log("serverPage()...", item);
      location.href = `/blog/post_detail.html?id=${item}`;
    },
  },
};
</script>

<style scoped>
.mywrap {
  word-break:keep-all;
}
</style>
