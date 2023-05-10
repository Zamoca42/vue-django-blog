<template>
  <v-container fluid style="width: 1100px;">
    <v-row align="center" justify="center">
      <v-col cols="12" lg="10" class="mt-10 text-center">
        <p class="mywrap text-h4 font-weight-bold">{{ post.title }}</p>
        <p class="text-disabled mt-4">
          <span>{{ post.category }}</span>
          <span> | </span>
          <span>{{ post.create_dt }}</span>
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
      <v-col cols="12" sm="12" md="10" lg="10">
        <v-card class="pa-2" elevation="0" >
          <div class="markdown-body" v-html="sanitizedContent"></div>
          
          <div class="mt-5">  
            <div>
              <strong class="text-disabled">Last Modified at {{ post.modify_dt }}</strong>
            </div>
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
        v-if="prev" @click="$router.push({ name: 'Detail', params: { id: prev.id } })" 
        tile hover>
          <p class="text-disabled"> &lt; prev </p>
          <p class="myword ml-2" v-html="prev.title"></p>
        </v-card>
      </v-col>
      <v-col cols="6" sm="5" lg="5" class="text-right">
        <v-card elevation="1" class="pa-2 mb-5" height="65px"
        v-if="next" @click="$router.push({ name: 'Detail', params: { id: next.id } })"
        tile hover>
        <p class="text-disabled"> next &gt; </p>
        <p class="myword me-2" v-html="next.title"></p>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

</template>

<script>
import axios from "./index.js";
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import 'github-markdown-css/github-markdown-light.css'
import hljs from 'highlight.js/lib/core';
import javascript from 'highlight.js/lib/languages/javascript';
import python from 'highlight.js/lib/languages/python';
import plaintext from 'highlight.js/lib/languages/plaintext';
import bash from 'highlight.js/lib/languages/bash';
import json from 'highlight.js/lib/languages/json';
import 'highlight.js/styles/github.css';


hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('python', python);
hljs.registerLanguage('plaintext', plaintext);
hljs.registerLanguage('json', json);
hljs.registerLanguage('bash', bash);

export default {
  data: () => ({
    post: {},
    prev: {},
    next: {},
    markedContent: '',
  }),

  created() {
    const postId = this.$route.params.id;
    this.fetchPostDetail(postId);
  },

  watch: {
    $route(to, from) {
      if (to.params.id !== from.params.id) {
        this.fetchPostDetail(to.params.id);
      }
    }
  },
  
  computed: {
    sanitizedContent() {
      marked.setOptions({
        gfm: true,
        headerIds: false,
        tables: true,
        breaks: true,
        pedantic: false,
        smartLists: true,
        smartypants: false,
        highlight: function(code, lang) {
          if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
          } else {
            return hljs.highlight(code, { language: 'plaintext' }).value;
          }
        }
      });
      return DOMPurify.sanitize(marked(this.markedContent))
    }
  },

  methods: {
    fetchPostDetail(postId) {
      axios
        .get(`/api2/post/${postId}/`)
        .then((res) => {
          this.post = res.data.post;
          this.markedContent = this.post.content;
          this.prev = res.data.prevPost;
          this.next = res.data.nextPost;

          this.$nextTick(() => {
          window.scrollTo(0, 0); // Scroll to the top of the page
          });
        })
        .catch((err) => {
          console.log("POST DETAIL GET ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
        });
    },

    serverPage(tagname) {
      this.$router.push({ name: 'Blog', query: { tagname } });
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
.markdown-body {
  line-height: 1.7;
  color: #212529;
}
</style>
