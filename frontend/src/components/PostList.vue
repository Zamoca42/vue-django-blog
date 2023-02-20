<template>
  <v-container>
    <v-data-table :headers="headers" :items="posts" :items-per-page="5" :sort-by="[{ key: 'id', order: 'asc' }]"
      class="elevation-1" @click:row="serverPage">
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>
            Post List
            <span v-if="tagname" class="text-body-1 font-italic ml-3">(with {{ tagname }} tagged)</span>
          </v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-btn variant="tonal" color="blue-darken-4" @click.stop="dialogOpen('create', {})">
            New post
          </v-btn>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon size="small" class="me-2" @click.stop="dialogOpen('update', item.raw)">
          mdi-pencil
        </v-icon>
        <v-icon size="small" @click.stop="deletePost(item.raw)">
          mdi-delete
        </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="grey">
          No data exist
        </v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-toolbar dark color="blue-lighten-4">
          <v-toolbar-title>{{ formTitle }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn size="small" icon dark @click="cancel">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text>
          <v-form id="post-form" ref="postForm">
            <v-container>
              <v-row>
                <v-col cols="12" sm="2">
                  <v-text-field disabled variant="solo" label="id" v-model="editedItem.id"></v-text-field>
                </v-col>
                <v-col cols="12" sm="10">
                  <v-text-field variant="solo" label="title*" required v-model="editedItem.title"></v-text-field>
                </v-col>
                <v-col cols="12" sm="2">
                  <v-text-field disabled variant="solo" label="owner" v-model="editedItem.owner"></v-text-field>
                </v-col>
                <v-col cols="12" sm="10">
                  <v-text-field variant="solo" label="description" v-model="editedItem.description"></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea label="content" variant="solo" v-model="editedItem.content"></v-textarea>
                  <v-text-field variant="solo" label="tags" hint="comma separated tag names" persistent-hint
                   v-model="editedItem.tags"></v-text-field>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey-lighten-1" variant="outlined" @click="cancel">
            cancel
          </v-btn>
          <v-btn class="me-6" color="blue-darken-1" variant="outlined" @click="save">
            save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import axios from 'axios';
import { user } from './globals.js';

export default {
  setup() {
    return { user }
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
      document.getElementById('post-form').reset();
    },

    serverPage(e, { item }) {
      console.log("serverPage()...", item);
      location.href = `/blog/post_detail.html?id=${item.value}`;
    },

    createPost() {
      console.log("createPost()...", this.editedItem);
      const postData = new FormData();
      for (var key in this.editedItem) {
        postData.append(key, this.editedItem[key]);
      }

      axios
        .post("/api/post/create/", postData)
        .then((res) => {
          console.log("CREATE POST POST RES", res);
          this.posts.push(res.data);
        })
        .catch((err) => {
          console.log("CREATE POST POST ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
        });
    },

    updatePost() {
      console.log("updatePost()...", this.editedItem);
      const postData = new FormData();
      for (var key in this.editedItem) {
        postData.append(key, this.editedItem[key]);
      }
      postData.set("owner", this.user.userid);
      axios
        .post(`/api/post/${this.editedItem.id}/update/`, postData)
        .then((res) => {
          console.log("UPDATE POST POST RES", res);
          this.posts.splice(this.editedIndex, 1, res.data);
        })
        .catch((err) => {
          console.log("UPDATE POST POST ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
        });
    },

    deletePost(item) {
      console.log("deletePost()...", item, this.user);
      if (this.user.username === "Anonymous") {
        alert("Please login first !");
        return;
      }

      if (!confirm("Are you sure to delete ?")) return;
      axios
        .delete(`/api/post/${item.id}/delete/`)
        .then((res) => {
          console.log("DELETE POST DELETE RES", res);
          const index = this.posts.indexOf(item);
          this.posts.splice(index, 1);
        })
        .catch((err) => {
          console.log("DELETE POST DELETE ERR.RESPONSE", err.response);
          alert(err.response.status + " " + err.response.statusText);
        });
    },

  },
}
</script>

<style scoped>
.v-data-table :deep(tr.v-data-table__tr) :hover {
  cursor: pointer;
  background-color: #eee;
}
</style>
