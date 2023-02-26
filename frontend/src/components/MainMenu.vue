<template>
    <v-app-bar color="indigo" dark>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

        <v-toolbar-title>Zamoca.space</v-toolbar-title>
        <v-spacer></v-spacer>

        <v-btn variant="text" href="/home.html">Home</v-btn>
        <v-btn variant="text" href="/blog/post_list.html">Blog</v-btn>
        <template v-if="user.username === 'Anonymous'">
        </template>
        <template v-else>
            <v-btn variant="text" href="/admin/">Admin</v-btn>
        </template>

        <v-spacer></v-spacer>
        <v-menu location="bottom">
            <template v-slot:activator="{ props }">
                <v-btn variant="text" v-bind="props">
                    <v-icon>mdi-account</v-icon>{{ user.username }}
                    <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
            </template>

            <v-list>
                <template v-if="user.username === 'Anonymous'">
                    <v-list-item @click="dialogOpen('login')">
                        <v-list-item-title>Login</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="dialogOpen('register')">
                        <v-list-item-title>Register</v-list-item-title>
                    </v-list-item>
                </template>
                <template v-else>
                    <v-list-item @click="logout">
                        <v-list-item-title>Logout</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="dialogOpen('pwdchg')">
                        <v-list-item-title>Password change</v-list-item-title>
                    </v-list-item>
                </template>
            </v-list>
        </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app clipped>
        <v-list density="compact">
            <v-list-subheader>drawer menu</v-list-subheader>

            <v-list-item v-for="(item, i) in items" :key="i" :value="item" active-color="primary">
                <template v-slot:prepend>
                    <v-icon :icon="item.icon"></v-icon>
                </template>

                <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>

    // login dialog
    <v-dialog v-model="dialog.login">
        <v-sheet width="400" hheight="600" class="mx-auto">
            <v-toolbar dark color="primary">
                <v-toolbar-title>Login form</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn size="small" icon dark @click="cancel('login')">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-toolbar>

            <v-container class="mb-10">
                <v-form id="login-form" ref="loginForm">
                    <v-row justify="center">
                        <v-col cols="10">
                            <v-text-field label="username" name="username" required>
                            </v-text-field>
                            <v-text-field class="mt-n4 mb-n6" label="password" type="password" required
                                name="password"></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-btn color="bg-grey-lighten-1" variant="tonal" size="small" class="me-4" @click="reset('login')">
                            Reset
                        </v-btn>
                        <v-btn color="primary" variant="tonal" size="small" @click="save('login')">
                            Login
                        </v-btn>
                    </v-row>
                </v-form>

                <div class="text-center mt-8 mb-8">&mdash; or &mdash;</div>

                <v-row justify="center">
                    <div class="mb-2">
                        <v-btn color="#1c407c" small class="text-none text-white" width="250">
                            <v-icon>mdi-facebook</v-icon>
                            &ensp; Continue with Facebook
                        </v-btn>
                    </div>
                    <div class="mb-2">
                        <v-btn color="#da3d29" small class="text-none text-white" width="250">
                            <v-icon>mdi-google</v-icon>
                            &ensp; Continue with Google
                        </v-btn>
                    </div>
                    <div class="mb-2">
                        <v-btn color="#03c75a" small class="text-none" width="250">
                            <img src="/naver_my2.png" width="120" />
                        </v-btn>
                    </div>
                    <div>
                        <v-btn color="#FEE500" small class="text-none" width="250">
                            <img src="/kakao_my1.png" width="190" />
                        </v-btn>
                    </div>
                </v-row>

            </v-container>
        </v-sheet>
    </v-dialog>

    // register dialog
    <v-dialog v-model="dialog.register">
        <v-sheet width="400" hheight="600" class="mx-auto">
            <v-toolbar dark color="success">
                <v-toolbar-title>Register form</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn size="small" icon dark @click="cancel('register')">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-toolbar>

            <v-container class="mb-10">
                <v-form id="register-form" ref="registerForm">
                    <v-row justify="center">
                        <v-col cols="10">
                            <v-text-field label="username" name="username" required>
                            </v-text-field>
                            <v-text-field class="mt-n4" label="password" type="password" required
                                name="password1"></v-text-field>
                            <v-text-field class="mt-n4 mb-n6" label="password again" type="password" required
                                name="password2"></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-btn color="bg-grey-lighten-1" variant="tonal" size="small" class="me-4"
                            @click="reset('register')">
                            Reset
                        </v-btn>
                        <v-btn color="primary" variant="tonal" size="small" @click="save('register')">
                            Register
                        </v-btn>
                    </v-row>
                </v-form>

                <div class="text-center mt-8 mb-8">&mdash; or &mdash;</div>

                <v-row justify="center">
                    <div class="mb-2">
                        <v-btn color="#1c407c" small class="text-none text-white" width="250">
                            <v-icon>mdi-facebook</v-icon>
                            &ensp; Continue with Facebook
                        </v-btn>
                    </div>
                    <div class="mb-2">
                        <v-btn color="#da3d29" small class="text-none text-white" width="250">
                            <v-icon>mdi-google</v-icon>
                            &ensp; Continue with Google
                        </v-btn>
                    </div>
                    <div class="mb-2">
                        <v-btn color="#03c75a" small class="text-none" width="250">
                            <img src="/naver_my2.png" width="120" />
                        </v-btn>
                    </div>
                    <div>
                        <v-btn color="#FEE500" small class="text-none" width="250">
                            <img src="/kakao_my1.png" width="190" />
                        </v-btn>
                    </div>
                </v-row>

            </v-container>
        </v-sheet>
    </v-dialog>

    // pwdchg dialog
    <v-dialog v-model="dialog.pwdchg">
        <v-sheet width="400" hheight="600" class="mx-auto">
            <v-toolbar dark color="warning">
                <v-toolbar-title>Password change form</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-btn size="small" icon dark @click="cancel('pwdchg')">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-toolbar>

            <v-container class="mb-10">
                <v-form id="pwdchg-form" ref="pwdchgForm">
                    <v-row justify="center">
                        <v-col cols="10">
                            <v-text-field cclass="mt-n4 mb-n6" label="old password" type="password" required
                                name="old_password"></v-text-field>
                            <v-text-field cclass="mt-n4 mb-n6" label="new password" type="password" required
                                name="new_password1"></v-text-field>
                            <v-text-field cclass="mt-n4 mb-n6" label="new password again" type="password" required
                                name="new_password2"></v-text-field>
                        </v-col>
                    </v-row>

                    <v-row justify="center">
                        <v-btn color="bg-grey-lighten-1" variant="tonal" size="small" class="me-4" @click="reset('pwdchg')">
                            Reset
                        </v-btn>
                        <v-btn color="primary" variant="tonal" size="small" @click="save('pwdchg')">
                            Password change
                        </v-btn>
                    </v-row>
                </v-form>
            </v-container>

        </v-sheet>
    </v-dialog>
</template>
  
<script>
import axios from 'axios';
import { user } from './globals.js';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
    setup() {
        return { user }
    },

    data: () => ({
        drawer: null,
        items: [
            { text: 'Dashboard', icon: 'mdi-view-dashboard' },
            { text: 'Settings', icon: 'mdi-cog' },
            { text: 'Real-Time', icon: 'mdi-clock' },
            { text: 'Audience', icon: 'mdi-account' },
            { text: 'Conversions', icon: 'mdi-flag' },
        ],
        dialog: {
            login: false,
            register: false,
            pwdchg: false,
        },
    }),

    created() {
        console.log("created(MainMenu.vue)...");
        this.user.getUserInfo();
    },

    mounted() {
        console.log("mounted()...");
    },

    methods: {
        dialogOpen(kind) {
            console.log("dialogOpen()...", kind);
            if (kind === "login") {
                this.dialog.login = true;
            } else if (kind === "register") {
                this.dialog.register = true;
            } else if (kind === "pwdchg") {
                this.dialog.pwdchg = true;
            }
        },
        cancel(kind) {
            console.log("cancel()...", kind);
            if (kind === "login") {
                this.dialog.login = false;
                this.$refs.loginForm.reset();
            } else if (kind === "register") {
                this.dialog.register = false;
                this.$refs.registerForm.reset();
            } else if (kind === "pwdchg") {
                this.dialog.pwdchg = false;
                this.$refs.pwdchgForm.reset();
            }
        },

        save(kind) {
            console.log("save()...", kind);
            if (kind === "login") {
                this.login();
                this.dialog.login = false;
                this.$refs.loginForm.reset();
            } else if (kind === "register") {
                this.register();
                this.dialog.register = false;
                this.$refs.registerForm.reset();
            } else if (kind === "pwdchg") {
                this.pwdchg();
                this.dialog.pwdchg = false;
                this.$refs.pwdchgForm.reset();
            }
        },

        reset(kind) {
            console.log("reset()...", kind);
            if (kind === "login") {
                this.$refs.loginForm.reset();
            } else if (kind === "register") {
                this.$refs.registerForm.reset();
            } else if (kind === "pwdchg") {
                this.$refs.pwdchgForm.reset();
            }
        },

        login() {
            console.log("login()...");
            const postData = new FormData(document.getElementById("login-form"));
            axios
                .post("/api/login/", postData)
                .then((res) => {
                    console.log("LOGIN POST RES", res);
                    this.user.userid = res.data.id;
                    this.user.username = res.data.username;
                })
                .catch((err) => {
                    console.log("LOGIN POST ERR.RESPONSE", err.response);
                    alert("login NOK");
                });
        },

        register() {
            console.log("register()...");
            const postData = new FormData(document.getElementById("register-form"));
            axios
                .post("/api/register/", postData)
                .then((res) => {
                    console.log("REGISTER POST RES", res);
                    alert(`user ${res.data.username} created OK`);
                })
                .catch((err) => {
                    console.log("REGISTER POST ERR.RESPONSE", err.response);
                    alert("register NOK");
                });
        },

        logout() {
            console.log("logout()...");
            axios
                .get("/api/logout/")
                .then((res) => {
                    console.log("LOGOUT GET RES", res);
                    alert(`user ${this.user.username} logout OK`);
                    this.user.username = 'Anonymous';
                })
                .catch((err) => {
                    console.log("LOGOUT GET ERR.RESPONSE", err.response);
                    alert("logout NOK");
                });
        },

        pwdchg() {
            console.log("pwdchg()...");
            const postData = new FormData(document.getElementById("pwdchg-form"));
            axios
                .post("/api/pwdchg/", postData)
                .then((res) => {
                    console.log("PWDCHG POST RES", res);
                    alert(`user ${this.me.username} password change OK`);
                })
                .catch((err) => {
                    console.log("PWDCHG POST ERR.RESPONSE", err.response);
                    alert("password change NOK");
                });
        },
    },
}
</script>
