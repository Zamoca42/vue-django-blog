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
    <v-row>
      <v-col cols="12" class="text-subtitle-2">
        <span>category or tag</span>
      </v-col>
      <v-col v-for="post in posts" :key="post.id" sm="6" lg="3">
        <v-card
          elevation="0"
          @click="serverPage(post.id)"
          :ripple="false"
          class="rounded-xl"
        >
          <v-img
            :src="post.image"
            class="rounded-xl"
            style="height: 150px"
            cover
          ></v-img>
            <v-card-subtitle class="mt-2 text-caption text-disabled"> {{ post.modify_dt }} </v-card-subtitle>
            <v-card-title class="text-h6"> {{ post.title }} </v-card-title>
            <v-card-text class="text-body-2 text-disabled mb-6">{{ post.description }} </v-card-text>
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
  </v-container>
</template>

<script>
import axios from "axios";
import { user } from "./globals.js";

export default {
  setup() {
    return { user };
  },

  data: () => ({
    dialog: false,
    headers: [
      {
        title: "ID",
        align: "start",
        sortable: false,
        key: "id",
      },
      { title: "제 목", key: "title" },
      { title: "요 약", key: "description" },
      { title: "수정일", key: "modify_dt" },
      { title: "작성자", key: "owner" },
      { title: "Actions", key: "actions", sortable: false },
    ],
    posts: [],
    cateList: [],
    tagname: "",
    editedIndex: -1,
    editedItem: {},
    actionKind: "",

    dialogDelete: false,
  }),

  computed: {
    formTitle() {
      if (this.actionKind === "create") return "Create post";
      else return "Update post";
    },
  },

  created() {
    console.log("created(PostList.vue)...", this.user);
    const params = new URL(location).searchParams;
    this.tagname = params.get("tagname");
    this.fetchPostList();
    console.log("async.1 in created()...");
  },

  mounted() {
    console.log("mounted(PostList.vue)...", this.user);
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

    dialogOpen(actionKind, item) {
      console.log("dialogOpen()...", actionKind, item);
      if (this.user.username === "Anonymous") {
        alert("Please login first !");
        return;
      }

      this.actionKind = actionKind;
      if (actionKind === "create") {
        this.editedIndex = -1;
        this.editedItem = {};
      } else {
        this.editedIndex = this.posts.indexOf(item);
        this.editedItem = item;
      }
      this.dialog = true;
    },

    cancel() {
      console.log("cancel()...");
      this.dialog = false;
    },

    save() {
      console.log("save()...");
      if (this.actionKind === "create") this.createPost();
      else this.updatePost();
      this.dialog = false;
    },

    reset() {
      console.log("reset()...");
      document.getElementById("post-form").reset();
    },

    serverPage(item) {
      console.log("serverPage()...", item);
      location.href = `/blog/post_detail.html?id=${item}`;
    },
  },
};
</script>

<style scoped>
.v-data-table :deep(tr.v-data-table__tr) :hover {
  cursor: pointer;
  background-color: #eee;
}
</style>
