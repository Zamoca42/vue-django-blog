import { reactive } from "vue";
import axios from "axios";

// using Reactive API
export const user = reactive({
  userid: 99,
  username: "Anonymous",

  getUserInfo() {
    console.log("user.getUserInfo()...");
    axios
      .get("/api/me/")
      .then((res) => {
        console.log("GETUSERINFO GET RES", res);
        // me.value = res.data;
        this.userid = res.data.id;
        this.username = res.data.username;
      })
      .catch((err) => {
        console.log("GETUSERINFO GET ERR.RESPONSE", err.response);
        alert(err.response.status + " " + err.response.statusText);
      });
  },
});
