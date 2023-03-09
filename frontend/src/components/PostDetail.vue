<template>
  <v-container style="width:75%">
    <v-row align="center" justify="center">
      <v-col cols="12" lg="10" class="mt-10 text-center">
        <p class="mywrap text-h4">{{ post.title }}</p>
        <p class="text-disabled">
          <span>{{ post.category }}</span>
          <span> | </span>
          <span>{{ post.modify_dt }}</span>
          <span> | </span>
          <a
            class="text-disabled text-decoration-none"
            href="mailto:suntail93@gmail.com"
          >
            {{ post.owner }}
          </a>
        </p>
      </v-col>
    </v-row>
    <v-row align="start" justify="center" >
      <v-col cols="12" sm="10" lg="10">
        <v-card class="pa-2" elevation="0">
          <p class="mywrap" v-html="post.content"></p>
          <div class="mt-5">
            <strong class="text-disabled">TAGS:</strong>
            <v-chip
              class="ma-2 text-disabled"
              v-for="(tag, index) in post.tags"
              :key="index"
              size="small"
              @click="serverPage(tag)"
              >{{ tag }}
            </v-chip>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="6" sm="5" lg="5">
        <v-card elevation="1" class="pa-2 mb-5" height="65px"
        v-if="prev" @click="fetchPostDetail(prev.id)" 
        tile hover>
          <p class="text-disabled"> &lt; prev </p>
          <p class="myword" v-html="prev.title"></p>
        </v-card>
      </v-col>
      <v-col cols="6" sm="5" lg="5" class="text-right">
        <v-card elevation="1" class="pa-2 mb-5" height="65px"
        v-if="next" @click="fetchPostDetail(next.id)"
        tile hover>
        <p class="text-disabled"> next &gt; </p>
        <p class="myword" v-html="next.title"></p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    post: {},
    prev: {},
    next: {},
  }),

  created() {
    console.log("created()...");
    const params = new URL(location).searchParams;
    const postId = params.get("id");
    this.fetchPostDetail(postId);
  },

  methods: {
    fetchPostDetail(postId) {
      console.log("fetchPostDetail()...", postId);
      axios
        .get(`/api2/post/${postId}/`)
        .then((res) => {
          console.log("POST DETAIL GET RES", res);
          this.post = res.data.post;
          this.prev = res.data.prevPost;
          this.next = res.data.nextPost;
        })
        .catch((err) => {
          console.log("POST DETAIL GET ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
          self.location = '/';
        });
    },

    serverPage(tagname) {
      console.log("serverPage()...", tagname);
      location.href = `/blog/post_list.html?tagname=${tagname}`;
    },
  },
};
</script>

<style scoped>
.mywrap {
  word-break: keep-all;
  white-space: pre-wrap;
}
.myword {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}
</style>
